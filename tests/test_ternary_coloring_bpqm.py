from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
import pytest

from theorems import ternary_coloring_bpqm as audit


CHANNELS = (audit.PHYSICAL, (1, 0, 0), (Fraction(1, 3),)*3,
            (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)))


def test_negative_overlap_is_not_its_absolute_value():
    states = np.array([audit.state(audit.PHYSICAL, u) for u in range(3)]).T
    Gram = states.conj().T @ states
    assert np.allclose(Gram, np.full((3, 3), -0.5)+1.5*np.eye(3), atol=1e-12)
    assert np.linalg.matrix_rank(Gram, tol=1e-12) == 2
    assert np.allclose(np.linalg.eigvalsh(Gram), [0, 1.5, 1.5], atol=1e-12)
    assert Gram[0, 1]*Gram[1, 2]*Gram[2, 0] == pytest.approx(-Fraction(1, 8))
    positive = np.full((3, 3), 0.5)+0.5*np.eye(3)
    assert np.linalg.matrix_rank(positive) == 3
    assert positive[0, 1]*positive[1, 2]*positive[2, 0] == Fraction(1, 8)


def test_signed_native_source_has_a_fixed_basis_change_and_copying_changes_it():
    record = audit.signed_source_control()
    assert record["fixed_basis_change_residual"] < 1e-12
    assert not record["extra_copies_or_postselection_used"]
    assert record["two_identical_copies_normalized_spectrum"] == ["1/2", "1/4", "1/4"]
    assert record["duplicating_source_changes_zero_temperature_target"]
    assert audit.bit_spectrum(audit.PHYSICAL, audit.PHYSICAL)[0] > 0


@pytest.mark.parametrize("mu,nu", product(CHANNELS, repeat=2))
def test_actual_qutrit_unitaries_keep_all_amplitudes_and_herald_phases(mu, nu):
    record = audit.local_control(mu, nu)
    assert record["amplitude_identity_max_residual"] < 1e-12
    assert record["unitarity_max_residual"] < 1e-12
    assert record["herald_phase_OMEGA_to_x_h_retained"]
    assert not record["large_coherent_reliability_compiler_supplied"]


@pytest.mark.parametrize("mu,nu", product(CHANNELS, repeat=2))
def test_sum_check_density_blocks_independently_match_original_mixture(mu, nu):
    check, _ = audit.node_gates(mu, nu)
    for u in range(3):
        original = np.zeros((9, 9), complex)
        for x in range(3):
            psi = np.kron(audit.state(mu, x), audit.state(nu, (u-x) % 3))
            original += np.outer(psi, psi.conj())/3
        expected = np.zeros_like(original)
        for h, probability, message in audit.check_branches(mu, nu):
            psi = audit.state(message, u)
            expected[3*h:3*h+3, 3*h:3*h+3] = float(probability)*np.outer(psi, psi.conj())
        assert np.allclose(check @ original @ check.conj().T, expected, atol=1e-12)


def test_dropping_a_herald_phase_fails_even_though_density_statistics_agree():
    check, _ = audit.node_gates(audit.PHYSICAL, audit.PHYSICAL)
    actual = check @ np.kron(audit.state(audit.PHYSICAL, 1), audit.state(audit.PHYSICAL, 2))
    wrong = np.zeros(9, complex)
    for h, p, mu in audit.check_branches(audit.PHYSICAL, audit.PHYSICAL):
        wrong[3*h:3*h+3] = np.sqrt(float(p))*audit.state(mu, 0)
    assert np.linalg.norm(actual-wrong) > 1
    assert np.allclose(abs(actual)**2, abs(wrong)**2)


@pytest.mark.parametrize("mu", CHANNELS)
def test_exact_outward_PGM_error_bounds_include_independent_Gram_calculation(mu):
    lower, upper = audit.error_bounds(mu)
    states = np.array([audit.state(mu, u) for u in range(3)]).T
    values = np.linalg.eigvalsh(states.conj().T @ states)
    error = 1-sum(np.sqrt(np.maximum(0, values)))**2/9
    assert float(lower)-1e-8 <= error <= float(upper)+1e-8
    assert 0 <= lower <= upper <= Fraction(2, 3)
    assert upper-lower <= Fraction(2, 1 << 64)


@pytest.mark.parametrize("degree", (3, 4, 5, 6))
def test_exact_tree_density_is_normalized_and_does_not_claim_a_block_decoder(degree):
    record = audit.density_probe(degree)
    assert len(record["history"]) >= 2
    for row in record["history"]:
        assert row["probability_mass_exact"] == "1"
        assert Fraction(row["symbol_error_lower_exact"]) <= Fraction(row["symbol_error_upper_exact"])
        assert 0 <= Fraction(row["mean_squared_overlap_exact"]) <= 1
    assert not record["convergence_or_finite_block_error_proved"]
    assert not record["cyclic_graph_channels_reused_or_cloned"]
    assert record["cyclic_gauge_used_for_density_ONLY"]


