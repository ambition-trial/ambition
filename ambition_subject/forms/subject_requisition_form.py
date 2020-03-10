from ambition_labs.panels import chemistry_panel, chemistry_alt_panel
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES, NO
from edc_lab.forms import RequisitionFormMixin
from edc_lab.form_validators import RequisitionFormValidator
from edc_metadata.constants import NOT_REQUIRED

from ..models import SubjectRequisition
from .form_mixins import SubjectModelFormMixin
from edc_form_validators.form_validator_mixin import FormValidatorMixin


class SubjectRequisitionForm(
    RequisitionFormMixin, SubjectModelFormMixin, FormValidatorMixin
):

    form_validator_cls = RequisitionFormValidator

    requisition_identifier = forms.CharField(
        label="Requisition identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("reason_not_drawn") == NOT_REQUIRED:
            if self.cleaned_data.get("panel") == chemistry_panel.panel_model_obj:
                try:
                    self._meta.model.objects.get(
                        subject_visit=cleaned_data.get("subject_visit"),
                        panel=chemistry_alt_panel.panel_model_obj,
                        is_drawn=YES,
                    )
                except ObjectDoesNotExist:
                    raise forms.ValidationError(
                        {
                            "reason_not_drawn": "Invalid choice. At least one "
                            "chemistry panel is expected."
                        }
                    )
            else:
                raise forms.ValidationError(
                    {
                        "reason_not_drawn": "Invalid choice. Not expected "
                        "for this panel"
                    }
                )
        if (
            self.cleaned_data.get("panel") == chemistry_alt_panel.panel_model_obj
            and self.cleaned_data.get("is_drawn") == NO
        ):
            try:
                self._meta.model.objects.get(
                    subject_visit=cleaned_data.get("subject_visit"),
                    panel=chemistry_panel.panel_model_obj,
                    reason_not_drawn=NOT_REQUIRED,
                )
            except ObjectDoesNotExist:
                pass
            else:
                raise forms.ValidationError(
                    f'Remove the "{chemistry_panel.name}" requisition before '
                    f"setting this requisition to not drawn."
                )
        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = "__all__"
