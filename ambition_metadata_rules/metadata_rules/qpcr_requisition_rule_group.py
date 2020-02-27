from ambition_labs.panels import qpcr_blood_panel, qpcr_csf_panel, qpcr24_blood_panel
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register

from ..predicates import Predicates

app_label = "ambition_subject"
pc = Predicates()


@register()
class QpcrRequisitionRuleGroup(RequisitionRuleGroup):

    require_qpcr_blood = RequisitionRule(
        predicate=pc.func_require_qpcr_requisition,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[qpcr_blood_panel],
    )

    require_qpcr24_blood = RequisitionRule(
        predicate=pc.func_require_qpcr_requisition,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[qpcr24_blood_panel],
    )

    require_qpcr_csf = RequisitionRule(
        predicate=pc.func_require_qpcr_requisition,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[qpcr_csf_panel],
    )

    class Meta:
        app_label = app_label
        requisition_model = f"{app_label}.subjectrequisition"
