from django.db import models
from django.db.models.deletion import PROTECT
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_model.models import BaseUuidModel
from edc_offstudy.model_mixins import OffstudyCrfModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.model_mixins import (
    VisitTrackingCrfModelMixin,
    PreviousVisitModelMixin,
)

from .subject_visit import SubjectVisit


class CrfModelMixin(
    VisitTrackingCrfModelMixin,
    RequiresConsentFieldsModelMixin,
    PreviousVisitModelMixin,
    UpdatesCrfMetadataModelMixin,
    OffstudyCrfModelMixin,
    SiteModelMixin,
    ReferenceModelMixin,
    BaseUuidModel,
):

    """ Base model for all scheduled models
    """

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    def natural_key(self):
        return self.visit.natural_key()

    natural_key.dependencies = [
        "ambition_subject.subjectvisit",
        "sites.Site",
        "edc_appointment.appointment",
    ]

    @property
    def subject_identifier(self):
        return self.visit.subject_identifier

    class Meta:
        abstract = True
        indexes = [models.Index(fields=["subject_visit", "site", "id"])]
