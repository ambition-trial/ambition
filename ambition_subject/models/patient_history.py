from ambition_lists.models import Medication, Symptom, Neurological, ArvRegimens
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE, QUESTION_RETIRED
from edc_constants.utils import append_question_retired_choice
from edc_model.models import HistoricalRecords
from edc_model.validators import date_not_future
from edc_model_fields.fields import OtherCharField, IsDateEstimatedFieldNa
from edc_visit_tracking.managers import CrfModelManager

from ..choices import FIRST_LINE_REGIMEN, FIRST_ARV_REGIMEN, TB_SITE, ARV_DECISION
from ..choices import ECOG_SCORE, SECOND_ARV_REGIMEN, WEIGHT_DETERMINATION
from ..managers import CurrentSiteManager
from .crf_model_mixin import CrfModelMixin


FIRST_ARV_REGIMEN_RETIRED = append_question_retired_choice(FIRST_ARV_REGIMEN)
SECOND_ARV_REGIMEN_RETIRED = append_question_retired_choice(SECOND_ARV_REGIMEN)
FIRST_LINE_REGIMEN_RETIRED = append_question_retired_choice(FIRST_LINE_REGIMEN)
YES_NO_NA_RETIRED = append_question_retired_choice(YES_NO_NA)


class PatientHistory(CrfModelMixin):

    symptom = models.ManyToManyField(
        Symptom,
        blank=True,
        related_name="symptoms",
        verbose_name="What are your current symptoms?",
    )

    headache_duration = models.IntegerField(
        verbose_name="If headache, how many days did it last?",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    visual_loss_duration = models.IntegerField(
        verbose_name="If visual loss, how many days did it last?",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    tb_history = models.CharField(
        verbose_name="Previous medical history of Tuberculosis?",
        max_length=5,
        choices=YES_NO,
    )

    tb_site = models.CharField(
        verbose_name="If YES, site of TB?",
        max_length=15,
        choices=TB_SITE,
        default=NOT_APPLICABLE,
    )

    tb_treatment = models.CharField(
        verbose_name="Are you currently taking TB treatment?",
        max_length=5,
        choices=YES_NO,
    )

    taking_rifampicin = models.CharField(
        verbose_name="If YES, are you currently also taking Rifampicin?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rifampicin_started_date = models.DateField(
        verbose_name="If YES, when did you first start taking Rifampicin?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    new_hiv_diagnosis = models.CharField(
        verbose_name="Is this a new HIV diagnosis?", max_length=5, choices=YES_NO
    )

    taking_arv = models.CharField(
        verbose_name="If NO, has the patient ever been on ART?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    # retired
    first_arv_regimen = models.CharField(
        verbose_name="If YES, which drugs were prescribed for their first ART regimen?",
        max_length=50,
        choices=FIRST_ARV_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    first_arv_regimen_other = OtherCharField(editable=False)

    # retired
    first_line_choice = models.CharField(
        verbose_name="If first line:",
        max_length=25,
        choices=FIRST_LINE_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    initial_arv_date = models.DateField(
        verbose_name=mark_safe(
            "If YES, when did the patient <u>start</u> ART for the first time."
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    initial_arv_date_estimated = IsDateEstimatedFieldNa(
        verbose_name="If YES, is this ART date estimated?", default=NOT_APPLICABLE
    )

    initial_arv_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name=mark_safe(
            "If YES, which drugs were prescribed for their first ART regimen?"
        ),
        related_name="initial_arv",
    )

    initial_arv_regimen_other = OtherCharField()

    has_switched_regimen = models.CharField(
        verbose_name="Has the patient ever switched ART regimen?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    current_arv_date = models.DateField(
        verbose_name=mark_safe(
            "If YES, when was their <u>current or most recent</u> "
            "ART regimen started?"
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    current_arv_date_estimated = IsDateEstimatedFieldNa(
        verbose_name="If YES, is this ART date estimated?", default=NOT_APPLICABLE
    )

    current_arv_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name=mark_safe(
            "If YES, what is their current or most recent ART regimen?"
        ),
        related_name="current_arv",
    )

    current_arv_regimen_other = OtherCharField()

    current_arv_is_defaulted = models.CharField(
        verbose_name=mark_safe(
            "Has the patient <u>now</u> defaulted from their ART regimen?"
        ),
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="'DEFAULTED' means no ART for at least one month.",
    )

    current_arv_defaulted_date = models.DateField(
        verbose_name=mark_safe(
            "If the patient has DEFAULTED, on what date did they default "
            "from their <u>most recent</u> ART regimen?"
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    current_arv_defaulted_date_estimated = IsDateEstimatedFieldNa(
        verbose_name="If DEFAULTED, is this date estimated?", default=NOT_APPLICABLE
    )

    current_arv_is_adherent = models.CharField(
        verbose_name=mark_safe(
            "If the patient is currently on ART, are they ADHERENT to "
            "their <u>current</u> ART regimen?"
        ),
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    current_arv_tablets_missed = models.IntegerField(
        verbose_name=("If not ADHERENT, how many doses missed in the last month?"),
        validators=[MinValueValidator(0), MaxValueValidator(31)],
        null=True,
        blank=True,
    )

    current_arv_decision = models.CharField(
        verbose_name=mark_safe(
            "What decision was made at admission regarding their "
            "<u>current</u> ART regimen?"
        ),
        max_length=25,
        choices=ARV_DECISION,
        default=NOT_APPLICABLE,
    )

    # retired
    second_arv_regimen = models.CharField(
        verbose_name="Second line ARV regimen",
        max_length=50,
        choices=SECOND_ARV_REGIMEN_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    second_arv_regimen_other = OtherCharField(editable=False)

    # retired
    patient_adherence = models.CharField(
        verbose_name="Is the patient reportedly adherent?",
        max_length=25,
        choices=YES_NO_NA_RETIRED,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # retired
    last_dose = models.IntegerField(
        verbose_name=(
            "If no tablets taken this month, how many months "
            "since the last dose taken?"
        ),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        editable=False,
    )

    last_viral_load = models.DecimalField(
        verbose_name="Last Viral Load, if known?",
        decimal_places=3,
        max_digits=10,
        null=True,
        blank=True,
        help_text="copies/mL",
    )

    viral_load_date = models.DateField(
        verbose_name="Viral Load date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    vl_date_estimated = IsDateEstimatedFieldNa(
        verbose_name=("Is the subject's Viral Load date estimated?"),
        default=NOT_APPLICABLE,
    )

    last_cd4 = models.IntegerField(
        verbose_name="Last CD4, if known?",
        validators=[MinValueValidator(1), MaxValueValidator(2500)],
        null=True,
        blank=True,
        help_text=mark_safe("acceptable units are mm<sup>3</sup>"),
    )

    cd4_date = models.DateField(
        verbose_name="CD4 date", validators=[date_not_future], null=True, blank=True
    )

    cd4_date_estimated = IsDateEstimatedFieldNa(
        verbose_name=("Is the subject's CD4 date estimated?"), default=NOT_APPLICABLE
    )

    temp = models.DecimalField(
        verbose_name="Temperature:",
        validators=[MinValueValidator(30), MaxValueValidator(45)],
        decimal_places=1,
        max_digits=3,
        help_text="in degrees Celcius",
    )

    heart_rate = models.IntegerField(
        verbose_name="Heart rate:",
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="bpm",
    )

    sys_blood_pressure = models.IntegerField(
        verbose_name="Blood pressure: systolic",
        validators=[MinValueValidator(50), MaxValueValidator(220)],
        help_text="in mm. format SYS, e.g. 120",
    )

    dia_blood_pressure = models.IntegerField(
        verbose_name="Blood pressure: diastolic",
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        help_text="in Hg. format DIA, e.g. 80",
    )

    respiratory_rate = models.IntegerField(
        verbose_name="Respiratory rate:",
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        help_text="breaths/min",
    )

    weight = models.DecimalField(
        verbose_name="Weight:",
        validators=[MinValueValidator(20), MaxValueValidator(150)],
        decimal_places=1,
        max_digits=4,
        help_text="kg",
    )

    weight_determination = models.CharField(
        verbose_name="Is weight estimated or measured?",
        max_length=15,
        choices=WEIGHT_DETERMINATION,
    )

    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score:",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    neurological = models.ManyToManyField(Neurological, blank=True)

    neurological_other = OtherCharField(
        verbose_name='If "Other CN palsy", specify',
        max_length=250,
        blank=True,
        null=True,
    )

    focal_neurologic_deficit = models.TextField(
        verbose_name='If "Focal neurologic deficit" chosen, please specify details:',
        null=True,
        blank=True,
    )

    visual_acuity_day = models.DateField(
        verbose_name="Study day visual acuity recorded?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    left_acuity = models.DecimalField(
        verbose_name="Visual acuity left eye:",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    right_acuity = models.DecimalField(
        verbose_name="Visual acuity right eye",
        decimal_places=3,
        max_digits=4,
        null=True,
        blank=True,
    )

    ecog_score = models.CharField(
        verbose_name="ECOG Disability Score", max_length=15, choices=ECOG_SCORE
    )

    ecog_score_value = models.CharField(
        verbose_name="ECOG Score", max_length=15, choices=ECOG_SCORE
    )

    lung_exam = models.CharField(
        verbose_name="Abnormal lung exam:", max_length=5, choices=YES_NO
    )

    cryptococcal_lesions = models.CharField(
        verbose_name="Cryptococcal related skin lesions:", max_length=5, choices=YES_NO
    )

    specify_medications = models.ManyToManyField(Medication, blank=True)

    specify_medications_other = models.TextField(max_length=150, blank=True, null=True)

    previous_oi = models.CharField(
        verbose_name="Previous opportunistic infection other than TB?",
        max_length=5,
        choices=YES_NO,
    )

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Patient's History"
        verbose_name_plural = "Patient's History"
