from ambition_ae.action_items import AE_INITIAL_ACTION
from ambition_rando.randomization_list_importer import RandomizationListImporter
from ambition_sites import ambition_sites
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from django.urls.base import reverse
from edc_action_item.models.action_type import ActionType
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models.appointment import Appointment
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_facility.import_holidays import import_holidays
from edc_lab_dashboard.dashboard_urls import dashboard_urls
from edc_list_data.site_list_data import site_list_data
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin
from model_mommy import mommy
from selenium.webdriver.firefox.webdriver import WebDriver


style = color_style()


@override_settings(DEBUG=True)
class MySeleniumTests(SiteTestCaseMixin, SeleniumLoginMixin, SeleniumModelFormMixin,
                      StaticLiveServerTestCase):

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    action_item_model = 'edc_action_item.actionitem'
    extra_url_names = ['home_url', 'administration_url']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        RandomizationListImporter()
        import_holidays()
        site_list_data.autodiscover()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        url_names = (self.extra_url_names
                     + list(settings.DASHBOARD_URL_NAMES.values())
                     + list(settings.LAB_DASHBOARD_URL_NAMES.values())
                     + list(dashboard_urls.values()))
        self.url_names = list(set(url_names))
        super().setUp()

    def go_to_subject_dashboard(self):

        self.login()

        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'screening_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.implicitly_wait(3)
        self.selenium.find_element_by_id('subjectscreening_add').click()
        self.selenium.implicitly_wait(10)

        # add a subject screening form
        obj = mommy.prepare_recipe(self.subject_screening_model)
        model_obj = self.fill_form(
            model=self.subject_screening_model,
            obj=obj, exclude=['subject_identifier', 'report_datetime'])

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
        return subject_identifier

    def add_action_item(self, subject_identifier=None, name=None):
        # add action item
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
            verbose=True)
        return model_obj

    def add_consented_subject(self):
        screening_model_obj = mommy.make_recipe(self.subject_screening_model)
        consent_model_obj = mommy.make_recipe(
            self.subject_consent_model,
            **{'screening_identifier': screening_model_obj.screening_identifier,
               'dob': screening_model_obj.estimated_dob,
               'gender': screening_model_obj.gender})
        consent_model_obj.initials = (
            f'{consent_model_obj.first_name[0]}{consent_model_obj.last_name[0]}')
        consent_model_obj.save()
        return consent_model_obj.subject_identifier

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @tag('3')
    def test_action_item(self):

        action_type = ActionType.objects.get(name=AE_INITIAL_ACTION)

        for _ in range(0, 5):
            self.add_consented_subject()
        subject_identifier = self.consent_model_cls.objects.all()[
            0].subject_identifier

        appointment = Appointment.objects.filter(
            subject_identifier=subject_identifier).order_by('timepoint')[0]
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.appt_reason = SCHEDULED_APPT
        appointment.save()

        self.login()

        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'subject_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.find_element_by_id(
            f'btn-subject-dashboard-{subject_identifier}').click()

        self.selenium.find_element_by_id('prn-panel-title').click()

        # add action item
        action_item = self.add_action_item(
            subject_identifier=subject_identifier,
            name=action_type.name)

        # show action item popover
        self.selenium.find_element_by_id(
            f'actionitem-{action_item.action_identifier}').click()
        self.selenium.implicitly_wait(10)

        # fill reference model for link on popover
        self.selenium.find_element_by_id(
            f'referencemodel-change-{action_item.action_identifier}').click()
        obj = mommy.prepare_recipe(action_item.reference_model)
        self.fill_form(
            model=action_item.reference_model,
            obj=obj, exclude=[
                'subject_identifier', 'action_identifier', 'tracking_identifier'])

        assert f'actionitem-{action_item.action_identifier}' not in self.selenium.page_source

        model_cls = django_apps.get_model(self.action_item_model)
        action_item = model_cls.objects.get(
            parent_reference_identifier=action_item.action_identifier)
        # parent_action_item=action_item)

        assert f'actionitem-{action_item.action_identifier}' in self.selenium.page_source

        self.selenium.implicitly_wait(10)
    # assert action removed from action items list

    # assert next action shows
