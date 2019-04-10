from ambition_permissions import TMG
from ambition_permissions.updaters import update_permissions
from ambition_rando.randomization_list_importer import RandomizationListImporter
from ambition_screening.models.subject_screening import SubjectScreening
from ambition_sites.sites import ambition_sites, fqdn
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import tag
from django.test.utils import override_settings
from django.urls.base import reverse
from django_webtest import WebTest
from edc_appointment.constants import IN_PROGRESS_APPT, SCHEDULED_APPT
from edc_appointment.models import Appointment
from edc_facility.import_holidays import import_holidays
from edc_list_data.site_list_data import site_list_data
from edc_permissions.constants.group_names import (
    EVERYONE,
    AUDITOR,
    CLINIC,
    PII,
    EXPORT,
    LAB,
)
from edc_sites.utils import add_or_update_django_sites
from edc_utils import get_utcnow
from model_mommy import mommy
from django.urls.exceptions import NoReverseMatch
import sys
from ambition_edc.apps import style
from edc_dashboard.url_names import url_names


User = get_user_model()


def login(testcase, user=None, superuser=None, groups=None):
    user = testcase.user if user is None else user
    superuser = True if superuser is None else superuser
    if not superuser:
        user.is_superuser = False
        user.is_active = True
        user.save()
        for group_name in groups:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
    form = testcase.app.get(reverse(settings.LOGIN_REDIRECT_URL)).maybe_follow().form
    form["username"] = user.username
    form["password"] = "pass"
    return form.submit()


