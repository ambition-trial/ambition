from edc_adverse_event.model_mixins import AeInitialModelMixin
from edc_model.models import BaseUuidModel

from .ae_ambition_model_mixin import AeAmbitionModelMixin


class AeInitial(AeInitialModelMixin, AeAmbitionModelMixin, BaseUuidModel):
    class Meta(AeInitialModelMixin.Meta):
        pass
