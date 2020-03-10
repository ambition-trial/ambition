from edc_lab import Process, ProcessingProfile, sputum, wb, pl, bc, serum, urine

from .aliquot_types import csf, qfc, csf_testing, csf_supernatant, csf_pellet
from .aliquot_types import csf_glucose, csf_protein


suptum_processing_profile = ProcessingProfile(name="sputum", aliquot_type=sputum)
suptum_store = Process(aliquot_type=sputum, aliquot_count=1)
suptum_processing_profile.add_processes(suptum_store)

urine_processing_profile = ProcessingProfile(name="urine", aliquot_type=urine)
urine_store = Process(aliquot_type=urine, aliquot_count=1)
urine_processing_profile.add_processes(urine_store)

wb_paxgene_processing_profile = ProcessingProfile(name="wb_paxgene", aliquot_type=wb)
csf_paxgene_processing_profile = ProcessingProfile(name="wb_paxgene", aliquot_type=csf)

csf_store_processing_profile = ProcessingProfile(name="csf_culture", aliquot_type=csf)
process_qfc = Process(aliquot_type=qfc, aliquot_count=3)
process_csf_testing = Process(aliquot_type=csf_testing, aliquot_count=2)
csf_store_processing_profile.add_processes(process_qfc, process_csf_testing)

csf_stop_processing_profile = ProcessingProfile(name="csf_store", aliquot_type=csf)
csf_store = Process(aliquot_type=qfc, aliquot_count=2)
process_csf_testing = Process(aliquot_type=csf_testing, aliquot_count=1)
csf_stop_processing_profile.add_processes(csf_store, process_csf_testing)

csf_pkpd_processing_profile = ProcessingProfile(name="csf_pkpd", aliquot_type=csf)
process_csf_pkpd = Process(aliquot_type=csf, aliquot_count=2)
csf_pkpd_processing_profile.add_processes(process_csf_pkpd)

qpcr_csf_processing_profile = ProcessingProfile(name="qpcr_csf", aliquot_type=csf)
process_supernatant = Process(aliquot_type=csf_supernatant, aliquot_count=1)
process_pellet = Process(aliquot_type=csf_pellet, aliquot_count=1)
qpcr_csf_processing_profile.add_processes(process_supernatant, process_pellet)

csf_chem_processing_profile = ProcessingProfile(name="csf_chemistry", aliquot_type=csf)
process_csf_glucose = Process(aliquot_type=csf_glucose, aliquot_count=1)


process_csf_protein = Process(aliquot_type=csf_protein, aliquot_count=1)
csf_chem_processing_profile.add_processes(process_csf_glucose, process_csf_protein)

whole_blood_processing = ProcessingProfile(name="whole_blood_store", aliquot_type=wb)
wb_process = Process(aliquot_type=wb, aliquot_count=2)
whole_blood_processing.add_processes(wb_process)

viral_load_processing = ProcessingProfile(name="viral_load", aliquot_type=wb)
vl_pl_process = Process(aliquot_type=pl, aliquot_count=4)
vl_bc_process = Process(aliquot_type=bc, aliquot_count=2)
viral_load_processing.add_processes(vl_pl_process, vl_bc_process)

cd4_processing = ProcessingProfile(name="CD4", aliquot_type=wb)

fbc_processing = ProcessingProfile(name="FBC", aliquot_type=wb)

chemistry_processing = ProcessingProfile(name="Chem", aliquot_type=wb)

serum_processing = ProcessingProfile(name="Serum", aliquot_type=wb)
serum_process = Process(aliquot_type=serum, aliquot_count=2)
serum_processing.add_processes(serum_process)

plasma_buffycoat_processing = ProcessingProfile(name="Plasma and BC", aliquot_type=wb)
plasma_process = Process(aliquot_type=pl, aliquot_count=2)
buffycoat_process = Process(aliquot_type=bc, aliquot_count=1)
plasma_buffycoat_processing.add_processes(plasma_process, buffycoat_process)

plasma_processing = ProcessingProfile(name="Plasma", aliquot_type=wb)
plasma_process = Process(aliquot_type=pl, aliquot_count=4)
plasma_processing.add_processes(plasma_process)

qpcr_blood_processing = ProcessingProfile(name="qPCR", aliquot_type=wb)
qpcr_wb_process = Process(aliquot_type=wb, aliquot_count=1)
qpcr_pl_process = Process(aliquot_type=pl, aliquot_count=2)
qpcr_blood_processing.add_processes(qpcr_wb_process, qpcr_pl_process)

chemistry_alt_processing = ProcessingProfile(name="Chem + ALT", aliquot_type=wb)
