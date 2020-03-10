from django import forms
from edc_constants.constants import FEMALE, YES, NO, MALE, NOT_APPLICABLE
from edc_form_validators import FormValidator


class SubjectScreeningFormValidator(FormValidator):
    def clean(self):

        if self.cleaned_data.get("gender") == MALE:
            self.not_applicable_if(
                MALE, field="gender", field_applicable="pregnancy", inverse=False
            )

            self.not_required_if(
                MALE, field="gender", field_required="preg_test_date", inverse=False
            )

            self.not_applicable_if(
                MALE, field="gender", field_applicable="breast_feeding"
            )
        else:

            # note, for females, if pregnancy == YES, preg_test_date
            # is optional

            if self.cleaned_data.get("pregnancy") == NO:
                self.required_if(
                    FEMALE, field="gender", field_required="preg_test_date"
                )
            elif self.cleaned_data.get(
                "pregnancy"
            ) == NOT_APPLICABLE and self.cleaned_data.get("preg_test_date"):
                raise forms.ValidationError(
                    {"preg_test_date": "This field is not required."}
                )

        #             self.required_if(YES, NO, field='pregnancy',
        #                              field_required='breast_feeding')

        self.required_if(
            YES, field="unsuitable_for_study", field_required="reasons_unsuitable"
        )
