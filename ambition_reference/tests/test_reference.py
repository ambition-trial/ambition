from django.test import TestCase, tag

from edc_reference.site_reference import site_reference_configs


@tag("ambition_reference")
class TestReference(TestCase):
    def test_(self):
        self.assertTrue(site_reference_configs.registry)
