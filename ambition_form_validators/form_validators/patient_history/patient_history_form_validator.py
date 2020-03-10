from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator

from ...constants import HEADACHE, VISUAL_LOSS
from .arv_treatment_and_monitoring import ArvTreatmentAndMonitoringFormValidatorMixin


class PatientHistoryFormValidator(
    ArvTreatmentAndMonitoringFormValidatorMixin, FormValidator
):
    def clean(self):

        self.m2m_other_specify(
            HEADACHE, m2m_field="symptom", field_other="headache_duration"
        )

        self.m2m_other_specify(
            VISUAL_LOSS, m2m_field="symptom", field_other="visual_loss_duration"
        )

        self.applicable_if(YES, field="tb_history", field_applicable="tb_site")

        self.applicable_if(
            YES, field="tb_treatment", field_applicable="taking_rifampicin"
        )

        self.required_if(
            YES, field="taking_rifampicin", field_required="rifampicin_started_date"
        )

        self.validate_arv_treatment_and_monitoring()

        self.m2m_other_specify(
            "focal_neurologic_deficit",
            m2m_field="neurological",
            field_other="focal_neurologic_deficit",
        )

        self.m2m_other_specify(
            OTHER, m2m_field="neurological", field_other="neurological_other"
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="specify_medications",
            field_other="specify_medications_other",
        )
