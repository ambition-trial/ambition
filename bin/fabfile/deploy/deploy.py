import os

from fabric.api import env, put, sudo, cd, run, warn, prefix, lcd, task
from fabric.contrib.files import exists
from fabric.utils import abort

from edc_device.constants import CENTRAL_SERVER

from edc_fabric.fabfile import (
    update_fabric_env, create_venv,
    install_mysql, install_protocol_database)
from edc_fabric.fabfile.brew import update_brew_cache
from edc_fabric.fabfile.conf import put_project_conf
from edc_fabric.fabfile.constants import MACOSX, LINUX
from edc_fabric.fabfile.files import mount_dmg_locally, dismount_dmg_locally, mount_dmg
from edc_fabric.fabfile.gunicorn import install_gunicorn
from edc_fabric.fabfile.nginx import install_nginx
from edc_fabric.fabfile.pip import pip_install_from_cache
from edc_fabric.fabfile.python import install_python3
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import (
    update_settings, rsync_deployment_root,
    bootstrap_env, put_bash_config, launch_webserver)
from edc_fabric.fabfile.virtualenv import activate_venv

from ..utils import update_ambition_conf


def deploy(requirements_list=None, conf_filename=None, bootstrap_path=None, release=None, map_area=None, user=None,
           bootstrap_branch=None, skip_update_os=None, skip_db=None, skip_restore_db=None, skip_repo=None,
           skip_venv=None, skip_mysql=None, skip_python=None, skip_web=None, update=None, current_tag=None,
           skip_collectstatic=None, skip_bash_config=None, skip_keys=None, work_online=None, specific_tag=None):

    bootstrap_env(
        path=bootstrap_path,
        filename=conf_filename,
        bootstrap_branch=bootstrap_branch)
    if not release:
        abort('Specify the release')
    if not map_area:
        abort('Specify the map_area')

    env.project_release = release
    env.map_area = map_area

    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)

    rsync_deployment_root()

    if update:
        env.fabric_config_path = os.path.expanduser(os.path.join(
            '/Users/django/source', env.project_repo_name, 'fabfile/conf', env.fabric_conf))
        update_fabric_env()

        for package in requirements_list:
            run(f'source {activate_venv()} && pip3 uninstall {package}', warn_only=True)
            pip_install_from_cache(
                package_name=package, venv_name=env.venv_name)

        if not skip_repo:
            put_ambition_repo()

    else:
        update_fabric_env()
        if not skip_update_os:
            if env.target_os == MACOSX:
                update_brew_cache(no_auto_update=True)
            elif env.target_os == LINUX:
                sudo('apt-get update')

        if not skip_bash_config:
            put_bash_config()

        if not exists(os.path.join(env.remote_source_root, env.project_repo_name)):
            run('mkdir -p {remote_source_root}'.format(
                remote_source_root=env.remote_source_root), warn_only=True)

        if not skip_repo:
            put_ambition_repo()

        # make static and media
        if not exists(env.static_root):
            run('mkdir {static_root}'.format(
                static_root=env.static_root), warn_only=True)
        if not exists(env.media_root):
            run('mkdir {media_root}'.format(
                media_root=env.media_root), warn_only=True)

        if not skip_mysql:
            install_mysql()

        if not skip_python:
            install_python3()

        if not skip_venv:
            with cd(os.path.join(env.project_repo_root)):
                if specific_tag:
                    run(f'git checkout {release}')
            create_venv(work_online=work_online)

        if not skip_web:
            if env.log_root and exists(env.log_root):
                sudo('rm -rf {log_root}'.format(log_root=env.log_root),
                     warn_only=True)
            run('mkdir -p {log_root}'.format(log_root=env.log_root))
            install_nginx(skip_bootstrap=True)
            install_gunicorn(work_online=work_online)

        if not skip_keys:
            # crypto_keys DMG into etc/{project_app_name}/
            put(os.path.expanduser(os.path.join(env.fabric_config_root, 'etc', env.dmg_filename)),
                env.etc_dir,
                use_sudo=True)


    # copy ambition.conf into etc/{project_app_name}/
    put_project_conf()
    update_ambition_conf

    with cd(os.path.join(env.project_repo_root)):
        if specific_tag:
            run(f'git checkout {release}')
        else:
            run('git checkout master')

    # mount dmg
    if env.device_role == CENTRAL_SERVER:
        mount_dmg_locally(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                          dmg_passphrase=env.crypto_keys_passphrase)
        if not exists(env.key_path):
            sudo(f'mkdir -p {env.key_path}')
        with lcd(env.key_volume):
            put(local_path='user*',
                remote_path=f'{env.key_path}/', use_sudo=True)
        dismount_dmg_locally(volume_name=env.key_volume)
    else:
        mount_dmg(dmg_path=env.etc_dir, dmg_filename=env.dmg_filename,
                  dmg_passphrase=env.crypto_keys_passphrase)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        if specific_tag:
            run(f'git checkout {release}')
        else:
            run('git checkout master')
            result = run(
                'git diff --name-status master..{release}'.format(release=release))
            if result:
                warn('master is not at {release}'.format(release=release))

    update_settings()

    if not skip_db:
        run('brew services stop mysql', warn_only=True)
        run('brew services start mysql')
    if not skip_restore_db:
        install_protocol_database(skip_backup=True)

    if not skip_collectstatic:
        with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
            with prefix(f'source {activate_venv()}'.format(venv_name=env.venv_name)):
                run('python manage.py collectstatic')
                run('python manage.py collectstatic_js_reverse')

    launch_webserver()


def put_ambition_repo():
    # copy repo from deployment to source
    destination = env.remote_source_root
    if not exists(destination):
        run('mkdir -p {destination}'.format(destination=destination))
    run('rsync -pthrvz --delete {source} {destination}'.format(
        source=os.path.join(env.deployment_root, env.project_appname),
        destination=destination))
