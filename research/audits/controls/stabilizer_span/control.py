"""Exact classical falsifier control; finite checks do not prove an all-n claim.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python control.py.
Enumerates stabilizer descriptions, not copies of an unknown quantum state.
"""

import json
from itertools import combinations, product
from pathlib import Path

from sage.all import CyclotomicField, GF, PolynomialRing, QQ, VectorSpace, matrix, vector


F = CyclotomicField(8)
z = F.gen()
sqrt2 = z + z.conjugate()
imag = z**2


def norm2(v):
    return QQ(sum(a * a.conjugate() for a in v))


def cells(n):
    points = list(product(range(2), repeat=n))
    exceptional = [x for x in points if sum(x) <= 1]
    blocks = {}
    for i, j in combinations(range(n), 2):
        blocks[i, j] = [x for x in points if tuple(k for k in range(n) if x[k])[:2] == (i, j)]
    return points, exceptional, blocks


def six_qubit_check():
    n = 6
    points, exceptional, blocks = cells(n)
    assert len(exceptional) == n + 1
    assert sorted(exceptional + [x for block in blocks.values() for x in block]) == points
    root = vector(F, [sqrt2**(-n)] * 2**n)
    atoms = [root]
    overlaps = []
    for (i, j), block in blocks.items():
        dimension = n - j - 1
        assert len(block) == 2**dimension
        atom = vector(F, [sqrt2**(-dimension) if x in block else 0 for x in points])
        assert norm2(atom) == 1
        atoms.append(atom)
        overlaps.append(sqrt2**(-j - 1))
    basis = matrix(F, atoms).transpose()
    gram = basis.conjugate_transpose() * basis
    K = len(atoms)
    r = QQ(n + 1) / 2**n
    residual = root - sum((a * v for a, v in zip(overlaps, atoms[1:])), vector(F, 2**n))
    expected_residual = vector(F, [sqrt2**(-n) if x in exceptional else 0 for x in points])
    assert residual == expected_residual
    assert norm2(residual) == r
    assert basis.rank() == K
    assert gram.det() == r
    R = PolynomialRing(F, 't')
    t = R.gen()
    expected_charpoly = (t - 1)**(K - 2) * ((t - 1)**2 - (1 - r))
    assert R(gram.charpoly()) == expected_charpoly
    assert sum(a * a for a in overlaps) == 1 - r
    return {
        'n': n, 'K': K, 'exceptional_size': len(exceptional),
        'cell_dimensions': [n - j - 1 for i, j in blocks],
        'rank': int(basis.rank()), 'determinant': str(r),
        'residual_norm_squared': str(norm2(residual)),
        'charpoly': str(expected_charpoly),
        'checks': {'partition': True, 'cell_sizes': True, 'independence': True,
                   'gram_characteristic_polynomial': True, 'residual': True},
    }


def three_qubit_enumeration():
    n = 3
    points, exceptional, blocks = cells(n)
    ambient = VectorSpace(GF(2), n)
    target = vector(F, [F(1) / 2 if x in exceptional else 0 for x in points])
    states = set()
    by_dimension = {}
    in_span = {}
    maximum = QQ(0)
    maximizing_count = 0
    for d in range(n + 1):
        dimension_count = 0
        for subspace in ambient.subspaces(d):
            rows = list(subspace.basis())
            parameters = list(product(range(2), repeat=d))
            offsets_seen = set()
            for offset_tuple in points:
                offset = vector(GF(2), offset_tuple)
                support = [tuple(int(a) for a in offset + sum(
                    (bit * row for bit, row in zip(u, rows)), ambient.zero())) for u in parameters]
                coset_key = tuple(sorted(support))
                if coset_key in offsets_seen:
                    continue
                offsets_seen.add(coset_key)
                pairs = list(combinations(range(d), 2))
                for linear in product(range(4), repeat=d):
                    for quadratic in product(range(2), repeat=len(pairs)):
                        values = {x: F(0) for x in points}
                        for u, x in zip(parameters, support):
                            phase = sum(a * b for a, b in zip(linear, u)) + 2 * sum(
                                q * u[i] * u[j] for q, (i, j) in zip(quadratic, pairs))
                            values[x] = sqrt2**(-d) * imag**phase
                        # Canonicalize global phase for an independent uniqueness check.
                        first = next(values[x] for x in points if values[x] != 0)
                        phase_fix = first / sqrt2**(-d)
                        state = tuple(values[x] / phase_fix for x in points)
                        assert state not in states
                        states.add(state)
                        dimension_count += 1
                        assert norm2(state) == 1
                        overlap = sum(a.conjugate() * b for a, b in zip(target, state))
                        fidelity = QQ(overlap * overlap.conjugate())
                        if fidelity > maximum:
                            maximum, maximizing_count = fidelity, 1
                        elif fidelity == maximum:
                            maximizing_count += 1
                        groups = [exceptional] + list(blocks.values())
                        if all(len({values[x] for x in group}) == 1 for group in groups):
                            assert fidelity in (QQ(0), QQ(1) / 2)
                            key = str(fidelity)
                            in_span[key] = in_span.get(key, 0) + 1
        by_dimension[str(d)] = dimension_count
    assert len(states) == 1080
    assert maximum == QQ(9) / 16
    return {
        'n': n, 'state_count': len(states), 'distinct_up_to_global_phase': True,
        'states_by_support_dimension': by_dimension,
        'maximum_stabilizer_fidelity': str(maximum),
        'maximizing_state_count': maximizing_count,
        'in_V_fidelity_histogram': in_span,
        'enumeration': 'All GF(2) linear subspaces, all affine cosets, and phases i^(linear + 2 quadratic); exact Q(zeta_8).',
    }


if __name__ == '__main__':
    result = {
        'status': 'PASS', 'arithmetic': 'Sage exact cyclotomic field Q(zeta_8)',
        'scope': 'Classical supplied-description stabilizer simulation; finite falsifier controls only.',
        'six_qubit': six_qubit_check(),
        'three_qubit': three_qubit_enumeration(),
        'claim_gates': {
            'full_learner_execution': False, 'quantum_execution': False,
            'unrestricted_extent_lower_bound_exponential': False,
            'general_learning_no_go': False,
        },
    }
    destination = Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
