from django.apps import AppConfig as DjangoApponfig
from django.conf import settings
from django.core.management.color import color_style

style = color_style()


class AppConfig(DjangoApponfig):
    name = "ambition_subject"
    verbose_name = "Ambition Subject CRFs"
    admin_site_name = "ambition_subject_admin"
    has_exportable_data = True
    include_in_administration_section = True

    def ready(self):
        from .models.signals import subject_consent_on_post_save  # noqa


if settings.APP_NAME == "ambition_subject":

    from datetime import datetime
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from dateutil.tz import gettz
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
    from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    from edc_visit_tracking.constants import MISSED_VISIT
    from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = "BHP092"
        protocol_number = "092"
        protocol_name = "Ambition"
        protocol_title = ""
        year = datetime.now().year
        study_open_datetime = datetime(year, 1, 1, 0, 0, 0, tzinfo=gettz("UTC"))
        study_close_datetime = datetime(
            year + 5, 12, 31, 23, 59, 59, tzinfo=gettz("UTC")
        )

    class EdcLabAppConfig(BaseEdcLabAppConfig):
        base_template_name = f"ambition/bootstrap{settings.EDC_BOOTSTRAP}/base.html"
        result_model = "edc_lab.result"

        @property
        def site_name(self):
            return "Gaborone"

        @property
        def site_code(self):
            return "40"

    class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
        identifier_prefix = "092"

    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {"ambition_subject.subjectvisit": "reason"}
        create_on_reasons = [SCHEDULED, UNSCHEDULED]
        delete_on_reasons = [MISSED_VISIT]

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        default_appt_type = "hospital"
        configurations = [
            AppointmentConfig(
                model="edc_appointment.appointment",
                related_visit_model="ambition_subject.subjectvisit",
            )
        ]

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = "botswana"
        definitions = {
            "7-day clinic": dict(
                days=[MO, TU, WE, TH, FR, SA, SU],
                slots=[100, 100, 100, 100, 100, 100, 100],
            ),
            "5-day clinic": dict(
                days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]
            ),
        }
