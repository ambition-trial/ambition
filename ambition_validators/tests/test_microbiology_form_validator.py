from ambition_visit_schedule import DAY1
from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES, NO, POS, NOT_APPLICABLE, OTHER
from edc_registration.models import RegisteredSubject

from ..constants import KLEBSIELLA_SPP, BACTERIA, NO_GROWTH, CRYPTOCOCCUS_NEOFORMANS
from ..form_validators import MicrobiologyFormValidator
from .models import SubjectVisit


class TestMicrobiologyFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '1234'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            randomization_datetime=get_utcnow())
        appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code=DAY1)
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

    def test_urine_culture_performed_yes_require_urine_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_performed': YES,
            'urine_taken_date': get_utcnow(),
            'urine_culture_results': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('urine_culture_results', form_validator._errors)

    def test_urine_culture_performed_no_require_urine_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_performed': NO,
            'urine_culture_results': NO_GROWTH}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_urine_culture_performed_na_given_urine_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_performed': YES,
            'urine_culture_results': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

#     def test_urine_culture_performed_yes_given_urine_culture_results(self):
#         cleaned_data = {'urine_culture_performed': YES,
#                         'urine_culture_results': NO_GROWTH}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('urine_culture_results', form_validator._errors)

    def test_pos_urine_culture_results_none_urine_culture_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_results': POS,
            'urine_culture_organism': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('urine_culture_organism', form_validator._errors)

    def test_pos_urine_results_na_urine_culture_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_results': POS,
            'urine_culture_organism': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_urine_results_with_urine_culture_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_results': POS,
            'urine_culture_organism': KLEBSIELLA_SPP}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_other_urine_culture_results_require_urine_organism_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'urine_culture_organism': OTHER,
            'urine_culture_organism_other': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('urine_culture_organism_other', form_validator._errors)

