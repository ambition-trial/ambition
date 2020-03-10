from django import forms

from ambition_form_validators import BloodResultFormValidator
from edc_action_item.forms import ActionItemFormMixin

from ..models import BloodResult
from .form_mixins import SubjectModelFormMixin


class BloodResultForm(ActionItemFormMixin, SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = BloodResultFormValidator

    class Meta:
        model = BloodResult
        fields = "__all__"
