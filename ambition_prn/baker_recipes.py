from edc_constants.constants import NO
from faker import Faker
from model_bakery.recipe import Recipe

from .models import (
    ProtocolDeviationViolation,
    StudyTerminationConclusion,
    StudyTerminationConclusionW10,
)

fake = Faker()

studyterminationconclusion = Recipe(
    StudyTerminationConclusion,
    action_identifier=None,
    tracking_identifier=None,
    protocol_exclusion_criterion=NO,
)

studyterminationconclusionw10 = Recipe(
    StudyTerminationConclusionW10, action_identifier=None, tracking_identifier=None
)

protocoldeviationviolation = Recipe(
    ProtocolDeviationViolation, action_identifier=None, tracking_identifier=None
)
