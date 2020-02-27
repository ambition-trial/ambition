from edc_lab import RequisitionPanel

from .processing_profiles import (
    cd4_processing,
    chemistry_alt_processing,
    chemistry_processing,
    csf_chem_processing_profile,
    csf_paxgene_processing_profile,
    csf_pkpd_processing_profile,
    csf_stop_processing_profile,
    csf_store_processing_profile,
    fbc_processing,
    plasma_buffycoat_processing,
    plasma_processing,
    qpcr_blood_processing,
    qpcr_csf_processing_profile,
    serum_processing,
    suptum_processing_profile,
    urine_processing_profile,
    viral_load_processing,
    wb_paxgene_processing_profile,
    whole_blood_processing,
)

wb_panel = RequisitionPanel(
    name="wb_storage",
    verbose_name="Whole Blood Storage",
    processing_profile=whole_blood_processing,
)

csf_pkpd_panel = RequisitionPanel(  # TODO: Only for Blantyre
    name="csf_pk_pd",
    verbose_name="CSF PK/PD",
    processing_profile=csf_pkpd_processing_profile,
)

qpcr_csf_panel = RequisitionPanel(
    name="qpcr_csf",
    verbose_name="qPCR CSF",
    processing_profile=qpcr_csf_processing_profile,
)

csf_panel = RequisitionPanel(
    name="csf_test_and_store",
    verbose_name="CSF Test and Store",
    processing_profile=csf_store_processing_profile,
)

csf_stop_panel = RequisitionPanel(  # TODO: Blantyre only.
    name="csf_stop_cm",
    verbose_name="CSF STOP-CM",
    processing_profile=csf_stop_processing_profile,
)

csf_chemistry_panel = RequisitionPanel(
    name="csf_chem_haem_routine",
    verbose_name="CSF Chem and Haem Routine",
    processing_profile=csf_chem_processing_profile,
)

cd4_panel = RequisitionPanel(
    name="cd4", verbose_name="CD4", processing_profile=cd4_processing
)

viral_load_panel = RequisitionPanel(
    name="vl", verbose_name="Viral Load", processing_profile=viral_load_processing
)

fbc_panel = RequisitionPanel(
    name="fbc", verbose_name="Full Blood Count", processing_profile=fbc_processing
)

chemistry_panel = RequisitionPanel(
    name="chemistry",
    verbose_name="Creat, Urea, Elec",
    processing_profile=chemistry_processing,
)

chemistry_alt_panel = RequisitionPanel(
    name="chemistry_alt",
    verbose_name="Creat, Urea, Elec, ALT",
    processing_profile=chemistry_alt_processing,
)

serum_panel = RequisitionPanel(
    name="serum_storage",
    verbose_name="Serum Storage",
    processing_profile=serum_processing,
)

plasma_buffycoat_panel = RequisitionPanel(
    name="pl_bc_store",
    verbose_name="Plasma and Buffycoat Store",
    processing_profile=plasma_buffycoat_processing,
)

qpcr_blood_panel = RequisitionPanel(
    name="qpcr",
    verbose_name="qPCR Blood (0hr)",
    processing_profile=qpcr_blood_processing,
)

qpcr24_blood_panel = RequisitionPanel(
    name="qpcr23",
    verbose_name="qPCR Blood (24hr)",
    processing_profile=qpcr_blood_processing,
)

pk_plasma_panel_t0 = RequisitionPanel(  # TODO: For Blantyre only
    name="pk_pl_store_t0",
    verbose_name="PK Plasma Store T0",
    processing_profile=plasma_processing,
)

pk_plasma_panel_t2 = RequisitionPanel(  # TODO: For Blantyre only
    name="pk_pl_store_t2",
    verbose_name="PK Plasma Store T2",
    processing_profile=plasma_processing,
)

pk_plasma_panel_t4 = RequisitionPanel(
    name="pk_pl_store_t4",
    verbose_name="PK Plasma Store T4",
    processing_profile=plasma_processing,
)

pk_plasma_panel_t7 = RequisitionPanel(
    name="pk_pl_store_t7",
    verbose_name="PK Plasma Store T7",
    processing_profile=plasma_processing,
)

pk_plasma_panel_t12 = RequisitionPanel(
    name="pk_pl_store_t12",
    verbose_name="PK Plasma Store T12",
    processing_profile=plasma_processing,
)

pk_plasma_panel_t23 = RequisitionPanel(
    name="pk_pl_store_t23",
    verbose_name="PK Plasma Store T23",
    processing_profile=plasma_processing,
)

wb_paxgene_panel = RequisitionPanel(
    name="wb_paxgene",
    verbose_name="Blood PaxGene",
    processing_profile=wb_paxgene_processing_profile,
)

csf_paxgene_panel = RequisitionPanel(
    name="csf_paxgene",
    verbose_name="CSF PaxGene",
    processing_profile=csf_paxgene_processing_profile,
)

sputum_storage_panel = RequisitionPanel(
    name="sputum_storage",
    verbose_name="qPCR Sputum Storage",
    processing_profile=suptum_processing_profile,
)

urine_storage_panel = RequisitionPanel(
    name="urine_storage",
    verbose_name="qPCR Urine Storage",
    processing_profile=urine_processing_profile,
)
