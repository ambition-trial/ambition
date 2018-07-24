from fabric.api import execute, task

from edc_fabric.fabfile import prepare_deployment_host


@task
def deployment_host(bootstrap_path=None, release=None, specific_tag=None,
                    skip_clone=None, skip_pip_download=None,
                    use_branch=None, bootstrap_branch=None,):
    """
    Example:

        brew update && fab -H localhost deployment_host:bootstrap_path=/Users/django/source/ambition/fabfile/conf/,release=develop,use_branch=True,bootstrap_branch=develop,skip_pip_download=True,skip_clone=True

    """
    execute(prepare_deployment_host,
            bootstrap_path=bootstrap_path,
            release=release,
            specific_tag=specific_tag,
            skip_clone=skip_clone,
            skip_pip_download=skip_pip_download,
            use_branch=use_branch,
            bootstrap_branch=bootstrap_branch)
