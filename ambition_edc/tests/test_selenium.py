# import os
# import sys
# from ambition_ae.action_items import AE_INITIAL_ACTION
# from ambition_permissions.permissions_updater import PermissionsUpdater
# from ambition_rando.randomization_list_importer import RandomizationListImporter
# from ambition_sites import ambition_sites, fqdn
# from ambition_subject.models.follow_up import FollowUp
# from ambition_visit_schedule.constants import WEEK10
# from ambition_visit_schedule.visit_schedules import VISIT_SCHEDULE, SCHEDULE
# from django.apps import apps as django_apps
# from django.conf import settings
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.management.color import color_style
# from django.test.utils import override_settings, tag
# from django.urls.base import reverse
# from django.urls.exceptions import NoReverseMatch
# from edc_action_item.models.action_item import ActionItem
# from edc_constants.constants import NEW, OPEN, CLOSED, YES
# from edc_dashboard.url_names import url_names
# from edc_facility.import_holidays import import_holidays
# from edc_lab_dashboard.dashboard_urls import dashboard_urls
# from edc_list_data.site_list_data import site_list_data
# from edc_metadata.constants import REQUIRED
# from edc_metadata.models import RequisitionMetadata
# from edc_sites.tests import SiteTestCaseMixin
# from edc_sites.utils import add_or_update_django_sites
# from edc_utils import get_utcnow
# from edc_visit_schedule.site_visit_schedules import site_visit_schedules
# from model_mommy import mommy
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver import Firefox
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from unittest.case import skipIf
#
# from .mixins import AmbitionEdcSeleniumMixin
#
# style = color_style()
#
# try:
#     TRAVIS = os.environ["TRAVIS"]
# except KeyError:
#     TRAVIS = None
#
#
# @skipIf(TRAVIS, "skipped for TravisCI")
# @tag("selenium")
# @override_settings(DEBUG=True)
# class MySeleniumTests(
#     SiteTestCaseMixin, AmbitionEdcSeleniumMixin, StaticLiveServerTestCase
# ):
#     @classmethod
#     def setUpClass(cls):
#         cls.url_names = list(
#             cls.extra_url_names
#             + list(url_names.registry.values())
#             + list(settings.LAB_DASHBOARD_URL_NAMES.values())
#             + list(dashboard_urls.values())
#         )
#         super().setUpClass()
#
#     def setUp(self):
#         add_or_update_django_sites(
#             apps=django_apps, sites=ambition_sites, fqdn=fqdn
#         )
#         RandomizationListImporter()
#         PermissionsUpdater(verbose=False)
#         import_holidays()
#         site_list_data.autodiscover()
#         options = Options()
#         if os.environ.get("TRAVIS"):
#             options.add_argument("-headless")
#         self.selenium = Firefox(firefox_options=options)
#
#     def tearDown(self):
#         self.selenium.quit()
#         super().tearDown()
#
#     def test_follow_urls(self):
#         """Follows any url that can be reversed without kwargs.
#         """
#         self.login()
#         for url_name in self.url_names:
#             try:
#                 url = reverse(url_name)
#             except NoReverseMatch:
#                 sys.stdout.write(
#                     style.ERROR(
#                         f"NoReverseMatch: {url_name} without kwargs.\n")
#                 )
#             else:
#                 sys.stdout.write(style.SUCCESS(f"{url_name} {url}\n"))
#                 self.selenium.get("%s%s" % (self.live_server_url, url))
#
#     def test_new_subject(self):
#
#         self.login(
#             group_names=self.clinic_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         subject_visit = self.go_to_subject_visit_dashboard()
#
#         # add requisition
#         requisition = RequisitionMetadata.objects.filter(
#             subject_identifier=subject_visit.subject_identifier,
#             visit_code=subject_visit.visit_code,
#             entry_status=REQUIRED,
#         ).order_by("show_order")[0]
#         element = self.wait_for(
#             by=By.ID, text=f"add-{requisition.panel_name}")
#         element.click()
#         subject_requisition = self.fill_subject_requisition(subject_visit)
#
#         # go to lab section as CLINIC user
#         self.selenium.find_element_by_name("home").click()
#         element = self.wait_for(text="Specimens")
#         element.click()
#         self.selenium.save_screenshot(
#             os.path.join(
#                 settings.BASE_DIR, "screenshots", "new_subject_lab_requisitions.png"
#             )
#         )
#         self.assertIn(
#             subject_requisition.human_readable_identifier, self.selenium.page_source
#         )
#         # log out clinic user
#         self.logout()
#
#     """TMG"""
#
#     def test_tmg(self):
#
#         self.login(
#             group_names=self.clinic_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         # go to dashboard as a clinic user
#         appointment = self.go_to_subject_visit_schedule_dashboard()
#         subject_identifier = appointment.subject_identifier
#
#         # open popover
#         self.selenium.find_element_by_link_text(
#             "Add Action linked PRN").click()
#
#         # start an AE Initial report
#         self.selenium.find_element_by_link_text(
#             "Submit AE Initial Report").click()
#
#         # Save the action Item
#         self.selenium.find_element_by_name("_save").click()
#
#         action_item = ActionItem.objects.get(
#             subject_identifier=subject_identifier,
#             action_type__name=AE_INITIAL_ACTION,
#         )
#
#         # clinic user completes AE
#         mommy.make_recipe(
#             "ambition_ae.aeinitial",
#             subject_identifier=subject_identifier,
#             ae_classification="anaemia",
#             parent_action_item=action_item,
#         )
#
#         # verify TMG Action exists
#         try:
#             ActionItem.objects.get(reference_model="ambition_ae.aetmg")
#         except ObjectDoesNotExist:
#             self.fail("Action unexpectedly does not exist")
#
#         # log out clinic user
#         self.logout()
#
#         # login as TMG user
#         self.login(group_names=self.tmg_user_group_names)
#
#         # got to TMG listboard from Home page
#         self.selenium.find_element_by_id(
#             "home_list_group_tmg_listboard").click()
#
#         self.login(
#             group_names=self.tmg_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         self.selenium.find_element_by_id(
#             "home_list_group_tmg_listboard").click()
#
#         self.selenium.save_screenshot("screenshots/tmg_screenshot1.png")
#
#         self.selenium.find_element_by_id("tmg_ae").click()
#
#         # click on New tab
#         new_tab = self.selenium.find_element_by_css_selector(
#             f'ul.nav.nav-tabs a[href="#{NEW}-tab"]'
#         )
#         new_tab.click()
#
#         self.selenium.save_screenshot("screenshots/tmg_screenshot2.png")
#
#         # view AE Initial
#         self.selenium.find_element_by_partial_link_text(
#             f"AE Initial Report"
#         ).click()
#
#         # assert on Django Admin AE Initial change-form with
#         # VIEW permissions
#         if "View AE Initial Report" not in self.selenium.page_source:
#             self.fail(
#                 f"Unexpectedly did not find text. Expected 'View AE Initial'")
#
#         self.selenium.back()
#
#         self.selenium.find_element_by_partial_link_text(
#             "TMG Report").click()
#
#         obj = self.fill_form(
#             model="ambition_ae.aetmg",
#             values={
#                 "report_status": OPEN,
#                 "ae_classification": "anaemia",
#                 "original_report_agreed": YES,
#             },
#         )
#
#         open_tab = self.selenium.find_element_by_css_selector(
#             f'ul.nav.nav-tabs a[href="#{OPEN}-tab"]'
#         )
#         open_tab.click()
#
#         self.selenium.save_screenshot("screenshots/tmg_screenshot3.png")
#
#         self.selenium.find_element_by_partial_link_text(
#             "TMG Report").click()
#
#         obj = self.fill_form(
#             model="ambition_ae.aetmg",
#             obj=obj,
#             values={
#                 "ae_classification": "anaemia",
#                 "report_status": CLOSED,
#                 "report_closed_datetime": get_utcnow(),
#                 "original_report_agreed": YES,
#             },
#             exclude=["action_identifier"],
#         )
#
#         closed_tab = self.selenium.find_element_by_css_selector(
#             f'ul.nav.nav-tabs a[href="#{CLOSED}-tab"]'
#         )
#         closed_tab.click()
#
#         self.selenium.save_screenshot("screenshots/tmg_screenshot4.png")
#
#     """ Lab """
#
#     def test_to_specimens_clinic(self):
#
#         self.login(
#             group_names=self.lab_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         self.selenium.find_element_by_id("consented_subject")
#         self.selenium.find_element_by_id("specimens")
#         for id_label in ["screened_subject"]:
#             self.assertRaises(
#                 NoSuchElementException, self.selenium.find_element_by_id, id_label
#             )
#
#         self.selenium.find_element_by_id(
#             "home_list_group_requisition_listboard"
#         ).click()
#
#         self.selenium.find_element_by_id("requisition")
#         self.selenium.find_element_by_id("receive")
#         self.selenium.find_element_by_id("pack")
#         self.selenium.find_element_by_id("manifest")
#         self.selenium.find_element_by_id("aliquot")
#
#         # CLINIC user
#         self.login(
#             group_names=self.clinic_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#         self.selenium.find_element_by_id("consented_subject")
#         self.selenium.find_element_by_id("screened_subject")
#         self.selenium.find_element_by_id("specimens")
#
#         self.selenium.find_element_by_id(
#             "home_list_group_requisition_listboard"
#         ).click()
#         self.selenium.find_element_by_id("requisition")
#         for id_label in ["receive", "pack", "manifest", "aliquot"]:
#             self.assertRaises(
#                 NoSuchElementException, self.selenium.find_element_by_id, id_label
#             )
#
#         # TMG user
#         self.login(
#             group_names=self.tmg_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         for id_label in ["home_list_group_requisition_listboard"]:
#             self.assertRaises(
#                 NoSuchElementException, self.selenium.find_element_by_id, id_label
#             )
#
#     """ Action Item / AE """
#
#     @tag("1")
#     def test_action_item(self):
#
#         self.login(
#             group_names=self.clinic_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#
#         appointment = self.go_to_subject_visit_schedule_dashboard()
#         subject_identifier = appointment.subject_identifier
#
#         # open popover
#         self.selenium.find_element_by_link_text(
#             "Add Action linked PRN").click()
#
#         # start an AE Initial report
#         self.selenium.find_element_by_link_text(
#             "Submit AE Initial Report").click()
#
#         # Save the action Item
#         self.selenium.find_element_by_name("_save").click()
#
#         # get
#         action_item = ActionItem.objects.get(
#             subject_identifier=subject_identifier,
#             action_type__name=AE_INITIAL_ACTION,
#         )
#
#         # on dashboard, click on action item popover
#         self.selenium.find_element_by_link_text(
#             action_item.action_type.display_name
#         ).click()
#
#         # open AE Initial
#         self.selenium.find_element_by_id(
#             f"referencemodel-change-{action_item.action_identifier.upper()}"
#         ).click()
#
#         # fill form, AE Initial
#         obj = mommy.prepare_recipe(action_item.reference_model)
#         model_obj = self.fill_form(
#             model=action_item.reference_model, obj=obj, verbose=False
#         )
#
#         self.assertEqual(action_item.action_identifier,
#                          model_obj.action_identifier)
#
#         # verify no longer on dashboard
#         action_item_control_id = (
#             f"referencemodel-change-{action_item.action_identifier.upper()}"
#         )
#         if action_item_control_id in self.selenium.page_source:
#             self.fail(
#                 "Unexpectedly found action_item 'id' on dashboard. "
#                 f"Got {action_item_control_id}"
#             )
#
#         # find through PRN Forms
#         self.selenium.find_element_by_link_text("PRN Lists").click()
#         # go to admin change list
#         self.selenium.find_element_by_partial_link_text(
#             "Action Items").click()
#
#         # find action identifier on changelist
#         self.assertIn(action_item.identifier, self.selenium.page_source)
#
#         # assert next action shows, if required
#         for name in [name for name in action_item.action.get_next_actions()]:
#             assert name in self.selenium.page_source
#
#     def test_week10_followup(self):
#         """Asserts the form label on WEEK10 changes according to the
#         configuration in FollowupAdmin.
#         """
#         self.login(
#             group_names=self.clinic_user_group_names, site_names=[
#                 settings.TOWN]
#         )
#         # get visit_codes for where followup form is administered
#         for visit_code, visit in (
#             site_visit_schedules.get_visit_schedule(VISIT_SCHEDULE)
#             .schedules.get(SCHEDULE)
#             .visits.items()
#         ):
#             if "ambition_subject.followup" in [c.model for c in visit.crfs]:
#                 subject_visit = self.go_to_subject_visit_dashboard(
#                     visit_schedule_name=VISIT_SCHEDULE,
#                     schedule_name=SCHEDULE,
#                     visit_code=visit_code,
#                     save_only=True,
#                 )
#                 url_name = url_names.get("subject_dashboard_url")
#                 url = reverse(
#                     url_name,
#                     kwargs={
#                         "subject_identifier": subject_visit.subject_identifier,
#                         "appointment": str(subject_visit.appointment.id),
#                     },
#                 )
#                 self.selenium.get(f"{self.live_server_url}{url}")
#                 self.selenium.find_element_by_name(
#                     f'id_{FollowUp._meta.label_lower.replace(".", "_")}'
#                 ).click()
#                 if visit_code == WEEK10:
#                     self.assertIn(
#                         "Were any of the following antibiotics given since week two?",
#                         self.selenium.page_source,
#                     )
#                 else:
#                     self.assertNotIn(
#                         "Were any of the following antibiotics",
#                         self.selenium.page_source,
#                     )
