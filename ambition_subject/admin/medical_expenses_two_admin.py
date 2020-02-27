from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin

from ..admin_site import ambition_subject_admin
from ..forms import MedicalExpensesTwoDetailForm, MedicalExpensesTwoForm
from ..models import MedicalExpensesTwoDetail, MedicalExpensesTwo
from .modeladmin import CrfModelAdmin


class MedicalExpensesTwoDetailAdmin(StackedInlineMixin, admin.StackedInline):

    model = MedicalExpensesTwoDetail
    form = MedicalExpensesTwoDetailForm
    extra = 0
    min_num = 1
    max_num = 3

    list_display = ("location_care", "location_care_other", "transport_form")

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "location_care",
                    "location_care_other",
                    "transport_form",
                    "transport_cost",
                    "transport_duration",
                    "care_provider",
                    "care_provider_other",
                    "paid_treatment",
                    "paid_treatment_amount",
                    "medication_bought",
                    "medication_payment",
                    "other_place_visited",
                )
            },
        ],
        audit_fieldset_tuple,
    )

    radio_fields = {
        "care_provider": admin.VERTICAL,
        "medication_bought": admin.VERTICAL,
        "location_care": admin.VERTICAL,
        "other_place_visited": admin.VERTICAL,
        "paid_treatment": admin.VERTICAL,
        "transport_form": admin.VERTICAL,
    }


@admin.register(MedicalExpensesTwo, site=ambition_subject_admin)
class MedicalExpensesTwoAdmin(CrfModelAdmin):

    form = MedicalExpensesTwoForm

    inlines = [MedicalExpensesTwoDetailAdmin]

    fieldsets = ((None, {"fields": ["subject_visit", "report_datetime"]}),)
