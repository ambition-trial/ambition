import os
from pathlib import PurePath

from edc_device.constants import CENTRAL_SERVER
from edc_fabric.fabfile.environment import bootstrap_env, update_fabric_env
from edc_fabric.fabfile.files import mount_dmg_locally, dismount_dmg_locally, mount_dmg
from edc_fabric.fabfile.mysql import install_protocol_database
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.utils import launch_webserver
from edc_fabric.fabfile.virtualenv.tasks import activate_venv
from fabric.api import task, run, warn, cd, env, local, lcd, put
from fabric.colors import yellow, blue, red
from fabric.contrib.files import exists, sed
from fabric.contrib.project import rsync_project
from fabric.operations import sudo
from fabric.utils import abort

from .prepare_env import prepare_env


@task
def validate(release=None, pull=None):
    """
        fab -H mmathethe utils.validate:release=0.1.24 --user=django
    """
    result = run('workon ambition', warn_only=True)
    if result:
        warn(yellow(f'{env.host}: {result}'))
    else:
        result = run('workon ambition && python --version', warn_only=True)

        if result != 'Python 3.6.2':
            warn(yellow(f'{env.host}: {result}'))
        else:
            with cd('~/source/ambition'):
                result = run('git tag')
                if release not in result:
                    result = run('git describe --abbrev=0 --tags')
                    warn(
                        yellow(f'{env.host}: ambition tag not found. Got {result}'))
                    if pull:
                        run('git pull')
            result = run('curl http://localhost')
            if 'Bad Gateway' in result:
                warn(yellow(f'{env.host}: bad gateway'))
            else:
                result = run(
                    'curl http://localhost/static/ambition/label_templates/aliquot.lbl')
                if '404 Not Found' in result:
                    warn(yellow(f'{env.host}: 404 Not Found'))
                else:
                    if not exists('~/media/edc_map') or not exists('~/media/transactions'):
                        warn(yellow(f'{env.host}: Media folder not ready'))
                    else:
                        warn(blue(f'{env.host}: OK'))


@task
def restore_media_folder(bootstrap_path=None, bootstrap_branch=None, use_local_fabric_conf=True):
    """Restores media/edc_map from the external backup

    For example:

        fab -P -R mmankgodi utils.restore_media_folder:bootstrap_path=/Users/django/source/ambition/fabfile/conf/,bootstrap_branch=develop,use_local_fabric_conf=True --user=django
    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)

    update_fabric_env(use_local_fabric_conf=use_local_fabric_conf)

    local_dir = '/Volumes/BONTSI/Village\ Maps/mmankgodi\ maps/media/edc_map'

    remote_dir = os.path.join('~/media/edc_map')

    if exists(remote_dir):
        run(f'rm -rf {remote_dir}', warn_only=True)
    run(f'mkdir -p {remote_dir}', warn_only=True)

    rsync_project(local_dir=local_dir, remote_dir=remote_dir)


@task
def install_protocol_database_task(bootstrap_path=None, bootstrap_branch=None,
                                   release=None, map_area=None, skip_backup=None):
    """Overwrites the client DB.

    For example:

        fab -P -R lentsweletau deploy.install_protocol_database_task:bootstrap_path=/Users/erikvw/source/ambition/fabfile/conf/,release=,map_area=

    """
    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)
    if not release:
        abort('release not specified')
    if not map_area:
        abort('map_area not specified')

    update_fabric_env()

    install_protocol_database(skip_backup=skip_backup,
                              release=release, map_area=map_area)


def update_ambition_conf(project_conf=None, map_area=None):
    """Updates the ambition.conf file on the remote host.
    """
    project_conf = project_conf or env.project_conf
    map_area = map_area or env.map_area
    remote_copy = os.path.join(env.etc_dir, project_conf)
    if not exists(env.etc_dir):
        sudo('mkdir {etc_dir}'.format(etc_dir=env.etc_dir))
    sed(remote_copy, 'map_area \=.*',
        'map_area \= {}'.format(map_area or ''),
        use_sudo=True)


# @task
# def change_map_area_task(map_area=None, bootstrap_path=None, bootstrap_branch=None):
#     """Change a remote host's map area and restart web.
#
#     For example:
#
#         fab -H ambition057 utils.change_map_area_task:bootstrap_path=/Users/erikvw/source/ambition/fabfile/conf/,bootstrap_branch=develop,map_area=mmankgodi --user=django
#
#     """
#     bootstrap_env(
#         path=bootstrap_path,
#         filename='bootstrap_client.conf',
#         bootstrap_branch=bootstrap_branch)
#
#     update_fabric_env()
#
#     update_ambition_conf(map_area=map_area)
#
#     launch_webserver()
#
#
# def list_tags_from(pip_file=None):
#     data = {}
#     with open(os.path.expanduser(pip_file), 'r') as f:
#         lines = f.readlines()
#         for line in lines:
#             print(line)
#             package, tag = line.split('==')
#             data.update({package.strip(): tag.strip()})
#     return data


