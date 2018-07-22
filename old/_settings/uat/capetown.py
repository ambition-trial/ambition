import os

from ambition_sites import get_site_id

from .base_uat import *

SITE_NAME = 'capetown'

TIME_ZONE = 'Africa/Johannesburg'

SITE_ID = get_site_id(SITE_NAME)  # 40

WSGI_APPLICATION = f'ambition.wsgi.uat.{SITE_NAME}.application'

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1', f'uat.{SITE_NAME}.{FQDN}']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(MYSQL_DIR, f'uat.{SITE_NAME}.conf'),
        },
    },
}
