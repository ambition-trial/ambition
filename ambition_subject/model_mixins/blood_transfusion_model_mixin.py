from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO


class BloodTransfusionModelMixin(models.Model):

    blood_received = models.CharField(
        verbose_name="Blood transfusion received?", max_length=25, choices=YES_NO
    )

    units = models.IntegerField(
        verbose_name="If YES, number of units",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
