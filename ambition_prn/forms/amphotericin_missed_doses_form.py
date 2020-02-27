from ambition_form_validators import AmphotericinMissedDosesFormValidator
from django import forms
from edc_form_validators import FormValidatorMixin

from ..models import AmphotericinMissedDoses


class AmphotericinMissedDosesForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = AmphotericinMissedDosesFormValidator

    class Meta:
        model = AmphotericinMissedDoses
        fields = "__all__"
