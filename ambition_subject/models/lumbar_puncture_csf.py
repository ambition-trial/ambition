from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO_NA, NOT_APPLICABLE
from edc_model.models import HistoricalRecords
from edc_model.validators import datetime_not_future
from edc_reportable import (
    GRAMS_PER_LITER,
    MILLIMOLES_PER_LITER,
    MILLIGRAMS_PER_DECILITER,
)
from edc_reportable import MM3_DISPLAY
from edc_visit_tracking.managers import CrfModelManager

from ..choices import LP_REASON, POS_NEG, MG_MMOL_UNITS, MM3_PERC_UNITS
from ..choices import YES_NO_NOT_DONE_WAIT_RESULTS
from ..constants import AWAITING_RESULTS
from ..managers import CurrentSiteManager
from ..model_mixins import BiosynexSemiQuantitativeCragMixin
from .crf_model_mixin import CrfModelMixin
from .subject_requisition import SubjectRequisition


class LumbarPunctureCsf(CrfModelMixin, BiosynexSemiQuantitativeCragMixin):

    lp_datetime = models.DateTimeField(
        verbose_name="LP Date and Time", validators=[datetime_not_future]
    )

    qc_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="qcrequisition",
        verbose_name="QC Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    qc_assay_datetime = models.DateTimeField(
        verbose_name="QC Result Report Date and Time",
        validators=[datetime_not_future],
        blank=True,
        null=True,
    )

    csf_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="csfrequisition",
        verbose_name="CSF Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    csf_assay_datetime = models.DateTimeField(
        verbose_name="CSF Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    reason_for_lp = models.CharField(
        verbose_name="Reason for LP", max_length=50, choices=LP_REASON
    )

    opening_pressure = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        help_text=mark_safe("Units cm of H<sub>2</sub>O"),
    )

    closing_pressure = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        help_text=mark_safe("Units cm of H<sub>2</sub>O"),
    )

    csf_amount_removed = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="CSF amount removed ",
        validators=[MinValueValidator(1)],
        help_text="Units ml",
    )

    quantitative_culture = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100_000_000)],
        help_text="Units CFU/ml",
    )

    csf_culture = models.CharField(
        verbose_name="Other organism (non-Cryptococcus)",
        max_length=18,
        choices=YES_NO_NOT_DONE_WAIT_RESULTS,
        default=AWAITING_RESULTS,
        help_text="Complete after getting the results.",
    )

    other_csf_culture = models.CharField(
        verbose_name="If YES, specify organism:", max_length=75, blank=True, null=True
    )

    csf_wbc_cell_count = models.IntegerField(
        verbose_name="Total CSF WBC cell count:",
        help_text=mark_safe(f"acceptable units are {MM3_DISPLAY}"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    differential_lymphocyte_count = models.IntegerField(
        verbose_name="Differential lymphocyte cell count:",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text=mark_safe(f"acceptable units are {MM3_DISPLAY} or %"),
    )

    differential_lymphocyte_unit = models.CharField(
        choices=MM3_PERC_UNITS, max_length=6, null=True, blank=True
    )

    differential_neutrophil_count = models.IntegerField(
        verbose_name="Differential neutrophil cell count:",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text=mark_safe(f"acceptable units are {MM3_DISPLAY} or %"),
    )

    differential_neutrophil_unit = models.CharField(
        choices=MM3_PERC_UNITS, max_length=6, null=True, blank=True
    )

    india_ink = models.CharField(max_length=15, choices=POS_NEG, null=True, blank=True)

    csf_glucose = models.DecimalField(
        verbose_name="CSF glucose:",
        decimal_places=1,
        max_digits=3,
        blank=True,
        null=True,
        help_text=f"Units in {MILLIMOLES_PER_LITER} or {MILLIGRAMS_PER_DECILITER}",
    )

    csf_glucose_units = models.CharField(
        verbose_name="CSF glucose units:",
        max_length=6,
        choices=MG_MMOL_UNITS,
        blank=True,
        null=True,
    )

    csf_protein = models.DecimalField(
        verbose_name="CSF protein:",
        decimal_places=2,
        max_digits=4,
        blank=True,
        null=True,
        help_text=f"Units in {GRAMS_PER_LITER}",
    )

    csf_cr_ag = models.CharField(
        verbose_name="CSF CrAg:", max_length=15, choices=POS_NEG, blank=True, null=True
    )

    csf_cr_ag_lfa = models.CharField(
        verbose_name="CSF CrAg done by IMMY CrAg LFA:",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Lumbar Puncture/Cerebrospinal Fluid"
        verbose_name_plural = "Lumbar Puncture/Cerebrospinal Fluid"
