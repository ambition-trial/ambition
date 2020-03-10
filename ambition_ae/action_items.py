from ambition_subject.constants import BLOOD_RESULTS_ACTION
from edc_action_item import ActionWithNotification, site_action_items
from edc_adverse_event.action_items import (
    AeFollowupAction,
    AeInitialAction,
    AeSusarAction,
    AeTmgAction,
    DeathReportAction,
    DeathReportTmgAction,
    DeathReportTmgSecondAction,
)
from edc_adverse_event.constants import AE_INITIAL_ACTION
from edc_constants.constants import HIGH_PRIORITY, YES

from .constants import RECURRENCE_OF_SYMPTOMS_ACTION


class AeInitialAction(AeInitialAction):
    parent_action_names = [BLOOD_RESULTS_ACTION]

    def get_next_actions(self):
        next_actions = super().get_next_actions()
        # add next Recurrence of Symptoms if YES
        next_actions = self.append_to_next_if_required(
            next_actions=next_actions,
            action_name=RECURRENCE_OF_SYMPTOMS_ACTION,
            required=self.reference_obj.ae_cm_recurrence == YES,
        )
        return next_actions


class RecurrenceOfSymptomsAction(ActionWithNotification):
    name = RECURRENCE_OF_SYMPTOMS_ACTION
    display_name = "Submit Recurrence of Symptoms Report"
    notification_display_name = "Recurrence of Symptoms Report"
    parent_action_names = [AE_INITIAL_ACTION]
    reference_model = "ambition_ae.recurrencesymptom"
    show_link_to_changelist = True
    admin_site_name = "ambition_ae_admin"
    priority = HIGH_PRIORITY
    create_by_user = False
    help_text = "This document is triggered by AE Initial"


site_action_items.register(AeFollowupAction)
site_action_items.register(AeInitialAction)
site_action_items.register(AeSusarAction)
site_action_items.register(AeTmgAction)
site_action_items.register(DeathReportAction)
site_action_items.register(DeathReportTmgAction)
site_action_items.register(DeathReportTmgSecondAction)
site_action_items.register(RecurrenceOfSymptomsAction)
