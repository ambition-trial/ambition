from edc_notification import register
from edc_notification import NewModelNotification


@register()
class SubjectConsentNotification(NewModelNotification):

    name = "consent"
    display_name = "a subject has been randomized/consented"
    model = "ambition_subject.subjectconsent"
