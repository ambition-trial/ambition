from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_adverse_event.forms import AeInitialForm
from edc_adverse_event.modeladmin_mixins import AeInitialModelAdminMixin
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin

from ..admin_site import ambition_ae_admin
from ..form_validators.ae_initial import AeInitialFormValidator
from ..models import AeInitial


class CustomAeInitialForm(AeInitialForm):

    form_validator = AeInitialFormValidator


@admin.register(AeInitial, site=ambition_ae_admin)
class AeInitialAdmin(AeInitialModelAdminMixin, SimpleHistoryAdmin):

    form = CustomAeInitialForm

    email_contact = settings.EMAIL_CONTACTS.get("ae_reports")
    additional_instructions = mark_safe(
        "Complete the initial AE report and forward to the TMG. "
        f'Email to <a href="mailto:{email_contact}">{email_contact}</a>'
    )

    fieldsets = (
        (
            "Part 1:",
            {
                "fields": (
                    "subject_identifier",
                    "ae_classification",
                    "ae_classification_other",
                    "report_datetime",
                    "ae_description",
                    "ae_awareness_date",
                    "ae_start_date",
                    "ae_grade",
                    "ae_study_relation_possibility",
                )
            },
        ),
        (
            "Part 2: Relationship to study drug",
            {
                "fields": (
                    "fluconazole_relation",
                    "flucytosine_relation",
                    "amphotericin_relation",
                )
            },
        ),
        (
            "Part 3:",
            {
                "fields": (
                    "ae_cause",
                    "ae_cause_other",
                    "ae_treatment",
                    "ae_cm_recurrence",
                )
            },
        ),
        ("Part 4:", {"fields": ("sae", "sae_reason", "susar", "susar_reported")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "ae_cause": admin.VERTICAL,
        "ae_classification": admin.VERTICAL,
        "ae_cm_recurrence": admin.VERTICAL,
        "ae_grade": admin.VERTICAL,
        "ae_study_relation_possibility": admin.VERTICAL,
        "amphotericin_relation": admin.VERTICAL,
        "fluconazole_relation": admin.VERTICAL,
        "flucytosine_relation": admin.VERTICAL,
        "sae": admin.VERTICAL,
        "sae_reason": admin.VERTICAL,
        "susar": admin.VERTICAL,
        "susar_reported": admin.VERTICAL,
    }
