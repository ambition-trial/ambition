from django.db import models
from edc_model.validators import date_not_future


class StudyMedicationModelMixin(models.Model):

    ampho_start_date = models.DateField(
        verbose_name="Amphotericin B start date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    ampho_stop_date = models.DateField(
        verbose_name="Amphotericin B end date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    ampho_duration = models.IntegerField(
        verbose_name="Amphotericin B treatment duration", null=True, blank=True
    )

    flucon_start_date = models.DateField(
        verbose_name="Fluconazole start date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    flucon_stop_date = models.DateField(
        verbose_name="Fluconazole end date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    flucon_duration = models.IntegerField(
        verbose_name="Fluconazole treatment duration", null=True, blank=True
    )

    flucy_start_date = models.DateField(
        verbose_name="Flucytosine start date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    flucy_stop_date = models.DateField(
        verbose_name="Flucytosine end date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    flucy_duration = models.IntegerField(
        verbose_name="Flucytosine treatment duration", null=True, blank=True
    )

    ambi_start_date = models.DateField(
        verbose_name="Ambisome start date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    ambi_stop_date = models.DateField(
        verbose_name="Ambisome end date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    ambi_duration = models.IntegerField(
        verbose_name="Ambisome treatment duration", null=True, blank=True
    )

    class Meta:
        abstract = True
