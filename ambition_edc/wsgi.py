"""
Default wsgi for tests and local runserver or single app instance
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ambition_edc.settings")

application = get_wsgi_application()
