from django.db import models
from edc_model.validators import date_not_future

from ..choices import SIGNIFICANT_DX


class SignificantDiagnosesModelMixin(models.Model):

    possible_diagnoses = models.CharField(
        verbose_name="Significant diagnoses:",
        max_length=25,
        choices=SIGNIFICANT_DX,
        blank=True,
        null=True,
    )

    dx_date = models.DateField(
        verbose_name="Date of diagnosis:",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    dx_other = models.CharField(
        verbose_name="If other, please specify:", max_length=50, null=True, blank=True
    )

    class Meta:
        abstract = True
