# Generated by Django 2.1.4 on 2019-01-30 20:50

from django.db import migrations, models
import edc_model.validators.date
import edc_utils
import edc_model_fields.fields.other_charfield
import edc_protocol.validators


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0040_auto_20190114_0250")]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled visit"),
                    ("unscheduled", "Unscheduled visit"),
                    ("missed", "Missed visit"),
                ],
                max_length=25,
                verbose_name="What is the reason for this visit report?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason_missed",
            field=models.CharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'missed', provide the reason for the missed visit",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason_missed_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=25,
                null=True,
                verbose_name='If the reason for the missed visit is "other", specify',
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason_unscheduled",
            field=models.CharField(
                choices=[
                    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
                    ("recurrence_symptoms", "Recurrence of symptoms"),
                    ("raised_icp_management", "Raised ICP management"),
                    ("art_initiation", "ART initiation"),
                    ("patient_hospitalised", "Patient hospitalised"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="reason_unscheduled_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=25,
                null=True,
                verbose_name='If the reason for the unscheduled visit is "other", specify',
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectvisit",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                help_text="Date and time of this report",
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Report date and time",
            ),
        ),
        migrations.AlterField(
            model_name="historicalweek16",
            name="death_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="removed version 0.1.74",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If dead, date and time of death",
            ),
        ),
        migrations.AlterField(
            model_name="historicalweek16",
            name="patient_alive",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                max_length=5,
                verbose_name="Is the patient alive?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason",
            field=models.CharField(
                choices=[
                    ("scheduled", "Scheduled visit"),
                    ("unscheduled", "Unscheduled visit"),
                    ("missed", "Missed visit"),
                ],
                max_length=25,
                verbose_name="What is the reason for this visit report?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason_missed",
            field=models.CharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'missed', provide the reason for the missed visit",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason_missed_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=25,
                null=True,
                verbose_name='If the reason for the missed visit is "other", specify',
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason_unscheduled",
            field=models.CharField(
                choices=[
                    ("patient_unwell_outpatient", "Patient unwell (outpatient)"),
                    ("recurrence_symptoms", "Recurrence of symptoms"),
                    ("raised_icp_management", "Raised ICP management"),
                    ("art_initiation", "ART initiation"),
                    ("patient_hospitalised", "Patient hospitalised"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="reason_unscheduled_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=25,
                null=True,
                verbose_name='If the reason for the unscheduled visit is "other", specify',
            ),
        ),
        migrations.AlterField(
            model_name="subjectvisit",
            name="report_datetime",
            field=models.DateTimeField(
                default=edc_utils.date.get_utcnow,
                help_text="Date and time of this report",
                validators=[
                    edc_protocol.validators.datetime_not_before_study_start,
                    edc_model.validators.date.datetime_not_future,
                ],
                verbose_name="Report date and time",
            ),
        ),
        migrations.AlterField(
            model_name="week16",
            name="death_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="removed version 0.1.74",
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If dead, date and time of death",
            ),
        ),
        migrations.AlterField(
            model_name="week16",
            name="patient_alive",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("unknown", "Unknown")],
                max_length=5,
                verbose_name="Is the patient alive?",
            ),
        ),
    ]
