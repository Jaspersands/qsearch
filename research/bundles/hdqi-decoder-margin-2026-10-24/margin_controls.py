"""Independent capped Bell-state controls and actual Majorana cycle fixtures."""

import math
import numpy as np
from scipy.linalg import expm

from decoder_margin import d, lift


def matrix(pauli, n):
    x, z, phase = pauli
    out = np.zeros((1 << n, 1 << n), dtype=complex)
    for y in range(1 << n):
        out[y ^ x, y] = (1j)**phase * (-1)**((y & z).bit_count())
    return out


def native_pilot(model):
    m = model.pilot.m
    if m > 9:
        raise ValueError("dense native pilot audit capped at nine generators")
    h = sum(float(j)*matrix((1 << i, model.pilot.lower_masks[i], 0), m)
            for i, j in enumerate(model.pilot.couplings))
    state = expm(-float(model.pilot.beta)*h/2)[:, 0]
    return state / np.linalg.norm(state)


def pullback(model, decoder, observable):
    if model.pilot.m > 7 or model.n > 4:
        raise ValueError("physical Bell audit cap exceeded")
    d.validate_pauli(model.n, observable)
    operators, residues = [], []
    for y in range(1 << model.pilot.m):
        op = np.eye(1 << model.n, dtype=complex)
        for i, pauli in enumerate(model.paulis):
            if y >> i & 1:
                op = op @ matrix(pauli, model.n)
        operators.append(op)
        residues.append(y ^ decoder(model.label(y)))
    q = matrix(observable, model.n)
    answer = np.zeros((len(operators), len(operators)), dtype=complex)
    for y, left in enumerate(operators):
        for z, right in enumerate(operators):
            if residues[y] == residues[z]:
                answer[y, z] = np.trace(left.conj().T @ q @ right) / (1 << model.n)
    return answer


def cycle_model(length, beta, couplings=None):
    if type(length) is not int or not 3 <= length <= 64:
        raise ValueError("cycle fixture length must be in 3..64")
    n = (length + 1)//2
    gammas = []
    for u in range(length):
        j = u//2
        gammas.append((1 << j, ((1 << j)-1) | ((u % 2) << j), u % 2))
    ps = []
    for u, v in [(i, i+1) for i in range(length-1)] + [(0, length-1)]:
        x, z, p = d.multiply(gammas[u], gammas[v])
        ps.append((x, z, (p+1) % 4))
    return d.Physical.create(n, ps, couplings or [1]*length, beta)


def cycle_decoder(model):
    """Binary elimination then majority choice; no exponential syndrome table."""
    m = model.pilot.m
    basis, kernel = {}, []
    for i in range(m):
        value, word = model.label(1 << i), 1 << i
        while value:
            pivot = value.bit_length()-1
            if pivot not in basis:
                basis[pivot] = (value, word)
                break
            a, b = basis[pivot]
            value, word = value ^ a, word ^ b
        if not value:
            kernel.append(word)
    full = (1 << m)-1
    if kernel != [full]:
        raise ValueError("fixture must have exactly the repetition relation")

    def decode(syndrome):
        value, word = syndrome, 0
        while value:
            pivot = value.bit_length()-1
            if pivot not in basis:
                return 0
            a, b = basis[pivot]
            value, word = value ^ a, word ^ b
        return min((word, word ^ full), key=lambda y: (y.bit_count(), y))
    return decode


def repetition_quotient(vertices, edges, beta):
    """Native physical Paulis with one repetition relation, for even-degree G."""
    if type(vertices) is not int or vertices < 3:
        raise ValueError("need at least three generators")
    host = d.s.Model.create([1]*vertices, beta, edges)
    degree = [0]*vertices
    for i, j in host.edges:
        degree[i] += 1
        degree[j] += 1
    if any(value % 2 for value in degree):
        raise ValueError("all-ones relation is not central: graph has odd degree")
    n = vertices-1
    ps = [(1 << i, host.lower_masks[i], 0) for i in range(n)]
    x, z, p = (0, 0, 0)
    for item in ps:
        x, z, p = d.multiply((x, z, p), item)
    ps.append((x, z, (x & z).bit_count() % 2))
    model = d.Physical.create(n, ps, [1]*vertices, beta)
    assert model.pilot.edges == host.edges
    return model


def complete_root_quotient(v, beta):
    if type(v) is not int or not 3 <= v <= 32:
        raise ValueError("explicit complete-root fixture capped at 32 vertices")
    root_edges = [(i, j) for i in range(v) for j in range(i+1, v)]
    graph_edges = [(i, j) for i in range(len(root_edges)) for j in range(i+1, len(root_edges))
                   if set(root_edges[i]) & set(root_edges[j])]
    return repetition_quotient(len(root_edges), graph_edges, beta)


def hermitian_word(model, word):
    x, z, p = model.ordered(word)
    return x, z, (p + ((p-(x & z).bit_count()) % 2)) % 4


def control(model, decoder, observable, word, cutoff):
    state = native_pilot(model)
    actual = pullback(model, decoder, observable)
    lifted = matrix(lift(model, observable, word), model.pilot.m)
    inside = [y for y in range(len(state)) if y.bit_count() <= cutoff]
    outside = [y for y in range(len(state)) if y.bit_count() > cutoff]
    mass = float(np.sum(np.abs(state[outside])**2))
    return {"actual_expectation": float(np.vdot(state, actual @ state).real),
            "canonical_expectation": float(np.vdot(state, lifted @ state).real),
            "operator_norm_difference": float(np.linalg.norm(actual-lifted, 2)),
            "good_column_error": float(np.linalg.norm((actual-lifted)[:, inside])),
            "good_block_error": float(np.linalg.norm((actual-lifted)[np.ix_(inside, inside)])),
            "actual_tail_mass": mass,
            "short_word_error_bound_from_actual_mass": 2*math.sqrt(mass),
            "arbitrary_readout_error_bound_from_actual_mass": 4*math.sqrt(mass),
            "dense_finite_control_not_production_estimator": True}
