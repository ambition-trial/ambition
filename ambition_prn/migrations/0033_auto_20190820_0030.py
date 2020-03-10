# Generated by Django 2.2.2 on 2019-08-19 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0032_auto_20190808_2209")]

    operations = [
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="safety_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Could this occurrence have an impact on safety of the participant?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalprotocoldeviationviolation",
            name="study_outcomes_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Could this occurrence have an impact on study outcomes?",
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="safety_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Could this occurrence have an impact on safety of the participant?",
            ),
        ),
        migrations.AlterField(
            model_name="protocoldeviationviolation",
            name="study_outcomes_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Could this occurrence have an impact on study outcomes?",
            ),
        ),
    ]