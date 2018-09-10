from ambition_auth.permissions_updater import PermissionsUpdater
from ambition_rando.randomization_list_importer import RandomizationListImporter
from ambition_sites import ambition_sites, fqdn
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from edc_action_item.models.action_item import ActionItem
from edc_base.sites.utils import add_or_update_django_sites
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import NEW, OPEN, CLOSED
from edc_facility.import_holidays import import_holidays
from edc_lab_dashboard.dashboard_urls import dashboard_urls
from edc_list_data.site_list_data import site_list_data
from edc_selenium.mixins import SeleniumLoginMixin, SeleniumModelFormMixin
from model_mommy import mommy

from .mixins import AmbitionEdcMixin, AmbitionEdcSeleniumMixin


style = color_style()


@override_settings(DEBUG=True)
class TmgSeleniumTests(SiteTestCaseMixin, SeleniumLoginMixin, SeleniumModelFormMixin,
                       AmbitionEdcMixin, AmbitionEdcSeleniumMixin,
                       StaticLiveServerTestCase):

    default_sites = ambition_sites
    appointment_model = 'edc_appointment.appointment'
    subject_screening_model = 'ambition_screening.subjectscreening'
    subject_consent_model = 'ambition_subject.subjectconsent'
    action_item_model = 'edc_action_item.actionitem'
    extra_url_names = ['home_url', 'administration_url']

    def setUp(self):
        PermissionsUpdater(verbose=False)
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

    def test_tmg(self):

        self.login(group_names=['TMG', 'EVERYONE', 'ADMINISTRATION'])

        self.selenium.find_element_by_id(
            'home_list_group_tmg_listboard').click()

        for status in [NEW, OPEN, CLOSED]:
            self.selenium.find_element_by_css_selector(
                f'ul.nav.nav-tabs a[href="#{status}-tab"]').click()

    @tag('1')
    def test_tmg2(self):

        # go to dashboard as a clinic user
        subject_identifier = self.go_to_subject_dashboard(
            group_names=['CLINIC', 'PII', 'EVERYONE', 'ADMINISTRATION'])

        # open popover
        self.selenium.find_element_by_link_text(
            'Add Action linked PRN').click()

        # start an AE Initial report
        self.selenium.find_element_by_link_text(
            'Submit AE Initial Report').click()

        # Save the action Item
        self.selenium.find_element_by_name('_save').click()

        # clinic user completes AE
        mommy.make_recipe(
            'ambition_ae.aeinitial',
            subject_identifier=subject_identifier,
            ae_classification='anaemia')

        # verify TMG Action exists
        try:
            ActionItem.objects.get(
                reference_model='ambition_ae.aetmg')
        except ObjectDoesNotExist:
            self.fail('Action unexpectedly does not exist')

        # log out clinic user
        self.logout()

        # login as TMG user
        self.login(group_names=['TMG', 'EVERYONE', 'ADMINISTRATION'])

        # got to TMG listboard from Home page
        self.selenium.find_element_by_id(
            'home_list_group_tmg_listboard').click()

        self.selenium.save_screenshot('screenshots/tmg_screenshot1.png')

        # click on New tab
        new_tab = self.selenium.find_element_by_css_selector(
            f'ul.nav.nav-tabs a[href="#{NEW}-tab"]')
        new_tab.click()

        self.selenium.save_screenshot('screenshots/tmg_screenshot2.png')

        # view AE Initial
        self.selenium.find_element_by_partial_link_text(
            f'AE Initial Report').click()

        # assert on Django Admin AE Initial change-form with
        # VIEW permissions
        if ('View AE Initial Report' not in self.selenium.page_source):
            self.fail(
                f'Unexpectedly did not find text. Expected \'View AE Initial\'')

        self.selenium.back()

        self.selenium.find_element_by_partial_link_text('TMG Report').click()

        obj = self.fill_form(
            model='ambition_ae.aetmg',
            values={
                'report_status': OPEN,
                'ae_classification': 'anaemia'}
        )

        open_tab = self.selenium.find_element_by_css_selector(
            f'ul.nav.nav-tabs a[href="#{OPEN}-tab"]')
        open_tab.click()

        self.selenium.save_screenshot('screenshots/tmg_screenshot3.png')

        self.selenium.find_element_by_partial_link_text('TMG Report').click()

        obj = self.fill_form(
            model='ambition_ae.aetmg',
            obj=obj,
            values={
                'ae_classification': 'anaemia',
                'report_status': CLOSED,
                'report_closed_datetime': get_utcnow()}
        )

        closed_tab = self.selenium.find_element_by_css_selector(
            f'ul.nav.nav-tabs a[href="#{CLOSED}-tab"]')
        closed_tab.click()

        self.selenium.save_screenshot('screenshots/tmg_screenshot4.png')
