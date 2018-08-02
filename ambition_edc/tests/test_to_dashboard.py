import os
import sys

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models.appointment import Appointment
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_lab_dashboard.dashboard_urls import dashboard_urls
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin
from model_mommy import mommy
from selenium.webdriver.firefox.webdriver import WebDriver

from ambition_sites import ambition_sites

style = color_style()


@override_settings(DEBUG=True)
class MySeleniumTests(SiteTestCaseMixin, SeleniumLoginMixin, SeleniumModelFormMixin,
                      StaticLiveServerTestCase):

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    extra_url_names = ['home_url', 'administration_url']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        url_names = (self.extra_url_names
                     + list(settings.DASHBOARD_URL_NAMES.values())
                     + list(settings.LAB_DASHBOARD_URL_NAMES.values())
                     + list(dashboard_urls.values()))
        self.url_names = list(set(url_names))

    def test_follow_urls(self):
        """Follows any url that can be reversed without kwargs.
        """
        self.login()
        for url_name in self.url_names:
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                sys.stdout.write(style.ERROR(f'NoReverseMatch: {url_name}\n'))
            else:
                sys.stdout.write(style.SUCCESS(f'{url_name} {url}\n'))
                self.selenium.get('%s%s' % (self.live_server_url, url))
                self.selenium.implicitly_wait(2)

    @tag('1')
    def test_subject_screening_to_subject_dashboard(self):
        self.login()

        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'screening_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'screening_listboard.png'))
        self.selenium.implicitly_wait(3)
        self.selenium.find_element_by_id('subjectscreening_add').click()

        # add a subject screening form
        obj = mommy.prepare_recipe(self.subject_screening_model)
        model_obj = self.fill_form(
            model=self.subject_screening_model,
            obj=obj, exclude=['subject_identifier', 'report_datetime'])

        # assert back at screening listboard
        self.selenium.find_element_by_id('subjectscreening_add')

        # change a subject screening form
        self.selenium.find_element_by_id(
            f'subjectscreening_change_{model_obj.screening_identifier}').click()
        self.selenium.find_element_by_xpath(f"//input[@value='Save']").click()

        # add a subject consent for the newly screening subject
        self.selenium.find_element_by_id(
            f'subjectconsent_add_{model_obj.screening_identifier}').click()

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

        # assert reached at subject dashboard
        self.selenium.find_element_by_id(f'subject_dashboard')
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'subject_dashboard.png'))

        # set appointment in progress
        subject_identifier = model_obj.subject_identifier
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

        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'subject_dashboard2.png'))
        # assert back at subject_dashboard
        self.selenium.find_element_by_id(f'subject_dashboard')
        self.selenium.find_element_by_id(
            f'start_btn_{appointment.visit_code}_'
            f'{appointment.visit_code_sequence}').click()

    def test_jump_to_subject_dashboard(self):
        self.login()
        subject_screening = mommy.make_recipe(
            'ambition_screening.subjectscreening')
        subject_consent = mommy.make_recipe(
            'ambition_subject.subjectconsent',
            screening_identifier=subject_screening.screening_identifier)
        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'subject_dashboard_url'),
            kwargs=dict(subject_identifier=subject_consent.subject_identifier))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.find_element_by_id(f'subject_dashboard')
        self.selenium.implicitly_wait(10)
