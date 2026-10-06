"""Exact controls for prelabel unit/PIP output-class counting.

LOCAL DERIVATION / REVIEW PENDING. Small algebra controls and exact source
parameter inequalities, NOT an average-case quantum hardness theorem.
The general bound fixes a native-coordinate pair independently of the labels;
the high-CRT bound fixes only the nonzero denominator up to units.
"""

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import sympy as sp


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()
directory = Path(__file__).parent
counts = Counter()


def multiply(a, b):
    d = len(a)
    out = [0]*d
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            k = i+j
            out[k % d] += x*y*(1 if k < d else -1)
    return tuple(out)


def matrix(a):
    d = len(a)
    return sp.Matrix([[a[(i-j) % d]*(1 if i >= j else -1) for j in range(d)]
                       for i in range(d)])


def ball_cube_count(d, radius):
    return (2*radius+1)**d


def unit_upper(d, radius):
    assert d >= 2 and d & (d-1) == 0 and radius >= 1
    L = (d*radius).bit_length()
    return 2*d*(d*L+1)**(d//2), L


# Integer injectivity survives even when the modular map is constant.
for d, q in ((2, 3), (2, 5), (4, 3), (4, 5)):
    for f in ([1]+[0]*(d-1), [q]+[0]*(d-1), [1, 1]+[0]*(d-2)):
        assert matrix(f).det() != 0
        k = tuple([1]+[0]*(d-1))
        images = set()
        modular = set()
        for m in itertools.product(range(q), repeat=d):
            product = multiply(m, f)
            g = tuple(product[i]+q*k[i] for i in range(d))
            assert g not in images
            images.add(g)
            modular.add(tuple(value % q for value in g))
        assert len(images) == q**d
        if f[0] == q:
            assert len(modular) == 1
            counts['nonunit_modular_collapse_controls'] += 1
        for R in (1, 2, 3):
            successes = sum(sum(value*value for value in g) <= R*R for g in images)
            assert successes <= ball_cube_count(d, R)
            counts['fixed_pair_integer_small_ball_controls'] += 1
        counts['integer_injective_maps'] += 1

        # Even adaptive lift selection cannot make one integer image serve
        # two different labels when the native coordinate pair stays fixed.
        lifted_images = {}
        for m in itertools.product(range(q), repeat=d):
            for correction in itertools.product((-1, 0), repeat=d):
                lift = tuple(m[i]+q*correction[i] for i in range(d))
                product = multiply(lift, f)
                g = tuple(product[i]+q*k[i] for i in range(d))
                assert g not in lifted_images or lifted_images[g] == m
                lifted_images[g] = m
        for R in (1, 2, 3):
            good_labels = {m for g, m in lifted_images.items()
                           if sum(value*value for value in g) <= R*R}
            assert len(good_labels) <= ball_cube_count(d, R)
            counts['adaptive_lift_small_ball_controls'] += 1
        counts['adaptive_lift_integer_image_controls'] += 1

# High-CRT ideal images permit an arbitrary adaptive numerator correction.
for q in (3, 11):
    d = 4
    c = next(v for v in range(q) if (v*v+2) % q == 0)
    f = (-1, c, 1, 0)
    image_counts = Counter(tuple(value % q for value in multiply(m, f))
                           for m in itertools.product(range(q), repeat=d))
    assert len(image_counts) == q**(d//2)
    assert set(image_counts.values()) == {q**(d//2)}
    counts['high_crt_uniform_image_controls'] += 1
    opposite_ideal = {tuple(value[i]*(1 if i % 2 == 0 else -1) % q
                            for i in range(d)) for value in image_counts}
    assert len(opposite_ideal) == q**(d//2)
    assert set(image_counts) & opposite_ideal == {(0,)*d}
    unit_residues = set(itertools.product(range(q), repeat=d))-set(image_counts)-opposite_ideal
    assert len(unit_residues) == (q**(d//2)-1)**2
    counts['zero_denominator_unit_population_controls'] += 1
    for R in (1, 2, 3):
        points = []
        for g in itertools.product(range(-R, R+1), repeat=d):
            energy = sum(value*value for value in g)
            if energy > R*R or tuple(value % q for value in g) not in image_counts:
                continue
            points.append(g)
            if energy:
                assert energy >= q
                assert int(matrix(g).det()) % (q**(d//2)) == 0
                counts['high_crt_ideal_minimum_norm_controls'] += 1
        s = math.isqrt(q)
        assert len(points)*s**d <= (s+2*R)**d
        represented = {tuple(value % q for value in g) for g in points}
        actual_good_labels = sum(image_counts[value] for value in represented)
        assert actual_good_labels <= len(points)*q**(d//2)
        counts['adaptive_numerator_ideal_packing_controls'] += 1
        target = (1, 0, 0, 0)
        coset = {tuple((target[i]-value[i]) % q for i in range(d)) for value in image_counts}
        shifted = [g for g in itertools.product(range(-R, R+1), repeat=d)
                   if sum(v*v for v in g) <= R*R and tuple(v % q for v in g) in coset]
        assert len(shifted)*s**d <= (s+2*R)**d
        for a, b in itertools.combinations(shifted, 2):
            difference = tuple(a[i]-b[i] for i in range(d))
            assert sum(v*v for v in difference) >= q
            assert int(matrix(difference).det()) % q**(d//2) == 0
        counts['affine_coset_spacing_and_packing_controls'] += 1
        short_unit_residues = {tuple(v % q for v in g)
                               for g in itertools.product(range(-R, R+1), repeat=d)
                               if sum(v*v for v in g) <= R*R
                               and tuple(v % q for v in g) in unit_residues}
        # v=a1^-T e0 is uniform on units; charge every adaptive scalar t.
        good_inverse_labels = {tuple(value*pow(t, -1, q) % q for value in g)
                               for g in short_unit_residues for t in range(1, q)}
        assert good_inverse_labels <= unit_residues
        assert len(good_inverse_labels) <= (q-1)*ball_cube_count(d, R)
        counts['zero_denominator_adaptive_target_controls'] += 1

# An easy first label has a short zero-denominator witness. The source
# probability bound is not a pointwise impossibility claim.
assert multiply((1, 0, 0, 0), (1, 0, 0, 0)) == (1, 0, 0, 0)
counts['easy_first_label_countercontrol_retained'] += 1

# Splitting into low-degree factors defeats the sqrt(q) ideal minimum.
bad = (0, 0, 0, 1, 0, 1, 1, 1)
assert int(matrix(bad).det()) % 17 == 0 and sum(v*v for v in bad) < 17
counts['low_residue_degree_counterexample_retained'] += 1

# Generate a bounded catalogue only to check the elementary unit packing.
d = 4
eta = matrix([1, 1, 1, 0])
assert eta.det() == 1
units = {}
for exponent in range(-3, 4):
    base = eta**exponent
    for j in range(d):
        root = [0]*d
        root[j] = 1
        for sign in (-1, 1):
            C = sign*matrix(root)*base
            assert C.det() == 1 and all(value.q == 1 for value in C)
            unit = tuple(int(value) for value in C.col(0))
            inverse = tuple(int(value) for value in C.inv().col(0))
            assert multiply(unit, inverse) == (1, 0, 0, 0)
            units[unit] = inverse
for u, v in itertools.combinations(units, 2):
    ratio = multiply(u, units[v])
    energy = sum(value*value for value in ratio)
    assert energy >= 1
    if energy == 1:
        assert sum(value != 0 for value in ratio) == 1
        counts['root_of_unity_ratio_controls'] += 1
    else:
        assert energy >= 2
        assert (matrix(ratio).T*matrix(ratio)).trace() == d*energy
        counts['nonroot_unit_parseval_separation_controls'] += 1
for f in ((1, 0, 0, 0), (2, 1, 0, 0), (1, 1, 1, 0)):
    assert matrix(f).det() != 0
    for R in (1, 2, 4, 16):
        selected = [multiply(u, f) for u in units if sum(x*x for x in multiply(u, f)) <= R*R]
        cap, _ = unit_upper(d, R)
        assert len(selected) <= cap
        for vector in selected:
            assert abs(int(matrix(vector).det())) == abs(int(matrix(f).det()))
        counts['finite_unit_catalogue_count_controls'] += 1

# At d=2 the log-norm lower endpoint can be zero, not strictly positive.
gaussian_roots = ((1, 0), (-1, 0), (0, 1), (0, -1))
assert all(sum(v*v for v in unit) == 1 for unit in gaussian_roots)
assert len(gaussian_roots) <= unit_upper(2, 1)[0]
counts['degree_two_log_endpoint_control'] += 1

source = json.loads((directory/'native_rlwe_single_witness_d12_arithmetic.json').read_text())
rows = []
for parameter in source['parameter_rows']:
    d, q = parameter['d'], int(parameter['q'])
    for lane in parameter['lanes']:
        Rs, E = lane['prior_radius'], int(lane['total_training_error_norm_bound'])
        t = q//(2*Rs+1)
        R = (t+E-1)//E
        unit_count, L = unit_upper(d, R)
        numerator = unit_count*ball_cube_count(d, R)
        denominator = q**d
        binary_upper = numerator.bit_length()-denominator.bit_length()+1
        assert d >= 4 and q % 8 == 3 and R < q
        s = math.isqrt(q)
        adaptive_numerator = unit_count*(s+2*R)**d
        adaptive_denominator = s**d*q**(d//2)
        adaptive_binary_upper = adaptive_numerator.bit_length()-adaptive_denominator.bit_length()+1
        assert numerator*10**8 <= denominator
        assert numerator*(1 << d)*10**8 <= denominator
        assert numerator*d**10*10**8 <= denominator
        assert adaptive_numerator*(1 << d)*10**8 <= adaptive_denominator
        assert adaptive_numerator*d**10*10**8 <= adaptive_denominator
        assert adaptive_numerator*q*(1 << d)*10**8 <= adaptive_denominator
        zero_numerator = (q-1)*ball_cube_count(d, R)
        zero_denominator = (q**(d//2)-1)**2
        assert zero_numerator*10**8 <= zero_denominator
        combined_numerator = (adaptive_numerator*q*(1 << d)*zero_denominator
                              +zero_numerator*adaptive_denominator)
        combined_denominator = adaptive_denominator*zero_denominator
        assert combined_numerator*10**8 <= combined_denominator
        rows.append(dict(d=d, lane=lane['lane'], q=str(q),
                         prior_radius=Rs, noise_norm=str(E), label=str(t),
                         rounded_radius=str(R), unit_log_box_integer_L=L,
                         unit_count_factor='2*d*(d*L+1)^(d/2)',
                         ball_count_factor='(2*R+1)^d', label_count_factor='q^d',
                         probability_log2_strict_upper=binary_upper,
                         high_crt_adaptive_numerator_log2_strict_upper=adaptive_binary_upper,
                         high_crt_catalog_2_to_d_log2_strict_upper=adaptive_binary_upper+d,
                         high_crt_affine_q_targets_and_2_to_d_catalog_log2_strict_upper=adaptive_binary_upper+d+q.bit_length(),
                         high_crt_affine_q_targets_and_2_to_d_catalog_at_most_1e_minus8_exact=True,
                         zero_denominator_bound_factor='(q-1)*(2*R+1)^d/(q^(d/2)-1)^2',
                         zero_denominator_log2_strict_upper=zero_numerator.bit_length()-zero_denominator.bit_length()+1,
                         combined_affine_including_zero_denominator_at_most_1e_minus8_exact=True,
                         adaptive_bound_factor='2*d*(d*L+1)^(d/2)*(s+2*R)^d/(s^d*q^(d/2))',
                         s_floor_sqrt_q=str(s),
                         prime_premise='existing_saved_recursive_prime_certificates',
                         prime_certificates_replayed_this_run=False,
                         prelabel_catalog_2_to_d_log2_strict_upper=binary_upper+d,
                         probability_at_most_1e_minus8_exact=True,
                         catalog_2_to_d_at_most_1e_minus8_exact=True,
                         catalog_d_to10_at_most_1e_minus8_exact=True))
        counts['exact_reference_lane_bounds'] += 1

# Actual label-dependent LLL escapes the independent-pair hypothesis.
saved = json.loads((directory/'native_rlwe_babai_profile_d64.json').read_text())
d, q = saved['d'], int(saved['q'])
row = [int(value) for value in saved['reduced_row_basis'][0]]
g, f = row[:d], [-value for value in row[d:]]
original = [int(value) for value in saved['native_ratio']]
# Adjoint coefficient involution converts C_m^T to ordinary multiplication.
mu = [original[0]]+[-original[d-j] for j in range(1, d)]
product = multiply(mu, f)
assert all((g[i]-product[i]) % q == 0 for i in range(d))
assert any(f) and any(g[i]-product[i] for i in range(d))
for lane in saved['lanes']:
    E, t = int(lane['error_norm']), int(lane['chosen_label'])
    assert E*E*sum(value*value for value in row) < t*t
counts['adaptive_actual_lll_escape_controls'] += 1

output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING',
              scope='prelabel_pairs_any_q_and_prelabel_denominator_high_crt',
              quantum_algorithm=False, general_hardness_bound=False,
              prior_noise_laws_sampled=False,
              counts=dict(counts), rows=rows,
              uniform_bound_formula='min(1,2*d*(d*L+1)^(d/2)*(2*R+1)^d/q^d)',
              excludes_label_adaptive_cross_block_pair_generation=False)
output['high_crt_adaptive_numerator_included'] = True
output['high_crt_arbitrary_residue_preserving_lifts_included'] = True
output['high_crt_prelabel_affine_target_catalog_included'] = True
output['high_crt_ratio_bound_zero_denominator_excluded'] = True
output['combined_affine_zero_denominator_accounted_separately'] = True
output['zero_denominator_first_label_law'] = 'uniform_conditioned_on_unit'
output['general_pair_bound_fixed_lift_required'] = False
output['general_adaptive_residue_preserving_lifts_included'] = True
output['general_fixed_native_coordinate_pair_required'] = True
output['inputs'] = [dict(path=name, sha256=hashlib.sha256((directory/name).read_bytes()).hexdigest())
                    for name in ('native_rlwe_single_witness_d12_arithmetic.json',
                                 'native_rlwe_babai_profile_d64.json')]
if args.save:
    (directory/'native_rlwe_prelabel_unit_bounds.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(output, indent=2))
