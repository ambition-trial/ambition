from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import MicrobiologyForm
from ..models import Microbiology
from .modeladmin import CrfModelAdmin


@admin.register(Microbiology, site=ambition_subject_admin)
class MicrobiologyAdmin(CrfModelAdmin):

    form = MicrobiologyForm

    fieldsets = (
        [
            "Urine Culture (Only for patients with >50 white cells in urine)",
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "urine_culture_performed",
                    "urine_taken_date",
                    "urine_culture_results",
                    "urine_culture_organism",
                    "urine_culture_organism_other",
                )
            },
        ],
        [
            "Blood Culture",
            {
                "fields": (
                    "blood_culture_performed",
                    "blood_culture_results",
                    "blood_taken_date",
                    "day_blood_taken",
                    "blood_culture_organism",
                    "blood_culture_organism_other",
                    "bacteria_identified",
                    "bacteria_identified_other",
                )
            },
        ],
        [
            "Sputum Microbiology",
            {
                "fields": (
                    "sputum_afb_performed",
                    "sputum_afb_date",
                    "sputum_results_afb",
                    "sputum_performed",
                    "sputum_taken_date",
                    "sputum_results_culture",
                    "sputum_results_positive",
                    "sputum_genexpert_performed",
                    "sputum_genexpert_date",
                    "sputum_result_genexpert",
                )
            },
        ],
        [
            "CSF Microbiology",
            {
                "fields": (
                    "csf_genexpert_performed",
                    "csf_genexpert_date",
                    "csf_result_genexpert",
                )
            },
        ],
        [
            "Histopathology",
            {
                "fields": (
                    "tissue_biopsy_taken",
                    "tissue_biopsy_results",
                    "biopsy_date",
                    "day_biopsy_taken",
                    "tissue_biopsy_organism",
                    "tissue_biopsy_organism_other",
                    "histopathology_report",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    radio_fields = {
        "urine_culture_performed": admin.VERTICAL,
        "urine_culture_results": admin.VERTICAL,
        "urine_culture_organism": admin.VERTICAL,
        "blood_culture_performed": admin.VERTICAL,
        "blood_culture_results": admin.VERTICAL,
        "blood_culture_organism": admin.VERTICAL,
        "bacteria_identified": admin.VERTICAL,
        "sputum_afb_performed": admin.VERTICAL,
        "sputum_results_afb": admin.VERTICAL,
        "sputum_performed": admin.VERTICAL,
        "sputum_results_culture": admin.VERTICAL,
        "sputum_result_genexpert": admin.VERTICAL,
        "sputum_genexpert_performed": admin.VERTICAL,
        "csf_result_genexpert": admin.VERTICAL,
        "csf_genexpert_performed": admin.VERTICAL,
        "tissue_biopsy_taken": admin.VERTICAL,
        "tissue_biopsy_results": admin.VERTICAL,
        "tissue_biopsy_organism": admin.VERTICAL,
    }
