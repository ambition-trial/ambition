from fabric.api import env


def set_fab_env(user):
    env.user = user
    env.app_folder = f'/home/{env.user}/app'
    env.local_app_folder = '~/source/ambition-edc'
    env.activate = 'source ~/.venvs/ambition/bin/activate'
