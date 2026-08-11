import sys

sys.path.insert(0, "scratch")
from wire_generic_batch import wire_batch

BATCH_7_MODULES = [
    (
        "coset_hidden_involution_support_filter_no_go",
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO",
        "write_support_filter_no_go_report",
        "coset-hidden-involution-support-filter-no-go",
    ),
    (
        "dcp_cnot_linear_split_entanglement_no_go",
        "EXP-DHS-DCP-CNOT-LINEAR-SPLIT-ENTANGLEMENT-NO-GO",
        "write_cnot_linear_split_entanglement_report",
        "dcp-cnot-linear-split-entanglement-no-go",
    ),
    (
        "dcp_linear_reparameterization_affine_flat_no_go",
        "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO",
        "write_linear_reparameterization_affine_flat_report",
        "dcp-linear-reparameterization-affine-flat-no-go",
    ),
]

if __name__ == "__main__":
    wire_batch(BATCH_7_MODULES)
