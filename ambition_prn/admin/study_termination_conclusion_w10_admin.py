from copy import copy
from django.contrib import admin
from edc_action_item import action_fieldset_tuple, action_fields
from edc_model_admin import audit_fieldset_tuple, SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import ambition_prn_admin
from ..forms import StudyTerminationConclusionW10Form
from ..models import StudyTerminationConclusionW10


@admin.register(StudyTerminationConclusionW10, site=ambition_prn_admin)
class StudyTerminationConclusionW10Admin(
    ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin
):

    form = StudyTerminationConclusionW10Form

    additional_instructions = (
        "Note: if the patient is deceased, complete the Death Report "
        "before completing this form. "
    )

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "subject_identifier",
                    "offschedule_datetime",
                    "last_study_fu_date",
                    "termination_reason",
                )
            },
        ],
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {"termination_reason": admin.VERTICAL}

    list_display = (
        "subject_identifier",
        "dashboard",
        "offschedule_datetime",
        "last_study_fu_date",
        "tracking_identifier",
        "action_identifier",
    )

    list_filter = ("offschedule_datetime", "last_study_fu_date")

    search_fields = ("subject_identifier", "action_identifier", "tracking_identifier")

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        action_flds = copy(list(action_fields))
        action_flds.remove("action_identifier")
        fields = list(action_flds) + list(fields)
        return fields
