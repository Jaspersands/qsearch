"""Exact finite controls for analytic bounds, not native algorithm executions."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import comb, isqrt, prod
from pathlib import Path

from flint import fmpq_mat
import pytest

from theorems import mersenne_global_structure as structure
from theorems.mersenne_reciprocal_access import finite_walsh_spectrum
from theorems.mersenne_reciprocal_curve import reciprocal_trace
from theorems.explicit_quadratic_opi import element, encoded


@pytest.mark.parametrize("bits,s,length,checks", [(3, 1, 6, 2), (3, 2, 5, 2),
                                                (5, 2, 6, 2), (5, 3, 5, 1)])
def test_moment_bounds_against_exact_counts_and_dual_parseval(bits, s, length, checks):
    q = 1 << bits
    field = [element(bits, x) for x in range(q)]
    spectrum = finite_walsh_spectrum(bits, s)
    beta = max(Q(abs(w), q) for w in spectrum)
    fourth = sum((Q(w, q)**4 for w in spectrum), Q(0))
    report = structure.mds_moment_bounds(bits, length, checks, beta, fourth)
    for targets in ([0]*length, [i % 2 for i in range(length)]):
        counts = {(0,)*checks: 1}
        for i, target in enumerate(targets):
            roots = [x for x in range(q) if reciprocal_trace(bits, s, x) == target]
            contributions = [tuple(encoded(field[x]*field[i]**j) for j in range(checks))
                             for x in roots]
            following = defaultdict(int)
            for y, count in counts.items():
                for v in contributions:
                    following[tuple(a ^ b for a, b in zip(y, v))] += count
            counts = following
        mean = report["mean_completion_count"]
        errors = [Q(counts.get(y, 0), 1)/mean-1
                  for y in product(range(q), repeat=checks)]
        variance = sum((e*e for e in errors), Q(0))/q**checks
        assert variance <= report["syndrome_variance_upper"]
        assert variance >= report["syndrome_variance_integer_lower"]
        assert max(map(abs, errors)) <= report["uniform_error_upper"]
        if report["uniform_error_parseval_upper"] is not None:
            assert max(map(abs, errors)) <= report["uniform_error_parseval_upper"]
        dual_variance = Q(0)
        for coefficients in product(range(q), repeat=checks):
            if not any(coefficients):
                continue
            term = Q(1)
            for i in range(length):
                value = field[0]
                for j, c in enumerate(coefficients):
                    value += field[c]*field[i]**j
                frequency = encoded(value)
                term *= Q(spectrum[frequency], q)**2 if frequency else 1
            dual_variance += term
        assert variance == dual_variance
        if report["all_syndromes_nonempty_certified"]:
            assert all(counts.get(y, 0) for y in product(range(q), repeat=checks))


@pytest.mark.parametrize("bits,s", [(3, 1), (5, 2)])
def test_finite_poisson_minorant_against_actual_spectrum(bits, s):
    # Exhaustive F8/F32 controls only, not a canonical native field table.
    q, length, checks = 1 << bits, 3, 2
    field = [element(bits, x) for x in range(q)]
    spectrum = finite_walsh_spectrum(bits, s)
    signs = [1-2*reciprocal_trace(bits, s, x) for x in range(q)]
    characters = [[1-2*int((u*z).trace()) for u in field] for z in field]
    assert spectrum == tuple(sum(v*c for v, c in zip(signs, row)) for row in characters)
    correlation = [Q(sum(signs[x]*signs[x ^ z] for x in range(q)), q) for z in range(q)]
    pi = [Q(w*w, q*q) for w in spectrum]
    absolute = [Q(1) if u == 0 else Q(abs(w), q) for u, w in enumerate(spectrum)]
    assert pi[0] == 0 and sum(pi) == 1
    tight_a = max(max(absolute[1:]), max(-c for c in correlation[1:]))
    pole_a = Q(2*((1 << s)-1)*(isqrt(q)+1)+3, q)

    points = [field[i] for i in (1, 2, 4)]
    dual = [tuple(encoded(field[c0]+field[c1]*alpha) for alpha in points)
            for c0, c1 in product(range(q), repeat=checks)]
    direction = [points[1]+points[2], points[0]+points[2], points[0]+points[1]]
    kernel = [tuple(encoded(c*v) for v in direction) for c in field]
    assert len(set(kernel)) == q
    for word in kernel:
        assert sum((field[x] for x in word), field[0]) == field[0]
        assert sum((alpha*field[x] for alpha, x in zip(points, word)), field[0]) == field[0]
    actual_l = sum((prod(absolute[u] for u in word) for word in dual), Q(0))-1

    for a in (tight_a, pole_a):
        h = [Q(u == 0)+pi[u]/a for u in range(q)]
        hhat = [sum((h[u]*row[u] for u in range(q)), Q(0)) for row in characters]
        assert all(0 <= v <= r for v, r in zip(h, absolute))
        assert all(v >= 0 for v in hhat)
        assert hhat == [1+c/a for c in correlation]
        dual_sum = sum((prod(h[u] for u in word) for word in dual), Q(0))
        primal_sum = sum((prod(hhat[x] for x in word) for word in kernel), Q(0))/q
        b_lower = (1+1/a)**length/q**(length-checks)
        assert b_lower <= dual_sum == primal_sum <= 1+actual_l
        assert max(Q(0), b_lower-1) <= actual_l
    if bits == 3:
        # F8 has an autocorrelation -1, so the sharp minorant is a boundary control.
        assert min(correlation) == -1 and (1+1/tight_a)**length/q == 1
    else:
        assert (1+1/tight_a)**length/q > 1


@pytest.mark.parametrize("bits,remaining,numerator,b_power,second_power,relative_power", [
    (17, 45, 5085, 60, 118, 116),
    (31, 136, 11770617, 526, 1050, 1048),
    (61, 496, 49755179191503, 5797, 11592, 11590),
])
def test_single_term_certificate_exact_canonical_bounds(
        bits, remaining, numerator, b_power, second_power, relative_power, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("analytic certificate must not evaluate a field spectrum or completion counts")

    monkeypatch.setattr("theorems.mersenne_reciprocal_access.finite_walsh_spectrum", forbidden)
    monkeypatch.setattr("theorems.mersenne_reciprocal_access.element", forbidden)
    monkeypatch.setattr(structure, "canonical_moments", forbidden)
    result = structure.single_term_importance_certificate(bits, remaining)
    q, checks, s = 1 << bits, (bits*bits-1)//8, (bits-3)//4
    assert numerator == 2*((1 << s)-1)*(isqrt(q-1)+1)+3
    expected_b = Q((q+numerator)**remaining, q**(remaining-checks)*numerator**remaining)
    assert result["A"] == numerator
    assert result["a"] == Q(numerator, q)
    assert result["B_lower"] == expected_b >= 1 << b_power
    assert result["L_lower"] == expected_b-1
    assert result["second_moment_lower"] == (expected_b-1)**2 >= 1 << second_power
    assert result["relative_variance_lower"] == (4*(expected_b-1)**2-1)/9 > 1 << relative_power
    for key in ("a", "B_lower", "L_lower", "second_moment_lower", "relative_variance_lower"):
        assert type(result[key]) is Q
    assert result["relative_variance_g_interval"] == (Q(1, 2), Q(3, 2))
    assert result["relative_variance_requires_g_interval"]
    assert result["optimal_proposal_access_granted"]
    for key in ("all_syndromes_in_g_interval_certified", "all_estimator_hardness_claimed",
                "native_solver_implemented", "field_tables_materialized"):
        assert result[key] is False


def test_single_term_certificate_clips_uninformative_bounds_before_squaring():
    result = structure.single_term_importance_certificate(17, 17**2)
    assert 0 < result["B_lower"] < 1
    for key in ("L_lower", "second_moment_lower", "relative_variance_lower"):
        assert result[key] == Q(0) and type(result[key]) is Q
    terminal = structure.single_term_importance_certificate(17, 36)
    assert terminal["free_symbols"] == 0
    assert terminal["B_lower"] == (1+1/terminal["a"])**36


@pytest.mark.parametrize("bits,remaining", [
    (True, 45), (17.0, 45), (3, 3), (18, 45), (21, 60), (131, 3000),
    (17, True), (17, 45.0), (17, 35), (17, 290),
])
def test_single_term_certificate_input_guards(bits, remaining):
    with pytest.raises(ValueError):
        structure.single_term_importance_certificate(bits, remaining)


@pytest.mark.parametrize("value", [Q(0), Q(1, 3), Q(3, 7), Q(2), Q(1000001, 7)])
@pytest.mark.parametrize("precision", [1, 7, 31])
def test_square_root_is_minimal_outward_dyadic(value, precision):
    upper = structure.dyadic_sqrt_upper(value, precision)
    assert upper*upper >= value
    assert upper == 0 or (upper-Q(1, 1 << precision))**2 < value


def _pattern_counts(bits, s, length):
    q = 1 << bits
    roots = [[x for x in range(q) if reciprocal_trace(bits, s, x) == b] for b in (0, 1)]
    counts = {(0, 0): 1}
    for i in range(length):
        following = defaultdict(int)
        for (y, pattern), count in counts.items():
            for b in (0, 1):
                for x in roots[b]:
                    following[(y ^ x, pattern | (b << i))] += count
        counts = following
    return counts


def _kernel_matrix(left, right, radius, target=0):
    n = left+right
    rows = []
    for a in range(1 << left):
        row = []
        for b in range(1 << right):
            weight = (target ^ a ^ (b << left)).bit_count()
            value = sum((-1)**ell*comb(weight, ell)*comb(n-weight, j-ell)
                        for j in range(radius+1) for ell in range(j+1)
                        if ell <= weight and j-ell <= n-weight)
            row.append(value)
        rows.append(row)
    return rows


@pytest.mark.parametrize("radius", [5, 6, 7, 8, 9])
@pytest.mark.parametrize("target", [0, 1, 341, 511])
def test_exact_pattern_rank_and_syndrome_block_mass(radius, target):
    # Explicit F32,N9,K1 control, NOT the canonical N=n^2 native experiment.
    left, right, q, n = 4, 5, 32, 9
    a, b = _pattern_counts(5, 2, left), _pattern_counts(5, 2, right)
    assert len(a) == q*(1 << left) and min(a.values()) > 0
    assert len(b) == q*(1 << right) and min(b.values()) > 0
    kernel = _kernel_matrix(left, right, radius, target)
    _, rank = fmpq_mat(kernel).rref()
    assert rank == n-radius+1
    # Positive diagonal row/column scaling preserves each exact block rank.
    exact_rank = q*rank
    assert exact_rank == q*(n-radius+1)
    expected_left = Q(q**(left-1), 1 << left)
    expected_right = Q(q**(right-1), 1 << right)
    eta_left = max(abs(Q(c)/expected_left-1) for c in a.values())
    eta_right = max(abs(Q(c)/expected_right-1) for c in b.values())
    masses = [sum(a[(y, i)]*b[(y, j)]*kernel[i][j]**2
                  for i in range(1 << left) for j in range(1 << right))
              for y in range(q)]
    kernel_norm = sum(v*v for row in kernel for v in row)
    assert kernel_norm == (1 << n)*sum(comb(n, j) for j in range(radius+1))
    upper = expected_left*expected_right*(1+eta_left)*(1+eta_right)*kernel_norm
    lower_total = q*expected_left*expected_right*(1-eta_left)*(1-eta_right)*kernel_norm
    assert min(masses) > 0 and max(masses) <= upper
    assert sum(masses) >= lower_total
    assert Q(max(masses), sum(masses)) <= upper/lower_total


def test_missing_pattern_sectors_prevent_naive_rank_formula():
    # A linear predicate has empty syndrome-pattern classes; positivity matters.
    counts = _pattern_counts(3, 2, 4)
    assert len(counts) < 8*16


@pytest.mark.parametrize("bits", [17, 31, 61])
def test_native_rank_is_analytic_exponential_not_a_sampling_hardness_claim(bits):
    result = structure.coordinate_schmidt_certificate(bits)
    k, n = bits*bits//8, bits*bits
    assert result["syndrome_sector_count_log2"] == bits*k
    assert result["radius_filtered_rank"] == {
        "power_of_two": bits*k, "multiplier": n-3*n//5+1,
    }
    assert result["required_rank_power2_lower"] == bits*k-1
    for key in ("covers_arbitrary_qubit_interleavings", "sampling_hardness_claimed",
                "global_sampler_implemented", "native_state_materialized"):
        assert result[key] is False


@pytest.mark.parametrize("change", [dict(bits=True), dict(length=1), dict(checks=3),
                                  dict(beta=0.5), dict(fourth=Q(0)),
                                  dict(beta=Q(1, 10)), dict(fourth=Q(1, 100))])
def test_moment_input_guards(change):
    args = dict(bits=3, length=3, checks=1, beta=Q(1), fourth=Q(1))
    with pytest.raises(ValueError):
        structure.mds_moment_bounds(**(args | change))


@pytest.mark.parametrize("error", [-1, 0.1, Q(1), True])
def test_schmidt_distance_guard(error):
    with pytest.raises(ValueError):
        structure.coordinate_schmidt_certificate(17, error)


@pytest.mark.parametrize("bits", [17, 19, 31])
def test_native_three_quarter_prefix_is_extendible_not_constructively_solved(bits):
    checks = bits*bits//8
    result = structure.canonical_moments(bits, 2*checks+1)
    assert result["uniform_error_parseval_upper"] < 1
    assert result["uniform_error_upper"] <= result["uniform_error_parseval_upper"]
    assert result["all_syndromes_nonempty_certified"]
    assert not result["completion_solver_implemented"]


@pytest.mark.parametrize("bits", [101, 127])
def test_generic_length_cap_does_not_truncate_supported_canonical_lengths(bits):
    # One-check control exercises the size guard without a large rank sweep.
    result = structure.mds_moment_bounds(bits, bits*bits, 1, Q(1), Q(1))
    assert result["length"] == bits*bits
    assert result["uniform_error_upper"] == 1


def test_built_report_preserves_old_keys_and_binds_importance_certificate():
    root = Path(__file__).resolve().parents[1]
    previous = json.loads((root/"research/classical_baselines/mersenne_global_structure.json").read_text())
    report = structure.build_global_structure_report()
    assert previous.keys() <= report.keys()
    for key, value in previous.items():
        if key not in ("source_sha256", "single_term_importance_bounds"):
            assert report[key] == value
    assert json.loads(json.dumps(report)) == report
    rows = report["single_term_importance_bounds"]
    assert [(row["bits"], row["remaining"]) for row in rows] == [(17, 45), (31, 136), (61, 496)]
    for row in rows:
        exact = structure.single_term_importance_certificate(row["bits"], row["remaining"])
        for key in ("B_lower", "L_lower", "second_moment_lower", "relative_variance_lower"):
            exponent = row[key.replace("_lower", "_power2_lower")]
            power = Q(1 << exponent) if exponent >= 0 else Q(1, 1 << -exponent)
            assert power <= exact[key] < 2*power
        assert row["a"] == [exact["a"].numerator, exact["a"].denominator]
        assert row["relative_variance_g_interval"] == [[1, 2], [3, 2]]
        assert row["relative_variance_requires_g_interval"]
        assert row["all_syndromes_in_g_interval_certified"] is False
        assert row["all_estimator_hardness_claimed"] is False
        assert row["native_solver_implemented"] is False
    assert set(report["source_sha256"]) == {
        "theorems/mersenne_global_structure.py", "tests/test_mersenne_global_structure.py",
        "theorems/mersenne_reciprocal_access.py", "theorems/inverse_trace_gibbs_target.py",
        "research/MERSENNE_COMPLETION_MOMENTS.md", "research/MERSENNE_COORDINATE_SCHMIDT_FILTER.md",
        "research/audits/reviews/2026-10-30-mersenne-conditional-estimator.md",
    }
    for path, digest in report["source_sha256"].items():
        assert sha256((root/path).read_bytes()).hexdigest() == digest


def test_live_report_replays_and_binds_sources():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root/"research/classical_baselines/mersenne_global_structure.json").read_text())
    assert report == structure.build_global_structure_report()
