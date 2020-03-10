from ambition_visit_schedule import DAY1
from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_constants.constants import YES
from edc_metadata_rules import PredicateCollection


class Predicates(PredicateCollection):

    app_label = "ambition_subject"
    visit_model = f"{app_label}.subjectvisit"

    def datetime_gt_3_months(self, visit=None, field=None):
        values = self.exists(
            reference_name=f"{self.app_label}.patienthistory",
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name=field,
        )
        return (visit.report_datetime - relativedelta(months=3)).date() > (
            values[0] or (visit.report_datetime).date()
        )

    def blood_result_abnormal(self, visit=None):
        values = self.exists(
            reference_name=f"{self.app_label}.bloodresult",
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name="abnormal_results_in_ae_range",
        )
        return values[0] == YES

    def cause_of_death(self, visit=None, cause=None):
        values = self.exists(
            reference_name=f"{self.app_label}.deathreporttmg1",
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name="cause_of_death",
        )
        return not (values[0] == cause)

    def model_field_exists(self, visit=None, model_lower=None, model_field=None):
        values = self.exists(
            reference_name=f"{self.app_label}.{model_lower}",
            subject_identifier=visit.subject_identifier,
            report_datetime=visit.report_datetime,
            field_name=f"{model_field}",
        )
        return values[0] == YES

    def func_require_cd4(self, visit, **kwargs):
        if visit.visit_code == DAY1:
            return self.datetime_gt_3_months(visit=visit, field="cd4_date")
        return False

    def func_require_vl(self, visit, **kwargs):
        if visit.visit_code == DAY1:
            return self.datetime_gt_3_months(visit=visit, field="viral_load_date")
        return False

    def func_require_pkpd_stopcm(self, visit, **kwargs):
        """Required for ALL subjects in Blantyre only.
        """
        # Made available to all subjects instead of just CONTROL
        # subjects. See redmine issue 33

        # removed completely, see Redmine #70
        # site = Site.objects.get_current()
        # return site.name == 'blantyre'
        return False

    def func_require_qpcr_requisition(self, visit, **kwargs):
        site = Site.objects.get_current()
        # return site.name == "blantyre" or site.name == "gaborone"
        return site.name in ["blantyre", "gaborone", "capetown"]
