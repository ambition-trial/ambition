from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_subject.models.subject_visit import SubjectVisit
from ambition_visit_schedule import DAY1, WEEK10
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_constants.constants import YES
from edc_metadata.constants import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestSubjectRules(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        screening = baker.make_recipe(
            "ambition_screening.subjectscreening", report_datetime=get_utcnow()
        )
        self.consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            consent_datetime=get_utcnow(),
            screening_identifier=screening.screening_identifier,
            user_created="erikvw",
        )
        self.visit_code = WEEK10

        for appointment in Appointment.objects.all().order_by("timepoint"):
            self.subject_visit = baker.make_recipe(
                "ambition_subject.subjectvisit",
                appointment=appointment,
                reason=SCHEDULED,
            )
            if appointment.visit_code == self.visit_code:
                break

    def test_medical_expenses_two_required(self):
        appointment = Appointment.objects.get(
            subject_identifier=self.consent.subject_identifier, visit_code=DAY1
        )
        self.subject_visit = SubjectVisit.objects.get(appointment=appointment)

        baker.make_recipe(
            "ambition_subject.medicalexpenses",
            subject_visit=self.subject_visit,
            care_before_hospital=YES,
        )

        self.assertEqual(
            CrfMetadata.objects.get(
                model="ambition_subject.medicalexpensestwo",
                subject_identifier=self.consent.subject_identifier,
                visit_code=DAY1,
            ).entry_status,
            REQUIRED,
        )
