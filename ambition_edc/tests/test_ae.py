from ambition_ae.action_items import AE_INITIAL_ACTION
from ambition_rando.randomization_list_importer import RandomizationListImporter
from ambition_sites import ambition_sites, fqdn
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from django.urls.base import reverse
from edc_action_item.models.action_item import ActionItem
from edc_action_item.models.action_type import ActionType
from edc_base.sites.utils import add_or_update_django_sites
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_facility.import_holidays import import_holidays
from edc_lab_dashboard.dashboard_urls import dashboard_urls
from edc_list_data.site_list_data import site_list_data
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin
from model_mommy import mommy
from selenium.webdriver.firefox.webdriver import WebDriver

from .mixins import AmbitionEdcMixin


style = color_style()


@override_settings(DEBUG=True)
class MySeleniumTests(SiteTestCaseMixin, SeleniumLoginMixin, SeleniumModelFormMixin,
                      AmbitionEdcMixin, StaticLiveServerTestCase):

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    action_item_model = 'edc_action_item.actionitem'
    extra_url_names = ['home_url', 'administration_url']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(3)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn)
        RandomizationListImporter()
        import_holidays()
        site_list_data.autodiscover()
        url_names = (self.extra_url_names
                     + list(settings.DASHBOARD_URL_NAMES.values())
                     + list(settings.LAB_DASHBOARD_URL_NAMES.values())
                     + list(dashboard_urls.values()))
        self.url_names = list(set(url_names))
        super().setUp()

    def go_to_subject_dashboard(self):
        """Login, add screening, add subject consent, proceed
        to dashboard and update appointment to in_progress.
        """

        self.login()

        url = reverse(settings.DASHBOARD_URL_NAMES.get(
            'screening_listboard_url'))
        self.selenium.get('%s%s' % (self.live_server_url, url))
        self.selenium.find_element_by_id('subjectscreening_add').click()

        # add a subject screening form
        model_obj = self.add_subject_screening()

        # add a subject consent for the newly screening subject
        self.selenium.find_element_by_id(
            f'subjectconsent_add_{model_obj.screening_identifier}').click()

        model_obj = self.add_subject_consent(model_obj)
        subject_identifier = model_obj.subject_identifier

        # set appointment in progress
        self.update_appointment_in_progress(subject_identifier)

        return subject_identifier

    def add_action_item(self, subject_identifier=None, name=None, click_add=None):
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

    def test_action_item(self):

        subject_identifier = self.go_to_subject_dashboard()

        # open popover
        self.selenium.find_element_by_link_text(
            'Add Action linked PRN').click()

        # start an AE Initial report
        self.selenium.find_element_by_link_text(
            'Submit AE Initial Report').click()

        self.selenium.implicitly_wait(2)

        # Save the action Item
        self.selenium.find_element_by_name('_save').click()

        # get
        action_item = ActionItem.objects.get(
            subject_identifier=subject_identifier,
            action_type__name=AE_INITIAL_ACTION)

        # on dashboard, click on action item popover
        self.selenium.find_element_by_link_text(
            action_item.action_type.display_name).click()

        # open AE Initial
        self.selenium.find_element_by_id(
            f'referencemodel-change-{action_item.action_identifier.upper()}').click()

        self.selenium.implicitly_wait(2)

        # fill form, AE Initial
        obj = mommy.prepare_recipe(action_item.reference_model)
        model_obj = self.fill_form(
            model=action_item.reference_model, obj=obj,
            verbose=True)

        assert action_item.action_identifier == model_obj.action_identifier

        self.selenium.implicitly_wait(2)

        # verify no longer on dashboard
        action_item_control_id = (
            f'referencemodel-change-{action_item.action_identifier.upper()}')
        if (action_item_control_id in self.selenium.page_source):
            self.fail(
                f'Unexpectedly found id on dashboard. Got {action_item_control_id}')

        # find through PRN Forms
        self.selenium.find_element_by_link_text(
            'PRN Lists').click()
        # go to admin change list
        self.selenium.find_element_by_partial_link_text(
            'Action Items').click()

        # find action identifier on changelist
        assert action_item.identifier in self.selenium.page_source

        # assert next action shows, if required
        for name in [a.name for a in action_item.action.get_next_actions()]:
            assert name in self.selenium.page_source
