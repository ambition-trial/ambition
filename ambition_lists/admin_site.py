from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = "Ambition Lists"
    site_header = "Ambition Lists"
    index_title = "Ambition Lists"
    site_url = "/administration/"


ambition_lists_admin = AdminSite(name="ambition_lists_admin")
