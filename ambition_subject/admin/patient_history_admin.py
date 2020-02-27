from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin

from ..admin_site import ambition_subject_admin
from ..forms import PatientHistoryForm, PreviousOpportunisticInfectionForm
from ..models import PatientHistory, PreviousOpportunisticInfection
from .modeladmin import CrfModelAdmin


class PreviousOpportunisticInfectionInline(TabularInlineMixin, admin.TabularInline):

    model = PreviousOpportunisticInfection
    form = PreviousOpportunisticInfectionForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Previous Opportunistic Infection",
            {
                "fields": (
                    "previous_non_tb_oi",
                    "previous_non_tb_oi_other",
                    "previous_non_tb_oi_date",
                )
            },
        ],
    )


@admin.register(PatientHistory, site=ambition_subject_admin)
class PatientHistoryAdmin(CrfModelAdmin):

    form = PatientHistoryForm

    inlines = [PreviousOpportunisticInfectionInline]

    filter_horizontal = (
        "neurological",
        "symptom",
        "specify_medications",
        "initial_arv_regimen",
        "current_arv_regimen",
    )

    fieldsets = (
        (
            "Current Symptoms",
            {
                "fields": [
                    "subject_visit",
                    "report_datetime",
                    "symptom",
                    "headache_duration",
                    "visual_loss_duration",
                ]
            },
        ),
        (
            "Previous Medical History",
            {
                "fields": [
                    "tb_history",
                    "tb_site",
                    "tb_treatment",
                    "taking_rifampicin",
                    "rifampicin_started_date",
                ]
            },
        ),
        (
            "ARV Treatment and Monitoring",
            {
                "fields": [
                    "new_hiv_diagnosis",
                    "taking_arv",
                    "initial_arv_date",
                    "initial_arv_date_estimated",
                    "initial_arv_regimen",
                    "initial_arv_regimen_other",
                    "has_switched_regimen",
                    "current_arv_date",
                    "current_arv_date_estimated",
                    "current_arv_regimen",
                    "current_arv_regimen_other",
                    "current_arv_is_defaulted",
                    "current_arv_defaulted_date",
                    "current_arv_defaulted_date_estimated",
                    "current_arv_is_adherent",
                    "current_arv_tablets_missed",
                    "current_arv_decision",
                    "last_viral_load",
                    "viral_load_date",
                    "vl_date_estimated",
                    "last_cd4",
                    "cd4_date",
                    "cd4_date_estimated",
                ]
            },
        ),
        (
            "Vital Signs",
            {
                "fields": [
                    "temp",
                    "heart_rate",
                    "sys_blood_pressure",
                    "dia_blood_pressure",
                    "respiratory_rate",
                    "weight",
                    "weight_determination",
                    "glasgow_coma_score",
                ]
            },
        ),
        (
            "Neurological",
            {
                "fields": [
                    "neurological",
                    "neurological_other",
                    "focal_neurologic_deficit",
                    "visual_acuity_day",
                    "left_acuity",
                    "right_acuity",
                    "ecog_score",
                ]
            },
        ),
        (
            "Other",
            {
                "fields": [
                    "lung_exam",
                    "cryptococcal_lesions",
                    "specify_medications",
                    "specify_medications_other",
                ]
            },
        ),
        ("Previous Infection", {"fields": ["previous_oi"]}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "cd4_date_estimated": admin.VERTICAL,
        "cryptococcal_lesions": admin.VERTICAL,
        "current_arv_date_estimated": admin.VERTICAL,
        "current_arv_decision": admin.VERTICAL,
        "current_arv_defaulted_date_estimated": admin.VERTICAL,
        "current_arv_is_adherent": admin.VERTICAL,
        "current_arv_is_defaulted": admin.VERTICAL,
        "ecog_score": admin.VERTICAL,
        "has_switched_regimen": admin.VERTICAL,
        "initial_arv_date_estimated": admin.VERTICAL,
        "lung_exam": admin.VERTICAL,
        "new_hiv_diagnosis": admin.VERTICAL,
        "previous_oi": admin.VERTICAL,
        "taking_arv": admin.VERTICAL,
        "taking_rifampicin": admin.VERTICAL,
        "tb_history": admin.VERTICAL,
        "tb_site": admin.VERTICAL,
        "tb_treatment": admin.VERTICAL,
        "vl_date_estimated": admin.VERTICAL,
        "weight_determination": admin.VERTICAL,
    }
