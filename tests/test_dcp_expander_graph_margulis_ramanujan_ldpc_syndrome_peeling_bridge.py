"""Unit tests for Subsystem 152: Expander Graph Ramanujan Spectral Gap & LDPC Peeling Bridge."""

from theorems.dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_bridge import (
    generate_dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_certificate,
)


def test_expander_peeling_certificate():
    cert = generate_dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())


if __name__ == "__main__":
    test_expander_peeling_certificate()
    print("Subsystem 152 tests PASSED")
