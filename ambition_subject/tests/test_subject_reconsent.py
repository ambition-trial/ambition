from ambition_rando.tests.ambition_test_case_mixin import AmbitionTestCaseMixin
from django.contrib.sites.models import Site
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_action_item.models import ActionItem
from edc_constants.constants import ABNORMAL, NORMAL, CLOSED
from model_bakery import baker

from ..action_items import RECONSENT_ACTION


@tag("ambition_subject")
class TestReconsent(AmbitionTestCaseMixin, TestCase):
    def test_abnormal(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=ABNORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        try:
            baker.make_recipe(
                "ambition_subject.subjectreconsent",
                subject_identifier=subject_consent.subject_identifier,
                identity=subject_consent.identity,
                user_created="erikvw",
            )
        except ValidationError:
            self.fail("ValidationError unexpectedly raised")

    def test_normal_raises(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=NORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        self.assertRaises(
            ValidationError,
            baker.make_recipe,
            "ambition_subject.subjectreconsent",
            subject_identifier=subject_consent.subject_identifier,
            identity=subject_consent.identity,
            user_created="erikvw",
        )

    def test_abnormal_creates_action(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=ABNORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        try:
            ActionItem.objects.get(
                subject_identifier=subject_consent.subject_identifier,
                action_type__name=RECONSENT_ACTION,
            )
        except ObjectDoesNotExist:
            self.fail("ActionItem unexpectedly does not exist")

    def test_abnormal_creates_only_one_action(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=ABNORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        subject_consent.save()
        subject_consent.save()
        try:
            ActionItem.objects.get(
                subject_identifier=subject_consent.subject_identifier,
                action_type__name=RECONSENT_ACTION,
            )
        except MultipleObjectsReturned:
            self.fail("More than one ActionItem unexpectedly exist")

    def test_abnormal_to_normal_deletes_new_action(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=ABNORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        subject_screening.mental_status = NORMAL
        subject_screening.save()
        subject_consent.save()
        self.assertRaises(
            ObjectDoesNotExist,
            ActionItem.objects.get,
            subject_identifier=subject_consent.subject_identifier,
            action_type__name=RECONSENT_ACTION,
        )

    def test_reconsent_updates_action_status(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", mental_status=ABNORMAL
        )
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            user_created="erikvw",
        )
        baker.make_recipe(
            "ambition_subject.subjectreconsent",
            subject_identifier=subject_consent.subject_identifier,
            identity=subject_consent.identity,
            user_created="erikvw",
        )
        action_item = ActionItem.objects.get(
            subject_identifier=subject_consent.subject_identifier,
            action_type__name=RECONSENT_ACTION,
        )
        self.assertEqual(action_item.status, CLOSED)

    @override_settings(SITE_ID=10)
    def test_site_for_reconsent1(self):
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening",
            mental_status=ABNORMAL,
            site=Site.objects.get_current(),
        )
        self.assertEqual(subject_screening.site.pk, 10)
