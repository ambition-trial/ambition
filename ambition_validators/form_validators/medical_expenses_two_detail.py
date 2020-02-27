from django.forms import forms
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_form_validators import FormValidator, NOT_REQUIRED_ERROR


class MedicalExpensesTwoDetailFormValidator(FormValidator):

    def clean(self):
        self.validate_other_specify(field='location_care')

        self.only_not_required_if(
            NOT_APPLICABLE,
            field='transport_form',
            field_required='transport_cost',
            cleaned_data=self.cleaned_data)

        self.only_not_required_if(
            NOT_APPLICABLE,
            field='transport_form',
            field_required='transport_duration',
            cleaned_data=self.cleaned_data)

        self.validate_other_specify(field='care_provider')

        self.required_if(
            YES,
            field='paid_treatment',
            field_required='paid_treatment_amount')

        self.required_if(
            YES,
            field='medication_bought',
            field_required='medication_payment')

    def only_not_required_if(self, *responses, field=None, field_required=None,
                             cleaned_data=None):

        if ((self.cleaned_data.get(field) and self.cleaned_data.get(field) in responses)
                and (cleaned_data.get(field_required)
                     and cleaned_data.get(field_required) != NOT_APPLICABLE)):
            message = {
                field_required: 'This field is not required.'}
            self._errors.update(message)
            self._error_codes.append(NOT_REQUIRED_ERROR)
            raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)
