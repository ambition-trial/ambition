from django.forms import forms
from edc_form_validators import FormValidator
from edc_constants.constants import YES


class EducationFormValidator(FormValidator):
    def clean(self):

        self.validate_education_years()

        self.required_if(YES, field="elementary", field_required="elementary_years")

        self.required_if(YES, field="secondary", field_required="secondary_years")

        self.required_if(YES, field="higher_education", field_required="higher_years")

    def validate_education_years(self):
        """Raises if the total years of education is not
        the sum of the years spent in primary/secondary/higher.
        """
        elementary_years = self.cleaned_data.get("elementary_years") or 0
        secondary_years = self.cleaned_data.get("secondary_years") or 0
        higher_years = self.cleaned_data.get("higher_years") or 0
        education_years = self.cleaned_data.get("education_years") or 0
        calculated_total = elementary_years + secondary_years + higher_years
        if calculated_total != education_years or 0:
            raise forms.ValidationError(
                {
                    "education_years": "Incorrect.  "
                    f"Expected {elementary_years}+{secondary_years}+"
                    f"{higher_years}={calculated_total}. ("
                    f"The sum of the years spent in primary/secondary/higher) "
                    f"Got {elementary_years}+{secondary_years}+"
                    f"{higher_years}={education_years}."
                }
            )
