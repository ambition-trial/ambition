from ambition_form_validators import MedicalExpensesFormValidator

from ..models import MedicalExpenses
from .form_mixins import SubjectModelFormMixin


class MedicalExpensesForm(SubjectModelFormMixin):

    form_validator_cls = MedicalExpensesFormValidator

    class Meta:
        model = MedicalExpenses
        fields = "__all__"
