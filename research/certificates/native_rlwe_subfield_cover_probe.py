"""Exact restricted-coordinate affine-cover and source-density controls.

LOCAL DERIVATION / REVIEW PENDING. Classical compressed lattices and
output-class bounds; no quantum solver or growing-degree attack claim.
Small examples test identities, not newly generated research problems.
"""

import argparse
import hashlib
import itertools
import json
import math
import random
from collections import Counter
from pathlib import Path

import sympy as sp


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()
directory = Path(__file__).parent
counts = Counter()
rng = random.Random(290956)


def multiplication(a):
    d = len(a)
    return sp.Matrix([[a[(i-j) % d]*(1 if i >= j else -1)
                       for j in range(d)] for i in range(d)])


def gs(B):
    out = []
    for j in range(B.cols):
        v = B.col(j)
        residual = v.copy()
        for old in out:
            residual -= old*(v.dot(old)/old.dot(old))
        assert residual.dot(residual) > 0
        out.append(residual)
    return out


def babai(B, orthogonal, target):
    residual = target.copy()
    for j in range(B.cols-1, -1, -1):
        coefficient = sp.floor(residual.dot(orthogonal[j])/
                               orthogonal[j].dot(orthogonal[j])+sp.Rational(1, 2))
        residual -= coefficient*B.col(j)
    return residual


def ball_bound(n, R):
    # Unit cubes around integer points fit in the inflated Euclidean ball.
    # V_n <= (sqrt(2*pi*e/n))^n, and sqrt(2*pi*e)<5.
    s = math.isqrt(n)
    return (5*R+3*s)**n, s**n


for d in (2, 4, 8):
    for q in (17, 257):
        for depth in range(d.bit_length()):
            h = d >> depth
            r = d//h
            E = sp.eye(d)[:, list(range(0, d, r))]
            assert E.T*E == sp.eye(h)
            # Keep a nonunit ratio too: no inverse of M is required.
            for kind in ('uniform_control', 'zero_ratio_countercontrol'):
                mu = [rng.randrange(q) for _ in range(d)] if kind == 'uniform_control' else [0]*d
                M = multiplication(mu)
                public = sp.eye(d).row_join(M*E)
                B = (q*sp.eye(d)).row_join(-M*E).col_join(sp.zeros(h, d).row_join(sp.eye(h)))
                embed = sp.diag(sp.eye(d), E)
                assert embed.T*embed == sp.eye(d+h)
                assert public*B % q == sp.zeros(d, d+h)
                assert abs(int(B.det())) == q**d
                assert (embed*B).rows == 2*d and (embed*B).cols == d+h
                assert (embed*B).rank() == d+h
                counts['compressed_basis_and_metric_controls'] += 1
                reduced = B.T.lll().T
                assert public*reduced % q == sp.zeros(d, d+h)
                assert abs(int(reduced.det())) == q**d
                orthogonal = gs(reduced)
                lengths = [v.dot(v) for v in orthogonal]
                profile = sum(lengths)
                assert math.prod(lengths) == q**(2*d)
                assert profile**(d+h) >= (d+h)**(d+h)*q**(2*d)
                counts['exact_profile_volume_controls'] += 1
                for _ in range(3):
                    target = sp.Matrix([rng.randrange(q) for _ in range(d)])
                    section = target.col_join(sp.zeros(h, 1))
                    c = babai(reduced, orthogonal, section)
                    expanded = embed*c
                    assert public*c % q == target
                    assert sp.eye(d).row_join(M)*expanded % q == target
                    assert expanded.dot(expanded) == c.dot(c)
                    assert 4*c.dot(c) <= profile
                    counts['restricted_affine_cover_controls'] += 1

for n in range(2, 7):
    for R in (1, 2, 3):
        actual = sum(sum(v*v for v in point) <= R*R
                     for point in itertools.product(range(-R, R+1), repeat=n))
        numerator, denominator = ball_bound(n, R)
        assert actual*denominator <= numerator
        counts['integer_ball_bound_controls'] += 1

# Exact joint-density argument in the Gaussian integer ring at q=3.
# v=a1^-T e0 is uniform on units and independent of M; invertible and
# noninvertible second blocks must both obey the same density bound.
d, q = 2, 3
residues = list(itertools.product(range(q), repeat=d))
units = [v for v in residues if int(multiplication(v).det()) % q]
assert len(units) == q*q-1
for R in (1, 2):
    allowed = [c for c in itertools.product(range(-R, R+1), repeat=3)
               if sum(v*v for v in c) <= R*R]
    good_labels = set()
    for c in allowed:
        x, y = sp.Matrix(c[:d]), sp.Matrix([c[d], 0])
        for t in range(1, q):
            hits = 0
            for mu in residues:
                required_v = tuple(int(z)*pow(t, -1, q) % q
                                   for z in x+multiplication(mu)*y)
                if required_v in units:
                    hits += 1
                    good_labels.add((mu, required_v))
            assert hits <= q**d
            counts['fixed_vector_joint_density_controls'] += 1
    population = len(residues)*len(units)
    assert len(good_labels)*len(units) <= (q-1)*len(allowed)*population
    counts['adaptive_restricted_output_union_controls'] += 1

