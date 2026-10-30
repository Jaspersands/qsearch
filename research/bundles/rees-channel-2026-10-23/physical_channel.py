"""Bounded physical check of adaptive Rees central descent, over UT3(F3).

Constructs vectors, actual translation permutations and projective outcomes.
No regular-coefficient formula or supplied hidden subgroup enters the channel.
Enumeration is explicit: this is a falsifier, not a scalable HSP algorithm.
"""

from itertools import product
import numpy as np


class Fixture:
    def __init__(self):
        self.p = 3
        self.group = tuple(product(range(3), repeat=3))
        self.addresses = tuple(product(range(3), repeat=2))
        self.index = {g: i for i, g in enumerate(self.group)}

    @staticmethod
    def mul(a, b):
        x, y, z = a
        X, Y, Z = b
        return ((x+X) % 3, (y+Y) % 3, (z+Z+x*Y) % 3)

    @staticmethod
    def inv(a):
        x, y, z = a
        return (-x % 3, -y % 3, (-z+x*y) % 3)

    @staticmethod
    def dilation(a, scale):
        x, y, z = a
        return (scale*x % 3, scale*y % 3, scale*scale*z % 3)

    @staticmethod
    def section(q, twisted=False):
        x, y = q
        return (x, y, (x*x+y+x*y) % 3 if twisted else 0)

    def right_translate(self, vector, g):
        out = np.zeros_like(vector)
        inverse = self.inv(g)
        for i, x in enumerate(self.group):
            out[self.index[self.mul(x, inverse)]] = vector[i]
        return out

    def oracle_source(self, oracle):
        fibers = {}
        for g in self.group:
            fibers.setdefault(oracle(g), []).append(g)
        records = []
        for members in fibers.values():
            vector = np.zeros(len(self.group), dtype=complex)
            for g in members:
                vector[self.index[g]] = 1/np.sqrt(len(members))
            records.append((len(members)/len(self.group), vector))
        return records

    def central_branches(self, source):
        branches = {}
        for label in range(3):
            records, mass = [], 0.0
            for weight, vector in source:
                projected = sum(np.exp(-2j*np.pi*label*z/3)*self.right_translate(vector, (0, 0, z))
                                for z in range(3))/3
                mass += weight*float(np.vdot(projected, projected).real)
                records.append((weight, projected))
            if mass > 1e-14:
                branches[label] = (mass, tuple((weight/mass, vector) for weight, vector in records))
        return branches

    def branch_gram(self, branch, scale, twisted=False, repetitions=1):
        """Trace the target AFTER controlled permutation, keeping all q,q' entries."""
        result = np.zeros((9, 9), dtype=complex)
        for weight, vector in branch:
            evolved = []
            for q in self.addresses:
                value = vector
                action = self.dilation(self.section(q, twisted), scale)
                for _ in range(repetitions):
                    value = self.right_translate(value, action)
                evolved.append(value)
            matrix = np.array(evolved)
            result += weight*matrix@matrix.conj().T
        return result

    def packet_gram(self, branches, labels, scales, twisted=False):
        if len(labels) != len(scales):
            raise ValueError("one scale for each independently acquired target required")
        result, mass = np.ones((9, 9), dtype=complex), 1.0
        for label, scale in zip(labels, scales):
            mass *= branches[label][0]
            result *= self.branch_gram(branches[label][1], scale, twisted)
        return mass, result

    def ideal_gram(self):
        return np.array([[float(q[1] == r[1]) for r in self.addresses] for q in self.addresses])


def bounded_scales(labels):
    """Exhaustive 3^3 TEST solver, not the proposed asymptotic scalar backend."""
    for scales in product(range(3), repeat=len(labels)):
        if any(scales) and sum(label*s*s for label, s in zip(labels, scales)) % 3 == 0:
            return scales
    raise ArithmeticError("bounded scalar fixture failed")


def choi(gram):
    dimension = len(gram)
    out = np.zeros((dimension**2, dimension**2), dtype=complex)
    positions = [i*(dimension+1) for i in range(dimension)]
    out[np.ix_(positions, positions)] = gram/dimension
    return out


def trace_distance(a, b):
    return float(np.sum(np.abs(np.linalg.eigvalsh(a-b)))/2)


def apply_with_reference(gram, density, reference_dimension):
    dimension = len(gram)
    if density.shape != (dimension*reference_dimension,)*2:
        raise ValueError("density dimension does not match the reference")
    blocks = density.reshape(dimension, reference_dimension, dimension, reference_dimension)
    return (blocks*gram[:, None, :, None]).reshape(density.shape)


