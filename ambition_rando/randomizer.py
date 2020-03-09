from edc_randomization.randomizer import Randomizer as Base, InvalidAssignment

from .constants import CONTROL, SINGLE_DOSE


class Randomizer(Base):
    name = "ambition"
    assignment_map = {CONTROL: 1, SINGLE_DOSE: 2}
    model = "ambition_rando.randomizationlist"
    filename = "randomization_list.csv"
    is_blinded_trial = False

    @classmethod
    def get_assignment(cls, row):
        """Returns assignment as a word; 'single_dose' or 'control'.

        Converts a numeric assignment or allocation
        to a word.
        """
        assignment = row["assignment"]
        if assignment not in [SINGLE_DOSE, CONTROL]:
            if int(row["assignment"]) == 2:
                assignment = SINGLE_DOSE
            elif int(row["assignment"]) == 1:
                assignment = CONTROL
            else:
                raise InvalidAssignment(
                    f"Invalid assignment. "
                    f'Got \'{row["assignment"]}\'. Expected 1 or 2.'
                )
        return assignment

    @classmethod
    def get_allocation(cls, row):
        """Returns an allocation as 1 or 2 for the given
        assignment or raises.
        """
        assignment = cls.get_assignment(row)
        try:
            allocation = row["orig_allocation"]
        except KeyError:
            if assignment == SINGLE_DOSE:
                allocation = "2"
            elif assignment == CONTROL:
                allocation = "1"
            else:
                raise InvalidAssignment(f"Invalid assignment. Got {assignment}.")
        return allocation
