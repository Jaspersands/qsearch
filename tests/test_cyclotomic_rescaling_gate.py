from fractions import Fraction
from itertools import product
import json
import math

import numpy as np
import pytest
from sympy import Matrix, eye

from cyclotomic_rescaling_gate import (
    MPI, _lambda, affine_label_transport, divide_pi, elements, gaussian_plan, ideal_chart,
    level_classification, multiply, pairing, physical_merge, plus,
    reduce_element, rescale_label, residue, run_controls, uniform_source_control,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_index_rescaling_exactly_preserves_integer_secret_phase(level):
    for y in elements(level):
        for integer in range(3**math.ceil(level/2)):
            for j in range(3):
                old = pairing((integer, 0), multiply(y, _lambda(2*j % 3, level), level), level)
                new = pairing((integer, 0), multiply(rescale_label(y, 2, level), _lambda(j, level), level), level)
                assert old == new


def test_general_ring_secret_is_not_silently_given_integer_galois_invariance():
    level, secret = 3, (0, 1)
    mismatches = []
    for y in elements(level):
        for j in (1, 2):
            old = pairing(secret, multiply(y, _lambda(2*j % 3, level), level), level)
            new = pairing(secret, multiply(rescale_label(y, 2, level), _lambda(j, level), level), level)
            if old != new:
                mismatches.append((y, j))
    assert mismatches
    with pytest.raises(ValueError, match="integer-embedded"):
        physical_merge([[(1, 0)], [(1, 0)]], [secret], level)


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_every_ternary_basis_permutation_retains_global_phase_and_has_same_residue_gate(level):
    permutations = set()
    for a in (1, 2):
        for b in range(3):
            permutations.add(tuple((a*j+b) % 3 for j in range(3)))
            for y in elements(level):
                new = affine_label_transport(y, a, b, level)
                assert residue(new) == a**level*residue(y) % 3
                for j in range(3):
                    lhs = pairing((1, 0), multiply(y, _lambda((a*j+b) % 3, level), level), level)
                    rhs = (pairing((1, 0), multiply(y, _lambda(b, level), level), level)
                           +pairing((1, 0), multiply(new, _lambda(j, level), level), level)) % 1
                    assert lhs == rhs
    assert len(permutations) == 6


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_rescaling_is_well_defined_bijection_and_has_the_level_power_residue(level):
    ring = elements(level)
    assert set(rescale_label(y, 2, level) for y in ring) == set(ring)
    for y in ring:
        assert rescale_label(rescale_label(y, 2, level), 2, level) == y
        assert residue(rescale_label(y, 2, level)) == 2**level*residue(y) % 3
        for basis in (MPI**level).columnspace():
            lift = (y[0]+int(basis[0]), y[1]+int(basis[1]))
            assert rescale_label(lift, 2, level) == rescale_label(y, 2, level)


@pytest.mark.parametrize("level", [2, 3, 4, 5])
def test_rescaling_commutes_with_pi_division_at_the_correct_child_level(level):
    for z in elements(level-1):
        parent = multiply((-1, 1), z, level)
        child = divide_pi(rescale_label(parent, 2, level), level)
        assert child == rescale_label(z, 2, level-1)
        assert pairing((2, 0), parent, level) == pairing((2, 0), z, level-1)


@pytest.mark.parametrize("level", [1, 2, 3])
def test_trace_pairing_is_perfect_not_a_fake_finite_field(level):
    ring = elements(level)
    assert len(ring) == 3**level
    fourier = np.array([[np.exp(2j*math.pi*float(pairing(x, y, level)))
                         for y in ring] for x in ring])/math.sqrt(len(ring))
    assert np.max(abs(fourier @ fourier.conj().T-np.eye(len(ring)))) < 4e-12
    pi = (1, 0)
    for _ in range(level):
        before = pi
        pi = multiply(pi, (-1, 1), level)
    assert pi == (0, 0) and before != (0, 0)
    if level == 3:
        assert reduce_element((3, 0), level) != (0, 0)
        assert reduce_element((9, 0), level) == (0, 0)


@pytest.mark.parametrize("prime", [3, 5, 7])
def test_general_prime_rescaling_formula_against_exact_field_matrices(prime):
    # Independent rational power-basis matrices, not the FLINT p3 implementation.
    d = prime-1
    e0 = eye(d)[:, 0]
    Z = Matrix.hstack(*(eye(d)[:, j+1] if j+1 < d else -Matrix.ones(d, 1) for j in range(d)))
    pi = Z-eye(d)
    trace = Matrix([[d]+[-1]*(d-1)])
    lam = [sum((Z**k*e0 for k in range(j)), Matrix.zeros(d, 1)) for j in range(prime)]
    for level in range(1, 7):
        beta = trace*pi.inv()**(level-1)/prime
        for a in range(1, prime):
            b = pow(a, -1, prime)
            sigma = Matrix.hstack(*(Z**(b*k)*e0 for k in range(d)))
            unit = sum((Z**k for k in range(b)), Matrix.zeros(d))
            T = unit.inv()**level*sigma
            assert all(x.q == 1 for x in T)
            for k in range(d):
                y = eye(d)[:, k]
                assert sum(T*y) % prime == pow(a, level, prime)
                for j in range(prime):
                    left = (beta*sum((Z**v for v in range(a*j % prime)), Matrix.zeros(d))*y)[0]
                    right = (beta*sum((Z**v for v in range(j)), Matrix.zeros(d))*T*y)[0]
                    assert left == right
                if prime == 3:
                    assert reduce_element(tuple(map(int, T*y)), level) == rescale_label(tuple(map(int, y)), a, level)


def test_gaussian_choice_uses_only_low_labels_and_selects_no_more_than_n_plus_one():
    for low in product(range(3), repeat=6):
        labels = [[(low[2*j+i], 0) for i in range(2)] for j in range(3)]
        plan = gaussian_plan(labels, 3)
        assert 1 <= plan["selected_native_qudits"] <= 3
        c = plan["full_kernel_weights"]
        assert all(sum(c[j]*low[2*j+i] for j in range(3)) % 3 == 0 for i in range(2))
        lifted = [[plus(y, (3, 3), 3) for y in row] for row in labels]
        assert gaussian_plan(lifted, 3) == plan
        assert not plan["selection_uses_current_higher_label_digits"]


def test_even_level_rejection_does_not_claim_every_dependence_or_every_merge_is_illegal(report):
    with pytest.raises(ValueError, match="power residue subgroup"):
        gaussian_plan([[(1, 0)], [(1, 0)]], 2)
    valid = physical_merge([[(1, 0)], [(2, 0)]], [(1, 0)], 2)
    assert valid["plan"]["full_kernel_weights"] == [1, 1]
    assert valid["full_output_norm"] == pytest.approx(1)
    r = report["even_level_countercontrol"]
    assert r["actual_transformed_label_sum_residue"] == 2
    assert not r["native_phase_level_reduction_available"]
    assert not any(r["all_quantum_encodings_or_merges_excluded"] for r in report["level_power_classifications"])


def test_every_physical_branch_is_kept_and_costed(report):
    rows = report["physical_gaussian_merge_controls"]
    assert len(rows) == 8
    for r in rows:
        selected = r["plan"]["selected_native_qudits"]
        assert len(r["all_branches"]) == 3**(selected-1)
        assert sum(b["branch_probability"] for b in r["all_branches"]) == pytest.approx(1)
        assert max(b["maximum_full_phase_identity_error"] for b in r["all_branches"]) < 3e-12
        assert r["known_qudit_permutation_count"] == selected
        assert r["known_SUM_difference_count"] == selected-1
        assert not r["postselection_or_cloning_used"]
    assert {r["unfiltered_label_seed"] for r in rows} == set(range(45011, 45015))


def test_source_uniformity_holds_after_conditioning_each_measured_outcome():
    r = uniform_source_control()
    assert r["exact_parent_pairs"] == 81
    assert {x["count"] for x in r["child_label_counts"]} == {27}
    for branch in r["counts_conditioned_on_each_difference_outcome"]:
        assert {x["count"] for x in branch["child_label_counts"]} == {9}
    assert not r["selection_after_reading_higher_digits_covered"]


def test_sample_ledger_preserves_ramification_bottleneck_and_all_claim_gates(report):
    for r in report["ternary_scaling_ledgers"]:
        t = r["modulus_log3"]
        assert r["Gaussian_surjective_stages"] == t-1
        assert r["remaining_subset_zero_sum_stages"] == t
        assert not r["quasi_polynomial_bottleneck_removed"]
        assert not r["constant_cost_even_levels_alone_make_this_ledger_polynomial"]
        assert "not optimal sample lower bound" in r["bound_scope"]
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))
    assert level_classification(5, 2)["native_rescaling_residue_multipliers"] == [1, 4]
    assert level_classification(7, 3)["native_rescaling_residue_multipliers"] == [1, 6]


@pytest.mark.parametrize("labels,level", [([], 3), ([[]], 3), ([[(1, 0)], []], 3),
    ([[(1, .5)]], 3), ([[(1, 0)]], True), ([[(1, 0)]], 1)])
def test_malformed_native_plans_are_rejected(labels, level):
    with pytest.raises(ValueError):
        gaussian_plan(labels, level)


def test_actual_nondivisible_labels_cannot_be_renamed_as_a_lower_level():
    with pytest.raises(ValueError, match="pi divisibility"):
        divide_pi((1, 0), 3)
    with pytest.raises(ValueError, match="dependence"):
        gaussian_plan([[(1, 0)]], 3)
