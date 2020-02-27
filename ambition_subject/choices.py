from ambition_prn import FIRST_LINE_REGIMEN, FIRST_ARV_REGIMEN, SECOND_ARV_REGIMEN
from ambition_form_validators import WORKING, NO_GROWTH, KLEBSIELLA_SPP
from ambition_form_validators import CRYPTOCOCCUS_NEOFORMANS, BACTERIA
from edc_constants.constants import NEG, OTHER, POS, NOT_APPLICABLE, NOT_DONE
from edc_constants.constants import NORMAL, IND, YES, NO
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MICROMOLES_PER_LITER,
)
from edc_reportable import (
    ALREADY_REPORTED,
    GRADE3,
    GRADE4,
    MICROMOLES_PER_LITER_DISPLAY,
    MM3,
    MM3_DISPLAY,
    PRESENT_AT_BASELINE,
)
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, MISSED_VISIT

from .constants import FOOT, BICYCLE
from .constants import AZT_3TC_with_ATZ_r_or_Lopinavir_r
from .constants import AZT_3TC_with_EFV_NVP_or_DTG
from .constants import ROUTINE_APPT, THERAPEUTIC_PL
from .constants import ECOLI, TDF_3TC_FTC_with_EFV_or_NVP
from .constants import TDF_3TC_FTC_with_ATZ_r_or_Lopinavir_r
from .constants import RESULTS_UNKNOWN, AWAITING_RESULTS, PATIENT
from .constants import AMBISOME, AMPHOTERICIN, ART_CONTINUED, ART_STOPPED


ABNORMAL_RESULTS_REASON = (
    (NOT_APPLICABLE, "Not applicable"),
    ("cerebral_oedema", "Cerebral oedema"),
    ("hydrocephalus", "Hydrocephalus"),
    ("cryptococcomus", "Cryptococcomus"),
    ("dilated_virchow_robin_spaces", "Dilated Virchow-Robin spaces"),
    ("enhancing_mass_lesions", "Enhancing mass lesions DD Toxoplasmosis, TB, Lymphoma"),
    ("infarcts", "Infarcts"),
    (OTHER, "Other"),
)

ACTIVITIES_MISSED = (
    (WORKING, "Working"),
    ("studying", "Studying"),
    ("caring_for_children", "Caring for children"),
    ("maintaining_house", "Maintaining the house"),
    ("nothing", "Nothing"),
    (OTHER, "Other"),
)

AMPHOTERICIN_FORMULATION = (
    (AMBISOME, "AmBisome"),
    (AMPHOTERICIN, "Amphotericin B Deoxycholate"),
)

ANTIBIOTICS = (
    ("amoxicillin", "Amoxicillin"),
    ("doxycycline", "Doxycycline"),
    ("flucloxacillin", "Flucloxacillin"),
    ("ceftriaxone", "Ceftriaxone"),
    (
        "erythromycin",
        "Erythromycin (contra-indicated with concomitant high dose Fluconazole)",
    ),
    ("ciprofloxacin", "Ciprofloxacin (avoid with concomitant high dose Fluconazole)"),
    (OTHER, "Other"),
)

APPOINTMENT_REASON = ((ROUTINE_APPT, "Routine"), (UNSCHEDULED, "Unscheduled"))
ARV_REGIMEN = (
    (NOT_APPLICABLE, "Not applicable"),
    (TDF_3TC_FTC_with_EFV_or_NVP, "TDF + 3TC/FTC + either EFV or NVP or DTG"),
    (AZT_3TC_with_EFV_NVP_or_DTG, "AZT + 3TC + either EFV or NVP or DTG"),
    (
        TDF_3TC_FTC_with_ATZ_r_or_Lopinavir_r,
        "TDF + 3TC/FTC + either ATZ/r or Lopinavir/r",
    ),
    (AZT_3TC_with_ATZ_r_or_Lopinavir_r, "AZT + 3TC + either ATZ/r or Lopinavir/r"),
    (OTHER, "Other"),
)

ARV_DECISION = (
    (NOT_APPLICABLE, "Not applicable"),
    (ART_CONTINUED, "ART continued"),
    (ART_STOPPED, "ART stopped"),
)

BLOOD_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    (BACTERIA, "Bacteria"),
    ("bacteria_and_cryptococcus", "Bacteria and Cryptococcus"),
    (OTHER, "Other"),
)

