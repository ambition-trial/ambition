from edc_constants.constants import NORMAL, YES, NO

from .eligibility import Eligibility


def if_yes(value):
    if value == NORMAL:
        return True
    return value == YES


def if_no(value):
    return value == NO


def if_normal(value):
    return value == NORMAL


class SubjectScreeningEligibility:

    eligibility_cls = Eligibility

    def __init__(self, model_obj=None, allow_none=None):
        eligibility_obj = self.eligibility_cls(
            allow_none=allow_none,
            age=model_obj.age_in_years,
            gender=model_obj.gender,
            alt=model_obj.alt,
            neutrophil=model_obj.neutrophil,
            platelets=model_obj.platelets,
            will_hiv_test=if_yes(model_obj.will_hiv_test),
            consent_ability=if_yes(model_obj.consent_ability),
            meningitis_dx=if_yes(model_obj.meningitis_dx),
            pregnant=if_yes(model_obj.pregnancy),
            breast_feeding=if_yes(model_obj.breast_feeding),
            no_drug_reaction=if_no(model_obj.previous_drug_reaction),
            no_concomitant_meds=if_no(model_obj.contraindicated_meds),
            no_amphotericin=if_no(model_obj.received_amphotericin),
            no_fluconazole=if_no(model_obj.received_fluconazole),
            not_suitable=if_no(model_obj.unsuitable_for_study),
            subject_screening=model_obj,
        )
        self.eligible = eligibility_obj.eligible
        self.reasons_ineligible = eligibility_obj.reasons_ineligible
