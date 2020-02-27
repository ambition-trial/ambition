from ambition_dashboard.model_wrappers import SubjectScreeningModelWrapper
from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_screening.models import SubjectScreening
from ambition_subject.models.subject_consent import SubjectConsent
from ambition_subject.models.subject_visit import SubjectVisit
from django.test import TestCase, tag  # noqa
from edc_appointment.models import Appointment
from edc_model_wrapper.tests import ModelWrapperTestHelper
from edc_subject_model_wrappers import (
    AppointmentModelWrapper,
    SubjectLocatorModelWrapper,
    SubjectConsentModelWrapper,
    SubjectVisitModelWrapper,
)


class SubjectModelWrapperTestHelper(ModelWrapperTestHelper):
    dashboard_url = "/subject_dashboard/"


class ScreeningModelWrapperTestHelper(ModelWrapperTestHelper):
    dashboard_url = "/screening_listboard/"


class TestModelWrappers(AmbitionTestCaseMixin, TestCase):

    model_wrapper_helper_cls = SubjectModelWrapperTestHelper

    def setUp(self):
        self.subject_identifier = self.create_subject()

    def test_subject_screening(self):
        subject_screening = SubjectScreening.objects.all()[0]
        helper = ScreeningModelWrapperTestHelper(
            model_wrapper=SubjectScreeningModelWrapper, model_obj=subject_screening
        )
        helper.test(self)

    def test_subject_consent(self):
        subject_consent = SubjectConsent.objects.all()[0]
        helper = ModelWrapperTestHelper(
            model_wrapper=SubjectConsentModelWrapper, model_obj=subject_consent
        )
        helper.test(self)

    def test_subject_locator(self):
        helper = ModelWrapperTestHelper(
            model_wrapper=SubjectLocatorModelWrapper,
            subject_identifier=self.subject_identifier,
        )
        helper.test(self)

    def test_appointment(self):
        appointment = Appointment.objects.all()[0]
        helper = ModelWrapperTestHelper(
            model_wrapper=AppointmentModelWrapper, model_obj=appointment
        )
        helper.test(self)

    def test_subject_visit(self):
        appointment = Appointment.objects.all()[0]
        subject_visit = SubjectVisit.objects.create(
            appointment=appointment, reason="scheduled"
        )
        helper = ModelWrapperTestHelper(
            model_wrapper=SubjectVisitModelWrapper, model_obj=subject_visit
        )
        helper.test(self)
