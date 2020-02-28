import pytz

from ambition_labs.panels import wb_panel
from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_visit_schedule.constants import DAY1
from datetime import datetime
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_lab.constants import TUBE
from edc_lab.models.panel import Panel
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from ..forms import SubjectRequisitionForm


@tag("ambition_subject")
class TestForms(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        year = get_utcnow().year
        subject_screening = baker.make_recipe("ambition_screening.subjectscreening")
        consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            consent_datetime=datetime(year, 12, 1, 0, 0, 0, 0, pytz.utc),
            user_created="erikvw",
        )
        self.subject_identifier = consent.subject_identifier
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier, visit_code=DAY1
        )
        self.subject_visit = baker.make_recipe(
            "ambition_subject.subjectvisit",
            appointment=self.appointment,
            reason=SCHEDULED,
        )

        self.data = {
            "clinic_verified": YES,
            "clinic_verified_datetime": get_utcnow(),
            "drawn_datetime": None,
            "item_type": TUBE,
            "panel": str(Panel.objects.get(name=wb_panel.name).pk),
            "reason_not_drawn": NOT_APPLICABLE,
            "report_datetime": get_utcnow(),
            "requisition_datetime": get_utcnow(),
            "requisition_identifier": "12345",
            "subject_identifier": self.subject_identifier,
            "subject_visit": str(self.subject_visit.pk),
        }

    def test_is_drawn_and_drawn_datetime(self):
        data = {k: v for k, v in self.data.items()}
        data.update({"is_drawn": YES})

        form = SubjectRequisitionForm(data=data)
        form.is_valid()
        self.assertIn("drawn_datetime", form.errors.keys())
        self.assertEqual(["This field is required."], form.errors.get("drawn_datetime"))

    def test_is_drawn_and_drawn_datetime2(self):
        data = {k: v for k, v in self.data.items()}
        data.update({"is_drawn": YES, "drawn_datetime": get_utcnow()})
        form = SubjectRequisitionForm(data=data)
        form.is_valid()
        self.assertNotIn("drawn_datetime", form.errors.keys())
        self.assertNotIn("reason_not_drawn", form.errors.keys())

    def test_is_not_drawn_and_drawn_datetime(self):
        data = {k: v for k, v in self.data.items()}
        data.update({"is_drawn": NO, "drawn_datetime": get_utcnow()})
        form = SubjectRequisitionForm(data=data)
        form.is_valid()
        self.assertIn("reason_not_drawn", form.errors.keys())
        self.assertEqual(
            ["This field is applicable."], form.errors.get("reason_not_drawn")
        )
