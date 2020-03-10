from ..models import PkPdExtraSamples
from .form_mixins import InlineSubjectModelFormMixin


class PkPdExtraSamplesForm(InlineSubjectModelFormMixin):
    class Meta:
        model = PkPdExtraSamples
        fields = "__all__"
