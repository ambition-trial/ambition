from ambition_visit_schedule import DAY1
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES, OTHER, NO
from edc_form_validators import REQUIRED_ERROR

from ..form_validators import SignificantDiagnosesFormValidator
from .models import SubjectVisit, TestModel


class TestSignificantDiagnosesFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='11111111',
            appt_datetime=get_utcnow(),
            visit_code=DAY1)
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

        self.week4 = TestModel.objects.create(
            subject_visit=self.subject_visit,
            other_significant_dx=YES)

    def test_week4_no_significant_diagnoses_valid(self):
        self.week4.other_significant_dx = NO
        cleaned_data = {
            'week4': self.week4,
            'possible_diagnoses': None,
        }
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_week4_significant_diagnoses_invalid(self):
        cleaned_data = {
            'week4': self.week4,
            'possible_diagnoses': None,
        }
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('possible_diagnoses', form_validator._errors)

    def test_followup_significant_diagnoses_invalid(self):
        cleaned_data = {
            'followup': self.week4,
            'possible_diagnoses': None,
        }
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('possible_diagnoses', form_validator._errors)

    def test_other_significant_diagnoses(self):
        options = {
            'week4': self.week4,
            'other_significant_diagnoses': YES,
            'possible_diagnoses': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('possible_diagnoses',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_pulmonary_tb(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'pulmonary_tb',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_extra_pulmonary_tb(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'extra_pulmonary_tb',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_kaposi_sarcoma(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'kaposi_sarcoma',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_malaria(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'malaria',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_bacteraemia(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'bacteraemia',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_pneumonia(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'pneumonia',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_diarrhoeal_wasting(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': 'diarrhoeal_wasting',
            'dx_date': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_date',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)

    def test_possible_diagnoses_dx_other(self):
        options = {
            'week4': self.week4,
            'possible_diagnoses': OTHER,
            'dx_other': None}
        form_validator = SignificantDiagnosesFormValidator(
            cleaned_data=options)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn('dx_other',
                      form_validator._errors)
        self.assertIn(REQUIRED_ERROR, form_validator._error_codes)
