from django.contrib import admin
from edc_fieldsets import Fieldset
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin

from ..admin_site import ambition_subject_admin
from ..constants import DAY1, DAY7, DAY14
from ..forms import PkPdCrfForm, PkPdExtraSamplesForm
from ..models import PkPdCrf, PkPdExtraSamples
from .modeladmin import CrfModelAdmin

day1_fields = Fieldset(
    "blood_sample_one_datetime",
    "blood_sample_two_datetime",
    "blood_sample_three_datetime",
    "blood_sample_four_datetime",
    "blood_sample_five_datetime",
    "blood_sample_missed",
    "blood_sample_reason_missed",
    section="Blood Results",
)

day7_fields = (
    Fieldset(
        "blood_sample_one_datetime",
        "blood_sample_two_datetime",
        "blood_sample_three_datetime",
        "blood_sample_four_datetime",
        "blood_sample_five_datetime",
        "blood_sample_six_datetime",
        "blood_sample_missed",
        "blood_sample_reason_missed",
        section="Blood Results",
    ),
    Fieldset("pre_dose_lp", "post_dose_lp", "time_csf_sample_taken", section="CSF"),
)

day14_samples = Fieldset(
    "pre_dose_lp", "post_dose_lp", "time_csf_sample_taken", section="CSF"
)


class PkPdExtraSamplesAdmin(StackedInlineMixin, admin.StackedInline):

    model = PkPdExtraSamples
    form = PkPdExtraSamplesForm
    extra = 0

    fieldsets = (
        (
            None,
            {"fields": ("extra_csf_samples_datetime", "extra_blood_samples_datetime")},
        ),
        audit_fieldset_tuple,
    )


@admin.register(PkPdCrf, site=ambition_subject_admin)
class PkPdCrfAdmin(CrfModelAdmin):

    form = PkPdCrfForm

    inlines = [PkPdExtraSamplesAdmin]

    conditional_fieldsets = {DAY1: day1_fields, DAY7: day7_fields, DAY14: day14_samples}

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_visit",
                    "report_datetime",
                    # 'albumin'
                )
            },
        ),
        (
            "Amphotericin",
            {
                "fields": (
                    "amphotericin_given",
                    "amphotericin_formulation",
                    "amphotericin_dose",
                    "amphotericin_started_datetime",
                    "amphotericin_ended_datetime",
                    "amphotericin_full_dose_given",
                )
            },
        ),
        (
            "Flucytosine",
            {
                "fields": (
                    "flucytosine_dose",
                    "flucytosine_dose_one_given",
                    "flucytosine_dose_one_datetime",
                    "flucytosine_dose_one",
                    "flucytosine_dose_two_given",
                    "flucytosine_dose_two_datetime",
                    "flucytosine_dose_two",
                    "flucytosine_dose_three_given",
                    "flucytosine_dose_three_datetime",
                    "flucytosine_dose_three",
                    "flucytosine_dose_four_given",
                    "flucytosine_dose_four_datetime",
                    "flucytosine_dose_four",
                    "flucytosine_dose_reason_missed",
                )
            },
        ),
        (
            "Fluconazole",
            {
                "fields": (
                    "fluconazole_dose",
                    "fluconazole_dose_datetime",
                    "fluconazole_dose_given",
                    "fluconazole_dose_reason_missed",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "amphotericin_given": admin.VERTICAL,
        "amphotericin_formulation": admin.VERTICAL,
        "amphotericin_full_dose_given": admin.VERTICAL,
        "flucytosine_dose_one_given": admin.VERTICAL,
        "flucytosine_dose_two_given": admin.VERTICAL,
        "flucytosine_dose_three_given": admin.VERTICAL,
        "flucytosine_dose_four_given": admin.VERTICAL,
        "fluconazole_dose_given": admin.VERTICAL,
        "blood_sample_missed": admin.VERTICAL,
        "pre_dose_lp": admin.VERTICAL,
        "post_dose_lp": admin.VERTICAL,
    }
