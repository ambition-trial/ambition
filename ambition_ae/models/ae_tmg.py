from edc_adverse_event.model_mixins.ae_tmg.ae_tmg_model_mixin import AeTmgModelMixin
from edc_model.models import BaseUuidModel


class AeTmg(AeTmgModelMixin, BaseUuidModel):
    class Meta(AeTmgModelMixin.Meta):
        pass
