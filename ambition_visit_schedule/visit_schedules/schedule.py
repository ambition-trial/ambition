from ambition_labs.panels import chemistry_panel
from dateutil.relativedelta import relativedelta
from edc_visit_schedule import Schedule, Visit as BaseVisit
from edc_visit_schedule.visit.forms_collection import FormsCollection

from ..constants import DAY1, DAY3, DAY5, DAY7, DAY14, DAY12, DAY10
from ..constants import WEEK16, WEEK10, WEEK8, WEEK6, WEEK4
from .crfs import (
    crfs_d5,
    crfs_d1,
    crfs_d3,
    crfs_d7,
    crfs_d10,
    crfs_d12,
    crfs_d14,
    crfs_w4,
    crfs_w6,
    crfs_w8,
    crfs_w10,
    crfs_w16,
    crfs_prn as default_crfs_prn,
    crfs_unscheduled as default_crfs_unscheduled,
)
from .requisitions import (
    requisitions_d1,
    requisitions_d3,
    requisitions_d5,
    requisitions_d7,
    requisitions_d10,
    requisitions_d12,
    requisitions_d14,
    requisitions_w4,
    requisitions_prn as default_requisitions_prn,
)

default_requisitions = None

SCHEDULE = "schedule"


class Visit(BaseVisit):
    def __init__(
        self,
        crfs_unscheduled=None,
        requisitions_unscheduled=None,
        crfs_prn=None,
        requisitions_prn=None,
        allow_unscheduled=None,
        **kwargs
    ):
        super().__init__(
            allow_unscheduled=True if allow_unscheduled is None else allow_unscheduled,
            crfs_unscheduled=crfs_unscheduled or default_crfs_unscheduled,
            requisitions_unscheduled=requisitions_unscheduled or default_requisitions,
            crfs_prn=crfs_prn or default_crfs_prn,
            requisitions_prn=requisitions_prn or default_requisitions_prn,
            **kwargs
        )


# schedule for new participants
schedule = Schedule(
    name=SCHEDULE,
    verbose_name="Day 1 to Week 16 Follow-up",
    onschedule_model="ambition_prn.onschedule",
    offschedule_model="ambition_prn.studyterminationconclusion",
    consent_model="ambition_subject.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


visit0 = Visit(
    code=DAY1,
    title="Day 1",
    timepoint=0,
    rbase=relativedelta(days=0),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d1,
    crfs=crfs_d1,
    requisitions_prn=FormsCollection(
        *[r for r in default_requisitions_prn if r.panel != chemistry_panel]
    ),
    facility_name="7-day clinic",
)

visit1 = Visit(
    code=DAY3,
    title="Day 3",
    timepoint=1,
    rbase=relativedelta(days=2),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d3,
    crfs=crfs_d3,
    facility_name="7-day clinic",
)

visit2 = Visit(
    code=DAY5,
    title="Day 5",
    timepoint=2,
    rbase=relativedelta(days=4),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d5,
    crfs=crfs_d5,
    facility_name="7-day clinic",
)

visit3 = Visit(
    code=DAY7,
    title="Day 7",
    timepoint=3,
    rbase=relativedelta(days=6),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d7,
    crfs=crfs_d7,
    facility_name="7-day clinic",
)

visit4 = Visit(
    code=DAY10,
    title="Day 10",
    timepoint=4,
    rbase=relativedelta(days=9),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d10,
    crfs=crfs_d10,
    facility_name="7-day clinic",
)

visit5 = Visit(
    code=DAY12,
    title="Day 12",
    timepoint=5,
    rbase=relativedelta(days=11),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=0),
    requisitions=requisitions_d12,
    crfs=crfs_d12,
    facility_name="7-day clinic",
)

visit6 = Visit(
    code=DAY14,
    title="Day 14",
    timepoint=6,
    rbase=relativedelta(days=13),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=requisitions_d14,
    crfs=crfs_d14,
    facility_name="7-day clinic",
)

visit7 = Visit(
    code=WEEK4,
    title="Week 4",
    timepoint=7,
    rbase=relativedelta(weeks=4),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=requisitions_w4,
    crfs=crfs_w4,
    facility_name="5-day clinic",
)

visit8 = Visit(
    code=WEEK6,
    title="Week 6",
    timepoint=8,
    rbase=relativedelta(weeks=6),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=None,
    crfs=crfs_w6,
    facility_name="5-day clinic",
)

visit9 = Visit(
    code=WEEK8,
    title="Week 8",
    timepoint=9,
    rbase=relativedelta(weeks=8),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=None,
    crfs=crfs_w8,
    facility_name="5-day clinic",
)

visit10 = Visit(
    code=WEEK10,
    title="Week 10",
    timepoint=10,
    rbase=relativedelta(weeks=10),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=None,
    crfs=crfs_w10,
    facility_name="5-day clinic",
)

visit16 = Visit(
    code=WEEK16,
    title="Week 16",
    timepoint=16,
    rbase=relativedelta(weeks=16),
    rlower=relativedelta(days=0),
    rupper=relativedelta(days=6),
    requisitions=None,
    crfs=crfs_w16,
    facility_name="5-day clinic",
)

schedule.add_visit(visit=visit0)
schedule.add_visit(visit=visit1)
schedule.add_visit(visit=visit2)
schedule.add_visit(visit=visit3)
schedule.add_visit(visit=visit4)
schedule.add_visit(visit=visit5)
schedule.add_visit(visit=visit6)
schedule.add_visit(visit=visit7)
schedule.add_visit(visit=visit8)
schedule.add_visit(visit=visit9)
schedule.add_visit(visit=visit10)
schedule.add_visit(visit=visit16)
