from edc_form_validators import FormValidator
from edc_constants.constants import NO, OTHER, YES


class RecurrenceSymptomFormValidator(FormValidator):
    def clean(self):

        self.m2m_other_specify(
            OTHER,
            m2m_field="meningitis_symptom",
            field_other="meningitis_symptom_other",
        )

        self.m2m_other_specify(
            "focal_neurologic_deficit",
            m2m_field="neurological",
            field_other="focal_neurologic_deficit",
        )

        self.m2m_other_specify(
            OTHER, m2m_field="neurological", field_other="cn_palsy_chosen_other"
        )

        self.required_if(YES, field="amb_administered", field_required="amb_duration")

        self.required_if(
            YES, field="steroids_administered", field_required="steroids_duration"
        )

        self.applicable_if(
            YES, field="steroids_administered", field_applicable="steroids_choices"
        )

        self.validate_other_specify(
            field="steroids_choices",
            other_specify_field="steroids_choices_other",
            other_stored_value=OTHER,
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="antibiotic_treatment",
            field_other="antibiotic_treatment_other",
        )

        self.required_if(YES, field="on_arvs", field_required="arv_date")

        self.not_applicable_if(NO, field="on_arvs", field_applicable="arvs_stopped")

        self.validate_other_specify(field="dr_opinion")
