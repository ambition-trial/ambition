from ambition_rando.constants import SINGLE_DOSE, CONTROL
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_adverse_event.form_validators import ValidateDeathReportMixin
from edc_constants.constants import DEAD, NONE, OTHER
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from edc_randomization.utils import get_randomizationlist_model

from ..constants import CONSENT_WITHDRAWAL
from edc_randomization.site_randomizers import site_randomizers


class StudyTerminationConclusionFormValidator(ValidateDeathReportMixin, FormValidator):

    week2_model = "ambition_subject.week2"
    randomizer_name = "ambition"

    def clean(self):

        self.validate_death_report_if_deceased()

        self.required_if(
            YES,
            field="discharged_after_initial_admission",
            field_required="initial_discharge_date",
        )

        self.applicable_if(
            YES,
            field="discharged_after_initial_admission",
            field_applicable="readmission_after_initial_discharge",
        )

        self.required_if(
            YES,
            field="readmission_after_initial_discharge",
            field_required="readmission_date",
        )

        self.required_if(DEAD, field="termination_reason", field_required="death_date")

        self.required_if(
            CONSENT_WITHDRAWAL,
            field="termination_reason",
            field_required="consent_withdrawal_reason",
        )

        self.applicable_if(
            CONSENT_WITHDRAWAL,
            field="termination_reason",
            field_applicable="willing_to_complete_10w",
        )

        self.applicable_if(
            "care_transferred_to_another_institution",
            field="termination_reason",
            field_applicable="willing_to_complete_centre",
        )

        self.required_if_true(
            condition=(
                self.cleaned_data.get("willing_to_complete_10w") == YES
                or self.cleaned_data.get("willing_to_complete_centre") == YES
            ),
            field_required="willing_to_complete_date",
        )

        self.applicable_if(
            "late_exclusion_criteria_met",
            field="termination_reason",
            field_applicable="protocol_exclusion_criterion",
        )

        self.required_if(
            "included_in_error",
            field="termination_reason",
            field_required="included_in_error",
        )

        self.required_if(
            "included_in_error",
            field="termination_reason",
            field_required="included_in_error_date",
        )

        self.validate_other_specify(field="first_line_regimen")

        self.validate_other_specify(field="second_line_regimen")

        self.not_applicable_if(
            NOT_APPLICABLE,
            field="first_line_regimen",
            field_applicable="first_line_choice",
        )

        # redmine # 117
        arvs_switch_date = self.cleaned_data.get("arvs_switch_date")
        first_line_regimen = self.cleaned_data.get("first_line_regimen")
        first_line_choice = self.cleaned_data.get("first_line_choice")
        second_line_regimen = self.cleaned_data.get("second_line_regimen")
        if (
            (first_line_regimen and first_line_regimen != NOT_APPLICABLE)
            or (first_line_choice and first_line_choice != NOT_APPLICABLE)
            or (second_line_regimen and second_line_regimen != NOT_APPLICABLE)
        ):
            if not arvs_switch_date:
                raise forms.ValidationError(
                    {"arvs_switch_date": "This field is required."}
                )
        offschedule_datetime = self.cleaned_data.get("offschedule_datetime")
        if arvs_switch_date and offschedule_datetime:
            if arvs_switch_date > offschedule_datetime.date():
                raise forms.ValidationError(
                    {
                        "arvs_switch_date": (
                            "May not be after date patient terminated on study."
                        )
                    }
                )

        self.applicable_if_true(
            not self.completed_week2,
            field_applicable="on_study_drug",
            applicable_msg="Week 2 is not complete.",
            not_applicable_msg="Week 2 is complete.",
        )

        # self.validate_study_drug_start_stop_dates_after_wk2()

        if self.cleaned_data.get("on_study_drug") == YES:
            self.require_study_drug_start_and_stop_dates_by_arm()
            self.require_together_study_drug_start_and_stop_date()
        else:
            self.not_required_study_drug_start_stop_dates()

        if self.completed_week2:
            self.m2m_selection_expected(
                NOT_APPLICABLE,
                m2m_field="drug_intervention",
                error_msg='Week two complete. Select "Not Applicable" only.',
            )
            self.m2m_selection_expected(
                NOT_APPLICABLE,
                m2m_field="medicines",
                error_msg='Week two complete. Select "Not Applicable" only.',
            )
        else:
            self.m2m_selections_not_expected(
                NOT_APPLICABLE,
                m2m_field="drug_intervention",
                error_msg=(
                    "Week two not complete, selection " '"Not Applicable" is invalid.'
                ),
            )
            self.m2m_selections_not_expected(
                NOT_APPLICABLE,
                m2m_field="medicines",
                error_msg=(
                    "Week two not complete, selection " '"Not Applicable" is invalid.'
                ),
            )

        self.m2m_single_selection_if(NONE, m2m_field="drug_intervention")

        self.m2m_other_specify(
            "antibiotics", m2m_field="drug_intervention", field_other="antibiotic"
        )

        self.m2m_other_specify(
            OTHER, m2m_field="drug_intervention", field_other="drug_intervention_other"
        )

        self.m2m_other_specify(
            OTHER, m2m_field="antibiotic", field_other="antibiotic_other"
        )

        self.m2m_single_selection_if(NONE, m2m_field="medicines")

        self.m2m_other_specify(
            OTHER, m2m_field="medicines", field_other="medicine_other"
        )

        self.required_if(YES, field="blood_received", field_required="units")

    def not_required_study_drug_start_stop_dates(self):
        fields = [
            "ampho_start_date",
            "ampho_stop_date",
            "flucon_start_date",
            "flucon_stop_date",
            "flucy_start_date",
            "flucy_stop_date",
            "ambi_start_date",
            "ambi_stop_date",
        ]
        for fld in fields:
            self.not_required_if(
                NO, NOT_APPLICABLE, field="on_study_drug", field_required=fld
            )

    def require_study_drug_start_and_stop_dates_by_arm(self):
        """Raise if on drug but dates not provided.

        See PART 3 in Admin
        """

        if self.cleaned_data.get("on_study_drug") == YES:
            self.required_if_true(
                self.assignment == CONTROL, field_required="ampho_start_date"
            )

            self.required_if_true(
                self.assignment == CONTROL, field_required="ampho_stop_date"
            )
            self.required_if_true(
                self.assignment == SINGLE_DOSE, field_required="ambi_start_date"
            )

            self.required_if_true(
                self.assignment == SINGLE_DOSE, field_required="ambi_stop_date"
            )

    def require_together_study_drug_start_and_stop_date(self):
        self.require_together("ampho_start_date", "ampho_stop_date")
        self.require_together("flucon_start_date", "flucon_stop_date")
        self.require_together("flucy_start_date", "flucy_stop_date")
        self.require_together("ambi_start_date", "ambi_stop_date")

    @property
    def week2_model_cls(self):
        return django_apps.get_model(self.week2_model)

    @property
    def completed_week2(self):
        """Returns True if subject has completed week2 form.
        """
        subject_identifier = self.cleaned_data.get("subject_identifier")
        try:
            completed_week2 = self.week2_model_cls.objects.get(
                subject_visit__subject_identifier=subject_identifier
            )
        except ObjectDoesNotExist:
            completed_week2 = False
        return completed_week2

    @property
    def assignment(self):
        RandomizationList = get_randomizationlist_model()
        subject_identifier = self.cleaned_data.get("subject_identifier")
        obj = RandomizationList.objects.get(subject_identifier=subject_identifier)
        return site_randomizers.get(self.randomizer_name).get_assignment(
            {"assignment": obj.assignment}
        )
