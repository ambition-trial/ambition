from fabric.decorators import task
from fabric.operations import sudo
from fabric.api import env


@task
def restart_gunicorn(user):
    env.user = user
    sudo('systemctl daemon-reload')
    sudo('systemctl restart gunicorn')
    sudo('systemctl restart gunicorn-uat')
