import os

from edc_base.logging import verbose_formatter, file_handler
from django_offline.loggers import loggers as django_offline_loggers
from django_offline_files.loggers import loggers as django_offline_files_loggers


file_handler['filename'] = os.path.join(
    os.path.expanduser('~/'), 'ambition-django.log')

loggers = {}
loggers.update(**django_offline_loggers)
loggers.update(**django_offline_files_loggers)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': verbose_formatter,
    },
    'handlers': {
        'file': file_handler
    },
    'loggers': loggers,
}
