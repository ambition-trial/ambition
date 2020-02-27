from edc_constants.constants import FEMALE, YES, NO, MALE
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(FormValidator):

    def clean(self):

        condition = (
            self.cleaned_data.get('gender') == FEMALE and
            self.cleaned_data.get('pregnancy') in [YES, NO])

        self.required_if_true(
            condition=condition, field_required='preg_test_date')

        self.applicable_if(FEMALE, field='gender',
                           field_applicable='pregnancy')

        self.not_applicable_if(MALE, field='gender',
                               field_applicable='pregnancy')

        self.not_applicable_if(MALE, field='gender',
                               field_applicable='breast_feeding')

        self.required_if(
            YES,
            field='unsuitable_for_study',
            field_required='reasons_unsuitable')
