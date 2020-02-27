# import django
# from django.apps import apps as django_apps
# from django.test import tag
#
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.contrib.admin import AdminSite
# from django.contrib.admin.utils import quote
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
# from django.contrib.messages.storage.fallback import FallbackStorage
# from django.core.exceptions import ObjectDoesNotExist
# from django.test.client import RequestFactory
# from django.test.utils import override_settings
# from django.urls import reverse
# from django_webtest import WebTest
# from mock import ANY, patch
# from ambition_rando.tests import AmbitionTestCaseMixin
#
# User = get_user_model()
#
#
# def get_model_url(obj, site=None, change=None, changelist=None):
#     site = site or 'admin'
#     app, model = obj._meta.app_label, obj._meta.model_name
#     if change:
#         return reverse(f"{site}:{app}_{model}_change", args=[quote(obj.pk)])
#     elif changelist:
#         return reverse(f"{site}:{app}_{model}_changelist")
#     else:
#         return reverse(f"{site}:{app}_{model}_add")
#
#
# def get_changelist_url(obj, site=None):
#     site = site or 'admin'
#     app, model = obj._meta.app_label, obj._meta.model_name
#     return reverse(
#         f"{site}:{app}_{model}_changelist")
#
#
# def get_history_url(obj, history_index=None, site="admin"):
#     app, model = obj._meta.app_label, obj._meta.model_name
#     if history_index is not None:
#         history = obj.history.order_by("history_id")[history_index]
#         return reverse(
#             "{site}:{app}_{model}_simple_history".format(
#                 site=site, app=app, model=model
#             ),
#             args=[quote(obj.pk), quote(history.history_id)],
#         )
#     else:
#         return reverse(
#             "{site}:{app}_{model}_history".format(
#                 site=site, app=app, model=model),
#             args=[quote(obj.pk)],
#         )
#
#
# class AdminSiteTest(AmbitionTestCaseMixin, WebTest):
#     def setUp(self):
#         self.user = User.objects.create_superuser(
#             "user_login", "u@example.com", "pass")
#
#     def login(self, user=None, superuser=None):
#         user = self.user if user is None else user
#         superuser = True if superuser is None else superuser
#         if not superuser:
#             user.is_superuser = False
#             user.is_active = True
#             user.save()
#         form = self.app.get(reverse("admin:index")).maybe_follow().form
#         form["username"] = user.username
#         form["password"] = "pass"
#         return form.submit()
#
#     def test_form(self):
#         self.login()
#         app_config = django_apps.get_app_config('ambition_subject')
#         for model in app_config.get_models():
#             if 'historical' not in model._meta.label_lower:
#                 response = self.app.get(get_model_url(model), status=200)
#                 self.assertIn(model._meta.verbose_name,
#                               response.unicode_normal_body)
