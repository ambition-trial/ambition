from edc_adverse_event.pdf_reports import DeathReport
from edc_adverse_event.view_mixins import DeathReportListboardViewMixin
from reportlab.lib.units import cm


class CustomDeathReport(DeathReport):
    logo_data = {
        "app_label": "ambition_edc",
        "filename": "ambition_logo.png",
        "first_page": (4.0 * cm, 0.83 * cm),
        "later_pages": (3.0 * cm, 0.625 * cm),
    }


class DeathReportListboardView(DeathReportListboardViewMixin):

    pdf_report_cls = CustomDeathReport
