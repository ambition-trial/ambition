from django.contrib import admin

from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin
from edc_fieldsets import Fieldset

from ..admin_site import ambition_subject_admin
from ..forms import MedicalExpensesForm
from ..models import MedicalExpenses
from ..constants import DAY1, WEEK10
from .modeladmin import CrfModelAdmin

info_source = Fieldset("info_source", section="Information Source")

transport = Fieldset(
    "form_of_transport", "transport_fare", "travel_time", section="Transport"
)

house_essentials = Fieldset(
    "food_spend", "utilities_spend", "item_spend", section="House Essentials"
)

loans_insurance = Fieldset(
    "loans",
    "sold_anything",
    "private_healthcare",
    "healthcare_insurance",
    section="Loans and Insurance",
)

welfare = Fieldset("welfare", section="Welfare or social service support")


@admin.register(MedicalExpenses, site=ambition_subject_admin)
class MedicalExpensesAdmin(CrfModelAdmin):

    form = MedicalExpensesForm
    conditional_fieldsets = {
        DAY1: (info_source, house_essentials, transport, loans_insurance, welfare),
        WEEK10: (info_source, loans_insurance),
    }

    fieldsets = (
        (
            "Medical Expenses",
            {
                "fields": [
                    "subject_visit",
                    "report_datetime",
                    "currency",
                    "subject_spent_last_4wks",
                    "someone_spent_last_4wks",
                    "total_spent_last_4wks",
                    "duration_present_condition",
                    "activities_missed",
                    "activities_missed_other",
                    "time_off_work",
                    "carer_time_off",
                    "loss_of_earnings",
                    "earnings_lost_amount",
                    "care_before_hospital",
                ]
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "activities_missed": admin.VERTICAL,
        "care_before_hospital": admin.VERTICAL,
        "currency": admin.VERTICAL,
        "form_of_transport": admin.VERTICAL,
        "healthcare_insurance": admin.VERTICAL,
        "info_source": admin.VERTICAL,
        "loans": admin.VERTICAL,
        "loss_of_earnings": admin.VERTICAL,
        "private_healthcare": admin.VERTICAL,
        "sold_anything": admin.VERTICAL,
        "welfare": admin.VERTICAL,
    }
