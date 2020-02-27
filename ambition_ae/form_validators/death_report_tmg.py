from edc_adverse_event.form_validators import (
    DeathReportTmgFormValidator as FormValidator,
)
from edc_constants.constants import TUBERCULOSIS


class DeathReportTmgFormValidator(FormValidator):
    def clean(self):

        super().clean()

        self.applicable_if(
            TUBERCULOSIS, field="cause_of_death", field_applicable="tb_site"
        )
