# import os
# import sys
#
# from collections import namedtuple
# from django.conf import settings
# from django.core.checks import Warning
#
# from .randomization_list_verifier import RandomizationListVerifier
#
# err = namedtuple("Err", "id cls")
#
# error_configs = dict(randomization_list_check=err("ambition_edc.W001", Warning))
#
#
# def randomization_list_check(app_configs, **kwargs):
#     errors = []
#     error = error_configs.get("randomization_list_check")
#     if (
#         "test" not in sys.argv
#         and "showmigrations" not in sys.argv
#         and "makemigrations" not in sys.argv
#         and "migrate" not in sys.argv
#     ):
#         error_msg = RandomizationListVerifier().message
#         if error_msg:
#             errors.append(error.cls(error_msg, hint=None, obj=None, id=error.id))
#     if not settings.DEBUG:
#         if settings.ETC_DIR not in settings.RANDOMIZATION_LIST_PATH:
#             errors.append(
#                 Warning(
#                     f"Insecure configuration. Randomization list file must be "
#                     f"stored in the etc folder. Got {settings.RANDOMIZATION_LIST_PATH}",
#                     id=f"settings.RANDOMIZATION_LIST_PATH",
#                 )
#             )
#         if os.access(settings.RANDOMIZATION_LIST_PATH, os.W_OK):
#             errors.append(
#                 Warning(
#                     f"Insecure configuration. File is writeable by this user. "
#                     f"Got {settings.RANDOMIZATION_LIST_PATH}",
#                     id=f"settings.RANDOMIZATION_LIST_PATH",
#                 )
#             )
#     return errors
