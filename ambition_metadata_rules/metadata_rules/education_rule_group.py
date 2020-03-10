from edc_constants.constants import NO
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

app_label = "ambition_subject"


@register()
class EducationCrfRuleGroup(CrfRuleGroup):

    head_of_household = CrfRule(
        predicate=P("household_head", "eq", NO),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f"{app_label}.educationhoh"],
    )

    class Meta:
        app_label = app_label
        source_model = f"{app_label}.education"
