import os

from fabric.api import env
from edc_fabric.fabfile.repositories import get_repo_name
from edc_fabric.fabfile.environment.tasks import update_fabric_env,\
    bootstrap_env


def prepare_env(bootstrap_filename=None, bootstrap_path=None, release=None,
                map_area=None, bootstrap_branch=None, work_online=None,
                task_callable=None):
    bootstrap_env(
        path=bootstrap_path,
        filename=bootstrap_filename,
        bootstrap_branch=bootstrap_branch)
    env.project_release = release
    env.map_area = map_area
    env.project_repo_name = get_repo_name(env.project_repo_url)
    env.project_repo_root = os.path.join(
        env.deployment_root, env.project_repo_name)
    env.fabric_config_root = os.path.join(env.project_repo_root, 'fabfile')
    env.fabric_config_path = os.path.join(
        env.fabric_config_root, 'conf', env.fabric_conf)
    update_fabric_env(use_local_fabric_conf=True)
