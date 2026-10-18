"""Native physics and scope falsifiers for the independent HDQI proposal."""

from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

from theorems.hdqi_predecessor_uniform import (
    ARTIFACT, canonical_paulis, independent_profile, energy_certificate,
    native_control, pauli_matrix, run_controls,
    solve_ground_energy,
)


@pytest.mark.parametrize("m", range(1, 6))
def test_every_small_predecessor_pattern_against_physical_hamiltonian(m):
    coefficients = [Fraction((-1) ** j * (j + 1), 3) for j in range(m)]
    for suffix in itertools.product((0, 1), repeat=m - 1):
        result = native_control((0,) + suffix, coefficients)
        assert result["float_calibration_agrees"]
        assert result["native_ground_state_residual"] < 1e-11
        assert result["native_norm_error"] < 1e-12
        assert result["profile"]["symplectic_rank"] == m


def test_all_commuting_and_all_anticommuting_closed_forms():
    c = [3, -4, 12]
    commuting = energy_certificate(independent_profile(canonical_paulis([0, 0, 0]), c))
    anti = energy_certificate(independent_profile(canonical_paulis([0, 1, 1]), c))
    assert Fraction(commuting["energy_lower"]) == -19
    assert Fraction(commuting["energy_upper"]) == -19
    # A discovered ordering can create irrational intermediate square roots.
    # Outward rounding encloses the exact final integer; it need not collapse.
    assert Fraction(anti["energy_lower"]) <= -13 <= Fraction(anti["energy_upper"])
    assert Fraction(anti["width"]) <= Fraction(3, 2 ** 80)


def test_native_realization_with_fewer_qubits_and_y_terms():
    for words in (["X", "Z"], ["Y", "X"], ["XI", "ZI", "IZ"]):
        coeffs = [Fraction(j + 1, 7) for j in range(len(words))]
        profile = independent_profile(words, coeffs)
        cert = energy_certificate(profile)
        h = sum(float(c) * pauli_matrix(p) for p, c in zip(words, coeffs))
        assert np.linalg.eigvalsh(h)[0] == pytest.approx(float(Fraction(cert["energy_lower"])), abs=1e-11)


def test_order_discovered_after_input_permutation():
    words = canonical_paulis([0, 1, 0, 1, 0])
    c = [2, 3, -5, 7, -11]
    original = energy_certificate(independent_profile(words, c))
    for permutation in itertools.permutations(range(5)):
        changed = energy_certificate(independent_profile([words[j] for j in permutation],
                                                         [c[j] for j in permutation]))
        assert float(Fraction(changed["energy_lower"])) == pytest.approx(float(Fraction(original["energy_lower"])), abs=1e-12)


def test_exact_intervals_against_high_precision_independent_scalar_evaluation():
    profile = independent_profile(canonical_paulis([0, 1, 0, 1, 1]), ["1/3", "-2/7", "4/9", "5/13", "-8/17"])
    with localcontext() as context:
        context.prec = 120
        radius = Decimal(0)
        for mode, raw in zip(profile["anticommutes_with_predecessors"], profile["ordered_coefficients"]):
            fraction = Fraction(raw)
            c = Decimal(fraction.numerator) / Decimal(fraction.denominator)
            radius = (radius * radius + c * c).sqrt() if mode else radius + abs(c)
        cert = energy_certificate(profile, 80)
        lower, upper = (Fraction(cert[k]) for k in ("energy_lower", "energy_upper"))
        assert Decimal(lower.numerator) / Decimal(lower.denominator) <= -radius
        assert -radius <= Decimal(upper.numerator) / Decimal(upper.denominator)
        assert upper - lower <= Fraction(5, 2 ** 80)


def test_dependence_is_a_real_falsifier_not_an_optional_warning():
    # Commuting triangle: P1*P2*P3=I forbids three simultaneously negative signs.
    words = ["ZZI", "IZZ", "ZIZ"]
    h = sum(pauli_matrix(p) for p in words)
    assert np.linalg.eigvalsh(h)[0] == pytest.approx(-1)
    assert np.linalg.eigvalsh(h)[0] != -3
    with pytest.raises(ValueError, match="dependent"):
        solve_ground_energy(words, [1, 1, 1])


def test_nonpredecessor_graph_rejected_without_hardness_inference():
    # Canonical triangular construction for a path P4, not a threshold graph.
    words = ["XIII", "ZXII", "IZXI", "IIZX"]
    with pytest.raises(ValueError, match="unsupported, not hardness"):
        solve_ground_energy(words, [1] * 4)


def test_zero_and_signed_coefficients_do_not_break_ground_circuit():
    assert native_control([0, 1, 0, 1], [0, -2, 0, 3])["float_calibration_agrees"]
    result = native_control([0, 1], [0, 0])
    assert result["native_smallest_eigenvalue"] == 0
    assert result["float_calibration_agrees"]


@pytest.mark.parametrize("words,c", [(["I"], [1]), (["A"], [1]), (["X", "ZZ"], [1, 2]),
                                     (["X"], [0.5]), (["X"], [True]), (["X"], [])])
def test_invalid_or_inexact_input_rejected(words, c):
    with pytest.raises(ValueError):
        independent_profile(words, c)


def test_live_artifact_and_large_scalable_certificate():
    saved = json.loads(ARTIFACT.read_text())
    assert saved == run_controls()
    large = saved["large_symbolic_control"]
    assert large["profile"]["term_count"] == large["profile"]["symplectic_rank"] == 512
    assert not large["dense_quantum_run_performed"]
    assert large["certificate"]["arithmetic_steps"] == 512
    assert Fraction(large["certificate"]["width"]) <= Fraction(512, 2 ** 80)
    source = Path(__file__).resolve().parents[1] / "theorems/hdqi_predecessor_uniform.py"
    assert saved["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert not saved["new_quantum_algorithm_claimed"]
