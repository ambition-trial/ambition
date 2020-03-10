from django.contrib import admin
from django.urls.conf import path

app_name = "ambition_labs"

urlpatterns = [path("admin/", admin.site.urls)]
