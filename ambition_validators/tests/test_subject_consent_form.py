from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import SubjectConsentFormValidator
from .models import SubjectScreening


class TestSubjectConsentForm(TestCase):

    def setUp(self):
        self.screening_identifier = 'ABCDEF'
        self.subject_screening = SubjectScreening.objects.create(
            screening_identifier=self.screening_identifier, age_in_years=20)
        subject_screening_model = SubjectConsentFormValidator.subject_screening_model
        subject_screening_model = subject_screening_model.replace(
            'ambition_screening', 'ambition_validators')
        SubjectConsentFormValidator.subject_screening_model = subject_screening_model

    def test_subject_screening_ok(self):
        cleaned_data = dict(
            screening_identifier=self.screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_subject_screening_invalid(self):
        cleaned_data = dict(
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=20)).date())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('missing_subject_screening', form_validator._error_codes)

    def test_consent_datetime(self):
        dob = (get_utcnow() - relativedelta(years=20)).date()
        cleaned_data = dict(
            screening_identifier=self.screening_identifier,
            dob=dob)
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('consent_datetime', form_validator._errors)

        cleaned_data.update(consent_datetime=get_utcnow())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_consent_age_mismatch_with_screening_age_invalid(self):
        age_in_years = 18
        dob = (get_utcnow() - relativedelta(years=age_in_years)).date()
        cleaned_data = dict(
            dob=dob,
            screening_identifier=self.screening_identifier,
            consent_datetime=get_utcnow())
        form_validator = SubjectConsentFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(forms.ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)
