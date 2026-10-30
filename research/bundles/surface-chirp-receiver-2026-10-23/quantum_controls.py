"""Bounded Qiskit controls, NOT a scalable oracle or gate compiler.

Native oracle fibers are obtained by enumerating legal public queries.
That exponential classical construction is separately counted. Unknown
graph coefficients are never passed to the receiver or measurement gate.
"""

from collections import defaultdict
from functools import lru_cache
from itertools import product
from random import Random

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from sympy import Matrix, eye

from chirp_receiver import ChirpPacket, mod
from classical_siegel import inverse, levi


def width(p):
    if p > 13:
        raise ValueError("dense quantum controls are limited to p<=13")
    return (p-1).bit_length()


@lru_cache(maxsize=16)
def inverse_fourier(p):
    d = 1 << width(p)
    matrix = np.eye(d, dtype=complex)
    labels = np.arange(p)
    matrix[:p, :p] = np.exp(-2j*np.pi*np.outer(labels, labels)/p)/np.sqrt(p)
    return Operator(matrix)


@lru_cache(maxsize=128)
def translation_gate(p, shift):
    d = 1 << width(p)
    permutation = np.eye(d, dtype=complex)
    permutation[:p, :p] = 0
    for t in range(p):
        permutation[(t+shift) % p, t] = 1
    return Operator(permutation)


@lru_cache(maxsize=128)
def pair_circuit(p, gamma):
    w, d = width(p), 1 << width(p)
    permutation = np.zeros((d*d, d*d), dtype=complex)
    for second in range(d):
        for first in range(d):
            new_second = (second-gamma*first) % p if first < p and second < p else second
            permutation[first+d*new_second, first+d*second] = 1
    circuit = QuantumCircuit(2*w)
    circuit.unitary(Operator(permutation), range(2*w), label="s=t2-gamma*t1")
    circuit.unitary(inverse_fourier(p), range(w), label="Fp inverse Fourier")
    return circuit


def paired_state(first, second, gamma, p):
    state = Statevector(np.kron(second.data, first.data))
    return state.evolve(pair_circuit(p, gamma))


def reference_chirp(b, c, r, p):
    """Secret-dependent fixture; NEVER called by the native-fiber backend."""
    data = np.zeros(1 << width(p), dtype=complex)
    data[:p] = [np.exp(2j*np.pi*((r*(c*t*t+2*b*t)) % p)/p)/np.sqrt(p) for t in range(p)]
    return Statevector(data)


class NativeFiberControl:
    def __init__(self, oracle, p, seed=0):
        if p not in (3, 5):
            raise ValueError("exhaustive native-fiber control is limited to primes 3 and 5")
        self.oracle, self.p, self.rng = oracle, p, Random(seed)
        self.tables = {}
        self.reference_table_queries = self.prepared_copies = self.pair_measurements = 0
        self.w, self.d = width(p), 1 << width(p)

    def _table(self, chart, direction):
        key = tuple(chart), direction
        if key in self.tables:
            return self.tables[key]
        buckets, labels = defaultdict(list), []
        p, d, i = self.p, self.d, 1-direction
        inverse_chart = inverse(chart, p)
        for t, x11, x12, x22 in product(range(p), repeat=4):
            x, a = Matrix([[x11, x12], [x12, x22]]), eye(2)
            a[i, direction] = t
            u = eye(4)
            for row in range(2):
                for col in range(2):
                    u[2*row, 2*col+1] = x[row, col]
            query = mod(chart*u*levi(a, p)*inverse_chart, p)
            label = self.oracle(query)
            self.reference_table_queries += 1
            buckets[label].append(t+d*x11+d*d*x12+d*d*d*x22)
            labels.append(label)
        self.tables[key] = buckets, labels
        return buckets, labels

    def prepare(self, chart, direction):
        buckets, labels = self._table(chart, direction)
        indices = buckets[self.rng.choice(labels)]
        data = np.zeros(self.d**4, dtype=complex)
        data[indices] = 1/np.sqrt(len(indices))
        state = Statevector(data)
        for register in (1, 2, 3):
            state = state.evolve(inverse_fourier(self.p), qargs=list(range(register*self.w, (register+1)*self.w)))
        state.seed(self.rng.getrandbits(32))
        outcome, collapsed = state.measure(list(range(self.w, 4*self.w)))
        encoded = int(outcome, 2)
        u11, u12, u22 = encoded % self.d, (encoded//self.d) % self.d, encoded//(self.d*self.d)
        self.prepared_copies += 1
        if max(u11, u12, u22) >= self.p:
            raise AssertionError("Fourier sampling leaked into invalid padding")
        r = u11 if direction == 1 else u22
        if not r:
            return None
        start = self.d*encoded
        packet = Statevector(collapsed.data[start:start+self.d])
        shift = u12*pow(2*r, -1, self.p) % self.p
        packet = packet.evolve(translation_gate(self.p, shift))
        return ChirpPacket(r, packet)

    def measure_pair(self, first, second, gamma, p):
        state = paired_state(first.state, second.state, gamma, p)
        state.seed(self.rng.getrandbits(32))
        outcome, _ = state.measure()
        encoded = int(outcome, 2)
        frequency, s = encoded % self.d, encoded//self.d
        self.pair_measurements += 1
        if max(frequency, s) >= p:
            raise AssertionError("paired measurement leaked into invalid padding")
        return s, frequency
