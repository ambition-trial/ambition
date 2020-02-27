from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import NOT_APPLICABLE, YES_NO, YES_NO_NA
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField
from edc_protocol.validators import date_not_before_study_start
from edc_visit_tracking.managers import CrfModelManager

from ..choices import (
    BACTERIA_TYPE,
    BLOOD_CULTURE_RESULTS_ORGANISM,
    BIOPSY_RESULTS_ORGANISM,
    CULTURE_RESULTS,
    POS_NEG_NA,
    URINE_CULTURE_RESULTS_ORGANISM,
    SPUTUM_GENEXPERT,
)
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin


class Microbiology(CrfModelMixin):

    urine_culture_performed = models.CharField(
        max_length=5,
        choices=YES_NO,
        help_text="only for patients with >50 white cells in urine",
    )

    urine_taken_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    urine_culture_results = models.CharField(
        verbose_name="Urine culture results, if completed",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    urine_culture_organism = models.CharField(
        verbose_name="If positive, organism",
        max_length=25,
        choices=URINE_CULTURE_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    urine_culture_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    blood_culture_performed = models.CharField(max_length=5, choices=YES_NO)

    blood_culture_results = models.CharField(
        verbose_name="Blood culture results, if completed",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    blood_taken_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    day_blood_taken = models.IntegerField(
        verbose_name="If positive, study day positive culture sample taken",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    blood_culture_organism = models.CharField(
        verbose_name="If growth positive, organism",
        max_length=50,
        choices=BLOOD_CULTURE_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    blood_culture_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    bacteria_identified = models.CharField(
        verbose_name="If bacteria, type",
        max_length=50,
        choices=BACTERIA_TYPE,
        default=NOT_APPLICABLE,
    )

    bacteria_identified_other = OtherCharField(max_length=100, null=True, blank=True)

    sputum_afb_performed = models.CharField(
        verbose_name="AFB microscopy performed?",
        max_length=5,
        choices=YES_NO,
        help_text="Was sputum AFB done?",
    )

    sputum_afb_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    sputum_results_afb = models.CharField(
        verbose_name="AFB results",
        max_length=10,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    sputum_performed = models.CharField(
        verbose_name="Culture performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_taken_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    sputum_results_culture = models.CharField(
        verbose_name="Culture results",
        max_length=10,
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
    )

    sputum_results_positive = models.CharField(
        verbose_name="If culture is positive, please specify:",
        max_length=50,
        null=True,
        blank=True,
    )

    sputum_genexpert_performed = models.CharField(
        verbose_name="Sputum Gene-Xpert performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    sputum_genexpert_date = models.DateField(
        verbose_name="Date sputum Gene-Xpert taken",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    sputum_result_genexpert = models.CharField(
        verbose_name="Sputum Gene-Xpert results",
        max_length=45,
        choices=SPUTUM_GENEXPERT,
        default=NOT_APPLICABLE,
    )

    tissue_biopsy_taken = models.CharField(max_length=5, choices=YES_NO)

    tissue_biopsy_results = models.CharField(
        verbose_name="If YES, results",
        max_length=10,
        choices=CULTURE_RESULTS,
        default=NOT_APPLICABLE,
    )

    biopsy_date = models.DateField(
        validators=[date_not_before_study_start, date_not_future], null=True, blank=True
    )

    day_biopsy_taken = models.IntegerField(
        verbose_name="If positive, Study day positive culture sample taken",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    tissue_biopsy_organism = models.CharField(
        verbose_name="If growth positive, organism",
        max_length=50,
        choices=BIOPSY_RESULTS_ORGANISM,
        default=NOT_APPLICABLE,
    )

    tissue_biopsy_organism_other = OtherCharField(max_length=50, null=True, blank=True)

    histopathology_report = models.TextField(null=True, blank=True)

    csf_genexpert_performed = models.CharField(
        verbose_name="CSF Gene-Xpert performed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    csf_genexpert_date = models.DateField(
        verbose_name="Date CSF Gene-Xpert taken",
        validators=[date_not_before_study_start, date_not_future],
        null=True,
        blank=True,
    )

    csf_result_genexpert = models.CharField(
        verbose_name="CSF Gene-Xpert results",
        max_length=45,
        choices=SPUTUM_GENEXPERT,
        default=NOT_APPLICABLE,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
