from ambition_form_validators import FlucytosineMissedDosesFormValidator
from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import FlucytosineMissedDoses


class FlucytosineMissedDosesForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = FlucytosineMissedDosesFormValidator

    class Meta:
        model = FlucytosineMissedDoses
        fields = "__all__"
