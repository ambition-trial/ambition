from ambition_labs.panels import csf_panel
from ambition_sites import ambition_sites, fqdn
from ambition_visit_schedule import DAY1, DAY3
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_base.sites.utils import add_or_update_django_sites
from edc_constants.constants import YES, NO, NOT_DONE, NOT_APPLICABLE

from ..form_validators import LumbarPunctureCsfFormValidator
from .models import SubjectConsent, SubjectVisit, LumbarPunctureCsf, SubjectRequisition, Panel


class TestLumbarPunctureFormValidator(TestCase):

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

        appointment = Appointment.objects.create(
            subject_identifier=self.subject_consent.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code=DAY3)
        self.subject_visit_d3 = SubjectVisit.objects.create(
            appointment=appointment)

    def test_pressure(self):

        cleaned_data = {
            'subject_visit': self.subject_visit,
            'opening_pressure': 10,
            'closing_pressure': 9}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')

        cleaned_data = {
            'subject_visit': self.subject_visit,
            'opening_pressure': 10,
            'closing_pressure': 11}

        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('closing_pressure', form_validator._errors)
        self.assertIn('Cannot be greater', str(
            form_validator._errors.get('closing_pressure')))

    def test_other_csf_culture_required(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_culture': YES,
            'other_csf_culture': None}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('is required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_other_csf_culture_not_required(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_culture': NO,
            'other_csf_culture': 'blah'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_csf_culture_not_perfomed(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_culture': NOT_DONE,
            'other_csf_culture': 'culture'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('other_csf_culture', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('other_csf_culture')))

    def test_qc_culture(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'qc_requisition': None,
            'qc_assay_datetime': None,
            'quantitative_culture': None}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail('ValidationError unexpectedly raised')

    def test_qc_culture_requisition_not_required_if_no_result(self):
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel=panel)
        requisition.panel_object = csf_panel
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'qc_requisition': requisition,
            'qc_assay_datetime': get_utcnow(),
            'quantitative_culture': None}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('This field is not required', str(
            form_validator._errors.get('qc_requisition')))

    def test_qc_assay_datetime_not_required_if_no_result(self):
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel=panel)
        requisition.panel_object = csf_panel
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'qc_requisition': None,
            'qc_assay_datetime': get_utcnow(),
            'quantitative_culture': None}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('This field is not required', str(
            form_validator._errors.get('qc_assay_datetime')))

    def test_qc_culture_requisition_required_if_value(self):
        """Requisition is required if there is a value.
        """
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'qc_requisition': None,
            'qc_assay_datetime': None,
            'quantitative_culture': '12'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('This field is required', str(
            form_validator._errors.get('qc_requisition')))

    def test_qc_assay_datetime_required_if_value(self):
        """Requisition is required if there is a value.
        """
        panel = Panel.objects.create(name=csf_panel.name)
        requisition = SubjectRequisition.objects.create(
            subject_visit=self.subject_visit,
            panel=panel)
        requisition.panel_object = csf_panel
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'qc_requisition': requisition,
            'qc_assay_datetime': None,
            'quantitative_culture': '12'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('This field is required', str(
            form_validator._errors.get('qc_assay_datetime')))

    def test_india_ink_csf_arg_not_done_invalid(self):
        """Assert that either csf_cr_ag or india_ink is done.
        """
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_cr_ag': NOT_DONE,
            'india_ink': NOT_DONE}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('csf_cr_ag', form_validator._errors)
        self.assertIn('india_ink', form_validator._errors)

    def test_csf_wbc_cell_count_not_required_day1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_wbc_cell_count': None,
        }
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail('ValidationError unexpectedly raised')

    def test_csf_wbc_cell_count_not_required_day3(self):
        cleaned_data = {
            'subject_visit': self.subject_visit_d3,
            'csf_wbc_cell_count': None,
        }
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError:
            self.fail('ValidationError unexpectedly raised')

    def test_csf_wbc_cell_count_min_max(self):
        for i in range(0, 5):
            cleaned_data = {
                'subject_visit': self.subject_visit_d3,
                'csf_wbc_cell_count': i,
            }
            form_validator = LumbarPunctureCsfFormValidator(
                cleaned_data=cleaned_data,
                instance=LumbarPunctureCsf())
            try:
                form_validator.validate()
            except ValidationError:
                self.fail(
                    f'ValidationError unexpectedly raised. '
                    f'Got {form_validator._errors}')

    def test_csf_cr_ag_no_csf_cr_ag_lfa_not_required(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_cr_ag': NOT_DONE,
            'csf_cr_ag_lfa': YES}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('csf_cr_ag_lfa', form_validator._errors)
        self.assertIn('not required', str(
            form_validator._errors.get('csf_cr_ag_lfa')))

    def test_differential_neutrophil_count_percent_limit_passed(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_wbc_cell_count': 4,
            'differential_lymphocyte_count': 50,
            'differential_lymphocyte_unit': '%',
            'differential_neutrophil_count': 125.6,
            'differential_neutrophil_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_neutrophil_count', form_validator._errors)
        self.assertIn(
            'Cannot be greater than 100%',
            str(form_validator._errors.get('differential_neutrophil_count')))

    def test_differential_lymphocyte_count_percent_limit_passed(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'csf_wbc_cell_count': 4,
            'differential_lymphocyte_count': 125.6,
            'differential_lymphocyte_unit': '%'}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('differential_lymphocyte_count', form_validator._errors)
        self.assertIn(
            'Cannot be greater than 100%',
            str(form_validator._errors.get('differential_lymphocyte_count')))

    @override_settings(SITE_ID=10)
    def test_country_specific1(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bios_crag': NOT_APPLICABLE}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bios_crag', form_validator._errors)

    @override_settings(SITE_ID=10)
    def test_country_specific2(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bios_crag': YES}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')

    @override_settings(SITE_ID=20)
    def test_country_specific3(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bios_crag': YES}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('bios_crag', form_validator._errors)

    @override_settings(SITE_ID=20)
    def test_country_specific4(self):
        cleaned_data = {
            'subject_visit': self.subject_visit,
            'bios_crag': NOT_APPLICABLE}
        form_validator = LumbarPunctureCsfFormValidator(
            cleaned_data=cleaned_data,
            instance=LumbarPunctureCsf())
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got {e}')
