from edc_model.models import BaseUuidModel, HistoricalRecords

from .missed_doses_model_mixin import MissedDosesManager, MissedDosesModelMixin


class AmphotericinMissedDoses(MissedDosesModelMixin, BaseUuidModel):

    objects = MissedDosesManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.day_missed,) + self.study_termination_conclusion.natural_key()

    natural_key.dependencies = ["ambition_prn.study_termination_conclusion"]

    class Meta:
        verbose_name_plural = "Amphotericin Missed Doses"
        unique_together = ("study_termination_conclusion", "day_missed")
