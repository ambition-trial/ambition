# Generated by Django 2.2.2 on 2019-08-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0066_auto_20190808_2209")]

    operations = [
        migrations.AlterField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_four_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <b><u>DOSE&nbsp;4</u></b> given? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_three_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <b><u>DOSE&nbsp;3</u></b> given? ",
            ),
        ),
        migrations.AlterField(
            model_name="pkpdcrf",
            name="flucytosine_dose_four_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <b><u>DOSE&nbsp;4</u></b> given? ",
            ),
        ),
        migrations.AlterField(
            model_name="pkpdcrf",
            name="flucytosine_dose_three_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <b><u>DOSE&nbsp;3</u></b> given? ",
            ),
        ),
    ]