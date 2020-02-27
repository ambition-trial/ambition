from edc_dashboard.views import AdministrationView
from django.urls.conf import path, include

urlpatterns = [
    path("accounts/", include("edc_auth.urls")),
    path("edc_adverse_event/", include("edc_adverse_event.urls")),
    path("edc_dashboard/", include("edc_dashboard.urls")),
    path("edc_export/", include("edc_export.urls")),
    path("edc_lab/", include("edc_lab.urls")),
    path("edc_lab_dashboard/", include("edc_lab_dashboard.urls")),
    path("edc_auth/", include("edc_auth.urls")),
    path("edc_pharmacy/", include("edc_pharmacy.urls")),
    path("edc_reference/", include("edc_reference.urls")),
    path("meta_ae/", include("meta_ae.urls")),
    path("meta_lists/", include("meta_lists.urls")),
    path("meta_prn/", include("meta_prn.urls")),
    path("edc_randomization/", include("edc_randomization.urls")),
    path("meta_screening/", include("meta_screening.urls")),
    path("meta_consent/", include("meta_consent.urls")),
    path("meta_subject/", include("meta_subject.urls")),
    path("administration/", AdministrationView.as_view(), name="administration_url"),
]
