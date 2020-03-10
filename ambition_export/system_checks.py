import os
import sys

from collections import namedtuple
from django.conf import settings
from django.core.checks import Warning

err = namedtuple("Err", "id cls")

error_configs = dict(export_folder_check=err("ambition_export.W001", Warning))


def export_folder_check(app_configs, **kwargs):
    errors = []
    error_msg = None
    error = error_configs.get("export_folder_check")
    if (
        "test" not in sys.argv
        and "makemigrations" not in sys.argv
        and "migrate" not in sys.argv
    ):
        try:
            export_folder = settings.EXPORT_FOLDER
        except AttributeError:
            error_msg = "Export folder not set. See settings.EXPORT_FOLDER."
        else:
            if not os.path.exists(export_folder):
                error_msg = "Export folder does not exist. See settings.EXPORT_FOLDER."
        if error_msg:
            errors.append(error.cls(error_msg, hint=None, obj=None, id=error.id))
    return errors
