from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "ambition_labs"

    def ready(self):
        from . import reportables
