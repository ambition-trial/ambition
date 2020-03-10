from edc_adverse_event.views import SummaryListboardView


class TmgSummaryListboardView(SummaryListboardView):

    listboard_back_url = "ambition_dashboard:tmg_home_url"
