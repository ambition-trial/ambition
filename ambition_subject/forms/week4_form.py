from ambition_form_validators import (
    SignificantDiagnosesFormValidator,
    Week4FormValidator,
)
from django.forms import forms
from edc_constants.constants import YES
from edc_form_validators import NOT_REQUIRED_ERROR

from ..models import Week4, Week4Diagnoses
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin


class Week4Form(SubjectModelFormMixin):

    form_validator_cls = Week4FormValidator

    def clean(self):
        cleaned_data = super().clean()
        if self.data.get("other_significant_dx") == YES and not self.data.get(
            "week4diagnoses_set-0-possible_diagnoses"
        ):
            message = {
                "other_significant_dx": "Please complete significant diagnoses table below."
            }
            raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)
        return cleaned_data

    class Meta:
        model = Week4
        fields = "__all__"


class Week4DiagnosesForm(InlineSubjectModelFormMixin):

    form_validator_cls = SignificantDiagnosesFormValidator

    class Meta:
        model = Week4Diagnoses
        fields = "__all__"
