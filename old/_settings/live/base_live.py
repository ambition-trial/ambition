import os

from ambition_sites import fqdn

from ..base import *
from ..logging import LOGGING

DEBUG = False

ETC_DIR = os.path.join('/etc', APP_NAME, 'live')

RANDOMIZATION_LIST_PATH = os.path.join(ETC_DIR, 'randomization_list.csv')
LIVE_SYSTEM = 'LIVE'
KEY_PATH = os.path.join(ETC_DIR, 'crypto_fields')
AUTO_CREATE_KEYS = False

FQDN = fqdn

with open(os.path.join(ETC_DIR, 'secret_key')) as f:
    SECRET_KEY = f.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(MYSQL_DIR, 'live.conf'),
        },
    },
}

INDEX_PAGE = f'https://{FQDN}'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

STATIC_ROOT = os.path.expanduser('~/static/live/')

# django_collect_offline / django_collect_offline files
EDC_SYNC_SERVER_IP = None
DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST = None
DJANGO_COLLECT_OFFLINE_FILES_USER = None
DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME = None
