from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

app_label = "ambition_subject"


@register()
class MedicalExpensesCrfRuleGroup(CrfRuleGroup):

    medical_expenses = CrfRule(
        predicate=P("care_before_hospital", "eq", YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f"{app_label}.medicalexpensestwo"],
    )

    class Meta:
        app_label = app_label
        source_model = f"{app_label}.medicalexpenses"
