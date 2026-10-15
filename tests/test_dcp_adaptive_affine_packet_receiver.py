"""Exact feedback policies, stronger pairing baseline and opaque-state replay."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import networkx as nx
import numpy as np
import pytest

from theorems.dcp_adaptive_affine_packet_receiver import (
    REPORT, Policy, ResearchCap, build_report, canonical_chart, evaluate_quadratic,
    execute_public_policy, gaussian_binomial, is_useful_descent, output_label,
    points, quadratic_low_phase_map, search_cost, solve, split_chart,
)
from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_adaptive_affine_packet_receiver_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_prefixed_unfiltered_source_controls_and_strict_nonzero_feedback_gains(report):
    assert [c["public_source_selection"]["seed"] for c in report["source_controls"]] == list(range(6))
    gains = []
    for case in report["source_controls"]:
        adaptive = decode_dyadic(case["optimal_feedback_useful_descent_probability"])
        static = decode_dyadic(case["best_static_useful_descent_probability"])
        pairing = decode_dyadic(case["arbitrary_basis_pairing_useful_descent_upper_bound"])
        assert 0 <= static <= adaptive <= pairing <= 1
        gains.append(adaptive - static)
        assert case["objective_excludes_zero_labels"] is True
        assert case["resource_ledger_per_supplied_packet"]["initial_syndromes_postselected"] is False
    assert gains == [0, 0, Fraction(1, 2), 0, 0, Fraction(1, 4)]
    assert report["efficient_receiver_supplied"] is False


def test_selected_counterexample_falsifies_affine_equals_arbitrary_pairing(report):
    gap = report["affine_grammar_gap_counterexample"]
    assert decode_dyadic(gap["optimal_feedback_useful_descent_probability"]) == Fraction(9, 16)
    assert decode_dyadic(gap["arbitrary_basis_pairing_useful_descent_upper_bound"]) == Fraction(11, 16)
    assert gap["public_source_selection"]["kind"].startswith("SELECTED-")
    assert gap["affine_policy_saturates_arbitrary_pairing_bound"] is False
    boundary = report["known_algorithm_boundary"]
    assert boundary["fixed_t_full_HSP_oracle_novelty_claim_allowed"] is False
    assert boundary["copy_only_phase_source_transfer_proved"] is False
    assert boundary["exact_theorem_requires_subgroup_state_creating_unitary_and_inverse"] is True


def brute_affine_probability(labels, t, root_points):
    """Enumerate ambient physical functionals, not the solver's chart routine."""
    m = len(labels[0])
    @lru_cache(None)
    def best(vertices):
        if len(vertices) == 2:
            return 2 * int(is_useful_descent(output_label(labels, t, *vertices)))
        splits = set()
        for form in range(1, 1 << m):
            left = tuple(x for x in vertices if (x & form).bit_count() % 2 == 0)
            if len(left) != len(vertices) // 2:
                continue
            right = tuple(x for x in vertices if x not in left)
            splits.add(tuple(sorted((left, right))))
        return max(best(a) + best(b) for a, b in splits)
    return Fraction(best(tuple(sorted(root_points))), len(root_points))


@pytest.mark.parametrize("labels", [((1, 2, 2, 11, 5),), ((1, 2, 3, 4), (2, 5, 7, 6))])
def test_bellman_optimum_matches_independent_ambient_measurement_search(labels):
    case = solve(labels)
    successes = Fraction(0)
    for identifier in case["root_ids_all_syndromes"]:
        state = case["states"][identifier]
        vertices = points(tuple(int(v, 16) for v in state["basis_hex"]), int(state["origin_hex"], 16))
        expected = brute_affine_probability(labels, 4, vertices)
        assert expected == Fraction(state["good_assignments"], len(vertices))
        successes += expected / len(case["root_ids_all_syndromes"])
    assert successes == decode_dyadic(case["optimal_feedback_useful_descent_probability"])


def test_arbitrary_pairing_bound_against_independent_maximum_matching(report):
    for case in report["source_controls"]:
        labels = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
        for identifier, bound in zip(case["root_ids_all_syndromes"], case["arbitrary_basis_pairing_bounds_all_syndromes"]):
            state = case["states"][identifier]
            vertices = points(tuple(int(v, 16) for v in state["basis_hex"]), int(state["origin_hex"], 16))
            graph = nx.Graph()
            graph.add_nodes_from(vertices)
            graph.add_edges_from((x, y) for x in vertices for y in vertices if x < y and
                                 is_useful_descent(output_label(labels, 4, x, y)))
            matching = nx.max_weight_matching(graph, maxcardinality=True)
            assert 2 * len(matching) == bound["maximum_good_assignments"]


