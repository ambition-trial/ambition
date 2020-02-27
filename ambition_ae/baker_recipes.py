from edc_adverse_event.baker_recipes import causeofdeath
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE
from edc_reportable import GRADE4
from edc_utils import get_utcnow
from faker import Faker
from model_bakery.recipe import Recipe, foreign_key

from .models import AeInitial, AeTmg, AeFollowup, AeSusar
from .models import RecurrenceSymptom, Neurological
from .models import MeningitisSymptom
from .models import DeathReport, DeathReportTmg, DeathReportTmgSecond

fake = Faker()


aeinitial = Recipe(
    AeInitial,
    action_identifier=None,
    tracking_identifier=None,
    ae_description="A description of this event",
    ae_grade=GRADE4,
    ae_study_relation_possibility=YES,
    ae_start_date=get_utcnow().date(),
    ae_awareness_date=get_utcnow().date(),
    fluconazole_relation="not_related",
    flucytosine_relation="not_related",
    amphotericin_relation="not_related",
    ae_treatment="Some special treatment",
    ae_cm_recurrence=NO,
    sae=NO,
    susar=NO,
    susar_reported=NOT_APPLICABLE,
    ae_cause=NO,
    ae_cause_other=None,
)

aetmg = Recipe(AeTmg, action_identifier=None, tracking_identifier=None)

aesusar = Recipe(AeSusar, action_identifier=None, tracking_identifier=None)

aefollowup = Recipe(
    AeFollowup, relevant_history=NO, action_identifier=None, tracking_identifier=None
)

recurrencesymptom = Recipe(
    RecurrenceSymptom, action_identifier=None, tracking_identifier=None
)

meningitissymptom = Recipe(MeningitisSymptom, name=OTHER, display_name="Other")

neurological = Recipe(Neurological, name="meningismus", display_name="Meningismus")


deathreport = Recipe(
    DeathReport,
    study_day=1,
    death_as_inpatient=YES,
    cause_of_death=foreign_key(causeofdeath),
    cause_of_death_other=None,
    action_identifier=None,
    tracking_identifier=None,
)

deathreporttmg = Recipe(
    DeathReportTmg,
    action_identifier=None,
    cause_of_death=foreign_key(causeofdeath),
    cause_of_death_agreed=YES,
    tracking_identifier=None,
)

deathreporttmgsecond = Recipe(
    DeathReportTmgSecond,
    action_identifier=None,
    cause_of_death=foreign_key(causeofdeath),
    cause_of_death_agreed=YES,
    tracking_identifier=None,
)
