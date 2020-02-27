from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_visit_schedule.constants import DAY1
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag  # noqa
from edc_action_item.models.action_item import ActionItem
from edc_appointment.models import Appointment
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy


class TestStudyTerminationConclusion(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")

        options = {
            "screening_identifier": subject_screening.screening_identifier,
            "consent_datetime": get_utcnow,
            "user_created": "erikvw",
        }
        consent = mommy.make_recipe("ambition_subject.subjectconsent", **options)

        self.subject_identifier = consent.subject_identifier

        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code=DAY1
        )
        self.subject_visit = mommy.make_recipe(
            "ambition_subject.subjectvisit",
            appointment=self.appointment,
            reason=SCHEDULED,
        )

    def test_study_termination(self):

        obj = mommy.make_recipe(
            "ambition_prn.studyterminationconclusion",
            subject_identifier=self.subject_identifier,
        )
        obj.save()
        self.assertTrue(obj.action_identifier)
        try:
            ActionItem.objects.get(action_identifier=obj.action_identifier)
        except ObjectDoesNotExist:
            self.fail("ActionItem unexpectedly does not exist")
