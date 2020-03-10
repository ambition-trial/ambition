from ambition_form_validators import FluconazoleMissedDosesFormValidator

from ..models import FluconazoleMissedDoses
from .form_mixins import InlineSubjectModelFormMixin


class FluconazoleMissedDosesForm(InlineSubjectModelFormMixin):

    form_validator_cls = FluconazoleMissedDosesFormValidator

    class Meta:
        model = FluconazoleMissedDoses
        fields = "__all__"
