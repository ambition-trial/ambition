from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION
from edc_adverse_event.model_mixins import (
    DeathReportTmgSecondManager,
    DeathReportTmgSecondSiteManager,
)

from .death_report_tmg import DeathReportTmg


class DeathReportTmgSecond(DeathReportTmg):

    action_name = DEATH_REPORT_TMG_SECOND_ACTION

    on_site = DeathReportTmgSecondSiteManager()

    objects = DeathReportTmgSecondManager()

    class Meta:
        proxy = True
        verbose_name = "Death Report TMG (2nd)"
        verbose_name_plural = "Death Report TMG (2nd)"
