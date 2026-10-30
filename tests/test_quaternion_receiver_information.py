"""Bounded receiver-information controls, not a receiver or native algorithm.

The shadow identities assume an actual finite q-qubit state, D=2**q, and
uniform FULL global Clifford measurements followed by computational-basis
measurement. Their projective 3-design moments agree with Haar moments;
this calculation does not require implementing a Haar POVM. It does not
license replacing global Cliffords by independent local Pauli measurements.
See HKP 2020, arXiv:2002.08953, Supplement Theorem 1 and Proposition 1,
Eqs. (S13), (S38)--(S40). Candidate-score evaluation and net search remain
uncharged here; an efficient preparation circuit is not a classical overlap
evaluation algorithm.

The separate SU(2) fixture is a maximally entangled single spin-j orbit,
with reduced density I/d_j and maximum-likelihood amplitude chi_j. Its
growing peak does not imply large integrated recovery probability. This
does not prove that the ML measurement is suboptimal for the ball objective,
or transfer the fixture to the native quaternion lattice source. Integer
spins in the numerical controls have exact stabilizer {+I,-I}; both caps
must be counted. All quadratures are bounded numerical checks, not interval
certificates, and no growing-dimensional state or circuit is allocated.
"""

from itertools import permutations

import mpmath as mp
import sympy as sp


def _born_weighted_rank_one_moment(power, dimension, fidelity):
    """E_Born[|<phi|u>|**(2*power)] from moments of order at most three."""
    assert power in (0, 1, 2)
    # Expand the symmetric projector into permutations of (rho, P, ..., P).
    # Every all-P cycle has trace 1. The rho cycle has trace F unless rho
    # is a fixed point, in which case its trace is 1, also for mixed rho.
    cycle_traces = sum(
        fidelity if permutation[0] != 0 else sp.Integer(1)
        for permutation in permutations(range(power + 1))
    )
    denominator = sp.prod(dimension + k for k in range(power + 1))
    return sp.cancel(dimension * cycle_traces / denominator)


def test_global_three_design_rank_one_estimator_exact_moments():
    dimension = sp.symbols("D", integer=True, positive=True)
    fidelity = sp.symbols("F", real=True)  # Physical range: 0 <= F <= 1.
    zeroth, first, second = (
        _born_weighted_rank_one_moment(k, dimension, fidelity)
        for k in range(3)
    )
    assert zeroth == 1  # Includes Born weighting, not uniform records.
    assert sp.cancel(first - (1 + fidelity) / (dimension + 1)) == 0
    assert sp.cancel(
        second - (2 + 4 * fidelity) / ((dimension + 1) * (dimension + 2))
    ) == 0

    mean = sp.cancel((dimension + 1) * first - 1)
    second_moment = sp.cancel(
        (dimension + 1)**2 * second - 2 * (dimension + 1) * first + 1
    )
    variance = sp.cancel(second_moment - mean**2)
    assert mean == fidelity
    assert sp.cancel(second_moment - dimension * (1 + 2 * fidelity) / (dimension + 2)) == 0
    # A nonnegative certificate on the full physical range, not a scan.
    assert sp.cancel(
        3 - second_moment - (6 + 2 * dimension * (1 - fidelity)) / (dimension + 2)
    ) == 0
    ratio = dimension / (dimension + 2)
    assert sp.cancel(variance - (ratio + ratio**2 - (fidelity - ratio)**2)) == 0

    for qubits in (1, 2, 5):
        for overlap in (sp.Integer(0), sp.Rational(1, 3), sp.Integer(1)):
            evaluated = variance.subs({dimension: 2**qubits, fidelity: overlap})
            assert 0 <= evaluated < 3
    # Centering a rank-one target does not introduce a dimension factor.
    assert sp.simplify(
        (1 - 1 / dimension)**2 + (dimension - 1) / dimension**2
        - (1 - 1 / dimension)
    ) == 0


def test_local_pauli_product_shadow_does_not_inherit_global_bound():
    # On |0>, the local rank-one score is 2 for Z, and 1/2 for X or Y.
    local_scores = (sp.Integer(2), sp.Rational(1, 2), sp.Rational(1, 2))
    local_mean = sum(local_scores) / 3
    local_second = sum(score**2 for score in local_scores) / 3
    assert local_mean == 1
    assert local_second == sp.Rational(3, 2)
    qubits = 4
    product_variance = local_second**qubits - local_mean**(2 * qubits)
    assert product_variance == sp.Rational(65, 16) > 3
    dimension = 2**qubits
    global_variance = sp.Rational(3 * dimension, dimension + 2) - 1
    assert global_variance == sp.Rational(5, 3) < 3


