import pytz

from ambition_sites import ambition_sites, fqdn
from ambition_rando.tests import AmbitionTestCaseMixin
from ambition_visit_schedule.constants import WEEK10
from datetime import datetime
from django.apps import apps as django_apps
from django.contrib.auth.models import User, Permission
from django.contrib.sites.models import Site
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.test.utils import override_settings
from edc_appointment.models import Appointment
from edc_sites import add_or_update_django_sites
from edc_utils import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from ..admin_site import ambition_subject_admin
from ..models import FollowUp, SubjectVisit


@tag("ambition_subject")
@override_settings(SITE_ID="10")
class TestFollowUp(AmbitionTestCaseMixin, TestCase):
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
            if appointment.visit_code == WEEK10:
                self.appointment = appointment
                self.subject_visit = SubjectVisit.objects.create(
                    appointment=appointment,
                    subject_identifier=self.subject_identifier,
                    reason=SCHEDULED,
                )
                break
            else:
                SubjectVisit.objects.create(
                    appointment=appointment,
                    subject_identifier=self.subject_identifier,
                    reason=SCHEDULED,
                )

    #     def test_visit(self):
    #         subject_visit = SubjectVisit.objects.last()
    #         print('---------------------')
    #         print(
    #             'CrfMetadata', [pprint(o.__dict__) for o in CrfMetadata.objects.filter(
    #                 visit_code=subject_visit.visit_code)])
    #         print('---------------------')
    #         self.assertGreater(CrfMetadata.objects.filter(
    #             visit_code=subject_visit.visit_code).count(), 0)
    #         self.assertGreater(RequisitionMetadata.objects.filter(
    #             visit_code=subject_visit.visit_code).count(), 0)
    #         subject_visit.reason = MISSED_VISIT
    #         subject_visit.save()
    #         subject_visit.refresh_from_db()
    #         self.assertEqual(MISSED_VISIT, subject_visit.reason)
    #         print('---------------------')
    #         print(
    #             'CrfMetadata', [pprint(o.__dict__) for o in CrfMetadata.objects.filter(
    #                 visit_code=subject_visit.visit_code)])
    #         print('---------------------')
    #         self.assertEqual(CrfMetadata.objects.filter(
    #             visit_code=subject_visit.visit_code,
    #             subject_identifier=subject_visit.subject_identifier).exclude(
    #                 entry_status=KEYED).count(), 0)
    #         self.assertEqual(RequisitionMetadata.objects.filter(
    #             visit_code=subject_visit.visit_code).count(), 0)

    def test_(self):
        """Asserts custom antibiotic question shows for Week 10.
        """
        for model, model_admin in ambition_subject_admin._registry.items():
            if model == FollowUp:
                my_model_admin = model_admin.admin_site._registry.get(FollowUp)

        rf = RequestFactory()

        request = rf.get(f"/?appointment={str(self.appointment.id)}")

        request.user = self.user
        request.site = Site.objects.get_current()

        rendered_change_form = my_model_admin.changeform_view(
            request, None, "", {"subject_visit": self.subject_visit}
        )
        self.assertIn(
            "Were any of the following antibiotics given since week two?",
            rendered_change_form.rendered_content,
        )
