from ambition_screening.models import SubjectScreening
from ambition_subject.models import SubjectConsent, SubjectRequisition, SubjectVisit
from django.contrib.admin import AdminSite as DjangoAdminSite
from edc_locator.models import SubjectLocator


class AdminSite(DjangoAdminSite):
    site_title = "Ambition Subject"
    site_header = "Ambition Subject"
    index_title = "Ambition Subject"
    site_url = "/administration/"


ambition_test_admin = AdminSite(name="ambition_test_admin")

ambition_test_admin.register(SubjectScreening)
ambition_test_admin.register(SubjectConsent)
ambition_test_admin.register(SubjectLocator)
ambition_test_admin.register(SubjectVisit)
ambition_test_admin.register(SubjectRequisition)