@override_settings(SIMPLE_HISTORY_PERMISSIONS_ENABLED=True)
class AdminSiteTest(WebTest):
    def setUp(self):
        self.user = User.objects.create_superuser("user_login", "u@example.com", "pass")

    def login(self, **kwargs):
        return login(self, **kwargs)

    @tag("webtest")
    def test_home_everyone(self):
        self.login(superuser=False, groups=[EVERYONE])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertNotIn("Screening", response)
        self.assertNotIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_auditor(self):
        self.login(superuser=False, groups=[EVERYONE, AUDITOR])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_clinic(self):
        self.login(superuser=False, groups=[EVERYONE, CLINIC, PII])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_export(self):
        self.login(superuser=False, groups=[EVERYONE, EXPORT])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertNotIn("Screening", response)
        self.assertNotIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_tmg(self):
        self.login(superuser=False, groups=[EVERYONE, TMG])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertNotIn("Specimens", response)
        self.assertIn("Adverse events", response)
        self.assertIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_home_lab(self):
        self.login(superuser=False, groups=[EVERYONE, LAB])
        response = self.app.get(reverse("home_url"), user=self.user, status=200)
        self.assertIn("Screening", response)
        self.assertIn("Subjects", response)
        self.assertIn("Specimens", response)
        self.assertNotIn("Adverse events", response)
        self.assertNotIn("TMG reports", response)
        self.assertNotIn("Pharmacy", response)
        self.assertNotIn("Action items", response)
        self.assertNotIn("Export data", response)
        self.assertNotIn("Synchronization", response)
        self.assertIn("Switch sites", response)
        self.assertIn("Log out", response)

    @tag("webtest")
    def test_screening_no_pii(self):
        self.login(superuser=False, groups=[EVERYONE, CLINIC])
        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_page = home_page.click(description="Screening", index=1)
        self.assertNotIn("Add SubjectScreening", screening_page)

    @tag("webtest")
    def test_screening_form(self):
        subject_screening = mommy.prepare_recipe("ambition_screening.subjectscreening")
        self.login(superuser=False, groups=[EVERYONE, CLINIC, PII])

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)
        add_screening_page = screening_listboard_page.click(
            description="Add Subject Screening"
        )

        # submit blank form
        response = add_screening_page.form.submit()
        self.assertIn("Please correct the errors below", response)

        # submit completed form
        for field, _ in add_screening_page.form.fields.items():
            try:
                add_screening_page.form[field] = getattr(subject_screening, field)
            except AttributeError:
                pass
        page = add_screening_page.form.submit()

        # redirects back to listboard
        self.assertRedirects(
            page, reverse("ambition_dashboard:screening_listboard_url")
        )

        # new screened subject is available
        obj = SubjectScreening.objects.all().last()
        screening_listboard_page = home_page.click(description="Screening", index=1)
        self.assertIn(obj.screening_identifier, screening_listboard_page)

        add_subjectconsent_page = screening_listboard_page.click(
            description="Consent", index=1
        )

        self.assertEqual(add_subjectconsent_page.status_code, 200)

    @tag("webtest")
    def test_to_subject_dashboard(self):
        add_or_update_django_sites(apps=django_apps, sites=ambition_sites, fqdn=fqdn)
        RandomizationListImporter()
        update_permissions()
        import_holidays()
        site_list_data.autodiscover()
        self.login(superuser=False, groups=[EVERYONE, CLINIC, PII])

        subject_screening = mommy.make_recipe("ambition_screening.subjectscreening")

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)

        add_subjectconsent_page = screening_listboard_page.click(
            description="Consent", index=1
        )
        # submit blank form
        response = add_subjectconsent_page.form.submit()
        self.assertIn("Please correct the errors below", response)

        subject_consent = mommy.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            dob=(
                get_utcnow() - relativedelta(years=subject_screening.age_in_years)
            ).date(),
            first_name="Melissa",
            last_name="Rodriguez",
            initials="MR",
            consent_datetime=get_utcnow(),
        )

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        screening_listboard_page = home_page.click(description="Screening", index=1)

        self.assertIn("Dashboard", screening_listboard_page)
        self.assertIn(
            f"subjectscreening_change_{subject_screening.screening_identifier}",
            screening_listboard_page,
        )

        home_page = self.app.get(reverse("home_url"), user=self.user, status=200)
        subject_listboard_page = home_page.click(description="Subjects", index=1)

        self.assertIn(subject_consent.subject_identifier, subject_listboard_page)

        href = reverse(
            "ambition_dashboard:subject_dashboard_url",
            kwargs={"subject_identifier": subject_consent.subject_identifier},
        )
        subject_dashboard_page = subject_listboard_page.click(href=href)

        self.assertEqual(subject_dashboard_page.status_code, 200)

        # on subject_dashboard
        # assert all appointment are showing
        subject_identifier = subject_consent.subject_identifier
        appointments = Appointment.objects.filter(
            subject_identifier=subject_identifier
        ).order_by("appt_datetime")
        for appointment in appointments:
            self.assertIn(appointment.visit_code, subject_dashboard_page)

        # start appointment 1000
        page = subject_dashboard_page.click(linkid="start_btn_1000")
        page.form["appt_status"] = IN_PROGRESS_APPT
        page.form["appt_reason"] = SCHEDULED_APPT
        subject_dashboard_page = page.form.submit()
        self.assertEqual(subject_dashboard_page.status_code, 302)
        self.assertEqual(
            subject_dashboard_page.url,
            f"/subject/subject_dashboard/{subject_identifier}/",
        )

        subject_dashboard_page = self.app.get(
            subject_dashboard_page.url, user=self.user, status=200
        )

        # start visit 1000
        self.assertIn(" Start ", subject_dashboard_page)
        subject_visit_page = subject_dashboard_page.click(
            linkid=(
                f"start_btn_{appointments[0].visit_code}_"
                f"{appointments[0].visit_code_sequence}"
            )
        )
        subject_visit_page.form["info_source"] = "patient"
        subject_dashboard_page = subject_visit_page.form.submit()

        url = (
            f"/subject/subject_dashboard/{subject_identifier}/"
            f"{str(appointments[0].pk)}/"
        )
        self.assertEqual(subject_dashboard_page.status_code, 302)
        self.assertEqual(subject_dashboard_page.url, url)

        subject_dashboard_page = self.app.get(
            reverse(
                "ambition_dashboard:subject_dashboard_url",
                kwargs=dict(
                    subject_identifier=subject_identifier,
                    appointment=str(appointments[0].id),
                ),
            ),
            user=self.user,
            status=200,
        )

        self.assertIn("CRFs", subject_dashboard_page)
        self.assertIn("Requisitions", subject_dashboard_page)

    def test_follow_urls(self):
        """Follows any url that can be reversed without kwargs.
        """
        self.login(superuser=False, groups=[EVERYONE, CLINIC, PII])
        for url_name in url_names.registry.values():
            try:
                url = reverse(url_name)
            except NoReverseMatch:
                sys.stdout.write(
                    style.ERROR(f"NoReverseMatch: {url_name} without kwargs.\n")
                )
            else:
                sys.stdout.write(style.SUCCESS(f"{url_name} {url}\n"))
                self.app.get(url, user=self.user, status=200)
