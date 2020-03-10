from django.db import models


class DeathReport(models.Model):

    cause_of_death = models.CharField(max_length=50)
