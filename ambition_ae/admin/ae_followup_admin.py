from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeFollowupModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_ae_admin
from ..models import AeFollowup


@admin.register(AeFollowup, site=ambition_ae_admin)
class AeFollowupAdmin(AeFollowupModelAdminMixin, SimpleHistoryAdmin):

    pass
