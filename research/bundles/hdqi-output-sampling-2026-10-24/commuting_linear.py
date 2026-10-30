"""Polynomial left-output sampler for commuting Paulis and linear decoding.

This does not sample both halves of the purification. It samples the actual
decoder output, which is not automatically the desired Gibbs state.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

import output_sampling as o


@dataclass(frozen=True)
class LinearDecoder:
    n: int
    m: int
    columns: tuple[int, ...]

    @classmethod
    def create(cls, model, columns):
        columns = tuple(columns)
        if len(columns) != 2*model.n or any(type(v) is not int or not 0 <= v < 1 << model.pilot.m for v in columns):
            raise ValueError("decoder must be an explicit m by 2n binary matrix")
        result = cls(model.n, model.pilot.m, columns)
        if any(model.label(result(model.label(1 << i))) != model.label(1 << i)
               for i in range(model.pilot.m)):
            raise ValueError("linear decoder fails BDB=B")
        return result

    def __call__(self, syndrome):
        if type(syndrome) is not int or not 0 <= syndrome < 1 << (2*self.n):
            raise ValueError("invalid physical syndrome")
        answer = 0
        for j, column in enumerate(self.columns):
            if syndrome >> j & 1:
                answer ^= column
        return answer


def build_linear_decoder(model):
    """Gaussian section on im B, extended linearly to all syndromes."""
    width, m = 2*model.n, model.pilot.m
    rows = [tuple((model.label(1 << i) >> j) & 1 for j in range(width))+
            tuple(int(i == j) for j in range(m)) for i in range(m)]
    reduced = o.row_basis(rows, 2)
    pivots = [(next(j for j in range(width) if row[j]), row) for row in reduced if any(row[:width])]
    columns = []
    for coordinate in range(width):
        residual, answer = 1 << coordinate, 0
        for pivot, row in pivots:
            if residual >> pivot & 1:
                residual ^= sum(row[j] << j for j in range(width))
                answer ^= sum(row[width+j] << j for j in range(m))
        columns.append(answer)
    return LinearDecoder.create(model, columns)


def affine_solution(model_n, constraints, values, rng):
    if len(constraints) != len(values):
        raise ValueError("one right-hand side per constraint required")
    if not constraints:
        return rng.getrandbits(model_n)
    rows = [tuple((mask >> j) & 1 for j in range(model_n))+(value,)
            for mask, value in zip(constraints, values)]
    reduced = o.row_basis(rows, 2)
    if any(not any(row[:model_n]) and row[-1] for row in reduced):
        raise ValueError("inconsistent affine constraints")
    pivots = [(next(j for j in range(model_n) if row[j]), row) for row in reduced if any(row[:model_n])]
    pivot_set = {pivot for pivot, _ in pivots}
    answer = sum(rng.getrandbits(1) << j for j in range(model_n) if j not in pivot_set)
    for pivot, row in pivots:
        value = row[-1] ^ (sum(row[j] << j for j in range(model_n)) & answer).bit_count() % 2
        answer |= value << pivot
    return answer


class Sampler:
    def __init__(self, model, decoder, epsilon=F(1, 8)):
        epsilon = o.s.rational(epsilon)
        if not 0 < epsilon <= F(1, 4):
            raise ValueError("epsilon must be in (0,1/4]")
        if model.pilot.edges:
            raise ValueError("shortcut requires pairwise commuting physical Paulis")
        if not isinstance(decoder, LinearDecoder):
            raise ValueError("shortcut requires an explicit verified linear decoder")
        if decoder.n != model.n or decoder.m != model.pilot.m:
            raise ValueError("decoder dimensions do not match input")
        LinearDecoder.create(model, decoder.columns)
        self.model, self.decoder = model, decoder
        self.epsilon, self.eta = epsilon, epsilon/(16*model.pilot.m)
        self.constraints = o.pure_z_basis(model)["z_basis"]
        self.h, self.phases = [], []
        for z in self.constraints:
            h = decoder(z << model.n)
            x, actual_z, phase = model.ordered(h)
            if x or actual_z != z or phase % 2:
                raise ArithmeticError("invalid diagonal subgroup phase")
            self.h.append(h)
            self.phases.append(phase//2)
        self.coins, self.biases = [], []
        for j, x in zip(model.pilot.couplings, model.pilot.x):
            even = o.s.parity_law(x, 0, self.eta)
            odd = o.s.parity_law(x, 1, self.eta) if x else None
            e, v = even.law.normalizer, x*odd.law.normalizer if odd else F(0)
            bias = (-1 if j > 0 else 1)*2*e*v/(e*e+v*v)
            self.biases.append(bias)
            self.coins.append(o.s.RationalLaw.create((0, 1), (1+bias, 1-bias)))

    def sample(self, rng):
        word = sum(law.draw(rng) << i for i, law in enumerate(self.coins))
        rhs = [phase ^ ((h & word).bit_count() % 2) for phase, h in zip(self.phases, self.h)]
        return affine_solution(self.model.n, self.constraints, rhs, rng)

    def ledger(self):
        return {"physical_qubits": self.model.n, "generators": self.model.pilot.m,
                "diagonal_rank": len(self.constraints), "epsilon": str(self.epsilon),
                "site_tail": str(self.eta), "tv_upper": str(5*self.model.pilot.m*self.eta),
                "fiber_enumeration_used": False, "joint_purification_sampler": False,
                "target": "actual_decoder_left_computational_output",
                "gibbs_accuracy_assumed": False}

