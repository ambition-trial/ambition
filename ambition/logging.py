# see http://www.simonkrueger.com/2015/05/27/logging-django-apps-to-syslog.html
import environ
import os

env = environ.Env()
env.read_env('.env')

DJANGO_LOG_FOLDER = env.str('DJANGO_LOG_FOLDER')

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
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(DJANGO_LOG_FOLDER, 'ambition.log'),
        },
        #         'console': {
        #             'level': 'DEBUG',
        #             'filters': ['require_debug_true'],
        #             'class': 'logging.StreamHandler',
        #             'formatter': 'simple'
        #         },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # root logger
        '': {
            'handlers': ['syslog'],
            'level': 'INFO',
            'disabled': False
        },
        'ambition': {
            'handlers': ['syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
