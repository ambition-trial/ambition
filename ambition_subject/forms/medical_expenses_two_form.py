from django.forms import forms
from edc_constants.constants import YES
from edc_form_validators import NOT_REQUIRED_ERROR

from ..models import MedicalExpensesTwo
from .form_mixins import SubjectModelFormMixin


class MedicalExpensesTwoForm(SubjectModelFormMixin):
    def clean(self):
        """Force the next inline to be completed based on the
        response to 'other_place_visited'.
        """
        cleaned_data = super().clean()
        inline = "medicalexpensestwodetail_set"
        template = (
            "You visited a {} place for "
            "the treatment of the present situation. "
            'Please add details below by clicking [ "Add another Medical '
            'Expenses Part 2: Detail" ] at the bottom of this form.'
        )
        if self.data.get(
            f"{inline}-0-other_place_visited"
        ) == YES and not self.data.get(f"{inline}-1-other_place_visited"):
            message = template.format("second")
            raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)
        if self.data.get(
            f"{inline}-1-other_place_visited"
        ) == YES and not self.data.get(f"{inline}-2-other_place_visited"):
            message = template.format("third")
            raise forms.ValidationError(message, code=NOT_REQUIRED_ERROR)
        return cleaned_data

    class Meta:
        model = MedicalExpensesTwo
        fields = "__all__"
