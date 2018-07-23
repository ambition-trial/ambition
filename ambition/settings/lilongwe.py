from ambition_sites.get_site_id import get_site_id

from .base import *  # noqa

TOWN = 'lilongwe'
COUNTRY = 'malawi'
# CUPS_SERVERS =
# LANGUAGES =
SITE_ID = get_site_id(TOWN)
# TIME_ZONE =
ALLOWED_HOSTS = [f'.{TOWN}.edcdev.clinicedc.org']
