from django.conf import settings

if settings.APP_NAME == 'ambition_validators':
    from .tests import models
