from ambition_form_validators import FollowUpFormValidator
from ambition_form_validators import SignificantDiagnosesFormValidator

from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin
from ..models import FollowUp, FollowUpDiagnoses


class FollowUpForm(SubjectModelFormMixin):

    form_validator_cls = FollowUpFormValidator

    class Meta:
        model = FollowUp
        fields = "__all__"


class FollowUpDiagnosesForm(InlineSubjectModelFormMixin):

    form_validator_cls = SignificantDiagnosesFormValidator

    class Meta:
        model = FollowUpDiagnoses
        fields = "__all__"
