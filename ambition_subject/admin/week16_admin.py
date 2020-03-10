from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import Week16Form
from ..models import Week16
from .modeladmin import CrfModelAdmin


@admin.register(Week16, site=ambition_subject_admin)
class Week16Admin(CrfModelAdmin):

    form = Week16Form

    radio_fields = {
        "patient_alive": admin.VERTICAL,
        "activities_help": admin.VERTICAL,
        "illness_problems": admin.VERTICAL,
        "rankin_score": admin.VERTICAL,
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "patient_alive",
                    "death_datetime",
                    "activities_help",
                    "illness_problems",
                    "rankin_score",
                    "week16_narrative",
                )
            },
        ),
        audit_fieldset_tuple,
    )
