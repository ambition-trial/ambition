from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeSusarModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import ambition_ae_admin
from ..models import AeSusar


@admin.register(AeSusar, site=ambition_ae_admin)
class AeSusarAdmin(AeSusarModelAdminMixin, SimpleHistoryAdmin):

    pass
