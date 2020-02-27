from django.db import models
from edc_constants.choices import YES_NO
from edc_model.models import HistoricalRecords
from edc_visit_tracking.managers import CrfModelManager

from ..managers import CurrentSiteManager
from ..model_mixins import EducationModelMixin
from .crf_model_mixin import CrfModelMixin


class Education(EducationModelMixin, CrfModelMixin):

    household_head = models.CharField(
        verbose_name="Are you the person who earns the highest income?",
        max_length=5,
        choices=YES_NO,
        help_text=(
            'If NO, please complete the form "Health Economics: '
            'Education (Person who earns the highest income)" on behalf of the '
            "Person who earns the highest income."
        ),
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Health Economics: Education"
        verbose_name_plural = "Health Economics: Education"
