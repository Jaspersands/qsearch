"""Original mixed density instruments, weighted optimization and noise falsifiers."""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from theorems.dcp_adaptive_affine_packet_receiver import REPORT as SOURCE_REPORT
from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic as probability
from theorems.dcp_affine_packet_noise import (
    MODEL, REPORT, build_report, execute_noise_policy, pair_visibility,
    solve_noise, validate_visibilities,
)

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_affine_packet_noise_crosscheck.js"


@pytest.fixture(scope="module")
def source():
    return json.loads(SOURCE_REPORT.read_text())


@pytest.fixture(scope="module")
def report():
    return build_report()


def source_case(source, key):
    return {"unfiltered-seed-2": source["source_controls"][2],
            "unfiltered-seed-5": source["source_controls"][5],
            "selected-grammar-gap-94": source["affine_grammar_gap_counterexample"]}[key]


def product_density(case, secret, visibilities):
    q = 1 << case["phase_bits"]
    A = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
    rho = np.ones((1, 1), complex)
    for i in reversed(range(case["input_qubits"])):
        angle = 2 * math.pi * (sum(s * row[i] for s, row in zip(secret, A)) % q) / q
        off = float(visibilities[i]) * np.exp(-1j * angle)
        rho = np.kron(rho, np.array([[1, off], [off.conjugate(), 1]]) / 2)
    return rho


def mixed_port(case, secret, visibilities, target):
    density = product_density(case, secret, visibilities)
    total_probability = 1.0
    retained = None
    m = case["input_qubits"]
    def project(vertices):
        nonlocal density, total_probability
        new = np.zeros_like(density)
        new[np.ix_(vertices, vertices)] = density[np.ix_(vertices, vertices)]
        p = float(np.trace(new).real)
        assert p > 0
        total_probability *= p
        density = new / p
        return p
    def measure_initial_parity(rows):
        def syndrome(x):
            return sum(((b & x).bit_count() & 1) << j for j, b in enumerate(rows))
        observed = syndrome(target)
        allowed = [x for x in range(1 << m) if syndrome(x) == observed]
        assert project(allowed) == pytest.approx(1 / (1 << case["initial_parity_rank"]))
        return observed
    def measure_chart_linear(basis, origin, form):
        coordinates = {}
        for z in range(1 << len(basis)):
            x = origin
            for j, u in enumerate(basis):
                if z >> j & 1:
                    x ^= u
            coordinates[x] = z
        observed = (coordinates[target] & form).bit_count() & 1
        allowed = [x for x, z in coordinates.items() if ((z & form).bit_count() & 1) == observed]
        assert project(allowed) == pytest.approx(0.5)
        return observed
    def retain_pair(origin, direction):
        nonlocal retained
        retained = density[np.ix_([origin, origin ^ direction], [origin, origin ^ direction])]
        return "opaque-mixed-register"
    port = SimpleNamespace(measure_initial_parity=measure_initial_parity,
                           measure_chart_linear=measure_chart_linear, retain_pair=retain_pair)
    return port, lambda: (total_probability, retained)


@pytest.mark.parametrize("setting", ["3/4", "heterogeneous"])
@pytest.mark.parametrize("secret_seed", [0, 3])
def test_actual_original_mixed_instrument_all_outcomes(source, report, setting, secret_seed):
    for noisy in report["noise_controls"]:
        if noisy["noise_setting"] != setting:
            continue
        case = source_case(source, noisy["source_control"])
        secret = tuple(secret_seed + j for j in range(case["component_count"]))
        visibilities = tuple(probability(v) for v in noisy["visibility_by_original_register"])
        total, utility, label_success = 0.0, 0.0, 0.0
        for leaf_id in noisy["chosen_leaf_ids"]:
            leaf = case["states"][leaf_id]
            origin, direction = int(leaf["origin_hex"], 16), int(leaf["basis_hex"][0], 16)
            port, audit = mixed_port(case, secret, visibilities, origin)
            receipt = execute_noise_policy(case, noisy, port)
            mass, rho = audit()
            assert receipt["leaf_id"] == leaf_id
            assert receipt["unknown_output_receipt"] == "opaque-mixed-register"
            v = pair_visibility(visibilities, direction)
            assert probability(receipt["conditional_visibility_UNDER_PRODUCT_PROMISE"]) == v
            labels = tuple(int(a, 16) for a in leaf["output_label_hex"])
            Q = 1 << (case["phase_bits"] - 1)
            angle = 2 * math.pi * (sum(s*a for s,a in zip(secret, labels)) % Q) / Q
            off = float(v) * np.exp(-1j * angle)
            expected = np.array([[1, off], [off.conjugate(), 1]]) / 2
            assert np.allclose(rho, expected, atol=2e-14)
            assert mass == pytest.approx(2 / (1 << case["input_qubits"]))
            total += mass
            utility += mass * receipt["useful_descent"] * float(v)
            label_success += mass * receipt["useful_descent"]
        assert total == pytest.approx(1)
        assert utility == pytest.approx(float(probability(noisy["noise_aware_useful_retained_visibility"])))
        assert label_success == pytest.approx(float(probability(noisy["useful_label_probability_under_selected_noisy_policy"])))


