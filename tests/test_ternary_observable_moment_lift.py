from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest
from sympy import Matrix, eye

from ternary_character_synchronization import rank_one_character_lift
from ternary_covariant_noise import CovariantRecord
from ternary_observable_moment_lift import (
    BASE_REPORT, DERIVATION, REPORT, difference_basis, full_moment_stencils,
    native_falsifier, observable_refinement, partition_witness, residual_budget, run_controls,
)


@pytest.fixture(scope="module")
def controls():
    return run_controls()["native_controls"]


def records(c):
    return tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                 for r in c["records"])


@pytest.mark.parametrize("index", [0, 1, 2])
def test_full_native_moment_partition_is_PSD_but_not_a_character_mixture(controls, index):
    c = controls[index]
    base = json.loads(BASE_REPORT.read_text())["native_controls"][index]["adaptive_character_lift"]
    r = records(c)
    classes = np.array(c["partition_witness"]["class_labels"])
    gram = (classes[:, None] == classes[None, :]).astype(float)
    assert np.linalg.eigvalsh(gram).min() > -1e-10
    assert np.linalg.matrix_rank(gram, tol=1e-8) == c["partition_witness"]["matrix_rank_exact"]
    stencils, stats = full_moment_stencils(base, r[0].modulus)
    for s in stencils:
        assert gram[tuple(s["left_entry"])] == gram[tuple(s["right_entry"])]
    assert stats["all_moment_entries_checked"] == len(classes)**2
    assert all(gram[a, b] == 1 for a, b in c["saturated_native_pairs"])
    assert all(gram[i, 0] == 0 for i in c["original_native_nodes"])
    assert c["noncharacter_mixture_falsifier_certified"]
    assert not c["pointwise_representation_failure_is_random_source_decoder_failure"]


@pytest.mark.parametrize("index", [0, 1, 2])
def test_full_root_difference_basis_is_certified_without_prime_modulus_assumption(controls, index):
    c = controls[index]
    r = records(c)
    q = r[0].modulus
    basis = c["difference_basis"]
    D = Matrix([[ (a-b) % q for a, b in zip(r[i].first, r[i].second)] for i in basis["basis_record_indices"]])
    I = Matrix(basis["modular_unit_difference_inverse"])
    assert (D*I).applyfunc(lambda x: int(x) % q) == eye(len(r[0].first))
    assert basis["rank_mod3"] == len(r[0].first)


@pytest.mark.parametrize("index", [0, 1, 2])
def test_rational_separation_and_repaired_all_rank_bound_are_recorded(controls, index):
    c = controls[index]
    repair = c["observable_refinement"]
    r = records(c)
    m, q = len(r), r[0].modulus
    C = sum(sum(x*x for x in t["balanced_basis_coefficients"]) for t in repair["observable_native_target_maps"])
    w = min(Fraction(1, m*q*q), Fraction(1, 1+C))
    assert repair["sum_native_balanced_coefficient_squared_norms"] == C
    assert Fraction(c["weighted_diagnostic"]["native_anchor_penalty"]) == w
    assert Fraction(c["weighted_diagnostic"]["true_character_maximum"]) == m-2*m*w
    assert Fraction(c["weighted_diagnostic"]["exact_integrality_gap"]) == 2*m*w > 0
    assert w*C < 1
    assert not c["weighted_diagnostic"]["is_native_noisy_likelihood_objective"]
    classes = c["saturated_repaired_partition"]["class_labels"]
    assert all(classes[i] == classes[0] for i in c["original_native_nodes"])


@pytest.mark.parametrize("index", [0, 1, 2])
def test_all_honest_characters_pass_observable_circuit_including_balanced_powers(controls, index):
    c = controls[index]
    repair = c["observable_refinement"]
    q, n = c["records"][0]["modulus"], len(c["records"][0]["first"])
    assert any(x < 0 for t in repair["observable_native_target_maps"] for x in t["balanced_basis_coefficients"])
    assert all(x["endpoint"] == 0 for x in repair["observable_basis_q_loops"])
    for secret in ((0,)*n, (q-1,)*n, tuple((2*j+1) % q for j in range(n))):
        exponents = [sum(a*s for a, s in zip(x["frequency"], secret)) % q for x in repair["nodes"]]
        for s in repair["linear_moment_stencils"]:
            a, b = s["left_entry"]
            d, e = s["right_entry"]
            assert (exponents[a]-exponents[b]-exponents[d]+exponents[e]) % q == 0


