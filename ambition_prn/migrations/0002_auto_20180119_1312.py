# Generated by Django 2.0.1 on 2018-01-19 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="historicalprotocoldeviationviolation",
            name="short_description",
            field=models.CharField(
                help_text='Max 35 characters. Note: If this occurrence is a "violation" there is additional space below for a more detailed description',
                max_length=35,
                null=True,
                verbose_name="Provide a short description of this occurrence",
            ),
        ),
        migrations.AddField(
            model_name="protocoldeviationviolation",
            name="short_description",
            field=models.CharField(
                help_text='Max 35 characters. Note: If this occurrence is a "violation" there is additional space below for a more detailed description',
                max_length=35,
                null=True,
                verbose_name="Provide a short description of this occurrence",
            ),
        ),
    ]
