from django.apps import AppConfig as DjangoApponfig
from django.conf import settings
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig


class AppConfig(DjangoApponfig):
    name = "ambition_screening"
    verbose_name = "Ambition Subject Screening"
    screening_age_adult_upper = 99
    screening_age_adult_lower = 18
    include_in_administration_section = True
    has_exportable_data = True


if settings.APP_NAME == "ambition_screening":

    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

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
