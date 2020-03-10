from django.contrib import admin
from edc_action_item import action_fieldset_tuple, ModelAdminActionItemMixin
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import ambition_ae_admin
from ..forms import RecurrenceSymptomForm
from ..models import RecurrenceSymptom


@admin.register(RecurrenceSymptom, site=ambition_ae_admin)
class RecurrenceSymptomAdmin(
    ModelAdminSubjectDashboardMixin, ModelAdminActionItemMixin, SimpleHistoryAdmin
):
    form = RecurrenceSymptomForm

    fieldsets = (
        (None, {"fields": ["subject_identifier", "report_datetime"]}),
        (
            "Meningitis",
            {
                "fields": [
                    "meningitis_symptom",
                    "meningitis_symptom_other",
                    "patient_readmitted",
                ]
            },
        ),
        ("Glasgow Coma Score", {"fields": ["glasgow_coma_score"]}),
        (
            "Mental Status",
            {"fields": ["recent_seizure", "behaviour_change", "confusion"]},
        ),
        (
            "Neurological",
            {
                "fields": [
                    "neurological",
                    "focal_neurologic_deficit",
                    "cn_palsy_chosen_other",
                ]
            },
        ),
        (
            "Management",
            {
                "fields": [
                    "lp_completed",
                    "amb_administered",
                    "amb_duration",
                    "tb_treatment",
                    "steroids_administered",
                    "steroids_duration",
                    "steroids_choices",
                    "steroids_choices_other",
                    "CD4_count",
                    "antibiotic_treatment",
                    "antibiotic_treatment_other",
                    "on_arvs",
                    "arv_date",
                    "arvs_stopped",
                ]
            },
        ),
        (
            "Forms completed",
            {"fields": ["narrative_summary", "dr_opinion", "dr_opinion_other"]},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "patient_readmitted": admin.VERTICAL,
        "recent_seizure": admin.VERTICAL,
        "behaviour_change": admin.VERTICAL,
        "confusion": admin.VERTICAL,
        "lp_completed": admin.VERTICAL,
        "amb_administered": admin.VERTICAL,
        "tb_treatment": admin.VERTICAL,
        "steroids_administered": admin.VERTICAL,
        "steroids_choices": admin.VERTICAL,
        "on_arvs": admin.VERTICAL,
        "arvs_stopped": admin.VERTICAL,
        "dr_opinion": admin.VERTICAL,
    }

    list_display = (
        "subject_identifier",
        "dashboard",
        "report_datetime",
        "patient_readmitted",
        "action_identifier",
        "tracking_identifier",
    )

    filter_horizontal = ("meningitis_symptom", "neurological", "antibiotic_treatment")

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")
