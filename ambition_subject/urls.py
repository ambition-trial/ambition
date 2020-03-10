from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import ambition_subject_admin

app_name = "ambition_subject"

urlpatterns = [
    path("admin/", ambition_subject_admin.urls),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
