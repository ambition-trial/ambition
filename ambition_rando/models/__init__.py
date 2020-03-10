import sys

from django.conf import settings

from .randomization_list import RandomizationList, RandomizationListModelError

if settings.APP_NAME == "ambition_rando" and "makemigrations" not in sys.argv:
    from ..tests import models
