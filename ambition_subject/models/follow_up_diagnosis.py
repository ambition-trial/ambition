from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import BaseUuidModel
from edc_model.models import HistoricalRecords

from ..model_mixins import SignificantDiagnosesModelMixin
from .follow_up import FollowUp


class FollowUpDiagnosesManager(models.Manager):
    def get_by_natural_key(
        self,
        possible_diagnoses,
        dx_date,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            possible_diagnoses=possible_diagnoses,
            dx_date=dx_date,
            subject_visit__subject_identifier=subject_identifier,
            subject_visit__visit_schedule_name=visit_schedule_name,
            subject_visit__schedule_name=schedule_name,
            subject_visit__visit_code=visit_code,
        )


class FollowUpDiagnoses(SignificantDiagnosesModelMixin, BaseUuidModel):
    """Inline model.
    """

    follow_up = models.ForeignKey(FollowUp, on_delete=PROTECT)

    objects = FollowUpDiagnosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.possible_diagnoses, self.dx_date) + self.follow_up.natural_key()

    natural_key.dependencies = ["ambition_subject.followup"]

    class Meta:
        verbose_name = "Follow-up diagnosis"
        verbose_name_plural = "Follow-up diagnoses"
        unique_together = ("follow_up", "possible_diagnoses", "dx_date")
