# Generated by Django 2.0.7 on 2018-07-08 07:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0010_auto_20180512_1248")]

    operations = [
        migrations.RenameField(
            model_name="bloodresult",
            old_name="parent_tracking_identifier",
            new_name="parent_reference_identifier",
        ),
        migrations.RenameField(
            model_name="bloodresult",
            old_name="related_tracking_identifier",
            new_name="related_reference_identifier",
        ),
        migrations.RenameField(
            model_name="historicalbloodresult",
            old_name="parent_tracking_identifier",
            new_name="parent_reference_identifier",
        ),
        migrations.RenameField(
            model_name="historicalbloodresult",
            old_name="related_tracking_identifier",
            new_name="related_reference_identifier",
        ),
        migrations.RenameField(
            model_name="historicalsubjectreconsent",
            old_name="parent_tracking_identifier",
            new_name="parent_reference_identifier",
        ),
        migrations.RenameField(
            model_name="historicalsubjectreconsent",
            old_name="related_tracking_identifier",
            new_name="related_reference_identifier",
        ),
        migrations.RenameField(
            model_name="subjectreconsent",
            old_name="parent_tracking_identifier",
            new_name="parent_reference_identifier",
        ),
        migrations.RenameField(
            model_name="subjectreconsent",
            old_name="related_tracking_identifier",
            new_name="related_reference_identifier",
        ),
    ]
