from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from edc_adverse_event.constants import RECOVERING
from edc_adverse_event.models import SaeReason
from edc_constants.constants import YES, NO, DEAD
from edc_list_data.site_list_data import site_list_data
from edc_registration.models import RegisteredSubject
from model_bakery import baker

from ..admin_site import ambition_ae_admin
from ..models import AeFollowup, AeInitial


@tag("ambition_ae")
class TestAdmin(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.subject_identifier = self.create_subject()

    def test_ae_followup_status(self):
        modeladmin = ambition_ae_admin._registry.get(AeFollowup)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        ae_followup = baker.make_recipe(
            "ambition_ae.aefollowup",
            ae_initial=ae_initial,
            followup=YES,
            subject_identifier=self.subject_identifier,
        )
        self.assertEqual(
            modeladmin.status(ae_followup), ae_followup.get_outcome_display()
        )

        ae_followup.followup = NO
        ae_followup.save()
        self.assertEqual(
            modeladmin.status(ae_followup), ae_followup.get_outcome_display()
        )

    def test_ae_followup_ae_follow_ups(self):
        modeladmin = ambition_ae_admin._registry.get(AeFollowup)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )

        ae_followup = baker.make_recipe(
            "ambition_ae.aefollowup",
            ae_initial=ae_initial,
            followup=YES,
            outcome=RECOVERING,
            subject_identifier=self.subject_identifier,
        )

        self.assertIn(ae_followup.identifier, modeladmin.follow_up_reports(ae_followup))

    def test_ae_initial_follow_up_reports(self):
        modeladmin = ambition_ae_admin._registry.get(AeInitial)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        self.assertIsNone(modeladmin.follow_up_reports(ae_initial))

        ae_followup1 = baker.make_recipe(
            "ambition_ae.aefollowup",
            ae_initial=ae_initial,
            followup=YES,
            outcome=RECOVERING,
            subject_identifier=self.subject_identifier,
        )

        ae_followup2 = baker.make_recipe(
            "ambition_ae.aefollowup",
            ae_initial=ae_initial,
            followup=NO,
            outcome=RECOVERING,
            subject_identifier=self.subject_identifier,
        )

        self.assertIn(ae_followup1.identifier, modeladmin.follow_up_reports(ae_initial))
        self.assertIn(ae_followup2.identifier, modeladmin.follow_up_reports(ae_initial))

    def test_ae_initial_if_sae_reason(self):
        modeladmin = ambition_ae_admin._registry.get(AeInitial)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        self.assertIsNone(modeladmin.follow_up_reports(ae_initial))

        sae_reason = SaeReason.objects.get(name=DEAD)
        baker.make_recipe(
            "ambition_ae.aeinitial",
            sae_reason=sae_reason,
            subject_identifier=self.subject_identifier,
        )
        self.assertTrue(modeladmin.description(ae_initial))

    def test_ae_initial_description(self):
        modeladmin = ambition_ae_admin._registry.get(AeInitial)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        self.assertTrue(modeladmin.description(ae_initial))

    def test_ae_initial_user(self):
        modeladmin = ambition_ae_admin._registry.get(AeInitial)
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        self.assertTrue(modeladmin.user(ae_initial))
