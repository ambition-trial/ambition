from django.contrib.auth.models import Group, Permission
from edc_permissions.permissions_updater import (
    PermissionsUpdater as EdcPermissionsUpdater)


class PermissionsUpdater(EdcPermissionsUpdater):

    group_names = [
        'CLINIC',
        'RANDO',
        'TMG']
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

    def extra_lab_group_permissions(self, group):
        permission = Permission.objects.get(
            content_type__app_label='ambition_subject',
            content_type__model='subjectrequisition',
            codename__startswith='view')
        group.permissions.add(permission)

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

    def update_tmg_group_permissions(self):
        group_name = 'TMG'
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

    def update_rando_group_permissions(self):
        group_name = 'RANDO'
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
