from edc_adverse_event.views import DeathListboardView


class TmgDeathListboardView(DeathListboardView):

    listboard_back_url = "ambition_dashboard:tmg_home_url"
