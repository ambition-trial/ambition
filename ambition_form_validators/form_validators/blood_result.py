from ambition_labs.panels import cd4_panel, viral_load_panel, fbc_panel
from ambition_labs.panels import chemistry_panel, chemistry_alt_panel
from ambition_visit_schedule.constants import DAY1
from django.apps import apps as django_apps
from django.forms import forms
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_form_validators import FormValidator
from edc_lab import CrfRequisitionFormValidatorMixin
from edc_reportable import GRADE3, GRADE4, ReportablesFormValidatorMixin


class BloodResultFormValidator(
    ReportablesFormValidatorMixin, CrfRequisitionFormValidatorMixin, FormValidator
):

    reportable_grades = [GRADE3, GRADE4]

    def clean(self):
        Site = django_apps.get_model("sites.site")
        self.required_if_true(
            any(
                [
                    self.cleaned_data.get(f) is not None
                    for f in [f for f in self.instance.ft_fields]
                ]
            ),
            field_required="ft_requisition",
        )
        self.validate_requisition(
            "ft_requisition", "ft_assay_datetime", chemistry_panel, chemistry_alt_panel
        )

        self.required_if_true(
            any(
                [
                    self.cleaned_data.get(f) is not None
                    for f in [f for f in self.instance.cbc_fields]
                ]
            ),
            field_required="cbc_requisition",
        )
        self.validate_requisition("cbc_requisition", "cbc_assay_datetime", fbc_panel)

        self.required_if_true(
            self.cleaned_data.get("cd4") is not None, field_required="cd4_requisition"
        )
        self.validate_requisition("cd4_requisition", "cd4_assay_datetime", cd4_panel)

        self.required_if_true(
            self.cleaned_data.get("vl") is not None, field_required="vl_requisition"
        )
        self.validate_requisition(
            "vl_requisition", "vl_assay_datetime", viral_load_panel
        )

        self.validate_reportable_fields(reference_list_name="ambition")

        if (
            self.cleaned_data.get("subject_visit").visit_code == DAY1
            and self.cleaned_data.get("subject_visit").visit_code_sequence == 0
        ):
            if (
                Site.objects.get_current().name not in ["gaborone", "blantyre"]
                and self.cleaned_data.get("bios_crag") != NOT_APPLICABLE
            ):
                raise forms.ValidationError(
                    {f"bios_crag": "This field is not applicable"}
                )
            self.applicable_if(
                YES, field="bios_crag", field_applicable="crag_control_result"
            )

            self.applicable_if(
                YES, field="bios_crag", field_applicable="crag_t1_result"
            )

            self.applicable_if(
                YES, field="bios_crag", field_applicable="crag_t2_result"
            )
