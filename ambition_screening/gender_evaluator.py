from edc_constants.constants import MALE, FEMALE


class GenderEvaluator:
    """Eligible if gender is valid and female not pregnant.
    """

    def __init__(self, gender=None, pregnant=None, breast_feeding=None, **kwargs):
        self.eligible = False
        self.reasons_ineligible = None
        if gender == MALE:
            self.eligible = True
        elif gender == FEMALE and not pregnant and not breast_feeding:
            self.eligible = True
        if not self.eligible:
            self.reasons_ineligible = []
            if pregnant:
                self.reasons_ineligible.append("pregnant.")
            if breast_feeding:
                self.reasons_ineligible.append("breastfeeding")
            if gender not in [MALE, FEMALE]:
                self.reasons_ineligible.append(f"{gender} is an invalid gender.")
