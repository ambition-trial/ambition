from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator


class SignificantDiagnosesFormValidator(FormValidator):

    def clean(self):
        significant_dx_cls = (
            self.cleaned_data.get('week4')
            or self.cleaned_data.get('week2')
            or self.cleaned_data.get('followup'))

        self.required_if_true(
            condition=(significant_dx_cls
                       and significant_dx_cls.other_significant_dx == YES),
            field_required='possible_diagnoses')

        self.required_if(
            YES,
            field='other_significant_diagnoses',
            field_required='possible_diagnoses')

        self.not_required_if(
            None,
            field='possible_diagnoses',
            field_required='dx_date')

        self.required_if(
            OTHER,
            field='possible_diagnoses',
            field_required='dx_other')
