from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from django.forms import ValidationError

INCORRECT_TOTAL_DOSE = "incorrect_total_dose"


class PkPdCrfFormValidator(FormValidator):
    def clean(self):

        for field in [
            "amphotericin_formulation",
            "amphotericin_dose",
            "amphotericin_started_datetime",
            "amphotericin_ended_datetime",
            "amphotericin_full_dose_given",
        ]:
            self.required_if(
                YES,
                field="amphotericin_given",
                field_required=field,
                required_msg="[010]",
            )

        # flucytosine
        # if flucytosine_dose, require all dose given
        for num in ["one", "two", "three", "four"]:
            self.required_if_not_none(
                field="flucytosine_dose",
                field_required=f"flucytosine_dose_{num}_given",
                required_msg="[015]",
            )

        # if flucytosine_dose_{num}_given is YES
        # require datetime, if not, require reason_missed
        for num in ["one", "two", "three", "four"]:
            self.required_if(
                YES,
                field=f"flucytosine_dose_{num}_given",
                field_required=f"flucytosine_dose_{num}_datetime",
                required_msg="[020]",
            )
            self.required_if(
                NO,
                field=f"flucytosine_dose_{num}_given",
                field_required=f"flucytosine_dose_reason_missed",
                inverse=False,
                required_msg="[030]",
            )

        for num in ["two", "three", "four"]:
            self.required_if(
                YES,
                NO,
                field=f"flucytosine_dose_{num}_given",
                field_required=f"flucytosine_dose_{num}",
                required_msg="[016]",
            )

        if self.cleaned_data.get(f"flucytosine_dose") is not None:
            total_dose = 0
            for num in ["one", "two", "three", "four"]:
                total_dose += self.cleaned_data.get(f"flucytosine_dose_{num}") or 0
            if total_dose != self.cleaned_data.get(f"flucytosine_dose"):
                raise ValidationError(
                    {
                        "flucytosine_dose": (
                            f"Total Flucytosine dose is incorrect. "
                            f"Expected {total_dose} [050]"
                        )
                    },
                    code=INCORRECT_TOTAL_DOSE,
                )

        # fluconazole
        self.required_if(
            YES,
            field="fluconazole_dose_given",
            field_required="fluconazole_dose_datetime",
            required_msg="[060]",
        )

        self.required_if(
            NO,
            field="fluconazole_dose_given",
            field_required="fluconazole_dose_reason_missed",
            required_msg="[070]",
        )

        self.required_if(
            YES,
            field="blood_sample_missed",
            field_required="blood_sample_reason_missed",
            inverse=False,
            required_msg="[080]",
        )

        self.required_if(
            NO, field="pre_dose_lp", field_required="post_dose_lp", required_msg="[090]"
        )
