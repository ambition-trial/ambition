from django.apps import AppConfig as DjangoApponfig
from django.conf import settings


class AppConfig(DjangoApponfig):
    name = "ambition_ae"
    verbose_name = "Ambition Adverse Events"
    has_exportable_data = True
    include_in_administration_section = True


if settings.APP_NAME == "ambition_ae":

    from datetime import datetime
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from dateutil.tz.tz import gettz
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig

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

    class EdcLabAppConfig(BaseEdcLabAppConfig):
        base_template_name = f"ambition/bootstrap{settings.EDC_BOOTSTRAP}/base.html"
        result_model = "edc_lab.result"

        @property
        def site_name(self):
            return "Gaborone"

        @property
        def site_code(self):
            return "40"
