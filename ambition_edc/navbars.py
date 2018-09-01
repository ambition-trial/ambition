from ambition_dashboard.navbars import navbar as ambition_dashboard_navbar
from copy import copy
from django.conf import settings
from edc_lab_dashboard.navbars import navbar as lab_navbar
from edc_navbar import site_navbars, Navbar

navbar = Navbar(name=settings.APP_NAME)

navbar_item = copy([item for item in lab_navbar.items
                    if item.name == 'specimens'][0])
navbar_item.active = False
navbar_item.label = 'Specimens'
navbar.append_item(navbar_item)

navbar.append_item(
    [item for item in ambition_dashboard_navbar.items
     if item.name == 'screened_subject'][0])

navbar.append_item(
    [item for item in ambition_dashboard_navbar.items
     if item.name == 'consented_subject'][0])

navbar.append_item(
    [item for item in ambition_dashboard_navbar.items
     if item.name == 'tmg'][0])

site_navbars.register(navbar)