@task
def query_tx_task(**kwargs):
    """Check for any host with pending transactions.

    fab -P -R mmankgodi utils.query_tx_task:bootstrap_path=/Users/erikvw/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    # run('brew services restart mysql', quiet=True)
    run('mysql -uroot -p edc -Bse \'select  count(*) '
        'from django_offline_outgoingtransaction where is_consumed_server=0;\' > /tmp/stats1.txt')
    result = run('cat /tmp/stats1.txt')
    if result != '0':
        warn(red(f'{env.host}: pending {result}'))

    run(
        'mysql -uroot -p edc -Bse \'select count(*) '
        'from django_offline_files_history '
        'where sent=0;\' > /tmp/stats2.txt')
    result = run('cat /tmp/stats2.txt')
    if result != '0':
        warn(red(f'{env.host}: unsent {result}'))


@task
def generate_anonymous_transactions(**kwargs):
    """Generate anonymous transactions.

    fab -P -R mmathethe utils.generate_anonymous_transactions:bootstrap_path=/Users/imosweu/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    transactions_path = os.path.join(env.media_root, 'transactions/tmp/')

    enrollment_checklist_file = (
        f'{transactions_path}{env.host}_member_enrollmentchecklistanonymous.txt')
    historical_enrollment_file = (
        f'{transactions_path}{env.host}_member_historicalenrollmentchecklistanonymous.txt')

    if exists(f'{enrollment_checklist_file}'):
        run(f'rm {enrollment_checklist_file}')

    run("mysql -uroot -p edc -Bse \"SELECT * INTO OUTFILE "
        f"'{enrollment_checklist_file}' "
        "CHARACTER SET UTF8 "
        "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
        "LINES TERMINATED BY '\\n' "
        "FROM member_enrollmentchecklistanonymous;\" ")

    enrollment_result = run(
        f'cat {enrollment_checklist_file}')
    if not enrollment_result:
        warn(red(f'{env.host}: transactions not generated'))

    if exists(
            f'{historical_enrollment_file}'):
        run(
            f'rm {historical_enrollment_file}')

    run("mysql -uroot -p edc -Bse \"SELECT * INTO OUTFILE "
        f"'{historical_enrollment_file}' "
        "CHARACTER SET UTF8 "
        "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
        "LINES TERMINATED BY '\\n' "
        "FROM member_historicalenrollmentchecklistanonymous; \"")

    historical_result = run(
        f'cat {historical_enrollment_file}')
    if not historical_result:
        warn(red(f'{env.host}: transactions not generated'))

    local_transaction_path = os.path.join(
        env.media_root, 'transactions/pending/')
    local(
        f'scp django@{env.host}:{transactions_path}*.txt  {local_transaction_path}')


