"""Exact native-word sampling for real-rational transfer-matrix products.

The bond dimension (radius+1)**number_of_factors is charged, not hidden.
These products are not automatically thermal states.
"""

from fractions import Fraction as Q
from itertools import product


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError("explicit int/Fraction coefficients required")
    return Q(value)


class WordSampler:
    def __init__(self, couplings, radius, parameters, *, basis="Z"):
        self.couplings = tuple(exact(j) for j in couplings)
        self.parameters = tuple(exact(u) for u in parameters)
        if len(self.couplings) < 2 or any(not j or abs(j) > 1 for j in self.couplings):
            raise ValueError("need nonzero native couplings of magnitude <=1")
        if type(radius) is not int or not 1 <= radius < len(self.couplings):
            raise ValueError("invalid path radius")
        if basis not in ("Z", "X"):
            raise ValueError("basis must be Z or X")
        self.radius, self.basis = radius, basis
        self.states = tuple(product(range(radius+1), repeat=len(self.parameters)))
        indices = {state: i for i, state in enumerate(self.states)}
        self.bond_dimension = len(self.states)
        self.matrices = []
        for coupling in self.couplings:
            matrices = [[{} for _ in self.states] for _ in range(2)]
            for source, state in enumerate(self.states):
                available = [j for j, age in enumerate(state) if age == 0]
                for mask in range(1 << len(available)):
                    chosen = {available[j] for j in range(len(available)) if mask >> j & 1}
                    destination = indices[tuple(radius if j in chosen else max(0, age-1)
                                                for j, age in enumerate(state))]
                    inversions = sum(age > 0 and p > q for p, age in enumerate(state)
                                     for q in chosen)
                    weight = Q((-1)**inversions)
                    for j in chosen:
                        weight *= -self.parameters[j]*coupling
                    output = len(chosen) % 2
                    row = matrices[output][source]
                    row[destination] = row.get(destination, Q(0))+weight
            if basis == "X":
                transformed = [[{} for _ in self.states] for _ in range(2)]
                for output in range(2):
                    for source in range(self.bond_dimension):
                        for bit in range(2):
                            for destination, value in matrices[bit][source].items():
                                row = transformed[output][source]
                                row[destination] = row.get(destination, Q(0))+(-1)**(output*bit)*value
                matrices = transformed
            self.matrices.append(matrices)
        self.right = self._right_environments()
        self.norm_squared = self.right[0][0][0]
        if self.norm_squared <= 0:
            raise ValueError("transfer product is the zero vector; no sampling distribution")

    def _right_environments(self):
        d = self.bond_dimension
        right = [None]*(len(self.couplings)+1)
        # Any final cooldown is legal. The boundary is ones*ones^T, not I.
        right[-1] = [[Q(1) for _ in range(d)] for _ in range(d)]
        for site in reversed(range(len(self.couplings))):
            after = right[site+1]
            before = [[Q(0) for _ in range(d)] for _ in range(d)]
            for a in range(d):
                for b in range(a, d):
                    value = sum((u*v*after[c][e]
                                 for matrix in self.matrices[site]
                                 for c, u in matrix[a].items()
                                 for e, v in matrix[b].items()), Q(0))
                    before[a][b] = before[b][a] = value
            right[site] = before
        return right

    def _advance(self, row, site, bit):
        answer = {}
        for source, value in row.items():
            for destination, weight in self.matrices[site][bit][source].items():
                answer[destination] = answer.get(destination, Q(0))+value*weight
        return {i: value for i, value in answer.items() if value}

    def amplitude(self, word):
        if len(word) != len(self.couplings) or any(type(b) is not int or b not in (0, 1) for b in word):
            raise ValueError("one bit per native generator required")
        row = {0: Q(1)}
        for site, bit in enumerate(word):
            row = self._advance(row, site, bit)
        return sum(row.values(), Q(0))

    def probability(self, word):
        return self.amplitude(word)**2/self.norm_squared

    def sample(self, rng):
        row, word = {0: Q(1)}, []
        for site in range(len(self.couplings)):
            branches = [self._advance(row, site, bit) for bit in (0, 1)]
            environment = self.right[site+1]
            masses = [sum((a*b*environment[i][j] for i, a in branch.items()
                           for j, b in branch.items()), Q(0)) for branch in branches]
            if min(masses) < 0 or sum(masses) <= 0:
                raise ArithmeticError("invalid exact conditional mass")
            probability_one = masses[1]/sum(masses)
            bit = int(rng.randrange(probability_one.denominator) < probability_one.numerator)
            word.append(bit)
            row = branches[bit]
        return tuple(word)


def repeated_transfer_bound(couplings, beta, factors):
    """Conservative native thermal vector-distance bound for T(beta/(2L))^L."""
    couplings = tuple(exact(j) for j in couplings)
    beta = exact(beta)
    if beta < 0 or type(factors) is not int or factors < 1:
        raise ValueError("need beta>=0 and a positive integer factor count")
    mass = sum((j*j for j in couplings), Q(0))
    if beta**2*mass > factors**2:
        raise ValueError("not certified: beta*sqrt(sum J^2)/(2L) exceeds 1/2")
    return {"transfer_parameter": beta/(2*factors),
            "thermal_squared_vector_error_upper": beta**6*mass**3/(324*factors**4),
            "factor_count": factors, "uniform_efficient_sampler_claim": False}
