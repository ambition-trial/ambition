from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from ambition_screening.models.subject_screening import (
    SubjectScreening,
    SubjectScreeningDeleteError,
)


@receiver(pre_delete, weak=False, dispatch_uid="screening_on_pre_delete")
def screening_on_pre_delete(sender, instance, using, **kwargs):
    if isinstance(instance, SubjectScreening):
        if instance.consented:
            raise SubjectScreeningDeleteError(
                "Unable to deleted. Subject has consented."
            )
