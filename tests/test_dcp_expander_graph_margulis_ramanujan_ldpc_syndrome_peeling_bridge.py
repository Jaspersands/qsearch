"""Unit tests for Subsystem 152: Expander Graph Ramanujan Spectral Gap & Tanner Arithmetic Audit."""

from theorems.dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_bridge import (
    generate_dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_certificate,
)


def test_expander_peeling_certificate():
    cert = generate_dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert all(cert["theorem_checks"].values())
    assert cert["peeling_decoding_threshold_certified"] is False
    assert all(not r["guarantees_linear_time_peeling"] for r in cert["ramanujan_degree_sweep"])
    assert cert["falsification_status"]["accepted_speedup_candidate"] is False
    assert cert["falsification_status"]["novelty_claim"] is False


if __name__ == "__main__":
    test_expander_peeling_certificate()
    print("Subsystem 152 tests PASSED")
