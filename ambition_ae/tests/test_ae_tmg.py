from ambition_rando.tests import AmbitionTestCaseMixin
from django.contrib.auth.models import User, Permission
from django.test import TestCase, tag
from django.test.client import RequestFactory
from edc_adverse_event.models import AeClassification
from edc_list_data.site_list_data import site_list_data
from edc_registration.models import RegisteredSubject
from model_bakery import baker

from ..admin_site import ambition_ae_admin
from ..models.ae_tmg import AeTmg


@tag("ambition_ae")
class TestAeTmg(AmbitionTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        site_list_data.autodiscover()
        super().setUpClass()

    def setUp(self):

        self.user = User.objects.create(
            username="erikvw", is_staff=True, is_active=True
        )
        self.subject_identifier = "1234"
        permissions = Permission.objects.filter(
            content_type__app_label="ambition_ae",
            content_type__model__in=["aeinitial", "aetmg"],
        )
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.subject_identifier = "12345"
        RegisteredSubject.objects.create(subject_identifier=self.subject_identifier)

        anaemia = AeClassification.objects.get(name="anaemia")
        self.ae_initial = baker.make_recipe(
            "ambition_ae.aeinitial",
            subject_identifier=self.subject_identifier,
            ae_classification=anaemia,
        )

    def test_(self):
        for model, model_admin in ambition_ae_admin._registry.items():
            if model == AeTmg:
                ae_tmg_model_admin = model_admin.admin_site._registry.get(AeTmg)
        rf = RequestFactory()

        request = rf.get(
            f"/?subject_identifier={self.subject_identifier}&"
            f"ae_initial={str(self.ae_initial.pk)}"
        )

        request.user = self.user

        ModelForm = ae_tmg_model_admin.get_form(request, None, change=False)
        initial = ae_tmg_model_admin.get_changeform_initial_data(request)
        form = ModelForm(initial=initial)
        self.assertIn(self.ae_initial.ae_description, form.as_table())
