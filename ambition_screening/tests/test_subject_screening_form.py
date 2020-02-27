from ambition_rando.tests import AmbitionTestCaseMixin
from copy import copy
from django.test import TestCase, tag
from edc_utils import get_utcnow
from edc_constants.constants import YES, FEMALE, NO, NOT_APPLICABLE, MALE, NORMAL

from ..forms import SubjectScreeningForm


@tag("1")
class TestSubjectScreeningForm(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        self.male_data = dict(
            subject_identifier="092-20990003-1",
            report_datetime=get_utcnow(),
            gender=MALE,
            age_in_years=25,
            meningitis_dx=YES,
            will_hiv_test=YES,
            mental_status=NORMAL,
            consent_ability=YES,
            pregnancy=NOT_APPLICABLE,
            breast_feeding=NOT_APPLICABLE,
            previous_drug_reaction=NO,
            contraindicated_meds=NO,
            received_amphotericin=NO,
            received_fluconazole=NO,
            unsuitable_for_study=NO,
        )

        self.female_data = dict(
            subject_identifier="092-20990004-2",
            report_datetime=get_utcnow(),
            gender=FEMALE,
            age_in_years=25,
            meningitis_dx=YES,
            will_hiv_test=YES,
            mental_status=NORMAL,
            consent_ability=YES,
            pregnancy=NO,
            preg_test_date=get_utcnow().date(),
            breast_feeding=NO,
            previous_drug_reaction=NO,
            contraindicated_meds=NO,
            received_amphotericin=NO,
            received_fluconazole=NO,
            unsuitable_for_study=NO,
        )

    def test_default_ok(self):
        form = SubjectScreeningForm(data=self.male_data)
        form.is_valid()
        self.assertEqual(form.errors, {})
        self.assertTrue(form.save())

        form = SubjectScreeningForm(data=self.female_data)
        form.is_valid()
        self.assertEqual(form.errors, {})
        self.assertTrue(form.save())

    def test_pregnancy(self):
        data = copy(self.female_data)
        options = [
            (NO, None, NO, "preg_test_date"),
            (NO, None, YES, "preg_test_date"),
            (YES, None, YES, None),
            (NO, get_utcnow().date(), NO, None),
            (YES, get_utcnow().date(), NO, None),
            (YES, get_utcnow().date(), YES, None),
            (YES, get_utcnow().date(), NOT_APPLICABLE, None),
            (NOT_APPLICABLE, get_utcnow().date(), NOT_APPLICABLE, "preg_test_date"),
            (NOT_APPLICABLE, None, NOT_APPLICABLE, None),
        ]
        for pregnancy, preg_test_date, breast_feeding, error_key in options:
            with self.subTest(
                pregnancy=pregnancy,
                preg_test_date=preg_test_date,
                breast_feeding=breast_feeding,
                error_key=error_key,
            ):
                data.update(
                    pregnancy=pregnancy,
                    preg_test_date=preg_test_date,
                    breast_feeding=breast_feeding,
                )
                form = SubjectScreeningForm(data=data)
                form.is_valid()
                if error_key:
                    self.assertIn(error_key, form.errors)
                else:
                    self.assertFalse(form.errors)

    def test_male_pregnancy_yes(self):
        data = copy(self.male_data)
        data.update(pregnancy=YES)
        form = SubjectScreeningForm(data=data)
        form.is_valid()
        self.assertEqual(form.errors, {"pregnancy": ["This field is not applicable."]})
