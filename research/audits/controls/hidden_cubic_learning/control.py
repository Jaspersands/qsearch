"""Exact classical falsifier for one occurrence-two cubic; not a learner."""
from pathlib import Path
import json
from itertools import combinations
from sage.all import GF, matrix, vector, QQ

n = 6
triples = [(0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5)]
F = GF(2)
bits = [vector(F, [(x >> i) & 1 for i in range(n)]) for x in range(2**n)]
def phase(x):
    return sum(all((x >> i) & 1 for i in edge) for edge in triples) % 2

def walsh(q):
    v = [1 - 2*t for t in q]
    h = 1
    while h < len(v):
        for i in range(0, len(v), 2*h):
            for j in range(i, i+h):
                a, b = v[j], v[j+h]
                v[j], v[j+h] = a+b, a-b
        h *= 2
    return v

support = []
rank_counts = {}
offset_counterexample = None
numerator_total = 0
for a in range(2**n):
    q = [phase(x) ^ phase(x ^ a) for x in range(2**n)]
    W = walsh(q)
    B = matrix(F, n, n, lambda i, j: q[(1 << i) ^ (1 << j)] ^ q[1 << i] ^ q[1 << j] ^ q[0])
    radical = B.right_kernel().basis_matrix()
    rhs = vector(F, [q[sum(int(v[i]) << i for i in range(n))] ^ q[0] for v in radical.rows()])
    point = radical.solve_right(rhs)
    directions = radical.right_kernel().basis_matrix()
    rank = B.rank()
    rank_counts[int(rank)] = rank_counts.get(int(rank), 0) + 1
    linear = vector(F, [q[1 << i] ^ q[0] for i in range(n)])
    if radical*linear != rhs and offset_counterexample is None:
        offset_counterexample = {'a': a, 'radical_basis': [[int(t) for t in row] for row in radical.rows()], 'rhs': list(map(int, rhs)), 'naive_linear': list(map(int, linear))}
    assert directions.nrows() == rank
    for b in range(2**n):
        legal = radical*bits[b] == rhs
        assert (W[b] != 0) == legal
        assert W[b]**2 == (2**(2*n-rank) if legal else 0)
        numerator_total += W[b]**2
        if legal:
            support.append(a | (b << n))
            for i in range(n):
                neighbours = {j for e in triples if i in e for j in e if j != i}
                assert not ((b >> i & 1) and all(not (a >> j & 1) for j in neighbours))
assert numerator_total == 2**(3*n)
assert offset_counterexample is not None

# Standard exact F2 ranks: identify finite-case linear/quadratic equations.
monomials = [()] + [(i,) for i in range(2*n)] + list(combinations(range(2*n), 2))
E = matrix(F, [[int(all(v >> i & 1 for i in monomial)) for monomial in monomials] for v in support])
k1 = 1+2*n-E[:, :1+2*n].rank()
k2 = len(monomials)-E.rank()

# Algebraic affine Clifford relabel only, not a second quantum simulation.
def relabel(v):
    a, b = v & (2**n-1), v >> n
    b ^= ((a & 1) ^ 1)  # S on qubit0: b0 <- b0+a0+1
    ai, bi = (a >> 2) & 1, (b >> 2) & 1  # H on qubit2
    a ^= (ai ^ bi) << 2
    b ^= (ai ^ bi) << 2
    a ^= ((a >> 0) & 1) << 4  # CNOT0->4
    b ^= ((b >> 4) & 1) << 0
    return a | (b << n)
all_labels = list(range(2**(2*n)))
assert len({relabel(v) for v in all_labels}) == len(all_labels)
def swap(v):
    return ((v & (2**n-1)) & (v >> n)).bit_count() % 2
assert all(swap(v) == swap(relabel(v)) for v in all_labels)
assert all(swap(v) == 0 for v in support)

# A finite product-parity event, sampled exhaustively with exact weights.
# Its transformed counterpart has the same weight under the relabeled law.
weights = {}
for v in support:
    a, b = v & (2**n-1), v >> n
    q = [phase(x) ^ phase(x ^ a) for x in range(2**n)]
    weights[v] = QQ(walsh(q)[b]**2) / 2**(3*n)
forms = [(1, 0), (1 << (n+1), 1), ((1 << 2) | (1 << (n+4)), 0)]
event = sum(w for v, w in weights.items() if all(((v & mask).bit_count() % 2) ^ c for mask, c in forms))
assert event > 0
assert event >= QQ(1) / 2**(2*len(forms)+2*(2**len(forms)-1))
result = {
    'instance': 'six edge variables, four cubic vertex stars of K4',
    'n': n, 'triples': triples, 'max_occurrence': 2,
    'quadratic_radical_sampler_matches_all_4096_Bell_probabilities': True,
    'normalization': '1', 'support_size': len(support), 'derivative_rank_counts': rank_counts,
    'all_local_factored_constraints_hold': True, 'naive_linear_offset_rejected': offset_counterexample,
    'affine_Clifford_relabel_is_bijection_preserving_swap': True,
    'relabel_control_is_algebraic_only': True,
    'K1_dimension': int(k1), 'K2_dimension': int(k2),
    'one_three_factor_event_probability': str(event),
    'finite_control_only': True, 'all_n_gap_established_by_control': False,
    'frame_extractor_implemented': False, 'full_learner_implemented': False,
    'quantum_execution': False, 'classical_separation': False, 'novelty_claim': False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['support_size','derivative_rank_counts','K1_dimension','K2_dimension','one_three_factor_event_probability']}, sort_keys=True))
