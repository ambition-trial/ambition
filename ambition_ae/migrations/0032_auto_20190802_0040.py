# Generated by Django 2.2.2 on 2019-08-01 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_ae", "0031_auto_20190801_2340")]

    operations = [
        migrations.AlterField(
            model_name="aeinitial",
            name="ae_classification_old",
            field=models.CharField(
                choices=[
                    ("anaemia", "Anaemia"),
                    ("bacteraemia/sepsis", "Bacteraemia/Sepsis"),
                    ("CM_IRIS", "CM IRIS"),
                    ("diarrhoea", "Diarrhoea"),
                    ("hypokalaemia", "Hypokalaemia"),
                    ("neutropaenia", "Neutropaenia"),
                    ("pneumonia", "Pneumonia"),
                    ("renal_impairment", "Renal impairment"),
                    ("respiratory_distress", "Respiratory distress"),
                    ("TB", "TB"),
                    ("thrombocytopenia", "Thrombocytopenia"),
                    ("thrombophlebitis", "Thrombophlebitis"),
                    ("OTHER", "Other"),
                ],
                default="QUESTION_RETIRED",
                max_length=150,
            ),
        ),
        migrations.AlterField(
            model_name="historicalaeinitial",
            name="ae_classification_old",
            field=models.CharField(
                choices=[
                    ("anaemia", "Anaemia"),
                    ("bacteraemia/sepsis", "Bacteraemia/Sepsis"),
                    ("CM_IRIS", "CM IRIS"),
                    ("diarrhoea", "Diarrhoea"),
                    ("hypokalaemia", "Hypokalaemia"),
                    ("neutropaenia", "Neutropaenia"),
                    ("pneumonia", "Pneumonia"),
                    ("renal_impairment", "Renal impairment"),
                    ("respiratory_distress", "Respiratory distress"),
                    ("TB", "TB"),
                    ("thrombocytopenia", "Thrombocytopenia"),
                    ("thrombophlebitis", "Thrombophlebitis"),
                    ("OTHER", "Other"),
                ],
                default="QUESTION_RETIRED",
                max_length=150,
            ),
        ),
    ]