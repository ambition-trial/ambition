from django.db import models
from edc_adverse_event.model_mixins import DeathReportModelMixin
from edc_constants.constants import NOT_APPLICABLE, QUESTION_RETIRED
from edc_model.models import BaseUuidModel

from ..choices import TB_SITE_DEATH


class DeathReport(DeathReportModelMixin, BaseUuidModel):

    cause_of_death_old = models.CharField(
        max_length=50,
        verbose_name=("Main cause of death"),
        help_text=(
            "Main cause of death in the opinion of the "
            "local study doctor and local PI"
        ),
        default=QUESTION_RETIRED,
        editable=False,
    )

    tb_site = models.CharField(
        verbose_name="If cause of death is TB, specify site of TB disease",
        max_length=25,
        choices=TB_SITE_DEATH,
        default=NOT_APPLICABLE,
    )

    class Meta(DeathReportModelMixin.Meta):
        pass
