from edc_lab import LabProfile

from .panels import (
    cd4_panel,
    chemistry_alt_panel,
    chemistry_panel,
    csf_chemistry_panel,
    csf_panel,
    csf_paxgene_panel,
    csf_pkpd_panel,
    csf_stop_panel,
    fbc_panel,
    pk_plasma_panel_t0,
    pk_plasma_panel_t12,
    pk_plasma_panel_t2,
    pk_plasma_panel_t23,
    pk_plasma_panel_t4,
    pk_plasma_panel_t7,
    plasma_buffycoat_panel,
    qpcr24_blood_panel,
    qpcr_blood_panel,
    qpcr_csf_panel,
    serum_panel,
    sputum_storage_panel,
    urine_storage_panel,
    viral_load_panel,
    wb_panel,
    wb_paxgene_panel,
)

subject_lab_profile = LabProfile(
    name="subject_lab_profile", requisition_model="ambition_subject.subjectrequisition"
)

subject_lab_profile.add_panel(wb_panel)
subject_lab_profile.add_panel(csf_pkpd_panel)
subject_lab_profile.add_panel(qpcr_csf_panel)
subject_lab_profile.add_panel(csf_panel)
subject_lab_profile.add_panel(csf_stop_panel)
subject_lab_profile.add_panel(csf_chemistry_panel)  # goes to PMH
subject_lab_profile.add_panel(cd4_panel)
subject_lab_profile.add_panel(viral_load_panel)
subject_lab_profile.add_panel(fbc_panel)
subject_lab_profile.add_panel(chemistry_panel)
subject_lab_profile.add_panel(chemistry_alt_panel)
subject_lab_profile.add_panel(serum_panel)
subject_lab_profile.add_panel(plasma_buffycoat_panel)
subject_lab_profile.add_panel(qpcr_blood_panel)
subject_lab_profile.add_panel(qpcr24_blood_panel)
subject_lab_profile.add_panel(pk_plasma_panel_t0)
subject_lab_profile.add_panel(pk_plasma_panel_t2)
subject_lab_profile.add_panel(pk_plasma_panel_t4)
subject_lab_profile.add_panel(pk_plasma_panel_t7)
subject_lab_profile.add_panel(pk_plasma_panel_t12)
subject_lab_profile.add_panel(pk_plasma_panel_t23)
subject_lab_profile.add_panel(wb_paxgene_panel)
subject_lab_profile.add_panel(csf_paxgene_panel)
subject_lab_profile.add_panel(sputum_storage_panel)
subject_lab_profile.add_panel(urine_storage_panel)
