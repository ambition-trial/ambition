from ambition_permissions.updaters import update_permissions
from django.test import tag
from edc_permissions.tests.test_group_permissions import TestGroupPermissions


class MyTestGroupPermissions(TestGroupPermissions):
    def test_permissions(self):
        update_permissions()