BIOPSY_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (CRYPTOCOCCUS_NEOFORMANS, "Cryptococcus neoformans"),
    ("mycobacterium_tuberculosis", "Mycobacterium Tuberculosis"),
    (OTHER, "Other"),
)

BACTERIA_TYPE = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    ("streptococcus_pneumoniae", "Streptococcus pneumoniae"),
    ("staphylococus_aureus", "(Sensitive) Staphylococus aureus"),
    ("mrsa", "MRSA"),
    (OTHER, "Other"),
)

BRAIN_IMAGINING_REASON = (
    (NOT_APPLICABLE, "Not applicable"),
    ("reduction_in_gcs", "Reduction in GCS"),
    ("new_neurology", "New neurology"),
    (OTHER, "Other"),
)

CARE_PROVIDER = (
    ("doctor", "Doctor"),
    ("clinical_officer", "Clinical Officer"),
    ("nurse", "Nurse"),
    ("traditional_healer", "Traditional Healer"),
    ("spiritual_healer", "Spiritual Healer"),
    ("family/friend", "Family/Friend"),
    ("pharmacist", "Pharmacist"),
    (OTHER, "Other"),
)

CN_PALSY = (("3", "III"), ("6", "VI"), ("7", "VII"), ("8", "VIII"))

CLINICAL_ASSESSMENT = ((NOT_APPLICABLE, "Not applicable"),)

CULTURE_RESULTS = (
    (NOT_APPLICABLE, "Not applicable"),
    (NO_GROWTH, "No growth"),
    (POS, "Positive"),
)

CURRENCY = (
    ("botswana_pula", "Botswana Pula"),
    ("malawian_kwacha", "Malawian Kwacha"),
    ("south_african_rand", "South African Rand"),
    ("ugandan_shilling", "Ugandan Shilling"),
    ("us_dollar", "US Dollar"),
    ("zimbabwean_dollar", "Zimbabwean Dollar"),
)

CXR_TYPE = (
    (NOT_APPLICABLE, "Not applicable"),
    (NORMAL, "Normal"),
    ("hilar_adenopathy", "Hilar adenopathy"),
    ("miliary_appearance", "Miliary appearance"),
    ("pleural_effusion", "Pleural effusion"),
    ("infiltrates", "Infiltrates"),
)

ECOG_SCORE = (
    (
        "0",
        "Fully active, able to carry on all pre-disease performance without restriction",
    ),
    (
        "1",
        "Restricted in physically strenuous activity but "
        "ambulatory and able to carry out work of a light or sedentary nature, e.g., "
        "light house work, office work",
    ),
    (
        "2",
        "Ambulatory and capable of all self-care but unable to carry out "
        "any work activities; up and about more than 50% of waking hours ",
    ),
    (
        "3",
        "Capable of only limited self-care; confined to bed or chair more than "
        "50% of waking hours",
    ),
    (
        "4",
        "Completely disabled; cannot carry on any self-care; totally confined to bed or chair",
    ),
    ("5", "Deceased"),
)

FLUCONAZOLE_DOSE = (
    ("800mg_daily", "800mg daily"),
    (OTHER, "Other"),
    (NOT_DONE, "Not done"),
)

FLUCYTOSINE_DOSE_MISSED = (
    ("dose_1", "Dose 1"),
    ("dose_2", "Dose 2"),
    ("dose_3", "Dose 3"),
    ("dose_4", "Dose 4"),
)

GLASGOW_COMA_SCORE_EYES = (
    ("does_not_open_eyes", "Does not open eyes"),
    ("opens_eyes_to_pain_only", "Opens eyes to pain only"),
    ("opens_eyes_to_voice", "Opens eyes to voice"),
    ("opens_eyes_spontaneously", "Opens eyes spontaneously"),
    (NOT_APPLICABLE, "Not applicable"),
)

GLASGOW_COMA_SCORE_VERBAL = (
    ("makes_no_sounds", "Makes no sounds"),
    ("makes_sounds", "Makes sounds"),
    ("makes_words", "Makes words"),
    ("disoriented", "Disoriented"),
    ("oriented", "Oriented"),
    (NOT_APPLICABLE, "Not applicable"),
)

