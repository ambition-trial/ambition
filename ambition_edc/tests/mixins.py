from django.conf import settings
from django.urls.base import reverse
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models.appointment import Appointment
from model_mommy import mommy
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AmbitionEdcSeleniumMixin:

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        # cls.selenium.implicitly_wait(2)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def go_to_subject_dashboard(self, **kwargs):
        """Login, add screening, add subject consent, proceed
        to dashboard and update appointment to in_progress.
        """

        self.login(**kwargs)

        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'screening_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))

        self.selenium.find_element_by_partial_link_text(
            f'Add Subject Screening').click()

        # add a subject screening form
        model_obj = self.add_subject_screening()

        # add a subject consent for the newly screening subject
        element_id = f'subjectconsent_add_{model_obj.screening_identifier}'
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.ID, element_id)))
        self.selenium.find_element_by_id(element_id).click()

        model_obj = self.add_subject_consent(model_obj)
        subject_identifier = model_obj.subject_identifier

        # set appointment in progress
        self.update_appointment_in_progress(subject_identifier)

        return subject_identifier


class AmbitionEdcMixin:

    def add_subject_screening(self):
        """Add a subject screening form.
        """
        obj = mommy.prepare_recipe(self.subject_screening_model)
        model_obj = self.fill_form(
            model=self.subject_screening_model,
            obj=obj, exclude=['subject_identifier', 'report_datetime'])
        return model_obj

    def add_subject_consent(self, model_obj):
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
            verbose=True)
        return model_obj

    def update_appointment_in_progress(self, subject_identifier):
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
            verbose=True)
        return model_obj
