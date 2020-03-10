from django.db import models
from edc_model_fields.fields import OtherCharField

from ...choices import REASON_DRUG_MISSED, DAYS_MISSED
from .week2 import Week2


class MissedDosesManager(models.Manager):
    def get_by_natural_key(
        self,
        day_missed,
        missed_reason,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            day_missed=day_missed,
            missed_reason=missed_reason,
            subject_visit__subject_identifier=subject_identifier,
            subject_visit__visit_schedule_name=visit_schedule_name,
            subject_visit__schedule_name=schedule_name,
            subject_visit__visit_code=visit_code,
        )


class MissedDosesModelMixin(models.Model):

    week2 = models.ForeignKey(Week2, on_delete=models.PROTECT)

    day_missed = models.IntegerField(verbose_name="Day missed:", choices=DAYS_MISSED)

    missed_reason = models.CharField(
        verbose_name="Reason:", max_length=25, blank=True, choices=REASON_DRUG_MISSED
    )

    missed_reason_other = OtherCharField()

    class Meta:
        abstract = True
