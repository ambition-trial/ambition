from edc_constants.constants import YES
from edc_form_validators import FormValidator


class PreviousOpportunisticInfectionFormValidator(FormValidator):

    def clean(self):
        condition = self.cleaned_data.get(
            'patient_history') and self.cleaned_data.get(
            'patient_history').previous_oi == YES

        self.required_if_true(
            condition=condition,
            field_required='previous_non_tb_oi',
            not_required_msg=(
                'Cannot fill in this form without any previous '
                'opportunistic infections in patient\'s history form.'))

        self.not_required_if(
            None,
            field='previous_non_tb_oi',
            field_required='previous_non_tb_oi_date')

        self.validate_other_specify(field='previous_non_tb_oi')
