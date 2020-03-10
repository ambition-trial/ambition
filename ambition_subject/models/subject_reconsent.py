from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django_crypto_fields.fields.identity_field import IdentityField
from edc_action_item.models import ActionModelMixin
from edc_consent.field_mixins import ReviewFieldsMixin
from edc_constants.constants import ABNORMAL
from edc_identifier.managers import SubjectIdentifierManager
from edc_identifier.model_mixins import TrackingModelMixin
from edc_identifier.model_mixins import UniqueSubjectIdentifierModelMixin
from edc_model.models import BaseUuidModel
from edc_registration.models import RegisteredSubject
from edc_sites.models import SiteModelMixin
from edc_utils import get_utcnow

from ..action_items import RECONSENT_ACTION
from ..managers import CurrentSiteManager
from ..model_mixins import SearchSlugModelMixin


class SubjectReconsent(
    UniqueSubjectIdentifierModelMixin,
    SiteModelMixin,
    ReviewFieldsMixin,
    SearchSlugModelMixin,
    ActionModelMixin,
    TrackingModelMixin,
    BaseUuidModel,
):

    """ A model completed by the user that updates the consent
    for those originally consented by next of kin.
    """

    subject_screening_model = "ambition_screening.subjectscreening"

    subject_consent_model = "ambition_subject.subjectconsent"

    tracking_identifier_prefix = "SR"

    action_name = RECONSENT_ACTION

    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, editable=False)

    report_datetime = models.DateTimeField(default=get_utcnow)

    identity = IdentityField(
        verbose_name="Identity number",
        help_text=(
            "Provide the same identity number provided on the original "
            "consent complete by the next of kin."
        ),
    )

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    def __str__(self):
        return self.subject_identifier

    def save(self, *args, **kwargs):
        subject_screening = self.get_subject_screening()
        if subject_screening.mental_status != ABNORMAL:
            raise ValidationError("Reconsent is not required.")
        try:
            self.get_subject_consent(
                screening_identifier=subject_screening.screening_identifier
            )
        except ObjectDoesNotExist:
            raise ValidationError("Previous consent does not exist.")
        super().save(*args, **kwargs)

    def natural_key(self):
        return (self.subject_identifier, self.version)

    def get_subject_consent(self, screening_identifier=None):
        """Returns the first subject consent model instance.
        """
        if not screening_identifier:
            screening_identifier = self.get_subject_screening().screening_identifier
        model_cls = django_apps.get_model(self.subject_consent_model)
        return model_cls.objects.get(
            screening_identifier=screening_identifier,
            subject_identifier=self.subject_identifier,
            identity=self.identity,
        )

    def get_subject_screening(self):
        """Returns the subject screening model instance.
        """
        rs = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
        model_cls = django_apps.get_model(self.subject_screening_model)
        return model_cls.objects.get(screening_identifier=rs.screening_identifier)

    @property
    def registration_unique_field(self):
        """Required for UpdatesOrCreatesRegistrationModelMixin.
        """
        return "subject_identifier"

    class Meta:
        verbose_name = "Subject re-consent"
