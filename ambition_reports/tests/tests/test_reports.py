from ambition_rando.tests import AmbitionTestCaseMixin
from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.test.client import RequestFactory
from edc_adverse_event.models import AeClassification
from edc_list_data.site_list_data import site_list_data
from model_mommy import mommy

from ...ae_report import AeReport


class TestReports(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.subject_identifier = self.create_subject()
        self.user = User.objects.create(
            username="erikvw", is_staff=True, is_active=True
        )

    def test_aereport(self):

        rf = RequestFactory()
        request = rf.get("/")
        request.user = self.user
        ae_classification = AeClassification.objects.all()[0]
        ae_initial = mommy.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            ae_classification=ae_classification,
        )

        report = AeReport(
            ae_initial=ae_initial,
            subject_identifier=ae_initial.subject_identifier,
            user=request.user,
            request=request,
        )
        return report.render()
