from edc_constants.constants import YES, OTHER, CLOSED
from edc_form_validators import FormValidator

from ..constants import VIOLATION


class ProtocolDeviationViolationFormValidator(FormValidator):
    def clean(self):

        self.applicable_if(
            VIOLATION, field="report_type", field_applicable="safety_impact"
        )

        self.applicable_if(
            VIOLATION, field="report_type", field_applicable="study_outcomes_impact"
        )

        self.required_if(
            YES, field="safety_impact", field_required="safety_impact_details"
        )

        self.required_if(
            YES,
            field="study_outcomes_impact",
            field_required="study_outcomes_impact_details",
        )

        self.required_if(
            VIOLATION, field="report_type", field_required="violation_datetime"
        )

        self.applicable_if(
            VIOLATION, field="report_type", field_applicable="violation_type"
        )

        self.validate_other_specify(
            field="violation_type",
            other_specify_field="violation_type_other",
            other_stored_value=OTHER,
        )

        self.required_if(
            VIOLATION, field="report_type", field_required="violation_description"
        )

        self.required_if(
            VIOLATION, field="report_type", field_required="violation_reason"
        )

        self.required_if_not_none(
            field="corrective_action_datetime", field_required="corrective_action"
        )

        self.required_if_not_none(
            field="preventative_action_datetime", field_required="preventative_action"
        )

        self.required_if(
            CLOSED, field="report_status", field_required="report_closed_datetime"
        )