def test_density_caps_never_promote_a_partial_or_renormalized_law():
    record = audit.density_probe(4, states_cap=1)
    assert record["history"] == [] and "UNKNOWN" in record["status"]
    record = audit.density_probe(4, pairs_cap=1)
    assert record["history"] == [] and "UNKNOWN" in record["status"]


@pytest.mark.parametrize("children", range(1, 6))
def test_singular_support_scalar_law_matches_actual_check_branches(children):
    full = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    rotated = (Fraction(1, 2), Fraction(0), Fraction(1, 2))
    for singular in range(children+1):
        channels = [rotated if j % 2 else audit.PHYSICAL for j in range(singular)]+[full]*(children-singular)
        record = audit.singular_support_control(channels)
        expected = 1-Fraction(2, 2**singular) if singular else Fraction(0)
        assert Fraction(record["actual_singular_output_mass_exact"]) == expected
        assert record["full_branch_mass_exact"] == "1"
    # Independently integrate the fixed support-count law over Bernoulli inputs.
    from math import comb
    for p in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
        direct = sum(comb(children, s)*p**s*(1-p)**(children-s)*(1-Fraction(2, 2**s))
                     for s in range(1, children+1))
        assert direct == audit.singular_step(p, children)


@pytest.mark.parametrize("degree", (3, 4, 5, 6))
def test_singular_recursion_matches_full_exact_density_not_only_scalar_producer(degree):
    probability = Fraction(1)
    record = audit.density_probe(degree)
    for row in record["history"]:
        probability = audit.singular_step(probability, degree-1)
        assert Fraction(row["singular_message_mass_exact"]) == probability


@pytest.mark.parametrize("degree", (3, 4, 5))
def test_all_depth_singularity_contraction_is_not_a_decoding_certificate(degree):
    record = audit.singular_density_certificate(degree)
    assert record["singular_mass_vanishes_certified"]
    assert Fraction(record["contraction"]["lambda_upper_exact"]) < 1
    assert not record["word_or_symbol_error_vanishes_inferred"]
    assert not record["cyclic_or_finite_block_receiver_constructed"]
    # Exact grid counterchecks supplement, not replace, the written inequality.
    factor = Fraction(record["global_geometric_factor_upper_exact"])
    for i in range(101):
        p = Fraction(i, 100)
        assert audit.singular_step(p, degree-1) <= factor*p
    upper = Fraction(1)
    for row in record["history"]:
        upper = audit.singular_step(upper, degree-1)
        assert upper <= Fraction(row["singular_mass_upper_exact"])


def test_six_regular_tree_has_a_persistent_singular_branch_even_when_error_improves():
    record = audit.singular_density_certificate(6)
    assert not record["singular_mass_vanishes_certified"]
    assert record["contraction"] is None
    assert audit.singular_step(Fraction(1, 2), 5) == Fraction(285, 512) > Fraction(1, 2)
    assert all(Fraction(row["singular_mass_upper_exact"]) >= Fraction(1, 2) for row in record["history"])


def test_support_recursion_requires_the_specific_singular_channel_not_just_any_rank_loss():
    with pytest.raises(ValueError):
        audit.singular_support_control([(1, 0, 0)])
    with pytest.raises(ValueError):
        audit.singular_step(Fraction(3, 2), 3)


@pytest.mark.parametrize("vertices,edges", (
    (3, tuple(combinations(range(3), 2))), (4, tuple(combinations(range(4), 2))),
    (4, ((0, 1), (1, 2), (2, 3))),
))
def test_all_original_offset_colorings_match_the_ternary_code_reduction(vertices, edges):
    code = audit.graph_code(vertices, edges)
    counts = {}
    for word in product((1, 2), repeat=len(edges)):
        s = audit.syndrome(code, word)
        counts[s] = counts.get(s, 0)+1
    for offsets in product(range(3), repeat=len(edges)):
        actual = sum(audit.valid_coloring(code, offsets, (0,)+colors)
                     for colors in product(range(3), repeat=vertices-1))
        assert actual == counts.get(audit.syndrome(code, offsets), 0)
    record = audit.exact_graph_control(vertices, edges)
    assert record["spectral_identity_max_residual"] < 1e-12
    assert record["physical_product_source_Gram_residual"] < 1e-12
    assert record["total_nonzero_source_words"] == 2**len(edges)
    assert record["all_empty_sectors_retained_not_rerolled"]


