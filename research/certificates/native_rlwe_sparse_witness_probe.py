"""Sparse-witness probability controls, LOCAL DERIVATION / REVIEW PENDING.

Small exact enumerations test a scoped counting argument. They are not
security estimates or scalable witness finders. Large-row volume values
are 90-digit numerical references, not outward-rounded certificates.
"""

import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import mpmath as mp


def mul2(a, b, q):
    return ((a[0] * b[0] - a[1] * b[1]) % q,
            (a[0] * b[1] + a[1] * b[0]) % q)


def inv2(a, q):
    determinant = (a[0]**2 + a[1]**2) % q
    if not determinant:
        return None
    inverse = pow(determinant, -1, q)
    return (a[0] * inverse % q, -a[1] * inverse % q)


def adjoint2(a, q):
    return (a[0] % q, -a[1] % q)


counts = Counter()
small_rows = []
for q in (3, 5, 7, 11):
    values = list(itertools.product(range(q), repeat=2))
    units = [a for a in values if inv2(a, q) is not None]
    denominator = len(units) * q**2
    for R in (1, 2):
        ball = [x for x in itertools.product(range(-R, R + 1), repeat=2)
                if sum(v*v for v in x) <= R*R]
        for k in (0, 1, 2):
            ys = [y for y in ball if sum(v != 0 for v in y) <= k]
            pairs = [(x, y) for y in ys for x in ball
                     if sum(v*v for v in x + y) <= R*R]
            hits = 0
            for a in units:
                aa = adjoint2(a, q)
                for b in values:
                    bb = adjoint2(b, q)
                    for x, y in pairs:
                        p, z = mul2(aa, x, q), mul2(bb, y, q)
                        if (p[1] + z[1]) % q == 0 and (p[0] + z[0]) % q:
                            hits += 1
                            break
                    counts['exact_native_label_pairs'] += 1
            actual = Fraction(hits, denominator)
            bound = Fraction((q - 1) * len(ys) * len(ball), len(units))
            assert actual <= min(Fraction(1), bound)
            counts['exact_event_bounds'] += 1
            small_rows.append(dict(q=q, R=R, k=k, label_pairs=denominator,
                                   actual_probability=str(actual), union_bound=str(bound),
                                   nonvacuous=bound < 1))
    # Fixed (y,t) density: no independent-matrix-entries assumption.
    for y in ((0, 0), (1, 0), (1, 1), (2, 1)):
        for t in (1, 2):
            histogram = Counter()
            for v in units:
                for T in values:
                    ty = mul2(T, y, q)
                    x = ((t*v[0]-ty[0]) % q, (t*v[1]-ty[1]) % q)
                    histogram[x] += 1
            assert max(histogram.values()) <= q**2
            counts['exact_fixed_pair_density_bounds'] += 1

    if q == 5:
        histogram = Counter(mul2(v, (2, 1), q) for v in units)
        assert max(histogram.values()) > 1
        counts['nonunit_h_breaks_unit_density_premise'] += 1

    if q == 11:
        assert Fraction((q - 1) * 5, len(units)) < 1
        for b in values:
            assert mul2((1, 0), (1, 0), q) == (1, 0)
            counts['biased_first_label_breaks_native_premise'] += 1

mp.mp.dps = 90
artifact = json.loads(Path(__file__).with_name('native_rlwe_single_witness_d12_arithmetic.json').read_text())
large_rows = []
for row in artifact['parameter_rows']:
    d, q, R = row['d'], int(row['q']), int(row['output_norm_bound'])
    assert d & (d-1) == 0 and row['residue_degree'] == d//2
    assert q % 8 == 3
    assert pow(q, d//2, 2*d) == 1 and pow(q, d//4, 2*d) != 1
    pU = (1 - mp.mpf(q)**(-d//2))**2
    logq = mp.log(q)

    def log_ball(n):
        if not n:
            return mp.mpf(0)
        return (n/2 * mp.log(mp.pi) - mp.loggamma(mp.mpf(n)/2+1)
                + n * mp.log(mp.mpf(R) + mp.sqrt(n)/2))

    logB = log_ball(d)
    logS = mp.mpf(0)
    all_bounds = []
    cube_sum = 0
    cube_threshold = -1
    cube_threshold_numerator = None
    unit_count_exact = (q**(d//2)-1)**2
    for k in range(d + 1):
        if k:
            term = mp.log(math.comb(d, k)) + log_ball(k)
            maximum = max(logS, term)
            logS = maximum + mp.log(mp.exp(logS - maximum) + mp.exp(term - maximum))
        logbound = mp.log(q-1) + logS + logB - mp.log(pU) - d*logq
        all_bounds.append(logbound / mp.log(10))
        cube_sum += math.comb(d, k) * (2*R)**k
        numerator = (q-1) * cube_sum * (2*R+1)**d
        if numerator * 10**8 <= unit_count_exact:
            cube_threshold = k
            cube_threshold_numerator = numerator
    safe = max(k for k, value in enumerate(all_bounds) if value <= -6)
    h = pow(2, d, q) + 1
    assert h % q != 0
    large_rows.append(dict(d=d, radius=str(R), q=str(q),
                           h_2_plus_X_is_unit_exact=True,
                           exact_cube_support_threshold_for_1e_minus_8=cube_threshold,
                           exact_cube_inequality_checked=cube_threshold_numerator * 10**8 <= unit_count_exact,
                           max_support_with_log10_bound_le_minus_6=safe,
                           log10_bound_at_threshold=mp.nstr(all_bounds[safe], 22),
                           log10_bound_at_threshold_plus_one=mp.nstr(all_bounds[safe+1], 22),
                           log10_bounds={str(k): mp.nstr(all_bounds[k], 22)
                                        for k in (0, 1, d//2, safe)}))

print(json.dumps(dict(scope='local_counting_probe_not_security_estimate',
                     counts=counts, small_rows=small_rows,
                     large_rows=large_rows), indent=2))
