# Generated by Django 2.2 on 2019-05-21 16:46

from django.db import migrations, models
import edc_model.validators.date
import edc_model_fields.fields.date_estimated


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0052_auto_20190521_1833")]

    operations = [
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If Yes, when was their <u>current or most recent</u> ART regimen started?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_date_estimated",
            field=edc_model_fields.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="Is the <u>current or most recent</u> ARV date estimated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_decision",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("ART continued", "ART continued"),
                    ("ART stopped", "ART stopped"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="What decision was made at admission regarding their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_defaulted_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If the patient has DEFAULTED, on what date did they default from their <u>most recent</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_is_adherent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=5,
                verbose_name="If the patient is currently on ART, are they adherent to their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_arv_is_defaulted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="'DEFAULTED' means no ART for at least one month.",
                max_length=5,
                verbose_name="Has the patient <u>now</u> defaulted from their ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="initial_arv_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If YES, when did the patient <u>start</u> ART for the first time.",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="initial_arv_date_estimated",
            field=edc_model_fields.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="Is the ARV <u>start</u> date estimated?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If Yes, when was their <u>current or most recent</u> ART regimen started?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_date_estimated",
            field=edc_model_fields.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="Is the <u>current or most recent</u> ARV date estimated?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_decision",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("ART continued", "ART continued"),
                    ("ART stopped", "ART stopped"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="What decision was made at admission regarding their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_defaulted_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If the patient has DEFAULTED, on what date did they default from their <u>most recent</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_is_adherent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=5,
                verbose_name="If the patient is currently on ART, are they adherent to their <u>current</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_is_defaulted",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="'DEFAULTED' means no ART for at least one month.",
                max_length=5,
                verbose_name="Has the patient <u>now</u> defaulted from their ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_arv_regimen",
            field=models.ManyToManyField(
                related_name="current_arv",
                to="ambition_lists.ArvRegimens",
                verbose_name="If Yes, what is their <u>current or most recent</u> ART regimen?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="initial_arv_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="If YES, when did the patient <u>start</u> ART for the first time.",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="initial_arv_date_estimated",
            field=edc_model_fields.fields.date_estimated.IsDateEstimatedFieldNa(
                choices=[
                    ("N/A", "Not applicable"),
                    ("not_estimated", "No."),
                    ("D", "Yes, estimated the Day"),
                    ("MD", "Yes, estimated Month and Day"),
                    ("YMD", "Yes, estimated Year, Month and Day"),
                ],
                default="N/A",
                help_text="If the exact date is not known, please indicate which part of the date is estimated.",
                max_length=25,
                verbose_name="Is the ARV <u>start</u> date estimated?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="initial_arv_regimen",
            field=models.ManyToManyField(
                related_name="initial_arv",
                to="ambition_lists.ArvRegimens",
                verbose_name="If YES, which drugs were prescribed for their <u>first</u> ART regimen?",
            ),
        ),
    ]