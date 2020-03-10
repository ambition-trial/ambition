from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import HistoricalRecords
from edc_model.models import BaseUuidModel
from edc_model.validators import datetime_not_future

from ..models import PkPdCrf


class ModelManager(models.Manager):
    def get_by_natural_key(
        self,
        extra_csf_samples_datetime,
        extra_blood_samples_datetime,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            extra_csf_samples_datetime=extra_csf_samples_datetime,
            extra_blood_samples_datetime=extra_blood_samples_datetime,
            pk_pd_crf__subject_visit__subject_identifier=subject_identifier,
            pk_pd_crf__subject_visit__visit_schedule_name=visit_schedule_name,
            pk_pd_crf__subject_visit__schedule_name=schedule_name,
            pk_pd_crf__subject_visit__visit_code=visit_code,
        )


class PkPdExtraSamples(BaseUuidModel):

    """Inline model.
    """

    pk_pd_crf = models.ForeignKey(PkPdCrf, on_delete=PROTECT)

    extra_csf_samples_datetime = models.DateTimeField(
        verbose_name=(
            "If any further CSF samples were taken, please"
            " add here the exact date and time sample was taken"
        ),
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    extra_blood_samples_datetime = models.DateTimeField(
        verbose_name=(
            "If any further blood samples were taken, please"
            " add here the exact date and time sample was taken"
        ),
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    objects = ModelManager()

    history = HistoricalRecords()

    def __str__(self):
        return str(self.pk_pd_crf)

    def natural_key(self):
        return (
            self.extra_csf_samples_datetime,
            self.extra_blood_samples_datetime,
        ) + self.pk_pd_crf.natural_key()

    natural_key.dependencies = ["ambition_subject.pkpdcrf"]

    class Meta:
        verbose_name = "PK/PD Extra Samples"
        verbose_name_plural = "PK/PD Extra Samples"
        unique_together = (
            "pk_pd_crf",
            "extra_csf_samples_datetime",
            "extra_blood_samples_datetime",
        )
