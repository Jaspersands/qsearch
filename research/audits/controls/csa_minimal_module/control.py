"""Exact classical module-extraction control, not a KM/quantum implementation.

Run: /opt/anaconda3/envs/qsearch-cas/bin/python control.py
The Q(i) splitting representation is an explicit fixture. PARI's index call
on the expanded table is retained even when unsupported; a separate cyclic-H
call checks this specialized fixture without claiming a table conversion.
"""

import json
from pathlib import Path

from sage.all import (QQ, NumberField, PolynomialRing, QuaternionAlgebra,
                      identity_matrix, matrix, pari, vector)


P = PolynomialRing(QQ, 't')
F = NumberField(P.gen()**2 + 1, 'ii')
ii = F.gen()
H = QuaternionAlgebra(QQ, -1, -1, names=('i', 'j', 'k'))
qb = [H(1)] + list(H.gens())
zero = matrix(H, 2, 2)
one = identity_matrix(H, 2)


def flat(a):
    return vector(QQ, [c for row in range(2) for col in range(2)
                       for c in a[row, col].coefficient_tuple()])


natural = []
for row in range(2):
    for col in range(2):
        for q in qb:
            a = matrix(H, zero)
            a[row, col] = q
            natural.append(a)
basis = [one] + natural[1:]
T = matrix(QQ, [flat(a) for a in basis]).transpose()
assert T.det() != 0
Tinv = T.inverse()


def coords(a):
    return Tinv * flat(a)


def algebra_element(v):
    return sum((c * a for c, a in zip(v, basis)), zero)


def rho(a):
    out = matrix(F, 4, 4)
    for row in range(2):
        for col in range(2):
            a0, a1, a2, a3 = a[row, col].coefficient_tuple()
            out[2*row:2*row+2, 2*col:2*col+2] = matrix(F, [
                [a0 + a1*ii, -a2 - a3*ii],
                [a2 - a3*ii, a0 - a1*ii],
            ])
    return out


def flat_v(v):
    return vector(QQ, [c for entry in v for c in F(entry).vector()])


v_basis = [vector(F, [ii**power if row == slot else 0 for row in range(4)])
           for slot in range(4) for power in range(2)]
left = [matrix(QQ, [coords(a*b) for b in basis]).transpose() for a in basis]
action = [matrix(QQ, [flat_v(rho(a)*v) for v in v_basis]).transpose() for a in basis]
assert left[0] == identity_matrix(QQ, 16)
assert action[0] == identity_matrix(QQ, 8)
assert all(c.denominator() == 1 for m in left for c in m.list())
for i, a in enumerate(basis):
    for j, b in enumerate(basis):
        assert rho(a*b) == rho(a)*rho(b)
        assert left[i]*left[j] == sum((c*L for c, L in zip(coords(a*b), left)), matrix(QQ, 16))
        assert action[i]*action[j] == sum((c*R for c, R in zip(coords(a*b), action)), matrix(QQ, 8))

# Actual expanded multiplication-table baseline, with no supplied cyclic form.
pari_algebra = pari('nfinit(y)').alginit(pari(left))
pari_index = None
pari_index_error = None
try:
    pari_index = int(pari_algebra.algindex())
except Exception as error:
    pari_index_error = str(error)
    assert 'computation of Hasse invariants over table CSA is not yet implemented' in pari_index_error
if pari_index is not None:
    assert pari_index == 2
# Separate specialized fixture verification; this is NOT table-input algindex.
assert H.discriminant() == 2
cyclic_H_index = int(pari('alginit(nfinit(y),[-1,-1],x)').algindex())
assert cyclic_H_index == 2
index = cyclic_H_index

# Row-major unknown f in M_(16,8)(Q), L_b f = f R_b.
entries = {}
for b, (L, R) in enumerate(zip(left, action)):
    for i in range(16):
        for j in range(8):
            row = (b*16 + i)*8 + j
            for k in range(16):
                if L[i, k]:
                    key = row, k*8 + j
                    entries[key] = entries.get(key, 0) + L[i, k]
            for k in range(8):
                if R[k, j]:
                    key = row, i*8 + k
                    entries[key] = entries.get(key, 0) - R[k, j]
