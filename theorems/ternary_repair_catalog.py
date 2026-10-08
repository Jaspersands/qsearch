"""Fixed public repair catalogs: exact decoders and collision-mass falsifiers.

LOCAL DERIVATIONS / REVIEW PENDING. Public known-word training is not unknown
quantum-phase access. No polynomial population coverage theorem is supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random
import time

from flint import fmpq, fmpz_mat

from native_rlwe_primal_babai import exact_row_profile
from ternary_pair_collimation import LowProblem, verify_pair
from ternary_pair_lattice import congruence_basis, coset_target, decode_shell, inverse_embed, public_center_offsets, scalar_labels, shell_norm
from ternary_pair_cell_coverage import compile_chart, integer_gs_directions, rounded_errors

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "research/phase_workbench/ternary_pair_cell_coverage.json"
REPORT = ROOT / "research/phase_workbench/ternary_repair_catalog.json"


def _positive(x, name):
    if type(x) is not int or x < 1: raise ValueError(f"positive integer {name} required")
    return x


def frozen_policy(problem, saved):
    """Revalidate frozen integer bases/GS directions; never silently rerun LLL."""
    A = scalar_labels(problem); M = problem.width; Q = problem.moduli[0]
    if M > 32: raise ValueError("finite policy replay width guard32")
    geometry = congruence_basis(problem); bases, directions = [], []
    offsets = tuple(tuple(Fraction(x) for x in row) for row in saved["offsets"])
    if offsets != public_center_offsets(M, saved["seed"], len(offsets)-1):
        raise ValueError("saved offsets disagree with public seed")
    for old in saved["bases"]:
        rows = tuple(tuple(int(x) for x in row) for row in old["rows"])
        if len(rows) != 2*M or any(len(row) != 3*M or any(x % 3 for x in row) for row in rows):
            raise ValueError("full integer embedded row basis required")
        kernel = tuple(inverse_embed(tuple(x//3 for x in row)) for row in rows)
        if any(sum(a*x for a, x in zip(A, row)) % Q for row in kernel):
            raise ValueError("saved basis left original kernel")
        R = fmpz_mat(rows)
        if int((R*R.transpose()).det()) != geometry["gram_determinant"]:
            raise ValueError("saved rows do not generate the full original kernel")
        profile = exact_row_profile(rows)
        expected_directions = integer_gs_directions(rows, profile)
        d = []
        for i, old_direction in enumerate(old["directions"]):
            v = tuple(int(x) for x in old_direction["vector"]); mult = Fraction(old_direction["multiplier"])
            if len(v) != 3*M or math.gcd(*v) != 1 or any(sum(v[j:j+3]) for j in range(0, len(v), 3)):
                raise ValueError("canonical primitive native GS direction required")
            inner = sum(x*y for x, y in zip(rows[i], v))
            if inner <= 0 or mult != Fraction(1, inner) or any(sum(x*y for x, y in zip(prior, v)) for prior in rows[:i]):
                raise ValueError("saved GS direction is not the true row projection")
            if v != expected_directions[i]["direction"] or mult != expected_directions[i]["multiplier"]:
                raise ValueError("orthogonality alone does not prove the actual GS projection")
            d.append({"direction": v, "multiplier": mult})
        if len(d) != len(rows): raise ValueError("full GS direction list required")
        bases.append({"rows": rows, "kernel_rows": kernel, "profile": profile,
                      "mu_q": tuple(tuple(fmpq(x.numerator, x.denominator) for x in r) for r in profile["mu"]),
                      "gs_q": tuple(fmpq(x.numerator, x.denominator) for x in profile["gs_squared"])})
        directions.append(tuple(d))
    if not bases or saved["number_charts"] != len(bases)*len(offsets):
        raise ValueError("nonempty complete saved chart schedule required")
    charts = tuple(compile_chart(d, offset) for d in directions for offset in offsets)
    key = {"labels": A, "Q": Q, "bases": [b["rows"] for b in bases], "offsets": [[str(x) for x in o] for o in offsets]}
    digest = hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()
    return {"labels": A, "Q": Q, "width": M, "geometry": geometry, "bases": bases,
            "offsets": offsets, "charts": charts, "frozen_geometry_sha256": digest,
            "lll_calls_rerun": 0, "original_lll_preparations_per_fresh_labels": len(bases)}


def _belongs(problem, policy):
    if policy["labels"] != scalar_labels(problem) or policy["Q"] != problem.moduli[0]:
        raise ValueError("policy belongs to different original labels")


def train_patterns(problem, policy, words=512, seed=0):
    _belongs(problem, policy); _positive(words, "training words")
    if type(seed) is not int: raise ValueError("integer training seed required")
    rng = random.Random(seed); counts = [Counter() for _ in policy["charts"]]
    collisions = [0]*len(counts); previous = None; start = time.perf_counter()
    for i in range(words):
        word = tuple(rng.randrange(3) for _ in range(problem.width))
        patterns = tuple(tuple(-x for x in rounded_errors(word, chart)) for chart in policy["charts"])
        for chart_counts, pattern in zip(counts, patterns): chart_counts[pattern] += 1
        if i % 2:
            for j, (a, b) in enumerate(zip(previous, patterns)): collisions[j] += a == b
        else: previous = patterns
    return {"counts": tuple(counts), "training_seed": seed, "training_words": words,
            "independent_disjoint_word_pairs": words//2, "disjoint_equal_pattern_pairs": tuple(collisions),
            "word_chart_classifications": words*len(counts), "wall_seconds": time.perf_counter()-start,
            "trained_from_target_or_unknown_phase": False, "fingerprint": policy["frozen_geometry_sha256"]}


def select_catalog(policy, training, per_chart=64):
    _positive(per_chart, "per-chart catalog budget")
    if training["fingerprint"] != policy["frozen_geometry_sha256"]:
        raise ValueError("training belongs to a different frozen public policy")
    zero = (0,)*(2*policy["width"]); selected = []
    for counts in training["counts"]:
        ranked = sorted(counts, key=lambda p: (-counts[p], p))
        # The ordinary Babai path has a reserved, fully charged public slot.
        selected.append((zero, *tuple(p for p in ranked if p != zero)[:per_chart-1]))
    return {"patterns": tuple(selected), "per_chart_budget": per_chart,
            "total_pattern_decodes_budget": sum(map(len, selected)),
            "training_words_per_fresh_label_attempt": training["training_words"],
            "fingerprint": policy["frozen_geometry_sha256"], "target_independent": True}


def _target_coordinates(basis, target):
    mu, norms = basis["mu_q"], basis["gs_q"]; inner = []
    T = tuple(fmpq(x.numerator, x.denominator) for x in target)
    for i, row in enumerate(basis["rows"]):
        inner.append(sum((a*b for a, b in zip(row, T)), fmpq(0))-
                     sum((mu[i][j]*inner[j] for j in range(i)), fmpq(0)))
    return tuple(a/b for a, b in zip(inner, norms))


def force_pattern(basis, coordinates, pattern):
    d = len(basis["rows"])
    if len(pattern) != d or any(type(x) is not int for x in pattern):
        raise ValueError("canonical complete integer forced pattern required")
    c = list(coordinates); integers = [0]*d
    for i in range(d-1, -1, -1):
        x = c[i]; integers[i] = int((2*x.p+x.q)//(2*x.q))+pattern[i]
        for j in range(i): c[j] -= integers[i]*basis["mu_q"][i][j]
    return tuple(integers)


def catalog_pair(problem, target, policy, catalog, max_decodes=None):
    _belongs(problem, policy); target = problem.target(target)
    if catalog["fingerprint"] != policy["frozen_geometry_sha256"]:
        raise ValueError("catalog belongs to different frozen public geometry")
    if max_decodes is not None: _positive(max_decodes, "decode cap")
    data = coset_target(problem, target, policy["geometry"])
    cost = {"candidate_decodes": 0, "rounding_steps": 0, "non_shell_candidates": 0, "duplicate_words": 0,
            "training_words_per_fresh_label_attempt": catalog["training_words_per_fresh_label_attempt"],
            "original_lll_preparations_per_fresh_labels": policy["original_lll_preparations_per_fresh_labels"],
            "frozen_bases_replayed_no_lll_rerun": True, "target_independent_catalog": True}
    if data is None: return {"status": "DIVISIBILITY_CERTIFIED_EMPTY", "pair": (), "witnesses": (), "cost": cost, "accepted_traces": []}
    z0, T = data; found, accepted = [], []; offset_count = len(policy["offsets"]); start = time.perf_counter()
    for chart_index, patterns in enumerate(catalog["patterns"]):
        basis = policy["bases"][chart_index//offset_count]
        offset = policy["offsets"][chart_index % offset_count]
        coordinates = _target_coordinates(basis, tuple(Fraction(x)+y for x, y in zip(T, offset)))
        for pattern_index, pattern in enumerate(patterns):
            if max_decodes is not None and cost["candidate_decodes"] >= max_decodes:
                cost["decode_wall_seconds"] = time.perf_counter()-start
                return {"status": "DECODE_CAP_NO_PAIR", "pair": (), "witnesses": tuple(found), "cost": cost, "accepted_traces": accepted}
            coeff = force_pattern(basis, coordinates, pattern)
            cost["candidate_decodes"] += 1; cost["rounding_steps"] += len(coeff)
            z = tuple(a+sum(c*r[j] for c, r in zip(coeff, basis["kernel_rows"])) for j, a in enumerate(z0))
            word = decode_shell(z)
            if word is None: cost["non_shell_candidates"] += 1; continue
            if problem.value(word) != target: raise ArithmeticError("catalog left original congruence coset")
            if word in found: cost["duplicate_words"] += 1; continue
            found.append(word); accepted.append({"chart": chart_index, "pattern_index": pattern_index,
                "word": word, "integer_coset_coordinates": z, "reduced_basis_coefficients": coeff,
                "exact_original_norm": str(shell_norm(z))})
            if len(found) == 2:
                cost["decode_wall_seconds"] = time.perf_counter()-start
                return {"status": "VERIFIED_CATALOG_PAIR_NO_COVERAGE_THEOREM", "pair": verify_pair(problem, target, found),
                        "witnesses": tuple(found), "cost": cost, "accepted_traces": accepted}
    cost["decode_wall_seconds"] = time.perf_counter()-start
    return {"status": "CATALOG_EXHAUSTED_NOT_UNSAT_PROOF", "pair": (), "witnesses": tuple(found), "cost": cost, "accepted_traces": accepted}


def sqrt_upper(x, bits=24):
    x = Fraction(x)
    if x < 0: raise ValueError("nonnegative rational square root required")
    _positive(bits, "dyadic precision")
    scale = 1 << bits; scaled = x.numerator*scale*scale
    root = math.isqrt(scaled//x.denominator)
    if root*root*x.denominator < scaled: root += 1
    return Fraction(root, scale)


def binomial_upper(n, successes, alpha=Fraction(1, 1800), bits=32):
    """One-sided rational upper endpoint; disjoint pairs only, no U-stat fiction."""
    _positive(n, "independent trials"); _positive(bits, "precision")
    if type(successes) is not int or not 0 <= successes <= n or type(alpha) is not Fraction or not 0 < alpha < 1:
        raise ValueError("valid integer successes and exact rational tail required")
    if successes == n: return Fraction(1)
    def tail(p):
        a, b = p.numerator, p.denominator
        return Fraction(sum(math.comb(n, i)*a**i*(b-a)**(n-i) for i in range(successes+1)), b**n)
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(bits):
        mid = (lo+hi)/2
        if tail(mid) <= alpha: hi = mid
        else: lo = mid
    assert tail(hi) <= alpha
    return hi


def heldout_words(problem, policy, catalogs, words=256, seed=0):
    _belongs(problem, policy)
    if type(seed) is not int or any(c["fingerprint"] != policy["frozen_geometry_sha256"] for c in catalogs):
        raise ValueError("integer heldout seed and catalogs for these public labels required")
    _positive(words, "held-out words"); rng = random.Random(seed)
    sets = [tuple(set(p) for p in c["patterns"]) for c in catalogs]; counts = [0]*len(catalogs)
    for _ in range(words):
        word = tuple(rng.randrange(3) for _ in range(problem.width))
        patterns = tuple(tuple(-x for x in rounded_errors(word, chart)) for chart in policy["charts"])
        for i, selected in enumerate(sets): counts[i] += any(p in S for p, S in zip(patterns, selected))
    return {"status": "INDEPENDENT_HELDOUT_WORDS_NOT_UNIFORM_TARGET_PAIR_BENCHMARK", "words": words, "seed": seed,
            "catalog_word_recall_counts": counts, "target_pair_coverage_estimated": False}


def exact_catalog_census(problem, policy, catalog, max_words=100_000):
    _belongs(problem, policy); _positive(max_words, "exact word budget")
    if catalog["fingerprint"] != policy["frozen_geometry_sha256"]: raise ValueError("catalog belongs to different source")
    D = 3**problem.width; Q = problem.moduli[0]
    if D > max_words: return {"status": "WORD_BUDGET_NO_PARTIAL_CENSUS", "words_classified": 0}
    counts = [Counter() for _ in policy["charts"]]; selected = [set(p) for p in catalog["patterns"]]
    covered_words, covered_targets = 0, Counter()
    for word in product(range(3), repeat=problem.width):
        patterns = tuple(tuple(-x for x in rounded_errors(word, chart)) for chart in policy["charts"])
        for hist, p in zip(counts, patterns): hist[p] += 1
        if any(p in S for p, S in zip(patterns, selected)):
            covered_words += 1; covered_targets[problem.value(word)[0]] += 1
    chart_bounds = []; upper = Fraction(0)
    for hist, patterns in zip(counts, catalog["patterns"]):
        C = Fraction(sum(n*n for n in hist.values()), D*D)
        mass = Fraction(sum(hist[p] for p in patterns), D); squared = len(patterns)*C
        assert mass*mass <= squared
        upper += sqrt_upper(squared)
        chart_bounds.append({"true_pattern_collision_mass": str(C), "catalog_captured_word_mass": str(mass),
            "catalog_size": len(patterns), "cauchy_squared_mass_upper": str(squared),
            "best_possible_top_K_word_mass": str(Fraction(sum(sorted(hist.values(), reverse=True)[:len(patterns)]), D))})
    union_upper = min(Fraction(1), upper); beta = Fraction(sum(n >= 2 for n in covered_targets.values()), Q)
    gamma = Fraction(covered_words, D)
    assert gamma <= union_upper and beta <= Fraction(D, 2*Q)*union_upper
    return {"status": "EXACT_EXPONENTIAL_CONDITIONAL_CATALOG_ANALYSIS", "words_classified": D,
            "recovered_words": covered_words, "gamma_exact": str(gamma), "uniform_target_beta_exact": str(beta),
            "pair_covered_targets": sum(n >= 2 for n in covered_targets.values()), "chart_collision_bounds": chart_bounds,
            "union_gamma_dyadic_upper": str(union_upper), "pair_beta_dyadic_upper": str(Fraction(D, 2*Q)*union_upper),
            "analysis_not_given_to_catalog_training": True}


def _sparse_catalog(catalog):
    return [[[ [i,x] for i,x in enumerate(pattern) if x] for pattern in patterns] for patterns in catalog["patterns"]]


def build_report():
    source = json.loads(FIXTURE.read_text()); cases = []
    comparisons = sum(c["prepared"]["number_charts"] for c in source["planted_geometry_probes"])
    _positive(comparisons, "statistical chart comparisons")
    alpha = Fraction(1, 20*comparisons)
    for case_index, fixture in enumerate(source["planted_geometry_probes"]):
        Q = int(fixture["modulus"]); A = tuple(int(x) for x in fixture["labels"]); M = len(A)//2
        problem = LowProblem((Q,), tuple(((a,), (c,)) for a,c in zip(A[::2],A[1::2])), 0)
        if fixture["root_digits"] != M+2 or Q != 3**(M+1): raise ValueError("underfull original source scale required")
        policy = frozen_policy(problem, fixture["prepared"])
        training = train_patterns(problem, policy, seed=83600+case_index)
        catalogs = [select_catalog(policy, training, k) for k in (16,64,256)]
        heldout = heldout_words(problem, policy, catalogs, seed=83700+case_index)
        catalog = catalogs[1]; statistical = []
        for successes in training["disjoint_equal_pattern_pairs"]:
            U = binomial_upper(training["independent_disjoint_word_pairs"], successes, alpha)
            statistical.append({"independent_word_pairs": training["independent_disjoint_word_pairs"], "successes": successes,
                                "conditional_collision_upper_assuming_IID_words": str(U), "per_chart_failure_probability": str(alpha)})
        # Bonferroni requires no independence across the shared-word charts.
        stat_gamma = min(Fraction(1), sum(sqrt_upper(len(p)*Fraction(s["conditional_collision_upper_assuming_IID_words"]))
                                         for p,s in zip(catalog["patterns"],statistical)))
        rng = random.Random(83800+case_index); trials = []
        for j in range(8):
            target = (rng.randrange(Q),); solved = catalog_pair(problem,target,policy,catalog)
            trials.append({"target": str(target[0]), "status": solved["status"], "pair": solved["pair"],
                           "witnesses": solved["witnesses"], "cost": solved["cost"], "accepted_traces": solved["accepted_traces"]})
        exact = exact_catalog_census(problem,policy,catalog) if M <= 10 else None
        cases.append({"fixture_probe_index": case_index, "root_digits": fixture["root_digits"], "width": M,
                      "labels": [str(x) for x in A], "Q": str(Q), "fingerprint": policy["frozen_geometry_sha256"],
                      "training": {k:v for k,v in training.items() if k != "counts"}, "heldout": heldout,
                      "catalog_budgets": [16,64,256], "actual_catalog_sizes": [list(map(len,c["patterns"])) for c in catalogs],
                      "live_per_chart_budget":64, "sparse_live_catalog":_sparse_catalog(catalog),
                      "collision_confidence":statistical, "conditional_statistical_gamma_upper": str(stat_gamma),
                      "statistical_bound_not_a_population_or_asymptotic_proof":True,
                      "uniform_target_trials":trials,"target_reuse_is_conditional_debugging_not_free_physical_amortization":True,
                      "exact_small_catalog_census":exact})
    return {"status":"FIXED_PUBLIC_CATALOGS_TESTED_NO_SCALABLE_PAIR_GUARANTEE", "local_derivations_review_pending":True,
            "polynomial_pair_finder_proved":False,"novelty_claim":False,"fixture":str(FIXTURE.relative_to(ROOT)),
            "LLL_rerun_calls":0,"all_preparation_training_and_failure_costs_charged":True,
            "statistical_family_IID_assumption_failure_union_upper":"1/20", "statistical_charts_not_independent":True,
            "cauchy_bound":"gamma_chart^2<=K*sum_pattern_probability_squared; union beta<=gamma_union/6",
            "target_adaptive_repairs_excluded_from_catalog_obstruction":True,"cases":cases}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--write",action="store_true")
    args=parser.parse_args(); report=build_report()
    if args.write: REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"cases":[{"root_digits":c["root_digits"],"heldout_recall":c["heldout"]["catalog_word_recall_counts"],
        "pairs_in_eight_uniform_targets":sum(bool(t["pair"]) for t in c["uniform_target_trials"]),
        "stat_gamma_upper":c["conditional_statistical_gamma_upper"]} for c in report["cases"]]},indent=2))
