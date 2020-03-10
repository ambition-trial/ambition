from edc_adverse_event.model_mixins.ae_susar import AeSusarModelMixin
from edc_model.models import BaseUuidModel


class AeSusar(AeSusarModelMixin, BaseUuidModel):
    class Meta(AeSusarModelMixin.Meta):
        pass
