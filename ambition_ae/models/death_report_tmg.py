from django.db import models
from django.db.models.deletion import PROTECT
from edc_adverse_event.model_mixins import DeathReportTmgModelMixin
from edc_constants.constants import QUESTION_RETIRED, NOT_APPLICABLE
from edc_model.models import BaseUuidModel

from ..choices import TB_SITE_DEATH
from .death_report import DeathReport


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):

    death_report = models.ForeignKey(DeathReport, on_delete=PROTECT)

    cause_of_death_old = models.CharField(
        verbose_name="Main cause of death",
        max_length=50,
        default=QUESTION_RETIRED,
        blank=True,
        null=True,
        help_text="Main cause of death in the opinion of TMG member",
    )

    tb_site = models.CharField(
        verbose_name="If cause of death is TB, specify site of TB disease",
        max_length=25,
        choices=TB_SITE_DEATH,
        default=NOT_APPLICABLE,
        blank=True,
    )

    class Meta(DeathReportTmgModelMixin.Meta):
        pass
