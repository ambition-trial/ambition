from ambition_labs.panels import viral_load_panel, cd4_panel
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register

from ..predicates import Predicates

app_label = "ambition_subject"
pc = Predicates()


@register()
class ViralloadCD4RequisitionRuleGroup(RequisitionRuleGroup):

    require_cd4 = RequisitionRule(
        predicate=pc.func_require_cd4,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[cd4_panel],
    )

    require_vl = RequisitionRule(
        predicate=pc.func_require_vl,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[viral_load_panel],
    )

    class Meta:
        app_label = app_label
        source_model = f"{app_label}.patienthistory"
        requisition_model = f"{app_label}.subjectrequisition"
