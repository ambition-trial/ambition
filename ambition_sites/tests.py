from django.test import TestCase
from edc_sites import get_site_id, InvalidSiteError

from .sites import ambition_sites


class SiteTests(TestCase):
    def test_all(self):
        self.assertEqual(get_site_id("reviewer", sites=ambition_sites), 1)
        self.assertEqual(get_site_id("gaborone", sites=ambition_sites), 10)
        self.assertEqual(get_site_id("harare", sites=ambition_sites), 20)
        self.assertEqual(get_site_id("lilongwe", sites=ambition_sites), 30)
        self.assertEqual(get_site_id("blantyre", sites=ambition_sites), 40)
        self.assertEqual(get_site_id("capetown", sites=ambition_sites), 50)
        self.assertEqual(get_site_id("kampala", sites=ambition_sites), 60)

    def test_bad(self):
        self.assertRaises(InvalidSiteError, get_site_id, "erik", sites=ambition_sites)
