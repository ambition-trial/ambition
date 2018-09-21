from ambition_ae.admin_site import ambition_ae_admin
from ambition_export.admin_site import ambition_export_admin
from ambition_prn.admin_site import ambition_prn_admin
from ambition_screening.admin_site import ambition_screening_admin
from ambition_subject.admin_site import ambition_subject_admin
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.template.response import TemplateResponse
from django.urls.conf import path, include
from django.views.defaults import page_not_found, server_error  # noqa
from django.views.generic.base import RedirectView
from django_collect_offline.admin import django_collect_offline_admin
from django_collect_offline_files.admin_site import django_collect_offline_files_admin
from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_dashboard.views import AdministrationView
from edc_export.admin_site import edc_export_admin
from edc_identifier.admin_site import edc_identifier_admin
from edc_lab.admin_site import edc_lab_admin
from edc_locator.admin_site import edc_locator_admin
from edc_metadata.admin_site import edc_metadata_admin
from edc_pdutils.admin_site import edc_pdutils_admin
from edc_pharmacy.admin_site import edc_pharmacy_admin
from edc_reference.admin_site import edc_reference_admin
from edc_registration.admin_site import edc_registration_admin
from edc_visit_schedule.admin_site import edc_visit_schedule_admin

from .views import HomeView


def handler500(request):
    """500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """

    context = {'request': request}
    template_name = '500.html'  # You need to create a 500.html template.
    return TemplateResponse(request, template_name, context, status=500)


urlpatterns = [
    path('accounts/', include('edc_auth.urls')),
    path('admin/', include('edc_auth.urls')),
    path('admin/', admin.site.urls),
    path('admin/', edc_appointment_admin.urls),
    path('admin/', ambition_subject_admin.urls),
    path('admin/', ambition_ae_admin.urls),
    path('admin/', ambition_export_admin.urls),
    path('admin/', ambition_prn_admin.urls),
    path('admin/', ambition_screening_admin.urls),
    path('admin/', edc_lab_admin.urls),
    path('admin/', edc_export_admin.urls),
    path('admin/', edc_locator_admin.urls),
    path('admin/', edc_identifier_admin.urls),
    path('admin/', edc_metadata_admin.urls),
    path('admin/', edc_registration_admin.urls),
    path('admin/', edc_reference_admin.urls),
    path('admin/', django_collect_offline_admin.urls),
    path('admin/', edc_pharmacy_admin.urls),
    path('admin/', edc_action_item_admin.urls),
    path('admin/', edc_pdutils_admin.urls),
    path('admin/edc_visit_schedule/', edc_visit_schedule_admin.urls),
    path('admin/django_collect_offline_files/',
         django_collect_offline_files_admin.urls),
    path('administration/', AdministrationView.as_view(),
         name='administration_url'),
    path('admin/ambition_subject/', RedirectView.as_view(url='admin/ambition_subject/'),
         name='subject_models_url'),
    path('ambition_subject/', include('ambition_subject.urls')),
    path('ambition_ae/', include('ambition_ae.urls')),
    path('ambition_export/', include('ambition_export.urls')),
    path('ambition_prn/', include('ambition_prn.urls')),
    path('ambition_screening/', include('ambition_screening.urls')),
    path('subject/', include('ambition_dashboard.urls')),
    path('appointment/', include('edc_appointment.urls')),
    path('edc_action_item/', include('edc_action_item.urls')),
    path('edc_base/', include('edc_base.urls')),
    path('edc_consent/', include('edc_consent.urls')),
    path('edc_device/', include('edc_device.urls')),
    path('edc_export/', include('edc_export.urls')),
    path('edc_pdutils/', include('edc_pdutils.urls')),
    path('edc_lab/', include('edc_lab.urls')),
    path('edc_lab_dashboard/', include('edc_lab_dashboard.urls')),
    path('edc_locator/', include('edc_locator.urls')),
    path('edc_pharmacy/', include('edc_pharmacy.urls')),
    path('edc_pharmacy_dashboard/', include('edc_pharmacy_dashboard.urls')),
    path('edc_label/', include('edc_label.urls')),
    path('edc_metadata/', include('edc_metadata.urls')),
    path('edc_protocol/', include('edc_protocol.urls')),
    path('edc_identifier/', include('edc_identifier.urls')),
    path('edc_reference/', include('edc_reference.urls')),
    path('edc_registration/', include('edc_registration.urls')),
    path('edc_subject_dashboard/', include('edc_subject_dashboard.urls')),
    path('django_collect_offline/', include('django_collect_offline.urls')),
    path('django_collect_offline_files/',
         include('django_collect_offline_files.urls')),
    path('edc_visit_schedule/', include('edc_visit_schedule.urls')),
    path('switch_sites/', LogoutView.as_view(next_page=settings.INDEX_PAGE),
         name='switch_sites_url'),
    path('home/', HomeView.as_view(), name='home_url'),
    path('', HomeView.as_view(), name='home_url'),
]
