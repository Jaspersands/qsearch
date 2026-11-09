"""Exact finite classical falsifier; no global-transform/quantum execution.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from itertools import combinations, product
from pathlib import Path
from sage.all import (CyclotomicField, QQ, binomial, diagonal_matrix,
                      identity_matrix, matrix, vector)


def kron(*factors):
    result = factors[0]
    for factor in factors[1:]:
        result = result.tensor_product(factor)
    return result


F4 = CyclotomicField(4)
ii = F4.gen()
I = identity_matrix(F4, 2).dense_matrix()
X = matrix(F4, [[0, 1], [1, 0]])
Y = matrix(F4, [[0, -ii], [ii, 0]])
Z = diagonal_matrix(F4, [1, -1]).dense_matrix()
local = (-(identity_matrix(F4, 16) + kron(Z, I, I, Z))
         * (kron(I, X, X, I) + kron(I, Y, Y, I))/8).change_ring(QQ).sparse_matrix()


def physical_H(N):
    return sum((kron(identity_matrix(QQ, 2**j, sparse=True), local,
                     identity_matrix(QQ, 2**(N-2-j), sparse=True))
                for j in range(N-1)), matrix(QQ, 2**(N+2), sparse=True))


def encode(spins):
    bonds = tuple(a ^ b for a, b in zip(spins, spins[1:]))
    tokens, position, final = [], 0, 0
    while position < len(bonds):
        if bonds[position] == 0:
            tokens.append('C')
            position += 1
        elif position+1 == len(bonds):
            final = 1
            position += 1
        else:
            tokens.append('A' if bonds[position+1] else 'B')
            position += 2
    word = ''.join(token for token in tokens if token != 'A')
    squeezed = tuple(int(token == 'A') for token in tokens)
    return (spins[0], word, final, sum(squeezed)), squeezed


def decode(label, squeezed):
    first, word, final, particles = label
    assert sum(squeezed) == particles and squeezed.count(0) == len(word)
    zero_labels = iter(word)
    tokens = ['A' if bit else next(zero_labels) for bit in squeezed]
    expansion = {'A': (1, 1), 'B': (1, 0), 'C': (0,)}
    bonds = tuple(bit for token in tokens for bit in expansion[token]) + (1,)*final
    spins = [first]
    for bit in bonds:
        spins.append(spins[-1] ^ bit)
    return tuple(spins)


def index(bits):
    return sum(bit << (len(bits)-1-j) for j, bit in enumerate(bits))


cases, Hamiltonians = [], {}
for N in range(2, 9):
    H = physical_H(N)
    Hamiltonians[N] = H
    sectors, lookup = {}, {}
    for spins in product(range(2), repeat=N+2):
        label, q = encode(spins)
        assert decode(label, q) == spins
        assert 2*label[3] + 2*label[1].count('B') + label[1].count('C') + label[2] == N+1
        assert (label, q) not in lookup
        lookup[label, q] = index(spins)
        sectors.setdefault(label, set()).add(q)
    assert len(lookup) == 2**(N+2)
    predicted, outgoing = {}, set()
    for label, words in sectors.items():
        m, ell = label[3], label[3]+len(label[1])
        expected_words = {tuple(int(i in occupied) for i in range(ell))
                          for occupied in combinations(range(ell), m)}
        assert words == expected_words and len(words) == binomial(ell, m)
        for q in words:
            for j in range(ell-1):
                if q[j] == q[j+1]:
                    continue
                neighbor = q[:j] + (q[j+1], q[j]) + q[j+2:]
                edge = lookup[label, neighbor], lookup[label, q]
                assert edge not in predicted
                predicted[edge] = -QQ(1)/2
                outgoing.add(edge[1])
    actual = {edge: value for edge, value in H.dict().items() if value}
    assert actual == predicted
    assert all(row != col and value == -QQ(1)/2 for (row, col), value in actual.items())
    cases.append({'N': N, 'spins': N+2, 'states': 2**(N+2), 'label_blocks': len(sectors),
                  'directed_transitions': len(actual), 'jammed_states': 2**(N+2)-len(outgoing),
                  'final_D_states': sum(len(words) for label, words in sectors.items() if label[2]),
                  'bijection_inverse_and_all_binomial_block_dimensions': True,
                  'Pauli_H_equals_squeezed_path_H': True, 'transition_multiplicity': 1})

# Exact supplied two-particle Slater eigenstate, with BOTH nontrivial B/C labels.
N, ell, m = 6, 4, 2
label = (0, 'BC', 0, m)
F = CyclotomicField(20)
z = F.gen()
imag = z**5
orbitals = matrix(F, [[(z**(2*k*(site+1))-z**(-2*k*(site+1)))/(2*imag)
                       for site in range(ell)] for k in (1, 2)])
energy = -sum((z**(2*k)+z**(-2*k))/2 for k in (1, 2))
psi, determinant_numerator, determinant_norm = vector(F, 2**(N+2)), F(0), F(0)
for occupied in combinations(range(ell), m):
    amplitude = orbitals.matrix_from_columns(occupied).det()
    squeezed = tuple(int(j in occupied) for j in range(ell))
    spins = decode(label, squeezed)
    psi[index(spins)] = amplitude
    probability = amplitude*amplitude.conjugate()
    determinant_norm += probability
    determinant_numerator += (-1)**sum(spins[:6])*probability
assert Hamiltonians[N].change_ring(F)*psi == energy*psi
pauli = diagonal_matrix(F, [(-1)**sum(spins[:6]) for spins in product(range(2), repeat=N+2)])
dense_norm = sum(a.conjugate()*a for a in psi)
dense_expectation = sum(a.conjugate()*b for a, b in zip(psi, pauli*psi))/dense_norm
assert dense_norm == determinant_norm
assert dense_expectation == determinant_numerator/determinant_norm
result = {
    'status': 'PASS', 'scope': 'Exact finite classical Pauli/bijection/Slater controls only; all-n proof separate.',
    'cases': cases,
    'Slater_control': {'N': N, 'label': list(label), 'ell': ell, 'occupied_sine_modes': [1, 2],
                       'exact_energy': str(energy), 'exact_norm_squared': str(dense_norm),
                       'physical_Pauli_word': 'ZZZZZZII', 'exact_expectation': str(dense_expectation),
                       'determinant_equals_dense_expectation': True,
                       'polynomial_simulation_for_general_observables_claimed': False},
    'claim_gates': {'all_n_theorem_from_control': False, 'quantum_execution': False,
                    'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'cases': cases, 'Slater_control': result['Slater_control']}, indent=2))
