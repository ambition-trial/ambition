from edc_identifier.managers import SubjectIdentifierManager
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import OnScheduleModelMixin, CurrentSiteManager


class OnScheduleW10(OnScheduleModelMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the signal.
    """

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    class Meta(OnScheduleModelMixin.Meta):
        pass
