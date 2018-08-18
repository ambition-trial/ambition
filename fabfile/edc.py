import os

from fabric.api import cd, env, run, prefix
from contextlib import contextmanager as _contextmanager

"""
fab -P update:user=ambition
"""

with open(os.path.expanduser(
        '~/source/ambition-edc/fabfile/.hosts'), 'r') as f:
    env.hosts = f.readlines()


@_contextmanager
def virtualenv():
    with prefix(env.activate):
        yield


def update(user=None):
    env.user = user
    env.app_folder = f'/home/{env.user}/app'
    env.activate = 'source ~/.venvs/ambition/bin/activate'
    with virtualenv():
        with cd(env.app_folder):
            run('git checkout master')
            run('git pull')
            run('pip install -U -r requirements/stable.txt --no-cache-dir')
            run('python manage.py migrate')
            run('python manage.py update_edc_permissions')
