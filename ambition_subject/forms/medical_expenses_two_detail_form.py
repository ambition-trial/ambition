from ambition_form_validators import MedicalExpensesTwoDetailFormValidator

from ..models import MedicalExpensesTwoDetail
from .form_mixins import InlineSubjectModelFormMixin


class MedicalExpensesTwoDetailForm(InlineSubjectModelFormMixin):

    form_validator_cls = MedicalExpensesTwoDetailFormValidator

    class Meta:
        model = MedicalExpensesTwoDetail
        fields = "__all__"
