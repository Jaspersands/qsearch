from fractions import Fraction
from itertools import product
import json
import math

import numpy as np
import pytest

from dcp_path_code_fusion import (
    compile_state, compiler, extract_branches, linear_label_countercontrol,
    logical_formula, measured_fusion_instrument, native_input, path_rows,
    run_controls, scaling_ledger, sign_distances,
)
from dcp_projective_code_admission import (
    _purified_instrument, _words, code_signal_certificate, overlapping_zero_branch,
    validate_code,
)


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("m", [2, 3, 4, 5])
def test_full_syndrome_formula_matches_independent_known_clifford_network(report, m):
    controls = [r for r in report["native_controls"] if r["pairs"] == m]
    assert controls
    for r in controls:
        assert r["maximum_compiler_formula_error"] < 2e-12
        assert r["maximum_measured_fusion_formula_error"] < 2e-12
        assert len(r["all_syndrome_probabilities"]) == 4**(m-1)
        assert sum(r["all_syndrome_probabilities"]) == pytest.approx(1)
        assert r["all_branches_charged"]
        assert r["all_Z_syndrome_marginals"] == pytest.approx([2**(1-m)]*2**(m-1))


def test_compiler_matches_original_purified_projective_instrument_all_syndromes():
    for m in (2, 3, 4):
        labels = list(range(1, 2*m+1))
        rows = path_rows(m)
        _, physical = _purified_instrument(rows, 32, 3, labels)
        branches = logical_formula(32, 3, labels)
        for y, state in enumerate(physical):
            decoded = extract_branches(compile_state(state, m), m)
            assert np.max(abs(decoded[y]-branches[y])) < 2e-12
            decoded[y] = 0
            assert np.max(abs(decoded)) < 2e-12


def test_channel_identity_on_every_computational_basis_input_not_only_phase_states():
    # Equality on every basis vector proves each finite Kraus map by linearity.
    m, D = 3, 64
    C = _words(path_rows(m))
    for v in range(D):
        source = np.zeros(D, complex)
        source[v] = 1
        actual = extract_branches(compile_state(source, m), m)
        row_masks = [sum(x << i for i, x in enumerate(row)) for row in path_rows(m)]
        z = sum(((v & mask).bit_count() % 2) << j for j, mask in enumerate(row_masks))
        for x in range(4):
            projected = np.zeros(D, complex)
            for b, mask in enumerate(C):
                projected[v ^ mask] = (-1)**((b & x).bit_count())/4
            decoded = extract_branches(compile_state(projected, m), m)
            y = z | x << 2
            assert np.max(abs(decoded[y]-actual[y])) < 2e-12
            decoded[y] = 0
            assert np.max(abs(decoded)) < 2e-12
        assert sum(abs(actual.ravel())**2) == pytest.approx(1)


def test_six_to_two_zero_syndrome_agrees_with_previous_paid_logical_a_formula(report):
    for r in report["native_controls"]:
        if r["pairs"] != 3:
            continue
        old = overlapping_zero_branch(32, 1, r["native_labels"])
        t = logical_formula(32, 1, r["native_labels"])[0]
        a = np.stack((t[:, 0]+t[:, 1], t[:, 0]-t[:, 1]), axis=1)/math.sqrt(2)
        assert np.max(abs(a.ravel()-[complex(*v) for v in old["unnormalized_logical_amplitudes"]])) < 2e-12


def test_measured_fusion_is_exact_common_parity_dephasing_not_full_coherent_equivalence(report):
    strict = 0
    for r in report["native_controls"]:
        m, labels = r["pairs"], r["native_labels"]
        coherent = extract_branches(compile_state(native_input(32, 1, labels), m), m)
        measured = measured_fusion_instrument(32, 1, labels)
        for u, v in zip(coherent, measured):
            for p in (0, 1):
                assert np.max(abs(np.outer(u[p], u[p].conj())-np.outer(v[p], v[p].conj()))) < 2e-12
        assert r["measured_pair_fusion_sign_trace_distance"] <= r["full_coherent_instrument_sign_trace_distance"]+2e-12
        strict += r["full_coherent_instrument_sign_trace_distance"] > r["measured_pair_fusion_sign_trace_distance"]+1e-4
    assert strict > 0


