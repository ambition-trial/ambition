from .missed_doses import MissedDosesFormValidator


class FluconazoleMissedDosesFormValidator(MissedDosesFormValidator):

    field = 'flucon_day_missed'
    reason_field = 'flucon_missed_reason'
    reason_other_field = 'missed_reason_other'
    day_range = range(1, 15)
