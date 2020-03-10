from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == "ambition_ae" else False

ambition_ae = Navbar(name="ambition_ae")

ambition_ae.append_item(
    NavbarItem(
        name="ae",
        title="Adverse Events",
        # label='AE',
        fa_icon="fa-heartbeat",
        url_name="ambition_ae:home_url",
        codename="edc_navbar.nav_ambition_ae",
        no_url_namespace=no_url_namespace,
    )
)

site_navbars.register(ambition_ae)
