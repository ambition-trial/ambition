from ambition_auth import RANDO, TMG
from ambition_auth.permissions_updater import PermissionsUpdater
from django.test import tag
from edc_permissions.constants import CLINIC
from edc_permissions.permissions_inspector import PermissionsInspector
from edc_permissions.tests.test_group_permissions import TestGroupPermissions


@tag('permissions')
class MyTestGroupPermissions(TestGroupPermissions):

    permissions_updater_cls = PermissionsUpdater

    def setUp(self):
        self.updater = self.permissions_updater_cls(verbose=True)
        self.inspector = PermissionsInspector(
            extra_group_names=[RANDO, TMG],
            extra_pii_models=[
                'ambition_screening.subjectscreening',
                'ambition_subject.subjectconsent',
                'ambition_subject.subjectreconsent',
                'edc_locator.subjectlocator',
                'edc_registration.registeredsubject',
            ])

    def test_clinic(self):
        self.compare_codenames(CLINIC)

    def test_rando(self):
        self.compare_codenames(RANDO)

    def test_tmg(self):
        self.compare_codenames(TMG)