#     def test_other_urine_culture_results_na_urine_organism_other(self):
#         cleaned_data = {'urine_culture_organism': OTHER,
#                         'urine_culture_organism_other': NOT_APPLICABLE}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('urine_culture_organism', form_validator._errors)

    def test_yes_blood_culture_performed_none_blood_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_performed': YES,
            'blood_culture_results': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('blood_culture_results', form_validator._errors)

    def test_no_blood_culture_performed_none_blood_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_performed': NO,
            'blood_culture_results': POS}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('blood_culture_results', form_validator._errors)

    def test_no_blood_culture_performed_with_blood_culture_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_performed': NO,
            'blood_culture_results': NO_GROWTH}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_blood_culture_results_require_date_blood_taken(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_results': POS,
            'blood_taken_date': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

#     def test_pos_blood_culture_results_with_date_blood_taken(self):
#         cleaned_data = {'blood_culture_results': POS,
#                         'date_blood_taken': get_utcnow(),
#                         'blood_culture_organism': CRYPTOCOCCUS_NEOFORMANS}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('blood_culture_organism', form_validator._errors)

    def test_pos_blood_culture_results_require_blood_culture_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_results': POS,
            'blood_taken_date': get_utcnow().date(),
            'day_blood_taken': 1,
            'blood_culture_organism': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('blood_culture_organism', form_validator._errors)

    def test_pos_blood_culture_results_na_blood_culture_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_results': POS,
            'blood_culture_organism': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

#     def test_pos_blood_culture_results_with_blood_culture_organism(self):
#         cleaned_data = {'blood_culture_results': POS,
#                         'blood_culture_organism': CRYPTOCOCCUS_NEOFORMANS,
#                         'date_blood_taken': get_utcnow()}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('blood_culture_organism', form_validator._errors)

    def test_other_blood_culture_organism_require_culture_organism_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_organism': OTHER,
            'blood_culture_organism_other': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_blood_culture_organism_na_culture_organism_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_organism': CRYPTOCOCCUS_NEOFORMANS,
            'blood_culture_organism_other': CRYPTOCOCCUS_NEOFORMANS}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_blood_culture_organism_with_culture_organism_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_organism': OTHER,
            'blood_culture_organism_other': 'other organism'}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_blood_organism_is_bacteria_require_bacteria_identified(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_organism': BACTERIA,
            'bacteria_identified': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bacteria_identified', form_validator._errors)

    def test_blood_organism_is_bacteria_na_bacteria_identified(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'blood_culture_organism': NOT_APPLICABLE,
            'bacteria_identified': KLEBSIELLA_SPP}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bacteria_identified', form_validator._errors)

#     def test_blood_organism_is_bacteria_with_bacteria_identified(self):
#         cleaned_data = {'blood_culture_organism': BACTERIA,
#                         'bacteria_identified': 'staphylococus_aureus'}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except forms.ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_other_bacteria_identified_require_bacteria_identified_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bacteria_identified': OTHER,
            'bacteria_identified_other': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_bacteria_identified_na_bacteria_identified_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bacteria_identified': OTHER,
            'bacteria_identified_other': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

#     def test_other_bacteria_identified_with_bacteria_identified_other(self):
#         cleaned_data = {'bacteria_identified': OTHER,
#                         'bacteria_identified_other': 'other_bacteria'}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         try:
#             form_validator.validate()
#         except forms.ValidationError as e:
#             self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_pos_sputum_results_culture_require_sputum_results_positive(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'sputum_results_culture': POS,
            'sputum_results_positive': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_sputum_results_culture_na_sputum_results_positive(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'sputum_results_culture': POS,
            'sputum_results_positive': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_sputum_results_culture_with_sputum_results_positive(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'sputum_results_culture': POS,
            'sputum_results_positive': 'Value results_positive'}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_tissue_biopsy_taken_require_tissue_biopsy_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': YES,
            'tissue_biopsy_results': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

#     def test_tissue_biopsy_taken_with_tissue_biopsy_results(self):
#         cleaned_data = {'tissue_biopsy_taken': YES,
#                         'tissue_biopsy_results': NO_GROWTH}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('urine_culture_results', form_validator._errors)

    def test_no_tissue_biopsy_taken_none_tissue_biopsy_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': NO,
            'tissue_biopsy_results': POS}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('tissue_biopsy_results', form_validator._errors)

    def no_test_tissue_biopsy_taken_with_tissue_biopsy_results(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': NO,
            'tissue_biopsy_results': NO_GROWTH}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_results_none_biopsy_date(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': NO,
            'biopsy_date': get_utcnow().date()}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_results_na_biopsy_date(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': YES,
            'biopsy_date': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('biopsy_date', form_validator._errors)

    def test_pos_tissue_biopsy_results_with_day_biopsy_taken(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': YES,
            'biopsy_date': get_utcnow(),
            'tissue_biopsy_results': POS,
            'day_biopsy_taken': None}
        form = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form.validate)
        self.assertIn('day_biopsy_taken', form._errors)

#     def test_pos_tissue_biopsy_results_with_biopsy_date(self):
#         cleaned_data = {'tissue_biopsy_results': YES,
#                         'biopsy_date': get_utcnow(),
#                         'day_biopsy_taken': 3,
#                         'tissue_biopsy_organism': 'mycobacterium_tuberculosis'}
#         form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
#         self.assertRaises(ValidationError, form_validator.validate)
#         self.assertIn('day_biopsy_taken', form_validator._errors)

    def test_pos_tissue_biopsy_results_none_tissue_biopsy_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_taken': YES,
            'biopsy_date': get_utcnow(),
            'tissue_biopsy_results': POS,
            'tissue_biopsy_organism': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_pos_tissue_biopsy_results_na_tissue_biopsy_organism(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_results': POS,
            'tissue_biopsy_organism': NOT_APPLICABLE}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_tissue_biopsy_org_none_tissue_biopsy_org_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_organism': OTHER,
            'tissue_biopsy_organism_other': None}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_other_tissue_biopsy_org_with_tissue_biopsy_org_other(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'tissue_biopsy_organism': OTHER,
            'tissue_biopsy_organism_other': 'some tissue organism'}
        form_validator = MicrobiologyFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
