"""Independent bounded algebra controls; no parent imports or sampler replays.

Run with Python -B. Results go to stdout; this script never writes files.
"""

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
import json


def rank(rows, p):
    a = [list(row) for row in rows]
    height, width = len(a), len(a[0]) if a else 0
    pivot = 0
    for j in range(width):
        found = next((i for i in range(pivot, height) if a[i][j] % p), None)
        if found is None:
            continue
        a[pivot], a[found] = a[found], a[pivot]
        inverse = pow(a[pivot][j] % p, -1, p)
        a[pivot] = [(x * inverse) % p for x in a[pivot]]
        for i in range(height):
            if i != pivot:
                factor = a[i][j] % p
                a[i] = [(x - factor * y) % p
                        for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == height:
            break
    return pivot


def dot(x, y, p):
    return sum(a * b for a, b in zip(x, y)) % p


def projective_data(b, p):
    """One representative per nonzero scalar orbit, also for dependent rows."""
    k, m = len(b), len(b[0])
    result = []
    for u in product(range(p), repeat=k):
        if next((x for x in u if x), 0) != 1:
            continue
        word = tuple(sum(u[i] * b[i][j] for i in range(k)) % p
                     for j in range(m))
        result.append((u, sum(x != 0 for x in word)))
    return result


def character_count(b, s, p, data, *, signed=True, phase=True):
    k, m = len(b), len(b[0])
    tail = Fraction(0)
    for u, weight in data:
        scalar_sum = p - 1 if not phase or dot(u, s, p) == 0 else -1
        sign = (-1)**weight if signed else 1
        tail += Fraction(scalar_sum * sign, (p - 1)**weight)
    return Fraction((p - 1)**m, p**k) * (1 + tail), tail


def inclusion_exclusion_count(b, s, p):
    """Count by coordinate-zero subsets and affine ranks, not word enumeration."""
    m = len(b[0])
    answer = 0
    for mask in range(1 << m):
        keep = [j for j in range(m) if not (mask >> j) & 1]
        restricted = [[row[j] for j in keep] for row in b]
        r = rank(restricted, p)
        if rank([row + [value] for row, value in zip(restricted, s)], p) == r:
            answer += (-1)**mask.bit_count() * p**(len(keep) - r)
    return answer


def run():
    fixtures = [
        ("even_weight_phase", 3, ((1, 1),)),
        ("odd_weight_sign", 3, ((1, 1, 1),)),
        ("forced_zero", 5, ((1, 0),)),
        ("square_unique_point", 3, ((1, 0), (0, 1))),
        ("correlated_pivots_empty_fiber", 3, ((1, 0, 1), (0, 1, 1))),
        ("nonleading_pivots_zero_column", 5, ((0, 0, 2, 1, 0), (0, 1, 1, 0, 2))),
        ("scaled_columns", 7, ((2, 1, 4, 0), (0, 3, 2, 6))),
        ("rank_deficient_promise_trap", 5, ((1, 1, 1, 1), (1, 1, 1, 1))),
    ]
    receipts, all_counts = [], {}
    comparisons = cap_checks = sign_mutations = phase_mutations = 0
    phase_reversal_checks = 0
    for name, p, b in fixtures:
        k, m, r = len(b), len(b[0]), rank(b, p)
        data = projective_data(b, p)
        counts = {}
        nonzero_weights = [weight for _, weight in data if weight]
        delta = min(nonzero_weights)
        alpha = Fraction(p**k - 1, (p - 1)**delta)
        max_tail = Fraction(0)
        local_sign_failures = local_phase_failures = 0
        for s in product(range(p), repeat=k):
            count = inclusion_exclusion_count(b, s, p)
            fourier, tail = character_count(b, s, p, data)
            assert fourier.denominator == 1 and fourier == count
            assert count >= 0
            counts[s] = count
            comparisons += 1
            max_tail = max(max_tail, abs(tail))
            local_sign_failures += character_count(b, s, p, data, signed=False)[0] != count
            local_phase_failures += character_count(b, s, p, data, phase=False)[0] != count
            if r == k:
                assert abs(tail) <= alpha
                proposals = (p - 1)**(m - k)
                probability = Fraction(count, proposals)
                assert 0 <= probability <= 1
                assert probability == Fraction(p - 1, p)**k * (1 + tail)
                if count:
                    affine = Fraction(count, p**(m - k))
                    assert probability / affine == Fraction(p, p - 1)**(m - k)
                    for cap in (1, 2, 4):
                        # Per-witness probability under a uniform injective proposal.
                        first_mass = sum((1 - probability)**t / proposals
                                         for t in range(cap))
                        success_mass = 1 - (1 - probability)**cap
                        assert first_mass / success_mass == Fraction(1, count)
                        cap_checks += 1
        assert sum(counts.values()) == (p - 1)**m
        for s, count in counts.items():
            assert counts[tuple((-x) % p for x in s)] == count
            phase_reversal_checks += 1
        all_counts[name] = counts
        sign_mutations += local_sign_failures
        phase_mutations += local_phase_failures
        receipts.append({
            "fixture": name, "prime": p, "matrix": b, "rank": r,
            "syndromes_checked": len(counts), "empty_fibers": sum(v == 0 for v in counts.values()),
            "nonzero_rowspace_minimum_weight": delta,
            "max_abs_tail": str(max_tail), "formal_alpha_using_row_count": str(alpha),
            "unsigned_weight_mutation_failures": local_sign_failures,
            "omitted_phase_mutation_failures": local_phase_failures,
            "counts_in_lexicographic_syndrome_order": list(counts.values()),
        })

    assert list(all_counts["even_weight_phase"].values()) == [2, 1, 1]
    assert list(all_counts["odd_weight_sign"].values()) == [2, 3, 3]
    assert all_counts["correlated_pivots_empty_fiber"][(1, 2)] == 0
    assert all_counts["forced_zero"][(0,)] == 0
    false_distance_success = Fraction(4, 5) * (1 - Fraction(4, 4**2))
    assert false_distance_success == Fraction(3, 5) > 0
    assert all_counts["square_unique_point"][(1, 2)] == 1
    assert all_counts["square_unique_point"][(1, 0)] == 0
    assert all_counts["rank_deficient_promise_trap"][(0, 1)] == 0
    assert Fraction(5**2 - 1, 4**4) == Fraction(3, 32) < 1
    assert sign_mutations and phase_mutations

    q = 100003
    tower = []
    with localcontext() as context:
        context.prec = 60
        dlog = (Decimal(q) / Decimal(q - 1)).ln() / Decimal(2).ln()
        for e in (8, 16, 32, 64, 128, 1024):
            k, delta = 5*e + 3, 12*e - 3
            alpha = Fraction(q**k - 1, (q - 1)**delta)
            loose = Fraction(1, q**(e - 5))
            assert alpha < loose <= Fraction(1, q**3) < Fraction(1, 2)
            assert (q - 1)**(12*e - 4) > q**(6*e - 2)
            alpha_decimal = Decimal(alpha.numerator) / Decimal(alpha.denominator)
            base_trials = (Decimal(q) / Decimal(q - 1))**k
            tower.append({
                "e": e, "k": k, "delta_lower": delta,
                "alpha_decimal_approximation": str(alpha_decimal),
                "loose_tail_decimal_approximation": str(Decimal(1) / Decimal(q)**(e - 5)),
                "base_trial_factor_decimal_approximation": str(base_trials),
                "worst_rank_four_list_log2_length": (10*e + 4) // 3,
                "four_list_tower_contract_covers_level": e >= 64,
                "exact_inequalities_passed": True,
            })
        rates = {
            "systematic_log2_trials_per_e_decimal_approximation": str(5*dlog),
            "rank_per_e_comparison_threshold_decimal_approximation": str(15*dlog),
        }

    return {
        "status": "PASS", "imports_parent_sampler": False,
        "enumerates_nonzero_free_assignments": False,
        "method": "exact projective character sums versus rank inclusion-exclusion",
        "fixture_count": len(fixtures), "all_syndrome_comparisons": comparisons,
        "conditional_cap_mass_identities": cap_checks,
        "phase_reversal_invariance_checks": phase_reversal_checks,
        "false_distance_promise_success_bound_on_empty_full_rank_fiber": str(false_distance_success),
        "unsigned_weight_mutation_failures": sign_mutations,
        "omitted_phase_mutation_failures": phase_mutations,
        "fixtures": receipts, "tower_exact_arithmetic_controls": tower,
        "rates": rates,
        "scope": "Bounded algebra controls, not a proof by extrapolation or a production implementation test.",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
