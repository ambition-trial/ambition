from django.contrib import admin
from django.utils.safestring import mark_safe
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import EducationHohForm
from ..models import EducationHoh
from .modeladmin import CrfModelAdmin


@admin.register(EducationHoh, site=ambition_subject_admin)
class EducationHohAdmin(CrfModelAdmin):

    form = EducationHohForm

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">'
        "The following questions refer to the educational background of "
        "the Person who earns the highest income</span></H5>"
        "Please respond on behalf of the Person who earns the highest income."
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
                ]
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "elementary": admin.VERTICAL,
        "secondary": admin.VERTICAL,
        "higher_education": admin.VERTICAL,
    }
