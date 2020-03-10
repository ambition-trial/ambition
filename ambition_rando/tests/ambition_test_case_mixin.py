from ambition_sites import ambition_sites, fqdn
from django.apps import apps as django_apps
from django.contrib.sites.models import Site
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_randomization.randomization_list_importer import RandomizationListImporter
from edc_randomization.site_randomizers import site_randomizers
from edc_sites import add_or_update_django_sites
from edc_utils import get_utcnow
from faker import Faker
from model_bakery import baker

from ..constants import SINGLE_DOSE, CONTROL
from ..models import RandomizationList
from ..randomizer import Randomizer

fake = Faker()


class AmbitionTestCaseMixin:
    import_randomization_list = True
    randomizer_name = "ambition"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        site_randomizers._registry = {}
        site_randomizers.register(Randomizer)
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn, verbose=False
        )
        if cls.import_randomization_list:
            RandomizationListImporter(name="ambition", verbose=False)
        import_holidays(test=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()

    @property
    def site_names(self):
        return [obj.name for obj in Site.objects.all()]

    def create_subject(self, consent_datetime=None, first_name=None):
        consent_datetime = consent_datetime or get_utcnow()
        first_name = first_name or fake.first_name()
        subject_screening = baker.make_recipe(
            "ambition_screening.subjectscreening", report_datetime=consent_datetime
        )
        consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            consent_datetime=consent_datetime,
            first_name=first_name,
            user_created="erikvw",
        )
        return consent.subject_identifier

    def get_subject_by_assignment(self, assignment):
        randomization_list_model_cls = site_randomizers.get(
            self.randomizer_name
        ).model_cls()
        for _ in range(0, 4):
            subject_identifier = self.create_subject()
            obj = randomization_list_model_cls.objects.get(
                subject_identifier=subject_identifier
            )
            if Randomizer.get_assignment({"assignment": obj.assignment}) == assignment:
                return subject_identifier
        raise ValueError(
            f"Subject identifier cannot be None. Git assignment={assignment}"
        )

    def get_single_dose_subject(self):
        return self.get_subject_by_assignment(SINGLE_DOSE)

    def get_control_subject(self):
        return self.get_subject_by_assignment(CONTROL)
