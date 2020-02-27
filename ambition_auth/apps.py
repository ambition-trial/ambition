from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = "ambition_auth"
    verbose_name = "Ambition Authentication and Permissions"
