from django.contrib.sites.models import Site
from django.conf import settings


class SiteDetectionMiddleware:
    def process_request(self, request):
        settings.SITE_ID = 1  # MUST BE
        host = request.META.get('HTTP_HOST')
        if host:
            try:
                site = Site.objects.get(domain=host)
                settings.SITE_ID = site.id
            except Site.DoesNotExist:
                pass
