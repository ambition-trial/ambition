from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel


class AntibioticTreatment(ListModelMixin, BaseUuidModel):

    pass


class MeningitisSymptom(ListModelMixin, BaseUuidModel):

    pass


class Neurological(ListModelMixin, BaseUuidModel):

    pass