# Proper zero divisors (not just zero) in the high-CRT ring are legal in
# the fixed-vector density argument, including restriction of the first block.
d, q = 4, 3
residues = list(itertools.product(range(q), repeat=d))
units = {v for v in residues if int(multiplication(v).det()) % q}
assert len(units) == (q**(d//2)-1)**2
x = sp.Matrix([1, 0, 0, 0])
y = sp.Matrix([-1, 1, 1, 0])
assert any(y) and int(multiplication(y).det()) % q == 0
for t in range(1, q):
    hits = []
    for mu in residues:
        required_v = tuple(int(z)*pow(t, -1, q) % q for z in x+multiplication(mu)*y)
        if required_v in units:
            hits.append(mu)
    assert len(hits) <= q**d
    assert (0,)*d in hits
    counts['proper_zero_divisor_joint_density_controls'] += 1

source_name = 'native_rlwe_single_witness_d12_arithmetic.json'
source = json.loads((directory/source_name).read_text())
rows = []
for parameter in source['parameter_rows']:
    d, q = parameter['d'], int(parameter['q'])
    assert d & (d-1) == 0 and q % 8 == 3
    for lane in parameter['lanes']:
        Rs = lane['prior_radius']
        noise = int(lane['total_training_error_norm_bound'])
        t = q//(2*Rs+1)
        R = (t+2*noise-1)//(2*noise)
        h = d
        while h:
            n = d+h
            necessary_left = (n*noise*noise)**n*q**(2*d)
            necessary_right = t**(2*n)
            headroom = necessary_left < necessary_right
            ball_num, ball_den = ball_bound(n, R)
            unit_population = (q**(d//2)-1)**2
            probability_num = (q-1)*ball_num
            probability_den = unit_population*ball_den
            # Both blocks and every monomial shift of the subfield support
            # are allowed; joint density avoids discarding a2 nonunits.
            support_catalog = 2*(d//h)
            scoped_negative = support_catalog*probability_num*10**8 <= probability_den
            rows.append(dict(d=d, lane=lane['lane'], q=str(q),
                             subfield_degree=h, compressed_dimension=n,
                             restriction_stride=d//h,
                             prior_radius=Rs, noise_norm=str(noise), label=str(t),
                             rounded_affine_radius=str(R),
                             geometric_headroom_necessary_only=headroom,
                             integer_ball_sqrt_floor=math.isqrt(n),
                             density_upper_formula='(q-1)*(5*R+3*s)^n/[s^n*(q^(d/2)-1)^2]',
                             density_log2_strict_upper=probability_num.bit_length()-probability_den.bit_length()+1,
                             density_bound_vacuous=probability_num >= probability_den,
                             support_catalog_size=support_catalog,
                             support_catalog_density_bound_vacuous=support_catalog*probability_num >= probability_den,
                             either_block_all_monomial_shifts_at_most_1e_minus8_exact=scoped_negative,
                             prime_certificates_replayed_this_run=False))
            counts['exact_reference_restriction_rows'] += 1
            h //= 2

assert all(not row['geometric_headroom_necessary_only']
           for row in rows if row['subfield_degree'] <= row['d']//4)
assert all(row['either_block_all_monomial_shifts_at_most_1e_minus8_exact']
           for row in rows if row['subfield_degree'] <= row['d']//4)
output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING',
              scope='restricted_coefficient_output_class_and_compressed_classical_cover',
              quantum_algorithm=False, asymptotic_attack_proved=False,
              original_prior_noise_laws_sampled=False,
              actual_large_degree_restricted_lll_run=False,
              conditional_first_label_law='uniform_conditioned_on_unit',
              second_label_law='independently_uniform_whole_ring',
              nonunit_second_labels_included=True,
              fixed_original_coefficient_metric_required=True,
              headroom_gate_is_necessary_not_sufficient=True,
              arbitrary_subfield_norm_descent_excluded_from_claim=True,
              counts=dict(counts), rows=rows,
              source=dict(path=source_name,
                          sha256=hashlib.sha256((directory/source_name).read_bytes()).hexdigest()))
if args.save:
    (directory/'native_rlwe_subfield_cover_bounds.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(dict(status=output['status'], counts=dict(counts),
                     reference_half_degree=[row for row in rows if row['subfield_degree'] == row['d']//2],
                     all_quarter_or_deeper_rows_excluded=True), indent=2))
