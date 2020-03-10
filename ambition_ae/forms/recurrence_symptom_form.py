from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_registration.modelform_mixins import ModelFormSubjectIdentifierMixin

from ..form_validators import RecurrenceSymptomFormValidator
from ..models import RecurrenceSymptom


class RecurrenceSymptomForm(
    FormValidatorMixin,
    ModelFormSubjectIdentifierMixin,
    ActionItemFormMixin,
    forms.ModelForm,
):

    form_validator_cls = RecurrenceSymptomFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = RecurrenceSymptom
        fields = "__all__"
