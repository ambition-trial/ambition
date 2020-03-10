from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_action_item.managers import (
    ActionIdentifierSiteManager,
    ActionIdentifierManager,
)
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA, NOT_APPLICABLE
from edc_identifier.model_mixins import (
    TrackingModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
)
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from ..constants import RECURRENCE_OF_SYMPTOMS_ACTION
from ..choices import DR_OPINION, STEROIDS_CHOICES, YES_NO_ALREADY_ARV
from .list_models import Neurological, MeningitisSymptom, AntibioticTreatment


class RecurrenceSymptom(
    NonUniqueSubjectIdentifierFieldMixin,
    ActionModelMixin,
    TrackingModelMixin,
    SiteModelMixin,
    BaseUuidModel,
):

    tracking_identifier_prefix = "RS"

    action_name = RECURRENCE_OF_SYMPTOMS_ACTION

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time", default=get_utcnow
    )

    meningitis_symptom = models.ManyToManyField(
        MeningitisSymptom, verbose_name="What are your current symptoms?"
    )

    meningitis_symptom_other = models.CharField(
        verbose_name="If other symptom, please specify",
        max_length=50,
        null=True,
        blank=True,
    )

    patient_readmitted = models.CharField(
        verbose_name=(
            "Has the patient been re-admitted due to these recurrent symptoms?"
        ),
        max_length=5,
        choices=YES_NO,
    )

    glasgow_coma_score = models.IntegerField(
        verbose_name="Score:",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    recent_seizure = models.CharField(
        verbose_name=("Recent seizure (<72 hrs):"), max_length=5, choices=YES_NO
    )

    behaviour_change = models.CharField(max_length=5, choices=YES_NO)

    confusion = models.CharField(max_length=5, choices=YES_NO)

    neurological = models.ManyToManyField(Neurological, verbose_name="neurologic:")

    focal_neurologic_deficit = models.CharField(
        verbose_name='If "Focal neurologic deficit" chosen, please specify',
        max_length=15,
        null=True,
        blank=True,
    )

    cn_palsy_chosen_other = models.CharField(
        verbose_name="If other CN Palsy", max_length=15, null=True, blank=True
    )

    lp_completed = models.CharField(
        verbose_name="LP completed",
        max_length=5,
        choices=YES_NO,
        help_text="If YES, complete LP form",
    )

    amb_administered = models.CharField(max_length=5, choices=YES_NO)

    amb_duration = models.IntegerField(
        verbose_name="If YES, specify length of course",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    tb_treatment = models.CharField(
        verbose_name="TB treatment:", max_length=5, choices=YES_NO
    )

    steroids_administered = models.CharField(max_length=5, choices=YES_NO)

    steroids_duration = models.IntegerField(
        verbose_name="If YES, specify the length of course in days:",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    steroids_choices = models.CharField(
        verbose_name="If YES",
        max_length=25,
        default=NOT_APPLICABLE,
        choices=STEROIDS_CHOICES,
    )

    steroids_choices_other = models.CharField(
        blank=True, max_length=50, verbose_name="If other steroids, please specify"
    )

    CD4_count = models.IntegerField(
        verbose_name="CD4 count (if available)",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    antibiotic_treatment = models.ManyToManyField(
        AntibioticTreatment, verbose_name="Antibiotics treatment"
    )

    antibiotic_treatment_other = models.CharField(
        verbose_name="If other antibiotic treatment, please specify",
        max_length=50,
        blank=True,
        null=True,
    )

    on_arvs = models.CharField(
        verbose_name="On ARVs:", max_length=26, choices=YES_NO_ALREADY_ARV
    )

    arv_date = models.DateField(
        verbose_name="Study date ARVs started.",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    arvs_stopped = models.CharField(
        verbose_name="ARVs stopped this clinical episode?",
        max_length=5,
        choices=YES_NO_NA,
    )

    narrative_summary = models.TextField(
        verbose_name="Narrative summary of recurrence of symptoms:",
        help_text=(
            "Please ensure the following forms have been completed: "
            "LP, Bloods, Microbiology, Radiology"
        ),
    )

    dr_opinion = models.CharField(
        verbose_name="Study doctor's opinion:", max_length=10, choices=DR_OPINION
    )

    dr_opinion_other = models.CharField(
        verbose_name="If other doctor's opinion, please specify",
        blank=True,
        max_length=50,
        null=True,
    )

    on_site = ActionIdentifierSiteManager()

    objects = ActionIdentifierManager()

    def __str__(self):
        return f"{self.action_identifier[-9:]}"

    def natural_key(self):
        return (self.action_identifier,)

    class Meta:
        verbose_name = "Recurrence of Symptoms"
        verbose_name_plural = "Recurrence of Symptoms"
        indexes = [
            models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"]
            )
        ]
