from .base_test import *

# site is gaborone
SITE_ID = get_site_id('blantyre')

WSGI_APPLICATION = 'ambition.wsgi.uat-blantyre.application'


ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    'uat-blantyre.ambition.clinicedc.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(MYSQL_DIR, 'uat.conf'),
        },
    },
}

TIME_ZONE = 'Africa/Blantyre'
