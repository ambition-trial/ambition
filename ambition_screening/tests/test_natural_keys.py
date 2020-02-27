from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from django.test.utils import override_settings
from django_collect_offline.models import OutgoingTransaction
from django_collect_offline.tests import OfflineTestHelper
from model_mommy import mommy


@override_settings(SITE_ID="10")
class TestNaturalKey(AmbitionTestCaseMixin, TestCase):

    offline_test_helper = OfflineTestHelper()

    def test_natural_key_attrs(self):
        self.offline_test_helper.offline_test_natural_key_attr("ambition_screening")

    def test_get_by_natural_key_attr(self):
        self.offline_test_helper.offline_test_get_by_natural_key_attr(
            "ambition_screening"
        )

    def test_deserialize_subject_screening(self):
        ambition_screening = mommy.make_recipe("ambition_screening.subjectscreening")
        outgoing_transaction = OutgoingTransaction.objects.get(
            tx_name=ambition_screening._meta.label_lower
        )
        self.offline_test_helper.offline_test_deserialize(
            ambition_screening, outgoing_transaction
        )
