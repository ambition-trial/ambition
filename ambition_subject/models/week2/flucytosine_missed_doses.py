from django.db import models
from edc_model.models import HistoricalRecords
from edc_model.models import BaseUuidModel

from ...choices import DOSES_MISSED
from .missed_doses_model_mixin import MissedDosesManager, MissedDosesModelMixin


class FlucytosineMissedDoses(MissedDosesModelMixin, BaseUuidModel):

    doses_missed = models.IntegerField(
        verbose_name="Doses missed:", choices=DOSES_MISSED
    )

    objects = MissedDosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.day_missed,) + self.week2.natural_key()

    natural_key.dependencies = ["ambition_subject.week2"]

    class Meta:
        verbose_name_plural = "Flucytosine Missed Doses"
        unique_together = ("week2", "day_missed")
