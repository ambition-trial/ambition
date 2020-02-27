from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, NORMAL_ABNORMAL, PREG_YES_NO_NA
from edc_model.models import BaseUuidModel
from edc_reportable import IU_LITER, TEN_X_9_PER_LITER
from edc_screening.model_mixins import ScreeningModelMixin, EligibilityModelMixin

from ..subject_screening_eligibility import SubjectScreeningEligibility


class SubjectScreeningDeleteError(Exception):
    pass


class SubjectScreening(ScreeningModelMixin, EligibilityModelMixin, BaseUuidModel):

    eligibility_cls = SubjectScreeningEligibility

    meningitis_dx = models.CharField(
        verbose_name="First episode cryptococcal meningitis diagnosed by "
        "either: CSF India Ink or CSF cryptococcal antigen "
        "(CRAG)",
        choices=YES_NO,
        max_length=5,
    )

    will_hiv_test = models.CharField(
        verbose_name="Known HIV positive/willing to consent to an HIV test.",
        max_length=5,
        choices=YES_NO,
    )

    mental_status = models.CharField(
        verbose_name="Mental status", max_length=10, choices=NORMAL_ABNORMAL
    )

    pregnancy = models.CharField(
        verbose_name="Is the patient pregnant?", max_length=15, choices=PREG_YES_NO_NA
    )

    preg_test_date = models.DateTimeField(
        verbose_name="Pregnancy test (Urine or serum βhCG) date", blank=True, null=True
    )

    breast_feeding = models.CharField(
        verbose_name="Is the patient breasfeeding?", max_length=15, choices=YES_NO_NA
    )

    previous_drug_reaction = models.CharField(
        verbose_name=(
            "Previous Adverse Drug Reaction (ADR) to study drug "
            "(e.g. rash, drug induced blood abnormality)"
        ),
        max_length=5,
        choices=YES_NO,
    )

    contraindicated_meds = models.CharField(
        verbose_name=(
            "Taking concomitant medication that is contra-indicated "
            "with any study drug"
        ),
        max_length=5,
        choices=YES_NO,
        help_text="Contraindicated Meds: Cisapride, Pimozide,"
        "Terfenadine, Quinidine, Astemizole, Erythromycin",
    )

    received_amphotericin = models.CharField(
        verbose_name=(
            "Has received >48 hours of Amphotericin B "
            "(>=0.7mg/kg/day) prior to screening."
        ),
        max_length=5,
        choices=YES_NO,
    )

    received_fluconazole = models.CharField(
        verbose_name=(
            "Has received >48 hours of fluconazole treatment (>= "
            "800mg/day) prior to screening."
        ),
        max_length=5,
        choices=YES_NO,
    )

    alt = models.IntegerField(
        verbose_name="ALT result",
        null=True,
        blank=True,
        help_text=(
            "Leave blank if unknown. Units: 'IU/mL'. " f"Ineligible if > 200 {IU_LITER}"
        ),
    )

    neutrophil = models.DecimalField(
        verbose_name="Neutrophil result",
        decimal_places=2,
        max_digits=4,
        null=True,
        blank=True,
        help_text=(
            f"Leave blank if unknown. Units: '{TEN_X_9_PER_LITER}'. "
            f"Ineligible if < 0.5  {TEN_X_9_PER_LITER}"
        ),
    )

    platelets = models.IntegerField(
        verbose_name="Platelets result",
        null=True,
        blank=True,
        help_text=(
            f"Leave blank if unknown. Units: '{TEN_X_9_PER_LITER}'. "
            f"Ineligible if < 50 {TEN_X_9_PER_LITER}"
        ),
    )
