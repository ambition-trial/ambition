from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import BaseUuidModel


class SubjectVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)


class Week2(BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)
