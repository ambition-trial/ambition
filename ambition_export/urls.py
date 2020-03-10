from django.urls import path
from django.views.generic.base import RedirectView

from .admin_site import ambition_export_admin

app_name = "ambition_export"

urlpatterns = [
    path("admin/", ambition_export_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
