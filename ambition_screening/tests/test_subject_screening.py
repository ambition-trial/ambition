from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from edc_constants.constants import FEMALE, YES, NORMAL, NO, MALE, NOT_APPLICABLE
from edc_form_validators.base_form_validator import NOT_APPLICABLE_ERROR
from model_mommy import mommy

from ..models import SubjectScreening


class TestSubjectScreening(AmbitionTestCaseMixin, TestCase):
    def test_eligible_with_default_recipe_criteria(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        self.assertTrue(subject_screening.eligible)
        self.assertTrue(subject_screening.gender, MALE)
        self.assertTrue(subject_screening.pregnancy, NOT_APPLICABLE)
        self.assertTrue(subject_screening.breast_feeding, NOT_APPLICABLE_ERROR)

    def test_subject_invalid_age(self):
        subject_screening = mommy.prepare_recipe(
            "ambition_screening.subjectscreening", age_in_years=17
        )
        self.assertFalse(subject_screening.eligible)

    def test_subject_age_minor_invalid_reason(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", age_in_years=17
        )
        self.assertFalse(subject_screening.eligible)
        self.assertIn(subject_screening.reasons_ineligible, "age<18.")

    def test_subject_age_valid_no_reason(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", age_in_years=18
        )
        self.assertTrue(subject_screening.eligible)
        self.assertEqual(subject_screening.reasons_ineligible, None)

    def test_subject_not_eligible_if_female_pregnant(self):
        options = {"gender": FEMALE, "pregnancy": YES}
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", **options
        )
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_previous_adverse_drug_reaction(self):
        """Assert eligibility of a participant with a previous adverse
        drug reaction.
        """
        options = {"previous_drug_reaction": YES}
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", **options
        )
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_taking_concomitant_medication(self):
        """Test eligibility of a participant taking concomitant
        medication.
        """
        options = {"contraindicated_meds": YES}
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", **options
        )
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_two_days_amphotricin_b(self):
        """Test eligibility of a participant that received two days
        amphotricin_b before screening.
        """
        options = {"received_amphotericin": YES}
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", **options
        )
        self.assertFalse(subject_screening.eligible)

    def test_subject_ineligible_took_received_fluconazole(self):
        """Assert eligibility of a participant that received two days
        fluconazole before screening.
        """
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", received_fluconazole=YES
        )
        self.assertFalse(subject_screening.eligible)

    def test_eligible_mental_status_normal(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        self.assertIn(subject_screening.mental_status, NORMAL)
        self.assertTrue(subject_screening.eligible)

    def test_ineligible_not_willing_to_hiv_test(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", will_hiv_test=NO
        )
        self.assertFalse(subject_screening.eligible)

    def test_eligible_willing_to_hiv_test(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", will_hiv_test=YES
        )
        self.assertTrue(subject_screening.eligible)

    def test_ineligible_without_consent_ability(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", consent_ability=NO
        )
        self.assertFalse(subject_screening.eligible)

    def test_ineligible_if_breastfeeding(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening",
            gender=FEMALE,
            pregnancy=NO,
            breast_feeding=YES,
        )
        self.assertFalse(subject_screening.eligible)

    def test_eligible_if_not_breastfeeding(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening",
            gender=FEMALE,
            pregnancy=NO,
            breast_feeding=NO,
        )
        self.assertTrue(subject_screening.eligible)

    def test_ineligible_if_pregnant(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", gender=FEMALE, pregnancy=YES
        )
        self.assertFalse(subject_screening.eligible)

    def test_ineligible_if_unsuitable_for_study_yes(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", unsuitable_for_study=YES
        )
        self.assertFalse(subject_screening.eligible)

    def test_eligible_if_unsuitable_for_study_no(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", unsuitable_for_study=NO
        )
        self.assertTrue(subject_screening.eligible)

    def test_screening_id_created(self):
        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        # requery
        subject_screening = SubjectScreening.objects.get(pk=subject_screening.id)
        self.assertIsNotNone(subject_screening.screening_identifier)

    def test_screening_id_unchanged_on_resave(self):
        """Test subject screening id is not changed when resaving.
        """
        obj = mommy.make_recipe("ambition_screening.subjectscreening")
        # resave
        obj.save()
        # requery
        subject_screening = SubjectScreening.objects.get(pk=obj.id)
        screening_identifier = subject_screening.screening_identifier
        self.assertEqual(obj.screening_identifier, screening_identifier)

    def test_alt(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", alt=201
        )
        self.assertFalse(subject_screening.eligible)
        self.assertEqual(
            subject_screening.reasons_ineligible,
            "High ALT: 201. Ref: x<=200.0 IU/L MF 18<=AGE years.",
        )

    def test_neutrophil(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", neutrophil=0.4
        )
        self.assertFalse(subject_screening.eligible)
        self.assertEqual(
            subject_screening.reasons_ineligible,
            "Low neutrophil: 0.4. Ref: 0.5<=x 10^9/L MF 18<=AGE years.",
        )

    def test_platelets(self):
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", platelets=49
        )
        self.assertFalse(subject_screening.eligible)
        self.assertEqual(
            subject_screening.reasons_ineligible,
            "Low platelets: 49. Ref: 50.0<=x 10^9/L MF 18<=AGE years.",
        )
