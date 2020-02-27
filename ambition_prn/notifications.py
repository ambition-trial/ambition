from edc_notification import register
from edc_notification import NewModelNotification


@register()
class StudyTerminationNotification(NewModelNotification):

    name = "study_termination"
    display_name = "a subject has been terminated from the study"
    model = "ambition_prn.studyterminationconclusion"


@register()
class StudyTerminationNotificationW10(NewModelNotification):

    name = "study_termination_w10"
    display_name = "a subject has been terminated from the study (W10)"
    model = "ambition_prn.studyterminationconclusionw10"


@register()
class ProtocolViolationNotification(NewModelNotification):

    name = "protocol_violation"
    display_name = "a protocol violation has occurred"
    model = "ambition_prn.protocolviolation"
