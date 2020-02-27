from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO


class EducationModelMixin(models.Model):

    profession = models.CharField(
        verbose_name=("What is your profession?"), max_length=25
    )

    education_years = models.IntegerField(
        verbose_name="How many years of education did you complete?",
        validators=[MinValueValidator(0)],
    )

    education_certificate = models.CharField(
        verbose_name="What is the your highest education certificate?", max_length=25
    )

    elementary = models.CharField(
        verbose_name=("Did you go to elementary/primary school?"),
        max_length=5,
        choices=YES_NO,
    )

    elementary_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )

    secondary = models.CharField(
        verbose_name="Did you go to secondary school?", max_length=5, choices=YES_NO
    )

    secondary_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )

    higher_education = models.CharField(
        verbose_name="Did you go to higher education?", max_length=5, choices=YES_NO
    )

    higher_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
