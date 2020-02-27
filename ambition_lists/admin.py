from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import ambition_lists_admin
from .models import (
    Antibiotic,
    Day14Medication,
    Medication,
    Neurological,
    Symptom,
    OtherDrug,
    AbnormalResultsReason,
    CXRType,
    InfiltrateLocation,
    MissedDoses,
    ArvRegimens,
)


@admin.register(Antibiotic, site=ambition_lists_admin)
class AntibioticAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Day14Medication, site=ambition_lists_admin)
class Day14MedicationAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Medication, site=ambition_lists_admin)
class MedicationAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Neurological, site=ambition_lists_admin)
class NeurologicalAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Symptom, site=ambition_lists_admin)
class SymptomAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OtherDrug, site=ambition_lists_admin)
class OtherDrugAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(AbnormalResultsReason, site=ambition_lists_admin)
class AbnormalResultsReasonAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(CXRType, site=ambition_lists_admin)
class CXRTypeAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(InfiltrateLocation, site=ambition_lists_admin)
class InfiltrateLocationAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(MissedDoses, site=ambition_lists_admin)
class MissedDosesAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArvRegimens, site=ambition_lists_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
