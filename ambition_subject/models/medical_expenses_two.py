from edc_model.models import HistoricalRecords
from edc_visit_tracking.managers import CrfModelManager

from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin


class MedicalExpensesTwo(CrfModelMixin):

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Health Economics: Medical Expenses Part 2"
        verbose_name_plural = "Health Economics: Medical Expenses Part 2"
