# Generated by Django 2.2 on 2019-05-15 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0047_auto_20190319_0029")]

    operations = [
        migrations.RenameField(
            model_name="historicalweek2",
            old_name="ampho_end_date",
            new_name="ampho_stop_date",
        ),
        migrations.RenameField(
            model_name="week2", old_name="ampho_end_date", new_name="ampho_stop_date"
        ),
    ]