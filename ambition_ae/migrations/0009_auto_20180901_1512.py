from django.db import migrations


def merge_amphotericin(apps, schema_editor):
    """Merge fields amphotericin_b_relation and ambisome_relation
    into amphotericin_relation by selecting the "highest"
    ranking relation to study drug.
    """
    ranked_responses = [
        "N/A",
        "not_related",
        "unlikely_related",
        "possibly_related",
        "probably_related",
        "definitely_related",
    ]
    AeInitial = apps.get_model("ambition_ae", "aeinitial")
    for obj in AeInitial.objects.all():
        amphotericin_rank = [
            i
            for i, response in enumerate(ranked_responses)
            if response == obj.amphotericin_b_relation
        ][0]
        ambisome_rank = [
            i
            for i, response in enumerate(ranked_responses)
            if response == obj.ambisome_relation
        ][0]
        obj.amphotericin_relation = ranked_responses[
            max([amphotericin_rank, ambisome_rank])
        ]
        obj.save_base(raw=True)


class Migration(migrations.Migration):

    dependencies = [("ambition_ae", "0008_auto_20180901_1512")]

    operations = [migrations.RunPython(merge_amphotericin)]
