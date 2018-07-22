# see http://www.simonkrueger.com/2015/05/27/logging-django-apps-to-syslog.html
import environ
import os

env = environ.Env()
env.read_env('.env')

LOG_FOLDER = env.str('DJANGO_LOG_FOLDER')
LOGGING_FILE_LEVEL = env.str('DJANGO_LOGGING_FILE_LEVEL')
LOGGING_SYSLOG_LEVEL = env.str('DJANGO_LOGGING_SYSLOG_LEVEL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': LOGGING_FILE_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'ambition.log'),
        },
        'syslog': {
            'level': LOGGING_SYSLOG_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGGING_FILE_LEVEL,
            'propagate': True,
        },
        # root logger
        '': {
            'handlers': ['syslog'],
            'level': LOGGING_SYSLOG_LEVEL,
            'disabled': False
        },
        'ambition': {
            'handlers': ['syslog'],
            'level': LOGGING_SYSLOG_LEVEL,
            'propagate': False,
        },
    },
}
