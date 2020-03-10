from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = "Ambition PRN"
    site_header = "Ambition PRN"
    index_title = "Ambition PRN"
    site_url = "/administration/"


ambition_prn_admin = AdminSite(name="ambition_prn_admin")
ambition_prn_admin.disable_action("delete_selected")
