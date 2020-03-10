from ambition_lists.models import AbnormalResultsReason, CXRType, InfiltrateLocation
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, NOT_APPLICABLE
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future, datetime_not_future
from edc_visit_tracking.managers import CrfModelManager

from ..choices import BRAIN_IMAGINING_REASON
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin


class Radiology(CrfModelMixin):

    cxr_done = models.CharField(
        verbose_name="Is CXR done", choices=YES_NO, max_length=5
    )

    cxr_date = models.DateField(
        verbose_name="If yes, when was CXR done",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    cxr_type = models.ManyToManyField(
        CXRType, verbose_name="If YES, result", blank=True
    )

    infiltrate_location = models.ManyToManyField(
        InfiltrateLocation, verbose_name="If infiltrates, specify location", blank=True
    )

    cxr_description = models.TextField(
        verbose_name="Description/Comments", blank=True, null=True
    )

    ct_performed = models.CharField(
        verbose_name="CT/MRI brain scan performed?", choices=YES_NO, max_length=5
    )

    ct_performed_date = models.DateTimeField(
        verbose_name="Date CT performed",
        validators=[datetime_not_future],
        editable=True,
        blank=True,
        null=True,
    )

    scanned_with_contrast = models.CharField(
        verbose_name="CT/MRI brain scan performed with contrast?",
        blank=False,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=5,
        null=False,
    )

    brain_imaging_reason = models.CharField(
        verbose_name="Reason for brain imaging",
        blank=False,
        choices=BRAIN_IMAGINING_REASON,
        default=NOT_APPLICABLE,
        max_length=25,
        null=True,
    )

    brain_imaging_reason_other = models.CharField(
        verbose_name="If other, please specify", blank=True, max_length=50, null=True
    )

    are_results_abnormal = models.CharField(
        blank=False, choices=YES_NO_NA, default=NOT_APPLICABLE, null=False, max_length=5
    )

    abnormal_results_reason = models.ManyToManyField(
        AbnormalResultsReason,
        verbose_name="If results are abnormal, what is the reason?",
        blank=True,
    )

    abnormal_results_reason_other = models.CharField(
        verbose_name="If other, please specify reason",
        blank=True,
        max_length=50,
        null=True,
    )

    infarcts_location = models.CharField(
        verbose_name="If results are abnormal because of Infarcts, what is the location?",
        blank=True,
        max_length=50,
        null=True,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Radiology"
        verbose_name_plural = "Radiology"
