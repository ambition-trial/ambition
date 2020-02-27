from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.constants import YES, UNKNOWN


class AeInitialFormValidator(FormValidator):
    def validate_relationship_to_study_drug(self):
        drugs = [
            "fluconazole_relation",
            "flucytosine_relation",
            "amphotericin_relation",
        ]
        for drug in drugs:
            self.applicable_if(
                YES,
                UNKNOWN,
                field="ae_study_relation_possibility",
                field_applicable=drug,
            )
