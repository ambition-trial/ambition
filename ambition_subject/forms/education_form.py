from ambition_form_validators import EducationFormValidator

from ..models import Education
from .form_mixins import SubjectModelFormMixin


class EducationForm(SubjectModelFormMixin):

    form_validator_cls = EducationFormValidator

    class Meta:
        model = Education
        fields = "__all__"
