import os
import sys

from django.conf import settings
from django.core.management.color import color_style
from django.core.management.base import BaseCommand

style = color_style()


def update_forms_reference(sender=None, **kwargs):

    from ambition_subject.admin_site import ambition_subject_admin
    from ambition_visit_schedule.visit_schedules import visit_schedule
    from edc_form_describer import FormsReference

    sys.stdout.write(
        style.MIGRATE_HEADING(
            f"Refreshing CRF reference document for ambition_subject\n"
        )
    )
    doc_folder = os.path.join(settings.BASE_DIR, "docs")
    if not os.path.exists(doc_folder):
        os.mkdir(doc_folder)
    forms = FormsReference(
        visit_schedules=[visit_schedule], admin_site=ambition_subject_admin
    )
    path = os.path.join(doc_folder, "forms_reference.md")
    forms.to_file(path=path, exists_ok=True)


class Command(BaseCommand):

    help = "Update forms reference document (.md)"

    def handle(self, *args, **options):

        update_forms_reference()
