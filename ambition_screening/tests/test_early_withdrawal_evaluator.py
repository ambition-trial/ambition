from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_visit_schedule.constants import DAY1
from django.test import TestCase, tag  # noqa
from edc_reportable.units import IU_LITER, TEN_X_9_PER_LITER
from model_mommy import mommy

from ..early_withdrawal_evaluator import EarlyWithdrawalEvaluator
from ..early_withdrawal_evaluator import alt_ref, neutrophil_ref, platelets_ref
from .models import SubjectVisit, BloodResult


EarlyWithdrawalEvaluator.blood_result_model = "ambition_screening.bloodresult"


class TestEarlyWithdrawalEvaluator(AmbitionTestCaseMixin, TestCase):
    def test_early_withdrawal_criteria_no(self):
        """Asserts nulls or no data evaluates False by default.
        """
        opts = dict(alt=None, neutrophil=None, platelets=None)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertFalse(obj.eligible)

    def test_early_withdrawal_criteria_with_none(self):
        """Asserts nulls or no data evaluates True if allowed.
        """
        opts = dict(alt=None, neutrophil=None, platelets=None, allow_none=True)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertTrue(obj.eligible)

    def test_early_withdrawal_criteria_ok(self):
        """Asserts valid data evaluates True.
        """
        opts = dict(alt=200, neutrophil=0.5, platelets=50, allow_none=True)
        obj = EarlyWithdrawalEvaluator(**opts)
        self.assertTrue(obj.eligible)

    def test_alt_refs(self):
        """Asserts alt > 200 not eligible.
        """
        self.assertTrue(alt_ref.in_bounds(199, units=IU_LITER))
        self.assertTrue(alt_ref.in_bounds(200, units=IU_LITER))
        self.assertFalse(alt_ref.in_bounds(201, units=IU_LITER))
        self.assertFalse(alt_ref.in_bounds(202, units=IU_LITER))

    def test_neutrophil_refs(self):
        """Asserts neutrophil < 0.5 not eligible.
        """
        self.assertFalse(neutrophil_ref.in_bounds(0.3, units=TEN_X_9_PER_LITER))
        self.assertFalse(neutrophil_ref.in_bounds(0.4, units=TEN_X_9_PER_LITER))
        self.assertTrue(neutrophil_ref.in_bounds(0.5, units=TEN_X_9_PER_LITER))
        self.assertTrue(neutrophil_ref.in_bounds(0.6, units=TEN_X_9_PER_LITER))

    def test_platelet_refs(self):
        """Asserts platelets < 50 not eligible.
        """
        self.assertFalse(platelets_ref.in_bounds(48, units=TEN_X_9_PER_LITER))
        self.assertFalse(platelets_ref.in_bounds(49, units=TEN_X_9_PER_LITER))
        self.assertTrue(platelets_ref.in_bounds(50, units=TEN_X_9_PER_LITER))
        self.assertTrue(platelets_ref.in_bounds(51, units=TEN_X_9_PER_LITER))

    def test_with_day1_blood_result_none(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        subject_identifier = "12345"
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier,
            screening_identifier=subject_screening.screening_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
        )

        BloodResult.objects.create(subject_visit=subject_visit)
        obj = EarlyWithdrawalEvaluator(
            subject_identifier=subject_identifier, allow_none=True
        )
        self.assertTrue(obj.eligible)

    def test_with_day1_blood_result1(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        subject_identifier = "12345"
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier,
            screening_identifier=subject_screening.screening_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
        )

        BloodResult.objects.create(subject_visit=subject_visit, platelets=49)
        obj = EarlyWithdrawalEvaluator(subject_identifier=subject_identifier)
        self.assertFalse(obj.eligible)
        self.assertIn("platelets", obj.reasons_ineligible)

    def test_with_day1_blood_result2(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        subject_identifier = "12345"
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier,
            screening_identifier=subject_screening.screening_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
        )

        BloodResult.objects.create(subject_visit=subject_visit, platelets=49, alt=201)
        obj = EarlyWithdrawalEvaluator(subject_identifier=subject_identifier)
        self.assertFalse(obj.eligible)
        self.assertIn("alt", obj.reasons_ineligible)
        self.assertIn("platelets", obj.reasons_ineligible)

    def test_with_day1_blood_result3(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        subject_identifier = "12345"
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier,
            screening_identifier=subject_screening.screening_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
        )

        BloodResult.objects.create(
            subject_visit=subject_visit, platelets=49, alt=201, neutrophil=0.3
        )
        obj = EarlyWithdrawalEvaluator(subject_identifier=subject_identifier)
        self.assertFalse(obj.eligible)
        self.assertIn("alt", obj.reasons_ineligible)
        self.assertIn("platelets", obj.reasons_ineligible)
        self.assertIn("neutrophil", obj.reasons_ineligible)

    def test_with_day1_blood_result4(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        subject_identifier = "12345"
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier,
            screening_identifier=subject_screening.screening_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
        )

        BloodResult.objects.create(
            subject_visit=subject_visit, platelets=50, alt=200, neutrophil=0.5
        )
        obj = EarlyWithdrawalEvaluator(subject_identifier=subject_identifier)
        self.assertTrue(obj.eligible)
        self.assertFalse(obj.reasons_ineligible)