system = matrix(QQ, 2048, 128, entries, sparse=True)
kernel = system.right_kernel().basis()
assert len(kernel) == 8
assert system.rank() == 120
f = sum(((j + 1)*matrix(QQ, 16, 8, row) for j, row in enumerate(kernel)), matrix(QQ, 16, 8))
assert f.rank() == 8
assert all(L*f == f*R for L, R in zip(left, action))
ideal = [algebra_element(f.column(j)) for j in range(8)]
affine = matrix(QQ, 128, 8)
for j, l in enumerate(ideal):
    for k, h in enumerate(ideal):
        affine[16*j:16*(j+1), k] = matrix(QQ, 16, 1, coords(l*h))
rhs = vector(QQ, [c for l in ideal for c in coords(l)])
assert affine.rank() == 4
solution = affine.solve_right(rhs)
assert affine*solution == rhs
e = sum((c*l for c, l in zip(solution, ideal)), zero)
assert all(l*e == l for l in ideal)
assert e*e == e
Ae = matrix(QQ, [coords(a*e) for a in basis]).transpose()
corner = matrix(QQ, [coords(e*a*e) for a in basis]).transpose()
assert Ae.rank() == 8
assert Ae.column_space() == f.column_space()
assert corner.rank() == 4

# Wrong module dimension: regular A gives image A and right identity e=1.
# The degree-4 splitting-field realization of this regular module was already
# checked in the referenced reduced_norms control; it is not rerun here.
assert one*one == one
assert matrix(QQ, [coords(a*one) for a in basis]).rank() == 16
e11 = matrix(H, [[1, 0], [0, 0]])
e22 = one - e11
assert e11 != zero and e22 != zero
assert e11*e11 == e11 and e22*e22 == e22
assert e11*e22 == zero and e22*e11 == zero
assert all(a*one == a for a in basis)

result = {
    'status': 'PASS_MODULE_EXTRACTION_TABLE_INDEX_UNSUPPORTED' if pari_index is None else 'PASS',
    'scope': 'One exact classical fixture/control, not an asymptotic proof or a KM execution.',
    'algebra': 'M2((-1,-1)_Q)', 'degree_n': 4, 'index_d': index,
    'splitting_fixture': 'Q(i), explicit known matrices',
    'module_Q_dimension': 8, 'basis_products_checked': 256,
    'pari_baseline': {
        'input': 'alginit(nfinit(y), expanded integral identity-first left multiplication table)',
        'table_size': [16, 16, 16], 'alginit_succeeded': True,
        'algindex': pari_index, 'algindex_error': pari_index_error,
        'algindex_status': 'PASS' if pari_index is not None else 'UNSUPPORTED_TABLE_INPUT',
        'supplied_cyclic_or_local_invariant_advice': False,
    },
    'separate_specialized_fixture_check': {
        'input': 'Explicit quaternion/cyclic presentation (-1,-1), plus known M2(H) factorization of this fixture',
        'Hamilton_discriminant': 2, 'Hamilton_algindex': cyclic_H_index, 'fixture_index': index,
        'general_table_to_cyclic_conversion_claim': False,
    },
    'hom_system': {'equations': 2048, 'variables': 128, 'rank': 120, 'nullity': 8,
                   'chosen_combination': list(range(1, 9)), 'chosen_map_rank': int(f.rank())},
    'extraction': {
        'affine_coefficient_rank': int(affine.rank()), 'idempotent_coordinates': [str(c) for c in coords(e)],
        'idempotent_verified': True, 'image_equals_Ae': True,
        'Ae_Q_dimension': int(Ae.rank()), 'corner_eAe_Q_dimension': int(corner.rank()),
    },
    'wrong_degree_control': {
        'regular_module_Q_dimension': 16, 'image_ideal_Q_dimension': 16,
        'extracted_idempotent': '1', 'nonminimal': True,
        'orthogonal_nonzero_idempotent_decomposition': '1 = E11 + E22',
        'prior_degree_4_field_control': 'research/audits/controls/reduced_norms/control.py',
        'prior_control_rerun': False,
    },
    'claim_gates': {'full_algorithm_execution': False, 'quantum_execution': False,
                    'general_asymptotic_clock_verified': False, 'finite_control_proves_minimality_in_general': False,
                    'novelty_or_classical_separation': False},
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