def test_exact_original_input_trace_distance_not_a_marginal_union_heuristic(source, report):
    for noisy in report["noise_controls"]:
        case = source_case(source, noisy["source_control"])
        visibilities = tuple(probability(v) for v in noisy["visibility_by_original_register"])
        secret = tuple(1+j for j in range(case["component_count"]))
        rho = product_density(case, secret, visibilities)
        pure = product_density(case, secret, (1,) * case["input_qubits"])
        trace_distance = sum(abs(np.linalg.eigvalsh(rho-pure))) / 2
        assert trace_distance == pytest.approx(float(probability(noisy["exact_product_input_trace_distance_from_ideal"])), abs=2e-14)


def test_optimization_changes_when_actual_noise_weights_change(report):
    improved = []
    for noisy in report["noise_controls"]:
        optimum = probability(noisy["noise_aware_useful_retained_visibility"])
        frozen = probability(noisy["frozen_pure_policy_useful_retained_visibility"])
        static = probability(noisy["noise_aware_best_static_useful_retained_visibility"])
        arbitrary = probability(noisy["arbitrary_pairing_useful_retained_visibility_upper_bound"])
        assert max(frozen, static) <= optimum <= arbitrary <= 1
        if optimum > frozen:
            improved.append((noisy["source_control"], noisy["noise_setting"]))
        if noisy["noise_setting"] == "0":
            assert optimum == static == arbitrary == 0
    assert ("unfiltered-seed-2", "heterogeneous") in improved
    assert ("selected-grammar-gap-94", "3/4") in improved


def test_exact_physical_mask_law_not_all_leaves_or_merge_depth():
    visibility = (Fraction(1, 2), Fraction(3, 4), Fraction(15, 16), Fraction(1))
    assert pair_visibility(visibility, 5) == Fraction(15, 32)
    assert pair_visibility(visibility, 8) == 1
    assert pair_visibility(visibility, 15) == Fraction(45, 128)


def test_correlated_source_has_same_marginals_but_different_retained_coherence(report):
    c = report["correlation_counterexample"]
    rho = np.array(c["joint_density_numerators_denominator_8"]) / 8
    assert np.linalg.eigvalsh(rho).min() > -1e-14
    assert np.trace(rho) == 1
    for bit in range(3):
        reduced = np.zeros((2, 2))
        for x in range(8):
            for y in range(8):
                if (x & ~(1 << bit)) == (y & ~(1 << bit)):
                    reduced[x >> bit & 1, y >> bit & 1] += rho[x,y]
        assert np.allclose(reduced, np.eye(2)/2)
    pair = rho[np.ix_([0,3],[0,3])]
    pair /= np.trace(pair)
    assert np.allclose(pair, np.ones((2,2))/2)
    assert 2 * pair[0,1] == probability(c["actual_even_weight_pair_visibility"])
    assert pair_visibility((0,0,0), 3) == 0
    assert c["flat_diagonal_alone_implies_visibility_factorization"] is False


def test_existing_full_qft_sine_source_finite_conditional_noise_bridge():
    from theorems.lattice_sine_window_source import SineWindowSource, exact_reference, audit_template
    source = SineWindowSource(((17, 0), (16, 1)), 7, 1, 0, 2, 4)
    reference = exact_reference(source)
    # Private forward audit AFTER public source construction, never policy input.
    audit = audit_template(source, reference, (1, -1))
    assert audit["finite_marginal_template_matches"] is True
    assert audit["full_growing_reduction_certified"] is False
    shift, N = audit["PRIVATE_AUDIT_ONLY_cyclic_shift"], source.phase_modulus
    def value(poly):
        return sum(float(Fraction(a)) * np.exp(2j * math.pi * i / reference["reference_root"])
                   for i, a in enumerate(reversed(poly)))
    assert value(audit["exact_marginal_visibility"]) == pytest.approx(0.25)
    for outcome in reference["all_label_outcomes"]:
        mass = value(outcome["joint_label_probability"]).real
        rho = np.array([[value(x) for x in row] for row in outcome["unnormalized_colour_density"]]) / mass
        angle = 2 * math.pi * (outcome["label"] * shift % N) / N
        off = 0.25 * np.exp(-1j * angle)
        expected = np.array([[1,off],[off.conjugate(),1]])/2
        assert mass == pytest.approx(1/N)
        assert np.allclose(rho,expected,atol=2e-14)
    # Conditional tensor products follow for independent fresh preparations;
    # no conclusion about correlated shots, truncated QFTs, or trial selection.


