from edc_constants.constants import OTHER, DEAD, YES, NO, NOT_APPLICABLE

from .constants import AZT_3TC_with_ATZ_r_or_Lopinavir_r
from .constants import (
    AZT_3TC_with_EFV_NVP_or_DTG,
    TDF_3TC_FTC_with_ATZ_r_or_Lopinavir_r,
)
from .constants import TDF_3TC_FTC_with_EFV_or_NVP
from .constants import DEVIATION, VIOLATION, CONSENT_WITHDRAWAL

ACTION_REQUIRED = (
    ("remain_on_study", "Participant to remain on trial"),
    ("to_be_withdrawn", "Participant to be withdrawn from trial"),
    (
        "remain_on_study_modified",
        "Patient remains on study but data analysis will be modified",
    ),
)


# CAUSE_OF_DEATH = (
#     (CRYTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
#     ("Cryptococcal_meningitis_relapse_IRIS", "Cryptococcal meningitis relapse/IRIS"),
#     (TUBERCULOSIS, "TB"),
#     ("bacteraemia", "Bacteraemia"),
#     ("bacterial_pneumonia", "Bacterial pneumonia"),
#     (MALIGNANCY, "Malignancy"),
#     ("art_toxicity", "ART toxicity"),
#     ("IRIS_non_CM", "IRIS non-CM"),
#     ("diarrhea_wasting", "Diarrhea/wasting"),
#     (UNKNOWN, "Unknown"),
#     (OTHER, "Other"),
# )


DEVIATION_VIOLATION = (
    (VIOLATION, "Protocol violation"),
    (DEVIATION, "Protocol deviation"),
)

FIRST_ARV_REGIMEN = (
    (NOT_APPLICABLE, "Not applicable"),
    (TDF_3TC_FTC_with_EFV_or_NVP, "TDF + 3TC/FTC + either EFV or NVP or DTG"),
    (AZT_3TC_with_EFV_NVP_or_DTG, "AZT+3TC+ either EFV or NVP or DTG"),
    (OTHER, "Other"),
)

FIRST_LINE_REGIMEN = (
    (NOT_APPLICABLE, "Not applicable"),
    ("EFV", "EFV"),
    ("DTG", "DTG"),
    ("NVP", "NVP"),
    (OTHER, "Other"),
)

PROTOCOL_VIOLATION = (
    ("failure_to_obtain_informed_consent", "Failure to obtain informed " "consent"),
    ("enrollment_of_ineligible_patient", "Enrollment of ineligible patient"),
    (
        "screening_procedure not done",
        "Screening procedure required by " "protocol not done",
    ),
    (
        "screening_or_on-study_procedure",
        "Screening or on-study procedure/lab " "work required not done",
    ),
    (
        "incorrect_research_treatment",
        "Incorrect research treatment given to " "patient",
    ),
    (
        "procedure_not_completed",
        "On-study procedure required by protocol not " "completed",
    ),
    ("visit_non-compliance", "Visit non-compliance"),
    ("medication_stopped_early", "Medication stopped early"),
    ("medication_noncompliance", "Medication_noncompliance"),
    (
        "national_regulations_not_met",
        "Standard WPD, ICH-GCP, local/national " "regulations not met",
    ),
    (OTHER, "Other"),
    (NOT_APPLICABLE, "Not applicable"),
)

REASON_STUDY_TERMINATED = (
    ("10_weeks_completed_follow_up", "Patient completed 10 weeks of follow-up"),
    ("patient_lost_to_follow_up", "Patient lost to follow-up"),
    (DEAD, "Reported/known to have died"),
    (CONSENT_WITHDRAWAL, "Withdrawal of Subject Consent for " "participation"),
    (
        "care_transferred_to_another_institution",
        "Care transferred to another institution",
    ),
    ("late_exclusion_criteria_met", "Late exclusion criteria met"),
    ("included_in_error", "Included in error"),
)

REASON_STUDY_TERMINATED_W10 = (
    ("16_weeks_completed_follow_up", "Patient completed 16 weeks of follow-up"),
    ("patient_lost_to_follow_up", "Patient lost to follow-up"),
    (DEAD, "Reported/known to have died"),
    (CONSENT_WITHDRAWAL, "Withdrawal of Subject Consent for " "participation"),
    (
        "care_transferred_to_another_institution",
        "Care transferred to another institution",
    ),
    ("included_in_error", "Included in error"),
)

SECOND_ARV_REGIMEN = (
    (NOT_APPLICABLE, "Not applicable"),
    (
        TDF_3TC_FTC_with_ATZ_r_or_Lopinavir_r,
        "TDF + 3TC/FTC + either ATZ/r or Lopinavir/r",
    ),
    (AZT_3TC_with_ATZ_r_or_Lopinavir_r, "AZT +3TC + either ATZ/r or Lopinavir/r"),
    (OTHER, "Other"),
)


YES_NO_ALREADY = (
    (YES, "Yes"),
    (NO, "No"),
    ("already_on_rifampicin", "Already on Rifampicin"),
)
