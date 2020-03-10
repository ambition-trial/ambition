from ambition_subject.models import PkPdCrf
from django.test import TestCase, tag
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..constants import DAY7
from ..visit_schedules.schedule import schedule
from ..visit_schedules.schedule_w10 import schedule_w10
from ..visit_schedules.visit_schedule import visit_schedule, VISIT_SCHEDULE


class TestVisitSchedule(TestCase):

    #     def setUp(self):
    #         site_visit_schedules

    def test_visit_schedule_models(self):

        self.assertEqual(visit_schedule.death_report_model, "ambition_ae.deathreport")
        self.assertEqual(visit_schedule.offstudy_model, "edc_offstudy.subjectoffstudy")
        self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        self.assertEqual(schedule.onschedule_model, "ambition_prn.onschedule")
        self.assertEqual(
            schedule.offschedule_model, "ambition_prn.studyterminationconclusion"
        )
        self.assertEqual(schedule.consent_model, "ambition_subject.subjectconsent")
        self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

        self.assertEqual(schedule_w10.onschedule_model, "ambition_prn.onschedulew10")
        self.assertEqual(
            schedule_w10.offschedule_model, "ambition_prn.studyterminationconclusionw10"
        )
        self.assertEqual(schedule_w10.consent_model, "ambition_subject.subjectconsent")
        self.assertEqual(schedule_w10.appointment_model, "edc_appointment.appointment")

    def test_pkpd_on_day_7(self):
        """Asserts DAY7 includes PK/PD crf.

        See Redmine issue #52
        """
        visit_schedule = site_visit_schedules.get_visit_schedule(VISIT_SCHEDULE)
        schedule = visit_schedule.schedules.get("schedule")
        self.assertIn(
            PkPdCrf._meta.label_lower,
            [crf.model for crf in schedule.visits.get(DAY7).crfs],
        )

    @tag("1")
    def test_week2_form(self):
        """Asserts DAY7 includes PK/PD crf.

        See Redmine issue #52
        """
        visit_schedule = site_visit_schedules.get_visit_schedule(VISIT_SCHEDULE)
        schedule = visit_schedule.schedules.get("schedule")
        self.assertIn(
            PkPdCrf._meta.label_lower,
            [crf.model for crf in schedule.visits.get(DAY7).crfs],
        )
