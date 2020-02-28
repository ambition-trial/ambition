import re

from ambition_prn.models import OnSchedule
from ambition_rando.tests import AmbitionTestCaseMixin
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_constants.constants import UUID_PATTERN
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from model_bakery import baker

from ..models import SubjectConsent


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestSubjectConsent(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        self.subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening"
        )

    def test_allocated_subject_identifier(self):
        """Test consent successfully allocates subject identifier on
        save.
        """
        options = {
            "screening_identifier": self.subject_screening.screening_identifier,
            "consent_datetime": get_utcnow,
            "user_created": "erikvw",
        }
        baker.make_recipe("ambition_subject.subjectconsent", **options)
        self.assertFalse(
            re.match(UUID_PATTERN, SubjectConsent.objects.all()[0].subject_identifier)
        )

    def test_consent_creates_registered_subject(self):
        options = {
            "screening_identifier": self.subject_screening.screening_identifier,
            "consent_datetime": get_utcnow,
            "user_created": "erikvw",
        }
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        baker.make_recipe("ambition_subject.subjectconsent", **options)
        self.assertEqual(RegisteredSubject.objects.all().count(), 1)

    def test_consent_creates_registered_subject_sets_screening_subject_identifier(self):
        # screening subject identifier starts out as a UUID
        self.assertTrue(
            re.match(UUID_PATTERN, self.subject_screening.subject_identifier)
        )
        options = {
            "screening_identifier": self.subject_screening.screening_identifier,
            "consent_datetime": get_utcnow,
            "user_created": "erikvw",
        }
        # consent
        baker.make_recipe("ambition_subject.subjectconsent", **options)

        rs = RegisteredSubject.objects.get(
            screening_identifier=self.subject_screening.screening_identifier
        )

        self.subject_screening.refresh_from_db()
        # screening subject identifier is not set to a valid study allocated
        # subject identifier.
        self.assertFalse(
            re.match(UUID_PATTERN, self.subject_screening.subject_identifier)
        )
        self.assertEqual(
            self.subject_screening.subject_identifier, rs.subject_identifier
        )

    def test_onschedule_created_on_consent(self):
        subject_consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            consent_datetime=get_utcnow,
            screening_identifier=self.subject_screening.screening_identifier,
            user_created="erikvw",
        )

        try:
            OnSchedule.objects.get(
                subject_identifier=subject_consent.subject_identifier
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist was unexpectedly raised.")
