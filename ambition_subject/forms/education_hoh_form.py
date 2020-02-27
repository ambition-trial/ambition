from ambition_form_validators import EducationFormValidator

from ..models import EducationHoh
from .form_mixins import SubjectModelFormMixin


class EducationHohForm(SubjectModelFormMixin):

    form_validator_cls = EducationFormValidator

    class Meta:
        model = EducationHoh
        fields = "__all__"

        labels = {
            "profession": "What is their profession?",
            "education_years": "How many years of education did they complete?",
            "education_certificate": "What is their highest education certificate?",
            "elementary": "Did they go to elementary/primary school?",
            "secondary": "Did they go to secondary school?",
            "higher_education": "Did they go to higher education?",
        }