def opaque_physical_port(case, secret, forced_point):
    """Unknown amplitudes stay in closures, never attached to controller port."""
    labels = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
    m, q = case["input_qubits"], 1 << case["phase_bits"]
    amplitude = np.array([np.exp(2j * math.pi * (sum(s * a * ((x >> i) & 1)
                        for s, row in zip(secret, labels) for i, a in enumerate(row)) % q) / q)
                        / math.sqrt(1 << m) for x in range(1 << m)])
    probability = 1.0
    density = None
    calls = []

    def project(allowed):
        nonlocal amplitude, probability
        new = np.zeros_like(amplitude)
        new[list(allowed)] = amplitude[list(allowed)]
        mass = float(np.vdot(new, new).real)
        assert mass > 0
        probability *= mass
        amplitude = new / math.sqrt(mass)
        return mass

    def measure_initial_parity(rows):
        syndrome = sum(((b & forced_point).bit_count() & 1) << j for j, b in enumerate(rows))
        allowed = [x for x in range(1 << m)
                   if sum(((b & x).bit_count() & 1) << j for j, b in enumerate(rows)) == syndrome]
        mass = project(allowed)
        assert mass == pytest.approx(1 / (1 << case["initial_parity_rank"]))
        calls.append("initial")
        return syndrome

    def measure_chart_linear(basis, origin, form):
        logical = {}
        for z in range(1 << len(basis)):
            x = origin
            for j, u in enumerate(basis):
                if z >> j & 1:
                    x ^= u
            logical[x] = z
        assert set(np.flatnonzero(abs(amplitude) > 1e-12)) == set(logical)
        outcome = (logical[forced_point] & form).bit_count() & 1
        allowed = [x for x, z in logical.items() if ((z & form).bit_count() & 1) == outcome]
        assert project(allowed) == pytest.approx(0.5)
        calls.append("complement")
        return outcome

    def retain_pair(origin, direction):
        nonlocal density
        assert set(np.flatnonzero(abs(amplitude) > 1e-12)) == {origin, origin ^ direction}
        state = amplitude[[origin, origin ^ direction]]
        density = np.outer(state, state.conj())
        calls.append("retain")
        return "opaque-unknown-phase-register"

    port = SimpleNamespace(measure_initial_parity=measure_initial_parity,
                           measure_chart_linear=measure_chart_linear, retain_pair=retain_pair)
    return port, lambda: (probability, density, calls)


@pytest.mark.parametrize("secret_seed", [0, 1, 3])
def test_actual_projector_execution_every_outcome_without_private_state_access(report, secret_seed):
    for case in report["source_controls"]:
        secret = tuple((secret_seed + 2*j) % 16 for j in range(case["component_count"]))
        total, success = 0.0, 0.0
        for leaf in case["chosen_policy_leaf_ids"]:
            target = int(case["states"][leaf]["origin_hex"], 16)
            port, audit = opaque_physical_port(case, secret, target)
            result = execute_public_policy(case, port)
            mass, density, calls = audit()
            assert result["leaf_id"] == leaf
            assert result["unknown_output_receipt"] == "opaque-unknown-phase-register"
            assert calls.count("complement") == case["root_kernel_dimension"] - 1
            assert mass == pytest.approx(2 / (1 << case["input_qubits"]))
            out = tuple(int(a, 16) for a in result["output_label_hex"])
            Q = 1 << (case["phase_bits"] - 1)
            angle = 2 * math.pi * (sum(s * a for s, a in zip(secret, out)) % Q) / Q
            state = np.array([1, np.exp(1j * angle)]) / math.sqrt(2)
            assert np.allclose(density, np.outer(state, state.conj()), atol=2e-14)
            total += mass
            success += mass * result["useful_descent"]
        assert total == pytest.approx(1)
        assert success == pytest.approx(float(decode_dyadic(case["optimal_feedback_useful_descent_probability"])))