GLASGOW_COMA_SCORE_MOTOR = (
    ("makes_no_movement", "Makes no movement"),
    ("extension_to_pain", "Extension to pain"),
    ("flexion_to_pain", "Flexion to pain"),
    ("withdraws_from_pain", "Withdraws from pain"),
    ("localizes_pain", "Localizes pain"),
    ("obey_commands", "Obey commands"),
)

INFECTION = (
    ("kaposi_sarcoma", "Kaposi Sarcoma"),
    ("herpes_zoster_virus", "Herpes-Zoster virus"),
    ("oesophageal_candidiasis", "Oesophageal Candidiasis"),
    ("PCP", "PCP"),
    ("cytomegalovirus", "Cytomegalovirus"),
    (OTHER, "Other"),
)


INFILTRATE_LOCATION = (
    (NOT_APPLICABLE, "Not applicable"),
    ("lul", "LUL"),
    ("lll", "LLL"),
    ("rul", "RUL"),
    ("rll", "RLL"),
    ("rml", "RML"),
    ("diffuse", "Diffuse"),
)

INFO_SOURCE = (
    ("hospital_notes", "Hospital notes"),
    ("outpatient_cards", "Outpatient cards"),
    (PATIENT, "Patient"),
    ("collateral_history", "Collateral History from relative/guardian"),
    (OTHER, "Other"),
)


LP_REASON = (
    ("scheduled_per_protocol", "Scheduled per protocol"),
    (THERAPEUTIC_PL, "Therapeutic LP"),
    ("clincal_deterioration", "Clinical deterioration"),
)

LOCATION_CARE = (
    ("government_healthcare", "Government healthcare"),
    ("private_healthcare", "Private healthcare"),
    ("ngo_healthcare", "NGO healthcare"),
    ("pharmacy", "Pharmacy"),
    ("home", "Home"),
    (OTHER, "Other"),
)

MEDICINES = (
    ("fluconazole", "Fluconazole"),
    ("amphotericin_b", "Amphotericin B"),
    ("rifampicin", "Rifampicin"),
    ("co_trimoxazole", "Co-trimoxazole"),
    (OTHER, "Other"),
)

POS_NEG_NA = ((POS, "Positive"), (NEG, "Negative"), (NOT_APPLICABLE, "Not applicable"))


REASON_DRUG_MISSED = (
    ("toxicity", "Toxicity"),
    ("missed", "Missed"),
    ("refused", "Refused"),
    ("not_required", "Not required according to protocol"),
    (OTHER, "Other"),
)


REPORTABLE = (
    (NOT_APPLICABLE, "Not applicable"),
    (GRADE3, "Yes, grade 3"),
    (GRADE4, "Yes, grade 4"),
    (NO, "Not reportable"),
    (ALREADY_REPORTED, "Already reported"),
    (PRESENT_AT_BASELINE, "Present at baseline"),
)

SIGNIFICANT_DX = (
    ("pulmonary_tb", "Pulmonary TB"),
    ("extra_pulmonary_tb", "Extra-pulmonary TB"),
    ("kaposi_sarcoma", "Kaposi-sarcoma"),
    ("malaria", "Malaria"),
    ("bacteraemia", "Bacteraemia"),
    ("pneumonia", "Pneumonia"),
    ("diarrhoeal_wasting", "Diarrhoeal wasting"),
    (OTHER, "Other"),
)

TB_SITE = (
    (NOT_APPLICABLE, "Not applicable"),
    ("pulmonary", "Pulmonary"),
    ("extra_pulmonary", "Extra-pulmonary"),
    ("both", "Both"),
)

TRANSPORT = (
    ("bus", "Bus"),
    ("train", "Train"),
    ("ambulance", "Ambulance"),
    ("private_taxi", "Private taxi"),
    ("hired_motorbike", "Hired motorbike"),
    ("own_car", "Own car"),
    ("own_motorbike", "Own motorbike"),
    (BICYCLE, "Bicycle"),
    (FOOT, "Foot"),
    (NOT_APPLICABLE, "Not applicable"),
)

URINE_CULTURE_RESULTS_ORGANISM = (
    (NOT_APPLICABLE, "Not applicable"),
    (ECOLI, "E.coli"),
    (KLEBSIELLA_SPP, "Klebsiella spp."),
    (OTHER, "Other"),
)

