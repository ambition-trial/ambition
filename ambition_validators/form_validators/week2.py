from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator


class Week2FormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='discharged',
            field_required='discharge_date')

        self.required_if(
            YES,
            field='discharged',
            field_required='research_discharge_date')

        self.required_if(
            YES,
            field='died',
            field_required='death_date_time')

        self.m2m_other_specify(
            OTHER,
            m2m_field='drug_intervention',
            field_other='drug_intervention_other')

        self.m2m_other_specify(
            OTHER,
            m2m_field='antibiotic',
            field_other='antibiotic_other')

        self.required_if(
            YES,
            field='blood_received',
            field_required='units')

        self.m2m_other_specify(
            OTHER,
            m2m_field='medicines',
            field_other='medicine_other')
