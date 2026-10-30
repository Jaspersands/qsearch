"""Matrix-only classical sparse-error decoding using a Schur locator.

This is NOT a classical solver for By=s with y nonzero. Its coherent version
is an ingredient of the existing ordinary decoding-based quantum reduction.
"""

from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb

from flint import fmpz, nmod_mat


def rows(matrix):
    return [[int(matrix[i, j]) for j in range(matrix.ncols())]
            for i in range(matrix.nrows())]


def row_basis(data, p):
    reduced, rank = nmod_mat(data, p).rref()
    return rows(reduced)[:rank]


class SchurLocator:
    def __init__(self, p, generator):
        if type(p) is not int or not 3 <= p < 2**63 or not fmpz(p).is_prime():
            raise ValueError("verified odd prime below2^63 required")
        data = [list(row) for row in generator]
        if (not data or not data[0] or any(len(row) != len(data[0]) for row in data)
                or any(type(x) is not int or not 0 <= x < p for row in data for x in row)):
            raise ValueError("nonempty canonical rectangular generator required")
        self.p, self.k, self.m = p, len(data), len(data[0])
        self.B = nmod_mat(data, p)
        if self.B.rank() != self.k:
            raise ValueError("independent rows required")
        self.W = row_basis([[a[i]*b[i] % p for i in range(self.m)]
                            for a, b in combinations_with_replacement(data, 2)], p)
        kernel, nullity = nmod_mat(self.W, p).nullspace()
        self.check = (nmod_mat([[int(kernel[i, j]) for i in range(self.m)]
                               for j in range(nullity)], p) if nullity
                      else nmod_mat(0, self.m, p))

    def encode(self, message):
        message = self._vector(message, self.k)
        return [int(x) for x in (nmod_mat([message], self.p)*self.B).entries()]

    def _vector(self, values, size):
        values = list(values)
        if len(values) != size or any(type(x) is not int or not 0 <= x < self.p for x in values):
            raise ValueError("canonical vector of required size expected")
        return values

    def decode(self, received, radius):
        r = self._vector(received, self.m)
        if type(radius) is not int or not 0 <= radius <= self.m:
            raise ValueError("bounded nonnegative integer radius required")
        multiplied = nmod_mat([[int(self.B[j, i])*r[i] % self.p for i in range(self.m)]
                               for j in range(self.k)], self.p)
        constraint = self.check * multiplied.transpose()
        kernel, dimension = constraint.nullspace()
        if not dimension:
            return {"status": "FAIL_NO_LOCATOR", "word": None}
        coefficients = [int(kernel[i, 0]) for i in range(self.k)]
        locator = self.encode(coefficients)
        support = [i for i, a in enumerate(locator) if a]
        equations = nmod_mat([[int(self.B[j, i]) for j in range(self.k)] for i in support], self.p)
        if equations.rank() != self.k:
            return {"status": "FAIL_NONUNIQUE_ERASURES", "word": None}
        augmented = nmod_mat([row + [r[i]] for row, i in zip(rows(equations), support)], self.p)
        reduced, rank = augmented.rref()
        if rank != self.k:
            return {"status": "FAIL_INCONSISTENT_ERASURES", "word": None}
        message = [int(reduced[i, self.k]) for i in range(self.k)]
        word = self.encode(message)
        errors = [i for i in range(self.m) if word[i] != r[i]]
        if len(errors) > radius:
            return {"status": "FAIL_OUTSIDE_RADIUS", "word": None}
        return {"status": "VERIFIED_CODEWORD_WITHIN_RADIUS", "word": word,
                "message_in_original_basis": message, "error_positions": errors,
                "locator": locator, "locator_solution_dimension": dimension,
                "uniqueness_requires_distance_promise": True,
                "full_support_search_solved_classically": False}


def native_bounds(e, p=1019):
    """Analytic AG promises, not a generator or a matrix-distance certificate."""
    if type(e) is not int or e < 8 or p != 1019:
        raise ValueError("stated p1019 family, e>=8 only")
    m, k, d = 22*e, 5*e+3, 10*e+3
    dv, dw = m-d, m-2*d
    t = min(k-1, dw-1)
    if not t >= 0 or not 2*dv > m:
        raise ArithmeticError("locator promises fail")
    tail = min(Fraction(1), Fraction(comb(m, t+1), p**(t+1)))
    alpha = Fraction(p**k-1, (p-1)**dv)
    success = max(Fraction(0), (1-alpha)*(1-tail))
    return {"prime": p, "cover_degree": e, "m": m, "k": k,
            "divisor_degree": d, "V_distance_lower": dv,
            "W_distance_lower": dw, "classical_decode_radius": t,
            "expected_basis_error_weight": Fraction(m, p),
            "truncated_source_failure_upper": tail,
            "normalization_tail_upper": alpha,
            "ordinary_DQI_raw_verified_success_lower": success,
            "ideal_verified_output_exactly_uniform": True,
            "requires_complete_AG_distance_promises": True,
            "higher_input_generated": False,
            "classical_full_support_solver_claimed": False}
