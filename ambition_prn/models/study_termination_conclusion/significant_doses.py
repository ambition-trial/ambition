from ambition_subject.model_mixins import SignificantDiagnosesModelMixin
from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords

from .study_termination_conclusion import StudyTerminationConclusion


class SignificantDiagnosesManager(models.Manager):
    def get_by_natural_key(self, possible_diagnoses, dx_date, action_identifier):
        return self.get(
            possible_diagnoses=possible_diagnoses,
            dx_date=dx_date,
            action_identifier=action_identifier,
        )


class SignificantDiagnoses(SignificantDiagnosesModelMixin, BaseUuidModel):

    study_termination_conclusion = models.ForeignKey(
        StudyTerminationConclusion, on_delete=models.PROTECT
    )

    objects = SignificantDiagnosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (
            self.possible_diagnoses,
            self.dx_date,
        ) + self.study_termination_conclusion.natural_key()

    natural_key.dependencies = ["ambition_prn.study_termination_conclusion"]

    class Meta:
        verbose_name = "Significant Diagnosis"
        verbose_name_plural = "Significant Diagnoses"
        unique_together = (
            "study_termination_conclusion",
            "possible_diagnoses",
            "dx_date",
            "dx_other",
        )
