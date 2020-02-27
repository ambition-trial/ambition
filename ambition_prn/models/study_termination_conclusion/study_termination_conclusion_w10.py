from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import (
    TrackingModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
)
from edc_model.models import BaseUuidModel
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ...constants import STUDY_TERMINATION_CONCLUSION_ACTION_W10
from ...choices import REASON_STUDY_TERMINATED_W10
from .base_study_termination import BaseStudyTerminationConclusion


class StudyTerminationConclusionW10(
    NonUniqueSubjectIdentifierFieldMixin,
    BaseStudyTerminationConclusion,
    OffScheduleModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BaseUuidModel,
):

    action_name = STUDY_TERMINATION_CONCLUSION_ACTION_W10

    tracking_identifier_prefix = "ST"

    subject_identifier = models.CharField(max_length=50, unique=True)

    termination_reason = models.CharField(
        verbose_name="Reason for study termination",
        max_length=75,
        choices=REASON_STUDY_TERMINATED_W10,
        help_text=("If included in error, be sure to fill in protocol deviation form."),
    )

    class Meta(OffScheduleModelMixin.Meta):
        verbose_name = "W10 Study Termination/Conclusion"
        verbose_name_plural = "W10 Study Terminations/Conclusions"
