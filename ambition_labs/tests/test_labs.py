from django.test import TestCase
from edc_lab.site_labs import site_labs
from edc_lab.models import Panel

from ..lab_profiles import subject_lab_profile


class TestLabs(TestCase):
    def setUp(self):
        site_labs._registry = {}
        site_labs.loaded = False
        site_labs.register(lab_profile=subject_lab_profile)

    def test_(self):
        obj = site_labs.get(lab_profile_name="subject_lab_profile")
        self.assertEqual(obj, subject_lab_profile)

    def test_lab_profile_model(self):
        obj = site_labs.get(lab_profile_name="subject_lab_profile")
        self.assertEqual("ambition_subject.subjectrequisition", obj.requisition_model)

    def test_panel_model(self):
        for panel in site_labs.get(
            lab_profile_name="subject_lab_profile"
        ).panels.values():
            self.assertEqual(
                panel.requisition_model, "ambition_subject.subjectrequisition"
            )

    def test_panels_exist(self):
        self.assertGreater(Panel.objects.all().count(), 0)
