from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import MALE, YES, NOT_APPLICABLE, NO, FEMALE

from ..form_validators import SubjectScreeningFormValidator


class TestSubjectScreeningFormValidator(TestCase):

    def test_gender(self):
        options = {
            'gender': MALE,
            'pregnancy': YES}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('pregnancy', form_validator._errors)

    def test_preg_test_date_yes(self):
        options = {
            'gender': FEMALE,
            'pregnancy': YES,
            'preg_test_date': None}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_preg_test_date_no(self):
        options = {
            'gender': FEMALE,
            'pregnancy': NO,
            'preg_test_date': None}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_preg_test_date_NA(self):
        options = {
            'gender': MALE,
            'pregnancy': NOT_APPLICABLE,
            'preg_test_date': get_utcnow}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('preg_test_date', form_validator._errors)

    def test_gender_male_breast_feeding_invalid(self):
        options = {
            'gender': MALE,
            'pregnancy': NOT_APPLICABLE,
            'breast_feeding': YES}
        form_validator = SubjectScreeningFormValidator(cleaned_data=options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('breast_feeding', form_validator._errors)
