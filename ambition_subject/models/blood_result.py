from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.validators import datetime_not_future
from edc_registration.models import RegisteredSubject
from edc_reportable import CELLS_PER_MILLIMETER_CUBED, MILLIMOLES_PER_LITER
from edc_reportable import COPIES_PER_MILLILITER
from edc_reportable import IU_LITER, GRAMS_PER_DECILITER, TEN_X_9_PER_LITER
from edc_reportable import site_reportables
from edc_visit_tracking.managers import CrfModelManager

from ..constants import BLOOD_RESULTS_ACTION
from ..choices import MG_MMOL_UNITS, MG_UMOL_UNITS, REPORTABLE
from ..managers import CurrentSiteManager
from ..model_mixins import BiosynexSemiQuantitativeCragMixin
from .crf_model_mixin import CrfModelMixin
from .subject_requisition import SubjectRequisition


class BloodResult(
    CrfModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BiosynexSemiQuantitativeCragMixin,
):

    action_name = BLOOD_RESULTS_ACTION

    tracking_identifier_prefix = "BR"

    ft_fields = ["creatinine", "urea", "sodium", "potassium", "magnesium", "alt"]

    cbc_fields = ["haemoglobin", "wbc", "neutrophil", "platelets"]

    ft_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="ft",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    ft_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    cbc_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="cbc",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    cbc_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    cd4_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="cd4",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    cd4_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    vl_requisition = models.ForeignKey(
        SubjectRequisition,
        on_delete=PROTECT,
        related_name="vl",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    vl_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    wbc = models.DecimalField(
        verbose_name="WBC", decimal_places=2, max_digits=6, null=True, blank=True
    )

    wbc_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),),
        null=True,
        blank=True,
    )

    wbc_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    wbc_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    platelets = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        null=True,
        blank=True,
    )

    platelets_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),),
        null=True,
        blank=True,
    )

    platelets_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    platelets_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    haemoglobin = models.DecimalField(
        decimal_places=1, max_digits=6, null=True, blank=True
    )

    haemoglobin_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),),
        null=True,
        blank=True,
    )

    haemoglobin_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    haemoglobin_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    neutrophil = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, blank=True
    )

    neutrophil_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),),
        null=True,
        blank=True,
    )

    neutrophil_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    neutrophil_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    creatinine = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, blank=True
    )

    creatinine_units = models.CharField(
        verbose_name="units",
        choices=MG_UMOL_UNITS,
        max_length=25,
        null=True,
        blank=True,
    )

    creatinine_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    creatinine_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    sodium = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999)], null=True, blank=True
    )

    sodium_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    sodium_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    sodium_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    potassium = models.DecimalField(
        decimal_places=1, max_digits=2, null=True, blank=True
    )

    potassium_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),),
        null=True,
        blank=True,
    )

    potassium_abnormal = models.CharField(
        verbose_name="abnormal",
        choices=YES_NO,
        # default=NO,
        max_length=25,
        null=True,
        blank=True,
    )

    potassium_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        # default=NOT_APPLICABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    magnesium = models.DecimalField(
        decimal_places=2, max_digits=6, null=True, blank=True
    )

    magnesium_units = models.CharField(
        verbose_name="units",
        choices=MG_MMOL_UNITS,
        null=True,
        blank=True,
        max_length=25,
    )

    magnesium_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, null=True, blank=True, max_length=25
    )

    magnesium_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        null=True,
        blank=True,
        max_length=25,
    )

    alt = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2999)],
        verbose_name="ALT",
        null=True,
        blank=True,
    )

    alt_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((IU_LITER, IU_LITER),),
        null=True,
        blank=True,
    )

    alt_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    alt_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    urea = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)

    urea_units = models.CharField(
        verbose_name="units",
        choices=MG_MMOL_UNITS,
        max_length=25,
        null=True,
        blank=True,
    )

    urea_abnormal = models.CharField(
        verbose_name="abnormal",
        choices=YES_NO,
        # default=NO,
        max_length=25,
        null=True,
        blank=True,
    )

    urea_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    cd4 = models.IntegerField(
        verbose_name="abs CD4",
        validators=[MinValueValidator(0), MaxValueValidator(999)],
        blank=True,
        null=True,
    )

    cd4_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED),),
        null=True,
        blank=True,
    )

    cd4_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    cd4_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    vl = models.FloatField(
        verbose_name="Viral Load",
        validators=[MinValueValidator(0.0)],
        blank=True,
        null=True,
    )

    vl_units = models.CharField(
        verbose_name="units",
        max_length=10,
        choices=((COPIES_PER_MILLILITER, COPIES_PER_MILLILITER),),
        null=True,
        blank=True,
    )

    vl_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    vl_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    results_abnormal = models.CharField(
        verbose_name="Are any of the above results abnormal?",
        choices=YES_NO,
        max_length=25,
    )

    results_reportable = models.CharField(
        verbose_name="If any results are abnormal, are results within grade III "
        "or above?",
        max_length=25,
        choices=YES_NO_NA,
        help_text=(
            "If YES, this value will open Adverse Event Form.<br/><br/>"
            "Note: On Day 1 only abnormal bloods should not be reported as adverse"
            "events."
        ),
    )

    summary = models.TextField(null=True, blank=True)

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    def save(self, *args, **kwargs):
        self.summary = "\n".join(self.get_summary())
        super().save(*args, **kwargs)

    def get_summary(self):
        registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )
        opts = dict(
            gender=registered_subject.gender,
            dob=registered_subject.dob,
            report_datetime=self.subject_visit.report_datetime,
        )
        summary = []
        for field in [f.name for f in self._meta.fields]:
            value = getattr(self, field)
            grp = site_reportables.get("ambition").get(field)
            if value and grp:
                units = getattr(self, f"{field}_units")
                opts.update(units=units)
                grade = grp.get_grade(value, **opts)
                if grade and grade.grade:
                    summary.append(f"{field}: {grade.description}.")
                elif not grade:
                    normal = grp.get_normal(value, **opts)
                    if not normal:
                        summary.append(f"{field}: {value} {units} is abnormal")
        return summary

    def get_action_item_reason(self):
        return self.summary

    @property
    def abnormal(self):
        return self.results_abnormal

    @property
    def reportable(self):
        return self.results_reportable

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Blood Result"
        verbose_name_plural = "Blood Results"
