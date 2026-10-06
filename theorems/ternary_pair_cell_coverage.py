"""Exact native-word recovery predicates for public Babai repair lists.

LOCAL DERIVATIONS / REVIEW PENDING. Exponential word census and planted-word
geometry probes are NOT efficient pair solvers or classical hardness proofs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random
import time

from ternary_pair_collimation import LowProblem
from ternary_pair_lattice import (
    embed, lattice_pair, prepared_bases, public_center_offsets, scalar_labels, word_coordinates,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_pair_cell_coverage.json"


def integer_gs_directions(rows, profile):
    """Primitive integer GS directions with exact projection multipliers."""
    stars, result = [], []
    for i, row in enumerate(rows):
        star = tuple(Fraction(x)-sum(profile["mu"][i][j]*stars[j][k] for j in range(i))
                     for k, x in enumerate(row))
        squared = sum(x*x for x in star)
        if squared != profile["gs_squared"][i] or squared <= 0:
            raise ArithmeticError("exact GS reconstruction mismatch")
        denominator = math.lcm(*(x.denominator for x in star))
        integer = tuple(int(x*denominator) for x in star)
        divisor = math.gcd(*integer)
        direction = tuple(x//divisor for x in integer)
        multiplier = Fraction(denominator, divisor)/sum(x*x for x in direction)
        if multiplier != Fraction(1, sum(x*y for x, y in zip(row, direction))):
            raise ArithmeticError("primitive GS reciprocal identity failed")
        if any(sum(direction[j:j+3]) for j in range(0, len(direction), 3)):
            raise ValueError("native A2 block-plane GS directions required")
        result.append({"direction": direction, "multiplier": multiplier})
        stars.append(star)
    return tuple(result)


def compile_chart(directions, offset):
    """Compile word projections to integer ternary tables and half-up tests."""
    if not directions or len(offset) != len(directions[0]["direction"]):
        raise ValueError("compatible GS directions and center offset required")
    chart = []
    for row in directions:
        v, multiplier = row["direction"], row["multiplier"]
        shift = sum(Fraction(x)*y for x, y in zip(offset, v))*multiplier
        denominator = math.lcm(multiplier.denominator, shift.denominator)
        factor = multiplier.numerator*(denominator//multiplier.denominator)
        chart.append({"digits": tuple(tuple(3*x*factor for x in v[j:j+3]) for j in range(0, len(v), 3)),
                      "shift": shift.numerator*(denominator//shift.denominator), "denominator": denominator})
    return tuple(chart)


def projection_moments(row, offset=None):
    """Exact uniform-native-word moments, not Gaussian or independence fits."""
    v, m = row["direction"], row["multiplier"]
    if len(v) % 3 or any(sum(v[i:i+3]) for i in range(0, len(v), 3)):
        raise ValueError("native A2 plane direction required")
    if offset is not None and len(offset) != len(v):
        raise ValueError("compatible public offset required")
    mean = Fraction(0) if offset is None else sum(Fraction(a)*b for a, b in zip(offset, v))*m
    norm = sum(x*x for x in v)
    block_norms = [sum(x*x for x in v[i:i+3]) for i in range(0, len(v), 3)]
    variance = 3*m*m*norm
    third = 9*m**3*sum(x**3 for x in v)
    fourth = m**4*(27*norm*norm-Fraction(27, 2)*sum(x*x for x in block_norms))
    second_raw = variance+mean*mean
    fourth_raw = fourth+4*mean*third+6*mean*mean*variance+mean**4
    tail_lower = max(Fraction(0), second_raw-Fraction(1, 4))**2/fourth_raw
    return {"mean": mean, "variance": variance, "centered_third": third,
            "centered_fourth": fourth, "raw_second": second_raw, "raw_fourth": fourth_raw,
            "rounding_error_probability_upper": min(Fraction(1), 4*second_raw),
            "strict_half_cell_tail_probability_lower": tail_lower,
            "lower_bound_uses_strict_absolute_tail_not_symmetric_tie_rule": True}


def rounded_errors(word, chart):
    word = tuple(word); word_coordinates(word)
    if not chart or len(word) != len(chart[0]["digits"]):
        raise ValueError("original native word and chart width must agree")
    result = []
    for row in chart:
        numerator = row["shift"]+sum(digits[digit] for digits, digit in zip(row["digits"], word))
        d = row["denominator"]
        result.append((2*numerator+d)//(2*d))
    return tuple(result)


def repair_cost(errors, magnitude=1):
    if type(magnitude) is not int or magnitude < 1:
        raise ValueError("positive integer repair magnitude required")
    if any(type(x) is not int for x in errors):
        raise ValueError("canonical integer rounding errors required")
    if any(abs(x) > magnitude for x in errors): return None
    return sum(x != 0 for x in errors)


def best_repair_cost(word, charts, magnitude=1):
    if type(magnitude) is not int or magnitude < 1:
        raise ValueError("positive integer repair magnitude required")
    word = tuple(word); word_coordinates(word)
    if not charts or len(word) != len(charts[0][0]["digits"]):
        raise ValueError("nonempty compatible public charts required")
    best = None
    for chart in charts:
        count = 0
        for row in chart:
            numerator = row["shift"]+sum(digits[digit] for digits, digit in zip(row["digits"], word))
            d = row["denominator"]; error = (2*numerator+d)//(2*d)
            if abs(error) > magnitude:
                break
            count += bool(error)
            if best is not None and count >= best:
                break
        else:
            best = count
        if best == 0: break
    return best


def public_charts(problem, seed=0, basis_count=2, perturbations=2):
    scalar_labels(problem)
    geometry, bases = prepared_bases(problem, seed, basis_count)
    offsets = public_center_offsets(problem.width, seed, perturbations)
    directions = [integer_gs_directions(b["rows"], b["profile"]) for b in bases]
    charts = tuple(compile_chart(d, offset) for d in directions for offset in offsets)
    return {"geometry": geometry, "bases": bases, "directions": directions,
            "offsets": offsets, "charts": charts, "seed": seed,
            "lll_calls": basis_count, "exact_profiles": basis_count}


def repair_list_size(rank, repairs, magnitude=1):
    if type(rank) is not int or rank < 1 or type(repairs) is not int or not 0 <= repairs <= rank:
        raise ValueError("positive rank and repairs within rank required")
    if type(magnitude) is not int or magnitude < 1:
        raise ValueError("positive repair magnitude required")
    return sum(math.comb(rank, j)*(2*magnitude)**j for j in range(repairs+1))


def exact_word_census(problem, prepared, magnitudes=(1, 2), max_words=100_000):
    scalar_labels(problem); D = 3**problem.width; Q = problem.moduli[0]; d = 2*problem.width
    if type(max_words) is not int or max_words < 1: raise ValueError("positive word budget required")
    if prepared["geometry"]["labels"] != scalar_labels(problem) or prepared["geometry"]["original_modulus"] != Q:
        raise ValueError("public charts must belong to these source labels")
    if any(type(b) is not int or b < 1 for b in magnitudes) or not magnitudes:
        raise ValueError("nonempty positive repair magnitudes required")
    if D > max_words:
        return {"status": "WORD_BUDGET_NO_PARTIAL_CENSUS", "word_space": str(D), "words_classified": 0}
    costs = {b: Counter() for b in magnitudes}; buckets = {b: defaultdict(list) for b in magnitudes}
    truth = Counter(); start = time.perf_counter()
    for word in product(range(3), repeat=problem.width):
        target = problem.value(word)[0]; truth[target] += 1
        for b in magnitudes:
            cost = best_repair_cost(word, prepared["charts"], b)
            costs[b]["beyond_magnitude" if cost is None else cost] += 1
            if cost is not None:
                bucket = buckets[b][target]; bucket.append(cost); bucket.sort()
                del bucket[2:]
    layers = []
    for b in magnitudes:
        pair_minimum = Counter(v[1] for v in buckets[b].values() if len(v) == 2)
        bounds = []
        for k in range(d+1):
            recovered = sum(count for cost, count in costs[b].items() if type(cost) is int and cost <= k)
            covered = sum(count for cost, count in pair_minimum.items() if cost <= k)
            beta = Fraction(covered, Q); upper = Fraction(recovered, 2*Q)
            assert beta <= upper
            bounds.append({"repairs": k, "recovered_words": recovered, "pair_covered_targets": covered,
                           "gamma_exact_conditional": str(Fraction(recovered, D)),
                           "beta_exact_conditional_uniform_targets": str(beta),
                           "word_count_pair_coverage_upper": str(upper),
                           "scheduled_candidates_all_charts": str(len(prepared["charts"])*repair_list_size(d, k, b))})
        layers.append({"maximum_repair_magnitude": b,
                       "minimum_word_repairs_histogram": {str(k): v for k, v in sorted(costs[b].items(), key=lambda x: str(x[0]))},
                       "minimum_pair_repairs_histogram": {str(k): v for k, v in sorted(pair_minimum.items())},
                       "pair_targets_unreachable_even_at_full_support_for_this_magnitude": sum(v >= 2 for v in truth.values())-sum(pair_minimum.values()),
                       "depths": bounds})
    counterexample = None
    if 1 in buckets:
        missed = sorted(t for t, C in truth.items() if C >= 2 and
                        (len(buckets[1][t]) < 2 or buckets[1][t][1] > 1))
        if missed:
            target = missed[0]
            fiber = [w for w in product(range(3), repeat=problem.width) if problem.value(w) == (target,)]
            actual = lattice_pair(problem, (target,), seed=prepared["seed"],
                                  prepared=(prepared["geometry"], prepared["bases"]),
                                  perturbations=len(prepared["offsets"])-1,
                                  max_decodes=len(prepared["charts"])*(1+2*d))
            assert not actual["pair"]
            counterexample = {"target": str(target), "complete_actual_fiber": fiber,
                              "minimum_repairs_per_word_magnitude_one": [best_repair_cost(w, prepared["charts"]) for w in fiber],
                              "per_word_per_chart_rounded_errors": [[rounded_errors(w, chart) for chart in prepared["charts"]] for w in fiber],
                              "actual_complete_scheduled_decoder_status": actual["status"],
                              "actual_verified_words_before_exhaustion": actual["witnesses"],
                              "actual_decoder_candidate_cost": actual["cost"]["candidate_decodes"],
                              "scope": "This FIXED public single-repair decoder misses a real pair target; not a general CVP or quantum-source no-go."}
    return {"status": "EXACT_EXPONENTIAL_ANALYSIS_NOT_A_SOLVER", "words_classified": D, "word_space": str(D),
            "source_width": problem.width, "modulus": str(Q), "empty_uniform_targets": Q-len(truth),
            "singleton_uniform_targets": sum(v == 1 for v in truth.values()),
            "true_pair_targets": sum(v >= 2 for v in truth.values()), "layers": layers,
            "missed_pair_target_certificate": counterexample,
            "word_analysis_wall_seconds": time.perf_counter()-start,
            "LLL_preparations_separately_charged": prepared["lll_calls"],
            "sampled_targets_or_planted_targets_used": False,
            "target_denominator_includes_all_empty_cosets": True}


def planted_word_probe(problem, prepared, samples=256, seed=0):
    if type(samples) is not int or samples < 1 or type(seed) is not int:
        raise ValueError("positive word sample count and integer seed required")
    if prepared["geometry"]["labels"] != scalar_labels(problem) or prepared["geometry"]["original_modulus"] != problem.moduli[0]:
        raise ValueError("public charts belong to different stripped labels")
    rng = random.Random(seed); hist = Counter(); magnitudes = Counter(); records = []
    pattern_counts = [Counter() for _ in prepared["charts"]]
    for _ in range(samples):
        word = tuple(rng.randrange(3) for _ in range(problem.width))
        errors = [rounded_errors(word, chart) for chart in prepared["charts"]]
        for counts, error in zip(pattern_counts, errors): counts[error] += 1
        costs = [repair_cost(e) for e in errors]
        best = min((c for c in costs if c is not None), default=None)
        hist["beyond_magnitude" if best is None else str(best)] += 1
        magnitudes[min(max(map(abs, e)) for e in errors)] += 1
        records.append({"word": word, "minimum_repairs_magnitude_one": best,
                        "per_chart_nonzero_counts": [sum(x != 0 for x in e) for e in errors],
                        "per_chart_maximum_magnitudes": [max(map(abs, e)) for e in errors]})
    denominator = samples*(samples-1)//2
    pattern_stats = [{"chart": i, "distinct_observed_patterns": len(counts), "largest_observed_pattern_count": max(counts.values()),
                      "equal_pattern_sample_pairs": sum(c*(c-1)//2 for c in counts.values()),
                      "empirical_pair_collision_rate_not_population_proof": str(Fraction(sum(c*(c-1)//2 for c in counts.values()), denominator)) if denominator else None}
                     for i, counts in enumerate(pattern_counts)]
    return {"status": "PLANTED_WORD_GEOMETRY_ONLY_NOT_UNIFORM_TARGET_COVERAGE",
            "uniform_independent_words": True, "targets_would_be_planted_size_biased": True,
            "uniform_target_pair_coverage_estimated": False, "samples": samples,
            "minimum_repairs_magnitude_one_histogram": dict(hist),
            "minimum_chart_maximum_magnitude_histogram": {str(k): v for k, v in sorted(magnitudes.items())},
            "repair_pattern_sample_statistics": pattern_stats,
            "pattern_collision_estimates_are_not_certified_population_moments": True,
            "word_records": records}


def _serialized_prepared(prepared):
    return {"seed": prepared["seed"], "number_charts": len(prepared["charts"]),
            "bases": [{"rows": [[str(x) for x in row] for row in b["rows"]],
                       "directions": [{"vector": [str(x) for x in r["direction"]], "multiplier": str(r["multiplier"]),
                                       "unperturbed_uniform_word_moments": {k: str(v) if isinstance(v, Fraction) else v for k, v in projection_moments(r).items()}}
                                      for r in direction]}
                      for b, direction in zip(prepared["bases"], prepared["directions"])],
            "offsets": [[str(x) for x in offset] for offset in prepared["offsets"]],
            "lll_calls": prepared["lll_calls"]}


def build_report():
    rng = random.Random(83370); exact, probes = [], []
    for M in (2, 6, 10):
        Q = 3**(M+1)
        A = (1, 7, 11, 18) if M == 2 else tuple(rng.randrange(Q) for _ in range(2*M))
        problem = LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(A[::2], A[1::2])), 0)
        prepared = public_charts(problem, seed=83370+M)
        exact.append({"labels": [str(x) for x in A], "prepared": _serialized_prepared(prepared),
                      "census": exact_word_census(problem, prepared)})
    for r in (8, 12, 16, 24, 32):
        M = r-2; Q = 3**(r-1)
        for trial in range(3):
            A = tuple(rng.randrange(Q) for _ in range(2*M))
            problem = LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(A[::2], A[1::2])), 0)
            prepared = public_charts(problem, seed=83380+r+trial)
            probes.append({"root_digits": r, "width": M, "labels": [str(x) for x in A], "modulus": str(Q),
                           "prepared": _serialized_prepared(prepared),
                           "probe": planted_word_probe(problem, prepared, seed=83390+r+trial)})
    return {"status": "EXACT_DECODER_SPECIFIC_COVERAGE_NO_SPEEDUP_OR_HARDNESS",
            "local_derivations_review_pending": True, "polynomial_pair_finder_proved": False,
            "novelty_claim": False, "uniform_target_population_coverage_proved": False,
            "predicate": "Fixed public basis/center word appears in complete k-repair list iff at mostk rounded exact GS errors are nonzero and each magnitude<=B.",
            "deterministic_counting_bound": "beta_label<=3^M*gamma/(2Q); gamma/6 at underfull scalar source scale",
            "list_cost": "number_charts*sum_{j=0}^k binomial(2M,j)*(2B)^j",
            "analysis_never_given_to_public_solver": True, "exact_controls": exact, "planted_geometry_probes": probes,
            "unrounded_projection_covariances_zero_but_rounding_errors_not_assumed_independent": True,
            "scope_exclusions": ["General CVP solvers.", "Arbitrary quantum POVMs or nonlinear native instruments.",
                                 "Classical hardness of the native phase source.", "Uniform-target guarantees from planted-word data."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True); REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "exact": [{"width": c["census"]["source_width"],
        "truth_pairs": c["census"]["true_pair_targets"], "depth_one": c["census"]["layers"][0]["depths"][1],
        "depth_two": c["census"]["layers"][0]["depths"][2]} for c in report["exact_controls"]],
        "planted_word_probe_batches": len(report["planted_geometry_probes"])}, indent=2))
