from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from django.forms import ValidationError

INCORRECT_TOTAL_DOSE = 'incorrect_total_dose'


class PkPdCrfFormValidator(FormValidator):

    def clean(self):

        for num in ['one', 'two', 'three', 'four']:
            self.required_if(
                YES,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_{num}_datetime')
            self.required_if(
                YES,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_{num}')
            self.required_if(
                NO,
                field=f'flucytosine_dose_{num}_given',
                field_required=f'flucytosine_dose_reason_missed',
                inverse=False)

        total_dose = 0
        total_dose_is_required = False
        for num in ['one', 'two', 'three', 'four']:
            if self.cleaned_data.get(f'flucytosine_dose_{num}_given') == YES:
                total_dose_is_required = True
                total_dose += (self.cleaned_data.get(
                    f'flucytosine_dose_{num}') or 0)
        if total_dose_is_required:
            if total_dose != self.cleaned_data.get(f'flucytosine_dose'):
                raise ValidationError(
                    {'flucytosine_dose':
                     f'Total Flucytosine dose is incorrect. Expected {total_dose}'},
                    code=INCORRECT_TOTAL_DOSE)
        else:
            if self.cleaned_data.get(f'flucytosine_dose'):
                raise ValidationError(
                    {'flucytosine_dose':
                     f'Total Flucytosine dose is incorrect. '
                     'Doses 1-4 have not been given.'},
                    code=INCORRECT_TOTAL_DOSE)

        self.required_if(
            YES,
            field='fluconazole_dose_given',
            field_required='fluconazole_dose_datetime')

        self.required_if(
            NO,
            field='fluconazole_dose_given',
            field_required='fluconazole_dose_reason_missed')

        self.required_if(
            YES,
            field='full_ambisome_dose_given',
            field_required='ambisome_ended_datetime')

        self.required_if(
            YES,
            field='blood_sample_missed',
            field_required='blood_sample_reason_missed',
            inverse=False)

        self.required_if(
            NO,
            field='pre_dose_lp',
            field_required='post_dose_lp')
