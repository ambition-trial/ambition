from edc_adverse_event.form_validators import ValidateDeathReportMixin
from edc_constants.constants import DEAD
from edc_form_validators import FormValidator

from ..constants import CONSENT_WITHDRAWAL


class StudyTerminationConclusionW10FormValidator(
    ValidateDeathReportMixin, FormValidator
):
    def clean(self):

        self.validate_death_report_if_deceased()

        self.required_if(DEAD, field="termination_reason", field_required="death_date")

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="termination_reason",
            field_required="consent_withdrawal_reason",
        )

        self.applicable_if(
            CONSENT_WITHDRAWAL,
            field="termination_reason",
            field_applicable="willing_to_complete_10w",
        )

        self.applicable_if(
            "care_transferred_to_another_institution",
            field="termination_reason",
            field_applicable="willing_to_complete_centre",
        )
