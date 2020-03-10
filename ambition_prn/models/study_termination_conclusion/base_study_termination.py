from django.db import models
from edc_action_item.managers import (
    ActionIdentifierSiteManager,
    ActionIdentifierManager,
)
from edc_model.validators.date import date_not_future


class BaseStudyTerminationConclusion(models.Model):

    last_study_fu_date = models.DateField(
        verbose_name="Date of last research follow up (if different):",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    death_date = models.DateField(
        verbose_name="Date of Death",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    consent_withdrawal_reason = models.CharField(
        verbose_name="Reason for withdrawing consent",
        max_length=75,
        blank=True,
        null=True,
    )

    on_site = ActionIdentifierSiteManager()

    objects = ActionIdentifierManager()

    def natural_key(self):
        return (self.action_identifier,)

    class Meta:
        abstract = True
