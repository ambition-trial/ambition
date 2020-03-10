import pytz

from ambition_rando.tests import AmbitionTestCaseMixin
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_facility.holidays import Holidays
from edc_utils import get_utcnow
from model_bakery import baker


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestAppointment(AmbitionTestCaseMixin, TestCase):
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

    def test_appointments_creation(self):
        """Assert appointment triggering method creates appointments.
        """
        appointments = Appointment.objects.filter(
            subject_identifier=self.subject_identifier
        )
        self.assertEqual(appointments.count(), 12)

    def test_appointments_rdates(self):
        holidays = Holidays(country="botswana")
        appointments = Appointment.objects.filter(
            subject_identifier=self.subject_identifier
        ).order_by("appt_datetime")
        appt_datetimes = [obj.appt_datetime for obj in appointments]
        start = appt_datetimes[0]
        if not holidays.is_holiday(start + relativedelta(days=2)):
            self.assertEqual(
                appt_datetimes[1].date(), start.date() + relativedelta(days=2)
            )
        if not holidays.is_holiday(start + relativedelta(days=4)):
            self.assertEqual(
                appt_datetimes[2].date(), start.date() + relativedelta(days=4)
            )
        if not holidays.is_holiday(start + relativedelta(days=6)):
            self.assertEqual(
                appt_datetimes[3].date(), start.date() + relativedelta(days=6)
            )