def test_public_visibility_lower_bounds_give_conservative_fixed_policy_utility(source):
    case = source["source_controls"][2]
    lower = (Fraction(1,2),)*case["input_qubits"]
    actual = (Fraction(3,4),)*case["input_qubits"]
    policy = solve_noise(case,lower)
    true_utility = sum(pair_visibility(actual,int(case["states"][i]["basis_hex"][0],16))
                       for i in policy["chosen_leaf_ids"] if case["states"][i]["useful_descent"])
    true_utility *= Fraction(2,1 << case["input_qubits"])
    assert true_utility >= probability(policy["noise_aware_useful_retained_visibility"])


def test_nonflat_populations_break_the_fair_measurement_premise():
    rho = np.kron(np.diag([0.9,0.1]), np.diag([0.9,0.1]))
    even_parity_mass = rho[0,0] + rho[3,3]
    assert even_parity_mass == pytest.approx(0.82)
    assert even_parity_mass != 0.5
    conditional_pair = rho[np.ix_([0,3],[0,3])] / even_parity_mass
    assert not np.allclose(np.diag(conditional_pair), [0.5,0.5])


@pytest.mark.parametrize("value", [Fraction(1,3), -1, 2, True, 0.5, "1/2", Fraction(1,1<<300)])
def test_invalid_or_implicitly_rounded_noise_inputs_rejected(value):
    with pytest.raises(ValueError): validate_visibilities((value,))


def test_correlation_and_wrong_original_register_count_do_not_inherit_law(source):
    case = source["source_controls"][2]
    with pytest.raises(ValueError, match="premise"):
        solve_noise(case, (1,)*case["input_qubits"], source_model="correlated-marginals-only")
    with pytest.raises(ValueError, match="ORIGINAL"):
        solve_noise(case, (1,))


def run_checker(payload, tmp_path):
    target = tmp_path / "certificate.json"
    target.write_text(json.dumps(payload))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_matching_dp(report, tmp_path):
    assert json.loads(REPORT.read_text()) == report
    assert hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest() == report["source_geometry_sha256"]
    done = run_checker(report,tmp_path)
    assert done.returncode == 0,done.stderr
    assert json.loads(done.stdout)["weighted_matching_checker"] == "independent exact subset DP"


@pytest.mark.parametrize("mutation", ["score","policy","matching","visibility","trace","scope","correlation","provenance"])
def test_forged_noise_and_mathematical_claims_rejected(report,tmp_path,mutation):
    bad = deepcopy(report)
    c = bad["noise_controls"][1]
    if mutation == "score": c["scaled_optimal_weighted_good_assignments_by_state"][0] += 1
    elif mutation == "policy": c["chosen_form_by_state"][-1] = 0
    elif mutation == "matching": c["arbitrary_weighted_pairings"][0]["scaled_weight_sum"] += 1
    elif mutation == "visibility": c["visibility_by_original_register"][0]["numerator_hex"] = "0x1"
    elif mutation == "trace": c["exact_product_input_trace_distance_from_ideal"]["numerator_hex"] = "0x0"
    elif mutation == "scope": bad["scope"]["arbitrary_correlated_contamination_covered"] = True
    elif mutation == "correlation": bad["correlation_counterexample"]["joint_density_numerators_denominator_8"][0][3] = 0
    else: bad["source_geometry_sha256"] = "0"*64
    assert run_checker(bad,tmp_path).returncode != 0


def test_read_only_cli_does_not_rewrite_artifact():
    before = REPORT.read_bytes()
    done = subprocess.run([sys.executable,"qsearch.py","dcp-affine-packet-noise","--no-write"],
                          cwd=ROOT,capture_output=True,text=True)
    assert done.returncode == 0,done.stderr
    assert json.loads(done.stdout)["actual_lattice_noise_matched"] is False
    assert REPORT.read_bytes() == before
