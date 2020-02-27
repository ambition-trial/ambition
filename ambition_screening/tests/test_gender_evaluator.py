from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from edc_constants.constants import FEMALE, MALE

from ..eligibility import GenderEvaluator


class TestGenderEvaluator(AmbitionTestCaseMixin, TestCase):
    def test_eligibility_gender(self):
        gender_evaluator = GenderEvaluator()
        self.assertFalse(gender_evaluator.eligible)
        gender_evaluator = GenderEvaluator(gender=FEMALE, pregnant=False)
        self.assertTrue(gender_evaluator.eligible)
        gender_evaluator = GenderEvaluator(gender=MALE)
        self.assertTrue(gender_evaluator.eligible)

        gender_evaluator = GenderEvaluator(
            gender=FEMALE, pregnant=False, breast_feeding=True
        )
        self.assertFalse(gender_evaluator.eligible)

        gender_evaluator = GenderEvaluator(
            gender=FEMALE, pregnant=True, breast_feeding=False
        )
        self.assertFalse(gender_evaluator.eligible)

        gender_evaluator = GenderEvaluator(
            gender=FEMALE, pregnant=False, breast_feeding=False
        )
        self.assertTrue(gender_evaluator.eligible)

    def test_eligibility_gender_reasons_ineligibles(self):
        gender_evaluator = GenderEvaluator()
        self.assertIn("None is an invalid gender.", gender_evaluator.reasons_ineligible)
        gender_evaluator = GenderEvaluator(gender=FEMALE, pregnant=True)
        self.assertIn("pregnant.", gender_evaluator.reasons_ineligible)
        gender_evaluator = GenderEvaluator(gender="DOG")
        self.assertIn("DOG is an invalid gender.", gender_evaluator.reasons_ineligible)
        gender_evaluator = GenderEvaluator(gender=MALE)
        self.assertIsNone(gender_evaluator.reasons_ineligible)
