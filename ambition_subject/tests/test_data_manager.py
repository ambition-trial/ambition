import pytz

from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_sites import ambition_sites, fqdn
from datetime import datetime
from django.apps import apps as django_apps
from django.contrib.auth.models import User, Permission
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject
from edc_sites import add_or_update_django_sites
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from ..models import SubjectVisit


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestDataManager(AmbitionTestCaseMixin, TestCase):
    def setUp(self):
        year = get_utcnow().year
        add_or_update_django_sites(
            apps=django_apps, sites=ambition_sites, fqdn=fqdn, verbose=False
        )
        self.user = User.objects.create(
            username="erikvw", is_staff=True, is_active=True
        )
        for permission in Permission.objects.filter(
            content_type__app_label="ambition_subject", content_type__model="followup"
        ):
            self.user.user_permissions.add(permission)

        subject_screening = baker.make_recipe("ambition_screening.subjectscreening")
        consent = baker.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            consent_datetime=datetime(year, 12, 1, 0, 0, 0, 0, pytz.utc),
            user_created="erikvw",
        )
        self.subject_identifier = consent.subject_identifier

        for appointment in Appointment.objects.filter(
            subject_identifier=self.subject_identifier
        ).order_by("timepoint"):
            SubjectVisit.objects.create(
                appointment=appointment,
                subject_identifier=self.subject_identifier,
                reason=SCHEDULED,
            )

        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=consent.subject_identifier
        )
