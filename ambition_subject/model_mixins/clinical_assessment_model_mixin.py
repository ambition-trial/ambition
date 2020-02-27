from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ..choices import YES_NO_ND


class ClinicalAssessmentModelMixin(models.Model):

    physical_symptoms = models.CharField(
        verbose_name="Physical symptoms", max_length=10, choices=YES_NO_ND, null=True
    )

    headache = models.CharField(
        verbose_name="Headache", max_length=10, choices=YES_NO_ND, null=True
    )

    visual_acuity_left_eye = models.DecimalField(
        verbose_name="Visual acuity Left Eye",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    visual_acuity_right_eye = models.DecimalField(
        verbose_name="Visual acuity Right Eye",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score",
        validators=[MaxValueValidator(15), MinValueValidator(3)],
        null=True,
        help_text="/15",
    )

    confusion = models.CharField(
        verbose_name="Confusion", max_length=10, choices=YES_NO_ND, null=True
    )

    recent_seizure_less_72 = models.CharField(
        verbose_name="Recent seizure (<72 hrs)",
        max_length=10,
        choices=YES_NO_ND,
        null=True,
    )

    cn_palsy = models.CharField(
        verbose_name="CN palsy", max_length=10, choices=YES_NO_ND, null=True
    )

    behaviour_change = models.CharField(
        verbose_name="Behaviour change", max_length=10, choices=YES_NO_ND, null=True
    )

    focal_neurology = models.CharField(
        verbose_name="Focal neurology", max_length=10, choices=YES_NO_ND, null=True
    )

    class Meta:
        abstract = True
