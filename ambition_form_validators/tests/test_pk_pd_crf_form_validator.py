from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO, YES
from edc_utils import get_utcnow

from ..form_validators import PkPdCrfFormValidator


class TestPkPdCrfFormValidator(TestCase):
    def test_flucytosine_dose_given_yes_datetime_required(self):
        cleaned_data = {"flucytosine_dose": 4500}
        for num in ["one", "two", "three", "four"]:
            cleaned_data.update(
                {
                    f"flucytosine_dose_{num}_given": YES,
                    f"flucytosine_do)se_{num}_datetime": None,
                }
            )
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(f"flucytosine_dose_one_datetime", form_validator._errors)

    def test_flucytosine_dose_given_no_datetime_not_required(self):
        cleaned_data = {"flucytosine_dose": 4500}
        for num in ["one", "two", "three", "four"]:
            cleaned_data.update(
                {
                    f"flucytosine_dose_{num}_given": NO,
                    f"flucytosine_dose_{num}_datetime": get_utcnow(),
                }
            )
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn(f"flucytosine_dose_one_datetime", form_validator._errors)

    def test_flucytosine_dose_total_incorrect(self):

        # enter incorrect total, all dose amounts shown
        cleaned_data = {"flucytosine_dose": 1}
        for num in ["one", "two", "three", "four"]:
            cleaned_data.update({f"flucytosine_dose_{num}": 5})
            cleaned_data.update({f"flucytosine_dose_{num}_given": YES})
            cleaned_data.update({f"flucytosine_dose_{num}_datetime": get_utcnow()})
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("flucytosine_dose", form_validator._errors)

    def test_flucytosine_dose_total_correct(self):
        # enter correct total, all dose amounts shown
        cleaned_data = {"flucytosine_dose": 20}
        for num in ["one", "two", "three", "four"]:
            cleaned_data.update(
                {
                    f"flucytosine_dose_{num}_given": YES,
                    f"flucytosine_dose_{num}_datetime": get_utcnow(),
                    f"flucytosine_dose_{num}": 5,
                }
            )
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"Validation error unexpectedly raised. Got {e}")

    def test_flucytosine_dose_total_correct2(self):
        # enter correct total, all dose amounts shown
        cleaned_data = {"flucytosine_dose": 40}
        for num in ["one", "two"]:
            cleaned_data.update(
                {
                    f"flucytosine_dose_{num}_given": YES,
                    f"flucytosine_dose_{num}_datetime": get_utcnow(),
                    f"flucytosine_dose_{num}": 10,
                }
            )
        for num in ["three", "four"]:
            cleaned_data.update(
                {f"flucytosine_dose_{num}_given": NO, f"flucytosine_dose_{num}": 10}
            )
        cleaned_data.update({"flucytosine_dose_reason_missed": "blah"})
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"Validation error unexpectedly raised. Got {e}")

    def test_flucytosine_missing_doses(self):
        # try total when not all doses given
        cleaned_data = {"flucytosine_dose": 40}
        for num in ["one", "two", "three"]:  # skip 'four'
            cleaned_data.update(
                {
                    f"flucytosine_dose_{num}_given": YES,
                    f"flucytosine_dose_{num}_datetime": get_utcnow(),
                    f"flucytosine_dose_{num}": 10,
                }
            )
        cleaned_data.update(
            {
                f"flucytosine_dose_four_given": YES,
                f"flucytosine_dose_four_datetime": get_utcnow(),
            }
        )
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("flucytosine_dose_four", form_validator._errors)

    def test_fluconazole_dose_given_yes(self):
        cleaned_data = {
            "fluconazole_dose_given": YES,
            "fluconazole_dose_datetime": None,
        }
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_dose_datetime", form_validator._errors)

    def test_fluconazole_dose_given_no(self):
        cleaned_data = {
            "fluconazole_dose_given": NO,
            "fluconazole_dose_datetime": get_utcnow(),
        }
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_dose_datetime", form_validator._errors)

    def test_fluconazole_dose_given_no_reason_missed_none(self):
        cleaned_data = {
            "fluconazole_dose_given": NO,
            "fluconazole_dose_datetime": None,
            "fluconazole_dose_reason_missed": None,
        }
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_dose_reason_missed", form_validator._errors)

    def test_fluconazole_dose_given_no_reason_missed_not_none(self):
        cleaned_data = {
            "fluconazole_dose_given": YES,
            "fluconazole_dose_datetime": get_utcnow(),
            "fluconazole_dose_reason_missed": "blah blah!!",
        }
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("fluconazole_dose_reason_missed", form_validator._errors)

    def test_full_ambisome_dose_given_yes(self):
        cleaned_data = {"amphotericin_given": YES, "amphotericin_formulation": None}
        for field in [
            "amphotericin_formulation",
            "amphotericin_dose",
            "amphotericin_started_datetime",
            "amphotericin_ended_datetime",
            "amphotericin_full_dose_given",
        ]:
            form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
            self.assertRaises(ValidationError, form_validator.validate)
            self.assertIn(field, form_validator._errors)
            cleaned_data.update({field: "some value"})

    def test_blood_sample_missed_no_reason_missed_none(self):
        cleaned_data = {"blood_sample_missed": YES, "blood_sample_reason_missed": None}
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("blood_sample_reason_missed", form_validator._errors)

    def test_post_dose_lp(self):
        cleaned_data = {"pre_dose_lp": NO, "post_dose_lp": None}
        form_validator = PkPdCrfFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("post_dose_lp", form_validator._errors)