def test_K4_empty_target_and_actual_Gram_rank_defect_are_not_discarded():
    record = audit.exact_graph_control(4, tuple(combinations(range(4), 2)))
    assert record["ordinary_graph_gauge_fixed_colorings"] == 0
    assert record["Gram_rank_exact_from_all_sectors"] == 26
    assert record["ANY_uniform_codeword_decoder_error_lower_exact"] == "1/27"
    assert record["uniform_original_offset_colorability_probability_exact"] == "26/27"
    empty = [r for r in record["all_sector_rows"] if r["gauge_fixed_colorings"] == 0]
    assert len(empty) == 1 and empty[0]["syndrome"] == (0, 0, 0)
    assert empty[0]["status"] == "EMPTY_TARGET_NO_NORMALIZED_COLORING_LAW"


def test_binary_constant_gap_repair_fails_even_between_nonempty_coloring_targets():
    from flint import nmod_mat
    record = audit.compressed_shift_countercontrol()
    zeros = record["all_zero_transitions_between_NONEMPTY_sectors"]
    assert len(zeros) == 12
    for row in zeros:
        assert row["source_valid_count"] > 0 and row["target_valid_count"] > 0
        assert row["actual_compressed_shift_norm_numeric"] < 1e-12
        columns = row["information_coordinate_extension"]
        assert row["edge"] in columns
        assert nmod_mat([[b[j] for j in columns] for b in record["cycle_basis_rows"]], 3).rank() == 3
    assert not record["binary_uniform_gap_lemma_extends_to_this_ternary_source"]
    assert not record["all_quantum_coloring_or_BPQM_algorithms_excluded"]


@pytest.mark.parametrize("vertices", (8, 64, 256, 1024))
def test_six_regular_family_cannot_have_a_reliable_uniform_word_decoder(vertices):
    record = audit.regular_word_rank_bound(vertices, 6)
    assert Fraction(record["ANY_uniform_word_decoder_success_upper_exact"]) == Fraction(1, 3)*Fraction(8, 9)**vertices
    assert record["uniform_original_offset_colorability_upper_exact"] == record["ANY_uniform_word_decoder_success_upper_exact"]
    assert not record["arbitrary_fixed_offset_colorability_bound_inferred"]
    assert not record["coloring_or_sampling_impossibility_inferred"]
    # Local tree-error improvement is compatible with this GLOBAL obstruction.
    probe = audit.density_probe(6, levels=2)
    assert Fraction(probe["history"][1]["symbol_error_upper_exact"]) < Fraction(1, 3)
    assert not probe["convergence_or_finite_block_error_proved"]


def test_classical_SAT_returns_only_original_verified_colorings_and_keeps_UNSAT():
    pytest.importorskip("z3")
    triangle = audit.graph_code(3, tuple(combinations(range(3), 2)))
    record = audit.classical_sat(triangle, (0, 0, 0))
    assert record["status"] == "CLASSICAL_ORIGINAL_COLORING_WITNESS"
    assert audit.valid_coloring(triangle, (0, 0, 0), record["colors"])
    clique = audit.graph_code(4, tuple(combinations(range(4), 2)))
    record = audit.classical_sat(clique, (0,)*6)
    assert record["status"] == "SOLVER_UNSAT_NOT_AN_INDEPENDENT_GENERAL_PROOF"
    assert not record["quantum_advantage_inferred"]


@pytest.mark.parametrize("call", (
    lambda: audit.spectrum((1, 1, 0)), lambda: audit.spectrum((-1, 1, 1)),
    lambda: audit.spectrum((0., .5, .5)),
    lambda: audit.graph_code(3, ((0, 1),)), lambda: audit.graph_code(3, ((1, 0), (1, 2))),
    lambda: audit.graph_code(3, ((0, 1), (0, 1), (1, 2))),
    lambda: audit.exact_graph_control(6, tuple(combinations(range(6), 2))),
    lambda: audit.regular_word_rank_bound(5, 3), lambda: audit.density_probe(2),
))
def test_model_and_exponential_reference_gates(call):
    with pytest.raises(ValueError):
        call()


def test_live_report_binds_sources_and_has_no_quantum_algorithm_promotion():
    report = json.loads(audit.REPORT.read_text())
    assert report["producer_sha256"] == hashlib.sha256(Path(audit.__file__).read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((audit.ROOT/"theorems"/name).read_bytes()).hexdigest()
    assert report["physical_overlap_exact"] == "-1/2"
    assert not report["natural_family_word_decoder_implemented"]
    assert not report["zero_temperature_sampling_reduction_executed"]
    assert not report["accepted_speedup_candidate"] and not report["speedup_claim_allowed"]
    assert all(not row["source_conditioned_on_colorability_or_success"] for row in report["classical_original_input_baselines"])
