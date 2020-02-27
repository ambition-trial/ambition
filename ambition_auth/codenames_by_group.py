from edc_auth import (
    AE,
    AUDITOR,
    CLINIC,
    SCREENING,
    UNBLINDING_REQUESTORS,
    UNBLINDING_REVIEWERS,
    get_default_codenames_by_group,
)

from .codenames import (
    ae,
    auditor,
    clinic,
    screening,
)


def get_codenames_by_group():
    codenames_by_group = {k: v for k, v in get_default_codenames_by_group().items()}
    codenames_by_group[AE] = ae
    codenames_by_group[AUDITOR] = auditor
    codenames_by_group[CLINIC] = clinic
    codenames_by_group[SCREENING] = screening
    codenames_by_group[UNBLINDING_REQUESTORS] = []
    codenames_by_group[UNBLINDING_REVIEWERS] = []
    return codenames_by_group
