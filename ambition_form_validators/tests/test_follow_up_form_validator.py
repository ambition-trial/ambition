from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import YES, NO
from edc_utils import get_utcnow

from ..form_validators import FollowUpFormValidator


@tag("ambition_form_validators")
class TestFollowUpFormValidator(TestCase):
    def test_rifampicin_started_yes_require_rifampicin_start_date(self):
        cleaned_data = {"rifampicin_started": YES, "rifampicin_start_date": None}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("rifampicin_start_date", form_validator._errors)

        cleaned_data = {
            "rifampicin_started": YES,
            "rifampicin_start_date": get_utcnow(),
        }
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_rifampicin_started_no_require_rifampicin_start_datee(self):
        cleaned_data = {"rifampicin_started": NO, "rifampicin_start_date": get_utcnow()}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("rifampicin_start_date", form_validator._errors)

        cleaned_data = {"rifampicin_started": NO, "rifampicin_start_date": None}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_fluconazole_dosed_no_require_rifampicin_start_datee(self):
        cleaned_data = {"fluconazole_dose": NO, "fluconazole_dose_other": "reason"}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_dose_other", form_validator._errors)

    def test_blood_transfusions_blood_yes_transfusions_units(self):
        cleaned_data = {"blood_transfusions": YES, "blood_transfusions_units": None}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_transfusions_units", form_validator._errors)

    def test_blood_transfusions_blood_no_transfusions_units(self):
        cleaned_data = {"blood_transfusions": NO, "blood_transfusions_units": 30}
        form_validator = FollowUpFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_transfusions_units", form_validator._errors)
