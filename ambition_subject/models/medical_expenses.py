from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, NOT_APPLICABLE
from edc_model.models import HistoricalRecords
from edc_model_fields.fields import OtherCharField
from edc_visit_tracking.managers import CrfModelManager

from ..choices import PATIENT_REL, ACTIVITIES_MISSED, CURRENCY, TRANSPORT
from ..managers import CurrentSiteManager
from ..validators import hm_validator
from .crf_model_mixin import CrfModelMixin


class MedicalExpenses(CrfModelMixin):

    info_source = models.CharField(
        verbose_name="What is the main source of this information?",
        max_length=25,
        choices=PATIENT_REL,
    )

    currency = models.CharField(
        verbose_name="Which currency do you use?", max_length=20, choices=CURRENCY
    )

    food_spend = models.DecimalField(
        verbose_name="How much do you/your family spend on food in a week?",
        decimal_places=2,
        max_digits=15,
        null=True,
        validators=[MinValueValidator(0)],
    )

    utilities_spend = models.DecimalField(
        verbose_name="How much do you/your family spent on rent and utilities a month?",
        decimal_places=2,
        max_digits=15,
        null=True,
        validators=[MinValueValidator(0)],
    )

    item_spend = models.DecimalField(
        verbose_name=(
            "How much have you spent on large items (e.g. furniture, electrical "
            "items, cars) in the last year?"
        ),
        decimal_places=2,
        max_digits=15,
        null=True,
        validators=[MinValueValidator(0)],
    )

    subject_spent_last_4wks = models.DecimalField(
        verbose_name=(
            "Over the last 4/10 weeks, how much have you "
            "spent on activities relating to your health?"
        ),
        decimal_places=2,
        max_digits=15,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=(
            "On D1 record data for the four weeks prior to recruitment. "
            "On W10 record data for the ten weeks since recruitment."
        ),
    )

    someone_spent_last_4wks = models.DecimalField(
        verbose_name=(
            "Over the last 4/10 weeks, how much has someone else "
            "spent on activities relating to your health?"
        ),
        decimal_places=2,
        max_digits=15,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=(
            "On D1 record data for the four weeks prior to recruitment. "
            "On W10 record data for the ten weeks since recruitment."
        ),
    )
    total_spent_last_4wks = models.DecimalField(
        verbose_name=(
            "How much in total has been spent on your healthcare in the last 4/10 weeks?"
        ),
        decimal_places=2,
        max_digits=16,
        null=True,
        validators=[MinValueValidator(0)],
        help_text=(
            "On D1 record data for the four weeks prior to recruitment. "
            "On W10 record data for the ten weeks since recruitment."
        ),
    )

    care_before_hospital = models.CharField(
        verbose_name=(
            "Have you received any treatment or care "
            "for your present condition, before coming to the hospital?"
        ),
        max_length=5,
        choices=YES_NO,
        help_text="If YES, please complete medical expenses part 2",
    )

    duration_present_condition = models.IntegerField(
        verbose_name="How long have you been sick with your current condition?",
        validators=[MinValueValidator(0)],
        null=True,
        help_text="in days",
    )

    activities_missed = models.CharField(
        verbose_name=(
            "What would you have been doing if you were not sick "
            "with your present condition"
        ),
        max_length=25,
        null=True,
        choices=ACTIVITIES_MISSED,
    )

    activities_missed_other = OtherCharField(max_length=25, blank=True, null=True)

    time_off_work = models.DecimalField(
        verbose_name="How much time did you take off work?",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="in days",
    )

    carer_time_off = models.IntegerField(
        verbose_name=(
            "How much time did a caring family member "
            "take to accompany you to the hospital?"
        ),
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="in days",
    )

    loss_of_earnings = models.CharField(
        verbose_name="Did you lose earnings as a result?",
        max_length=5,
        choices=YES_NO_NA,
    )

    earnings_lost_amount = models.DecimalField(
        verbose_name="How much did you lose?",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    form_of_transport = models.CharField(
        verbose_name="Which form of transport did you take to get here today?",
        max_length=25,
        default=NOT_APPLICABLE,
        choices=TRANSPORT,
    )

    transport_fare = models.DecimalField(
        verbose_name="How much did you spend on the transport (in total)?",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    travel_time = models.CharField(
        verbose_name="How long did it take you to reach there?",
        validators=[hm_validator],
        max_length=8,
        help_text="Specify as hours:minutes (format HH:MM)",
        null=True,
        blank=True,
    )

    loans = models.CharField(
        verbose_name="Did you take out any loans to pay for your healthcare?",
        max_length=5,
        choices=YES_NO,
    )

    sold_anything = models.CharField(
        verbose_name="Did you sell anything to pay for your healthcare?",
        max_length=5,
        choices=YES_NO,
    )

    private_healthcare = models.CharField(
        verbose_name="Do you have private healthcare insurance?",
        max_length=5,
        choices=YES_NO,
    )

    healthcare_insurance = models.CharField(
        verbose_name="Did you use it to help pay for your healthcare?",
        max_length=5,
        choices=YES_NO_NA,
    )

    welfare = models.CharField(
        verbose_name="Do you receive any welfare or social service support?",
        max_length=5,
        choices=YES_NO,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Health Economics: Medical Expenses"
        verbose_name_plural = "Health Economics: Medical Expenses"
