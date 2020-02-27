from ambition_rando.tests import AmbitionTestCaseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag
from edc_identifier.models import IdentifierModel
from model_mommy import mommy

from ..identifiers import ScreeningIdentifier


class TestIdentifiers(AmbitionTestCaseMixin, TestCase):
    def test_identifier(self):
        identifier = ScreeningIdentifier()
        self.assertTrue(identifier.identifier)
        self.assertTrue(identifier.identifier.startswith("S"))

    def test_identifier_history(self):
        identifier = ScreeningIdentifier()
        try:
            IdentifierModel.objects.get(identifier=identifier.identifier)
        except ObjectDoesNotExist:
            self.fail("IdentifierHistory.DoesNotExist unexpectedly raised.")

    def test_model_allocates_identifier(self):
        obj = mommy.make_recipe("ambition_screening.subjectscreening")
        self.assertIsNotNone(obj.screening_identifier)
        self.assertTrue(obj.screening_identifier.startswith("S"))
