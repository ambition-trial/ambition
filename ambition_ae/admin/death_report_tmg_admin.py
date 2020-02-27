from django.contrib import admin
from edc_adverse_event.forms import DeathReportTmgForm
from edc_adverse_event.modeladmin_mixins import DeathReportTmgModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_ae_admin
from ..form_validators import DeathReportTmgFormValidator
from ..models import DeathReport, DeathReportTmg


class CustomDeathReportTmgForm(DeathReportTmgForm):

    form_validator_cls = DeathReportTmgFormValidator


@admin.register(DeathReportTmg, site=ambition_ae_admin)
class DeathReportTmgAdmin(DeathReportTmgModelAdminMixin, SimpleHistoryAdmin):

    form = CustomDeathReportTmgForm

    @property
    def death_report_model_cls(self):
        return DeathReport
