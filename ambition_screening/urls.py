from django.urls.conf import path
from django.views.generic.base import RedirectView

from .admin_site import ambition_screening_admin

app_name = "ambition_screening"

urlpatterns = [
    path("admin/", ambition_screening_admin.urls),
    path("", RedirectView.as_view(url="/ambition_screening/admin/"), name="home_url"),
]
