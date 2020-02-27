from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag

from ..reportables import age_evaluator


class TestAgeEvaluator(AmbitionTestCaseMixin, TestCase):
    def test_eligibility_invalid_age_in_years(self):
        self.assertFalse(age_evaluator.eligible(17))
        self.assertTrue(age_evaluator.eligible(18))
        self.assertTrue(age_evaluator.eligible(19))

    def test_eligibility_invalid_age_in_years_reasons_ineligible(self):
        age_evaluator.eligible(17)
        self.assertIn("age<18.", age_evaluator.reasons_ineligible)
        age_evaluator.eligible(18)
        self.assertIsNone(age_evaluator.reasons_ineligible)
