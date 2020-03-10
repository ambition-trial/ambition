from django.forms import forms
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator

from ..constants import WORKING


class MedicalExpensesFormValidator(FormValidator):
    def clean(self):

        subject_costs = self.cleaned_data.get("subject_spent_last_4wks")
        someone_costs = self.cleaned_data.get("someone_spent_last_4wks")
        try:
            total = subject_costs + someone_costs
        except TypeError:
            pass
        else:
            if total != self.cleaned_data.get("total_spent_last_4wks"):
                raise forms.ValidationError(
                    {"total_spent_last_4wks": f"Expected '{total}'."}
                )

        self.validate_other_specify(field="care_before_hospital")

        self.required_if(
            WORKING, field="activities_missed", field_required="time_off_work"
        )

        self.validate_other_specify(
            field="activities_missed",
            other_specify_field="activities_missed_other",
            other_stored_value=OTHER,
        )

        self.required_if(
            YES, field="loss_of_earnings", field_required="earnings_lost_amount"
        )

        self.required_if_true(
            condition=self.cleaned_data.get("form_of_transport")
            not in [NOT_APPLICABLE, "foot", "bicycle"],
            field_required="transport_fare",
        )

        self.required_if_true(
            condition=self.cleaned_data.get("form_of_transport") != NOT_APPLICABLE,
            field_required="travel_time",
        )

        self.required_if(
            YES, field="private_healthcare", field_required="healthcare_insurance"
        )
