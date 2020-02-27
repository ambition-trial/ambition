from django.contrib import admin
from django.urls.conf import path
from django.views.generic.base import RedirectView

app_name = "ambition_rando"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/ambition_rando/admin/"), name="home_url"),
]