@task
def verify_deployment_db(**kwargs):
    """Generate anonymous transactions.

    fab -P -R mmathethe utils.verify_deployment_db:bootstrap_path=/Users/imosweu/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    run("mysql -uroot -p edc -Bse \"SELECT COUNT(*) from information_schema.tables "
        "where TABLE_SCHEMA='edc';\"")


def get_pip_freeze_list_from_requirements(requirements_file=None):
    package_names = []
    with cd(env.project_repo_root):
        data = run('cat {requirements}'.format(
            requirements=requirements_file))
        data = data.split('\n')
        for line in data:
            if 'botswana-harvard' in line or 'erikvw' in line:
                repo_url = line.split('@')[0].replace('git+', '')
                tag = line.split('@')[1].split('#')[0]
                package = get_repo_name(repo_url) + '==' + tag
                package_names.append(package)
    return package_names


@task
def import_anonymous_transactions(**kwargs):
    """Import anonymous transactions.

    fab -P -R mmathethe utils.import_anonymous_transactions:bootstrap_path=
        /Users/tsetsiba/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    transactions_path = os.path.join(env.media_root, 'transactions/pending/')
    for filename in os.listdir(transactions_path):
        transactions_path = os.path.join(transactions_path, filename)
        if filename.endswith('_member_enrollmentchecklistanonymous.txt'):
            result = run(
                "mysql -uroot -p edc -Bse \"LOAD DATA LOCAL INFILE "
                f"'{transactions_path}' "
                f"INTO TABLE member_enrollmentchecklistanonymous "
                "CHARACTER SET UTF8 "
                "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
                "LINES TERMINATED BY '\\n' "
            )
            if not result:
                warn(red(f'{transactions_path} not imported'))
        else:
            result = run(
                "mysql -uroot -p edc -Bse \"LOAD DATA LOCAL INFILE "
                f"'{transactions_path}' "
                f"INTO TABLE member_historicalenrollmentchecklistanonymous "
                "CHARACTER SET UTF8 "
                "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
                "LINES TERMINATED BY '\\n' "
            )
            if not result:
                warn(red(f'{transactions_path} not imported'))


@task
def check_repo_status(expected_tag=None, **kwargs):
    """Check repo tag.

    fab -P -R mmathethe utils.check_repo_status:bootstrap_path=/Users/imosweu/source/ambition/fabfile/conf/,expected_tag=0.1.47  --user=django

    """

    prepare_env(**kwargs)

    with cd(os.path.join(env.remote_source_root, env.project_repo_name)):
        if exists('env_dependencies.txt'):
            run('rm env_dependencies.txt')
        run('git checkout master')
        run('source ~/.venvs/ambition/bin/activate && pip freeze > env_dependencies.txt')
        result = run('git describe --tags')
        if result != expected_tag:
            warn(red(f'master is not at {expected_tag}'))
        data = run('cat env_dependencies.txt')
        data = [d[:-1] for d in data.split('\n')]
        requirements_list = get_pip_freeze_list_from_requirements(
            requirements_file=env.requirements_file)
        for requirement in requirements_list:
            if requirement not in data:
                warn(red(f'{requirement} is not in {env.host}'))


@task
def load_keys_ambition(device_role=None, **kwargs):
    """Load keys for project.

    fab -H ambition010 utils.load_keys_ambition:bootstrap_path=
        /Users/imosweu/source/ambition/fabfile/conf/,device_role=Client  --user=django

    """

    prepare_env(**kwargs)
    # mount dmg
    if device_role == CENTRAL_SERVER:
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


