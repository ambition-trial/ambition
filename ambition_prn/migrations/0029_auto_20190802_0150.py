# Generated by Django 2.2.2 on 2019-08-01 17:44

from ambition_ae.constants import CRYTOCOCCAL_MENINGITIS
from django.db import migrations
from edc_constants.constants import OTHER, TUBERCULOSIS, MALIGNANCY, UNKNOWN
from edc_list_data.preload_data import PreloadData


def update_cause_of_death(apps, schema_editor):

    list_data = {
        "edc_adverse_event.causeofdeath": [
            (CRYTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
            (
                "Cryptococcal_meningitis_relapse_IRIS",
                "Cryptococcal meningitis relapse/IRIS",
            ),
            (TUBERCULOSIS, "TB"),
            ("bacteraemia", "Bacteraemia"),
            ("bacterial_pneumonia", "Bacterial pneumonia"),
            (MALIGNANCY, "Malignancy"),
            ("art_toxicity", "ART toxicity"),
            ("IRIS_non_CM", "IRIS non-CM"),
            ("diarrhea_wasting", "Diarrhea/wasting"),
            (UNKNOWN, "Unknown"),
            (OTHER, "Other"),
        ]
    }

    PreloadData(list_data=list_data, apps=apps)

    CauseOfDeath = apps.get_model("edc_adverse_event.CauseOfDeath")
    DeathReportTmg = apps.get_model("ambition_prn.DeathReportTmg")
    for obj in DeathReportTmg.objects.all():
        cause_of_death = CauseOfDeath.objects.get(short_name=obj.cause_of_death_old)
        obj.cause_of_death = cause_of_death
        obj.save()


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0028_auto_20190802_0148")]

    operations = [
        migrations.RunPython(update_cause_of_death, hints={"target_db": "default"})
    ]
