from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField
from edc_visit_tracking.managers import CrfModelManager

from ...choices import FLUCONAZOLE_DOSE, YES_NO_ALREADY_ND
from ...managers import CurrentSiteManager
from ...model_mixins import ClinicalAssessmentModelMixin
from ..crf_model_mixin import CrfModelMixin


class Week4(ClinicalAssessmentModelMixin, CrfModelMixin):

    fluconazole_dose = models.CharField(
        verbose_name="Fluconazole dose (day prior to visit)",
        max_length=25,
        choices=FLUCONAZOLE_DOSE,
    )

    fluconazole_dose_other = OtherCharField(max_length=25)

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

    lp_done = models.CharField(
        verbose_name="LP done?",
        max_length=5,
        choices=YES_NO,
        help_text="If yes, ensure LP CRF completed.",
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
        verbose_name = "Week 4"
        verbose_name_plural = "Week 4"
