from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import LumbarPunctureCsfForm
from ..models import LumbarPunctureCsf
from .modeladmin import CrfModelAdmin


@admin.register(LumbarPunctureCsf, site=ambition_subject_admin)
class LumbarPunctureCSFAdmin(CrfModelAdmin):

    form = LumbarPunctureCsfForm

    autocomplete_fields = ["qc_requisition", "csf_requisition"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "lp_datetime",
                    "reason_for_lp",
                    "opening_pressure",
                    "closing_pressure",
                    "csf_amount_removed",
                )
            },
        ),
        (
            "Quantitative Culture",
            {"fields": ("qc_requisition", "qc_assay_datetime", "quantitative_culture")},
        ),
        (
            "CSF",
            {
                "fields": (
                    "csf_requisition",
                    "csf_assay_datetime",
                    "csf_culture",
                    "other_csf_culture",
                    "csf_wbc_cell_count",
                    "differential_lymphocyte_count",
                    "differential_lymphocyte_unit",
                    "differential_neutrophil_count",
                    "differential_neutrophil_unit",
                    "india_ink",
                    "csf_glucose",
                    "csf_glucose_units",
                    "csf_protein",
                    "csf_cr_ag",
                    "csf_cr_ag_lfa",
                    "bios_crag",
                    "crag_control_result",
                    "crag_t1_result",
                    "crag_t2_result",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "reason_for_lp": admin.VERTICAL,
        "csf_culture": admin.VERTICAL,
        "india_ink": admin.VERTICAL,
        "csf_cr_ag": admin.VERTICAL,
        "csf_cr_ag_lfa": admin.VERTICAL,
        "differential_lymphocyte_unit": admin.VERTICAL,
        "differential_neutrophil_unit": admin.VERTICAL,
        "csf_glucose_units": admin.VERTICAL,
        "bios_crag": admin.VERTICAL,
        "crag_control_result": admin.VERTICAL,
        "crag_t1_result": admin.VERTICAL,
        "crag_t2_result": admin.VERTICAL,
    }

    list_display = ("lp_datetime", "reason_for_lp")

    list_filter = ("lp_datetime", "reason_for_lp")
