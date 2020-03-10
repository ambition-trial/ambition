# Generated by Django 2.0.2 on 2018-02-27 07:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0005_auto_20180129_0908")]

    operations = [
        migrations.AlterField(
            model_name="historicallumbarpuncturecsf",
            name="csf_cr_ag",
            field=models.CharField(
                blank=True,
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("IND", "Indeterminate"),
                    ("not_done", "Not done"),
                ],
                max_length=15,
                null=True,
                verbose_name="CSF CrAg:",
            ),
        ),
        migrations.AlterField(
            model_name="historicallumbarpuncturecsf",
            name="csf_wbc_cell_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup>",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Total CSF WBC cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="historicallumbarpuncturecsf",
            name="differential_lymphocyte_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup> or %",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Differential lymphocyte cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="historicallumbarpuncturecsf",
            name="differential_neutrophil_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup> or %",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Differential neutrophil cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="historicallumbarpuncturecsf",
            name="india_ink",
            field=models.CharField(
                blank=True,
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("IND", "Indeterminate"),
                    ("not_done", "Not done"),
                ],
                max_length=15,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="lumbarpuncturecsf",
            name="csf_cr_ag",
            field=models.CharField(
                blank=True,
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("IND", "Indeterminate"),
                    ("not_done", "Not done"),
                ],
                max_length=15,
                null=True,
                verbose_name="CSF CrAg:",
            ),
        ),
        migrations.AlterField(
            model_name="lumbarpuncturecsf",
            name="csf_wbc_cell_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup>",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Total CSF WBC cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="lumbarpuncturecsf",
            name="differential_lymphocyte_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup> or %",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Differential lymphocyte cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="lumbarpuncturecsf",
            name="differential_neutrophil_count",
            field=models.IntegerField(
                blank=True,
                help_text="acceptable units are mm<sup>3</sup> or %",
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="Differential neutrophil cell count:",
            ),
        ),
        migrations.AlterField(
            model_name="lumbarpuncturecsf",
            name="india_ink",
            field=models.CharField(
                blank=True,
                choices=[
                    ("POS", "Positive"),
                    ("NEG", "Negative"),
                    ("IND", "Indeterminate"),
                    ("not_done", "Not done"),
                ],
                max_length=15,
                null=True,
            ),
        ),
    ]
