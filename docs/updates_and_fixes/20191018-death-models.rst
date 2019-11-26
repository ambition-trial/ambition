

from edc_registration.models import RegisteredSubject
from edc_constants.constants import CANCELLED
from edc_action_item.models import ActionItem
from edc_adverse_event.constants import (
    DEATH_REPORT_ACTION, DEATH_REPORT_TMG_ACTION, DEATH_REPORT_TMG_SECOND_ACTION,
    AE_INITIAL_ACTION,
    AE_FOLLOWUP_ACTION,
)

from ambition_ae.models import AeFollowup

ActionItem.objects.filter(
    reference_model="ambition_prn.deathreport").update(
        reference_model="ambition_ae.deathreport")

ActionItem.objects.filter(
    reference_model="ambition_prn.deathreporttmg").update(
        reference_model="ambition_ae.deathreporttmg")        

for obj in ActionItem.objects.filter(action_type__name=DEATH_REPORT_ACTION):
    obj.save()        

for obj in ActionItem.objects.filter(action_type__name=DEATH_REPORT_TMG_ACTION):
    obj.save()    

for obj in ActionItem.objects.filter(action_type__name=AE_INITIAL_ACTION):
    obj.save()        

for obj in ActionItem.objects.filter(action_type__name=AE_FOLLOWUP_ACTION):
    obj.save()            


for obj in ActionItem.objects.filter(status=CANCELLED):
    obj.delete()

RegisteredSubject.objects.all().update(randomization_list_model="ambition_rando.randomizationlist")


SET FOREIGN_KEY_CHECKS=0;
SET FOREIGN_KEY_CHECKS=1;

update .env
------------

Delete::
    
    DJANGO_RANDOMIZATIONLIST_FILE= ...

Add::

    EDC_RANDOMIZATION_LIST_FILE=test_randomization_list.csv
    EDC_RANDOMIZATION_LIST_MODEL=ambition_rando.randomizationlist
    EDC_RANDOMIZATION_BLINDED_TRIAL=True
    EDC_RANDOMIZATION_UNBLINDED_USERS=erikvw
