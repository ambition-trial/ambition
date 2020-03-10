from ambition_form_validators import PreviousOpportunisticInfectionFormValidator

from ..models import PreviousOpportunisticInfection
from .form_mixins import InlineSubjectModelFormMixin


class PreviousOpportunisticInfectionForm(InlineSubjectModelFormMixin):

    form_validator_cls = PreviousOpportunisticInfectionFormValidator

    class Meta:
        model = PreviousOpportunisticInfection
        fields = "__all__"
