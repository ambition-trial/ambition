from ambition_sites import ambition_sites, fqdn
from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.checks import register
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
from edc_appointment.appointment_config import AppointmentConfig
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from .system_checks import ambition_check


style = color_style()


def post_migrate_update_sites(sender=None, **kwargs):
    from edc_base.sites.utils import add_or_update_django_sites
    add_or_update_django_sites(
        apps=django_apps, sites=ambition_sites, fqdn=fqdn, verbose=True)


def post_migrate_update_edc_permissions(sender=None, **kwargs):
    from ambition_auth.permissions_updater import PermissionsUpdater
    PermissionsUpdater(verbose=True)


class AppConfig(DjangoAppConfig):
    name = 'ambition_edc'

    def ready(self):
        from ambition_rando.system_checks import randomization_list_check
        register(randomization_list_check)(['ambition_edc'])
        register(ambition_check)
        post_migrate.connect(post_migrate_update_sites, sender=self)
        post_migrate.connect(post_migrate_update_edc_permissions, sender=self)


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP092'
    protocol_name = 'Ambition'
    protocol_number = '092'
    protocol_title = ''
    study_open_datetime = datetime(
        2016, 12, 31, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(
        2019, 12, 31, 23, 59, 59, tzinfo=gettz('UTC'))


class EdcLabAppConfig(BaseEdcLabAppConfig):
    result_model = 'edc_lab.result'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'Ambition'
    institution = ''
    project_repo = 'https://github.com/ambition-trial'


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = '99'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'ambition_subject': ('subject_visit', 'ambition_subject.subjectvisit')}


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '092'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'ambition_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    configurations = [
        AppointmentConfig(
            model='edc_appointment.appointment',
            related_visit_model='ambition_subject.subjectvisit',
            appt_type='hospital')]


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])}
