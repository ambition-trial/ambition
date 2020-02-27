from ambition_subject.admin_site import ambition_subject_admin
from django.contrib import admin
from django.urls.conf import path, include

urlpatterns = [
    path("ambition_subject/", include("ambition_ae.urls")),
    path("admin/", ambition_subject_admin.urls),
    path("admin/", admin.site.urls),
]
