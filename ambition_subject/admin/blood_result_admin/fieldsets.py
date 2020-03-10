from edc_action_item import action_fieldset_tuple
from edc_fieldsets import Fieldset
from edc_model_admin import audit_fieldset_tuple

from ...models import BloodResult


def get_results_fieldset(fields):
    fieldsets = []
    for field in fields:
        fieldset = Fieldset(
            field,
            f"{field}_units",
            f"{field}_abnormal",
            f"{field}_reportable",
            section=f"{field.upper()}",
        )
        fieldsets.append(fieldset.fieldset)
    return fieldsets


ft_requisition_fieldset = Fieldset(
    "ft_requisition", "ft_assay_datetime", section="RFT and LFT"
)
cbc_requisition_fieldset = Fieldset(
    "cbc_requisition", "cbc_assay_datetime", section="FBC"
)
cd4_requisition_fieldset = Fieldset(
    "cd4_requisition", "cd4_assay_datetime", section="Immunology"
)
vl_requisition_fieldset = Fieldset(
    "vl_requisition", "vl_assay_datetime", section="Virology"
)

results_fieldsets = []
results_fieldsets.append(ft_requisition_fieldset.fieldset)
results_fieldsets.extend(get_results_fieldset(BloodResult.ft_fields))
results_fieldsets.append(cbc_requisition_fieldset.fieldset)
results_fieldsets.extend(get_results_fieldset(BloodResult.cbc_fields))
results_fieldsets.append(cd4_requisition_fieldset.fieldset)
results_fieldsets.extend(get_results_fieldset(["cd4"]))
results_fieldsets.append(vl_requisition_fieldset.fieldset)
results_fieldsets.extend(get_results_fieldset(["vl"]))

biosynex_fieldset = Fieldset(
    "bios_crag",
    "crag_control_result",
    "crag_t1_result",
    "crag_t2_result",
    section="BIOSYNEX® CryptoPS (Semi-quantitative CrAg)",
)

fieldset = [(None, {"fields": ("subject_visit", "report_datetime")})]
fieldset.extend(results_fieldsets)
fieldset.append(("Conclusion", {"fields": ("results_abnormal", "results_reportable")}))
fieldset.append(("Summary", {"classes": ("collapse",), "fields": ("summary",)}))
fieldset.append(action_fieldset_tuple)
fieldset.append(audit_fieldset_tuple)
