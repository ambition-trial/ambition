import os
import sys

from ambition_ae.action_items import AE_INITIAL_ACTION
from ambition_auth.permissions_updater import PermissionsUpdater
from ambition_labs.panels import fbc_panel
from ambition_rando.randomization_list_importer import RandomizationListImporter
from ambition_sites import ambition_sites, fqdn
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.color import color_style
from django.test.utils import override_settings, tag
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_action_item.models.action_item import ActionItem
from edc_base import get_utcnow
from edc_base.sites.utils import add_or_update_django_sites
from edc_base.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_constants.constants import NEW, OPEN, CLOSED
from edc_facility.import_holidays import import_holidays
from edc_lab_dashboard.dashboard_urls import dashboard_urls
from edc_list_data.site_list_data import site_list_data
from model_mommy import mommy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .mixins import AmbitionEdcSeleniumMixin

style = color_style()


@override_settings(DEBUG=True)
class MySeleniumTests(SiteTestCaseMixin, AmbitionEdcSeleniumMixin,
                      StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        url_names = (cls.extra_url_names
                     + list(settings.DASHBOARD_URL_NAMES.values())
                     + list(settings.LAB_DASHBOARD_URL_NAMES.values())
                     + list(dashboard_urls.values()))
        cls.url_names = list(set(url_names))
        super().setUpClass()

    def setUp(self):
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn)
        RandomizationListImporter()
        PermissionsUpdater(verbose=False)
        import_holidays()
        site_list_data.autodiscover()
        options = Options()
        if os.environ.get('TRAVIS'):
            options.add_argument('-headless')
        self.selenium = Firefox(firefox_options=options)

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_follow_urls(self):
        """Follows any url that can be reversed without kwargs.
        """
        self.login()
        for url_name in self.url_names:
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                sys.stdout.write(style.ERROR(
                    f'NoReverseMatch: {url_name} without kwargs.\n'))
            else:
                sys.stdout.write(style.SUCCESS(f'{url_name} {url}\n'))
                self.selenium.get('%s%s' % (self.live_server_url, url))

    @tag('1')
    def test_new_subject(self):

        self.login(
            group_names=self.clinic_user_group_names,
            site_names=[settings.TOWN])

        subject_visit = self.go_to_subject_visit_dashboard()

        # add requisition
        element = self.wait_for(by=By.ID, text=f'add-{fbc_panel.name}')
        element.click()
        subject_requisition = self.fill_subject_requisition(subject_visit)

        # go to lab section as CLINIC user
        element = self.wait_for(text='Specimens')
        element.click()
        self.selenium.save_screenshot(
            os.path.join(settings.BASE_DIR, 'screenshots', 'new_subject_lab_requisitions.png'))
        self.assertIn(subject_requisition.requisition_identifier,
                      self.selenium.page_source)

    """TMG"""

    def test_tmg(self):

        self.login(group_names=self.clinic_user_group_names,
                   site_names=[settings.TOWN])

        # go to dashboard as a clinic user
        appointment = self.go_to_subject_visit_schedule_dashboard()
        subject_identifier = appointment.subject_identifier

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
        self.login(group_names=self.tmg_user_group_names)

        # got to TMG listboard from Home page
        self.selenium.find_element_by_id(
            'home_list_group_tmg_listboard').click()

        self.login(
            group_names=self.tmg_user_group_names,
            site_names=[settings.TOWN])

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

    """ Lab """

    def test_to_specimens_clinic(self):

        self.login(
            group_names=self.lab_user_group_names,
            site_names=[settings.TOWN])

        self.selenium.find_element_by_id('consented_subject')
        self.selenium.find_element_by_id('specimens')
        for id_label in ['screened_subject']:
            self.assertRaises(
                NoSuchElementException,
                self.selenium.find_element_by_id, id_label)

        self.selenium.find_element_by_id(
            'home_list_group_requisition_listboard').click()

        self.selenium.find_element_by_id('requisition')
        self.selenium.find_element_by_id('receive')
        self.selenium.find_element_by_id('pack')
        self.selenium.find_element_by_id('manifest')
        self.selenium.find_element_by_id('aliquot')

        # CLINIC user
        self.login(
            group_names=self.clinic_user_group_names,
            site_names=[settings.TOWN])
        self.selenium.find_element_by_id('consented_subject')
        self.selenium.find_element_by_id('screened_subject')
        self.selenium.find_element_by_id('specimens')

        self.selenium.find_element_by_id(
            'home_list_group_requisition_listboard').click()
        self.selenium.find_element_by_id('requisition')
        for id_label in ['receive', 'pack', 'manifest', 'aliquot']:
            self.assertRaises(
                NoSuchElementException,
                self.selenium.find_element_by_id, id_label)

        # TMG user
        self.login(
            group_names=self.tmg_user_group_names,
            site_names=[settings.TOWN])

        for id_label in ['home_list_group_requisition_listboard']:
            self.assertRaises(
                NoSuchElementException,
                self.selenium.find_element_by_id, id_label)

    """ Action Item / AE """

    def test_action_item(self):

        self.login(group_names=self.clinic_user_group_names,
                   site_names=[settings.TOWN])

        appointment = self.go_to_subject_visit_schedule_dashboard()
        subject_identifier = appointment.subject_identifier

        # open popover
        self.selenium.find_element_by_link_text(
            'Add Action linked PRN').click()

        # start an AE Initial report
        self.selenium.find_element_by_link_text(
            'Submit AE Initial Report').click()

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

        # fill form, AE Initial
        obj = mommy.prepare_recipe(action_item.reference_model)
        model_obj = self.fill_form(
            model=action_item.reference_model, obj=obj,
            verbose=False)

        self.assertEqual(action_item.action_identifier,
                         model_obj.action_identifier)

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
        self.assertIn(action_item.identifier,
                      self.selenium.page_source)

        # assert next action shows, if required
        for name in [a.name for a in action_item.action.get_next_actions()]:
            assert name in self.selenium.page_source