VISIT_UNSCHEDULED_REASON = (
    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
    ("recurrence_symptoms", "Recurrence of symptoms"),
    ("raised_icp_management", "Raised ICP management"),
    ("art_initiation", "ART initiation"),
    ("patient_hospitalised", "Patient hospitalised"),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

DAYS_MISSED = (
    (1, "Day 1"),
    (2, "Day 2"),
    (3, "Day 3"),
    (4, "Day 4"),
    (5, "Day 5"),
    (6, "Day 6"),
    (7, "Day 7"),
    (8, "Day 8"),
    (9, "Day 9"),
    (10, "Day 10"),
    (11, "Day 11"),
    (12, "Day 12"),
    (13, "Day 13"),
    (14, "Day 14"),
)

DOSES_MISSED = ((1, "1 Dose"), (2, "2 Doses"), (3, "3 Doses"), (4, "4 Doses"))


MG_MMOL_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER),
)

MG_UMOL_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MICROMOLES_PER_LITER, MICROMOLES_PER_LITER_DISPLAY),
)

MM3_PERC_UNITS = ((MM3, MM3_DISPLAY), ("%", "%"))

POS_NEG = (
    (POS, "Positive"),
    (NEG, "Negative"),
    (IND, "Indeterminate"),
    (NOT_DONE, "Not done"),
)

RANKIN_SCORE = (
    ("0", "0 - No symptoms at all"),
    (
        "1",
        (
            "1 - No significant disability despite symptoms; able to carry "
            "out all usual duties and activities"
        ),
    ),
    (
        "2",
        (
            "2 - Slight disability; unable to carry out all previous activities, "
            "but able to look after own affairs without assistance"
        ),
    ),
    (
        "3",
        (
            "3 - Moderate disability; requiring some help, but able to "
            "walk without assistance"
        ),
    ),
    (
        "4",
        (
            "4 - Moderately severe disability; unable to walk without "
            "assistance and unable to attend to own bodily needs without assistance"
        ),
    ),
    (
        "5",
        (
            "5 - Severe disability; bedridden, incontinent and requiring "
            "constant nursing care and attention"
        ),
    ),
    ("6", "6 - Dead"),
    (NOT_DONE, "Not done"),
    (NOT_APPLICABLE, "Not applicable"),
)

# REASON_NOT_DRAWN = (
#     (NOT_APPLICABLE, "Not applicable"),
#     ("collection_failed", "Tried, but unable to obtain sample from patient"),
#     ("absent", "Patient did not attend visit"),
#     ("refused", "Patient refused"),
#     ("no_supplies", "No supplies"),
#     (NOT_REQUIRED, "No longer required for this visit"),
#     (OTHER, "Other"),
# )

WEIGHT_DETERMINATION = (("estimated", "Estimated"), ("measured", "Measured"))

VISIT_REASON = (
    (SCHEDULED, "Scheduled visit"),
    (UNSCHEDULED, "Unscheduled visit"),
    (MISSED_VISIT, "Missed visit"),
)

YES_NO_ND = ((YES, "Yes"), (NO, "No"), (NOT_DONE, "Not done"))

YES_NO_ALREADY_ND = (
    (YES, "Yes"),
    (NO, "No"),
    ("already_on_rifampicin", "Already on Rifampicin"),
    (NOT_DONE, "Not done"),
)


YES_NO_RESULTS_UNKNOWN = ((YES, YES), (NO, NO), (RESULTS_UNKNOWN, "Results unknown"))

PATIENT_REL = (("patient", "Patient"), ("next_of_kin", "Next of Kin/Relative"))

YES_NO_NOT_DONE_WAIT_RESULTS = (
    (YES, YES),
    (NO, NO),
    (AWAITING_RESULTS, "Awaiting results"),
    (NOT_DONE, "Not done"),
)

SPUTUM_GENEXPERT = (
    ("mtb_detected_rif_resistance_detected", "MTB DETECTED & Rif Resistance DETECTED"),
    (
        "mtb_detected_rif_resistance_not_detected",
        "MTB DETECTED & Rif Resistance NOT detected",
    ),
    (
        "mtb_detected_rif_resistance_indeterminate",
        "MTB DETECTED & Rif Resistance INDETERMINATE",
    ),
    ("mtb_not_detected", "MTB NOT detected"),
    (NOT_APPLICABLE, "Not applicable"),
)
