from ambition_prn.admin_site import ambition_prn_admin
from django.contrib import admin
from django.urls.conf import path, include
from edc_action_item.admin_site import edc_action_item_admin

urlpatterns = [
    path("ambition_prn/", include("ambition_prn.urls")),
    path("dashboard/", include("ambition_dashboard.urls")),
    path("admin/", ambition_prn_admin.urls),
    path("admin/", edc_action_item_admin.urls),
    path("admin/", admin.site.urls),
]
