from edc_visit_schedule import Schedule

from .schedule import visit10, visit16

SCHEDULE_W10 = "schedule"

# schedule for terminated participants.
schedule_w10 = Schedule(
    name="schedule",
    verbose_name="Week 10 to Week 16 Follow-up",
    onschedule_model="ambition_prn.onschedulew10",
    offschedule_model="ambition_prn.studyterminationconclusionw10",
    consent_model="ambition_subject.subjectconsent",
    appointment_model="edc_appointment.appointment",
)


schedule_w10.add_visit(visit=visit10)
schedule_w10.add_visit(visit=visit16)
