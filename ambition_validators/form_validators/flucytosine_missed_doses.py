from .missed_doses import MissedDosesFormValidator


class FlucytosineMissedDosesFormValidator(MissedDosesFormValidator):

    field = 'flucy_day_missed'
    reason_field = 'flucy_missed_reason'
    reason_other_field = 'missed_reason_other'
    day_range = range(1, 15)
