from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "ambition_lists"
    verbose_name = "Ambition Lists"
    include_in_administration_section = True
