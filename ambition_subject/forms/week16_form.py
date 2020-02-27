from ambition_form_validators import Week16FormValidator
from django import forms
from edc_constants.constants import NO, NOT_DONE, YES

from ..models import Week16
from .form_mixins import SubjectModelFormMixin


class Week16Form(SubjectModelFormMixin):

    form_validator_cls = Week16FormValidator

    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get("patient_alive") == NO:
            if self.cleaned_data.get("rankin_score") not in ["6", NOT_DONE]:
                raise forms.ValidationError({"rankin_score": "Invalid response."})
        if self.cleaned_data.get("patient_alive") == YES:
            if self.cleaned_data.get("rankin_score") == "6":
                raise forms.ValidationError({"rankin_score": "Invalid response."})
        return cleaned_data

    class Meta:
        model = Week16
        fields = "__all__"
