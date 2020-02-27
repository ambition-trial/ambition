from ambition_lists.models import Antibiotic, Symptom, SignificantNewDiagnosis
from ambition_lists.models import Neurological, Day14Medication
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import NOT_APPLICABLE, YES, NEG, NO
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, related, seq

from .models import BloodResult, Microbiology, FollowUp
from .models import Education, EducationHoh
from .models import LumbarPunctureCsf, Radiology
from .models import MedicalExpensesTwo
from .models import PatientHistory, Week16, Week4
from .models import PkPdCrf, SubjectReconsent
from .models import SubjectConsent, MedicalExpensesTwoDetail
from .models import SubjectRequisition
from .models import Week2, SubjectVisit, MedicalExpenses


fake = Faker()

antibiotic = Recipe(Antibiotic)

bloodresult = Recipe(BloodResult, action_identifier=None, tracking_identifier=None)

medicines = Recipe(Day14Medication)

neurological = Recipe(Neurological)

symptom = Recipe(Symptom)

significantnewdiagnosis = Recipe(
    SignificantNewDiagnosis, display_name=NOT_APPLICABLE, name=NOT_APPLICABLE
)


followup = Recipe(
    FollowUp,
    physical_symptoms=NO,
    headache=NO,
    glasgow_coma_score=8,
    confusion=NO,
    cn_palsy=NO,
    behaviour_change=NO,
    focal_neurology=NO,
    fluconazole_dose="800mg_daily",
    rifampicin_started=NO,
)

subjectvisit = Recipe(SubjectVisit, reason=SCHEDULED)

subjectrequisition = Recipe(SubjectRequisition)

microbiology = Recipe(
    Microbiology,
    urine_culture_performed=NO,
    blood_culture_performed=NO,
    sputum_results_culture=NEG,
    tissue_biopsy_taken=NO,
)

patienthistory = Recipe(
    PatientHistory,
    headache_duration=2,
    visual_loss_duration=1,
    tb_history=YES,
    symptom=related(symptom),
    neurological=related(neurological),
    tb_site="pulmonary",
    tb_treatment=YES,
    taking_rifampicin=NO,
    taking_arv=NO,
    patient_adherence=NO,
    last_dose=1,
    temp=38,
    heart_rate=88,
    respiratory_rate=22,
    weight=60,
    glasgow_coma_score=8,
    visual_acuity_day=date.today,
    left_acuity=0.52,
    right_acuity=0.53,
    lung_exam=YES,
    cryptococcal_lesions=NO,
    cd4_date=None,
    viral_load_date=None,
)


week2 = Recipe(
    Week2,
    discharged=NO,
    died=NO,
    flucy_start_date=date.today(),
    flucon_stop_date=date.today(),
    antibiotic=related(antibiotic),
    blood_received=NO,
    units=None,
    headache=YES,
    temperature=41.2,
    behaviour_change=YES,
    confusion=NO,
    cn_palsy=YES,
    focal_neurology=NO,
    medicines=related(medicines),
)


radiology = Recipe(
    Radiology,
    is_cxr_done=NO,
    cxr_date=None,
    cxr_type=NOT_APPLICABLE,
    infiltrate_location=NOT_APPLICABLE,
    cxr_description=None,
    is_ct_performed=YES,
    date_ct_performed=get_utcnow(),
    is_scanned_with_contrast=NO,
    brain_imaging_reason="reduction_in_gcs",
    brain_imaging_reason_other=None,
    are_results_abnormal=NOT_APPLICABLE,
    abnormal_results_reason=NOT_APPLICABLE,
    abnormal_results_reason_other=NOT_APPLICABLE,
    if_infarcts_location=None,
)

lumbarpuncturecsf = Recipe(
    LumbarPunctureCsf,
    csf_culture=NO,
    opening_pressure=15,
    csf_amount_removed=5,
    csf_wbc_cell_count=250,
    differential_lymphocyte_count=250,
    differential_neutrophil_count=250,
    csf_protein=10,
)

subjectconsent = Recipe(
    SubjectConsent,
    assessment_score=YES,
    confirm_identity=seq("12315678"),
    consent_copy=YES,
    consent_datetime=get_utcnow(),
    consent_reviewed=YES,
    consent_signature=YES,
    dob=get_utcnow() - relativedelta(years=25),
    first_name=fake.first_name,
    gender="M",
    identity=seq("12315678"),
    identity_type="country_id",
    initials="XX",
    is_dob_estimated="-",
    is_incarcerated=NO,
    is_literate=YES,
    last_name=fake.last_name,
    screening_identifier=None,
    study_questions=YES,
    site=Site.objects.get_current(),
    subject_identifier=None,
)

week16 = Recipe(Week16)

medicalexpenses = Recipe(MedicalExpenses)

medicalexpensestwo = Recipe(MedicalExpensesTwo)

medicalexpensestwodetail = Recipe(MedicalExpensesTwoDetail)

education = Recipe(Education)

educationhoh = Recipe(EducationHoh)

pkpdcrf = Recipe(PkPdCrf)

week4 = Recipe(Week4)

subjectreconsent = Recipe(
    SubjectReconsent,
    site=Site.objects.get_current(),
    consent_reviewed=YES,
    assessment_score=YES,
    study_questions=YES,
    consent_copy=YES,
    action_identifier=None,
    tracking_identifier=None,
)
