import sys

from ambition_sites import ambition_sites, fqdn
from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.checks import register
from django.core.management.color import color_style
from django.db.models.signals import post_migrate
from django_collect_offline.apps import AppConfig as BaseDjangoCollectOfflineAppConfig
from edc_appointment.appointment_config import AppointmentConfig
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig

from .system_checks import ambition_check


style = color_style()


def post_migrate_update_sites(sender=None, **kwargs):
    from edc_sites.utils import add_or_update_django_sites
    sys.stdout.write(
        style.MIGRATE_HEADING("Updating sites:\n")
    )
    add_or_update_django_sites(
        apps=django_apps, sites=ambition_sites, fqdn=fqdn, verbose=True
    )
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


def post_migrate_update_edc_permissions(sender=None, **kwargs):
    from ambition_permissions.updaters import update_permissions
    sys.stdout.write(
        style.MIGRATE_HEADING("Updating permissions:\n")
    )
    update_permissions()
    sys.stdout.write("Done.\n")
    sys.stdout.flush()


class AppConfig(DjangoAppConfig):
    name = "ambition_edc"

    def ready(self):
        from ambition_rando.system_checks import randomization_list_check

        register(randomization_list_check)(["ambition_edc"])
        register(ambition_check)
        post_migrate.connect(post_migrate_update_sites, sender=self)
        post_migrate.connect(post_migrate_update_edc_permissions, sender=self)


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    institution = "London School of Hygiene & Tropical Medicine"
    project_name = "Ambition"
    project_repo = "https://github.com/ambition-trial"
    protocol = "BHP092"
    protocol_name = "Ambition"
    protocol_number = "092"
    protocol_title = (
        "High Dose AMBISOME on a Fluconazole Backbone for Cryptococcal Meningitis "
        "Induction Therapy in sub-Saharan Africa: A Phase 3 Randomised Controlled "
        "Non-Inferiority Trial (P.I. Joe Jarvis)."
    )
    study_open_datetime = datetime(2016, 12, 31, 0, 0, 0, tzinfo=gettz("UTC"))
    study_close_datetime = datetime(
        2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))


class EdcLabAppConfig(BaseEdcLabAppConfig):
    result_model = "edc_lab.result"


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = "99"


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        "ambition_subject": ("subject_visit", "ambition_subject.subjectvisit")
    }


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = "092"


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {"ambition_subject.subjectvisit": "reason"}


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    configurations = [
        AppointmentConfig(
            model="edc_appointment.appointment",
            related_visit_model="ambition_subject.subjectvisit",
            appt_type="hospital",
        )
    ]


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = "botswana"
    definitions = {
        "7-day clinic": dict(
            days=[MO, TU, WE, TH, FR, SA, SU], slots=[
                100, 100, 100, 100, 100, 100, 100]
        ),
        "5-day clinic": dict(
            days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]
        ),
    }


class DjangoCollectOfflineAppConfig(BaseDjangoCollectOfflineAppConfig):
    base_template_name = "edc_dashboard/bootstrap3/base.html"
