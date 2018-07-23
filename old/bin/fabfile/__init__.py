# import sys
# 
# if 'fab' in sys.argv[1]:
#     print("getting here atleast..")
#     from edc_fabric import fabfile as common
#     from .local_base_env import load_base_env
#     from .deploy import deploy
#     from .deploy import deploy_client
#     from .deploy import deployment_host
#     from .utils import restore_media_folder, generate_anonymous_transactions
# 
#     load_base_env()

from .deploy import (deploy_client, deploy, deployment_host)

