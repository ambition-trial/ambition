from ambition_subject.choices import DOSES_MISSED
from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords

from .missed_doses_model_mixin import MissedDosesManager, MissedDosesModelMixin


class FlucytosineMissedDoses(MissedDosesModelMixin, BaseUuidModel):

    doses_missed = models.IntegerField(
        verbose_name="Doses missed:", choices=DOSES_MISSED
    )

    objects = MissedDosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.day_missed,) + self.study_termination_conclusion.natural_key()

    natural_key.dependencies = ["ambition_prn.study_termination_conclusion"]

    class Meta:
        verbose_name_plural = "Flucytosine Missed Doses"
        unique_together = ("study_termination_conclusion", "day_missed")
