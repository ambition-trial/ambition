from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeTmgModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_ae_admin
from ..models import AeTmg


@admin.register(AeTmg, site=ambition_ae_admin)
class AeTmgAdmin(AeTmgModelAdminMixin, SimpleHistoryAdmin):

    pass
