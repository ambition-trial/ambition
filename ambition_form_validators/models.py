from django.conf import settings

if settings.APP_NAME == "ambition_form_validators":
    from .tests import models  # noqa
