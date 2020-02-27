from django.forms import forms
from edc_form_validators import FormValidator
from edc_constants.constants import YES


class EducationFormValidator(FormValidator):

    def clean(self):

        self.validate_education_years()

        self.required_if(
            YES,
            field='elementary',
            field_required='attendance_years')

        self.required_if(
            YES,
            field='secondary',
            field_required='secondary_years')

        self.required_if(
            YES,
            field='higher_education',
            field_required='higher_years')

    def validate_education_years(self):
        """Raises if the total years of education is not
        the sum of the years spent in primary/secondary/higher.
        """
        attendance_years = self.cleaned_data.get('attendance_years')
        secondary_years = self.cleaned_data.get('secondary_years')
        higher_years = self.cleaned_data.get('higher_years')
        education_years = self.cleaned_data.get('education_years')
        try:
            education_sum = attendance_years + secondary_years + higher_years
        except TypeError:
            pass
        else:
            if education_sum != education_years:
                raise forms.ValidationError({
                    'education_years':
                    'The total years of education should be the sum of '
                    'the years spent in primary/secondary/higher.'
                    f'Expected {education_sum}.'})
