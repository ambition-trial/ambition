from ambition_form_validators import SubjectScreeningFormValidator
from django import forms
from edc_form_validators import FormValidatorMixin

from ..models.subject_screening import SubjectScreening


class SubjectScreeningForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectScreeningFormValidator

    class Meta:
        model = SubjectScreening
        fields = "__all__"
