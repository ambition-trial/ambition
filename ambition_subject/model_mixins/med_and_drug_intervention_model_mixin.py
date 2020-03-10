from ambition_lists.models import Antibiotic, OtherDrug, Day14Medication
from django.db import models


class MedAndDrugInterventionModelMixin(models.Model):

    medicines = models.ManyToManyField(Day14Medication, verbose_name="Medicine day 14")

    medicine_other = models.TextField(
        verbose_name="If other, please specify", null=True, blank=True
    )

    drug_intervention = models.ManyToManyField(
        OtherDrug, verbose_name="Other drugs/interventions given during first 14 days"
    )

    drug_intervention_other = models.TextField(
        verbose_name="If other, please specify", blank=True, null=True
    )

    antibiotic = models.ManyToManyField(
        Antibiotic,
        blank=True,
        verbose_name="Were any of the following antibiotics given?",
    )

    antibiotic_other = models.TextField(
        verbose_name="If other antibiotics, please specify", null=True, blank=True
    )

    class Meta:
        abstract = True
