from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class MissedDosesFormValidator(FormValidator):

    field = None
    reason_field = None
    reason_other_field = None
    day_range = None

    def clean(self):

        field_value = self.cleaned_data.get(self.field)

        self.required_if_true(
            condition=field_value in self.day_range,
            field_required=self.reason_field)

        self.required_if(
            OTHER,
            field=self.reason_field,
            field_required=self.reason_other_field)
