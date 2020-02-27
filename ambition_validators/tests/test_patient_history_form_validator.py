from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE

from ..constants import HEADACHE, VISUAL_LOSS
from ..form_validators import PatientHistoryFormValidator
from .models import ListModel


class TestPatientHistoryFormValidator(TestCase):

    def test_headache_requires_headache_duration(self):
        """Assert that headache selection requires duration
        """
        ListModel.objects.create(name=HEADACHE, short_name=HEADACHE)

        cleaned_data = {'symptom': ListModel.objects.all(),
                        'headache_duration': None}
        form_validator = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('headache_duration', form_validator._errors)

    def test_visual_loss_requires_duration(self):
        """Assert that visual_loss selection requires duration
        """
        ListModel.objects.create(name=VISUAL_LOSS, short_name=VISUAL_LOSS)

        cleaned_data = {'symptom': ListModel.objects.all(),
                        'visual_loss_duration': None}
        form_validator = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('visual_loss_duration', form_validator._errors)

    def test_tb_history_yes_tb_site_none_invalid(self):
        cleaned_data = {'tb_history': YES,
                        'tb_site': NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('tb_site', form._errors)

    def test_tb_treatment_taking_rifapicin_none_invalid(self):
        cleaned_data = {'tb_treatment': YES,
                        'taking_rifampicin': NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('taking_rifampicin', form._errors)

    def test_taking_rifapicin_started_date_none_invalid(self):
        cleaned_data = {'taking_rifampicin': YES,
                        'rifampicin_started_date': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('rifampicin_started_date', form._errors)

    def test_not_new_hiv_diagnosis_taking_arv_none_invalid(self):
        cleaned_data = {'new_hiv_diagnosis': NO,
                        'taking_arv': NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('taking_arv', form._errors)

    def test_taking_arv_arv_date_none_invalid(self):
        cleaned_data = {'taking_arv': YES,
                        'arv_date': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('arv_date', form._errors)

    def test_arv_date_estimated_invalid(self):
        cleaned_data = {'arv_date': None,
                        'arv_date_estimated': YES}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('arv_date_estimated', form._errors)

    def test_arv_date_estimated_valid(self):
        cleaned_data = {'arv_date': None,
                        'arv_date_estimated': NOT_APPLICABLE}
        form_validator = PatientHistoryFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_taking_arv_first_arv_regimen_none_invalid(self):
        cleaned_data = {'taking_arv': YES,
                        'arv_date': get_utcnow(),
                        'first_arv_regimen': NOT_APPLICABLE}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('first_arv_regimen', form._errors)

    def test_taking_arv_first_arv_regimen_no(self):
        cleaned_data = {'taking_arv': NO,
                        'first_arv_regimen': 'Other'}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('first_arv_regimen', form._errors)

    def test_taking_arv_first_line_choice_no(self):
        cleaned_data = {'taking_arv': NO,
                        'first_arv_regimen': NOT_APPLICABLE,
                        'first_line_choice': 'EFV'}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('first_line_choice', form._errors)

    def test_taking_arv_patient_adherence_no(self):
        cleaned_data = {'taking_arv': NO,
                        'first_arv_regimen': NOT_APPLICABLE,
                        'first_line_choice': NOT_APPLICABLE,
                        'patient_adherence': YES}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('patient_adherence', form._errors)

    def test_first_arv_regimen_other_none_invalid(self):
        cleaned_data = {'first_arv_regimen': OTHER,
                        'first_arv_regimen_other': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('first_arv_regimen_other', form._errors)

    def test_second_arv_regimen_other_none_invalid(self):
        cleaned_data = {'second_arv_regimen': OTHER,
                        'second_arv_regimen_other': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('second_arv_regimen_other', form._errors)

    def test_taking_arv_patient_adherence_none_invalid(self):
        cleaned_data = {'taking_arv': NO,
                        'patient_adherence': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('patient_adherence', form._errors)

    def test_no_last_viral_load_date_invalid(self):
        cleaned_data = {'last_viral_load': None,
                        'viral_load_date': get_utcnow()}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('viral_load_date', form._errors)

    def test_no_viral_load_date_estimated_invalid(self):
        cleaned_data = {'viral_load_date': None,
                        'vl_date_estimated': 'blah'}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('vl_date_estimated', form._errors)

    def test_no_last_cd4_date_invalid(self):
        cleaned_data = {'last_cd4': None,
                        'cd4_date': get_utcnow()}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('cd4_date', form._errors)

    def test_no_cd4_date_estimated_invalid(self):
        cleaned_data = {'cd4_date': None,
                        'cd4_date_estimated': 'blah'}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('cd4_date_estimated', form._errors)

    def test_neurological_focal_neurologic_deficit_none_invalid(self):
        ListModel.objects.create(name='focal_neurologic_deficit',
                                 short_name='focal_neurologic_deficit')

        cleaned_data = {'neurological': ListModel.objects.all(),
                        'focal_neurologic_deficit': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('focal_neurologic_deficit', form._errors)

    def test_neurological_neurological_other_none_invalid(self):
        ListModel.objects.create(name=OTHER,
                                 short_name=OTHER)

        cleaned_data = {'neurological': ListModel.objects.all(),
                        'neurological_other': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('neurological_other', form._errors)

    def test_specify_medications_NO_other_none_invalid(self):
        ListModel.objects.create(name=OTHER,
                                 short_name=OTHER)

        cleaned_data = {'specify_medications': ListModel.objects.all(),
                        'specify_medications_other': None}
        form = PatientHistoryFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('specify_medications_other', form._errors)