def correlated_bank_control():
    """A real three-target GHZ bank with correct raw and conditional marginals.

    The hidden subgroup is trivial. The joint state is NOT the fresh product
    promised by the algorithm. Its central branch still obeys the moment.
    """
    fixture = Fixture()
    dimension = len(fixture.group)
    raw = np.zeros((dimension,)*3, dtype=complex)
    for i in range(dimension):
        raw[i, i, i] = 1/np.sqrt(dimension)

    def translate_axis(tensor, g, axis):
        sources = [0]*dimension
        inverse = fixture.inv(g)
        for i, x in enumerate(fixture.group):
            sources[fixture.index[fixture.mul(x, inverse)]] = i
        return np.take(tensor, sources, axis=axis)

    def marginal(tensor, axis):
        matrix = np.moveaxis(tensor, axis, 0).reshape(dimension, -1)
        return matrix@matrix.conj().T

    raw_error = max(np.max(np.abs(marginal(raw, axis)-np.eye(dimension)/dimension))
                    for axis in range(3))
    projected = raw
    for axis in range(3):
        projected = sum(np.exp(-2j*np.pi*z/3)*translate_axis(projected, (0, 0, z), axis)
                        for z in range(3))/3
    mass = float(np.vdot(projected, projected).real)
    conditioned = projected/np.sqrt(mass)
    branches = fixture.central_branches(fixture.oracle_source(lambda g: g))
    expected_local = sum(w*np.outer(v, v.conj()) for w, v in branches[1][1])
    conditional_error = max(np.max(np.abs(marginal(conditioned, axis)-expected_local))
                            for axis in range(3))
    evolved = []
    for q in fixture.addresses:
        value = conditioned
        for axis in range(3):
            value = translate_axis(value, fixture.section(q, True), axis)
        evolved.append(value.reshape(-1))
    matrix = np.array(evolved)
    gram = matrix@matrix.conj().T
    _, independent = fixture.packet_gram(branches, (1, 1, 1), (1, 1, 1), True)
    return {
        "central_record": [1, 1, 1], "scales": [1, 1, 1],
        "moment_mod_3": 0, "central_record_mass": mass,
        "raw_single_target_maximum_error": float(raw_error),
        "conditional_single_target_maximum_error": float(conditional_error),
        "joint_output_identity_channel_error": float(np.max(np.abs(gram-1))),
        "joint_choi_trace_distance_from_required_pinching": trace_distance(choi(gram), choi(np.eye(9))),
        "independent_bank_choi_trace_distance": trace_distance(choi(independent), choi(np.eye(9))),
    }


def audit():
    fixture = Fixture()
    branches = fixture.central_branches(fixture.oracle_source(lambda g: g[1:]))
    ideal = fixture.ideal_gram()
    records, mass_sum, cq_distance = [], 0.0, 0.0
    for labels in product(range(3), repeat=3):
        scales = bounded_scales(labels)
        mass, gram = fixture.packet_gram(branches, labels, scales)
        _, twisted = fixture.packet_gram(branches, labels, scales, True)
        difference = trace_distance(choi(gram), choi(ideal))
        if np.max(np.abs(gram-ideal)) > 1e-12 or np.max(np.abs(twisted-ideal)) > 1e-12:
            raise ArithmeticError("complete adaptive branch failed")
        mass_sum += mass
        cq_distance += mass*difference
        records.append({"labels": labels, "scales": scales, "mass": mass,
                        "normalized_choi_trace_distance": difference})
    reused = fixture.branch_gram(branches[1][1], 1, repetitions=3)
    wrong_labels, wrong_scales = (1, 1, 0), (1, 2, 0)
    _, wrong_moment = fixture.packet_gram(branches, wrong_labels, wrong_scales, True)
    nonhomogeneous = fixture.central_branches(fixture.oracle_source(lambda g: (g[1], (g[2]-g[0]) % 3)))
    _, unlifted = fixture.packet_gram(nonhomogeneous, (1, 2, 0), (1, 2, 0))
    return {
        "all_positive_adaptive_label_tuples": records,
        "complete_instrument_mass": mass_sum,
        "complete_cq_choi_trace_distance": cq_distance,
        "target_reuse_choi_trace_distance": trace_distance(choi(reused), choi(ideal)),
        "wrong_linear_moment_choi_trace_distance": trace_distance(choi(wrong_moment), choi(ideal)),
        "unlifted_nonhomogeneous_hidden_subgroup_choi_trace_distance": trace_distance(choi(unlifted), choi(ideal)),
        "correlated_three_target_bank": correlated_bank_control(),
        "enumerated_group_order": 27, "address_dimension": 9,
        "scalable_quantum_receiver_implemented": False,
        "quantum_device_executed": False, "speedup_claim": False,
    }
