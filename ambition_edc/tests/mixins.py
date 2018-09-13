import os

from ambition_auth.group_names import (
    CLINIC_USER_GROUPS, LAB_USER_GROUPS, TMG_USER_GROUPS)
from ambition_sites.sites import ambition_sites
from ambition_subject.constants import PATIENT
from django.apps import apps as django_apps
from django.conf import settings
from django.urls.base import reverse
from edc_action_item.models.action_type import ActionType
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models.appointment import Appointment
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin, SeleniumUtilsMixin
from model_mommy import mommy
from selenium.webdriver.common.by import By
from edc_visit_tracking.constants import SCHEDULED
from edc_constants.constants import YES
from edc_base.utils import get_utcnow
from edc_lab.constants import TUBE


class AmbitionEdcSeleniumMixin(
        SeleniumLoginMixin, SeleniumModelFormMixin, SeleniumUtilsMixin):

    clinic_user_group_names = CLINIC_USER_GROUPS
    lab_user_group_names = LAB_USER_GROUPS
    tmg_user_group_names = TMG_USER_GROUPS

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    subject_visit_model = 'ambition_subject.subjectvisit'
    subject_requisition_model = 'ambition_subject.subjectrequisition'
    action_item_model = 'edc_action_item.actionitem'
    extra_url_names = ['home_url', 'administration_url']

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def go_to_subject_visit_schedule_dashboard(self):
        """Add screening, add subject consent, proceed
        to dashboard and update appointment to in_progress.
        """
        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'screening_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject1.png'))

        element = self.wait_for('Add Subject Screening')
        element.click()

        # add a subject screening form
        model_obj = self.fill_subject_screening()
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject2.png'))

        # add a subject consent for the newly screened subject
        element = self.wait_for(
            text=f'subjectconsent_add_{model_obj.screening_identifier}',
            by=By.ID)
        element.click()

        model_obj = self.fill_subject_consent(model_obj)
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject3.png'))
        subject_identifier = model_obj.subject_identifier

        # set appointment in progress
        appointment = self.fill_appointment_in_progress(subject_identifier)
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject4.png'))

        return appointment

    def go_to_subject_visit_dashboard(self, visit_code=None):
        appointment = self.go_to_subject_visit_schedule_dashboard()
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject5.png'))
        self.selenium.find_element_by_partial_link_text('Start').click()
        subject_visit = self.fill_subject_visit(appointment)
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject6.png'))
        self.wait_for_edc()
        return subject_visit

    def fill_subject_screening(self):
        """Add a subject screening form.
        """
        obj = mommy.prepare_recipe(self.subject_screening_model)
        model_obj = self.fill_form(
            model=self.subject_screening_model,
            obj=obj, exclude=['subject_identifier', 'report_datetime'])
        self.wait_for_edc()
        return model_obj

    def fill_subject_consent(self, model_obj):
        """Add a subject consent for the newly screening subject.
        """
        obj = mommy.prepare_recipe(
            self.subject_consent_model,
            **{'screening_identifier': model_obj.screening_identifier,
               'dob': model_obj.estimated_dob,
               'gender': model_obj.gender})
        obj.initials = f'{obj.first_name[0]}{obj.last_name[0]}'
        model_obj = self.fill_form(
            model=self.subject_consent_model, obj=obj,
            exclude=['subject_identifier', 'citizen', 'legal_marriage',
                     'marriage_certificate', 'subject_type',
                     'gender', 'study_site'],
            verbose=False)
        self.wait_for_edc()
        return model_obj

    def fill_appointment_in_progress(self, subject_identifier):
        appointment = Appointment.objects.filter(
            subject_identifier=subject_identifier).order_by('timepoint')[0]
        self.selenium.find_element_by_id(
            f'start_btn_{appointment.visit_code}_'
            f'{appointment.visit_code_sequence}').click()
        model_obj = self.fill_form(
            model=self.appointment_model, obj=appointment,
            values={'appt_status': IN_PROGRESS_APPT,
                    'appt_reason': SCHEDULED_APPT},
            exclude=['subject_identifier',
                     'timepoint_datetime', 'timepoint_status',
                     'facility_name'],
            verbose=False)
        self.wait_for_edc()
        return model_obj

    def fill_subject_visit(self, appointment):
        obj = mommy.prepare_recipe(
            self.subject_visit_model,
            **{'appointment': appointment,
               'reason': SCHEDULED,
               'info_source': PATIENT})
        model_obj = self.fill_form(
            model=self.subject_visit_model, obj=obj,
            verbose=False)
        self.wait_for_edc()
        return model_obj

    def fill_subject_requisition(self, subject_visit):
        obj = mommy.prepare_recipe(
            self.subject_requisition_model,
            **{'subject_visit': subject_visit,
               'is_drawn': YES,
               'drawn_dateime': get_utcnow(),
               'item_type': TUBE,
               'item_count': 1,
               'estimated_volume': 0.5})
        model_obj = self.fill_form(
            model=self.subject_visit_model, obj=obj,
            verbose=False)
        self.wait_for_edc()
        return model_obj

    def fill_action_item(self, subject_identifier=None, name=None, click_add=None):
        # add action item
        if click_add:
            self.selenium.find_element_by_id(
                'edc_action_item_actionitem_add').click()
        action_type = ActionType.objects.get(name=name)
        obj = mommy.prepare_recipe(
            self.action_item_model,
            subject_identifier=subject_identifier,
            action_type=action_type)
        model_obj = self.fill_form(
            model=self.action_item_model, obj=obj,
            exclude=['action_identifier'],
            verbose=False)
        return model_obj
