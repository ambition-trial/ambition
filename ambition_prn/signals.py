from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_constants.constants import YES, NO
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_schedule.subject_schedule import NotOnScheduleError

from .models import StudyTerminationConclusion


@receiver(
    post_save,
    weak=False,
    sender=StudyTerminationConclusion,
    dispatch_uid="study_termination_conclusion_on_post_save",
)
def study_termination_conclusion_on_post_save(sender, instance, raw, created, **kwargs):
    """Enroll to W10 if willing_to_complete_10w == YES.
    """
    if not raw:
        try:
            willing_to_complete_10w = instance.willing_to_complete_10w
        except AttributeError:
            pass
        else:
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                "ambition_prn.onschedulew10"
            )
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=instance.subject_identifier
            )
            if willing_to_complete_10w == YES:
                schedule.put_on_schedule(
                    subject_identifier=instance.subject_identifier,
                    onschedule_datetime=registered_subject.registration_datetime,
                )
            elif willing_to_complete_10w == NO:
                try:
                    schedule.take_off_schedule(
                        subject_identifier=instance.subject_identifier,
                        offschedule_datetime=registered_subject.registration_datetime,
                    )
                except NotOnScheduleError:
                    pass
