import os
import sys

from django.core.exceptions import ImproperlyConfigured
from pathlib import Path


# simple version check
try:
    assert sys.version_info >= (3, 6), 'hello'
    assert sys.version_info < (3, 7)
except AssertionError:
    raise ImproperlyConfigured(
        'Incorrect python version. Expected 3.6. Check your environment.')

BASE_DIR = str(Path(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))).parent)

APP_NAME = 'ambition'

REVIEWER_SITE_ID = 1

MYSQL_DIR = os.path.join('/etc', APP_NAME, 'mysql.conf')

LOGIN_REDIRECT_URL = 'home_url'

# Application definition
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
    'django_offline.apps.AppConfig',
    'django_offline_files.apps.AppConfig',
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

ROOT_URLCONF = 'ambition.urls'

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

WSGI_APPLICATION = 'ambition.wsgi.application'

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
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('af', 'Afrikaans'),
    ('ny', 'Chichewa'),
    ('en', 'English'),
    ('xh', 'isiXhosa'),
    ('lg', 'Luganda'),
    ('rny', 'Runyankore'),
    ('tn', 'Setswana'),
    ('sn', 'Shona'))

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True

# set to False so DATE formats below are used
USE_L10N = False

USE_TZ = True

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
STATIC_URL = '/static/'

# edc app specific settings  ################

# edc_base
MAIN_NAVBAR_NAME = APP_NAME

# edc_lab and label
LABEL_TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'label_templates')

# django_offline / django_offline files
EDC_SYNC_SERVER_IP = None
DJANGO_OFFLINE_FILES_REMOTE_HOST = None
DJANGO_OFFLINE_FILES_USER = None
DJANGO_OFFLINE_FILES_USB_VOLUME = None

# dashboards
DASHBOARD_URL_NAMES = {
    'subject_models_url': 'subject_models_url',
    'subject_listboard_url': 'ambition_dashboard:subject_listboard_url',
    'screening_listboard_url': 'ambition_dashboard:screening_listboard_url',
    'subject_dashboard_url': 'ambition_dashboard:subject_dashboard_url',
}
DASHBOARD_BASE_TEMPLATES = {
    'listboard_base_template': 'ambition/base.html',
    'dashboard_base_template': 'ambition/base.html',
    'screening_listboard_template': 'ambition_dashboard/screening/listboard.html',
    'subject_listboard_template': 'ambition_dashboard/subject/listboard.html',
    'subject_dashboard_template': 'ambition_dashboard/subject/dashboard.html',
}
LAB_DASHBOARD_URL_NAMES = {}
LAB_DASHBOARD_BASE_TEMPLATES = {}
LAB_DASHBOARD_REQUISITION_MODEL = 'ambition_subject.subjectrequisition'

# edc_facility
HOLIDAY_FILE = os.path.join(BASE_DIR, 'holidays.csv')
COUNTRY = 'botswana'

# ambition
EMAIL_CONTACTS = {
    'ae_reports': 'ambitionreporting@lshtm.ac.uk'}

# django_revision
GIT_DIR = BASE_DIR

EXPORT_FOLDER = os.path.expanduser('~/')
