from ambition_form_validators import PatientHistoryFormValidator
from django.forms import forms
from edc_constants.constants import YES
from edc_form_validators.base_form_validator import NOT_REQUIRED_ERROR

from ..models import PatientHistory
from .form_mixins import SubjectModelFormMixin


class PatientHistoryForm(SubjectModelFormMixin):

    form_validator_cls = PatientHistoryFormValidator

    def clean(self):
        cleaned_data = super().clean()
        if self.data.get("previous_oi") == YES and not self.data.get(
            "previousopportunisticinfection_set-0-previous_non_tb_oi"
        ):
            message = {
                "previous_oi": "Please complete the opportunistic infection table below."
            }
            raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)
        return cleaned_data

    class Meta:
        model = PatientHistory
        fields = "__all__"