@pytest.mark.parametrize("index", [0, 1, 2])
def test_all_rank_error_bound_holds_after_arbitrary_character_twist(controls, index):
    c = controls[index]
    repair = c["observable_refinement"]
    r = records(c)
    q, n = r[0].modulus, len(r[0].first)
    center = tuple((2*j+1) % q for j in range(n))
    other = (q-1,)*n
    phases = lambda secret: np.exp(2j*math.pi*np.array([sum(a*s for a, s in zip(x["frequency"], secret)) % q for x in repair["nodes"]])/q)
    vectors = np.column_stack((math.sqrt(.37)*phases(center), math.sqrt(.63)*phases(other)))
    h = phases(center)
    deficits = 1-(np.conjugate(h)*np.einsum("ij,j->i", vectors, np.conjugate(vectors[0]))).real
    A = sum(deficits[repair["pair_difference_nodes"][i]] for i in repair["difference_basis"]["basis_record_indices"])
    B = sum(deficits[i] for i in c["original_native_nodes"])
    assert B <= repair["sum_native_balanced_coefficient_squared_norms"]*A+1e-10
    eps = np.linalg.norm(vectors-h[:, None]*vectors[0], axis=1)
    for s in repair["linear_moment_stencils"]:
        a, b = s["left_entry"]
        d, e = s["right_entry"]
        assert np.vdot(vectors[b], vectors[a]) == pytest.approx(np.vdot(vectors[e], vectors[d]))
        if s["kind"] == "addition":
            assert eps[a] <= eps[d]+eps[e]+1e-10
    A_all = sum(deficits[i] for i in repair["pair_difference_nodes"])
    weight = Fraction(repair["weighted_separating_score_anchor_weight"])
    score = len(r)-A_all-float(weight)*(2*len(r)-B)
    assert score <= float(Fraction(repair["weighted_diagnostic_repaired_all_rank_optimum"]))+1e-10


def test_bounded_native_calibration_exhaustively_checks_separating_objective():
    r = (CovariantRecord((1, 0), (0, 1), (2, 3), 9),
         CovariantRecord((1, 1), (1, 2), (1, 7), 9))
    repair = observable_refinement(r)
    w = float(Fraction(repair["weighted_separating_score_anchor_weight"]))
    scores = []
    for secret in product(range(9), repeat=2):
        total = 0.
        for record in r:
            a, c = [sum(x*s for x, s in zip(row, secret)) % 9 for row in (record.first, record.second)]
            total += math.cos(2*math.pi*(a-c)/9)-w*(math.cos(2*math.pi*a/9)+math.cos(2*math.pi*c/9))
        scores.append(total)
    assert max(scores) == pytest.approx(float(Fraction(repair["weighted_diagnostic_repaired_all_rank_optimum"])))
    assert scores[0] == max(scores)


def test_difference_rank_failure_is_unknown_not_a_false_falsifier():
    r = (CovariantRecord((1, 0), (1, 0), (2, 3), 9),)
    assert difference_basis(r)["rank_mod3"] == 0
    assert not observable_refinement(r)["observable_saturation_bound_certified"]
    assert not native_falsifier(r)["noncharacter_mixture_falsifier_certified"]


def test_partition_cap_and_circuit_caps_do_not_allow_partial_certification(controls):
    r = records(controls[0])
    base = rank_one_character_lift(r)
    with pytest.raises(ValueError, match="whole-table cap"):
        full_moment_stencils(base, r[0].modulus, max_entries=10)
    with pytest.raises(ValueError, match="node cap"):
        observable_refinement(r, max_nodes=10)
    with pytest.raises(ValueError, match="whole-table cap"):
        observable_refinement(r, max_entries=10)
    with pytest.raises(ValueError, match="outside complete node"):
        partition_witness(base, r[0].modulus, ((0, len(base["nodes"])),))


def test_circuit_and_falsifier_selection_are_outcome_blind(controls):
    original = records(controls[0])
    changed = tuple(CovariantRecord(r.first, r.second, tuple((x+1) % r.modulus for x in r.outcome), r.modulus) for r in original)
    other = native_falsifier(changed)
    c = controls[0]
    assert other["partition_witness"] == c["partition_witness"]
    assert other["weighted_diagnostic"] == c["weighted_diagnostic"]
    assert other["observable_refinement"]["linear_moment_stencils"] == c["observable_refinement"]["linear_moment_stencils"]
    for a, b in zip(other["observable_refinement"]["nodes"], c["observable_refinement"]["nodes"]):
        assert a["frequency"] == b["frequency"] and a["formal_coefficients"] == b["formal_coefficients"]


def test_live_artifact_pins_actual_native_source_and_scope(controls):
    report = json.loads(REPORT.read_text())
    assert report["native_controls"] == json.loads(json.dumps(controls))
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert report["source_report_sha256"] == hashlib.sha256(BASE_REPORT.read_bytes()).hexdigest()
    for key in ("full_group_or_secret_enumeration_used", "native_noisy_likelihood_tightness_or_decoder_proved", "quantum_speedup_proved", "candidate_record_accepted"):
        assert not report[key]


