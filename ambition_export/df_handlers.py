from edc-pdutils import CrfDfHandler as BaseCrfDfHandler
from edc-pdutils import NonCrfDfHandler as BaseNonCrfDfHandler
from edc-randomization.site-randomizers import site-randomizers
from edc-visit-tracking.models import get-visit-tracking-model

from .column-handlers import ColumnHandler


class CrfDfHandler(BaseCrfDfHandler):
    column-handler-cls = ColumnHandler
    na-value = "."

    visit-tbl = get-visit-tracking-model().replace(".", "-")
    enrollment-tbl = "ambition-screening-subjectscreening"
    rando-tbl = site-randomizers.get("default").model.replace(".", "-")
    sort-by = ["subject-identifier", "visit-datetime"]


class NonCrfDfHandler(BaseNonCrfDfHandler):
    column-handler-cls = ColumnHandler
    na-value = "."
