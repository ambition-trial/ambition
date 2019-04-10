from django.test import tag
from edc_permissions.tests.test_group_permissions import TestGroupPermissions

from ..updaters import update_permissions


class MyTestGroupPermissions(TestGroupPermissions):
    def test_permissions(self):
        update_permissions()
