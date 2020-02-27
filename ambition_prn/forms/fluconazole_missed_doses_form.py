from ambition_form_validators import FluconazoleMissedDosesFormValidator
from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import FluconazoleMissedDoses


class FluconazoleMissedDosesForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = FluconazoleMissedDosesFormValidator

    class Meta:
        model = FluconazoleMissedDoses
        fields = "__all__"
