from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE

from ..form_validators import MedicalExpensesTwoDetailFormValidator


class TestMedicalExpensesTwoDetailFormValidator(TestCase):

    def test_location_care_other_invalid(self):

        cleaned_data = {'location_care': OTHER,
                        'location_care_other': None}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('location_care_other', form._errors)

    def test_transport_form_transport_cost_invalid(self):

        cleaned_data = {'transport_form': NOT_APPLICABLE,
                        'transport_cost': 2.00}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('transport_cost', form._errors)

    def test_transport_form_transport_duration_invalid(self):

        cleaned_data = {'transport_form': NOT_APPLICABLE,
                        'transport_duration': '08:11'}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('transport_duration', form._errors)

    def test_care_provider_other_invalid(self):

        cleaned_data = {'care_provider': OTHER,
                        'care_provider_other': None}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('care_provider_other', form._errors)

    def test_paid_treatment_amount_invalid(self):

        cleaned_data = {'paid_treatment': YES,
                        'paid_treatment_amount': None}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('paid_treatment_amount', form._errors)

    def test_medication_bought_no_payment_invalid(self):

        cleaned_data = {'medication_bought': YES,
                        'medication_payment': None}
        form = MedicalExpensesTwoDetailFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('medication_payment', form._errors)
