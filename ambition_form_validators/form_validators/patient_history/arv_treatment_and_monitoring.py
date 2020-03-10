from django import forms
from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, UNKNOWN
from edc_form_validators import FormValidator
from edc_registration import get_registered_subject


class ArvTreatmentAndMonitoringFormValidatorMixin(FormValidator):
    def validate_arv_treatment_and_monitoring(self):
        self.applicable_if(NO, field="new_hiv_diagnosis", field_applicable="taking_arv")

        self.validate_initial_arv_date()

        self.validate_initial_arv_regimen()

        self.applicable_if(
            YES, field="taking_arv", field_applicable="has_switched_regimen"
        )

        self.validate_current_arv_date()

        self.validate_current_arv_regimen()

        self.applicable_if(
            YES, field="taking_arv", field_applicable="current_arv_is_defaulted"
        )

        self.validate_current_arv_defaulted_date()

        self.applicable_if(
            NO,
            field="current_arv_is_defaulted",
            field_applicable="current_arv_is_adherent",
        )

        self.required_if(
            NO,
            field="current_arv_is_adherent",
            field_required="current_arv_tablets_missed",
        )

        self.applicable_if(
            YES, field="taking_arv", field_applicable="current_arv_decision"
        )

        self.validate_cd4_vl()

    def validate_cd4_vl(self):
        self.not_required_if(
            None, field="last_viral_load", field_required="viral_load_date"
        )

        self.not_required_if(
            None, field="viral_load_date", field_required="vl_date_estimated"
        )

        self.not_required_if(None, field="last_cd4", field_required="cd4_date")

        self.not_required_if(
            None, field="cd4_date", field_required="cd4_date_estimated"
        )

    def validate_initial_arv_regimen(self):

        self.m2m_single_selection_if(
            NOT_APPLICABLE, UNKNOWN, m2m_field="initial_arv_regimen"
        )

        self.m2m_applicable_if(YES, field="taking_arv", m2m_field="initial_arv_regimen")

        self.m2m_other_specify(
            OTHER,
            m2m_field="initial_arv_regimen",
            field_other="initial_arv_regimen_other",
        )

    def validate_current_arv_regimen(self):

        self.m2m_single_selection_if(
            NOT_APPLICABLE, UNKNOWN, m2m_field="current_arv_regimen"
        )

        self.m2m_selections_not_expected(UNKNOWN, m2m_field="current_arv_regimen")

        self.m2m_applicable_if(
            YES, field="has_switched_regimen", m2m_field="current_arv_regimen"
        )

        self.m2m_other_specify(
            OTHER,
            m2m_field="current_arv_regimen",
            field_other="current_arv_regimen_other",
        )

    def validate_initial_arv_date(self):
        self.required_if(YES, field="taking_arv", field_required="initial_arv_date")

        if self.cleaned_data.get("taking_arv") == YES:
            try:
                days = (
                    self.cleaned_data.get("initial_arv_date")
                    - self.cleaned_data.get("report_datetime").date()
                ).days
            except TypeError:
                pass
            else:
                if days > 0:
                    raise forms.ValidationError(
                        {"initial_arv_date": "Date cannot be after the report date."}
                    )

            registered_subject = get_registered_subject(
                self.cleaned_data.get("subject_visit").subject_identifier
            )
            try:
                days = (
                    self.cleaned_data.get("initial_arv_date") - registered_subject.dob
                ).days
            except TypeError:
                pass
            else:
                if days < 0:
                    raise forms.ValidationError(
                        {
                            "initial_arv_date": (
                                "Date cannot be before subject's date of birth."
                            )
                        }
                    )

        self.not_applicable(
            None,
            field="initial_arv_date",
            field_applicable="initial_arv_date_estimated",
        )

    def validate_current_arv_date(self):
        self.required_if(
            YES, field="has_switched_regimen", field_required="current_arv_date"
        )

        if self.cleaned_data.get("has_switched_regimen") == YES:
            try:
                days = (
                    self.cleaned_data.get("current_arv_date")
                    - self.cleaned_data.get("initial_arv_date")
                ).days
            except TypeError:
                pass
            else:
                if days == 0:
                    raise forms.ValidationError(
                        {
                            "current_arv_date": (
                                "Date cannot equal to the initial ARV date."
                            )
                        }
                    )
                elif days < 0:
                    raise forms.ValidationError(
                        {
                            "current_arv_date": (
                                "Date cannot be before the initial ARV date."
                            )
                        }
                    )
        self.not_applicable(
            None,
            field="current_arv_date",
            field_applicable="current_arv_date_estimated",
        )

    def validate_current_arv_defaulted_date(self):
        self.required_if(
            YES,
            field="current_arv_is_defaulted",
            field_required="current_arv_defaulted_date",
        )
        if self.cleaned_data.get("current_arv_is_defaulted") == YES:
            try:
                days = (
                    self.cleaned_data.get("current_arv_defaulted_date")
                    - self.cleaned_data.get("initial_arv_date")
                ).days
            except TypeError:
                pass
            else:
                if days == 0:
                    raise forms.ValidationError(
                        {
                            "current_arv_defaulted_date": (
                                "Date cannot equal to the initial ARV date."
                            )
                        }
                    )
                elif days < 0:
                    raise forms.ValidationError(
                        {
                            "current_arv_defaulted_date": (
                                "Date cannot be before the initial ARV date."
                            )
                        }
                    )
        self.not_applicable(
            None,
            field="current_arv_defaulted_date",
            field_applicable="current_arv_defaulted_date_estimated",
        )
