from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import ambition_subject_admin
from ..forms import RadiologyForm
from ..models import Radiology
from .modeladmin import CrfModelAdmin


@admin.register(Radiology, site=ambition_subject_admin)
class RadiologyAdmin(CrfModelAdmin):

    form = RadiologyForm

    radio_fields = {
        "cxr_done": admin.VERTICAL,
        "ct_performed": admin.VERTICAL,
        "scanned_with_contrast": admin.VERTICAL,
        "brain_imaging_reason": admin.VERTICAL,
        "are_results_abnormal": admin.VERTICAL,
    }

    fieldsets = (
        [
            "CXR",
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    "cxr_done",
                    "cxr_date",
                    "cxr_type",
                    "infiltrate_location",
                    "cxr_description",
                )
            },
        ],
        [
            "CT/MRI Brain",
            {
                "fields": (
                    "ct_performed",
                    "ct_performed_date",
                    "scanned_with_contrast",
                    "brain_imaging_reason",
                    "brain_imaging_reason_other",
                    "are_results_abnormal",
                    "abnormal_results_reason",
                    "abnormal_results_reason_other",
                    "infarcts_location",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    filter_horizontal = ("abnormal_results_reason", "cxr_type", "infiltrate_location")
