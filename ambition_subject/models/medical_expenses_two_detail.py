from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model.models import HistoricalRecords
from edc_model_fields.fields import OtherCharField

from ..choices import LOCATION_CARE, CARE_PROVIDER, TRANSPORT
from ..validators import hm_validator
from .medical_expenses_two import MedicalExpensesTwo


class ModelManager(models.Manager):
    def get_by_natural_key(
        self,
        location_care,
        subject_identifier,
        visit_schedule_name,
        schedule_name,
        visit_code,
    ):
        return self.get(
            location_care=location_care,
            medical_expenses_two__subject_visit__subject_identifier=subject_identifier,
            medical_expenses_two__subject_visit__visit_schedule_name=visit_schedule_name,
            medical_expenses_two__subject_visit__schedule_name=schedule_name,
            medical_expenses_two__subject_visit__visit_code=visit_code,
        )


class MedicalExpensesTwoDetail(BaseUuidModel):

    medical_expenses_two = models.ForeignKey(MedicalExpensesTwo, on_delete=PROTECT)

    location_care = models.CharField(
        verbose_name="Where did you receive treatment or care?",
        max_length=35,
        choices=LOCATION_CARE,
    )

    location_care_other = OtherCharField()

    transport_form = models.CharField(
        verbose_name="Which form of transport did you take to reach there?",
        max_length=20,
        choices=TRANSPORT,
        default=NOT_APPLICABLE,
    )

    transport_cost = models.DecimalField(
        verbose_name="How much did you spend on the transport (return)?",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    transport_duration = models.CharField(
        verbose_name="How long did it take you to reach there?",
        validators=[hm_validator],
        max_length=8,
        help_text="Specify as hours:minutes (format HH:MM)",
        null=True,
        blank=True,
    )

    care_provider = models.CharField(
        verbose_name="Who provided treatment or care during that visit?",
        max_length=35,
        choices=CARE_PROVIDER,
    )

    care_provider_other = OtherCharField(max_length=25, blank=True, null=True)

    paid_treatment = models.CharField(
        verbose_name=(
            "Did you pay for the consultation you received during that visit"
        ),
        max_length=15,
        choices=YES_NO,
    )

    paid_treatment_amount = models.DecimalField(
        verbose_name=("How much did you pay for this visit?"),
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    medication_bought = models.CharField(
        verbose_name="Did you buy other medication for relief?",
        max_length=15,
        choices=YES_NO,
    )

    medication_payment = models.DecimalField(
        verbose_name="How much did you pay?",
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )

    other_place_visited = models.CharField(
        verbose_name="Before this, did you go to another place "
        "for the treatment of the present situation?",
        max_length=15,
        choices=YES_NO,
        help_text='If YES, click "Add another Medical Expenses Part 2: Detail" below.',
    )

    objects = ModelManager()

    history = HistoricalRecords()

    def __str__(self):
        return self.medical_expenses_two.visit.subject_identifier

    def natural_key(self):
        return (self.location_care,) + self.medical_expenses_two.natural_key()

    natural_key.dependencies = ["ambition_subject.medicalexpensestwo"]

    class Meta:
        verbose_name = "Medical Expenses Part 2: Detail"
        verbose_name_plural = "Medical Expenses Part 2: Detail"
