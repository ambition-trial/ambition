from ambition_lists.models import Day14Medication
from ambition_subject.model_mixins import BloodTransfusionModelMixin
from ambition_subject.model_mixins import MedAndDrugInterventionModelMixin
from ambition_subject.model_mixins import StudyMedicationModelMixin
from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA, NOT_APPLICABLE
from edc_identifier.model_mixins import (
    TrackingModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
)
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ...constants import STUDY_TERMINATION_CONCLUSION_ACTION
from ...choices import FIRST_ARV_REGIMEN, FIRST_LINE_REGIMEN, SECOND_ARV_REGIMEN
from ...choices import REASON_STUDY_TERMINATED, YES_NO_ALREADY
from .base_study_termination import BaseStudyTerminationConclusion


class StudyTerminationConclusion(
    NonUniqueSubjectIdentifierFieldMixin,
    BaseStudyTerminationConclusion,
    OffScheduleModelMixin,
    StudyMedicationModelMixin,
    MedAndDrugInterventionModelMixin,
    BloodTransfusionModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BaseUuidModel,
):

    action_name = STUDY_TERMINATION_CONCLUSION_ACTION

    tracking_identifier_prefix = "ST"

    subject_identifier = models.CharField(max_length=50, unique=True)

    discharged_after_initial_admission = models.CharField(
        verbose_name="Was the patient discharged after initial admission?",
        max_length=6,
        choices=YES_NO,
    )

    initial_discharge_date = models.DateField(
        verbose_name="Date of initial discharge",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    readmission_after_initial_discharge = models.CharField(
        verbose_name="Was the patient re-admitted following initial discharge?",
        max_length=7,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    readmission_date = models.DateField(
        verbose_name="Date of readmission",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    discharged_date = models.DateField(
        verbose_name="Date discharged",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    termination_reason = models.CharField(
        verbose_name="Reason for study termination",
        max_length=75,
        choices=REASON_STUDY_TERMINATED,
        help_text=("If included in error, be sure to fill in protocol deviation form."),
    )

    willing_to_complete_10w = models.CharField(
        verbose_name=(
            "Is the patient willing to complete the W10 " "and W16 FU visit only?"
        ),
        max_length=12,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    willing_to_complete_centre = models.CharField(
        verbose_name=(
            "Is the patient willing to complete the W10"
            "and W16 FU visit only at their new care centre?"
        ),
        max_length=17,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    willing_to_complete_date = models.DateField(
        verbose_name="Date the 10W FU due",
        validators=[date_not_future],
        editable=False,
        null=True,
        help_text="get value from Ambition visit schedule",
    )

    protocol_exclusion_criterion = models.CharField(
        verbose_name="Late protocol exclusion met?",
        max_length=12,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    included_in_error_date = models.DateField(
        verbose_name="If included in error, date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    included_in_error = models.TextField(
        verbose_name="If included in error, narrative:",
        max_length=300,
        blank=True,
        null=True,
    )

    rifampicin_started = models.CharField(
        verbose_name="Rifampicin started since week 4?",
        max_length=30,
        choices=YES_NO_ALREADY,
    )

    first_line_regimen = models.CharField(
        verbose_name=(
            "ART regimen started for naive patients (or regimen"
            " switched for those already on ARVs)"
        ),
        max_length=75,
        choices=FIRST_ARV_REGIMEN,
        default=NOT_APPLICABLE,
    )

    first_line_regimen_other = OtherCharField()

    second_line_regimen = models.CharField(
        verbose_name="Second line / second switch ARV regimen",
        max_length=50,
        choices=SECOND_ARV_REGIMEN,
        default=NOT_APPLICABLE,
    )

    second_line_regimen_other = OtherCharField()

    arvs_switch_date = models.DateField(
        verbose_name="ARV start/switch date",
        blank=True,
        null=True,
        validators=[date_not_future],
    )

    first_line_choice = models.CharField(
        verbose_name="If first line:",
        max_length=5,
        choices=FIRST_LINE_REGIMEN,
        default=NOT_APPLICABLE,
    )

    arvs_delay_reason = models.CharField(
        verbose_name="Reason ARVs not started", max_length=75, blank=True, null=True
    )

    medicines = models.ManyToManyField(
        Day14Medication, verbose_name="Medicines on study termination day:"
    )

    on_study_drug = models.CharField(
        verbose_name="Has the patient started 'study' drug",
        max_length=25,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    def save(self, *args, **kwargs):
        if not self.last_study_fu_date:
            self.last_study_fu_date = self.offschedule_datetime.date()
        super().save(*args, **kwargs)

    class Meta(OffScheduleModelMixin.Meta):
        verbose_name = "Study Termination/Conclusion"
        verbose_name_plural = "Study Terminations/Conclusions"
