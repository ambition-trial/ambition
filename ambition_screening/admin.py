from django.contrib import admin, messages
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from .admin_site import ambition_screening_admin
from .forms import SubjectScreeningForm
from .models import SubjectScreening, SubjectScreeningDeleteError


@admin.register(SubjectScreening, site=ambition_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = SubjectScreeningForm

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    list_display = (
        "screening_identifier",
        "report_datetime",
        "consented",
        "gender",
        "age_in_years",
        "mental_status",
        "unsuitable",
    )

    list_filter = (
        "report_datetime",
        "consented",
        "gender",
        "age_in_years",
        "mental_status",
        "unsuitable_for_study",
    )

    radio_fields = {
        "gender": admin.VERTICAL,
        "meningitis_dx": admin.VERTICAL,
        "will_hiv_test": admin.VERTICAL,
        "mental_status": admin.VERTICAL,
        "consent_ability": admin.VERTICAL,
        "pregnancy": admin.VERTICAL,
        "breast_feeding": admin.VERTICAL,
        "previous_drug_reaction": admin.VERTICAL,
        "contraindicated_meds": admin.VERTICAL,
        "received_amphotericin": admin.VERTICAL,
        "received_fluconazole": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "gender",
                    "age_in_years",
                    "meningitis_dx",
                    "will_hiv_test",
                    "mental_status",
                    "consent_ability",
                    "pregnancy",
                    "preg_test_date",
                    "breast_feeding",
                    "previous_drug_reaction",
                    "contraindicated_meds",
                    "received_amphotericin",
                    "received_fluconazole",
                    "unsuitable_for_study",
                    "reasons_unsuitable",
                )
            },
        ),
        ("Blood Results", {"fields": ("alt", "neutrophil", "platelets")}),
    )

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    def unsuitable(self, obj=None):
        return obj.get_unsuitable_for_study_display()

    def delete_model(self, request, obj):
        try:
            super().delete_model(request, obj)
        except SubjectScreeningDeleteError as e:
            messages.add_message(request, messages.ERROR, f"{str(e)} Got `{obj}`.")
