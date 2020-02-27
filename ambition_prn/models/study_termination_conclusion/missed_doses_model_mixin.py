from ambition_subject.choices import REASON_DRUG_MISSED, DAYS_MISSED
from django.db import models
from edc_model_fields.fields import OtherCharField

from .study_termination_conclusion import StudyTerminationConclusion


class MissedDosesManager(models.Manager):
    def get_by_natural_key(self, day_missed, missed_reason, action_identifier):
        return self.get(
            day_missed=day_missed,
            missed_reason=missed_reason,
            action_identifier=action_identifier,
        )


class MissedDosesModelMixin(models.Model):

    study_termination_conclusion = models.ForeignKey(
        StudyTerminationConclusion, on_delete=models.PROTECT
    )

    day_missed = models.IntegerField(verbose_name="Day missed:", choices=DAYS_MISSED)

    missed_reason = models.CharField(
        verbose_name="Reason:", max_length=25, blank=True, choices=REASON_DRUG_MISSED
    )

    missed_reason_other = OtherCharField()

    def __str__(self):
        return (
            f"{self.study_termination_conclusion}: "
            f"Missed {self.get_day_missed_display()}"
        )

    class Meta:
        abstract = True
