"""An actual fixed AG control in the refined gap, killed by classical sampling."""

from fractions import Fraction
import importlib.util
from itertools import product
from pathlib import Path

from flint import nmod_poly

from affine_sampling import AffineFiber, bonferroni_bound


BASELINE = Path(__file__).resolve().parent.parent / "schur-growth-classical-gate-2026-10-26/schur_gate.py"
spec = importlib.util.spec_from_file_location("prior_schur_baseline", BASELINE)
schur = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schur)


def control():
    p, genus, degree = 13, 3, 7
    f = nmod_poly([0, 3, 0, 0, 0, 0, 0, 1], p)
    if f.gcd(f.derivative()) != nmod_poly([1], p):
        raise ArithmeticError("singular hyperelliptic curve")
    all_points = [(x, y) for x, y in product(range(p), repeat=2)
                  if (y*y-x**7-3*x) % p == 0]
    first = sorted(dict((x, (x, y)) for x, y in reversed(all_points)).values())
    rest = [point for point in all_points if point not in first]
    points = first+rest[:6]
    if len(points) != 19 or len(set(points)) != 19:
        raise ArithmeticError("changed fixed original evaluation set")
    B = [[pow(x, i, p) for x, y in points] for i in range(4)]+[[y for x, y in points]]
    old = schur.FullSupportProblem(p, B, relation="full_support")
    fiber = AffineFiber(p, B, relation="full_support")
    if (len(old.W), len(old.U), len(old.annihilator)) != (12, 19, 0):
        raise ArithmeticError("control is no longer outside the cubic-annihilator solver")
    # A nonzero a(x)+b*y, deg a<=3, has <=7 zeros: for b!=0 use
    # a(x)^2-b^2*(x^7+3x), whose degree is exactly7; for b=0 use <=6.
    distance_lower = fiber.m-degree
    bound = bonferroni_bound(fiber.m, p, distance_lower-1)
    quantum_e = Fraction((p**fiber.k-1)*p**len(old.W), (p-1)**fiber.m)
    gram_tail = Fraction(p**fiber.k-1, (p-1)**distance_lower)
    if not 0 < quantum_e < 1 or not bound["success_lower"] > Fraction(1, 5):
        raise ArithmeticError("refined-quantum/classical control no longer has its claimed bounds")
    return fiber, {"prime": p, "genus": genus, "divisor_degree": degree,
                   "curve_coefficients_low_first": [0, 3, 0, 0, 0, 0, 0, 1],
                   "points": points, "affine_points_found": len(all_points),
                   "point_pairs_enumerated": p*p, "original_parity": B,
                   "dual_distance_lower": distance_lower,
                   "distance_reason": "nonzero a(x)+b*y has at most7 evaluation zeros",
                   "schur_square_dimension": len(old.W), "schur_cube_dimension": len(old.U),
                   "cube_annihilator_dimension": len(old.annihilator),
                   "refined_decoder_failure_upper": quantum_e,
                   "gram_tail_upper": gram_tail,
                   "conditional_refined_quantum_success_lower": (1-quantum_e)/(1+gram_tail),
                   "classical_probability_certificate": bound,
                   "128_trial_failure_below_1e_minus_12": (
                       (1-bound["success_lower"])**128 < Fraction(1, 10**12)),
                   "quantum_execution": False, "quantum_advantage_established": False}
