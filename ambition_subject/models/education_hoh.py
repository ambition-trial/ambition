from edc_model.models import HistoricalRecords
from edc_visit_tracking.managers import CrfModelManager

from ..managers import CurrentSiteManager
from ..model_mixins import EducationModelMixin
from .crf_model_mixin import CrfModelMixin


class EducationHoh(EducationModelMixin, CrfModelMixin):

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = (
            "Health Economics: Education (Person who earns the highest income)"
        )
        verbose_name_plural = (
            "Health Economics: Education (Person who earns the highest income)"
        )
