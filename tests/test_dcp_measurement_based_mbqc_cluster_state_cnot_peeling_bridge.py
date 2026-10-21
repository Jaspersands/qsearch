"""Unit tests for Subsystem 142: MBQC Cluster State O(1)-Depth CNOT Peeling Bridge."""

from theorems.dcp_measurement_based_mbqc_cluster_state_cnot_peeling_bridge import (
    propagate_mbqc_cnot_byproduct_frame,
    verify_exhaustive_f2_linearity_of_mbqc_cnot,
    generate_dcp_measurement_based_mbqc_cluster_state_cnot_peeling_certificate,
)


def test_mbqc_byproduct_frame_rules():
    # X on control spreads to target; Z on target spreads to control
    res_xc = propagate_mbqc_cnot_byproduct_frame((1, 0), (0, 0), (0, 0))
    assert res_xc["x_out"] == (1, 1) and res_xc["z_out"] == (0, 0)
    res_zt = propagate_mbqc_cnot_byproduct_frame((0, 0), (0, 1), (0, 0))
    assert res_zt["x_out"] == (0, 0) and res_zt["z_out"] == (1, 1)


def test_mbqc_certificate():
    cert = generate_dcp_measurement_based_mbqc_cluster_state_cnot_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_mbqc_byproduct_frame_rules()
    test_mbqc_certificate()
    print("Subsystem 142 tests PASSED")
