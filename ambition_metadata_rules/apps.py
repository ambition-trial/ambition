from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = "ambition_metadata_rules"


if settings.APP_NAME == "ambition_metadata_rules":
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_metadata.apps import AppConfig as MetadataAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig

    class EdcMetadataAppConfig(MetadataAppConfig):
        reason_field = {"ambition_metadata_rules.subjectvisit": "reason"}

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
