# Generated by Django 2.2.2 on 2019-08-01 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("edc_adverse_event", "0002_auto_20190802_0059"),
        ("ambition_prn", "0025_auto_20190802_0130"),
    ]

    operations = [
        migrations.AddField(
            model_name="deathreport",
            name="cause_of_death",
            field=models.ForeignKey(
                help_text="Main cause of death in the opinion of the local study doctor and local PI",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_adverse_event.CauseOfDeath",
                verbose_name="Main cause of death",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeathreport",
            name="cause_of_death",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="Main cause of death in the opinion of the local study doctor and local PI",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_adverse_event.CauseOfDeath",
                verbose_name="Main cause of death",
            ),
        ),
        migrations.AlterField(
            model_name="deathreport",
            name="cause_of_death_old",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Main cause of death in the opinion of the local study doctor and local PI",
                max_length=50,
                verbose_name="Main cause of death",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeathreport",
            name="cause_of_death_old",
            field=models.CharField(
                default="QUESTION_RETIRED",
                help_text="Main cause of death in the opinion of the local study doctor and local PI",
                max_length=50,
                verbose_name="Main cause of death",
            ),
        ),
    ]
