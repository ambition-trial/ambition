from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar
from edc_lab_dashboard.dashboard_urls import dashboard_urls as lab_dashboard_urls

navbar = Navbar(name='ambition')

navbar.append_item(
    NavbarItem(
        name='pharmacy',
        label='Pharmacy',
        fa_icon='fas fa-medkit',
        url_name=f'home_url'))

navbar.append_item(
    NavbarItem(
        name='lab',
        label='Specimens',
        fa_icon='fas fa-flask',
        url_name=lab_dashboard_urls.get('requisition_listboard_url')))

navbar.append_item(
    NavbarItem(
        name='screened_subject',
        label='Screening',
        fa_icon='fas fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')))

navbar.append_item(
    NavbarItem(
        name='consented_subject',
        label='Subjects',
        fa_icon='fas fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES.get('subject_listboard_url')))


site_navbars.register(navbar)
