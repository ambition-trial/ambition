from .missed_doses import MissedDosesFormValidator


class AmphotericinMissedDosesFormValidator(MissedDosesFormValidator):

    field = 'ampho_day_missed'
    reason_field = 'ampho_missed_reason'
    reason_other_field = 'missed_reason_other'
    day_range = range(1, 15)
