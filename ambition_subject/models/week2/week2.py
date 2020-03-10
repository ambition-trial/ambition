from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future, datetime_not_future
from edc_visit_tracking.managers import CrfModelManager

from ...managers import CurrentSiteManager
from ...model_mixins import BloodTransfusionModelMixin
from ...model_mixins import StudyMedicationModelMixin
from ...model_mixins import ClinicalAssessmentModelMixin
from ...model_mixins import MedAndDrugInterventionModelMixin
from ..crf_model_mixin import CrfModelMixin


class Week2(
    ClinicalAssessmentModelMixin,
    StudyMedicationModelMixin,
    MedAndDrugInterventionModelMixin,
    BloodTransfusionModelMixin,
    CrfModelMixin,
):

    discharged = models.CharField(
        verbose_name="Discharged", max_length=25, choices=YES_NO
    )

    discharge_date = models.DateField(
        validators=[date_not_future], null=True, blank=True
    )

    research_discharge_date = models.DateField(
        verbose_name="On which date did the research team feel the patient was well "
        "enough to go home",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    died = models.CharField(verbose_name="Died", max_length=25, choices=YES_NO)

    death_date_time = models.DateTimeField(
        validators=[datetime_not_future], null=True, blank=True
    )

    temperature = models.FloatField(
        verbose_name="Temperature", null=True, blank=True, default=None
    )

    weight = models.DecimalField(
        verbose_name="Weight",
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        decimal_places=1,
        max_digits=4,
        help_text="kg",
    )

    significant_dx = models.CharField(
        verbose_name="Other significant diagnoses since enrolment",
        max_length=25,
        choices=YES_NO,
    )

    significant_dx_datetime = models.DateTimeField(
        validators=[date_not_future], null=True, blank=True
    )

    flucon_missed_doses = models.CharField(
        verbose_name="Were any Fluconazole drug doses missed",
        max_length=25,
        choices=YES_NO,
    )

    amphotericin_missed_doses = models.CharField(
        verbose_name="Were any Amphotericin B drug doses missed",
        max_length=25,
        choices=YES_NO,
    )

    other_significant_dx = models.CharField(
        verbose_name="Other significant diagnosis since enrollment",
        max_length=5,
        choices=YES_NO,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Week 2"
        verbose_name_plural = "Week 2"
