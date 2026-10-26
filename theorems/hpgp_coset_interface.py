"""Scope controls for reducing nilpotent cosets to known polynomial graphs.

The obstruction is ONLY to fixed public fibre-preserving injective charts.
It is not a quantum lower bound, a novelty certificate, or a refutation of
collective state conversion. Finite group/state enumeration is capped.
"""
from fractions import Fraction
from itertools import product

from flint import fmpz
import numpy as np

from theorems.ut5_matrix_phase_alignment import _identity, _lists, _matrix


def _prime(p):
    if type(p) is not int or p <= 3 or not fmpz(p).is_prime():
        raise ValueError("prime p>3 required")


def _vector(p, vector, length):
    if len(vector) != length or any(type(a) is not int or not 0 <= a < p for a in vector):
        raise ValueError("canonical base-field vector required")


def matrix_power(p, matrix, exponent):
    """Binary powering: the FLINT wrapper's exponent is machine-sized."""
    if type(exponent) is not int or exponent < 0:
        raise ValueError("nonnegative integer exponent required")
    if matrix.nrows() != matrix.ncols():
        raise ValueError("square matrix required")
    result = _matrix(_identity(matrix.nrows()), p)
    while exponent:
        if exponent & 1:
            result = result*matrix
        exponent >>= 1
        if exponent:
            matrix = matrix*matrix
    return result


def tail_product(p, left, right):
    """N=ker(x12:UT4->Fp), in coordinates (x23,x13,x34,x24,x14)."""
    _vector(p, left, 5)
    _vector(p, right, 5)
    b, d, c, e, f = left
    B, D, C, E, F = right
    return ((b+B) % p, (d+D) % p, (c+C) % p,
            (e+E+b*C) % p, (f+F+d*C) % p)


def tail_matrix(p, vector, quotient_coordinate=0):
    _vector(p, vector, 5)
    _vector(p, (quotient_coordinate,), 1)
    b, d, c, e, f = vector
    return ((1, quotient_coordinate, d, f), (0, 1, b, e),
            (0, 0, 1, c), (0, 0, 0, 1))


def tail_commutator(p, left, right):
    """Central coordinates of [left,right], from their N/Z coordinates."""
    _vector(p, left, 3)
    _vector(p, right, 3)
    b, d, c = left
    B, D, C = right
    return ((b*C-B*c) % p, (d*C-D*c) % p)


def transverse_curve(p, vector, t):
    """N component of (v*r)^t, r=I+E12; no field-size loop."""
    _prime(p)
    _vector(p, vector, 5)
    _vector(p, (t,), 1)
    b, d, c, e, f = vector
    choose2 = t*(t-1)*pow(2, -1, p) % p
    choose3 = t*(t-1)*(t-2)*pow(6, -1, p) % p
    return (t*b % p, (t*d+choose2*b) % p, t*c % p,
            (t*e+choose2*b*c) % p,
            (t*f+choose2*(e+d*c)+choose3*b*c) % p)


def chart_coverage_bound(p, factors, chart_count=1):
    """Analytic bound for fixed charts, not a bound on adaptive quantum work.

    N^m has order p^(5m) and largest abelian subgroup order p^(4m).
    Good transverse parameters for any chart lie in one abelian coset.
    """
    _prime(p)
    if type(factors) is not int or factors < 1:
        raise ValueError("positive product factor count required")
    if type(chart_count) is not int or chart_count < 1:
        raise ValueError("positive fixed chart count required")
    denominator = p**factors
    commuting_probability = Fraction(2*p*p-1, p**4)**factors
    approximate_error = (1-Fraction(1, p))*(1-commuting_probability)/8
    return dict(prime=p, factors=factors, lie_dimension=5*factors+1,
                nilpotency_class=3, normal_tail_order=p**(5*factors),
                maximum_abelian_tail_order=p**(4*factors),
                fixed_chart_count=chart_count,
                uniform_hidden_parameter_coverage_upper=str(min(Fraction(1), Fraction(chart_count, denominator))),
                charts_required_for_complete_coverage=denominator,
                normal_tail_commuting_probability=str(commuting_probability),
                single_fixed_chart_mean_trace_distance_lower_bound=str(approximate_error),
                approximate_bound_is_average_over_hidden_parameters=True,
                arbitrary_adaptive_reductions_excluded=False,
                collective_quantum_reductions_excluded=False)


def chart_collision_relation(p, a, b):
    """Integer combination of eight chart equations, without choosing a chart.

    E(n,v)=phi1(n*v)-phi0(n)-q_v. The combination below reduces to
    phi0(b*a)-phi0(a*b), so an injective chart cannot satisfy these
    equations when a and b do not commute. It works in any abelian output.
    """
    zero = (0,)*5
    ab, ba = tail_product(p, a, b), tail_product(p, b, a)
    terms = [(1, ab, zero), (-1, a, b), (-1, ba, zero), (1, b, a),
             (1, a, zero), (-1, zero, a), (-1, b, zero), (1, zero, b)]
    coefficients = {}
    for sign, n, v in terms:
        equation = [(1, ("phi1", tail_product(p, n, v))),
                    (-1, ("phi0", n)), (-1, ("q", v))]
        for coefficient, symbol in equation:
            coefficients[symbol] = coefficients.get(symbol, 0)+sign*coefficient
    return {symbol: coefficient for symbol, coefficient in coefficients.items() if coefficient}


