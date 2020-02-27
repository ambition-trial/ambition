import arrow

from ambition_prn.form_validators import StudyTerminationConclusionFormValidator
from ambition_rando.tests import AmbitionTestCaseMixin
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag  # noqa
from django.test.utils import override_settings
from edc_constants.constants import DEAD
from edc_facility.import_holidays import import_holidays
from edc_list_data import site_list_data
from edc_utils import get_utcnow

from ...models import DeathReport


class TestStudyTerminationConclusionFormValidator(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        import_holidays()
        super().setUpClass()

    def test_died_no_death_date_invalid(self):
        subject_identifier = self.create_subject()

        DeathReport.objects.create(
            subject_identifier=subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1,
        )

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": DEAD,
            "death_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("death_date", form_validator._errors)

    def test_died_death_date_mismatch(self):
        subject_identifier = self.create_subject()
        DeathReport.objects.create(
            subject_identifier=subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1,
        )

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": DEAD,
            "death_date": date(2011, 1, 1),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("death_date", form_validator._errors)

    @override_settings(TIME_ZONE="Africa/Kampala")
    def test_died_death_date_ok(self):
        from dateutil import tz
        from datetime import datetime

        subject_identifier = self.create_subject()

        dte1 = arrow.get(datetime(2018, 8, 12, 0, 0, 0), tz.tzutc())
        dte2 = date(2018, 8, 12)
        DeathReport.objects.create(
            subject_identifier=subject_identifier,
            death_datetime=dte1.datetime,
            study_day=1,
        )

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": DEAD,
            "death_date": dte2,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_died_death_date_change(self):
        dte = get_utcnow()
        subject_identifier = self.create_subject()

        DeathReport.objects.create(
            subject_identifier=subject_identifier,
            death_datetime=get_utcnow(),
            study_day=1,
        )

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": DEAD,
            "death_date": dte.date(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")
