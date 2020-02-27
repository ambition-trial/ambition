from edc_list_data import PreloadData
from edc_constants.constants import (
    OTHER,
    NOT_APPLICABLE,
    DEAD,
    TUBERCULOSIS,
    MALIGNANCY,
    UNKNOWN,
)
from .constants import CRYTOCOCCAL_MENINGITIS


list_data = {
    "ambition_ae.antibiotictreatment": [
        ("amoxicillin", "Amoxicillin"),
        ("flucloxacillin", "Flucloxacillin"),
        ("doxycycline", "Doxycycline"),
        ("ceftriaxone", "Ceftriaxone"),
        ("erythromycin", "Erythromycin"),
        ("ciprofloxacin", "Ciprofloxacin"),
        ("no_treatment", "- No treatment"),
        (OTHER, "- Other, specify"),
    ],
    "ambition_ae.meningitissymptom": [
        ("headache", "Headache"),
        ("vomiting", "Vomiting"),
        ("fever", "Fever"),
        ("seizures", "Seizures"),
        ("neck_pain", "Neck pain"),
        ("no_symptoms", "- No symptoms"),
        (OTHER, "- Other, specify"),
    ],
    "ambition_ae.neurological": [
        ("meningism", "Meningism"),
        ("papilloedema", " Papilloedema"),
        ("focal_neurologic_deficit", "Focal neurologic deficit"),
        ("CN_VI_palsy", "Cranial Nerve VI palsy"),
        ("CN_III_palsy", "Cranial Nerve III palsy"),
        ("CN_IV_palsy", "Cranial Nerve IV palsy"),
        ("CN_VII_palsy", "Cranial Nerve VII palsy"),
        ("CN_VIII_palsy", "Cranial Nerve VIII palsy"),
        ("no_symptoms", "- No symptoms"),
        (OTHER, "- Other CN palsy"),
    ],
    "edc_adverse_event.aeclassification": [
        ("anaemia", "Anaemia"),
        ("bacteraemia/sepsis", "Bacteraemia/Sepsis"),
        ("CM_IRIS", "CM IRIS"),
        ("diarrhoea", "Diarrhoea"),
        ("hypokalaemia", "Hypokalaemia"),
        ("neutropaenia", "Neutropaenia"),
        ("pneumonia", "Pneumonia"),
        ("renal_impairment", "Renal impairment"),
        ("respiratory_distress", "Respiratory distress"),
        ("TB", "TB"),
        ("thrombocytopenia", "Thrombocytopenia"),
        ("thrombophlebitis", "Thrombophlebitis"),
        (OTHER, "Other"),
    ],
    "edc_adverse_event.saereason": [
        (NOT_APPLICABLE, "Not applicable"),
        (DEAD, "Death"),
        ("life_threatening", "Life-threatening"),
        ("significant_disability", "Significant disability"),
        (
            "in-patient_hospitalization",
            (
                "In-patient hospitalization or prolongation "
                "(17 or more days from study inclusion)"
            ),
        ),
        (
            "medically_important_event",
            "Medically important event (e.g. Severe thrombophlebitis, Bacteraemia, "
            "recurrence of symptoms not requiring admission, Hospital acquired "
            "pneumonia)",
        ),
    ],
    "edc_adverse_event.causeofdeath": [
        (CRYTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
        (
            "Cryptococcal_meningitis_relapse_IRIS",
            "Cryptococcal meningitis relapse/IRIS",
        ),
        (TUBERCULOSIS, "TB"),
        ("bacteraemia", "Bacteraemia"),
        ("bacterial_pneumonia", "Bacterial pneumonia"),
        (MALIGNANCY, "Malignancy"),
        ("art_toxicity", "ART toxicity"),
        ("IRIS_non_CM", "IRIS non-CM"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other"),
    ],
}

preload_data = PreloadData(list_data=list_data, model_data={}, unique_field_data=None)
