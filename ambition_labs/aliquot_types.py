from edc_lab import AliquotType

fbc = AliquotType(name="FBC", alpha_code="FBC", numeric_code="63")

qfc = AliquotType(name="Quantitative FC", alpha_code="QFC", numeric_code="61")

csf_store = AliquotType(name="CSF store", alpha_code="CSF", numeric_code="62")

csf_testing = AliquotType(name="Isolates", alpha_code="ISOLATES", numeric_code="64")

csf_glucose = AliquotType(name="Glucose", alpha_code="GLUCOSE", numeric_code="65")

csf_protein = AliquotType(name="Protein", alpha_code="PROTEIN", numeric_code="66")

csf_pellet = AliquotType(name="CSF Pellet", alpha_code="PELLET", numeric_code="67")

csf_supernatant = AliquotType(
    name="CSF Supernatant", alpha_code="SUPERNATANT", numeric_code="68"
)

csf = AliquotType(name="Cerebro Spinal Fluid", alpha_code="CSF", numeric_code="56")
csf.add_derivatives(
    qfc,
    csf_store,
    csf_testing,
    csf_glucose,
    csf_protein,
    csf,
    csf_pellet,
    csf_supernatant,
)
