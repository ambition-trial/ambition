from ambition_form_validators import SignificantDiagnosesFormValidator
from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import SignificantDiagnoses


class SignificantDiagnosesForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SignificantDiagnosesFormValidator

    class Meta:
        model = SignificantDiagnoses
        fields = "__all__"
