from ambition_prn.form_validators import StudyDayFormValidatorMixin
from edc_adverse_event.form_validators import DeathReportFormValidator as FormValidator
from edc_constants.constants import TUBERCULOSIS


class DeathReportFormValidator(StudyDayFormValidatorMixin, FormValidator):
    def clean(self):

        super().clean()

        self.validate_study_day_with_datetime(
            study_day=self.cleaned_data.get("study_day"),
            compare_date=self.cleaned_data.get("death_datetime"),
            study_day_field="study_day",
        )

        tb = self.cause_of_death_model_cls.objects.get(name=TUBERCULOSIS)
        self.required_if(tb.name, field="cause_of_death", field_required="tb_site")
