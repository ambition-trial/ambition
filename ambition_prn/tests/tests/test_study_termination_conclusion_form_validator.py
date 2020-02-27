import arrow

from ambition_lists.models import OtherDrug
from ambition_rando.constants import SINGLE_DOSE, CONTROL
from ambition_prn.constants import CONSENT_WITHDRAWAL
from ambition_prn.form_validators import StudyTerminationConclusionFormValidator as Base
from ambition_rando.tests import AmbitionTestCaseMixin
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag  # noqa
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, DEAD
from edc_form_validators import M2M_SELECTION_ONLY, M2M_INVALID_SELECTION
from edc_list_data import site_list_data
from edc_utils import get_utcnow

from ..models import Week2, SubjectVisit


class StudyTerminationConclusionFormValidator(Base):

    week2_model = "ambition_prn.week2"


class TestStudyTerminationConclusionFormValidator(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_date_not_required_if_week2_complete(self):

        subject_identifier = self.get_control_subject()
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier
        )
        # complete week2
        Week2.objects.create(subject_visit=subject_visit)

        week2_date_fields = [
            "ambi_start_date",
            "ambi_stop_date",
            "ampho_start_date",
            "ampho_stop_date",
            "flucy_start_date",
            "flucy_stop_date",
            "flucon_start_date",
            "flucon_stop_date",
        ]

        for date_field in week2_date_fields:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": NOT_APPLICABLE,
                    date_field: get_utcnow(),
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                self.assertRaises(ValidationError, form_validator.validate)
                self.assertIn(date_field, form_validator._errors)

    def test_date_required_if_week2_not_complete(self):
        """If not week 2, expect YES or NO and responses
        for each date.
        """
        subject_identifier = self.create_subject()

        # NOT_APPLICABLE not allowed for on_study_drug
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "on_study_drug": NOT_APPLICABLE,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("on_study_drug", form_validator._errors)

        # YES, NO is accepted for on_study_drug
        for response in [YES, NO]:
            with self.subTest(response=response):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": response,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                try:
                    form_validator.validate()
                except ValidationError:
                    self.fail("ValidationError unexpectedly raised")

        # if NO ... do not expect date fields
        for date_field in [
            "ampho_start_date",
            "ampho_stop_date",
            "ambi_start_date",
            "ambi_stop_date",
            "flucy_start_date",
            "flucy_stop_date",
            "flucon_start_date",
            "flucon_stop_date",
        ]:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": NO,
                    date_field: None,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                try:
                    form_validator.validate()
                except ValidationError:
                    self.fail("ValidationError unexpectedly raised")

    def test_date_required_if_week2_not_complete_single_dose(self):
        """If YES and SINGLE_DOSE... expect date fields.
        """
        subject_identifier = self.get_single_dose_subject()
        single_dose_fields = ["ambi_start_date", "ambi_stop_date"]

        for date_field in single_dose_fields:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": YES,
                    date_field: None,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                if form_validator.assignment == SINGLE_DOSE:
                    self.assertRaises(ValidationError, form_validator.validate)
                    self.assertIn(date_field, form_validator._errors)

    def test_date_required_if_week2_not_complete_control(self):
        """If YES and CONTROL... expect date fields.
        """
        subject_identifier = self.get_control_subject()
        control_fields = ["ampho_start_date", "ampho_stop_date"]

        for date_field in control_fields:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": YES,
                    date_field: None,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                if form_validator.assignment == CONTROL:
                    self.assertRaises(ValidationError, form_validator.validate)
                    self.assertIn(date_field, form_validator._errors)

    def test_m2m_not_applicable_if_week2_complete(self):
        subject_identifier = self.create_subject()
        subject_visit = SubjectVisit.objects.create(
            subject_identifier=subject_identifier
        )

        # week 2 not complete, cannot be NOT_APPLICABLE
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "drug_intervention": OtherDrug.objects.filter(name=NOT_APPLICABLE),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("drug_intervention", form_validator._errors)
        self.assertIn(M2M_INVALID_SELECTION, form_validator._error_codes)

        # week 2 complete, must be NOT_APPLICABLE
        Week2.objects.create(subject_visit=subject_visit)
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "drug_intervention": OtherDrug.objects.filter(name=NOT_APPLICABLE),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("Validation error unexpectedly raised.")

        # week 2 complete, must be NOT_APPLICABLE only!
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "drug_intervention": OtherDrug.objects.all(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("drug_intervention", form_validator._errors)
        self.assertIn(M2M_SELECTION_ONLY, form_validator._error_codes)

    def test_termination_reason_death_no_death_form_invalid(self):

        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": DEAD,
            "death_date": get_utcnow().date(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("termination_reason", form_validator._errors)

    def test_yes_discharged_after_initial_admission_none_date_discharged(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "discharged_after_initial_admission": YES,
            "initial_discharge_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("initial_discharge_date", form_validator._errors)

    def test_no_discharged_after_initial_admission_with_date_discharged(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "discharged_after_initial_admission": NO,
            "initial_discharge_date": get_utcnow,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("initial_discharge_date", form_validator._errors)

    def test_no_discharged_after_initial_admission_readmission_invalid(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "discharged_after_initial_admission": NO,
            "initial_discharge_date": None,
            "readmission_after_initial_discharge": YES,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("readmission_after_initial_discharge", form_validator._errors)

    def test_no_discharged_after_initial_admission_no_readmission_valid(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "discharged_after_initial_admission": NO,
            "initial_discharge_date": None,
            "readmission_after_initial_discharge": NOT_APPLICABLE,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_yes_readmission_none_readmission_date(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "readmission_after_initial_discharge": YES,
            "readmission_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("readmission_date", form_validator._errors)

    def test_no_readmission_with_readmission_date(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "readmission_after_initial_discharge": NO,
            "readmission_date": get_utcnow,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("readmission_date", form_validator._errors)

    def test_twilling_to_complete_10w_withdrawal_of_consent(self):
        """ Asserts willing_to_complete_10w when termination reason
            is consent_withdrawn.
        """
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "consent_withdrawn",
            "consent_withdrawal_reason": "Reason",
            "willing_to_complete_10w": NOT_APPLICABLE,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_10w", form_validator._errors)

    def test_centre_care_transfer_willing_to_complete_in_centre_given(self):
        """ Asserts willing_to_complete_centre when termination reason
            is care_transferred_to_another_institution.
        """
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "care_transferred_to_another_institution",
            "willing_to_complete_centre": NOT_APPLICABLE,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_centre", form_validator._errors)

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "care_transferred_to_another_institution",
            "willing_to_complete_centre": NO,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_yes_willing_to_complete_willing_to_complete_date(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "willing_to_complete_10w": YES,
            "willing_to_complete_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_date", form_validator._errors)

    def test_no_willing_tocomplete_10WFU_with_date_to_complete(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "willing_to_complete_10w": NO,
            "willing_to_complete_date": get_utcnow(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_date", form_validator._errors)

    def test_yes_willing_to_complete_centre_none_date_to_complete(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "willing_to_complete_centre": YES,
            "willing_to_complete_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_date", form_validator._errors)

    def test_no_willing_to_complete_centre_none_date_to_complete(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "willing_to_complete_centre": NO,
            "willing_to_complete_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_no_willing_to_complete_centreU_with_date_to_complete(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "willing_to_complete_centre": NO,
            "willing_to_complete_date": get_utcnow(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("willing_to_complete_date", form_validator._errors)

    def test_included_in_error_reason_date_provided(self):
        """ Asserts included_in_error_date when termination reason
            is error_description.
        """
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "included_in_error",
            "included_in_error": "blah blah blah blah",
            "included_in_error_date": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("included_in_error_date", form_validator._errors)

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "included_in_error",
            "included_in_error": "blah blah blah blah",
            "included_in_error_date": get_utcnow(),
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_included_in_error_reason_narrative_provided(self):
        """ Asserts included_in_error_date when termination reason
            is included_in_error.
        """
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "included_in_error",
            "included_in_error_date": get_utcnow(),
            "included_in_error": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("included_in_error", form_validator._errors)

        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": "included_in_error",
            "included_in_error_date": get_utcnow(),
            "included_in_error": "blah blah blah blah",
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_other_late_protocol_exclusion_none_date_to_complete(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "first_line_regimen": OTHER,
            "first_line_regimen_other": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("first_line_regimen_other", form_validator._errors)

    def test_other_second_line_regimen_none_second_line_regime_other(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "second_line_regimen": OTHER,
            "second_line_regimen_other": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("second_line_regimen_other", form_validator._errors)

    def test_consent_withdrawal_reason_invalid(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": CONSENT_WITHDRAWAL,
            "consent_withdrawal_reason": None,
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("consent_withdrawal_reason", form_validator._errors)

    def test_consent_withdrawal_reason_valid(self):
        subject_identifier = self.create_subject()
        cleaned_data = {
            "subject_identifier": subject_identifier,
            "termination_reason": CONSENT_WITHDRAWAL,
            "consent_withdrawal_reason": "Reason",
        }
        form_validator = StudyTerminationConclusionFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_not_required_if_not_on_study_drug(self):
        subject_identifier = self.create_subject()
        subject_identifier2 = self.create_subject()

        for date_field in [
            "ambi_start_date",
            "ambi_stop_date",
            "flucy_start_date",
            "flucy_stop_date",
        ]:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": NO,
                    date_field: None,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                try:
                    form_validator.validate()
                except ValidationError:
                    self.fail("ValidationError unexpectedly raised")
        subject_identifier = subject_identifier2
        for date_field in [
            "ampho_start_date",
            "ampho_stop_date",
            "flucy_start_date",
            "flucy_stop_date",
        ]:
            with self.subTest(date_field=date_field):
                cleaned_data = {
                    "subject_identifier": subject_identifier,
                    "on_study_drug": NO,
                    date_field: None,
                }
                form_validator = StudyTerminationConclusionFormValidator(
                    cleaned_data=cleaned_data
                )
                try:
                    form_validator.validate()
                except ValidationError:
                    self.fail("ValidationError unexpectedly raised")
