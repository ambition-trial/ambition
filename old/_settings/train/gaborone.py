import os

from ambition_sites import get_site_id

from .base_train import *

# site is gaborone
SITE_ID = get_site_id('gaborone')

WSGI_APPLICATION = 'ambition.wsgi.train.application'


ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    'train.ambition.bhp.org.bw']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(MYSQL_DIR, 'train.conf'),
        },
    },
}
