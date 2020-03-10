from edc_model.models import HistoricalRecords, BaseUuidModel

from .missed_doses_model_mixin import MissedDosesManager, MissedDosesModelMixin


class FluconazoleMissedDoses(MissedDosesModelMixin, BaseUuidModel):

    objects = MissedDosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.day_missed,) + self.week2.natural_key()

    natural_key.dependencies = ["ambition_subject.week2"]

    class Meta:
        verbose_name_plural = "Fluconazole Missed Doses"
        unique_together = ("week2", "day_missed")
