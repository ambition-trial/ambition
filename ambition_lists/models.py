from edc_list_data.model_mixins import ListModelMixin
from edc_model.models import BaseUuidModel

"""Models with explicit db_table were moved into this
module after the system went live.
"""


class Antibiotic(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_antibiotic"


class Day14Medication(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_day14medication"


class Medication(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_medication"


class Neurological(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_neurological"


class SignificantNewDiagnosis(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_significantnewdiagnosis"
        verbose_name = "Significant New Diagnosis"
        verbose_name_plural = "Significant New Diagnoses"


class Symptom(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_symptom"


class OtherDrug(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_otherdrug"


class AbnormalResultsReason(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_abnormalresultsreason"


class CXRType(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_cxrtype"


class InfiltrateLocation(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_infiltratelocation"


class MissedDoses(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_misseddoses"
        verbose_name = "Missed Dose"
        verbose_name_plural = "Missed Doses"


class ArvRegimens(ListModelMixin, BaseUuidModel):
    class Meta(ListModelMixin.Meta):
        db_table = "ambition_subject_arvregimens"
        verbose_name = "Arv Regimen"
        verbose_name_plural = "Arv Regimens"
