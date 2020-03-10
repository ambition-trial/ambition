from django.db import models
from edc_constants.choices import YES_NO_NA, YES_NO_UNKNOWN
from edc_model.models import HistoricalRecords
from edc_model.validators import datetime_not_future
from edc_visit_tracking.managers import CrfModelManager

from ..choices import RANKIN_SCORE
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin
from edc_constants.constants import NOT_APPLICABLE


class Week16(CrfModelMixin):

    patient_alive = models.CharField(
        verbose_name="Is the patient alive?", max_length=15, choices=YES_NO_UNKNOWN
    )

    death_datetime = models.DateTimeField(
        verbose_name="If deceased, date and time of death",
        validators=[datetime_not_future],
        null=True,
        blank=True,
        help_text="Leave blank if date is unknown.",
    )

    activities_help = models.CharField(
        verbose_name=(
            "Does the patient require help from anybody for everyday activities?"
        ),
        max_length=5,
        choices=YES_NO_NA,
        help_text=(
            "For example eating, drinking, washing, brushing teeth, "
            "going to the toilet."
        ),
    )

    illness_problems = models.CharField(
        verbose_name="Has the illness left the patient with any other problems?",
        max_length=5,
        choices=YES_NO_NA,
    )

    rankin_score = models.CharField(
        verbose_name="Modified Rankin score",
        max_length=10,
        choices=RANKIN_SCORE,
        default=NOT_APPLICABLE,
    )

    week16_narrative = models.TextField(
        verbose_name="Narrative", max_length=1000, null=True, blank=True
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Week 16"
        verbose_name_plural = "Week 16"
