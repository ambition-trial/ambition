from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from ..admin_site import ambition_ae_admin
from ..models import AntibioticTreatment, MeningitisSymptom, Neurological


@admin.register(AntibioticTreatment, site=ambition_ae_admin)
class AntibioticTreatmentAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(MeningitisSymptom, site=ambition_ae_admin)
class MeningitisSymptomAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Neurological, site=ambition_ae_admin)
class NeurologicalAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
