from django.test import TestCase, tag
from edc_reportable import site_reportables, ParserError
from tempfile import mkdtemp


@tag("ambition_labs")
class TestReportables(TestCase):
    def test(self):
        try:
            from ambition_labs import reportables
        except ParserError:
            self.fail("ParserError unexpectedly raised.")
        self.assertIsNotNone(site_reportables.get("ambition"))
        filename1, filename2 = site_reportables.to_csv("ambition", path=mkdtemp())
        print(filename1)
        print(filename2)
