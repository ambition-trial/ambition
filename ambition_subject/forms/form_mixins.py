import arrow

from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.modelform_mixins import SubjectScheduleCrfModelFormMixin
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin

from ..models import SubjectVisit


class SubjectModelFormMixin(
    SiteModelFormMixin,
    FormValidatorMixin,
    SubjectScheduleCrfModelFormMixin,
    VisitTrackingModelFormMixin,
    forms.ModelForm,
):

    visit_model = SubjectVisit


class InlineSubjectModelFormMixin(FormValidatorMixin, forms.ModelForm):

    visit_model = SubjectVisit


class PreviousAppointmentFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_appointment_rdate = None
        self._previous_appointment = None

    @property
    def previous_appointment(self):
        if not self._previous_appointment:
            cleaned_data = self.cleaned_data
            self._previous_appointment = cleaned_data.get(
                "subject_visit"
            ).appointment.previous_by_timepoint
        return self._previous_appointment

    @property
    def previous_appointment_rdate(self):
        """Returns the utc arrow object of appt_datetime of the previous
        appointment

        Usage:
            from django.conf import settings
            rdate.to(settings.TIME_ZONE).date()
            rdate.to(settings.TIME_ZONE).datetime
        """
        if not self._previous_appointment_rdate:
            if self.previous_appointment:
                rdate = arrow.Arrow.fromdatetime(
                    self.previous_appointment.appt_datetime,
                    tzinfo=self.previous_appointment.appt_datetime.tzinfo,
                )
            else:
                rdate = None
            self._previous_appointment_rdate = rdate
        return self._previous_appointment_rdate
