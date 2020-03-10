from ambition_form_validators import PkPdCrfFormValidator

from ..models import PkPdCrf
from .form_mixins import SubjectModelFormMixin


class PkPdCrfForm(SubjectModelFormMixin):

    form_validator_cls = PkPdCrfFormValidator

    class Meta:
        model = PkPdCrf
        fields = "__all__"
