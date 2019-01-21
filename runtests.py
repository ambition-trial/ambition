#!/usr/bin/env python
import django
import logging
import sys

from django.conf import settings
from django.test.runner import DiscoverRunner
from os.path import abspath, dirname, join

APP_NAME = 'ambition_edc'


class DisableMigrations:

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


installed_apps = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'django_extensions',
    'logentry_admin',
    'simple_history',
    'storages',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_collect_offline.apps.AppConfig',
    'django_collect_offline_files.apps.AppConfig',

    'edc_action_item.apps.AppConfig',
    'edc_auth.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_dashboard.apps.AppConfig',
    'edc_export.apps.AppConfig',
    'edc_fieldsets.apps.AppConfig',
    'edc_form_validators.apps.AppConfig',
    'edc_lab_dashboard.apps.AppConfig',
    'edc_label.apps.AppConfig',
    'edc_locator.apps.AppConfig',
    'edc_reference.apps.AppConfig',
    'edc_metadata_rules.apps.AppConfig',
    'edc_model_admin.apps.AppConfig',
    'edc_navbar.apps.AppConfig',
    'edc_notification.apps.AppConfig',
    'edc_offstudy.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_pdutils.apps.AppConfig',
    'edc_pharmacy.apps.AppConfig',
    'edc_pharmacy_dashboard.apps.AppConfig',
    'edc_prn.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_subject_dashboard.apps.AppConfig',
    'edc_timepoint.apps.AppConfig',
    'edc_list_data.apps.AppConfig',
    'ambition_lists.apps.AppConfig',
    'ambition_auth.apps.AppConfig',
    'ambition_dashboard.apps.AppConfig',
    'ambition_labs.apps.AppConfig',
    'ambition_metadata_rules.apps.AppConfig',
    'ambition_rando.apps.AppConfig',
    'ambition_reference.apps.AppConfig',
    'ambition_subject.apps.AppConfig',
    'ambition_form_validators.apps.AppConfig',
    'ambition_visit_schedule.apps.AppConfig',
    'ambition_ae.apps.AppConfig',
    'ambition_prn.apps.AppConfig',
    'ambition_export.apps.AppConfig',
    'ambition_screening.apps.AppConfig',
    'ambition_edc.apps.EdcAppointmentAppConfig',
    'ambition_edc.apps.EdcBaseAppConfig',
    'ambition_edc.apps.EdcDeviceAppConfig',
    'ambition_edc.apps.EdcIdentifierAppConfig',
    'ambition_edc.apps.EdcLabAppConfig',
    'ambition_edc.apps.EdcMetadataAppConfig',
    'ambition_edc.apps.EdcProtocolAppConfig',
    'ambition_edc.apps.EdcVisitTrackingAppConfig',
    'ambition_edc.apps.EdcFacilityAppConfig',
    'ambition_edc.apps.AppConfig',
]

DEFAULT_SETTINGS = dict(
    BASE_DIR=join(dirname(dirname(abspath(__file__))), 'ambition-edc'),
    ALLOWED_HOSTS=['localhost'],
    DEBUG=True,
    # AUTH_USER_MODEL='custom_user.CustomUser',
    ROOT_URLCONF=f'{APP_NAME}.urls',
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        },
    },
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],

    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,

    APP_NAME=f'{APP_NAME}',
    SITE_ID=10,
    EDC_BOOTSTRAP=3,
    VERBOSE_MODE=None,
    DASHBOARD_URL_NAMES={
        'subject_dashboard_url': f'{APP_NAME}:subject_dashboard_url',
    },

    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    MIGRATION_MODULES=DisableMigrations(),
    PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher', ),
    AUTH_PASSWORD_VALIDATORS=[
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
    ],
)

if not DEFAULT_SETTINGS.get('DEBUG'):
    DEFAULT_SETTINGS.update(KEY_PATH=join(
        DEFAULT_SETTINGS.get('BASE_DIR'), 'crypto_fields'))


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    failures = DiscoverRunner(failfast=True).run_tests(
        [f'{APP_NAME}.tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
