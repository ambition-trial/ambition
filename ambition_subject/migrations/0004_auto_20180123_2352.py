# Generated by Django 2.0.1 on 2018-01-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0003_auto_20180121_1456")]

    operations = [
        migrations.RemoveField(
            model_name="historicalpkpdcrf", name="fluconazole_dose_missed"
        ),
        migrations.RemoveField(
            model_name="historicalpkpdcrf", name="flucytosine_missed"
        ),
        migrations.RemoveField(
            model_name="historicalpkpdcrf", name="reason_blood_sample_missed"
        ),
        migrations.RemoveField(
            model_name="historicalpkpdcrf", name="reason_fluconazole_dose_missed"
        ),
        migrations.RemoveField(
            model_name="historicalpkpdcrf", name="reason_flucytosine_dose_missed"
        ),
        migrations.RemoveField(model_name="pkpdcrf", name="fluconazole_dose_missed"),
        migrations.RemoveField(model_name="pkpdcrf", name="flucytosine_dose_missed"),
        migrations.RemoveField(model_name="pkpdcrf", name="flucytosine_missed"),
        migrations.RemoveField(model_name="pkpdcrf", name="reason_blood_sample_missed"),
        migrations.RemoveField(
            model_name="pkpdcrf", name="reason_fluconazole_dose_missed"
        ),
        migrations.RemoveField(
            model_name="pkpdcrf", name="reason_flucytosine_dose_missed"
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="blood_sample_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If any blood samples missed, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="fluconazole_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Units in mg",
                null=True,
                verbose_name="Fluconazole dose?",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="fluconazole_dose_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If Fluconazole dose not given, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_four_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;4</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_one_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;1</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If any Flucytosine doses not given, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_three_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;3</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose_two_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;2</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="blood_sample_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If any blood samples missed, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="fluconazole_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Units in mg",
                null=True,
                verbose_name="Fluconazole dose?",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="fluconazole_dose_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If Fluconazole dose not given, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="flucytosine_dose_four_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;4</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="flucytosine_dose_one_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;1</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="flucytosine_dose_reason_missed",
            field=models.TextField(
                blank=True,
                max_length=75,
                null=True,
                verbose_name="If any Flucytosine doses not given, provide reason",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="flucytosine_dose_three_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;3</u> given? ",
            ),
        ),
        migrations.AddField(
            model_name="pkpdcrf",
            name="flucytosine_dose_two_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Flucytosine <u>DOSE&nbsp;2</u> given? ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpkpdcrf",
            name="fluconazole_dose_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Was the Fluconazole dose given?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpkpdcrf",
            name="flucytosine_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Units in mg",
                null=True,
                verbose_name="Flucytosine dose?",
            ),
        ),
        migrations.AlterField(
            model_name="pkpdcrf",
            name="fluconazole_dose_given",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=5,
                null=True,
                verbose_name="Was the Fluconazole dose given?",
            ),
        ),
        migrations.AlterField(
            model_name="pkpdcrf",
            name="flucytosine_dose",
            field=models.IntegerField(
                blank=True,
                help_text="Units in mg",
                null=True,
                verbose_name="Flucytosine dose?",
            ),
        ),
    ]
