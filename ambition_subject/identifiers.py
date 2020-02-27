from edc_identifier.simple_identifier import (
    SimpleUniqueIdentifier,
    SimpleTimestampIdentifier,
)


class AeIdentifier(SimpleUniqueIdentifier):
    random_string_length = 2
    identifier_type = "tracking_identifier"
    template = "AE{device_id}{timestamp}{random_string}"
    identifier_cls = SimpleTimestampIdentifier


class PdIdentifier(SimpleUniqueIdentifier):
    random_string_length = 2
    identifier_type = "pd_identifier"
    template = "PD{device_id}{timestamp}{random_string}"
    identifier_cls = SimpleTimestampIdentifier
