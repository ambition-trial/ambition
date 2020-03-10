from ambition_rando.tests import AmbitionTestCaseMixin
from django.test import TestCase, tag
from django.test.utils import override_settings
from django_collect_offline.models import OutgoingTransaction
from django_collect_offline.tests import OfflineTestHelper
from edc_adverse_event.constants import RECOVERING
from edc_adverse_event.models.cause_of_death import CauseOfDeath
from edc_metadata.tests import CrfTestHelper
from edc_registration.models import RegisteredSubject
from model_bakery import baker

from ..constants import CRYTOCOCCAL_MENINGITIS


@tag("ambition_ae")
@override_settings(SITE_ID="10")
class TestNaturalKey(AmbitionTestCaseMixin, TestCase):
    offline_test_helper = OfflineTestHelper()
    crf_test_helper = CrfTestHelper()

    def setUp(self):
        self.subject_identifier = "12345"
        RegisteredSubject.objects.create(subject_identifier=self.subject_identifier)

    def test_natural_key_attrs(self):
        self.offline_test_helper.offline_test_natural_key_attr("ambition_ae")

    def test_get_by_natural_key_attr(self):
        self.offline_test_helper.offline_test_get_by_natural_key_attr("ambition_ae")

    def test_deserialize_ae_initial(self):
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=ae_initial._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                ae_initial, outgoing_transaction
            )

    def test_deserialize_ae_tmg(self):
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        ae_tmg = baker.make_recipe(
            "ambition_ae.aetmg",
            ae_initial=ae_initial,
            subject_identifier=self.subject_identifier,
        )
        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=ae_tmg._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                ae_tmg, outgoing_transaction
            )

    def test_deserialize_ae_followup(self):
        ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial", subject_identifier=self.subject_identifier
        )
        ae_followup = baker.make_recipe(
            "ambition_ae.aefollowup",
            ae_initial=ae_initial,
            subject_identifier=self.subject_identifier,
            outcome=RECOVERING,
        )
        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=ae_followup._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                ae_followup, outgoing_transaction
            )

    def test_deserialize_recurrence_symptom(self):
        recurrence_symptoms = baker.make_recipe(
            "ambition_ae.recurrencesymptom", subject_identifier=self.subject_identifier
        )
        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=recurrence_symptoms._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                recurrence_symptoms, outgoing_transaction
            )

    def test_deserialize_death_report(self):
        self.subject_identifier = self.create_subject()

        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=self.subject_identifier,
            cause_of_death=cause_of_death,
        )

        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=death_report._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                death_report, outgoing_transaction
            )

    def test_deserialize_death_report_tmg(self):
        self.subject_identifier = self.create_subject()
        cause_of_death = CauseOfDeath.objects.get(name=CRYTOCOCCAL_MENINGITIS)
        death_report = baker.make_recipe(
            "ambition_ae.deathreport",
            subject_identifier=self.subject_identifier,
            cause_of_death=cause_of_death,
        )
        death_report_tmg = baker.make_recipe(
            "ambition_ae.deathreporttmg",
            subject_identifier=self.subject_identifier,
            death_report=death_report,
            cause_of_death=cause_of_death,
        )
        for outgoing_transaction in OutgoingTransaction.objects.filter(
            tx_name=death_report_tmg._meta.label_lower
        ):
            self.offline_test_helper.offline_test_deserialize(
                death_report_tmg, outgoing_transaction
            )
