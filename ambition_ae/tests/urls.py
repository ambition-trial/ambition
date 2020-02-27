from ambition_ae.admin_site import ambition_ae_admin
from django.contrib import admin
from django.urls.conf import path, include
from edc_action_item.admin_site import edc_action_item_admin

urlpatterns = [
    path("ambition_ae/", include("ambition_ae.urls")),
    path("dashboard/", include("ambition_dashboard.urls")),
    path("admin/", ambition_ae_admin.urls),
    path("admin/", edc_action_item_admin.urls),
    path("admin/", admin.site.urls),
]
