from ambition_form_validators import SignificantDiagnosesFormValidator

from ..models import SignificantDiagnoses
from .form_mixins import InlineSubjectModelFormMixin


class SignificantDiagnosesForm(InlineSubjectModelFormMixin):

    form_validator_cls = SignificantDiagnosesFormValidator

    class Meta:
        model = SignificantDiagnoses
        fields = "__all__"
