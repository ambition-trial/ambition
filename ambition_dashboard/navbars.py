from edc_navbar import NavbarItem, site_navbars, Navbar
from edc_review_dashboard.navbars import navbar_item as review_navbar_item
from edc_adverse_event.navbars import ae_navbar_item, tmg_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item

from edc_navbar.get_default_navbar import get_default_navbar


no_url_namespace = False  # True if settings.APP_NAME == "ambition_dashboard" else False

navbar = Navbar(name=get_default_navbar())

navbar.append_item(
    NavbarItem(
        name="screened_subject",
        title="Screening",
        label="Screening",
        fa_icon="fas fa-user-plus",
        codename="edc_navbar.nav_screening_section",
        url_name="screening_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(
    NavbarItem(
        name="consented_subject",
        title="Subjects",
        label="Subjects",
        fa_icon="far fa-user-circle",
        codename="edc_navbar.nav_subject_section",
        url_name="subject_listboard_url",
        no_url_namespace=no_url_namespace,
    )
)

navbar.append_item(tmg_navbar_item)
navbar.append_item(ae_navbar_item)
navbar.append_item(dm_navbar_item)
navbar.append_item(review_navbar_item)

site_navbars.register(navbar)
