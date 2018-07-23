from fabric.api import task
from .deploy import deploy


@task
def deploy_client(*requirements_list, **kwargs):
    """Deploy clients from the deployment host.

    Assumes you have already prepared the deployment host

    Will use conf files on deployment

    For example:

    Copy ssh keys:

        fab -P -R mmankgodi deploy.ssh_copy_id:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf,bootstrap_branch=develop --user=django

    Deploy:

        fab -H bcpp038 deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.24,map_area=mmankgodi --user=django

    - OR -

        fab -P -R mmankgodi deploy.deploy_client:bootstrap_path=/Users/erikvw/source/bcpp/fabfile/conf/,release=0.1.24,map_area=mmankgodi --user=django

    Once complete:

        fab -P -R mmankgodi deploy.validate:release=0.1.24 --user=django

    """
    conf_filename = 'bootstrap_client.conf'
    deploy(requirements_list=requirements_list,
           conf_filename=conf_filename, **kwargs)
