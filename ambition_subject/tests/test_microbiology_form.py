from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_visit_schedule import DAY1
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_constants.constants import YES
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker
from unittest.case import skip

from ..forms import MicrobiologyForm


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestMicrobiologyForm(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        subject_screening = baker.make_recipe("ambition_screening.subjectscreening")
        options = {
            "screening_identifier": subject_screening.screening_identifier,
            "consent_datetime": get_utcnow,
            "user_created": "erikvw",
        }
        consent = baker.make_recipe("ambition_subject.subjectconsent", **options)
        self.subject_identifier = consent.subject_identifier
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code=DAY1
        )
        self.subject_visit = baker.make_recipe(
            "ambition_subject.subjectvisit",
            appointment=self.appointment,
            reason=SCHEDULED,
        )

    @skip("fix this test")
    def test_yes_blood_culture_performed_with_blood_culture_results(self):
        data = {
            "subject_visit": self.subject_visit,
            "blood_culture_performed": YES,
            "blood_taken_date": get_utcnow().date(),
            "blood_culture_results": "no_growth",
        }
        form = MicrobiologyForm(initial=data)
        form.is_valid()


#         self.assertTrue(form.is_valid())
#         self.assertTrue(form.save())
