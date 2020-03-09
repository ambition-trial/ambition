from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel

"""Models with explicit db_table were moved into this
module after the system went live.
"""


class Antibiotic(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Antibiotic"
        verbose_name_plural = "Antibiotics"
        db_table = "ambition_subject_antibiotic"


class Day14Medication(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Day 14 Medication"
        verbose_name_plural = "Day 14 Medications"
        db_table = "ambition_subject_day14medication"


class Medication(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Medication"
        verbose_name_plural = "Medications"
        db_table = "ambition_subject_medication"


class Neurological(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Neurological"
        verbose_name_plural = "Neurological"
        db_table = "ambition_subject_neurological"


class SignificantNewDiagnosis(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Significant New Diagnosis"
        verbose_name_plural = "Significant New Diagnoses"
        db_table = "ambition_subject_significantnewdiagnosis"


class Symptom(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Symptom"
        verbose_name_plural = "Symptoms"
        db_table = "ambition_subject_symptom"


class OtherDrug(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Othe Drug"
        verbose_name_plural = "Other Drugs"
        db_table = "ambition_subject_otherdrug"


class AbnormalResultsReason(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Abnormal Results Reason"
        verbose_name_plural = "Abnormal Results Reasons"
        db_table = "ambition_subject_abnormalresultsreason"


class CXRType(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "CXR Type"
        verbose_name_plural = "CXR Types"
        db_table = "ambition_subject_cxrtype"


class InfiltrateLocation(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Infiltrate Location"
        verbose_name_plural = "Infiltrate Locations"
        db_table = "ambition_subject_infiltratelocation"


class MissedDoses(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Missed Dose"
        verbose_name_plural = "Missed Doses"
        db_table = "ambition_subject_misseddoses"


class ArvRegimens(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        verbose_name = "Arv Regimen"
        verbose_name_plural = "Arv Regimens"
        db_table = "ambition_subject_arvregimens"
