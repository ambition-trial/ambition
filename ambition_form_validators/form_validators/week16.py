from edc_constants.constants import YES, UNKNOWN, NO
from edc_form_validators import FormValidator


class Week16FormValidator(FormValidator):
    def clean(self):
        self.not_required_if(
            YES,
            UNKNOWN,
            field="patient_alive",
            field_required="death_datetime",
            inverse=False,
        )
        self.applicable_if(
            YES, field="patient_alive", field_applicable="activities_help"
        )

        self.applicable_if(
            YES, field="patient_alive", field_applicable="illness_problems"
        )

        self.applicable_if(
            YES, NO, field="patient_alive", field_applicable="rankin_score"
        )
