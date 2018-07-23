# reviewer.ambition gunicorn.conf
import os

from pathlib import Path

SOURCE_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

errorlog = os.path.join(SOURCE_ROOT, 'log/ambition-gunicorn-error.log')
accesslog = os.path.join(SOURCE_ROOT, 'log/ambition-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'run/ambition-reviewer.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = [f'DJANGO_SETTINGS_MODULE=ambition.settings.live.reviewer']

bind = "127.0.0.1:9001"
