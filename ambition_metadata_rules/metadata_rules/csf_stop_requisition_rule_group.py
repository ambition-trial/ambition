from ambition_labs.panels import csf_stop_panel
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register

from ..predicates import Predicates

app_label = "ambition_subject"
pc = Predicates()


@register()
class CsfStopCmRequisitionRuleGroup(RequisitionRuleGroup):

    require_csf_stop = RequisitionRule(
        predicate=pc.func_require_pkpd_stopcm,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[csf_stop_panel],
    )

    class Meta:
        app_label = app_label
        requisition_model = f"{app_label}.subjectrequisition"
