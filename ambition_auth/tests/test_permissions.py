from django.test import TestCase, tag
from edc_auth.utils import compare_codenames_for_group
from edc_auth.group_permissions_updater import GroupPermissionsUpdater
from edc_auth import (
    ACCOUNT_MANAGER,
    AE,
    AE_REVIEW,
    AUDITOR,
    CLINIC,
    EVERYONE,
    LAB,
    LAB_VIEW,
    SCREENING,
    PII,
    PII_VIEW,
    RANDO,
    TMG,
)

from edc_auth.codenames import (
    ae_review,
    account_manager,
    everyone,
    lab,
    lab_view,
    pii,
    pii_view,
    get_rando,
    tmg,
)

from ..codenames import (
    ae,
    auditor,
    clinic,
    screening,
)
from ..codenames_by_group import get_codenames_by_group


class TestPermissions(TestCase):
    @classmethod
    def setUpClass(cls):
        GroupPermissionsUpdater(
            codenames_by_group=get_codenames_by_group(), verbose=True
        )
        return super(TestPermissions, cls).setUpClass()

    def test_pii(self):
        # update_permissions()
        # show_permissions_for_group(group_name=PII)
        compare_codenames_for_group(group_name=PII, expected=pii)
        # show_permissions_for_group(group_name=PII_VIEW)
        compare_codenames_for_group(group_name=PII_VIEW, expected=pii_view)

    @tag("1")
    def test_ae(self):
        # update_permissions()
        compare_codenames_for_group(group_name=AE, expected=ae)

    def test_ae_review(self):
        # update_permissions()
        compare_codenames_for_group(group_name=AE_REVIEW, expected=ae_review)

    def test_screening(self):
        # update_permissions()
        compare_codenames_for_group(group_name=SCREENING, expected=screening)

    def test_everyone(self):
        # update_permissions()
        compare_codenames_for_group(group_name=EVERYONE, expected=everyone)

    def test_auditors(self):
        # update_permissions()
        compare_codenames_for_group(group_name=AUDITOR, expected=auditor)

    def test_account_manager(self):
        # update_permissions()
        compare_codenames_for_group(
            group_name=ACCOUNT_MANAGER, expected=account_manager
        )

    @tag("1")
    def test_clinic(self):
        # update_permissions()
        compare_codenames_for_group(group_name=CLINIC, expected=clinic)

    def test_rando(self):
        # update_permissions()
        compare_codenames_for_group(group_name=RANDO, expected=get_rando())

    def test_lab(self):
        # update_permissions()
        compare_codenames_for_group(group_name=LAB, expected=lab)
        compare_codenames_for_group(group_name=LAB_VIEW, expected=lab_view)

    def test_tmg(self):
        # update_permissions()
        compare_codenames_for_group(group_name=TMG, expected=tmg)
