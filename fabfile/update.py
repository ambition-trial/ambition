import os

from fabric.api import cd, env, prefix
from fabric.decorators import serial, task

from .freeze import _pip_freeze
from .gunicorn import restart_gunicorn
from .migrate import migrate
from .utils import set_fab_env
from .virtual_env import update_virtualenv

"""
fab update:user=uat
fab update:user=ambition
"""


with open(os.path.expanduser(
        '~/source/ambition-edc/fabfile/.hosts'), 'r') as f:
    env.hosts = f.readlines()


@serial
@task
def update(user=None):
    """Update virtualenv, migrate and update permissions.
    """
    set_fab_env(user)
    with prefix(env.activate):
        with cd(env.app_folder):
            update_virtualenv(user)
            migrate(user)
            _pip_freeze()
    restart_gunicorn(user)
