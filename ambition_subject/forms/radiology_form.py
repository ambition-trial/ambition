from ambition_form_validators import RadiologyFormValidator

from ..models import Radiology
from .form_mixins import SubjectModelFormMixin


class RadiologyForm(SubjectModelFormMixin):

    form_validator_cls = RadiologyFormValidator

    class Meta:
        model = Radiology
        fields = "__all__"
