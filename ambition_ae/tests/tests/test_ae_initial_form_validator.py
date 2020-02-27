from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_adverse_event.models import SaeReason
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import NOT_REQUIRED_ERROR
from edc_sites.tests import SiteTestCaseMixin

from ...form_validators import AeInitialFormValidator


class TestAeInitialFormValidator(SiteTestCaseMixin, TestCase):
    def test_ae_cause_yes(self):
        options = {"ae_cause": YES, "ae_cause_other": None}
        form_validator = AeInitialFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("ae_cause_other", form_validator._errors)

    def test_ae_cause_no(self):
        cleaned_data = {"ae_cause": NO, "ae_cause_other": YES}
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        self.assertIn("ae_cause_other", form_validator._errors)
        self.assertIn(NOT_REQUIRED_ERROR, form_validator._error_codes)

    def test_fluconazole_relation_invalid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "amphotericin_relation": "possibly_related",
            "flucytosine_relation": "possibly_related",
            "fluconazole_relation": NOT_APPLICABLE,
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_relation", form_validator._errors)

    def test_amphotericin_relation_invalid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "fluconazole_relation": "possibly_related",
            "flucytosine_relation": "possibly_related",
            "amphotericin_relation": NOT_APPLICABLE,
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("amphotericin_relation", form_validator._errors)

    def test_flucytosine_relation_invalid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "fluconazole_relation": "possibly_related",
            "amphotericin_relation": "not_related",
            "flucytosine_relation": NOT_APPLICABLE,
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("flucytosine_relation", form_validator._errors)

    def test_fluconazole_relation_valid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "amphotericin_relation": "not_related",
            "flucytosine_relation": "not_related",
            "fluconazole_relation": "possibly_related",
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_amphotericin_relation_valid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "fluconazole_relation": "possibly_related",
            "flucytosine_relation": "not_related",
            "amphotericin_relation": "possibly_related",
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_flucytosine_relation_valid(self):
        cleaned_data = {
            "ae_study_relation_possibility": YES,
            "fluconazole_relation": "possibly_related",
            "amphotericin_relation": "possibly_related",
            "flucytosine_relation": "not_related",
        }
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_sae_reason_not_applicable(self):
        sae_reason = SaeReason.objects.get(name=NOT_APPLICABLE)
        cleaned_data = {"sae": YES, "sae_reason": sae_reason}
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("sae_reason", form_validator._errors)

    def test_susar_reported_not_applicable(self):
        cleaned_data = {"susar": YES, "susar_reported": NOT_APPLICABLE}
        form_validator = AeInitialFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("susar_reported", form_validator._errors)
