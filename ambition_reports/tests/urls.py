from ambition_ae.admin_site import ambition_ae_admin
from django.contrib import admin
from django.urls.conf import path, include

urlpatterns = [
    path("ambition_ae/", include("ambition_ae.urls")),
    path("admin/", ambition_ae_admin.urls),
    path("admin/", admin.site.urls),
]
