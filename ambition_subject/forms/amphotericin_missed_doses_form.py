from ambition_form_validators import AmphotericinMissedDosesFormValidator

from ..models import AmphotericinMissedDoses
from .form_mixins import InlineSubjectModelFormMixin


class AmphotericinMissedDosesForm(InlineSubjectModelFormMixin):

    form_validator_cls = AmphotericinMissedDosesFormValidator

    class Meta:
        model = AmphotericinMissedDoses
        fields = "__all__"