def test_sign_signal_does_not_require_coherent_pair_parity_and_even_paths_erase_it(report):
    controls = [r for r in report["native_controls"] if r["pairs"] == 3]
    assert len(controls) == 8
    assert {r["unfiltered_label_seed"] for r in controls} == set(range(43011, 43019))
    assert sum(r["measured_pair_fusion_sign_trace_distance"] > .01 for r in controls) >= 1
    for r in report["native_controls"]:
        assert r["classical_full_syndrome_total_variation"] < 2e-12
        assert not r["surviving_sign_signal_requires_common_parity_coherence"]
        assert r["measured_pair_fusion_sign_trace_distance"] == pytest.approx(r["measured_sign_distance_product_formula"])
        if r["pairs"] % 2 == 0:
            assert r["full_coherent_instrument_sign_trace_distance"] < 2e-12
            assert r["measured_pair_fusion_sign_trace_distance"] < 2e-12
        assert r["full_coherent_instrument_sign_trace_distance"] <= r["original_input_sign_trace_distance"]+2e-12


def test_path_code_all_ones_and_signal_ledger_use_exact_algebra_not_a_fitted_exponent():
    for m in range(2, 9):
        h, width, _, _ = validate_code(path_rows(m))
        assert h == m-1 and width == 2*m
        assert ((1 << width)-1 in _words(path_rows(m))) == (m % 2 == 0)
        cert = code_signal_certificate(path_rows(m))
        assert exact(scaling_ledger(m)["fixed_code_full_classical_kernel"]) == exact(cert["source_averaged_full_collision_kernel"])


def test_fixed_branch_mean_is_charged_and_is_not_expected_inverse_probability(report):
    for r in report["scaling_ledgers"]:
        m = r["pairs"]
        assert exact(r["IID_mean_fixed_coherent_syndrome_probability_nonzero_secret"]) == Fraction(1, 4**(m-1))
        assert exact(r["IID_mean_fixed_measured_parity_and_syndrome_probability_nonzero_secret"]) == Fraction(1, 2**(2*m-1))
        assert r["per_instance_success_lower_bound"] is None
        assert not r["label_adaptive_selection_covered_by_IID_mean"]
    # The full source average is uniform for nonzero secrets, but NOT at s=0.
    for s in (1, 2):
        total = np.zeros(4)
        for labels in product(range(8), repeat=4):
            total += np.sum(abs(logical_formula(8, s, labels))**2, axis=(1, 2))/8**4
        assert total == pytest.approx([.25]*4)
    zero = np.sum(abs(logical_formula(8, 0, [0]*4))**2, axis=(1, 2))
    assert np.max(abs(zero-.25)) > .1


def test_nonlinear_flat_phase_is_not_a_known_linear_DCP_label(report):
    r = report["linear_label_countercontrol"]
    assert r["flat_phase_does_not_imply_standard_DCP_label_closure"]
    assert r["minimum_over_known_labels_of_worst_secret_ratio_error"] > .1
    assert r["calibration_only_not_IID_source_evidence"]
    assert not r["arbitrary_nonlinear_decoders_excluded"]


def test_measured_fusion_full_public_label_mean_has_exact_exponential_sign_loss(report):
    # Pair independence gives the m-th power; labels remain part of the record.
    for N in (8, 16, 32):
        for s in (1, 3, 2):
            order = N//math.gcd(N, s)
            expectation = sum((abs(math.sin(2*math.pi*s*(k+l)/N))+
                               abs(math.sin(2*math.pi*s*(k-l)/N)))/2
                              for k in range(N) for l in range(N))/N**2
            assert expectation == pytest.approx((2/order)/math.tan(math.pi/order))
            assert expectation < 2/math.pi
    for r in report["scaling_ledgers"]:
        m = r["pairs"]
        expected = ((2/32)/math.tan(math.pi/32))**m if m % 2 else 0
        assert r["measured_fusion_IID_sign_distance_at_N32"] == pytest.approx(expected)
        assert not r["coherent_common_parity_protocol_covered_by_measured_decay"]


def test_public_compiler_has_linear_cost_and_no_state_inverse(report):
    for r in report["scaling_ledgers"]:
        m = r["pairs"]
        assert len(r["cnots_in_order"]) == r["CNOT_count"] == 3*m-2
        assert len(r["hadamards_after_cnots"]) == r["Hadamard_count"] == m
        assert r["measured_qubits"]+r["retained_qubits"] == 2*m
        assert not r["conditional_source_inverse_or_cloning"]
        assert not r["gate_choice_depends_on_secret_or_labels"]


def test_no_novel_primitive_or_algorithm_is_promoted(report):
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))


@pytest.mark.parametrize("call", [lambda: path_rows(1), lambda: compiler(True),
    lambda: compile_state(np.zeros(16), 7), lambda: native_input(8, 1, [0]*5),
    lambda: logical_formula(8, 8, [0]*6), lambda: measured_fusion_instrument(8, 1, [0]*3),
    lambda: linear_label_countercontrol(8, [0]*4)])
def test_invalid_promises_and_unbounded_enumerations_are_rejected(call):
    with pytest.raises(ValueError):
        call()
