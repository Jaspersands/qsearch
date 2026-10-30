"""Exhaustive distribution controls, not an algorithm for large instances."""

from collections import Counter
from fractions import Fraction
from itertools import product

from norm_sampling import GlobalNormSampler, NormCompletion
from norm_completion import affine_solution, rank


def fixture(outside=True):
    B = [[4, 3, 2, 1]+([1] if outside else [])]
    A = [[1, 1, 1, 1]+([0] if outside else []),
         [0, 1, 2, 3]+([0] if outside else [])]
    return NormCompletion(5, B, A, [1]*4+([0] if outside else []), 2)


def normalized(counts):
    total = sum(counts.values())
    return {word: Fraction(value, total) for word, value in counts.items()}


def tv(left, right):
    return sum((abs(left.get(x, 0)-right.get(x, 0))
                for x in left.keys() | right.keys()), Fraction(0))/2


def enumerate_control(syndrome=1, outside=True):
    case = fixture(outside)
    sampler = GlobalNormSampler(case)
    p, r = case.p, case.r
    all_lifts, good_lifts, wrong_retries, frozen_outside = (Counter() for _ in range(4))
    weighted_native, full_rank_only = Counter(), Counter()
    good_cosets, deficient_moment, weighted_bad = 0, 0, 0
    valid_sizes = []
    # Columns0,1 form an information set of A. Offsets zero there give
    # exactly one representative of every coset of row(A) in F_5^4.
    for tail in product(range(p), repeat=4):
        a, b = [0, 0, *tail[:2]], [0, 0, *tail[2:]]
        probe = case.prepare([syndrome], a, b)
        M = probe["matrix"]
        deficiency = case.k-rank(M, p)
        # R=2, k=1: each nonzero lambda has rank(U_lambda)=2.
        # Its conditioned offsets occupy one coset; thinning is1.
        mixture_denominator = p**4+(p-1)
        coset_mass = Fraction(p**4, mixture_denominator*p**4)
        for coefficient in range(1, p):
            if all(coefficient*x % p == 0 for x in M[0]):
                coset_mass += Fraction(1, mixture_denominator)
        good = (probe["status"] == "CERTIFIED_AFFINE_FIBER"
                and all(event["rank"] == 2 for event in probe["events"]))
        good_cosets += good
        deficient_moment += p**deficiency-1
        weighted_bad += (not good)*p**deficiency
        for outside_values in product(range(1, p), repeat=len(sampler.outside)):
            base = case.evaluate([0]*(2*r), a, b)
            for i, value in zip(sampler.outside, outside_values):
                base[i] = value
            target = [(syndrome-sum(x*y for x, y in zip(case.B[0], base))) % p]
            try:
                point, kernel = affine_solution(M, target, p)
            except ValueError:
                continue
            local = Counter()
            all_local = Counter()
            for free in product(range(p), repeat=len(kernel[0])):
                coefficients = [(x+sum(u*v for u, v in zip(row, free))) % p
                                for x, row in zip(point, kernel)]
                word = case.evaluate(coefficients, a, b)
                for i, value in zip(sampler.outside, outside_values):
                    word[i] = value
                assert sum(x*y for x, y in zip(case.B[0], word)) % p == syndrome
                if all(word):
                    word = tuple(word)
                    all_lifts[word] += 1
                    all_local[word] += 1
                    if good:
                        local[word] += 1
            per_lift_mass = coset_mass / (p**len(kernel[0])*(p-1)**len(sampler.outside))
            for word, count in all_local.items():
                weighted_native[word] += per_lift_mass*count
            if deficiency == 0:
                full_rank_only.update(all_local)
            if good:
                good_lifts.update(local)
                valid_sizes.append(sum(local.values()))
                for word, value in normalized(local).items():
                    wrong_retries[word] += value
                if not outside or outside_values == (1,):
                    frozen_outside.update(local)
    total_cosets = p**4
    uniform = normalized(all_lifts)
    good_law = normalized(good_lifts)
    wrong_law = normalized(wrong_retries)
    frozen_law = normalized(frozen_outside)
    bad_probability = Fraction(total_cosets-good_cosets, total_cosets)
    moment = Fraction(deficient_moment, total_cosets)
    weighted = Fraction(weighted_bad, total_cosets)
    alpha = (1-bad_probability)*(1-Fraction(4, p*p))
    bound = weighted/(alpha+weighted)
    return {
        "q": p, "syndrome": syndrome, "outside_randomized": outside,
        "cosets": total_cosets, "good_cosets": good_cosets,
        "native_witnesses": len(all_lifts),
        "norm_lift_multiplicities": sorted(set(all_lifts.values())),
        "good_coset_valid_lift_min": min(valid_sizes),
        "good_coset_valid_lift_max": max(valid_sizes),
        "bad_coset_probability": bad_probability,
        "deficiency_moment": moment,
        "weighted_bad_coset_mass": weighted,
        "weighted_bound_equals_probability_plus_moment": weighted == bad_probability+moment,
        "lift_tv_exact": 1-Fraction(sum(good_lifts.values()), sum(all_lifts.values())),
        "native_tv_exact": tv(good_law, uniform),
        "native_tv_certified_upper": bound,
        "whole_trial_success_exact": Fraction(sum(good_lifts.values()),
                                               (p-1)**len(sampler.outside)*total_cosets*p**3),
        "retry_same_coset_changes_law_tv": tv(wrong_law, good_law),
        "freeze_outside_changes_law_tv": tv(frozen_law, good_law),
        "native_reference_uniform": len(set(uniform.values())) == 1,
        "rank_weighted_native_tv_exact": tv(normalized(weighted_native), uniform),
        "rank_weighted_trial_success_exact": sum(weighted_native.values()),
        "count_recovered_from_acceptance": (sum(weighted_native.values())
             *(p-1)**len(sampler.outside)*p**7*Fraction(p**4+p-1, p**4)/6**4),
        "discard_rank_deficient_native_tv_exact": tv(normalized(full_rank_only), uniform),
    }
