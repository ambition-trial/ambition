from django.db import models
from django.db.models import options
from django.db.models.deletion import PROTECT, CASCADE
from edc_appointment.models import Appointment
from edc_base.model_mixins import ListModelMixin, BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


options.DEFAULT_NAMES = (options.DEFAULT_NAMES + ('consent_model',))


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class Panel(BaseUuidModel):

    name = models.CharField(
        max_length=25)


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)

    dob = models.DateField()


class SubjectVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class SubjectRequisition(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    requisition_datetime = models.DateTimeField(
        default=get_utcnow)

    panel = models.ForeignKey(Panel, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.subject_visit.subject_identifier
        super().save(*args, **kwargs)


class SubjectScreening(BaseUuidModel):

    screening_identifier = models.CharField(max_length=25, unique=True)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    mental_status = models.CharField(
        max_length=10)

    age_in_years = models.IntegerField()


class BloodResult(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    ft_fields = ['creatinine', 'urea', 'sodium',
                 'potassium', 'magnesium', 'alt']
    cbc_fields = ['haemoglobin', 'wbc', 'neutrophil', 'platelets']


class LumbarPunctureCsf(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)


class PatientHistory(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    previous_oi = models.CharField(
        verbose_name='Previous opportunistic infection other than TB?',
        max_length=5,
        choices=YES_NO)

    first_arv_regimen = models.CharField(
        verbose_name='Drug used in first line arv regimen',
        max_length=50)


class TestModel(BaseUuidModel):

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    other_significant_dx = models.CharField(
        verbose_name='Other significant diagnosis since last visit?',
        max_length=5,
        choices=YES_NO_NA)
