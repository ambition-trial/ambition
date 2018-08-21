from fabric.api import cd, env, run, prefix, local
from fabric.decorators import hosts, task

from .gunicorn import restart_gunicorn
from .utils import set_fab_env


@task
def update_virtualenv(user=None):
    set_fab_env(user)
    with prefix(env.activate):
        with cd(env.app_folder):
            run('git checkout master')
            run('git pull')
            run('pip install -U -r requirements/stable.txt --no-cache-dir')
    restart_gunicorn(user)


@task
@hosts('localhost')
def update_develop_virtualenv():
    """Create or recreate a virtualenv installing as editable
    my locally clones repos (on develop branch).
    """
    activate = 'source ~/.venvs/ambition/bin/activate'
    app_folder = '~/source/ambition-edc'
    source_folder = '~/source'
    requirements_file = f'{app_folder}/requirements/develop.txt'
    venv_folder = '~/.venvs/ambition'
    local(f'rm -rf {venv_folder}')
    local(f'python3 -m venv {venv_folder}')
    with prefix(activate):
        with cd(app_folder):
            local('git checkout develop')
            local('git pull')
            local(f'pip install -U -r {requirements_file} --no-cache-dir')
            # uninstall those installed via setup
            apps = [
                'edc-auth',
                'edc-appointment',
                'edc-constants',
                'edc-device',
                'edc-identifier',
                'edc-lab',
                'edc-list-data',
                'edc-metadata-rules',
                'edc-model-admin',
                'edc-model-fields',
                'edc-model-wrapper',
                'edc-navbar',
                'edc-protocol',
                'edc-reports',
                'edc-rest',
                'edc-search',
                'edc-subject-dashboard',
                'edc-timepoint',
                'edc-visit-schedule',
                'edc-visit-tracking',
                'edc-selenium',
                'ambition-prn',
                'ambition-rando',
                'ambition-reference',
                'ambition-screening',
                'ambition-sites',
                'ambition-subject',
                'ambition-validators',
                'ambition-visit-schedule',
                'django-crypto-fields',
                'django-revision',
                'django-collect-offline',
                'django-collect-offline-files',
            ]
            for app in apps:
                local(f'pip uninstall -y {app}')
                local(
                    f'pip install -U -e {source_folder}/{app} --no-cache-dir')
            local(
                f'pip install -U pip ipython setuptools wheel twine '
                f'edc-selenium coverage Fabric3 --no-cache-dir')
            local(
                f'pip install -U git+https://github.com/PyCQA/flake8.git --no-cache-dir')
