from ambition_form_validators import Week2FormValidator

from ..models import Week2
from .form_mixins import SubjectModelFormMixin


class Week2Form(SubjectModelFormMixin):

    form_validator_cls = Week2FormValidator

    class Meta:
        model = Week2
        fields = "__all__"
