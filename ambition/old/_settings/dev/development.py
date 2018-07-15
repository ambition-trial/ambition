# Settings for development, e.g. tests, runserver

from django import VERSION as DJANGO_VERSION
import os
import sys

from ..base import *

DEBUG = True

ETC_DIR = os.path.join(BASE_DIR, 'etc')

MYSQL_DIR = ETC_DIR
MYSQL_CONF = MYSQL_CONF

WSGI_APPLICATION = 'ambition.wsgi.wsgi.application'

ALLOWED_HOSTS = ['localhost', '192.168.157.7']

SECRET_KEY = '2^p0phb&x&ntbsduf6afw(@efi(+!&hm_lrjr-+$5v(t0_f+6t'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(MYSQL_DIR, MYSQL_CONF),
        },
    },
}

SITE_ID = 10

INDEX_PAGE = 'localhost:8000'

# use test rando list
RANDOMIZATION_LIST_PATH = os.path.join(
    BASE_DIR, APP_NAME, 'tests', 'test_randomization_list.csv')

STATIC_ROOT = os.path.join(BASE_DIR, APP_NAME, 'static')

CUPS_SERVERS = {
    'bhp.printers.bhp.org.bw': 'bhp.printers.bhp.org.bw',
    'ambition-test.bhp.org.bw': 'ambition-test.bhp.org.bw',
    'localhost': None}

if 'test' in sys.argv:

    class DisableMigrations:

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher', )
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
