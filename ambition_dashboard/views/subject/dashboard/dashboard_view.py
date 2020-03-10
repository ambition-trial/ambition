from ambition_rando.view_mixins import RandomizationListViewMixin
from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(RandomizationListViewMixin, SubjectDashboardView):

    consent_model = "ambition_subject.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "ambition_subject.subjectvisit"
