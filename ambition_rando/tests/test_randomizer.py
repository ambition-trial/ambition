import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_registration.models import RegisteredSubject
from edc_randomization.randomization_list_importer import RandomizationListImporter
from edc_randomization.randomization_list_verifier import (
    RandomizationListVerifier,
    RandomizationListError,
)
from edc_randomization.randomizer import (
    RandomizationError,
    AllocationError,
    AlreadyRandomized,
    InvalidAssignment,
)
from edc_randomization.site_randomizers import site_randomizers
from random import shuffle
from tempfile import mkdtemp

from ..randomizer import Randomizer
from .ambition_test_case_mixin import AmbitionTestCaseMixin
from .make_test_list import make_test_list
from .models import SubjectConsent


@tag("ambition_rando")
class TestRandomizer(AmbitionTestCaseMixin, TestCase):
    import_randomization_list = False

    def setUp(self):
        super().setUp()
        site_randomizers._registry = {}
        site_randomizers.register(Randomizer)

    def populate_list(self, site_names=None, per_site=None):
        make_test_list(
            site_names=site_names or self.site_names,
            per_site=per_site,
            full_path=os.path.join(
                settings.EDC_RANDOMIZATION_LIST_PATH,
                site_randomizers.get("ambition").filename,
            ),
        )
        RandomizationListImporter(name="ambition", overwrite=True)

    @override_settings(SITE_ID=40)
    def test_with_consent_no_site(self):
        self.populate_list()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        self.assertRaises(
            RandomizationError,
            site_randomizers.get("ambition"),
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=None,
            user=subject_consent.user_created,
        )

    @override_settings(SITE_ID=40)
    def test_with_consent_ok(self):
        self.populate_list()
        site = Site.objects.get_current()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", site=site, user_created="erikvw"
        )
        site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_with_list_selects_first(self):
        self.populate_list()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        site = Site.objects.get_current()
        randomization_list_model_cls.objects.update(site_name=site.name)
        first_obj = randomization_list_model_cls.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        rando = site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        self.assertEqual(rando.sid, first_obj.sid)

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_updates_registered_subject(self):
        self.populate_list()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        site = Site.objects.get_current()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        first_obj = randomization_list_model_cls.objects.all().first()
        rs = RegisteredSubject.objects.get(subject_identifier="12345")
        self.assertEqual(rs.subject_identifier, first_obj.subject_identifier)
        self.assertEqual(rs.sid, str(first_obj.sid))
        self.assertEqual(rs.randomization_datetime, first_obj.allocated_datetime)

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_updates_list_obj_as_allocated(self):
        self.populate_list()
        site = Site.objects.get_current()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        randomization_list_model_cls.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        first_obj = randomization_list_model_cls.objects.all().first()
        self.assertEqual(first_obj.subject_identifier, "12345")
        self.assertTrue(first_obj.allocated)
        self.assertIsNotNone(first_obj.allocated_user)
        self.assertEqual(first_obj.allocated_user, subject_consent.user_created)
        self.assertEqual(first_obj.allocated_datetime, subject_consent.consent_datetime)
        self.assertGreater(first_obj.modified, subject_consent.modified)

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_cannot_rerandomize(self):
        self.populate_list()
        site = Site.objects.get_current()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        first_obj = randomization_list_model_cls.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        rando = site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        self.assertEqual(rando.sid, first_obj.sid)
        self.assertRaises(
            AlreadyRandomized,
            site_randomizers.get("ambition"),
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_error_condition1(self):
        """Assert raises if RegisteredSubject not updated correctly.
        """
        self.populate_list()
        site = Site.objects.get_current()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        rando = site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        with self.assertRaises(AlreadyRandomized) as cm:
            site_randomizers.get("ambition")(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                site=subject_consent.site,
                user=subject_consent.user_created,
            )
        self.assertEqual(
            cm.exception.code, randomization_list_model_cls._meta.label_lower
        )

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_error_condition2(self):
        """Assert raises if randomization_list_model_cls not updated correctly.
        """
        self.populate_list()
        site = Site.objects.get_current()
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", user_created="erikvw"
        )
        rando = site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        with self.assertRaises(AlreadyRandomized) as cm:
            site_randomizers.get("ambition")(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                site=subject_consent.site,
                user=subject_consent.user_created,
            )
        self.assertEqual(
            cm.exception.code, randomization_list_model_cls._meta.label_lower
        )

    @override_settings(EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),)
    def test_error_condition3(self):
        """Assert raises if randomization_list_model_cls not updated correctly.
        """
        self.populate_list()
        site = Site.objects.get(name="gaborone")
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", site=site, user_created="erikvw"
        )
        site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        randomization_list_model_cls.objects.update(subject_identifier=None)
        with self.assertRaises(AlreadyRandomized) as cm:
            site_randomizers.get("ambition")(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                site=subject_consent.site,
                user=subject_consent.user_created,
            )
        self.assertEqual(cm.exception.code, "edc_registration.registeredsubject")

    @override_settings(EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),)
    def test_subject_does_not_exist(self):
        self.populate_list()
        site = Site.objects.get(name="gaborone")
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", site=site, user_created="erikvw"
        )
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            RandomizationError,
            site_randomizers.get("ambition"),
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )

    @override_settings(EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),)
    def test_str(self):
        self.populate_list()
        site = Site.objects.get(name="gaborone")
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.update(site_name=site.name)
        subject_consent = SubjectConsent.objects.create(
            subject_identifier="12345", site=site, user_created="erikvw"
        )
        site_randomizers.get("ambition")(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )
        obj = randomization_list_model_cls.objects.all().first()
        self.assertTrue(str(obj))

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_for_sites(self):
        """Assert that allocates by site correctly.
        """
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        randomization_list_model_cls.objects.all().delete()
        self.populate_list(site_names=self.site_names, per_site=5)
        site_names = [
            obj.site_name for obj in randomization_list_model_cls.objects.all()
        ]
        shuffle(site_names)
        assert len(site_names) == len(self.site_names * 5)
        # consent and randomize 5 for each site
        for index, site_name in enumerate(site_names):
            site = Site.objects.get(name=site_name)
            subject_consent = SubjectConsent.objects.create(
                subject_identifier=f"12345{index}", site=site, user_created="erikvw"
            )
            site_randomizers.get("ambition")(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                site=subject_consent.site,
                user=subject_consent.user_created,
            )
        # assert consented subjects were allocated SIDs in the
        # correct order per site.
        for site_name in site_names:
            randomized_subjects = [
                (obj.subject_identifier, str(obj.sid))
                for obj in randomization_list_model_cls.objects.filter(
                    allocated_site__name=site_name, subject_identifier__isnull=False
                ).order_by("sid")
            ]
            for index, obj in enumerate(
                SubjectConsent.objects.filter(site__name=site_name).order_by(
                    "consent_datetime"
                )
            ):
                rs = RegisteredSubject.objects.get(
                    subject_identifier=obj.subject_identifier
                )
                self.assertEqual(obj.subject_identifier, randomized_subjects[index][0])
                self.assertEqual(rs.sid, randomized_subjects[index][1])

        # clear out any unallocated
        randomization_list_model_cls.objects.filter(
            subject_identifier__isnull=True
        ).delete()

        # assert raises on next attempt to randomize
        subject_consent = SubjectConsent.objects.create(
            subject_identifier=f"ABCDEF", site=site, user_created="erikvw"
        )
        self.assertRaises(
            AllocationError,
            site_randomizers.get("ambition"),
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            site=subject_consent.site,
            user=subject_consent.user_created,
        )

    @override_settings(SITE_ID=40, EDC_RANDOMIZTION_LIST_PATH="/tmp/erik.csv")
    def test_invalid_path(self):
        with self.assertRaises(RandomizationListError) as cm:
            RandomizationListVerifier(randomizer_name="ambition").message
        self.assertIn("Randomization list has not been loaded.", str(cm.exception))

    @override_settings(
        SITE_ID=40, EDC_RANDOMIZATION_LIST_PATH=os.path.join(mkdtemp()),
    )
    def test_invalid_assignment(self):
        # change to a different assignments
        assignments = [100, 101]
        make_test_list(
            full_path=os.path.join(
                settings.EDC_RANDOMIZATION_LIST_PATH,
                site_randomizers.get("ambition").filename,
            ),
            site_names=self.site_names,
            assignments=assignments,
            count=5,
        )
        self.assertRaises(InvalidAssignment, RandomizationListImporter, name="ambition")

    @override_settings(SITE_ID=40)
    def test_invalid_sid(self):
        # change to a different starting SID
        RandomizationListImporter(name="ambition")
        randomization_list_model_cls = site_randomizers.get("ambition").model_cls()
        obj = randomization_list_model_cls.objects.all().order_by("sid").first()
        obj.sid = 100
        obj.save()
        with self.assertRaises(RandomizationListError) as cm:
            RandomizationListVerifier(randomizer_name="ambition")
        self.assertIn("Randomization list has invalid SIDs", str(cm.exception))

    @override_settings(SITE_ID=40)
    def test_invalid_count(self):
        Randomizer.model_cls().objects.all().delete()
        site = Site.objects.get_current()
        RandomizationListImporter(name="ambition")
        # change number of SIDs in DB
        cnt = Randomizer.model_cls().objects.all().count()
        Randomizer.model_cls().objects.create(
            sid=100, assignment="single_dose", site_name=site.name
        )
        self.assertEqual(cnt + 1, Randomizer.model_cls().objects.all().count())
        self.assertRaises(
            RandomizationListError,
            RandomizationListVerifier,
            randomizer_name="ambition",
        )
        with self.assertRaises(RandomizationListError) as cm:
            RandomizationListVerifier(randomizer_name="ambition")
        self.assertIn(
            f"Randomization list count is off. Expected {cnt} (CSV). Got {cnt + 1} (model_cls)",
            str(cm.exception),
        )
