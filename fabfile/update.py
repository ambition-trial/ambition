import os

from fabric.api import cd, env, run, prefix
from fabric.decorators import serial

from .freeze import _pip_freeze

"""
fab -H localhost local_freeze:version=0.1.20

fab update:user=ambition
"""


with open(os.path.expanduser(
        '~/source/ambition-edc/fabfile/.hosts'), 'r') as f:
    env.hosts = f.readlines()


@serial
def update(user=None):
    env.user = user
    env.migrate = True
    env.update_permissions = True
    env.app_folder = f'/home/{env.user}/app'
    env.local_app_folder = '~/source/ambition-edc'
    env.activate = 'source ~/.venvs/ambition/bin/activate'
    with prefix(env.activate):
        with cd(env.app_folder):
            run('git checkout master')
            run('git pull')
            run('pip install -U -r requirements/stable.txt --no-cache-dir')
            if env.migrate:
                run('python manage.py migrate')
                env.migrate = False
            if env.update_permissions:
                run('python manage.py update_edc_permissions')
                env.update_permissions = False
            _pip_freeze()
