from ambition_form_validators import MicrobiologyFormValidator

from ..models import Microbiology
from .form_mixins import SubjectModelFormMixin


class MicrobiologyForm(SubjectModelFormMixin):

    form_validator_cls = MicrobiologyFormValidator

    class Meta:
        model = Microbiology
        fields = "__all__"
