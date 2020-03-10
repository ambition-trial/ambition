from edc_adverse_event.constants import AE_INITIAL_ACTION
from ambition_prn.constants import STUDY_TERMINATION_CONCLUSION_ACTION
from ambition_screening import EarlyWithdrawalEvaluator
from ambition_visit_schedule import DAY1
from edc_action_item import Action, site_action_items
from edc_constants.constants import YES, HIGH_PRIORITY

from .constants import BLOOD_RESULTS_ACTION, RECONSENT_ACTION


class BloodResultAction(Action):
    name = BLOOD_RESULTS_ACTION
    display_name = "Reportable Blood Result"
    reference_model = "ambition_subject.bloodresult"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    create_by_user = False

    def reopen_action_item_on_change(self):
        return False

    def get_next_actions(self):
        next_actions = []
        if (
            self.reference_obj.subject_visit.visit_code == DAY1
            and self.reference_obj.subject_visit.visit_code_sequence == 0
        ):
            # early withdrawal if qualifying blood results
            # are abnormal on DAY1.0
            evaluator = EarlyWithdrawalEvaluator(
                subject_identifier=self.reference_obj.subject_identifier,
                allow_none=True,
            )
            if not evaluator.eligible:
                next_actions = [STUDY_TERMINATION_CONCLUSION_ACTION]
        elif (
            self.reference_obj.results_abnormal == YES
            and self.reference_obj.results_reportable == YES
        ):
            # AE for reportable result, though not on DAY1.0
            next_actions = [AE_INITIAL_ACTION]
        return next_actions


class ReconsentAction(Action):
    name = RECONSENT_ACTION
    display_name = "Re-consent participant"
    reference_model = "ambition_subject.subjectreconsent"
    priority = HIGH_PRIORITY
    show_on_dashboard = True
    show_link_to_changelist = True
    admin_site_name = "ambition_subject_admin"
    create_by_user = False
    singleton = True
    instructions = (
        "Participant must be re-consented as soon as able. "
        "Participant's ICF was initially completed by next-of-kin."
    )

    def reopen_action_item_on_change(self):
        return False


site_action_items.register(BloodResultAction)
site_action_items.register(ReconsentAction)