@task
def install_dependency_specific_tag(dependency=None, tag=None, account=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H ambition010 utils.install_dependency_specific_tag:bootstrap_path=
        /Users/imosweu/source/ambition/fabfile/conf/,dependency=ambition-subject,tag=0.1.22  --user=django

    """
    if not account:
        account = 'botswana-harvard'
    egg = '_'.join(dependency.split('-'))
    prepare_env(**kwargs)
    with cd(env.project_repo_root):
        run(f'source {activate_venv()} && pip uninstall {dependency}',
            warn_only=True)
        run(f'pip install git+https://github.com/{account}/'
            f'{dependency}.git@{tag}#egg={egg}')


@task
def install_dependency_not_in_requirements(dependency=None, tag=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H ambition010 utils.install_dependency_not_in_requirements:bootstrap_path=
        /Users/imosweu/source/ambition/fabfile/conf/,dependency=ambition-subject,tag=0.1.22  --user=django

    """
    prepare_env(**kwargs)
    with cd(env.project_repo_root):
        run(f'source {activate_venv()} && pip uninstall {dependency}',
            warn_only=True)
        run(f'source {activate_venv()} && pip install {dependency}=={tag}')


@task
def remove_old_sync_files(verify=None, **kwargs):
    """Install a dependency with a specific tag.

    fab -H ambition010 utils.remove_old_sync_files:bootstrap_path=
        /Users/imosweu/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    with cd('~/static/'):
        if not verify:
            if exists('django_offline'):
                run('rm -rf django_offline')
            if exists('django_offline_files'):
                run('rm -rf django_offline_files')
        else:
            if not exists('django_offline') or not exists('django_offline_files'):
                print(
                    blue('Missing django_offline and django_offline_files,'
                         ' folders do not exist.'))


@task
def load_containers_task(bootstrap_path=None, bootstrap_branch=None,
                         map_area=None, file_path=None):
    """Loads containers into the database.

    For example:

        fab -P -R lentsweletau utils.load_containers_task:bootstrap_path=
            /Users/imosweu/source/ambition/fabfile/conf/,file_path=,map_area=

    """

    bootstrap_env(
        path=bootstrap_path,
        filename='bootstrap_client.conf',
        bootstrap_branch=bootstrap_branch)
    if not map_area:
        abort('map_area not specified')

    update_fabric_env()

    with cd(env.project_repo_root):
        run(f'source {activate_venv()} &&  python manage.py'
            f' load_containers {file_path}{map_area}container.json edc_map.container')
        run(f'source {activate_venv()} &&  python manage.py'
            f' load_containers {file_path}{map_area}inner_container.json'
            ' edc_map.innercontainer')


@task
def add_missing_db_column(**kwargs):
    """Add missing DB column.

    fab -P -R mmathethe utils.add_missing_db_column:bootstrap_path=
        /Users/imosweu/source/ambition/fabfile/conf/  --user=django

    """
    prepare_env(**kwargs)

    run("mysql -uroot -p edc -Bse \"alter table edc_lab_result"
        " add column device_created varchar(10) NULL;\"")

    run("mysql -uroot -p edc -Bse \"alter table edc_lab_result"
        " add column device_modified varchar(10) NULL;\"")


@task
def ssh_copy_id(bootstrap_path=None, use_local_fabric_conf=None, bootstrap_branch=None):
    """
    Example:
        fab -R testhosts -P deploy.ssh_copy_id:config_path=
            /Users/erikvw/source/ambition/fabfile/,bootstrap_branch=develop,local_fabric_conf=True --user=django
    """

    bootstrap_env(
        path=os.path.expanduser(bootstrap_path),
        bootstrap_branch=bootstrap_branch)
    update_fabric_env(use_local_fabric_conf=use_local_fabric_conf)
    pub_key = local('cat ~/.ssh/id_rsa.pub', capture=True)
    with cd('~/.ssh'):
        run('touch authorized_keys')
        result = run('cat authorized_keys', quiet=True)
        if pub_key not in result:
            run('cp authorized_keys authorized_keys.bak')
            run(f'echo {pub_key} >> authorized_keys')


@task
def launch_webserver_ambition_task(**kwargs):
    """Add missing DB column.

    fab -P -R mmathethe utils.launch_webserver_ambition_task:target_os=Darwin --user=django

    """
    prepare_env(**kwargs)
    launch_webserver()