def test_finite_source_net_margin_survives_both_preparation_errors():
    source_error = sp.Rational(1, 128)
    # Mesh 1/(8*max(1,L)) gives ideal ket distance <= 1/8.
    near_distance = sp.Rational(1, 8) + 2 * source_error
    far_amplitude = sp.Rational(3, 4) + 2 * source_error
    assert near_distance == sp.Rational(9, 64)
    assert far_amplitude == sp.Rational(49, 64)

    exact_near_lower = (1 - near_distance**2 / 2)**2
    near_lower = 1 - near_distance**2
    far_upper = far_amplitude**2
    assert exact_near_lower - near_lower == near_distance**4 / 4
    assert near_lower == sp.Rational(4015, 4096)
    assert far_upper == sp.Rational(2401, 4096)

    estimate_error = sp.Rational(1, 8)  # Total statistical/numerical error.
    selected_lower = near_lower - 2 * estimate_error
    assert selected_lower == sp.Rational(2991, 4096)
    assert selected_lower - far_upper == sp.Rational(590, 4096) > 0
    assert far_upper + estimate_error < sp.Rational(3, 4)
    assert near_lower - estimate_error > sp.Rational(3, 4)
    # A much looser estimator would not establish the claimed separation.
    assert near_lower - 2 * sp.Rational(1, 4) < far_upper


def test_character_ml_peak_does_not_control_integrated_cap_mass():
    dimension = sp.symbols("d_j", integer=True, positive=True)
    angle = sp.symbols("theta", real=True)
    character = sp.sin(dimension * angle) / sp.sin(angle)
    # rho=I/d_j: sqrt(d_j)*Tr(D_j*sqrt(rho)) = chi_j, not d_j*chi_j.
    assert sp.simplify(sp.sqrt(dimension) * sp.sqrt(1 / dimension)) == 1
    likelihood = character**2
    assert sp.limit(likelihood, angle, 0) == dimension**2

    haar_angle_density = 2 * sp.sin(angle)**2 / sp.pi
    radial_likelihood = sp.cancel(haar_angle_density * likelihood)
    assert sp.simplify(radial_likelihood - 2 * sp.sin(dimension * angle)**2 / sp.pi) == 0
    cap = angle / sp.pi - sp.sin(2 * dimension * angle) / (2 * sp.pi * dimension)
    # Derivative plus endpoint verifies the integral with exact constants.
    assert sp.trigsimp(sp.diff(cap, angle) - radial_likelihood) == 0
    assert cap.subs(angle, 0) == 0
    assert sp.simplify(cap.subs(angle, sp.pi)) == 1
    shrinking_cap = sp.simplify(cap.subs(angle, 1 / dimension))
    constant = (1 - sp.sin(2) / 2) / sp.pi
    assert sp.simplify(shrinking_cap - constant / dimension) == 0
    assert sp.limit(shrinking_cap, dimension, sp.oo) == 0
    assert sp.limit(dimension**2, dimension, sp.oo) == sp.oo
    # Even a fixed cap need not capture a growing fraction of the mass.
    for value in (3, 9, 15):
        assert sp.simplify(cap.subs({dimension: value, angle: sp.pi / 6})) == sp.Rational(1, 6)


def test_integer_spin_quotient_counts_both_caps_with_bounded_quadrature():
    angle = sp.symbols("theta", real=True)
    with mp.workdps(60):
        constant = (1 - mp.sin(2) / 2) / mp.pi
        previous_peak, previous_success = 0, mp.mpf(1)
        for dimension in (3, 5, 9):  # j=1,2,4; exact vector stabilizer +/-I.
            character = sp.sin(dimension * angle) / sp.sin(angle)
            assert sp.trigsimp(character.subs(angle, sp.pi - angle) - character) == 0
            assert sp.limit(character, angle, sp.pi) == dimension
            theta = mp.mpf(1) / dimension
            assert 2 * theta < mp.pi  # The two caps are disjoint.

            def weighted_character(t):
                if t == 0 or t == mp.pi:
                    return mp.mpf(0)
                chi = mp.sin(dimension * t) / mp.sin(t)
                return chi**2 * 2 * mp.sin(t)**2 / mp.pi

            cap_plus = mp.quad(weighted_character, [0, theta])
            cap_minus = mp.quad(weighted_character, [mp.pi - theta, mp.pi])
            quotient_success = cap_plus + cap_minus
            assert abs(mp.quad(weighted_character, [0, mp.pi]) - 1) < mp.mpf("1e-50")
            assert abs(cap_plus - constant / dimension) < mp.mpf("1e-50")
            assert abs(cap_minus - cap_plus) < mp.mpf("1e-50")
            assert abs(quotient_success - 2 * constant / dimension) < mp.mpf("1e-50")
            assert dimension**2 > previous_peak
            assert 0 < quotient_success < previous_success
            previous_peak, previous_success = dimension**2, quotient_success