def test_next_low_phase_is_quadratic_but_public_polynomial_is_not_state_oracle(report):
    for case in report["source_controls"]:
        labels = tuple(tuple(int(a, 16) for a in row) for row in case["public_labels_hex"])
        for record in case["root_quadratic_maps"]:
            state = case["states"][record["root_id"]]
            basis = tuple(int(v, 16) for v in state["basis_hex"])
            origin = int(state["origin_hex"], 16)
            assert record["public_polynomial_is_unknown_state_preparation_oracle"] is False
            for z in range(1 << len(basis)):
                x = origin
                for j, u in enumerate(basis):
                    if z >> j & 1:
                        x ^= u
                original = output_label(labels, case["phase_bits"], origin, x)
                low = sum((a & 1) << j for j, a in enumerate(original))
                assert evaluate_quadratic(record, z) == low
            shifted = quadratic_low_phase_map(labels, case["phase_bits"], basis, origin ^ basis[0])
            assert shifted["cross_terms"] == record["cross_terms"]


def test_zero_labels_receive_no_credit():
    case = solve(((0, 0, 0),))
    assert decode_dyadic(case["optimal_feedback_useful_descent_probability"]) == 0
    assert decode_dyadic(case["arbitrary_basis_pairing_useful_descent_upper_bound"]) == 0
    assert all(not state["useful_descent"] for state in case["states"] if state["dimension"] == 1)


def test_caps_are_unknown_not_negative_and_cost_is_not_polynomial():
    with pytest.raises(ResearchCap, match="UNKNOWN"):
        solve(((0,) * 8,))
    with pytest.raises(ResearchCap, match="work cap"):
        solve(((1, 2, 3, 4),), policy=Policy(max_states=1))
    ledger = search_cost(64, 0)
    assert ledger["all_syndromes_chart_states"] > 1 << 1000
    assert gaussian_binomial(4, 2) == 35
    with pytest.raises(ValueError):
        Policy(max_states=True)


def test_all_exported_measurements_partition_the_actual_affine_chart(report):
    for case in report["source_controls"]:
        for s in case["states"]:
            basis, origin = tuple(int(v, 16) for v in s["basis_hex"]), int(s["origin_hex"], 16)
            assert canonical_chart(basis, origin, case["input_qubits"]) == (basis, origin)
            for action in s["actions"]:
                generated = split_chart(basis, origin, action["form"], case["input_qubits"])
                child_points = [set(points(*chart)) for chart in generated]
                assert not child_points[0] & child_points[1]
                assert child_points[0] | child_points[1] == set(points(basis, origin))


def js_check(payload, tmp_path):
    target = tmp_path / "certificate.json"
    target.write_text(json.dumps(payload))
    return subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)


def test_live_artifact_and_independent_replay(report, tmp_path):
    assert json.loads(REPORT.read_text()) == report
    checked = js_check(report, tmp_path)
    assert checked.returncode == 0, checked.stderr
    assert json.loads(checked.stdout)["strict_feedback_gains"] == 2


@pytest.mark.parametrize("mutation", ["chosen", "branch", "score", "static", "zero", "scope", "cost", "quadratic", "distribution", "pairing"])
def test_checker_rejects_favorable_branch_or_mathematical_tampering(report, tmp_path, mutation):
    bad = deepcopy(report)
    case = bad["source_controls"][2]
    state = case["states"][case["root_ids_all_syndromes"][0]]
    if mutation == "chosen": state["chosen_form"] = 0
    elif mutation == "branch": state["actions"][0]["children"][0] = state["actions"][0]["children"][1]
    elif mutation == "score": state["actions"][0]["good_assignments"] += 2
    elif mutation == "static": case["static_comparator_all_syndromes"][0]["best_good_assignments"] = 0
    elif mutation == "zero": case["states"][0]["output_label_hex"] = ["0x0"]
    elif mutation == "scope": bad["scope"]["efficient_search_or_uniform_policy_family_supplied"] = True
    elif mutation == "cost": case["search_cost"]["all_syndromes_chart_states"] = 1
    elif mutation == "quadratic": case["root_quadratic_maps"][0]["linear_coefficients_hex"][0] = "0x7"
    elif mutation == "distribution": case["retained_label_distribution_all_outcomes"][0]["physical_outcome_pairs"] += 1
    else: case["arbitrary_basis_pairing_bounds_all_syndromes"][0]["maximum_good_assignments"] += 2
    assert js_check(bad, tmp_path).returncode != 0


def test_cli_no_write_provenance():
    before = REPORT.read_bytes()
    done = subprocess.run([sys.executable, "qsearch.py", "dcp-adaptive-affine-packet-receiver", "--no-write"],
                          cwd=ROOT, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["accepted_speedup_candidate"] is False
    assert REPORT.read_bytes() == before
