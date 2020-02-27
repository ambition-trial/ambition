from edc_lab.model_mixins import RequisitionModelMixin
from edc_model.models import BaseUuidModel
from edc_reference.model_mixins import ReferenceModelMixin

# for reference by old migrations
from edc_lab.managers import RequisitionManager as Manager  # noqa


class SubjectRequisition(RequisitionModelMixin, ReferenceModelMixin, BaseUuidModel):
    class Meta(RequisitionModelMixin.Meta):
        pass
