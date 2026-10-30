"""Exact controls for rejected routes, not a solver or a hardness test."""

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fq_default_poly_ctx
import pytest

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import reciprocal_bound
from theorems.inverse_trace_norm import QuadraticTower
from theorems.inverse_trace_smt import (
    syndrome, vandermonde_eliminate_residual, verify_word,
)


@pytest.mark.parametrize("bits", [3, 5, 7, 17])
def test_monic_split_leading_term_has_no_root_at_odd_degree(bits):
    ring = fq_default_poly_ctx(field(bits))
    variable = ring.gen()
    assert int(field(bits).one().trace()) == 1
    assert (variable**2 + variable + 1).is_irreducible()


@pytest.mark.parametrize("bits", [2, 4, 6])
def test_odd_degree_obstruction_is_not_extended_to_even_fields(bits):
    ring = fq_default_poly_ctx(field(bits))
    variable = ring.gen()
    roots = (variable**2 + variable + 1).roots()
    assert len(roots) == 2
    for root, multiplicity in roots:
        assert multiplicity == 1
        assert root * (root + 1) == 1


@pytest.mark.parametrize("bits", [5, 7, 17])
def test_formal_infinity_lift_does_not_solve_the_native_congruence(bits):
    ring = fq_default_poly_ctx(field(bits))
    variable, polynomial = ring.gen(), ring.one()
    ell, checks = bits * bits - 1, bits * bits // 8
    degree = ell - 1
    for point in range(1, bits * bits):
        polynomial *= variable - element(bits, point)

    # The one-target point is zero. W/P agrees with 1/X for ell moments.
    total = polynomial // variable
    assert (polynomial - variable * total).degree() == 0
    assert checks <= ell
    root = element(bits, 2)
    leading = root**2 + root
    residue = polynomial.derivative()**2 % polynomial
    trial = residue + polynomial * leading * variable**(ell - 2)
    assert leading != 0 and int(leading.trace()) == 0
    assert trial.degree() == 2 * degree

    w = [total[degree - j] for j in range(degree + 1)]
    y = [root]
    for j in range(1, degree + 1):
        value = trial[2 * degree - j]
        for i in range(1, j + 1):
            value += w[i] * y[j - i]
        if j % 2 == 0:
            value += y[j // 2]**2
        y.append(value)
    left = ring(list(reversed(y)))
    right = left + total
    gap = trial - left * right
    assert gap.degree() == degree - 1
    assert (left * right) % polynomial != residue


@pytest.mark.parametrize("bits,exponent", [(17, -594), (31, -3688), (61, -28303)])
def test_native_repaired_split_proposal_bound_is_exact(bits, exponent):
    q = 1 << bits
    length, checks = bits * bits, bits * bits // 8
    _, eta = reciprocal_bound(bits, length - 1, checks)
    bound = (1 + eta) * Fraction(q)**(2 - checks) / (q - 2)
    assert Fraction(2)**(exponent - 1) < bound < Fraction(2)**exponent


def test_short_syndrome_does_not_supply_a_short_accepted_completion():
    bits, points, checks = 3, tuple(range(6)), 2
    alphabet = [x for x in range(8) if reciprocal_trace(bits, x) == 0]
    target = syndrome(bits, (points[0],), (1,), checks)
    counts = Counter()
    for values in product(alphabet, repeat=5):
        if syndrome(bits, points[1:], values, checks) == target:
            counts[sum(x != 0 for x in values)] += 1
    assert counts == {3: 6, 5: 8}


def test_systematic_curves_need_output_law_correction():
    bits, points, checks = 3, tuple(range(6)), 2
    problem = {
        "bits": bits, "points": points, "targets": [1] * len(points),
        "checks": checks,
        "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
    }
    pivots, free, constants, matrix = vandermonde_eliminate_residual(
        bits, points, range(len(points)), [0] * checks, checks,
    )
    offsets = [element(bits, c) for c in range(8) if int(element(bits, c).trace()) == 1]
    slopes = [element(bits, a) for a in (1, 2, 3, 4)]
    curve_count = len(offsets)**len(free)
    naive, corrected, per_parameter = Counter(), Counter(), [Counter() for _ in range(8)]
    nonempty = 0
    for row in product(offsets, repeat=len(free)):
        outputs = []
        for t in range(8):
            parameter = element(bits, t)
            word = [0] * len(points)
            for index, offset, slope in zip(free, row, slopes, strict=True):
                shift = slope * parameter
                inverse = offset + shift**2 + shift
                word[index] = encoded(inverse**-1) if inverse else 0
            for r, index in enumerate(pivots):
                value = element(bits, constants[r])
                for coefficient, j in zip(matrix[r], free, strict=True):
                    value += element(bits, coefficient) * element(bits, word[j])
                word[index] = encoded(value)
            assert not any(syndrome(bits, points, word, checks))
            assert all(reciprocal_trace(bits, word[j]) == 1 for j in free)
            if verify_word(problem, word):
                output = tuple(word)
                outputs.append(output)
                per_parameter[t][output] += 1
        if outputs:
            nonempty += 1
        for output in outputs:
            naive[output] += Fraction(1, curve_count * len(outputs))
            corrected[output] += Fraction(1, curve_count * 8)

    # At t=0 all accepted systematic assignments occur, so this is all Omega.
    native = per_parameter[0]
    assert len(native) == 68 and all(count == 1 for count in native.values())
    assert all(counts == native for counts in per_parameter)
    assert set(corrected) == set(native)
    assert set(corrected.values()) == {Fraction(1, curve_count)}
    assert sum(corrected.values()) == Fraction(len(native), curve_count) == Fraction(17, 64)
    naive_success = Fraction(nonempty, curve_count)
    assert sum(naive.values()) == naive_success == Fraction(31, 32)
    naive_tv = sum(abs(naive[x] / naive_success - Fraction(1, len(native)))
                   for x in native) / 2
    assert naive_tv == Fraction(467, 2108)


@pytest.mark.parametrize("target,order", [(0, 7), (1, 9)])
def test_local_norm_syndrome_fibers_are_not_subgroup_cosets(target, order):
    tower = QuadraticTower(3)
    variable = tower.ring.gen()
    roots = [t for t, multiplicity in (variable**order - 1).roots()
             if multiplicity == 1]
    assert len(roots) == order
    fibers = Counter()
    for t in roots:
        inverse = t**-1
        x, other = tower.components(t + inverse)
        assert other == 0
        assert t + inverse == inverse + inverse**-1
        if t != 1:
            assert x != 0 and reciprocal_trace(3, encoded(x)) == target
        fibers[encoded(x)] += 1
    # The identity fiber is a singleton; each nonzero fiber has two points.
    # A subgroup-hiding function must instead have equal-sized coset fibers.
    assert fibers[0] == 1
    assert Counter(fibers.values()) == {1: 1, 2: (order - 1) // 2}


def test_saved_affine_controls_replay_from_the_recorded_public_inputs():
    from theorems.inverse_trace_sparse_polynomial import classify_affine_singleton

    path = Path(__file__).resolve().parents[1] / "research/classical_baselines/inverse_trace_sparse_polynomial.json"
    report = json.loads(path.read_text())
    assert report["schema_version"] == "1.0" and not report["new_quantum_algorithm"]
    assert len(report["cases"]) == 2
    for case in report["cases"]:
        instance = case["instance"]
        digest = hashlib.sha256(json.dumps(
            instance, sort_keys=True, separators=(",", ":"),
        ).encode()).hexdigest()
        assert digest == case["instance_sha256"]
        assert len(instance["points"]) == instance["bits"]**2
        assert instance["checks"] == len(instance["points"]) // 8
        replay = classify_affine_singleton(instance)
        assert replay == {k: v for k, v in case.items()
                          if k not in ("control_id", "instance_sha256")}
        if case["witness"] is not None:
            assert verify_word(instance, case["witness"])
