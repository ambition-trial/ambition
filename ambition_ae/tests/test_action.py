from ambition_prn.action_items import STUDY_TERMINATION_CONCLUSION_ACTION
from ambition_rando.tests import AmbitionTestCaseMixin
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase, tag  # noqa
from edc_action_item.data_fixers import fix_null_action_items
from edc_action_item.helpers import ActionItemHelper
from edc_action_item.model_wrappers import ActionItemModelWrapper
from edc_action_item.models.action_item import ActionItem
from edc_adverse_event.constants import (
    DEATH_REPORT_TMG_ACTION,
    DEATH_REPORT_ACTION,
    DEATH_REPORT_TMG_SECOND_ACTION,
)
from edc_adverse_event.models.cause_of_death import CauseOfDeath
from edc_constants.constants import CLOSED, NEW, NO, YES, OPEN, MALIGNANCY
from edc_facility.import_holidays import import_holidays
from edc_list_data.site_list_data import site_list_data
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from model_bakery import baker

from ..action_items import (
    DeathReportAction,
    DeathReportTmgAction,
    DeathReportTmgSecondAction,
)
from ..constants import CRYTOCOCCAL_MENINGITIS
from ..models import DeathReport


@tag("ambition_ae")
class TestDeathReport(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        import_holidays()
        super().setUpClass()

    def create_multiple_subjects_and_death_reports(self):

        ActionItem.objects.all().delete()
        RegisteredSubject.objects.all().delete()
        names = ["Keletso", "Tshepo", "Ogaone"]
        for i in range(0, 3):
            subject_identifier = self.create_subject(first_name=names[i])
            DeathReportAction(subject_identifier=subject_identifier)
            cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
            baker.make_recipe(
                "ambition_ae.deathreport",
                subject_identifier=subject_identifier,
                cause_of_death=cause_of_death,
            )

    def test_add_death_report_action(self):
        """Note, death report action is a "singleton" action.
        """
        subject_identifier = self.create_subject()
        action = DeathReportAction(subject_identifier=subject_identifier)
        self.assertEqual(ActionItem.objects.all().count(), 1)
        action_item = ActionItem.objects.get(action_identifier=action.action_identifier)

        # fill on death report
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )
        self.assertEqual(action.action_identifier, death_report.action_identifier)

        # attempt to create a new action
        action = DeathReportAction(subject_identifier=subject_identifier)
        # show it just picks up existing action
        self.assertEqual(action.action_identifier, action_item.action_identifier)

        # try to fill in another death report, raises IntegrityError
        self.assertRaises(
            IntegrityError,
            baker.make_recipe,
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
        )

    def test_death_report_action_urls(self):

        subject_identifier = self.create_subject()
        action = DeathReportAction(subject_identifier=subject_identifier)
        action_item = ActionItem.objects.get(action_identifier=action.action_identifier)
        action_item_model_wrapper = ActionItemModelWrapper(action_item)
        helper = ActionItemHelper(
            action_item=action_item_model_wrapper.object,
            href=action_item_model_wrapper.href,
        )

        self.assertTrue(
            helper.reference_url.startswith(f"/admin/ambition_ae/deathreport/add/")
        )

        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )

        action = DeathReportAction(subject_identifier=subject_identifier)

        action_item = ActionItem.objects.get(action_identifier=action.action_identifier)
        action_item_model_wrapper = ActionItemModelWrapper(action_item)
        helper = ActionItemHelper(
            action_item=action_item_model_wrapper.object,
            href=action_item_model_wrapper.href,
        )
        self.assertTrue(
            helper.reference_url.startswith(
                f"/admin/ambition_ae/deathreport/{str(death_report.pk)}/change/"
            )
        )

    def test_death_report_action_creates_next_actions(self):
        subject_identifier = self.create_subject()

        DeathReportAction(subject_identifier=subject_identifier)
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )
        names = [obj.action_type.name for obj in ActionItem.objects.filter(status=NEW)]
        names.sort()
        self.assertEqual(
            names, ["submit-death-report-tmg", "submit-study-termination-conclusion"]
        )

    def test_death_report_closes_action(self):
        subject_identifier = self.create_subject()
        DeathReportAction(subject_identifier=subject_identifier)
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )
        obj = ActionItem.objects.get(action_identifier=death_report.action_identifier)
        self.assertEqual(obj.status, CLOSED)

    def test_add_tmg_death_report_action_cause_matches(self):

        subject_identifier = self.create_subject()
        death_report_action = DeathReportAction(subject_identifier=subject_identifier)
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )
        self.assertEqual(
            death_report_action.action_identifier, death_report.action_identifier
        )

        # assert death report creates one TMG Death Report Action
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DEATH_REPORT_TMG_ACTION
            ).count(),
            1,
        )

        # fill in TMG report with matching cause of death
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            related_action_item=death_report_action.action_item,
            parent_action_item=death_report_action.action_item,
        )
        self.assertEqual(death_report_tmg.parent_action_item, death_report.action_item)

        self.assertEqual(death_report_tmg.related_action_item, death_report.action_item)

        # assert a second TMG Death Report Action is NOT created
        # because the cause of death matches
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DEATH_REPORT_TMG_ACTION
            ).count(),
            1,
        )

    def test_add_two_tmg_death_report_action_cause_not_matching(self):

        subject_identifier = self.create_subject()
        death_report_action = DeathReportAction(subject_identifier=subject_identifier)

        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )

        # based on death_report_action next actions creates
        # 3 actions (death, death_tmg, study termination)
        self.assertEqual(ActionItem.objects.all().count(), 3)

        # one is closed (death report), the other two are NEW
        self.assertEqual(ActionItem.objects.filter(status=NEW).count(), 2)

        # the death action item
        action_item_death = ActionItem.objects.get(
            action_identifier=death_report.action_identifier,
            parent_action_item=None,
            related_action_item=None,
            action_type__name=DEATH_REPORT_ACTION,
        )

        # the death action item links the two NEW action items
        self.assertEqual(
            ActionItem.objects.filter(parent_action_item=action_item_death).count(), 2
        )

        # as well as the parent_action_item
        try:
            ActionItem.objects.get(
                parent_action_item=action_item_death,
                related_action_item=death_report.action_item,
                action_type__name=DEATH_REPORT_TMG_ACTION,
            )
        except ObjectDoesNotExist:
            self.fail("Action item unexpectedly does not exist")

        try:
            ActionItem.objects.get(
                parent_action_item=action_item_death,
                related_action_item=None,
                action_type__name=STUDY_TERMINATION_CONCLUSION_ACTION,
            )
        except ObjectDoesNotExist:
            self.fail("Action item unexpectedly does not exist")

        # fill in TMG report with non-matching cause of death
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            report_status=CLOSED,
            report_closed_datetime=get_utcnow(),
        )

        try:
            action_item_tmg = ActionItem.objects.get(
                action_identifier=death_report_tmg.action_identifier,
                parent_action_item=death_report.action_item,
                related_action_item=death_report.action_item,
                action_type__name=DEATH_REPORT_TMG_ACTION,
            )
        except ObjectDoesNotExist:
            self.fail("Action item unexpectedly does not exist")

        # assert TMG report action is closed
        self.assertEqual(action_item_tmg.status, CLOSED)

        # assert the cause of death on the tmg report does not match the
        # death report
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        self.assertEqual(death_report_tmg.cause_of_death, cause_of_death)
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        self.assertEqual(death_report.cause_of_death, cause_of_death)

        self.assertEqual(ActionItem.objects.all().count(), 4)

        # assert a second TMG Death Report Action is created
        # by death_report_tmg1 because the cause of death
        # does not match the death report
        ActionItem.objects.get(
            parent_action_item=death_report_tmg.action_item,
            related_action_item=death_report.action_item,
            action_type__name=DEATH_REPORT_TMG_SECOND_ACTION,
        )

        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DEATH_REPORT_TMG_ACTION
            ).count(),
            1,
        )

        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DEATH_REPORT_TMG_SECOND_ACTION
            ).count(),
            1,
        )

        # resave
        death_report_tmg.save()

        # still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # fill in second TMG report with any cause of death
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg_second = baker.make_recipe(
            "ambition_ae.deathreporttmgsecond",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            related_action_item=death_report_action.action_item,
            parent_action_item=death_report_tmg.action_item,
        )

        # still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        death_report_tmg_second.save()

        # still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # resave
        death_report.save()

        # still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # resave
        death_report_tmg.save()

        # still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # delete one reference model
        action_identifier_second = death_report_tmg_second.action_identifier
        death_report_tmg_second.delete()

        # still 2 action items
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # tmg second is re-opened
        action_item = ActionItem.objects.get(
            action_identifier=action_identifier_second,
            action_type__name=DEATH_REPORT_TMG_SECOND_ACTION,
            status=NEW,
        )

        # delete the action item
        action_item.delete()

        # recreates, so still 2
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

        # set the cause of death to agree
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report_tmg.cause_of_death = cause_of_death
        death_report_tmg.cause_of_death_agreed = YES
        death_report_tmg.save()

        # cause of death agrees, so deletes unused 2nd TMG action item
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            1,
        )

        # set the cause of death to NOT agree
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg.cause_of_death = cause_of_death
        death_report_tmg.cause_of_death_agreed = NO
        death_report_tmg.save()

        # cause of death doesn't agree, so recreates 2nd TMG
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name__in=[
                    DEATH_REPORT_TMG_ACTION,
                    DEATH_REPORT_TMG_SECOND_ACTION,
                ]
            ).count(),
            2,
        )

    def test_attempt_to_delete_death_report_tmg_action_item(self):

        subject_identifier = self.create_subject()

        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=subject_identifier,
            cause_of_death=cause_of_death,
        )
        # fill in TMG report with non-matching cause of death
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            report_status=CLOSED,
            report_closed_datetime=get_utcnow(),
        )

        # attempt to delete death_report_tmg
        action_item = ActionItem.objects.get(
            action_identifier=death_report_tmg.action_identifier
        )
        self.assertRaises(ProtectedError, action_item.delete)

    def test_death_report_action(self):

        self.create_multiple_subjects_and_death_reports()

        self.assertEqual(
            ActionItem.objects.filter(action_type__name=DeathReportAction.name).count(),
            3,
        )
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DeathReportTmgAction.name
            ).count(),
            3,
        )

        subject_identifier = RegisteredSubject.objects.all()[0].subject_identifier
        death_report = DeathReport.objects.get(subject_identifier=subject_identifier)
        self.assertEqual(
            ActionItem.objects.filter(
                subject_identifier=subject_identifier,
                action_type__name=DeathReportTmgAction.name,
            ).count(),
            1,
        )
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            related_action_item=death_report.action_item,
            parent_action_item=death_report.action_item,
            report_status=CLOSED,
            report_closed_datetime=get_utcnow(),
        )
        # no additional DeathReportTmgAction created for this subject
        self.assertEqual(
            ActionItem.objects.filter(
                subject_identifier=subject_identifier,
                action_type__name=DeathReportTmgAction.name,
            ).count(),
            1,
        )
        # a DeathReportTmgSecondAction is created for this subject
        # since cause_of_death_agreed==NO
        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DeathReportTmgSecondAction.name
            ).count(),
            1,
        )

        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg_second = baker.make_recipe(
            "ambition_ae.deathreporttmgsecond",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            related_action_item=death_report.action_item,
            parent_action_item=death_report_tmg.action_item,
            report_status=OPEN,
        )
        self.assertEqual(
            ActionItem.objects.filter(
                subject_identifier=subject_identifier,
                action_type__name=DeathReportTmgAction.name,
            ).count(),
            1,
        )

        death_report_tmg_second.report_status = CLOSED
        death_report_tmg_second.report_closed_datetime = get_utcnow()
        self.assertEqual(
            ActionItem.objects.filter(
                subject_identifier=subject_identifier,
                action_type__name=DeathReportTmgSecondAction.name,
            ).count(),
            1,
        )
        self.assertEqual(
            ActionItem.objects.filter(
                subject_identifier=subject_identifier,
                action_type__name=DeathReportTmgAction.name,
            ).count(),
            1,
        )

    def test_fix_null_action_items(self):

        self.create_multiple_subjects_and_death_reports()

        subject_identifier = RegisteredSubject.objects.all()[0].subject_identifier
        death_report = DeathReport.objects.get(subject_identifier=subject_identifier)
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            related_action_item=death_report.action_item,
            parent_action_item=death_report.action_item,
            report_status=CLOSED,
            report_closed_datetime=get_utcnow(),
        )
        cause_of_death = CauseOfDeath.objects.get(name=MALIGNANCY)
        death_report_tmg_second = baker.make_recipe(
            "ambition_ae.deathreporttmgsecond",
            subject_identifier=subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
            cause_of_death_agreed=NO,
            related_action_item=death_report.action_item,
            parent_action_item=death_report_tmg.action_item,
            report_status=OPEN,
        )
        death_report_tmg_second.report_status = CLOSED
        death_report_tmg_second.report_closed_datetime = get_utcnow()

        fix_null_action_items(django_apps)

        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DeathReportTmgAction.name
            ).count(),
            3,
        )

        self.assertEqual(
            ActionItem.objects.filter(
                action_type__name=DeathReportTmgSecondAction.name
            ).count(),
            1,
        )
