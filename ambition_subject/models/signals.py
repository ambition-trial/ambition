from ambition_rando.randomizer import Randomizer
from ambition_screening.models import SubjectScreening
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from edc_action_item import delete_action_item, ActionItemDeleteError
from edc_constants.constants import YES
from edc_randomization.site_randomizers import site_randomizers
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from ..action_items import ReconsentAction
from .subject_consent import SubjectConsent
from .subject_visit import SubjectVisit


@receiver(
    post_save,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subject_consent_on_post_save",
)
def subject_consent_on_post_save(sender, instance, raw, created, **kwargs):
    """Creates an onschedule instance for this consented subject, if
    it does not exist.
    """
    if not raw:
        if not created:
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                "ambition_prn.onschedule"
            )
            schedule.refresh_schedule(subject_identifier=instance.subject_identifier)
        else:
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=instance.screening_identifier
            )
            subject_screening.subject_identifier = instance.subject_identifier
            subject_screening.consented = True
            subject_screening.save_base(
                update_fields=["subject_identifier", "consented"]
            )

            # randomize
            Randomizer = site_randomizers.get("ambition")
            Randomizer(
                subject_identifier=instance.subject_identifier,
                report_datetime=instance.consent_datetime,
                site=instance.site,
                user=instance.user_created,
            )

            # put subject on schedule
            _, schedule = site_visit_schedules.get_by_onschedule_model(
                "ambition_prn.onschedule"
            )
            schedule.put_on_schedule(
                subject_identifier=instance.subject_identifier,
                onschedule_datetime=instance.consent_datetime,
            )

        # create / delete action for reconsent
        if instance.completed_by_next_of_kin == YES:
            ReconsentAction(subject_identifier=instance.subject_identifier)
        else:
            try:
                delete_action_item(
                    action_cls=ReconsentAction,
                    subject_identifier=instance.subject_identifier,
                )
            except ActionItemDeleteError:
                pass


@receiver(
    post_delete,
    weak=False,
    sender=SubjectConsent,
    dispatch_uid="subject_consent_on_post_delete",
)
def subject_consent_on_post_delete(sender, instance, using, **kwargs):
    """Updates/Resets subject screening.
    """
    # don't allow if subject visits exist. This should be caught
    # in the ModelAdmin delete view
    if SubjectVisit.objects.filter(
        subject_identifier=instance.subject_identifier
    ).exists():
        raise ValidationError("Unable to delete consent. Visit data exists.")

    _, schedule = site_visit_schedules.get_by_onschedule_model(
        "ambition_prn.onschedule"
    )
    schedule.take_off_schedule(
        subject_identifier=instance.subject_identifier,
        offschedule_datetime=instance.consent_datetime,
    )

    # update subject screening
    subject_screening = SubjectScreening.objects.get(
        screening_identifier=instance.screening_identifier
    )
    subject_screening.consented = False
    subject_screening.subject_identifier = subject_screening.subject_screening_as_pk
    subject_screening.save()
