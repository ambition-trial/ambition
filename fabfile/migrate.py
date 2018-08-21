from fabric.api import cd, env, run, prefix
from fabric.decorators import task

from .utils import set_fab_env
from .virtual_env import update_virtualenv


"""

fab migrate:user=ambition
fab migrate:user=uat

"""


@task
def migrate(user=None):
    """Run migrations and refresh permissions.

    Run once each for live and uat.
    """
    set_fab_env(user)
    with prefix(env.activate):
        with cd(env.app_folder):
            update_virtualenv(user)
            run('python manage.py migrate')
            run('python manage.py update_edc_permissions')
            # run('python manage.py collectstatic')
