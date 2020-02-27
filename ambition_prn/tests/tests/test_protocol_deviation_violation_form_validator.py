from ambition_prn.constants import DEVIATION, VIOLATION, MEDICATION_NONCOMPLIANCE
from ambition_prn.form_validators import ProtocolDeviationViolationFormValidator
from ambition_rando.tests import AmbitionTestCaseMixin
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase, tag  # noqa
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE
from edc_utils import get_utcnow


class TestDeviationViolationFormValidator(AmbitionTestCaseMixin, TestCase):
    def test_report_type_deviation(self):
        """If deviation, safety_impact and safety_impact_details
        are not applicable.
         """

        cleaned_data = {
            "violation_datetime": get_utcnow(),
            "violation_type": MEDICATION_NONCOMPLIANCE,
            "violation_description": "test description",
            "violation_reason": "test violation reason",
            "report_type": DEVIATION,
        }

        cleaned_data.update({"safety_impact": NO, "safety_impact_details": NO})

        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("safety_impact", form_validator._errors)

        cleaned_data.update(
            {"safety_impact": NOT_APPLICABLE, "safety_impact_details": NO}
        )

        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("safety_impact_details", form_validator._errors)

    def test_report_type(self):
        """ violation_datetime is not required if it's
        a protocol deviation
         """
        field_required_list = [
            ("violation_datetime", get_utcnow()),
            ("violation_type", MEDICATION_NONCOMPLIANCE),
            ("violation_description", "test description"),
            ("violation_reason", "test violation reason"),
        ]
        for field_item in field_required_list:
            field, value = field_item
            cleaned_data = {"report_type": DEVIATION, field: value}
            form_validator = ProtocolDeviationViolationFormValidator(
                cleaned_data=cleaned_data
            )
            self.assertRaises(ValidationError, form_validator.validate)
            self.assertIn(field, form_validator._errors)

    def test_report_type1(self):
        """ report_type is DEVIATION then
        (violation_datetime, violation_type, etc) should be None.
         """
        field_required_list = [
            ("violation_datetime", None),
            ("violation_type", None),
            ("violation_description", None),
            ("violation_reason", None),
        ]
        for field_item in field_required_list:
            field, value = field_item
            cleaned_data = {"report_type": DEVIATION, field: value}
            form_validator = ProtocolDeviationViolationFormValidator(
                cleaned_data=cleaned_data
            )
            self.assertFalse(form_validator._errors)

    def test_violation(self):
        """ violation_datetime is not required if it's
        a protocol deviation
         """
        field_required_list = [
            ("violation_datetime", get_utcnow()),
            ("violation_type", MEDICATION_NONCOMPLIANCE),
            ("violation_description", "test description"),
            ("violation_reason", "test violation reason"),
        ]
        for field_item in field_required_list:
            field, value = field_item
            cleaned_data = {"report_type": VIOLATION, field: value}
            form_validator = ProtocolDeviationViolationFormValidator(
                cleaned_data=cleaned_data
            )
            self.assertFalse(form_validator._errors)

    def test_yes_safety_impact_none_details(self):
        """ Asserts safety_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {"safety_impact": YES, "safety_impact_details": None}
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("safety_impact_details", form_validator._errors)

    def test_yes_safety_impact_with_details(self):
        """ Asserts safety_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {"safety_impact": YES, "safety_impact_details": "explanation"}
        protocol_dev = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            protocol_dev.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_no_safety_impact_none_details(self):
        """ Asserts safety_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {"safety_impact": NO, "safety_impact_details": None}
        protocol_dev = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            protocol_dev.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_no_safety_impact_with_details(self):
        """ Asserts safety_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {"safety_impact": NO, "safety_impact_details": "details"}
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("safety_impact_details", form_validator._errors)

    def test_study_outcomes_impact_with_details(self):
        """ Asserts study_outcomes_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {
            "study_outcomes_impact": YES,
            "study_outcomes_impact_details": None,
        }
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("study_outcomes_impact_details", form_validator._errors)

    def test_yes_study_outcomes_impact_with_details(self):
        """ Asserts study_outcomes_impact has valid
            safety_impact_details provided.
         """
        cleaned_data = {
            "study_outcomes_impact": YES,
            "study_outcomes_impact_details": "explanation",
        }
        protocol_dev = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            protocol_dev.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_no_study_outcomes_impact_none_details(self):
        cleaned_data = {
            "study_outcomes_impact": NO,
            "study_outcomes_impact_details": None,
        }
        protocol_dev = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            protocol_dev.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_no_study_outcomes_impact_with_details(self):
        cleaned_data = {
            "study_outcomes_impact": NO,
            "study_outcomes_impact_details": "details",
        }
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("study_outcomes_impact_details", form_validator._errors)

    def test_other_protocol_violation_none_other_protocol_violation(self):
        cleaned_data = {"violation_type": OTHER, "violation_type_other": None}
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("violation_type_other", form_validator._errors)

    def test_other_protocol_violation_other_protocol_violation(self):
        cleaned_data = {
            "violation_type": OTHER,
            "violation_type_other": "some_violation",
        }
        protocol_dev = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        try:
            protocol_dev.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got{e}")

    def test_corrective_action_datetime(self):
        cleaned_data = {
            "corrective_action_datetime": get_utcnow(),
            "corrective_action": None,
        }
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("corrective_action", form_validator._errors)

        cleaned_data = {"corrective_action_datetime": None, "corrective_action": "blah"}
        form_validator = ProtocolDeviationViolationFormValidator(
            cleaned_data=cleaned_data
        )
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn("corrective_action", form_validator._errors)
