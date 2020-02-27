import re

from django.db.models import Q
from edc_dashboard.view_mixins import EdcViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from edc_subject_model_wrappers import SubjectConsentModelWrapper


class ListboardView(
    EdcViewMixin,
    NavbarViewMixin,
    ListboardFilterViewMixin,
    SearchFormViewMixin,
    ListboardView,
):

    listboard_template = "subject_listboard_template"
    listboard_url = "subject_listboard_url"
    listboard_panel_style = "success"
    listboard_fa_icon = "far fa-user-circle"
    listboard_model = "ambition_subject.subjectconsent"
    listboard_view_permission_codename = "edc_dashboard.view_subject_listboard"

    model_wrapper_cls = SubjectConsentModelWrapper
    navbar_selected_item = "consented_subject"
    search_form_url = "subject_listboard_url"

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get("subject_identifier"):
            options.update({"subject_identifier": kwargs.get("subject_identifier")})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match("^[A-Z]+$", search_term):
            q = Q(first_name__exact=search_term)
        return [q]
