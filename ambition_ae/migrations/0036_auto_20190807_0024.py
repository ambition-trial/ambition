# Generated by Django 2.2.2 on 2019-08-06 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("ambition_ae", "0035_auto_20190806_2204")]

    operations = [
        migrations.AlterField(
            model_name="aeinitial",
            name="ae_classification",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_adverse_event.AeClassification",
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AlterField(
            model_name="aeinitial",
            name="sae_reason_old",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("dead", "Death"),
                    ("life_threatening", "Life-threatening"),
                    ("significant_disability", "Significant disability"),
                    (
                        "in-patient_hospitalization",
                        "In-patient hospitalization or prolongation (17 or more days from study inclusion)",
                    ),
                    (
                        "medically_important_event",
                        "Medically important event (e.g. Severe thrombophlebitis, Bacteraemia, recurrence of symptoms not requiring admission, Hospital acquired pneumonia)",
                    ),
                ],
                default="QUESTION_RETIRED",
                help_text="If subject deceased, submit a Death Report",
                max_length=50,
                verbose_name='If "Yes", reason for SAE:',
            ),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="ae_classification",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_adverse_event.AeClassification",
                verbose_name="Adverse Event (AE) Classification",
            ),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="sae_reason_old",
            field=models.CharField(
                choices=[
                    ("N/A", "Not applicable"),
                    ("dead", "Death"),
                    ("life_threatening", "Life-threatening"),
                    ("significant_disability", "Significant disability"),
                    (
                        "in-patient_hospitalization",
                        "In-patient hospitalization or prolongation (17 or more days from study inclusion)",
                    ),
                    (
                        "medically_important_event",
                        "Medically important event (e.g. Severe thrombophlebitis, Bacteraemia, recurrence of symptoms not requiring admission, Hospital acquired pneumonia)",
                    ),
                ],
                default="QUESTION_RETIRED",
                help_text="If subject deceased, submit a Death Report",
                max_length=50,
                verbose_name='If "Yes", reason for SAE:',
            ),
        ),
    ]
