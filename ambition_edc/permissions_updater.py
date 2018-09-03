from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import ObjectDoesNotExist
from edc_permissions.permissions_updater import CLINIC, LAB, AUDITOR, ADMINISTRATION, PII
from edc_permissions.permissions_updater import PermissionsUpdater as EdcPermissionsUpdater


RANDO = 'RANDO'
TMG = 'TMG'


class PermissionsUpdater(EdcPermissionsUpdater):

    group_names = [RANDO, TMG]

    pii_models = [
        'edc_locator.subjectconsent',
        'ambition_subject.subjectreconsent',
        'ambition_screening.subjectscreening']
    auditor_app_labels = [
        'ambition_ae',
        'ambition_screening',
        'ambition_subject',
        'ambition_prn',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ensure in ADMINITRATION group
        administration_group = Group.objects.get(name=ADMINISTRATION)
        for user in User.objects.filter(groups__name__in=[CLINIC, LAB, TMG]):
            try:
                user.groups.get(name=administration_group.name)
            except ObjectDoesNotExist:
                user.groups.add(administration_group)
        # ensure in PII group
        pii_group = Group.objects.get(name=PII)
        for user in User.objects.filter(groups__name__in=[CLINIC, LAB]):
            try:
                user.groups.get(name=pii_group.name)
            except ObjectDoesNotExist:
                user.groups.add(pii_group)
        # ensure NOT in PII group
        for user in User.objects.filter(groups__name__in=[TMG, AUDITOR]):
            try:
                user.groups.get(name=pii_group.name)
            except ObjectDoesNotExist:
                pass
            else:
                user.groups.remove(pii_group)
        # ensure NOT in RANDO group
        rando_group = Group.objects.get(name=RANDO)
        for user in User.objects.filter(groups__name__in=[TMG, AUDITOR]):
            try:
                user.groups.get(name=rando_group.name)
            except ObjectDoesNotExist:
                pass
            else:
                user.groups.remove(rando_group)

    def extra_lab_group_permissions(self, group):
        permission = Permission.objects.get(
            content_type__app_label='ambition_subject',
            content_type__model='subjectrequisition',
            codename__startswith='view')
        group.permissions.add(permission)
        self.add_navbar_permissions(
            group=group, codenames=['nav_subject_section'])

    def extra_clinic_group_permissions(self, group):
        exclude_models = [
            m.split('.')[1] for m in self.pii_models] + ['aetmg', 'deathreporttmg']
        for permission in Permission.objects.filter(content_type__app_label__in=[
                'ambition_ae', 'ambition_prn', 'ambition_subject',
                'edc_offstudy']).exclude(
                    content_type__model__in=exclude_models):
            group.permissions.add(permission)
        group.permissions.filter(
            codename__in=['historicalaetmg',
                          'historicaldeathreporttmg',
                          'historicalsubjectconsent',
                          'historicalsubjectreconsent']).delete()
        group.permissions.filter(codename__contains='historical').exclude(
            codename__startswith='view').delete()
        group.permissions.filter(
            codename__in=['view_historicalaetmg',
                          'view_historicaldeathreporttmg',
                          'view_historicalsubjectconsent',
                          'view_historicalsubjectreconsent']).delete()
        # allow CLINIC users to view AeTmg
        for permission in Permission.objects.filter(
                content_type__app_label__in=['ambition_ae'],
                content_type__model__in=['aetmg'],
                codename__startswith='view'):
            group.permissions.add(permission)
        self.add_navbar_permissions(
            group=group, codenames=[
                'nav_subject_section', 'nav_screening_section'])

    def update_tmg_group_permissions(self):
        group_name = TMG
        group = Group.objects.get(name=group_name)
        group.permissions.clear()
        for permission in Permission.objects.filter(
                content_type__app_label__in=['edc_action_item']):
            group.permissions.add(permission)
        for permission in Permission.objects.filter(
                content_type__app_label__in=['ambition_ae'],
                content_type__model__in=['aetmg']):
            group.permissions.add(permission)
        for permission in Permission.objects.filter(
                content_type__app_label__in=['ambition_ae'],
                codename__startswith='view'):
            group.permissions.add(permission)
        for permission in Permission.objects.filter(
                content_type__app_label__in=['ambition_prn'],
                content_type__model__in=['deathreporttmg']):
            group.permissions.add(permission)
        Permission.objects.get(
            content_type__app_label='edc_navbar',
            codename='nav_tmg_section')
        group.permissions.add(permission)
        self.add_navbar_permissions(
            group=group, codenames=['nav_tmg_section'])

    def update_rando_group_permissions(self):
        group_name = RANDO
        group = Group.objects.get(name=group_name)
        group.permissions.clear()
        for permission in Permission.objects.filter(
                content_type__app_label='ambition_rando',
                codename='ambition_rando.view_randomizationlist'):
            group.permissions.add(permission)
        permission = Permission.objects.get(
            content_type__app_label='ambition_rando',
            codename='display_randomization')
        group.permissions.add(permission)
