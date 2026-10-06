"""Exact norm-lift and conditional norm-fibre falsifier controls.

LOCAL DERIVATION / REVIEW PENDING. Native uniform-label output classes,
not a runtime lower bound, asymptotic attack or quantum algorithm.
"""

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', action='store_true')
args = parser.parse_args()
directory = Path(__file__).parent
counts = Counter()


def multiply(a, b, q=None):
    d = len(a)
    out = [0]*d
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            k = i+j
            out[k % d] += x*y*(1 if k < d else -1)
    return tuple(value % q if q else value for value in out)


def tau(a, q=None):
    out = tuple(value*(1 if i % 2 == 0 else -1) for i, value in enumerate(a))
    return tuple(value % q for value in out) if q else out


def norm_down(a, q=None):
    product = multiply(a, tau(a, q), q)
    assert not any(product[1::2])
    return product[::2]


def absolute_norm(a):
    while len(a) > 1:
        a = norm_down(a)
    return abs(a[0])


def native_unit(a, q):
    # At q=3 mod 8 the bottom degree-two ring is F_(q^2); upper
    # relative norms are products of nonzero field norms exactly for units.
    while len(a) > 2:
        a = norm_down(a, q)
    return any(a)


def embed(a):
    out = [0]*(2*len(a))
    out[::2] = a
    return tuple(out)