@pytest.mark.parametrize("index", [0, 1, 2])
def test_conditional_rational_residual_budget_and_fractional_counterfeit(controls, index):
    c = controls[index]
    repair = c["observable_refinement"]
    m = len(c["records"])
    C = repair["sum_native_balanced_coefficient_squared_norms"]
    betas = [6*sum(abs(x) for x in t["balanced_basis_coefficients"])+1 for t in repair["observable_native_target_maps"]]
    assert repair["per_native_target_stencil_residual_error_constants"] == betas
    E = sum(x*x for x in betas)
    w = Fraction(repair["weighted_separating_score_anchor_weight"])
    assert Fraction(repair["weighted_objective_excess_upper_per_max_complex_stencil_residual"]) == w*E/(1-w*C)
    threshold = Fraction(repair["max_stencil_residual_for_half_diagnostic_gap"])
    assert residual_budget(repair, threshold)["at_most_half_original_diagnostic_gap"]
    assert not residual_budget(repair, 2*threshold)["at_most_half_original_diagnostic_gap"]
    zero = residual_budget(repair, 0)
    assert zero["conditional_weighted_diagnostic_score_upper"] == repair["weighted_diagnostic_repaired_all_rank_optimum"]
    assert zero["condition_requires_exact_PSD_and_unit_diagonal"]
    assert not zero["floating_solver_eigenvalues_or_diagonal_certified"]
    # Extend the old orthogonal Gram with fresh singleton nodes, then mix with
    # the honest all-ones Gram. This is exactly PSD/unit diagonal, not feasible.
    labels = list(c["partition_witness"]["class_labels"])
    labels += list(range(len(labels), len(repair["nodes"])))
    residual = 0
    for s in repair["linear_moment_stencils"]:
        a, b = s["left_entry"]
        d, e = s["right_entry"]
        residual = max(residual, abs(int(labels[a] == labels[b])-int(labels[d] == labels[e])))
    assert residual == 1
    mixing = Fraction(1, 1000)
    B = 2*m*mixing
    assert B <= E*mixing  # Chosen basis pair deficits are exactly zero.
    actual_score = Fraction(repair["weighted_diagnostic_repaired_all_rank_optimum"])+2*m*w*mixing
    assert actual_score <= Fraction(residual_budget(repair, mixing)["conditional_weighted_diagnostic_score_upper"])


@pytest.mark.parametrize("bad", [-1, .0001, True, "1/1000"])
def test_residual_budget_requires_explicit_nonnegative_exact_rational(controls, bad):
    with pytest.raises(ValueError, match="exact rational"):
        residual_budget(controls[0]["observable_refinement"], bad)


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_observable_moment_lift_crosscheck.js"


def test_independent_full_translation_falsifier_and_repair_checker():
    p = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    report = json.loads(p.stdout)
    assert report["status"] == "PASS"
    assert report["original_full_moment_entries"] == 104804
    assert report["repaired_full_moment_entries"] == 509288
    assert not report["native_noisy_decoder_supplied"] and not report["external_IID_supply_certified"]


@pytest.mark.parametrize("mutation", ["class", "basis", "gap", "weight", "target", "stencil", "loop", "closure", "residual", "noisy_claim", "source"])
def test_independent_checker_rejects_corrupt_or_overclaimed_evidence(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    c = report["native_controls"][0]
    repair = c["observable_refinement"]
    if mutation == "class":
        c["partition_witness"]["class_labels"][1] = 0
    elif mutation == "basis":
        c["difference_basis"]["modular_unit_difference_inverse"][0][0] += 1
    elif mutation == "gap":
        c["weighted_diagnostic"]["exact_integrality_gap"] = "1"
    elif mutation == "weight":
        repair["weighted_separating_score_anchor_weight"] = "1"
    elif mutation == "target":
        repair["observable_native_target_maps"][-1]["balanced_basis_coefficients"][0] += 1
    elif mutation == "stencil":
        repair["linear_moment_stencils"].pop()
    elif mutation == "loop":
        repair["observable_basis_q_loops"][0]["endpoint"] = 1
    elif mutation == "closure":
        repair["complete_moment_closure"]["all_moment_entries_checked"] -= 1
    elif mutation == "residual":
        repair["max_stencil_residual_for_half_diagnostic_gap"] = "1"
    elif mutation == "noisy_claim":
        repair["noisy_recovery_or_general_convex_tightness_proved"] = True
    elif mutation == "source":
        c["records"][0]["first"][0] += 1
    target = tmp_path/"corrupt.json"
    target.write_text(json.dumps(report))
    p = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert p.returncode != 0
