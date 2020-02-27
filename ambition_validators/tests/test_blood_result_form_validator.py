from ambition_sites import ambition_sites, fqdn
from ambition_visit_schedule import DAY1
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_base.sites.utils import add_or_update_django_sites
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, POS, NOT_APPLICABLE
from edc_reportable import GRAMS_PER_DECILITER, IU_LITER, TEN_X_9_PER_LITER
from edc_reportable import MICROMOLES_PER_LITER, MILLIGRAMS_PER_DECILITER
from edc_reportable import MILLIMOLES_PER_LITER

from ..form_validators import BloodResultFormValidator
from .models import SubjectVisit, SubjectConsent, BloodResult


class TestBloodResultFormValidator(TestCase):

    @classmethod
    def setUpClass(cls):
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn, verbose=True)
        return super().setUpClass()

    def setUp(self):

        self.subject_consent = SubjectConsent.objects.create(
            subject_identifier='11111111',
            gender='M', dob=(get_utcnow() - relativedelta(years=25)).date())

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code=DAY1)
        self.subject_visit = SubjectVisit.objects.create(
            appointment=appointment)

        self.cleaned_data = {
            'haemoglobin': 15,
            'haemoglobin_units': GRAMS_PER_DECILITER,
            'haemoglobin_abnormal': NO,
            'haemoglobin_reportable': NOT_APPLICABLE,
            'alt': 10,
            'alt_units': IU_LITER,
            'alt_abnormal': NO,
            'alt_reportable': NOT_APPLICABLE,

            'magnesium': .8,
            'magnesium_units': MILLIMOLES_PER_LITER,
            'magnesium_abnormal': NO,
            'magnesium_reportable': NOT_APPLICABLE,

            'creatinine': 100,
            'creatinine_units': MICROMOLES_PER_LITER,
            'creatinine_abnormal': NO,
            'creatinine_reportable': NOT_APPLICABLE,
            'alt_abnormal': NO,
            'alt_reportable': NOT_APPLICABLE,
            'neutrophil': 3,
            'neutrophil_units': TEN_X_9_PER_LITER,
            'neutrophil_abnormal': NO,
            'neutrophil_reportable': NOT_APPLICABLE,
            'sodium': 135,
            'sodium_units': MILLIMOLES_PER_LITER,
            'sodium_abnormal': NO,
            'sodium_reportable': NOT_APPLICABLE,
            'potassium': 4.0,
            'potassium_units': MILLIMOLES_PER_LITER,
            'potassium_abnormal': NO,
            'potassium_reportable': NOT_APPLICABLE,
            'platelets': 450,
            'platelets_units': TEN_X_9_PER_LITER,
            'platelets_abnormal': NO,
            'platelets_reportable': NOT_APPLICABLE,
            'subject_visit': self.subject_visit,
            'results_normal': YES,
            'results_reportable': NOT_APPLICABLE
        }

    def test_haemoglobin_units_invalid_female(self):
        self.subject_consent.gender = 'F'
        self.subject_consent.save()
        self.cleaned_data.update(
            haemoglobin=6.4,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('haemoglobin', form_validator._errors)

    def test_haemoglobin_units_invalid_male(self):
        self.cleaned_data.update(
            haemoglobin=6.9,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('haemoglobin', form_validator._errors)

    def test_haemoglobin_units_male_valid(self):
        self.cleaned_data.update(
            haemoglobin=14,
            results_abnormal=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_no_creatinine_mg_invalid(self):
        self.cleaned_data.update(
            creatinine=0.3,
            creatinine_units=MILLIGRAMS_PER_DECILITER)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('creatinine', form_validator._errors)

    def test_no_creatinine_mg_sodium_invalid(self):
        self.cleaned_data.update(
            creatinine=900,
            creatinine_units=MICROMOLES_PER_LITER,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('creatinine', form_validator._errors)

    def test_creatinine_mg_invalid(self):
        self.cleaned_data.update(
            creatinine=2.48,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            results_abnormal=YES,)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('creatinine', form_validator._errors)

    def test_creatinine_mg(self):

        self.cleaned_data.update(
            creatinine=1.3,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            results_abnormal=NO,
            results_reportable=NOT_APPLICABLE)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')

    def test_creatinine_umol_invalid(self):
        self.cleaned_data.update(
            creatinine=217,
            creatinine_units=MICROMOLES_PER_LITER,
            are_results_normal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('creatinine', form_validator._errors)

    def test_creatinine_umol(self):

        self.cleaned_data.update(
            creatinine=100,
            creatinine_units=MICROMOLES_PER_LITER)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_magnesium_invalid(self):
        self.cleaned_data.update(
            magnesium=0.01,
            are_results_normal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('magnesium', form_validator._errors)

    def test_magnesium(self):
        self.cleaned_data.update(
            magnesium=0.35,
            results_abnormal=YES,
            results_reportable=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('magnesium', form_validator._errors)

    def test_potassium_invalid(self):
        self.cleaned_data.update(
            potassium=1.0,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('potassium', form_validator._errors)

    def test_potassium_high(self):

        self.cleaned_data.update(
            potassium=6.8,
            results_abnormal=YES,
            results_reportable=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('potassium', form_validator._errors)

    def test_potassium_low(self):
        self.cleaned_data.update(
            potassium=2.3,
            results_abnormal=YES,
            results_reportable=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('potassium', form_validator._errors)

    def test_sodium_invalid(self):
        self.cleaned_data.update(
            sodium=100,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sodium', form_validator._errors)

    def test_sodium_invalid_1(self):
        self.cleaned_data.update(
            sodium=119,
            results_abnormal=YES,
            results_reportable=NOT_APPLICABLE)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sodium', form_validator._errors)

    def test_sodium_invalid_2(self):
        self.cleaned_data.update(
            sodium=119,
            results_abnormal=YES,
            results_reportable=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sodium', form_validator._errors)

    def test_sodium(self):
        self.cleaned_data.update(
            sodium=135,
            results_abnormal=NO,
            results_reportable=NOT_APPLICABLE)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_alt_invalid(self):
        self.cleaned_data.update(
            alt=201,
            are_results_normal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('alt', form_validator._errors)

    def test_alt(self):

        self.cleaned_data.update(
            alt=10,
            results_abnormal=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_platelets_invalid(self):

        self.cleaned_data.update(
            platelets=50,
            results_abnormal=YES)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('platelets', form_validator._errors)

    def test_platelets(self):

        self.cleaned_data.update(
            platelets=450,
            results_abnormal=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')

    def test_neutrophil_invalid(self):
        self.cleaned_data.update(
            neutrophil=0.5)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('neutrophil', form_validator._errors)

    def test_neutrophil(self):

        self.cleaned_data.update(
            neutrophil=4,
            results_abnormal=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_results_reportable_invalid(self):
        self.cleaned_data.update(
            sodium=1000,
            results_abnormal=YES,
            results_reportable=NO)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('sodium', form_validator._errors)

    def test_crag_country_botswana_crag_control_result_none(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            are_results_normal=YES,
            bios_crag=YES,
            crag_control_result=NOT_APPLICABLE
        )
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('crag_control_result', form_validator._errors)

    def test_crag_country_botswana_crag_t1_result_none(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            are_results_normal=YES,
            bios_crag=YES,
            crag_control_result=POS,
            crag_t1_result=NOT_APPLICABLE
        )
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('crag_t1_result', form_validator._errors)

    @override_settings(SITE_ID=40)
    def test_crag_blantyre_crag_t1_result_none(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            are_results_normal=YES,
            bios_crag=YES,
            crag_control_result=POS,
            crag_t1_result=NOT_APPLICABLE
        )
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('crag_t1_result', form_validator._errors)

    def test_crag_country_botswana_crag_t2_result_none(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            are_results_normal=YES,
            bios_crag=YES,
            crag_control_result=POS,
            crag_t1_result=POS,
            crag_t2_result=NOT_APPLICABLE)
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('crag_t2_result', form_validator._errors)

    @override_settings(SITE_ID=20)
    def test_crag_country_zimbabwe_crag_control_result_yes(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            results_abnormal=NO,
            bios_crag=YES
        )
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bios_crag', form_validator._errors)

    @override_settings(SITE_ID=20)
    def test_crag_country_zimbabwe_crag_control_result_no(self):
        self.cleaned_data.update(
            absolute_neutrophil=4,
            are_results_normal=YES,
            bios_crag=NO
        )
        form_validator = BloodResultFormValidator(
            cleaned_data=self.cleaned_data,
            instance=BloodResult())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bios_crag', form_validator._errors)
