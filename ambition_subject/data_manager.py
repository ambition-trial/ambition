from ambition_subject.constants import AWAITING_RESULTS
from edc_constants.constants import NOT_DONE, YES, NO
from edc_data_manager.handlers import QueryRuleHandler
from edc_data_manager.site_data_manager import site_data_manager
from edc_data_manager.handlers.handlers import CrfInspectionFailed


class LumbarPunctureQueryRuleHandlerQ13(QueryRuleHandler):

    name = "lumbar_puncture_q13"
    display_name = "Lumbar Puncture (Q13, 15, 21, 23, 24)"
    model_name = "ambition_subject.lumbarpuncturecsf"

    def inspect_model(self):
        """Lumbar Puncture/Cerebrospinal Fluid 13, 15, 21, 23, 24.
        """
        valid = False
        if not self.model_obj:
            raise CrfInspectionFailed()
        if self.get_field_value("csf_culture") == AWAITING_RESULTS:
            raise CrfInspectionFailed("csf_culture")
        elif self.get_field_value("csf_culture") == NOT_DONE:
            valid = True
        elif self.get_field_value("csf_culture") == YES:
            if (
                self.get_field_value("other_csf_culture")
                and self.get_field_value("csf_wbc_cell_count")
                and self.get_field_value("csf_glucose")
                and self.get_field_value("csf_protein")
                and (
                    self.get_field_value("csf_cr_ag")
                    or self.get_field_value("india_ink")
                )
            ):
                valid = True
        elif self.get_field_value("csf_culture") == NO:
            if (
                self.get_field_value("csf_wbc_cell_count")
                and self.get_field_value("csf_glucose")
                and self.get_field_value("csf_protein")
                and (
                    self.get_field_value("csf_cr_ag")
                    or self.get_field_value("india_ink")
                )
            ):
                valid = True
        if not valid:
            raise CrfInspectionFailed()


site_data_manager.register(LumbarPunctureQueryRuleHandlerQ13)