def noncommuting_tail_witness(p):
    """Three valid transverse order-p subgroups defeat universal recoding."""
    _prime(p)
    a, b, zero = (1, 0, 0, 0, 0), (0, 0, 1, 0, 0), (0,)*5
    ab, ba = tail_product(p, a, b), tail_product(p, b, a)
    generators = [_matrix(tail_matrix(p, v, 1), p) for v in (zero, a, b)]
    identity = _matrix(_identity(4), p)
    if not all(matrix_power(p, g, p) == identity and g != identity for g in generators) or ab == ba:
        raise ArithmeticError("invalid universal-chart counterwitness")
    relation = chart_collision_relation(p, a, b)
    if relation != {("phi0", ba): 1, ("phi0", ab): -1}:
        raise ArithmeticError("symbolic chart equations did not force the claimed collision")
    for u, v in ((a, b), (b, a)):
        actual = _matrix(tail_matrix(p, u), p)*_matrix(tail_matrix(p, v, 1), p)
        if _lists(actual) != [list(row) for row in tail_matrix(p, tail_product(p, u, v), 1)]:
            raise ArithmeticError("coset t=1 product does not match the claimed chart relation")
    return dict(prime=p, tail_a=a, tail_b=b, tail_ab=ab, tail_ba=ba,
                transverse_generators=[_lists(g) for g in generators],
                distinct_ab_ba=True, all_transverse_generators_have_order_p=True,
                integer_chart_equation_elimination_checked=True,
                forced_additive_chart_images_equal=True,
                universal_injective_chart_impossible=True,
                quantum_lower_bound=False)


def discarded_center_control(p=5):
    """Actually trace the center of the UT3 mixed coset source.

    H=exp(span(E12+E23)); canonical section has x13=0.
    This p<=7 dense control is NOT an efficient HSP algorithm.
    """
    _prime(p)
    if p > 7:
        raise ValueError("dense control is capped at p<=7")
    elements = list(product(range(p), repeat=3))
    index = {g: i for i, g in enumerate(elements)}
    hidden = [(t, t, t*t*pow(2, -1, p) % p) for t in range(p)]
    # Literal right translations construct rho_H=sum_h R_h/|G|.
    density = np.zeros((p**3, p**3), dtype=float)
    for j, (a, b, z) in enumerate(elements):
        for t, u, w in hidden:
            inverse = ((-t) % p, (-u) % p, (-w+t*u) % p)
            T, U, W = inverse
            moved = ((a+T) % p, (b+U) % p, (z+W+a*U) % p)
            density[index[moved], j] += 1/p**3
    actual = np.trace(density.reshape(p*p, p, p*p, p), axis1=1, axis2=3)
    quotient = list(product(range(p), repeat=2))
    target = np.array([[int((a-A-b+B) % p == 0)/p**2 for A, B in quotient]
                       for a, b in quotient])
    projector = p*target
    support_mass = float(np.trace(projector@actual))
    expected = Fraction(2*p-1, p*p)
    if abs(support_mass-float(expected)) > 1e-12:
        raise ArithmeticError("actual partial trace contradicts the analytic support-mass formula")
    distance = float(np.abs(np.linalg.eigvalsh(actual-target)).sum()/2)
    return dict(prime=p, group_order=p**3, actual_trace=float(np.trace(actual)),
                desired_fourier_support_mass=support_mass,
                desired_fourier_support_mass_exact=str(expected),
                trace_distance=distance, trace_distance_lower_bound=str(1-expected),
                quotient_kernel_contained_in_hidden=False,
                actual_partial_trace_performed=True,
                arbitrary_quotient_conversion_impossible=False)


def report():
    return dict(status="HPGP_INTERFACE_AUDIT_NOT_NOVELTY_CERTIFICATE",
                source="https://arxiv.org/pdf/1503.09016",
                source_scope="Corollary6, Proposition7, Sections4.1 and5",
                counterwitnesses=[noncommuting_tail_witness(p) for p in (5, 2**127-1)],
                coverage=[chart_coverage_bound(5, 1), chart_coverage_bound(43, 8, 1000)],
                discarded_center=discarded_center_control(),
                known_hpgp_solver_implemented=False, rees_correctness_verified=False,
                rees_novelty_established=False, quantum_speedup_claimed=False,
                general_hpgp_reduction_ruled_out=False)


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/hpgp_coset_interface.json"
        path.write_text(payload)
    print(payload, end="")
