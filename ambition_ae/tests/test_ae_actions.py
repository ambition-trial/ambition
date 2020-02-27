# see also tests in edc_adverse_events

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag
from edc_action_item.models.action_item import ActionItem
from edc_constants.constants import YES, NO
from edc_list_data.site_list_data import site_list_data
from edc_registration.models import RegisteredSubject
from model_bakery import baker

from ..action_items import RecurrenceOfSymptomsAction


@tag("ambition_ae")
class TestAeActions(TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.subject_identifier = "12345"
        RegisteredSubject.objects.create(subject_identifier=self.subject_identifier)

    def test_no_ae_cm_recurrence_action(self):

        baker.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            susar=YES,
            susar_reported=NO,
            ae_cm_recurrence=NO,
            user_created="erikvw",
        )

        self.assertRaises(
            ObjectDoesNotExist,
            ActionItem.objects.get,
            action_type__name=RecurrenceOfSymptomsAction.name,
        )

    def test_ae_cm_recurrence_action(self):

        baker.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            susar=YES,
            susar_reported=NO,
            ae_cm_recurrence=YES,
            user_created="erikvw",
        )

        try:
            ActionItem.objects.get(action_type__name=RecurrenceOfSymptomsAction.name)
        except ObjectDoesNotExist:
            self.fail(
                "ActionItem for recurrence of syptoms unexpectedly does not exist"
            )
