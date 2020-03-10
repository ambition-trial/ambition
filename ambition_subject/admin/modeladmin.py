from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import (
    ModelAdminSubjectDashboardMixin,
    ModelAdminCrfDashboardMixin,
)


class ModelAdminMixin(ModelAdminSubjectDashboardMixin):
    pass


class CrfModelAdminMixin(ModelAdminCrfDashboardMixin):

    pass


class CrfModelAdmin(ModelAdminCrfDashboardMixin, SimpleHistoryAdmin):

    pass
