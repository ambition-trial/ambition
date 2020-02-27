from django.test import TestCase, tag
from edc_list_data.preload_data import PreloadData

from ..list_data import list_data
from ..models import (
    AbnormalResultsReason,
    Antibiotic,
    ArvRegimens,
    CXRType,
    Day14Medication,
    InfiltrateLocation,
    Medication,
    MissedDoses,
    Neurological,
    OtherDrug,
    SignificantNewDiagnosis,
    Symptom,
)


class TestPreload(TestCase):
    def test_preload(self):

        PreloadData(list_data=list_data)
        self.assertGreater(AbnormalResultsReason.objects.count(), 0)
        self.assertGreater(Antibiotic.objects.count(), 0)
        self.assertGreater(ArvRegimens.objects.count(), 0)
        self.assertGreater(CXRType.objects.count(), 0)
        self.assertGreater(Day14Medication.objects.count(), 0)
        self.assertGreater(InfiltrateLocation.objects.count(), 0)
        self.assertGreater(Medication.objects.count(), 0)
        self.assertGreater(MissedDoses.objects.count(), 0)
        self.assertGreater(Neurological.objects.count(), 0)
        self.assertGreater(OtherDrug.objects.count(), 0)
        self.assertGreater(SignificantNewDiagnosis.objects.count(), 0)
        self.assertGreater(Symptom.objects.count(), 0)
