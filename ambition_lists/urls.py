from django.conf import settings
from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import ambition_lists_admin

app_name = "ambition_lists"

urlpatterns = [
    path("admin/", ambition_lists_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]


if settings.APP_NAME == "ambition_lists":
    from django.contrib import admin

    urlpatterns += [path("admin/", admin.site.urls)]
