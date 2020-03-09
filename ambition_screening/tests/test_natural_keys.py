from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from django.test.utils import override_settings
from django_collect_offline.models import OutgoingTransaction
from django_collect_offline.site_offline_models import site_offline_models
from django_collect_offline.tests import OfflineTestHelper
from model_bakery import baker


@tag("ambition_screening1")
@override_settings(SITE_ID="10")
class TestNaturalKey(AmbitionTestCaseMixin, TestCase):
    offline_test_helper = OfflineTestHelper()

    def test_natural_key_attrs(self):
        self.offline_test_helper.offline_test_natural_key_attr("ambition_screening")

    def test_get_by_natural_key_attr(self):
        self.offline_test_helper.offline_test_get_by_natural_key_attr(
            "ambition_screening"
        )

    @override_settings(DJANGO_COLLECT_OFFLINE_ENABLED=True)
    def test_deserialize_subject_screening(self):
        site_offline_models.autodiscover()
        ambition_screening = baker.make_recipe("ambition_screening.subjectscreening")
        outgoing_transaction = OutgoingTransaction.objects.get(
            tx_name=ambition_screening._meta.label_lower
        )
        self.offline_test_helper.offline_test_deserialize(
            ambition_screening, outgoing_transaction
        )
