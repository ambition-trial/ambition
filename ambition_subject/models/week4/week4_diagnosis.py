from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import BaseUuidModel
from edc_model.models import HistoricalRecords

from ...model_mixins import SignificantDiagnosesModelMixin
from .week4 import Week4


class Week4DiagnosesManager(models.Manager):
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


class Week4Diagnoses(SignificantDiagnosesModelMixin, BaseUuidModel):

    week4 = models.ForeignKey(Week4, on_delete=PROTECT)

    objects = Week4DiagnosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.possible_diagnoses, self.dx_date) + self.week4.natural_key()

    natural_key.dependencies = ["ambition_subject.week4"]

    class Meta:
        verbose_name = "Week 4 Diagnoses"
        verbose_name_plural = "Week 4 Diagnoses"
        unique_together = ("week4", "possible_diagnoses", "dx_date")
