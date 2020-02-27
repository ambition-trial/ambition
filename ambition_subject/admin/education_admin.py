from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import EducationForm
from ..models import Education
from .modeladmin import CrfModelAdmin


@admin.register(Education, site=ambition_subject_admin)
class EducationAdmin(CrfModelAdmin):

    form = EducationForm

    additional_instructions = (
        "The following questions refer to the educational background of the patient."
    )

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "subject_visit",
                    "report_datetime",
                    "profession",
                    "education_years",
                    "education_certificate",
                    "elementary",
                    "elementary_years",
                    "secondary",
                    "secondary_years",
                    "higher_education",
                    "higher_years",
                    "household_head",
                ]
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "household_head": admin.VERTICAL,
        "elementary": admin.VERTICAL,
        "secondary": admin.VERTICAL,
        "higher_education": admin.VERTICAL,
    }
