from .base import *

# don't change!
DEBUG = False

ETC_DIR = os.path.join('/etc', APP_NAME)

SECRET_KEY = '2^p0phb&x&ntbsduf6afw(@efi(+!&hm_lrjr-+$5v(t0_f+6t'

# site is gaborone
SITE_ID = '10'

ALLOWED_HOSTS = [
    'ambition-test.bhp.org.bw',
    'ambition.clinicedc.org']

# use the test rando list
# copy tests/'test_randomization_list.csv' to /etc/ambition
RANDOMIZATION_LIST_PATH = os.path.join(ETC_DIR, 'test_randomization_list.csv')

STATIC_ROOT = os.path.join(str(Path(BASE_DIR).parent), 'static')

KEY_PATH = os.path.join(ETC_DIR, 'crypto_fields')
# for first time use
# AUTO_CREATE_KEYS = True

# dont firget to copy mysql.conf to ETC_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, 'mysql.conf'),
        },
    },
}

# see https://docs.djangoproject.com/en/2.0/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, f'{APP_NAME}-debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
