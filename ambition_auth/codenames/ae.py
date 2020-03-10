from edc_auth.codenames import ae as orig_ae
from copy import copy

ae = copy(orig_ae)

ae.extend(
    [
        "ambition_ae.view_antibiotictreatment",
        "ambition_ae.view_meningitissymptom",
        "ambition_ae.view_neurological",
        "ambition_ae.add_recurrencesymptom",
        "ambition_ae.change_recurrencesymptom",
        "ambition_ae.delete_recurrencesymptom",
        "ambition_ae.view_recurrencesymptom",
        "ambition_ae.view_historicalrecurrencesymptom",
    ]
)
