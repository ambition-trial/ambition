from edc_pdutils import CrfDfHandler as BaseCrfDfHandler
from edc_pdutils import NonCrfDfHandler as BaseNonCrfDfHandler
from edc_randomization.utils import get_randomizationlist_model_name
from edc_visit_tracking.models import get_visit_tracking_model

from .column_handlers import ColumnHandler


class CrfDfHandler(BaseCrfDfHandler):

    column_handler_cls = ColumnHandler
    na_value = "."

    visit_tbl = get_visit_tracking_model().replace(".", "_")
    enrollment_tbl = "ambition_screening_subjectscreening"
    rando_tbl = get_randomizationlist_model_name().replace(".", "_")
    sort_by = ["subject_identifier", "visit_datetime"]


class NonCrfDfHandler(BaseNonCrfDfHandler):

    column_handler_cls = ColumnHandler
    na_value = "."
