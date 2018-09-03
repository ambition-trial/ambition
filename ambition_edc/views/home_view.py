from ambition_ae.models import AeTmg
from django.conf import settings
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

    template_name = f'ambition_edc/bootstrap{settings.EDC_BOOTSTRAP}/home.html'
    navbar_name = settings.APP_NAME
    navbar_selected_item = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(aetmg_opts=AeTmg._meta)
        return context
