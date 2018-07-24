import environ
import os
import sys

from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

# simple version check
try:
    assert (3, 6) <= (sys.version_info.major, sys.version_info.minor) <= (3, 7)
except AssertionError:
    raise ImproperlyConfigured(
        'Incorrect python version. Expected 3.6 or 3.7. Check your environment.')


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_AUTO_CREATE_KEYS=(bool, False),
    DJANGO_CSRF_COOKIE_SECURE=(bool, True),
    DJANGO_SESSION_COOKIE_SECURE=(bool, True),
    DJANGO_USE_I18N=(bool, True),
    DJANGO_USE_L10N=(bool, False),
    DJANGO_USE_TZ=(bool, True),
)
environ.Env.read_env()

BASE_DIR = str(Path(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))).parent)

DEBUG = env('DEBUG')

SECRET_KEY = env('DJANGO_SECRET_KEY')

APP_NAME = env('DJANGO_APP_NAME')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', [])

REVIEWER_SITE_ID = env.int('DJANGO_REVIEWER_SITE_ID', 1)

LOGIN_REDIRECT_URL = env('DJANGO_LOGIN_REDIRECT_URL', 'home_url')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'django_extensions',
    'simple_history',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'edc_model_admin.apps.AppConfig',
    'edc_prn.apps.AppConfig',
    'edc_offstudy.apps.AppConfig',
    'edc_dashboard.apps.AppConfig',
    'edc_form_validators.apps.AppConfig',
    'edc_fieldsets.apps.AppConfig',
    'edc_subject_dashboard.apps.AppConfig',
    'edc_lab_dashboard.apps.AppConfig',
    'edc_list_data.apps.AppConfig',
    'django_collect_offline.apps.AppConfig',
    'django_collect_offline_files.apps.AppConfig',
    'edc_pharmacy.apps.AppConfig',
    # 'edc_pharmacy_dashboard.apps.AppConfig',
    'edc_navbar.apps.AppConfig',
    'edc_reference.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_action_item.apps.AppConfig',
    'edc_label.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_metadata_rules.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'ambition_dashboard.apps.AppConfig',
    'ambition_labs.apps.AppConfig',
    'ambition_metadata_rules.apps.AppConfig',
    'ambition_rando.apps.AppConfig',
    'ambition_reference.apps.AppConfig',
    'ambition_subject.apps.AppConfig',
    'ambition_validators.apps.AppConfig',
    'ambition_visit_schedule.apps.AppConfig',
    'ambition_ae.apps.AppConfig',
    'ambition_prn.apps.AppConfig',
    'ambition_export.apps.AppConfig',
    'ambition_screening.apps.AppConfig',
    'ambition.apps.EdcAppointmentAppConfig',
    'ambition.apps.EdcBaseAppConfig',
    'ambition.apps.EdcDeviceAppConfig',
    'ambition.apps.EdcIdentifierAppConfig',
    'ambition.apps.EdcLabAppConfig',
    'ambition.apps.EdcMetadataAppConfig',
    'ambition.apps.EdcProtocolAppConfig',
    'ambition.apps.EdcVisitTrackingAppConfig',
    'ambition.apps.EdcFacilityAppConfig',
    'ambition.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',
    'edc_lab_dashboard.middleware.DashboardMiddleware',
]

ROOT_URLCONF = f'{APP_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': env.db(),
    'extra': env.db('SQLITE_URL', default='sqlite:////tmp/my-tmp-sqlite.db')
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str('DJANGO_LANGUAGE_CODE', 'en-us')

LANGUAGES = [x.split(':') for x in env.list(
    'DJANGO_LANGUAGES')] or (('en', 'English'),)

TIME_ZONE = env.str('DJANGO_TIME_ZONE', 'Africa/Gaborone')

USE_I18N = env('DJANGO_USE_I18N')

# set to False so DATE formats below are used
USE_L10N = env('DJANGO_USE_L10N', False)

USE_TZ = env('DJANGO_USE_TZ', True)

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y']
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%d/%m/%Y %H:%M:%S',     # '25/10/2006 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',  # '25/10/2006 14:30:59.000200'
    '%d/%m/%Y %H:%M',        # '25/10/2006 14:30'
    '%d/%m/%Y',              # '25/10/2006'
]
DATE_FORMAT = 'j N Y'
DATETIME_FORMAT = 'j N Y H:i'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'

# static
STATIC_URL = env('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = env('DJANGO_STATIC_ROOT',
                  os.path.join(BASE_DIR, APP_NAME, 'static'))

CSRF_COOKIE_SECURE = env('DJANGO_CSRF_COOKIE_SECURE')
SECURE_PROXY_SSL_HEADER = env.tuple('DJANGO_SECURE_PROXY_SSL_HEADER')
SESSION_COOKIE_SECURE = env('DJANGO_SESSION_COOKIE_SECURE')

# edc_base
MAIN_NAVBAR_NAME = env('DJANGO_MAIN_NAVBAR_NAME')

# edc_lab and label
LABEL_TEMPLATE_FOLDER = env(
    'DJANGO_LABEL_TEMPLATE_FOLDER', os.path.join(BASE_DIR, 'label_templates'))
CUPS_SERVERS = env.dict('DJANGO_CUPS_SERVERS')

# django_collect_offline / django_collect_offline files
DJANGO_COLLECT_OFFLINE_SERVER_IP = env('DJANGO_COLLECT_OFFLINE_SERVER_IP')
DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST = env('DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST')
DJANGO_COLLECT_OFFLINE_FILES_USER = env('DJANGO_COLLECT_OFFLINE_FILES_USER')
DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME = env('DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME')

# dashboards
DASHBOARD_URL_NAMES = env.dict('DJANGO_DASHBOARD_URL_NAMES')
DASHBOARD_URL_NAMES = env.dict('DJANGO_DASHBOARD_BASE_TEMPLATES')
LAB_DASHBOARD_URL_NAMES = env.dict('DJANGO_LAB_DASHBOARD_URL_NAMES')
LAB_DASHBOARD_BASE_TEMPLATES = env.dict('DJANGO_LAB_DASHBOARD_BASE_TEMPLATES')
LAB_DASHBOARD_REQUISITION_MODEL = env(
    'DJANGO_LAB_DASHBOARD_REQUISITION_MODEL')

# edc_facility
HOLIDAY_FILE = env('DJANGO_HOLIDAY_FILE')
COUNTRY = env('DJANGO_COUNTRY', 'botswana')

# ambition
EMAIL_CONTACTS = env.dict('DJANGO_EMAIL_CONTACTS', {})

# django_revision
GIT_DIR = BASE_DIR

# django_crypto_fields
KEY_PATH = env('DJANGO_KEY_PATH')
AUTO_CREATE_KEYS = env('DJANGO_AUTO_CREATE_KEYS')

EXPORT_FOLDER = env('DJANGO_EXPORT_FOLDER', os.path.expanduser('~/'))

FQDN = env('DJANGO_FQDN')
