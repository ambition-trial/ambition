from copy import copy
from django.contrib import admin
from edc_action_item import action_fieldset_tuple, action_fields
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import ambition_prn_admin
from ..forms import AmphotericinMissedDosesForm
from ..forms import FluconazoleMissedDosesForm
from ..forms import FlucytosineMissedDosesForm
from ..forms import SignificantDiagnosesForm
from ..forms import StudyTerminationConclusionForm
from ..models import FluconazoleMissedDoses, AmphotericinMissedDoses
from ..models import FlucytosineMissedDoses, SignificantDiagnoses
from ..models import StudyTerminationConclusion


class SignificantDiagnosesInline(TabularInlineMixin, admin.TabularInline):

    model = SignificantDiagnoses
    form = SignificantDiagnosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {"fields": ("possible_diagnoses", "dx_date", "dx_other")},
        ],
    )


class AmphotericinMissedDosesInline(TabularInlineMixin, admin.TabularInline):

    model = AmphotericinMissedDoses
    form = AmphotericinMissedDosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {"fields": ("day_missed", "missed_reason", "missed_reason_other")},
        ],
    )


class FluconazoleMissedDosesInline(TabularInlineMixin, admin.TabularInline):

    model = FluconazoleMissedDoses
    form = FluconazoleMissedDosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {"fields": ("day_missed", "missed_reason", "missed_reason_other")},
        ],
    )


class FlucytosineMissedDosesInline(TabularInlineMixin, admin.TabularInline):

    model = FlucytosineMissedDoses
    form = FlucytosineMissedDosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {
                "fields": (
                    "day_missed",
                    "doses_missed",
                    "missed_reason",
                    "missed_reason_other",
                )
            },
        ],
    )


@admin.register(StudyTerminationConclusion, site=ambition_prn_admin)
class StudyTerminationConclusionAdmin(
    ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = StudyTerminationConclusionForm

    additional_instructions = (
        "Note: if the patient is deceased, complete the Death Report "
        "before completing this form. "
    )

    inlines = [
        AmphotericinMissedDosesInline,
        FluconazoleMissedDosesInline,
        FlucytosineMissedDosesInline,
        SignificantDiagnosesInline,
    ]

    fieldsets = (
        [
            "Part 1:",
            {
                "fields": (
                    "subject_identifier",
                    "offschedule_datetime",
                    "last_study_fu_date",
                    "discharged_after_initial_admission",
                    "initial_discharge_date",
                    "readmission_after_initial_discharge",
                    "readmission_date",
                    "discharged_date",
                    "termination_reason",
                    "death_date",
                    "consent_withdrawal_reason",
                    "willing_to_complete_10w",
                    "willing_to_complete_centre",
                    "protocol_exclusion_criterion",
                    "included_in_error",
                    "included_in_error_date",
                )
            },
        ],
        [
            "Part 2:",
            {
                "fields": (
                    "rifampicin_started",
                    "first_line_regimen",
                    "first_line_regimen_other",
                    "first_line_choice",
                    "second_line_regimen",
                    "second_line_regimen_other",
                    "arvs_switch_date",
                    "arvs_delay_reason",
                )
            },
        ],
        [
            "Part3: Study medication",
            {
                "fields": (
                    "on_study_drug",
                    ("ampho_start_date", "ampho_stop_date"),
                    ("flucon_start_date", "flucon_stop_date"),
                    ("flucy_start_date", "flucy_stop_date"),
                    ("ambi_start_date", "ambi_stop_date"),
                ),
                "description": (
                    "<h5>Special Instructions</h5>Please only "
                    f"complete the below questions if "
                    "the patient started study drug and "
                    "was terminated from the study "
                    "before the completion of the Week 2 form."
                ),
            },
        ],
        [
            "Part4: Other drugs/interventions given during first 14 days",
            {
                "fields": (
                    "drug_intervention",
                    "drug_intervention_other",
                    "antibiotic",
                    "antibiotic_other",
                    "medicines",
                    "medicine_other",
                )
            },
        ],
        ["Part5: Blood transfusion", {"fields": ("blood_received", "units")}],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "discharged_after_initial_admission": admin.VERTICAL,
        "readmission_after_initial_discharge": admin.VERTICAL,
        "termination_reason": admin.VERTICAL,
        "willing_to_complete_10w": admin.VERTICAL,
        "willing_to_complete_centre": admin.VERTICAL,
        "protocol_exclusion_criterion": admin.VERTICAL,
        "rifampicin_started": admin.VERTICAL,
        "first_line_regimen": admin.VERTICAL,
        "second_line_regimen": admin.VERTICAL,
        "first_line_choice": admin.VERTICAL,
        "blood_received": admin.VERTICAL,
        "on_study_drug": admin.VERTICAL,
    }

    filter_horizontal = ("antibiotic", "medicines", "drug_intervention")

    list_display = (
        "subject_identifier",
        "dashboard",
        "offschedule_datetime",
        "last_study_fu_date",
        "tracking_identifier",
        "action_identifier",
    )

    list_filter = ("offschedule_datetime", "last_study_fu_date")

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
