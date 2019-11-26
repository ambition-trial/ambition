from ambition_dashboard.navbars import navbar as ambition_dashboard_navbar
from copy import copy
from django.conf import settings
from edc_lab_dashboard.navbars import navbar as lab_navbar
from edc_navbar import site_navbars, Navbar
from edc_review_dashboard.navbars import navbar as review_navbar
from edc_adverse_event.navbars import tmg_navbar_item, ae_navbar_item
from edc_data_manager.navbar_item import dm_navbar_item

navbar = Navbar(name=settings.APP_NAME)

navbar_item = copy([item for item in lab_navbar.items if item.name == "specimens"][0])
navbar_item.active = False
navbar_item.label = "Specimens"
navbar.append_item(navbar_item)

navbar.append_item(
    [
        item
        for item in ambition_dashboard_navbar.items
        if item.name == "screened_subject"
    ][0]
)

navbar.append_item(
    [
        item
        for item in ambition_dashboard_navbar.items
        if item.name == "consented_subject"
    ][0]
)

for item in review_navbar.items:
    navbar.append_item(item)

navbar.append_item(tmg_navbar_item)
navbar.append_item(ae_navbar_item)
navbar.append_item(dm_navbar_item)

site_navbars.register(navbar)
