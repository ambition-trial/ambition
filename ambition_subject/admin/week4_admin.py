from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, TabularInlineMixin

from ..admin_site import ambition_subject_admin
from ..forms import Week4Form, Week4DiagnosesForm
from ..models import Week4, Week4Diagnoses
from .modeladmin import CrfModelAdmin


class Week4DiagnosesInline(TabularInlineMixin, admin.TabularInline):

    model = Week4Diagnoses
    form = Week4DiagnosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Admission history",
            {"fields": ("possible_diagnoses", "dx_date", "dx_other")},
        ],
    )


@admin.register(Week4, site=ambition_subject_admin)
class Week4Admin(CrfModelAdmin):

    form = Week4Form

    inlines = [Week4DiagnosesInline]

    radio_fields = {
        "physical_symptoms": admin.VERTICAL,
        "headache": admin.VERTICAL,
        "recent_seizure_less_72": admin.VERTICAL,
        "behaviour_change": admin.VERTICAL,
        "confusion": admin.VERTICAL,
        "cn_palsy": admin.VERTICAL,
        "focal_neurology": admin.VERTICAL,
        "fluconazole_dose": admin.VERTICAL,
        "rifampicin_started": admin.VERTICAL,
        "other_significant_dx": admin.VERTICAL,
    }

    fieldsets = (
        [
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
        ],
        [
            "Drug Treatment",
            {
                "fields": (
                    "fluconazole_dose",
                    "fluconazole_dose_other",
                    "rifampicin_started",
                    "rifampicin_start_date",
                    "other_significant_dx",
                )
            },
        ],
        audit_fieldset_tuple,
    )
