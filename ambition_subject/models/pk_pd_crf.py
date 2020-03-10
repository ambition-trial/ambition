from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import HistoricalRecords
from edc_visit_tracking.managers import CrfModelManager

from ..choices import AMPHOTERICIN_FORMULATION
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin


class PkPdCrf(CrfModelMixin):

    # removed v 0.1.61
    albumin = models.IntegerField(
        verbose_name="Albumin", null=True, blank=True, help_text="Units in g/L"
    )

    amphotericin_given = models.CharField(
        verbose_name=(
            "Did the patient receive any amphotericin "
            "formulation in the last 24 hours?"
        ),
        choices=YES_NO,
        max_length=5,
        null=True,
    )

    amphotericin_formulation = models.CharField(
        verbose_name=("If Yes, Which formulation of amphotericin?"),
        choices=AMPHOTERICIN_FORMULATION,
        max_length=25,
        blank=True,
        null=True,
    )

    amphotericin_dose = models.IntegerField(
        verbose_name="Dose given", null=True, blank=True, help_text="Units in mg"
    )

    amphotericin_started_datetime = models.DateTimeField(
        verbose_name="Date and time started", null=True, blank=True
    )

    amphotericin_ended_datetime = models.DateTimeField(
        verbose_name="Date and time stopped", null=True, blank=True
    )

    amphotericin_full_dose_given = models.CharField(
        verbose_name="Was the entire dose given?",
        choices=YES_NO,
        max_length=5,
        null=True,
        blank=True,
    )

    flucytosine_dose = models.IntegerField(
        verbose_name="Flucytosine dose?",
        null=True,
        blank=True,
        help_text="Total of all doses given. Units in mg",
    )

    flucytosine_dose_one_given = models.CharField(
        verbose_name="Flucytosine <b><u>DOSE&nbsp;1</u></b> given? ",
        choices=YES_NO,
        max_length=5,
        null=True,
        blank=True,
    )

    flucytosine_dose_one_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "Date and time Flucytosine <u>DOSE&nbsp;1</u> was swallowed?"
        ),
        null=True,
        blank=True,
    )

    flucytosine_dose_one = models.IntegerField(
        verbose_name="Flucytosine <u>DOSE&nbsp;1</u>",
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        null=True,
        blank=True,
        help_text="Units in mg",
    )

    flucytosine_dose_two_given = models.CharField(
        verbose_name="Flucytosine <b><u>DOSE&nbsp;2</u></b> given? ",
        choices=YES_NO_NA,
        max_length=5,
        null=True,
        blank=True,
    )

    flucytosine_dose_two_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "Date and time Flucytosine <u>DOSE&nbsp;2</u> was swallowed?"
        ),
        null=True,
        blank=True,
    )

    flucytosine_dose_two = models.IntegerField(
        verbose_name="Flucytosine <u>DOSE&nbsp;2</u>",
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        null=True,
        blank=True,
        help_text="Units in mg",
    )

    flucytosine_dose_three_given = models.CharField(
        verbose_name="Flucytosine <b><u>DOSE&nbsp;3</u></b> given? ",
        choices=YES_NO_NA,
        max_length=5,
        null=True,
        blank=True,
    )

    flucytosine_dose_three_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "Date and time Flucytosine <u>DOSE&nbsp;3</u> was swallowed?"
        ),
        null=True,
        blank=True,
    )

    flucytosine_dose_three = models.IntegerField(
        verbose_name="Flucytosine <u>DOSE&nbsp;3</u>",
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        null=True,
        blank=True,
        help_text="Units in mg",
    )

    flucytosine_dose_four_given = models.CharField(
        verbose_name="Flucytosine <b><u>DOSE&nbsp;4</u></b> given? ",
        choices=YES_NO_NA,
        max_length=5,
        null=True,
        blank=True,
    )

    flucytosine_dose_four_datetime = models.DateTimeField(
        verbose_name=mark_safe(
            "Date and time Flucytosine <u>DOSE&nbsp;4</u> was swallowed?"
        ),
        null=True,
        blank=True,
    )

    flucytosine_dose_four = models.IntegerField(
        verbose_name="Flucytosine <u>DOSE&nbsp;4</u>",
        validators=[MinValueValidator(0), MaxValueValidator(9999)],
        null=True,
        blank=True,
        help_text="Units in mg",
    )

    flucytosine_dose_reason_missed = models.TextField(
        verbose_name="If any Flucytosine doses not given, provide reason",
        max_length=75,
        null=True,
        blank=True,
    )

    fluconazole_dose = models.IntegerField(
        verbose_name="Fluconazole dose?", null=True, blank=True, help_text="Units in mg"
    )

    fluconazole_dose_given = models.CharField(
        verbose_name="Was the Fluconazole dose given?",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=11,
        null=True,
    )

    fluconazole_dose_datetime = models.DateTimeField(
        verbose_name="Date and time Fluconazole was swallowed?", null=True, blank=True
    )

    fluconazole_dose_reason_missed = models.TextField(
        verbose_name="If Fluconazole dose not given, provide reason",
        max_length=75,
        null=True,
        blank=True,
    )

    blood_sample_one_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;1</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_two_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;2</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_three_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;3</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_four_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;4</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_five_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;5</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_six_datetime = models.DateTimeField(
        verbose_name=mark_safe("Date and time blood <u>SAMPLE&nbsp;6</u> taken?"),
        null=True,
        blank=True,
    )

    blood_sample_missed = models.CharField(
        verbose_name="Were any blood samples missed?",
        choices=YES_NO,
        max_length=5,
        null=True,
        blank=True,
    )

    blood_sample_reason_missed = models.TextField(
        verbose_name="If any blood samples missed, provide reason",
        max_length=75,
        null=True,
        blank=True,
    )

    pre_dose_lp = models.CharField(
        verbose_name="Is this a pre-dose LP?",
        choices=YES_NO,
        max_length=5,
        null=True,
        blank=True,
    )

    post_dose_lp = models.CharField(
        verbose_name="Is this a post-dose LP?",
        choices=YES_NO,
        max_length=5,
        null=True,
        blank=True,
    )

    time_csf_sample_taken = models.DateTimeField(
        verbose_name="What date and time was the CSF sample taken?",
        null=True,
        blank=True,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "PK/PD"
        verbose_name_plural = "PK/PD"
