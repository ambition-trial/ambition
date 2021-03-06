# Generated by Django 2.2.6 on 2019-10-09 19:45
from django.db import migrations
from edc_adverse_event.constants import (
    DEATH_REPORT_TMG_ACTION,
    DEATH_REPORT_TMG_SECOND_ACTION,
)
from edc_visit_schedule.utils import OnScheduleError
from django.db.models.deletion import ProtectedError
from edc_action_item.create_or_update_action_type import create_or_update_action_type
from edc_adverse_event.action_items.death_report_tmg_second_action import (
    DeathReportTmgSecondAction,
)


def change_action_item_to_tmg_second(apps, schema_editor):
    ActionItem = apps.get_model("edc_action_item.actionitem")
    ActionType = apps.get_model("edc_action_item.actiontype")

    for obj in ActionItem.objects.filter(
        action_type__name=DEATH_REPORT_TMG_ACTION,
        related_action_item__isnull=True,
        parent_action_item__isnull=False,
    ):
        obj.related_action_item = obj.parent_action_item
        obj.save()

    create_or_update_action_type(**DeathReportTmgSecondAction.as_dict())

    action_type = ActionType.objects.get(name=DEATH_REPORT_TMG_SECOND_ACTION)
    ActionItem.objects.filter(
        parent_action_item__action_type__name=DEATH_REPORT_TMG_ACTION
    ).update(
        action_type=action_type, reference_model="ambition_prn.deathreporttmgsecond"
    )

    # clear out cancelled action items, if possible
    for obj in ActionItem.objects.filter(status="Cancelled"):
        try:
            obj.delete()
        except ProtectedError:
            pass
        except OnScheduleError:
            pass


class Migration(migrations.Migration):

    dependencies = [("ambition_prn", "0037_auto_20191009_0750")]

    operations = [migrations.RunPython(change_action_item_to_tmg_second)]
