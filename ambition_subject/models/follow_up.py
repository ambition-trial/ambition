from ambition_lists.models import Antibiotic
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField
from edc_visit_tracking.managers import CrfModelManager

from ..choices import FLUCONAZOLE_DOSE, RANKIN_SCORE, YES_NO_ND, YES_NO_ALREADY_ND
from ..managers import CurrentSiteManager
from ..model_mixins import ClinicalAssessmentModelMixin
from .crf_model_mixin import CrfModelMixin


class FollowUp(ClinicalAssessmentModelMixin, CrfModelMixin):

    fluconazole_dose = models.CharField(
        verbose_name="Fluconazole dose (day prior to visit)",
        max_length=25,
        choices=FLUCONAZOLE_DOSE,
    )

    fluconazole_dose_other = OtherCharField(
        verbose_name="If other, specify dose:", max_length=25
    )

    rifampicin_started = models.CharField(
        verbose_name="Rifampicin started since last visit?",
        max_length=25,
        choices=YES_NO_ALREADY_ND,
    )

    rifampicin_start_date = models.DateField(
        verbose_name="Date Rifampicin started",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    days_hospitalized = models.DecimalField(
        verbose_name=(
            "Over the ten weeks spent in the study how "
            "many days did the patient spend in hospital?"
        ),
        decimal_places=3,
        max_digits=5,
        null=True,
    )

    antibiotic = models.ManyToManyField(
        Antibiotic,
        blank=True,
        verbose_name="Were any of the following antibiotics given?",
    )

    antibiotic_other = models.CharField(
        verbose_name="If other antibiotics, please specify:",
        max_length=50,
        null=True,
        blank=True,
    )

    blood_transfusions = models.CharField(
        verbose_name="Has the patient had any blood transfusions since week two? ",
        max_length=5,
        choices=YES_NO,
        null=True,
    )

    blood_transfusions_units = models.DecimalField(
        verbose_name="If YES, no. of units?    ",
        decimal_places=3,
        max_digits=5,
        null=True,
        blank=True,
    )

    patient_help = models.CharField(
        verbose_name=(
            "Does the patient require help from" " anybody for everyday activities? "
        ),
        max_length=10,
        choices=YES_NO_ND,
        help_text=(
            "For example eating, drinking, washing,"
            " brushing teeth, going to the toilet"
        ),
    )

    patient_problems = models.CharField(
        verbose_name="Has the illness left the patient with any other problems?",
        max_length=10,
        choices=YES_NO_ND,
    )

    rankin_score = models.CharField(
        verbose_name="Modified Rankin score",
        choices=RANKIN_SCORE,
        max_length=10,
        null=True,
    )

    other_significant_dx = models.CharField(
        verbose_name="Other significant diagnosis since last visit?",
        max_length=5,
        choices=YES_NO_NA,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Follow-up"
        verbose_name_plural = "Follow-up"
