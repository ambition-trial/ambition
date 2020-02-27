import os
import shutil

from django.contrib.auth.models import User
from django.test import TestCase, tag
from django.test.utils import override_settings
from edc_export.archive_exporter import ArchiveExporter
from edc_registration.models import RegisteredSubject
from tempfile import mkdtemp


@override_settings(EXPORT_FOLDER=mkdtemp())
class TestExport(TestCase):
    def setUp(self):

        user = User.objects.create(username="erikvw")
        RegisteredSubject.objects.create(subject_identifier="12345")

        models = ["auth.user", "edc_registration.registeredsubject"]
        self.exported = ArchiveExporter(models=models, user=user, archive=True)

    def test_request_archive(self):

        folder = mkdtemp()
        shutil.unpack_archive(self.exported.archive_filename, folder, "zip")
        filenames = os.listdir(folder)
        self.assertGreater(len([f for f in filenames]), 0)

    def test_request_archive_filename_exists(self):
        filename = self.exported.archive_filename
        self.assertIsNotNone(filename)
        self.assertTrue(
            os.path.exists(filename), msg=f"file '{filename}' does not exist"
        )
