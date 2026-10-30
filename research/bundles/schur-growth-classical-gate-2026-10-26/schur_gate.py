"""A matched classical full-support solver and a scoped comparison certificate.

The solver is Ragavan--Shutty (2610.00502), not a new algorithm. The gate
compares their two sufficient guarantees; it is not a quantum lower bound.
Inverse-trace and halfset predicates are intentionally outside this interface.
"""

from fractions import Fraction
from itertools import combinations_with_replacement, product
import random

from flint import fmpz, nmod_mat


def rows(matrix):
    return [[int(matrix[i, j]) for j in range(matrix.ncols())]
            for i in range(matrix.nrows())]


def basis(vectors, p):
    reduced, rank = nmod_mat(vectors, p).rref()
    return rows(reduced)[:rank]


def selected(matrix, columns):
    return nmod_mat([[int(matrix[i, j]) for j in columns]
                     for i in range(matrix.nrows())], matrix.modulus())


def vector(values, p):
    return nmod_mat([[x] for x in values], p)


class FullSupportProblem:
    def __init__(self, p, parity_rows, *, relation):
        if relation != "full_support":
            raise ValueError("only By=s with EVERY y_i != 0; not inverse-trace or halfsets")
        if type(p) is not int or not 3 <= p < 2**63 or not fmpz(p).is_prime():
            raise ValueError("verified odd prime below 2^63 required by this backend")
        data = tuple(tuple(row) for row in parity_rows)
        if not data or not data[0] or any(len(row) != len(data[0]) for row in data):
            raise ValueError("nonempty rectangular parity matrix required")
        if any(type(x) is not int or not 0 <= x < p for row in data for x in row):
            raise ValueError("canonical prime-field entries required")
        self.p, self.k, self.m = p, len(data), len(data[0])
        self.B = nmod_mat(data, p)
        if self.B.rank() != self.k:
            raise ValueError("independent original parity rows required")
        self.V = basis(data, p)
        self.W = basis([[v[i]*w[i] % p for i in range(self.m)]
                        for v, w in combinations_with_replacement(self.V, 2)], p)
        self.U = basis([[v[i]*w[i] % p for i in range(self.m)]
                        for v in self.V for w in self.W], p)
        kernel, nullity = nmod_mat(self.U, p).nullspace()
        self.annihilator = tuple(tuple(int(kernel[i, j]) for i in range(self.m))
                                for j in range(nullity))

    def field_vector(self, values, length):
        values = tuple(values)
        if (len(values) != length
                or any(type(x) is not int or not 0 <= x < self.p for x in values)):
            raise ValueError("canonical vector of the required length expected")
        return values

    def verifies(self, word, syndrome):
        word = self.field_vector(word, self.m)
        syndrome = self.field_vector(syndrome, self.k)
        return all(word) and self.B*vector(word, self.p) == vector(syndrome, self.p)

    def dominance(self, unit=None):
        unit = self.field_vector((1,)*self.m if unit is None else unit, self.m)
        certified_unit = all(unit) and nmod_mat(self.V+[list(unit)], self.p).rank() == self.k
        delta = len(self.U)-len(self.W)
        factor = (Fraction(self.p)**(delta-self.k)/(2*(self.p-1))
                  if certified_unit else None)
        covered = certified_unit and factor <= 1
        return {"status": "CLASSICAL_COVERS_THIS_QUANTUM_CRITERION" if covered else
                "NO_DOMINANCE_CERTIFICATE_NOT_ADVANTAGE",
                "rank": self.k, "length": self.m, "square_dimension": len(self.W),
                "cube_dimension": len(self.U), "multiplication_growth": delta,
                "public_unit_verified": bool(certified_unit),
                "classical_bound_over_quantum_bound_upper": factor,
                "quantum_advantage_established": False}

    def quantum_bound_floor(self):
        """A lower bound on the published Q expression, NOT on actual failure."""
        return 2*(self.p**self.k-1)*Fraction(self.p)**(self.k+len(self.W)-self.m)

    def shortened_dimension(self, space, zero_positions):
        if not zero_positions:
            return len(space)
        return len(space)-selected(nmod_mat(space, self.p), zero_positions).rank()

    def exact_bounds(self):
        """Exponential diagnostic, refused above 4096 codewords."""
        if self.p**self.k > 4096:
            raise ValueError("exact enumeration cap: use a proved symbolic quantum bound")
        quantum_sum, classical_sum = Fraction(0), Fraction(0)
        distance = self.m
        for coefficients in product(range(self.p), repeat=self.k):
            if not any(coefficients):
                continue
            word = [sum(c*v[i] for c, v in zip(coefficients, self.V)) % self.p
                    for i in range(self.m)]
            zeros = [i for i, x in enumerate(word) if x == 0]
            weight = self.m-len(zeros)
            distance = min(distance, weight)
            sw, su = (self.shortened_dimension(space, zeros) for space in (self.W, self.U))
            quantum_sum += Fraction(self.p**sw, (self.p-1)**weight)
            classical_sum += Fraction(self.p)**(su-weight)
        return {"quantum_failure_expression": 2*self.p**self.k*quantum_sum,
                "classical_failure_bound": classical_sum/(self.p-1),
                "minimum_distance": distance, "codewords_enumerated": self.p**self.k,
                "expressions_are_not_actual_failure_probabilities": True}

    def from_annihilator(self, syndrome, h, nonsquare):
        """One checked constructive attempt. Failed rank is not UNSAT."""
        p, B = self.p, self.B
        syndrome = self.field_vector(syndrome, self.k)
        h = self.field_vector(h, self.m)
        if (type(nonsquare) is not int or not 0 < nonsquare < p
                or pow(nonsquare, (p-1)//2, p) != p-1):
            raise ValueError("a verified nonsquare is required")
        if any(sum(u[i]*h[i] for i in range(self.m)) % p for u in self.U):
            raise ValueError("h must annihilate the full Schur cube")
        support = [i for i, x in enumerate(h) if x]
        if not support:
            return {"status": "RETRY_RANK", "witness": None, "support_size": 0}
        T = selected(B, support)
        reduced, rank = T.rref()
        if rank < self.k:
            return {"status": "RETRY_RANK", "witness": None, "support_size": len(support)}
        pivots = [next(j for j in range(len(support)) if reduced[i, j])
                  for i in range(self.k)]
        pivot_set = set(pivots)
        w = [int(j in pivot_set) for j in range(len(support))]
        inv4 = pow(4, -1, p)
        y0 = [(w[j]*pow(h[i], -1, p)-nonsquare*h[i])*inv4 % p
              for j, i in enumerate(support)]
        outside = [i for i in range(self.m) if not h[i]]
        rhs = [(syndrome[r]-sum(int(B[r, i]) for i in outside)
                -sum(int(T[r, j])*y0[j] for j in range(len(support))))*2 % p
               for r in range(self.k)]
        I = selected(T, pivots)
        z = (I*I.transpose()).inv()*vector(rhs, p)
        u = T.transpose()*z
        word = [1]*self.m
        for j, i in enumerate(support):
            shifted = (int(u[j, 0])+w[j]*pow(h[i], -1, p)) % p
            word[i] = h[i]*(shifted*shifted-nonsquare)*inv4 % p
        if not self.verifies(word, syndrome):
            raise ArithmeticError("constructed word failed the ORIGINAL input relation")
        return {"status": "VERIFIED_FULL_SUPPORT_WITNESS", "witness": word,
                "support_size": len(support), "pivot_columns": [support[j] for j in pivots],
                "uniform_witness_sampling": False, "algorithm_is_prior_art": True}

    def solve(self, syndrome, nonsquare, *, seed, attempts=8):
        syndrome = self.field_vector(syndrome, self.k)
        if type(attempts) is not int or attempts < 1:
            raise ValueError("positive attempt cap required")
        rng = random.Random(seed)
        for attempt in range(1, attempts+1):
            coefficients = [rng.randrange(self.p) for _ in self.annihilator]
            h = [sum(a*v[i] for a, v in zip(coefficients, self.annihilator)) % self.p
                 for i in range(self.m)]
            result = self.from_annihilator(syndrome, h, nonsquare)
            if result["witness"] is not None:
                return dict(result, attempts=attempt, field_draws=attempt*len(self.annihilator))
        return {"status": "UNKNOWN_ATTEMPT_CAP", "witness": None, "attempts": attempts,
                "field_draws": attempts*len(self.annihilator), "hardness_evidence": False}

    def deterministic_attempt(self, syndrome, nonsquare):
        """Try the first kernel basis vector; no curve promise is inferred."""
        h = self.annihilator[0] if self.annihilator else (0,)*self.m
        result = self.from_annihilator(syndrome, h, nonsquare)
        if result["witness"] is None:
            result = dict(result, status="UNKNOWN_FIRST_ANNIHILATOR", hardness_evidence=False)
        return dict(result, attempts=1, field_draws=0, annihilator=list(h))
