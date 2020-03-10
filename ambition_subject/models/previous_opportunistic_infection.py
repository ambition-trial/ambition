from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import HistoricalRecords
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future

from ..choices import INFECTION
from .patient_history import PatientHistory


class PreviousOpportunisticInfectionManager(models.Manager):
    def get_by_natural_key(
        self,
        previous_non_tb_oi,
        previous_non_tb_oi_date,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            previous_non_tb_oi=previous_non_tb_oi,
            previous_non_tb_oi_date=previous_non_tb_oi_date,
            patient_history__subject_visit__subject_identifier=subject_identifier,
            patient_history__subject_visit__visit_schedule_name=visit_schedule_name,
            patient_history__subject_visit__schedule_name=schedule_name,
            patient_history__subject_visit__visit_code=visit_code,
        )


class PreviousOpportunisticInfection(BaseUuidModel):

    patient_history = models.ForeignKey(PatientHistory, on_delete=PROTECT)

    previous_non_tb_oi = models.CharField(
        verbose_name="If other previous opportunistic infection, please specify.",
        max_length=25,
        choices=INFECTION,
        blank=True,
    )

    previous_non_tb_oi_other = models.CharField(null=True, blank=True, max_length=50)

    previous_non_tb_oi_date = models.DateField(
        verbose_name="If infection, what was the date?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    objects = PreviousOpportunisticInfectionManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (
            self.previous_non_tb_oi,
            self.previous_non_tb_oi_date,
        ) + self.patient_history.natural_key()

    natural_key.dependencies = ["ambition_subject.patienthistory"]

    class Meta:
        verbose_name_plural = "Previous Opportunistic Infection"
        unique_together = (
            "patient_history",
            "previous_non_tb_oi",
            "previous_non_tb_oi_date",
        )
