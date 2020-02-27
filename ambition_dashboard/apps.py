from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from datetime import datetime
from dateutil.tz.tz import gettz


class AppConfig(DjangoAppConfig):
    name = "ambition_dashboard"
    admin_site_name = "ambition_test_admin"
    include_in_administration_section = False


if settings.APP_NAME == "ambition_dashboard":

    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = "BHP092"
        protocol_name = "Ambition"
        protocol_number = "092"
        protocol_title = ""
        study_open_datetime = datetime(2016, 12, 31, 0, 0, 0, tzinfo=gettz("UTC"))
        study_close_datetime = datetime(2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC"))

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
                days=[MO, TU, WE, TH, FR, SA, SU],
                slots=[100, 100, 100, 100, 100, 100, 100],
            ),
            "5-day clinic": dict(
                days=[MO, TU, WE, TH, FR], slots=[100, 100, 100, 100, 100]
            ),
        }

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            "ambition_subject": ("subject_visit", "ambition_subject.subjectvisit")
        }

    class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
        identifier_prefix = "092"

    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {"ambition_subject.subjectvisit": "reason"}
