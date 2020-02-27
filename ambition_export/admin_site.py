from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Ambition Export"
    site_header = "Ambition Export"
    index_title = "Ambition Export"
    site_url = "/administration/"


ambition_export_admin = AdminSite(name="ambition_export_admin")
