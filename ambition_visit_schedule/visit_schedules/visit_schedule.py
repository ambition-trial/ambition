from edc_visit_schedule import VisitSchedule, site_visit_schedules

from .schedule import schedule
from .schedule_w10 import schedule_w10

VISIT_SCHEDULE = "visit_schedule"
VISIT_SCHEDULE_W10 = "visit_schedule_w10"


visit_schedule = VisitSchedule(
    name=VISIT_SCHEDULE,
    verbose_name="Ambition",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="ambition_ae.deathreport",
    locator_model="edc_locator.subjectlocator",
    previous_visit_schedule=None,
)

visit_schedule.add_schedule(schedule)

visit_schedule_w10 = VisitSchedule(
    name=VISIT_SCHEDULE_W10,
    verbose_name="Ambition W10",
    offstudy_model="edc_offstudy.subjectoffstudy",
    death_report_model="ambition_ae.deathreport",
    locator_model="edc_locator.subjectlocator",
    previous_visit_schedule=None,
)

visit_schedule_w10.add_schedule(schedule_w10)

site_visit_schedules.register(visit_schedule)
site_visit_schedules.register(visit_schedule_w10)
