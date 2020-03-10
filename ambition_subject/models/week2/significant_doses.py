from django.db import models
from edc_model.models import HistoricalRecords
from edc_model.models import BaseUuidModel

from ...model_mixins import SignificantDiagnosesModelMixin
from .week2 import Week2


class SignificantDiagnosesManager(models.Manager):
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


class SignificantDiagnoses(SignificantDiagnosesModelMixin, BaseUuidModel):

    week2 = models.ForeignKey(Week2, on_delete=models.PROTECT)

    objects = SignificantDiagnosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.possible_diagnoses, self.dx_date) + self.week2.natural_key()

    natural_key.dependencies = ["ambition_subject.week2"]

    class Meta:
        verbose_name = "Significant Diagnosis"
        verbose_name_plural = "Significant Diagnoses"
        unique_together = ("week2", "possible_diagnoses", "dx_date", "dx_other")
