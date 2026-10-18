"""Exact OPI filter moments and independently checked rational tail bounds.

RS K-wise independence determines moments only through degree K. A numerical
LP proposes dual polynomials; exact arithmetic verifies every inequality.
No executed quantum circuit or matched gate-cost advantage is claimed.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scipy
from scipy.optimize import linprog

from theorems.bpqm_gibbs_frontier import integer
from theorems.explicit_quadratic_opi import filter_bound

REPORT = ROOT/"research/classical_baselines/opi_filter_tail_certificate.json"


def krawtchouk(N, j, accepted):
    return sum((-1)**a*comb(N-accepted, a)*comb(accepted, j-a)
               for a in range(j+1) if a <= N-accepted and j-a <= accepted)


def filter_moments(problem, degree, *, order=None, precision_bits=128):
    """Use a specified rational polynomial P(s), not rounded irrational moments."""
    N, K = problem.length, problem.dimension
    integer(precision_bits, "rational filter precision", 32, 512)
    reference = filter_bound(problem, degree=degree)
    maximum = K-2*degree
    order = min(9, maximum) if order is None else order
    integer(order, "certified moment order", 1, min(15, N))
    if order > maximum:
        raise ValueError("filter squared plus moment exceeds RS dual-distance independence")
    scale = 1 << precision_bits
    weights = [Fraction(x) for x in reference["rational_filter_weights"]]
    coefficients = [w*Fraction(isqrt((scale*scale)//comb(N, j)), scale) for j, w in enumerate(weights)]
    if any(w and not b for w, b in zip(weights, coefficients)):
        raise ValueError("filter precision insufficient for nonzero Krawtchouk coefficients")
    norm = sum(b*b*comb(N, j) for j, b in enumerate(coefficients))
    moments = [Fraction(0) for _ in range(order+1)]
    for s in range(N+1):
        amplitude = sum(b*krawtchouk(N, j, s) for j, b in enumerate(coefficients))
        probability = Fraction(comb(N, s), 1 << N)*amplitude*amplitude/norm
        power = Fraction(1)
        for r in range(order+1):
            moments[r] += probability*power
            power *= Fraction(s, N)
    if moments[0] != 1:
        raise ArithmeticError("exact Krawtchouk norm identity failed")
    return {"positions": N, "RS_dimension": K, "filter_degree": degree,
            "certified_moment_order": order, "maximum_RS_certified_order": maximum,
            "rational_Krawtchouk_coefficients": list(map(str, coefficients)),
            "filter_normalization": str(norm), "normalized_score_moments": list(map(str, moments)),
            "mean_score": str(moments[1]), "precision_bits": precision_bits,
            "filter_is_this_rational_polynomial_not_exact_reference_eigenfilter": True,
            "weighted_binomial_law_is_the_native_full_score_distribution": False,
            "moments_beyond_RS_cutoff_not_certified_by_this_method": True,
            "RS_K_wise_independence_and_balanced_public_predicates_required": True,
            "coherent_filter_and_decoder_executed": False,
            "local_moment_derivation_review_pending": True}


def _evaluate(coefficients, x):
    value = Fraction(0)
    for c in reversed(coefficients):
        value = value*x+c
    return value


def _dyadic_enclose(probability, *, upper=False):
    scale = 1 << 80
    numerator, remainder = divmod(probability.numerator*scale, probability.denominator)
    return Fraction(numerator+int(upper and remainder != 0), scale)


def _minorant(N, moments, event):
    order = len(moments)-1
    matrix = [[(s/N)**r for s in range(N+1)] for r in range(order+1)]
    result = linprog(event, A_eq=matrix, b_eq=list(map(float, moments)),
                     bounds=(0, None), method="highs")
    if not result.success:
        return (Fraction(0),)*(order+1), {"status": "UNKNOWN_LP_ZERO_CERTIFICATE", "message": str(result.message)}
    proposed = tuple(Fraction(float(y)).limit_denominator(1 << 30) for y in result.eqlin.marginals)
    # Repair numerical dual infeasibility exactly at EVERY physically possible score.
    excess = max(Fraction(0), max(_evaluate(proposed, Fraction(s, N))-event[s] for s in range(N+1)))
    fixed = (proposed[0]-excess,)+proposed[1:]
    if sum(a*b for a, b in zip(fixed, moments)) < 0:
        fixed = (Fraction(0),)*(order+1)
    return fixed, {"status": "EXACTLY_VERIFIED_RATIONAL_DUAL", "constant_repair": str(excess),
                   "numerical_LP_optimum_is_certified": False}


def tail_certificate(moment_record, threshold):
    N = moment_record["positions"]
    integer(threshold, "accepted-count tail threshold", 0, N+1)
    moments = tuple(map(Fraction, moment_record["normalized_score_moments"]))
    event = [int(s >= threshold) for s in range(N+1)]
    lower, lower_status = _minorant(N, moments, event)
    complement, upper_status = _minorant(N, moments, [1-e for e in event])
    upper = (1-complement[0],)+tuple(-c for c in complement[1:])
    lo, hi = (sum(c*m for c, m in zip(poly, moments)) for poly in (lower, upper))
    certificate = {"accepted_count_threshold": threshold, "tail_probability_lower": str(lo),
                   "tail_probability_upper": str(hi), "minorant_coefficients": list(map(str, lower)),
                   "majorant_coefficients": list(map(str, upper)),
                   "lower_solver": lower_status, "upper_solver": upper_status,
                   "support_points_checked": N+1, "matched_quantum_gate_budget_supplied": False,
                   "independent_repetitions": [{"attempts": attempts,
                       "success_lower": str(_dyadic_enclose(1-(1-lo)**attempts)),
                       "success_upper": str(_dyadic_enclose(1-(1-hi)**attempts, upper=True)),
                       "dyadic_enclosure_bits": 80}
                       for attempts in (1, 4, 16)]}
    verify_tail_certificate(moment_record, certificate)
    return certificate


def verify_tail_certificate(moment_record, certificate):
    N = moment_record["positions"]
    order = moment_record["certified_moment_order"]
    if 2*moment_record["filter_degree"]+order > moment_record["RS_dimension"]:
        raise ValueError("unproved moments exceed RS independence cutoff")
    moments = tuple(map(Fraction, moment_record["normalized_score_moments"]))
    lower = tuple(map(Fraction, certificate["minorant_coefficients"]))
    upper = tuple(map(Fraction, certificate["majorant_coefficients"]))
    if len(moments) != order+1 or len(lower) != len(moments) or len(upper) != len(moments) or moments[0] != 1:
        raise ValueError("moment/dual polynomial dimension or normalization mismatch")
    threshold = certificate["accepted_count_threshold"]
    integer(threshold, "tail threshold", 0, N+1)
    for s in range(N+1):
        indicator, x = int(s >= threshold), Fraction(s, N)
        if not _evaluate(lower, x) <= indicator <= _evaluate(upper, x):
            raise ArithmeticError("pointwise tail polynomial inequality failed")
    lo, hi = (sum(c*m for c, m in zip(poly, moments)) for poly in (lower, upper))
    if (str(lo) != certificate["tail_probability_lower"] or str(hi) != certificate["tail_probability_upper"]
            or not 0 <= lo <= hi <= 1):
        raise ArithmeticError("tail expectation or probability range failed")
    for row in certificate["independent_repetitions"]:
        integer(row["attempts"], "independent attempts", 1, 1024)
        if (Fraction(row["success_lower"]) != _dyadic_enclose(1-(1-lo)**row["attempts"])
                or Fraction(row["success_upper"]) != _dyadic_enclose(1-(1-hi)**row["attempts"], upper=True)):
            raise ArithmeticError("independent repetition arithmetic failed")
    return True


def run_controls():
    from theorems.explicit_cubic_opi import REPORT as CUBIC_REPORT, from_specification
    saved = json.loads(CUBIC_REPORT.read_text())
    rows = []
    for source in saved["instances"]:
        problem = from_specification(source["specification"])
        top = (problem.dimension-1)//2
        degrees = sorted({max(0, top-j) for j in (0, 1, 3)})
        filters = []
        for degree in degrees:
            moments = filter_moments(problem, degree)
            thresholds = sorted({source["best_score_count"], (4*problem.length+4)//5})
            filters.append({"moments": moments,
                            "tail_certificates": [tail_certificate(moments, k) for k in thresholds]})
        rows.append({"field_bits": problem.bits, "positions": problem.length, "RS_dimension": problem.dimension,
                     "public_seed": source["public_seed"], "classical_best_of_four": source["best_score_count"],
                     "filters": filters, "classical_finite_best_score_is_not_a_quantum_tail_bound": True})
    return {"schema_version": "1.0", "subsystem": "opi_filter_tail_certificate", "instances": rows,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "input_artifact_sha256": hashlib.sha256(CUBIC_REPORT.read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                                  for name in ("explicit_quadratic_opi.py", "explicit_cubic_opi.py")},
            "scipy_version": scipy.__version__, "accepted_speedup_candidate": False,
            "new_quantum_algorithm_claimed": False, "matched_gate_budget_supplied": False,
            "literature": ["https://arxiv.org/html/2610.02145v2#A1"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{"N": r["positions"], "K": r["RS_dimension"], "seed": r["public_seed"],
                       "classical_best_of_four": r["classical_best_of_four"],
                       "filter_tails": [{"degree": f["moments"]["filter_degree"],
                           "moment_order": f["moments"]["certified_moment_order"],
                           "mean": float(Fraction(f["moments"]["mean_score"])),
                           "tails": [{"threshold": c["accepted_count_threshold"],
                                      "lower": float(Fraction(c["tail_probability_lower"])),
                                      "upper": float(Fraction(c["tail_probability_upper"]))}
                                     for c in f["tail_certificates"]]} for f in r["filters"]]}
                      for r in report["instances"]], indent=2))


if __name__ == "__main__":
    main()
