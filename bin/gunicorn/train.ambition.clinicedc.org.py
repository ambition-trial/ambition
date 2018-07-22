import os

from pathlib import Path

SOURCE_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

errorlog = os.path.join(SOURCE_ROOT, 'log/ambition-train-gunicorn-error.log')
accesslog = os.path.join(SOURCE_ROOT, 'log/ambition-train-gunicorn-access.log')
loglevel = 'debug'
workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

pidfile = os.path.join(SOURCE_ROOT, 'run/ambition-train.pid')

raw_env = [f'DJANGO_SETTINGS_MODULE=ambition.settings.test.train']

bind = "127.0.0.1:9102"
