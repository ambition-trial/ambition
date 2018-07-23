import os

from fabric.api import env
from datetime import datetime

from edc_fabric.fabfile.utils import get_hosts, get_device_ids
from fabfile.roledefs import roledefs
from edc_fabric.fabfile.environment.tasks import update_env_secrets
from fabfile.patterns import hostname_pattern
from edc_fabric.fabfile.prompts import prompts
from fabric.contrib import django


def load_base_env():
    django.settings_module('ambition.settings')

    CONFIG_FILENAME = 'ambition.conf'
    DOWNLOADS_DIR = '~/Downloads'

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ETC_CONFIG_PATH = os.path.join(BASE_DIR, 'fabfile', 'etc')
    FABRIC_CONFIG_PATH = os.path.join(
        BASE_DIR, 'fabfile', 'conf', 'fabric.conf')

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    env.log_folder = os.path.expanduser('~/fabric/{}'.format(timestamp))
    if not os.path.exists(env.log_folder):
        os.makedirs(env.log_folder)
    print('log_folder', env.log_folder)
    update_env_secrets(path=ETC_CONFIG_PATH)
    env.roledefs = roledefs
    env.hosts, env.passwords = get_hosts(
        path=ETC_CONFIG_PATH, gpg_filename='hosts.conf.gpg')
    env.hostname_pattern = hostname_pattern
    env.device_ids = get_device_ids()
    env.prompts = prompts

    env.prompts.update({'Enter password: ': env.dbpasswd})

    with open(os.path.join(env.log_folder, 'hosts.txt'), 'a') as f:
        f.write('{}\n'.format(',\n'.join([h for h in env.hosts])))
