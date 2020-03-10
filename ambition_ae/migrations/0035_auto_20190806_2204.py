# Generated by Django 2.2.2 on 2019-08-06 20:04
from django.db import migrations
from edc_constants.constants import NOT_APPLICABLE, DEAD
from edc_list_data.preload_data import PreloadData


def update_sae_reason(apps, schema_editor):

    list_data = {
        "edc_adverse_event.saereason": [
            (NOT_APPLICABLE, "Not applicable"),
            (DEAD, "Death"),
            ("life_threatening", "Life-threatening"),
            ("significant_disability", "Significant disability"),
            (
                "in-patient_hospitalization",
                "In-patient hospitalization or prolongation (17 or more days from study inclusion)",
            ),
            (
                "medically_important_event",
                "Medically important event (e.g. Severe thrombophlebitis, Bacteraemia, "
                "recurrence of symptoms not requiring admission, Hospital acquired "
                "pneumonia)",
            ),
        ]
    }

    PreloadData(list_data=list_data, apps=apps)

    SaeReason = apps.get_model("edc_adverse_event.SaeReason")
    AeInitial = apps.get_model("ambition_ae.AeInitial")
    for obj in AeInitial.objects.all():
        sae_reason = SaeReason.objects.get(short_name=obj.sae_reason_old)
        obj.sae_reason = sae_reason
        obj.save()


class Migration(migrations.Migration):

    dependencies = [("ambition_ae", "0034_auto_20190806_2203")]

    operations = [
        migrations.RunPython(update_sae_reason, hints={"target_db": "default"})
    ]
