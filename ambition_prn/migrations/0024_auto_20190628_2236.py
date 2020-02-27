# Generated by Django 2.2.2 on 2019-06-28 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0023_auto_20190628_2151")]

    operations = [
        migrations.AddIndex(
            model_name="deathreport",
            index=models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"],
                name="ambition_pr_subject_2d450e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="deathreporttmg",
            index=models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"],
                name="ambition_pr_subject_732cea_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="protocoldeviationviolation",
            index=models.Index(
                fields=["subject_identifier", "action_identifier", "site", "id"],
                name="ambition_pr_subject_2ee369_idx",
            ),
        ),
    ]
