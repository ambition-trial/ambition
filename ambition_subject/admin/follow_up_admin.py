from django.contrib import admin
from edc_fieldsets import Fieldset
from edc_form_label import FormLabel, CustomLabelCondition
from edc_form_label import FormLabelModelAdminMixin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin, SimpleHistoryAdmin

from ..admin_site import ambition_subject_admin
from ..constants import WEEK10
from ..forms import FollowUpForm, FollowUpDiagnosesForm
from ..models import FollowUp, FollowUpDiagnoses
from .modeladmin import CrfModelAdminMixin

visual_acuity_fieldset = Fieldset(
    "visual_acuity_left_eye",
    "visual_acuity_right_eye",
    "patient_help",
    "patient_problems",
    "rankin_score",
    section="Disability Assessment",
)

hospitilization_and_drugs_fieldset = Fieldset(
    "days_hospitalized",
    "antibiotic",
    "antibiotic_other",
    "blood_transfusions",
    "blood_transfusions_units",
    section="Hospitalization and Drugs",
)


class AntibioticCustomLabelCondition(CustomLabelCondition):
    def check(self):
        return True if self.appointment.visit_code == WEEK10 else False


class FollowUpDiagnosesInline(TabularInlineMixin, admin.TabularInline):

    model = FollowUpDiagnoses
    form = FollowUpDiagnosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {"fields": ("possible_diagnoses", "dx_date", "dx_other")},
        ],
    )


@admin.register(FollowUp, site=ambition_subject_admin)
class FollowUpAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):

    form = FollowUpForm

    inlines = [FollowUpDiagnosesInline]

    conditional_fieldsets = {
        WEEK10: (hospitilization_and_drugs_fieldset, visual_acuity_fieldset)
    }

    custom_form_labels = [
        FormLabel(
            field="antibiotic",
            custom_label="Were any of the following antibiotics given since week two?",
            condition_cls=AntibioticCustomLabelCondition,
        )
    ]

    fieldsets = (
        (
            "Clinical Assessment",
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "physical_symptoms",
                    "headache",
                    "glasgow_coma_score",
                    "confusion",
                    "recent_seizure_less_72",
                    "cn_palsy",
                    "behaviour_change",
                    "focal_neurology",
                )
            },
        ),
        (
            "Drug Treatment",
            {
                "fields": (
                    "fluconazole_dose",
                    "fluconazole_dose_other",
                    "rifampicin_started",
                    "rifampicin_start_date",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "physical_symptoms": admin.VERTICAL,
        "headache": admin.VERTICAL,
        "confusion": admin.VERTICAL,
        "recent_seizure_less_72": admin.VERTICAL,
        "cn_palsy": admin.VERTICAL,
        "behaviour_change": admin.VERTICAL,
        "focal_neurology": admin.VERTICAL,
        "fluconazole_dose": admin.VERTICAL,
        "rifampicin_started": admin.VERTICAL,
        "other_significant_dx": admin.VERTICAL,
        "patient_help": admin.VERTICAL,
        "patient_problems": admin.VERTICAL,
        "rankin_score": admin.VERTICAL,
        "blood_transfusions": admin.VERTICAL,
    }

    filter_horizontal = ("antibiotic",)