def centered(a, q):
    return tuple((value+q//2) % q-q//2 for value in a)


def matrix(a):
    d = len(a)
    return sp.Matrix([[a[(i-j) % d]*(1 if i >= j else -1)
                       for j in range(d)] for i in range(d)])


for d, q in ((4, 3), (4, 11), (8, 3)):
    h = d//2
    all_m = list(itertools.product(range(q), repeat=d))
    fibres = defaultdict(list)
    raw_small = Counter()
    radii = [R for R in (1, 2, 3) if 2*R < q]
    for mu in all_m:
        lifted = centered(mu, q)
        norm = absolute_norm(lifted)
        for R in radii:
            raw_small[R] += norm <= R**d
        eta = norm_down(mu, q)
        if native_unit(mu, q):
            assert native_unit(eta, q)
            fibres[eta].append(mu)
        counts['exact_modular_norm_controls'] += 1
    expected = q**h-1 if d == 4 else (q**(h//2)+1)**2
    assert sum(map(len, fibres.values())) == (q**h-1)**2
    assert {len(fibre) for fibre in fibres.values()} == {expected}
    counts['uniform_native_unit_norm_maps'] += 1
    for R in radii:
        assert raw_small[R]*q*q <= h*(2*R+1)**2*q**d
        counts['canonical_raw_norm_event_counts'] += 1

    small_ring = list(itertools.product(range(q), repeat=h))
    square_counts = Counter(multiply(b, b, q) for b in small_ring)
    root_cap = 2 if d == 4 else 4
    assert max(square_counts.values()) <= root_cap
    counts['exact_square_root_multiplicity_controls'] += 1
    proper_b = next((b for b in small_ring if any(b) and not native_unit(b, q)), None)
    assert (proper_b is None) == (d == 4)
    for eta, fibre in fibres.items():
        multipliers = [tuple([1]+[0]*(h-1)), eta]
        if proper_b is not None:
            multipliers.append(proper_b)
        for b in multipliers:
            image = Counter(multiply(embed(b), tau(mu, q), q) for mu in fibre)
            unit_b = native_unit(b, q)
            orbit = expected if unit_b else q**(h//2)+1
            assert len(image) == orbit
            assert set(image.values()) == {expected//orbit}
            target_norm = multiply(multiply(b, b, q), eta, q)
            target_relation = embed(multiply(eta, b, q))
            for f in image:
                assert norm_down(f, q) == target_norm
            for mu in fibre:
                f = multiply(embed(b), tau(mu, q), q)
                assert multiply(mu, f, q) == target_relation
            counts['norm_only_multiplier_uniform_image_controls'] += 1
            for R in radii:
                good = [f for f in image if sum(v*v for v in centered(f, q)) <= R*R]
                if unit_b:
                    assert len(good) <= root_cap*(2*R+1)**h
                    counts['unit_multiplier_short_fibre_controls'] += 1
                else:
                    s = math.isqrt(q)
                    assert len(good)*s**h <= root_cap*(s+2*R)**h
                    for f in good:
                        f1 = centered(f, q)[1::2]
                        if any(f1):
                            assert sum(v*v for v in f1) >= q
                    counts['nonunit_multiplier_ideal_packing_controls'] += 1
        zero = (0,)*h
        assert {multiply(embed(zero), tau(mu, q), q) for mu in fibre} == {(0,)*d}
        counts['zero_multiplier_trivial_relation_controls'] += 1

    for mu in all_m[::max(1, len(all_m)//8)]:
        m = centered(mu, q)
        assert absolute_norm(m) == abs(int(matrix(m).det()))
        for b in (tuple([1]+[0]*(h-1)), tuple([1, 1]+[0]*(h-2))):
            f = multiply(embed(b), tau(m))
            assert absolute_norm(f) == absolute_norm(b)**2*absolute_norm(m)
            for j in (0, 1):
                u = tuple(int(i == j) for i in range(d))
                shortened = multiply(u, f)
                N = absolute_norm(shortened)
                assert N >= absolute_norm(m)
                assert N*N <= sum(v*v for v in shortened)**d
                counts['raw_lift_integral_norm_and_hadamard_controls'] += 1

# Units DO help some exceptional raw inputs; never promote a high-
# probability source statement to pointwise impossibility.
m = (1, 1, 1, 0)
f = tau(m)
u = tuple(int(v) for v in matrix(f).inv().col(0))
assert absolute_norm(m) == 1 and multiply(u, f) == (1, 0, 0, 0)
assert sum(v*v for v in f) > sum(v*v for v in multiply(u, f))
counts['exceptional_raw_unit_repair_countercontrol'] += 1

# Low-residue-degree base rings have many square roots; the root-cap
# constant cannot be transplanted from the native high-CRT family.
d, q = 8, 17
h = d//2
roots = [value for value in range(q) if (pow(value, h, q)+1) % q == 0]
assert len(roots) == h
evaluation = sp.Matrix([[pow(value, j, q) for j in range(h)] for value in roots])
inverse = evaluation.inv_mod(q)
square_roots_of_one = set()
for signs in itertools.product((-1, 1), repeat=h):
    b = tuple(int(value) % q for value in inverse*sp.Matrix(signs))
    assert multiply(b, b, q) == (1, 0, 0, 0)
    square_roots_of_one.add(b)
assert len(square_roots_of_one) == 16 > 4
counts['split_modulus_square_root_cap_countercontrol'] += 1

# Native content is (f,k), not the ambient (f,g). Its ideal norm is
# computable by classical HNF before asking for any PIP generator.
for d, q in ((4, 3), (4, 11), (8, 3)):
    h = d//2
    residues = [mu for mu in itertools.product(range(q), repeat=d) if native_unit(mu, q)]
    for mu in residues[::max(1, len(residues)//4)]:
        m = centered(mu, q)
        eta = centered(norm_down(mu, q), q)
        for b in (tuple([1]+[0]*(h-1)), tuple([2]+[0]*(h-1))):
            f = multiply(embed(b), tau(m))
            mf = multiply(m, f)
            for kind in ('modular_norm_relation', 'exact_integer_norm_relation'):
                g = embed(centered(multiply(eta, b, q), q)) if kind == 'modular_norm_relation' else mf
                assert all((g[i]-mf[i]) % q == 0 for i in range(d))
                k = tuple((g[i]-mf[i])//q for i in range(d))
                native_H = hermite_normal_form(matrix(f).row_join(matrix(k)))
                ambient_H = hermite_normal_form(matrix(f).row_join(matrix(g)))
                assert native_H == ambient_H
                ideal_norm = abs(int(native_H.det()))
                assert ideal_norm >= 1
                assert absolute_norm(f) % ideal_norm == 0
                assert absolute_norm(g) % ideal_norm == 0
                a = g[::2]
                assert not any(g[1::2])
                Na, Nb = absolute_norm(a), absolute_norm(b)
                C = 1
                while C**h*Nb < Na:
                    C *= 2
                assert absolute_norm(f)*C**d >= absolute_norm(m)*ideal_norm
                counts['fractional_content_norm_ratio_corollary_controls'] += 1
                if kind == 'exact_integer_norm_relation':
                    assert ideal_norm == absolute_norm(f)
                    # Reciprocal f is eligible here, but the quotient is
                    # just the native (M,-1) line, not a new generator.
                    for p in (1, 2):
                        assert p**d >= 1
                        assert absolute_norm(tuple(p*v for v in m)) == p**d*absolute_norm(g)//ideal_norm
                        assert p**d == p**d*absolute_norm(f)//ideal_norm
                        counts['eligible_fractional_scalar_norm_controls'] += 1
                counts['native_content_hnf_and_unit_mod_q_identity_controls'] += 1

d, q = 4, 17
zero = (0,)*d
one = (1, 0, 0, 0)
q_vector = (q, 0, 0, 0)
native = hermite_normal_form(matrix(zero).row_join(matrix(one)))
ambient = hermite_normal_form(matrix(zero).row_join(matrix(q_vector)))
assert abs(int(native.det())) == 1 and abs(int(ambient.det())) == q**d
assert absolute_norm(q_vector) > abs(int(native.det()))*1**d
assert absolute_norm(q_vector) <= abs(int(ambient.det()))*1**d
counts['ambient_content_gate_false_positive_retained'] += 1

# Algebraic norm gates are necessary, not sufficient even at tiny radii.
f = g = one
assert max(absolute_norm(f), absolute_norm(g)) <= 1*1**d
assert sum(v*v for v in f+g) > 1
counts['norm_gate_total_length_false_positive_retained'] += 1

# Comparable coefficient norms do not imply comparable algebraic norms.
b = (1, 0, 0, 0)
for _ in range(6):
    b = multiply(b, (1, 1, 1, 0))
energy = sum(v*v for v in b)
c = math.isqrt(energy)
c += c*c < energy
a = (c, 0, 0, 0)
assert absolute_norm(b) == 1 and absolute_norm(a) == c**4
assert energy <= c*c <= 4*energy and c > 8
counts['coefficient_balance_not_norm_ratio_countercontrol'] += 1

source_name = 'native_rlwe_single_witness_d12_arithmetic.json'
source = json.loads((directory/source_name).read_text())
rows = []
for parameter in source['parameter_rows']:
    d, q = parameter['d'], int(parameter['q'])
    h = d//2
    assert d >= 8 and q % 8 == 3
    root_cap = 4
    orbit = q**(h//2)+1
    s = math.isqrt(q)
    for lane in parameter['lanes']:
        E = int(lane['total_training_error_norm_bound'])
        t = q//(2*lane['prior_radius']+1)
        R = (t+E-1)//E
        assert 2*R < q
        raw_num, raw_den = h*(2*R+1)**2, q*q
        unit_num, unit_den = root_cap*(2*R+1)**h, orbit**2
        nonunit_num = root_cap*(s+2*R)**h
        nonunit_den = s**h*orbit
        # An arbitrary norm-conditioned catalogue may mix both types;
        # the larger per-entry bound suffices, so no extra union factor.
        if unit_num*nonunit_den >= nonunit_num*unit_den:
            num, den = unit_num, unit_den
        else:
            num, den = nonunit_num, nonunit_den
        bad_m_num = 2*q**h-1
        bad_m_den = q**(2*h)
        catalog = 1 << d
        combined_num = num*catalog*bad_m_den+bad_m_num*den
        combined_den = den*bad_m_den
        single_num = num*bad_m_den+bad_m_num*den
        single_den = den*bad_m_den
        markov_num = 100*single_num
        B = max(0, (single_den.bit_length()-markov_num.bit_length())//2)
        while markov_num*(1 << (2*B)) > single_den:
            B -= 1
        while markov_num*(1 << (2*(B+1))) <= single_den:
            B += 1
        assert B >= 3 and markov_num*(1 << (2*B)) <= single_den
        # On >=99% of source inputs, p_M<=2^(-2B). Ordinary Grover
        # success after r<=2^(B-2) is <=(1/2+2^(-B))^2<1/2.
        assert (2**(B-1)+1)**2*2 < 2**(2*B)
        assert raw_num*10**8 <= raw_den
        root_cutoff = math.isqrt(raw_den//(h*10**8))
        Cmax = (root_cutoff-1)//(2*R)
        assert Cmax >= 1
        assert h*(2*Cmax*R+1)**2*10**8 <= raw_den
        assert h*(2*(Cmax+1)*R+1)**2*10**8 > raw_den
        assert num*d**10*10**8 <= den
        assert combined_num*10**8 <= combined_den
        rows.append(dict(d=d, h=h, lane=lane['lane'], q=str(q),
                         prior_radius=lane['prior_radius'], noise_norm=str(E),
                         label=str(t), rounded_radius=str(R),
                         sqrt_q_floor=str(s),
                         raw_lift_bound_formula='h*(2*R+1)^2/q^2',
                         raw_lift_log2_strict_upper=raw_num.bit_length()-raw_den.bit_length()+1,
                         raw_lift_at_most_1e_minus8_exact=True,
                         fractional_content_norm_ratio_root_cap_for_1e_minus8=Cmax,
                         fractional_content_corollary_formula='h*(2*C*R+1)^2/q^2',
                         unit_b_bound_formula='4*(2*R+1)^h/(q^(h/2)+1)^2',
                         unit_b_log2_strict_upper=unit_num.bit_length()-unit_den.bit_length()+1,
                         nonunit_b_bound_formula='4*(s+2*R)^h/[s^h*(q^(h/2)+1)]',
                         nonunit_b_log2_strict_upper=nonunit_num.bit_length()-nonunit_den.bit_length()+1,
                         mixed_catalog_bound_log2_strict_upper=num.bit_length()-den.bit_length()+1,
                         catalog_2_to_d_with_nonunit_m_event_log2_strict_upper=combined_num.bit_length()-combined_den.bit_length()+1,
                         catalog_2_to_d_with_nonunit_m_event_at_most_1e_minus8_exact=True,
                         nonunit_m_probability_formula='(2*q^h-1)/q^(2*h)',
                         norm_only_coherent_preparation_included=True,
                         typical_source_fraction_numerator=99,
                         typical_source_fraction_denominator=100,
                         typical_marked_probability_power_two_exponent=-2*B,
                         ordinary_grover_iterations_must_exceed_power_two_exponent=B-2,
                         grover_target_success_numerator=1,
                         grover_target_success_denominator=2,
                         prime_certificates_replayed_this_run=False))
        counts['exact_reference_lane_bounds'] += 1

saved_name = 'native_rlwe_babai_profile_d64.json'
saved = json.loads((directory/saved_name).read_text())
d, q = saved['d'], int(saved['q'])
row = [int(value) for value in saved['reduced_row_basis'][0]]
g, f = tuple(row[:d]), tuple(-v for v in row[d:])
original = [int(value) for value in saved['native_ratio']]
mu = tuple([original[0]]+[-original[d-j] for j in range(1, d)])
product = multiply(mu, f)
assert all((g[i]-product[i]) % q == 0 for i in range(d))
assert math.gcd(absolute_norm(f), absolute_norm(g)) == 1
for lane in saved['lanes']:
    R = (int(lane['chosen_label'])+int(lane['error_norm'])-1)//int(lane['error_norm'])
    assert max(absolute_norm(f), absolute_norm(g)) <= R**d
    assert int(lane['error_norm'])**2*sum(v*v for v in row) < int(lane['chosen_label'])**2
counts['actual_primitive_classical_norm_gate_escape'] += 1

output = dict(status='LOCAL_DERIVATION_REVIEW_PENDING',
              scope='canonical_raw_norm_lift_and_modular_norm_only_multiplier_catalogues',
              quantum_algorithm=False, general_hardness_bound=False,
              original_prior_noise_laws_sampled=False,
              raw_lift_arbitrary_integral_unit_and_subfield_multiplier_included=True,
              raw_lift_arbitrary_integral_ring_multiplier_included=True,
              raw_lift_adaptive_modular_corrections_excluded=True,
              modular_recentered_lifts_included=True,
              modular_norm_summary_only=True,
              exact_integer_norm_carry_access_excluded=True,
              modular_arbitrary_unit_postprocessing_excluded=True,
              full_orientation_dependent_multiplier_generation_excluded=True,
              nonunit_subfield_multipliers_included=True,
              nonunit_public_ratio_event_charged=True,
              modular_zero_multiplier_trivial_relations_rejected=True,
              norm_only_coherent_preparation_included=True,
              quantum_resource_bound_scope='ordinary_amplitude_amplification_of_norm_only_preparation',
              general_quantum_query_lower_bound=False,
              native_content_norm_gate_formula='max(abs(Norm(f)),abs(Norm(g)))<=Norm((f,k))*R^d',
              content_gate_all_field_scalars_with_integral_native_outputs_included=True,
              content_gate_is_necessary_not_sufficient=True,
              fractional_content_corollary_requires_unrecentered_denominator=True,
              fractional_content_corollary_ratio='abs(Norm_S(a))<=C^h*abs(Norm_S(b))',
              coherent_b_domain='S_q_with_unique_modular_representatives',
              counts=dict(counts), rows=rows,
              source=dict(path=source_name,
                          sha256=hashlib.sha256((directory/source_name).read_bytes()).hexdigest()))
output['classical_escape_input'] = dict(path=saved_name,
                                       sha256=hashlib.sha256((directory/saved_name).read_bytes()).hexdigest())
if args.save:
    (directory/'native_rlwe_norm_lift_bounds.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps(dict(status=output['status'], counts=dict(counts), rows=rows), indent=2))
