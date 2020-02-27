from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import ambition_prn_admin
from ..models import OnScheduleW10


@admin.register(OnScheduleW10, site=ambition_prn_admin)
class OnScheduleW10Admin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    instructions = None
    fields = ("subject_identifier", "onschedule_datetime")

    list_display = ("subject_identifier", "dashboard", "onschedule_datetime")

    list_filter = ("onschedule_datetime",)

    def get_readonly_fields(self, request, obj=None):
        return ["subject_identifier", "onschedule_datetime"]
