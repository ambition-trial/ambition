from ambition_sites import get_site_id, fqdn

from .base_live import *


SITE_NAME = 'harare'

TIME_ZONE = 'Africa/Harare'

SITE_ID = get_site_id(f'{SITE_NAME}')

FQDN = fqdn

WSGI_APPLICATION = f'{APP_NAME}.wsgi.{SITE_NAME}.application'

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    f'{SITE_NAME}.{FQDN}']

# CUPS_SERVERS = {
#     'bhp.printers.bhp.org.bw': 'bhp.printers.bhp.org.bw',
#     'localhost': None}
