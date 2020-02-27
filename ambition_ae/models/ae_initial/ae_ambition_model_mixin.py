from django.db import models
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_constants.choices import YES_NO
from edc_constants.constants import UNKNOWN, QUESTION_RETIRED
from edc_model.validators import datetime_not_future


class AeAmbitionModelMixin(models.Model):

    # QUESTION_RETIRED
    ae_classification_old = models.CharField(max_length=150, default=QUESTION_RETIRED)

    # QUESTION_RETIRED
    sae_reason_old = models.CharField(
        verbose_name='If "Yes", reason for SAE:',
        max_length=50,
        # choices=SAE_REASONS,
        default=QUESTION_RETIRED,
        help_text="If subject deceased, submit a Death Report",
    )

    # removed issue #4
    ambisome_relation = models.CharField(
        verbose_name="Relationship to Ambisome:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
        editable=False,
    )

    fluconazole_relation = models.CharField(
        verbose_name="Relationship to Fluconozole:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    # removed issue #4
    amphotericin_b_relation = models.CharField(
        verbose_name="Relationship to Amphotericin B:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
        editable=False,
    )

    flucytosine_relation = models.CharField(
        verbose_name="Relationship to Flucytosine:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
    )

    # added issue #4
    amphotericin_relation = models.CharField(
        verbose_name="Amphotericin formulation:",
        max_length=25,
        choices=STUDY_DRUG_RELATIONSHIP,
        null=True,
    )

    details_last_study_drug = models.TextField(
        verbose_name="Details of the last implicated drug (name, dose, route):",
        max_length=1000,
        null=True,
        blank=True,
        editable=False,
    )

    med_administered_datetime = models.DateTimeField(
        verbose_name="Date and time of last implicated study medication administered",
        validators=[datetime_not_future],
        null=True,
        blank=True,
        editable=False,
    )

    ae_cm_recurrence = models.CharField(
        verbose_name="Was the AE a recurrence of CM symptoms?",
        max_length=10,
        choices=YES_NO,
        default=UNKNOWN,
        help_text='If "Yes", fill in the "Recurrence of Symptoms" form',
    )

    class Meta:
        abstract = True
