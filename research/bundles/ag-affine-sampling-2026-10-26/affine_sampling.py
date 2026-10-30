"""Matched classical full-support sampling with conditional moment bounds.

The matrix sampler needs no curve metadata. A Bonferroni number alone does
not verify the required dual-distance or t-wise-independence hypothesis.
"""

from fractions import Fraction
from math import comb
import random

from flint import fmpz, nmod_mat


def bonferroni_bound(length, alphabet_size, independence_order):
    if (type(length) is not int or length < 1 or type(alphabet_size) is not int
            or alphabet_size < 2 or type(independence_order) is not int
            or not 0 <= independence_order <= length):
        raise ValueError("positive length/alphabet and valid independence order required")
    partial, best, best_order = Fraction(1), Fraction(0), 0
    for j in range(1, independence_order+1):
        partial += Fraction((-1)**j*comb(length, j), alphabet_size**j)
        if j % 2 and partial > best:
            best, best_order = partial, j
    return {"success_lower": best, "odd_order_used": best_order,
            "expected_trials_upper": 1/best if best else None,
            "requires_uniform_marginals_through_order": independence_order,
            "independence_verified_by_this_helper": False,
            "quantum_advantage_established": False}


class AffineFiber:
    def __init__(self, prime, parity_rows, *, relation):
        if relation != "full_support":
            raise ValueError("only original By=s with every y_i nonzero")
        if type(prime) is not int or not 3 <= prime < 2**63 or not fmpz(prime).is_prime():
            raise ValueError("verified odd prime below 2^63 required")
        data = tuple(tuple(row) for row in parity_rows)
        if not data or not data[0] or any(len(row) != len(data[0]) for row in data):
            raise ValueError("nonempty rectangular matrix required")
        if any(type(x) is not int or not 0 <= x < prime for row in data for x in row):
            raise ValueError("canonical field entries required")
        self.p, self.k, self.m = prime, len(data), len(data[0])
        self.B = nmod_mat(data, prime)
        reduced, rank = self.B.rref()
        if rank != self.k:
            raise ValueError("original parity rows must be independent")
        self.pivots = [next(j for j in range(self.m) if reduced[i, j])
                       for i in range(self.k)]
        pivot_matrix = nmod_mat([[int(self.B[i, j]) for j in self.pivots]
                                 for i in range(self.k)], prime)
        self.pivot_inverse = pivot_matrix.inv()
        nullspace, nullity = self.B.nullspace()
        self.kernel = tuple(tuple(int(nullspace[i, j]) for i in range(self.m))
                            for j in range(nullity))

    def checked(self, values, length):
        values = tuple(values)
        if len(values) != length or any(type(x) is not int or not 0 <= x < self.p
                                        for x in values):
            raise ValueError("canonical vector of required length expected")
        return values

    def particular(self, syndrome):
        syndrome = self.checked(syndrome, self.k)
        answer = self.pivot_inverse*nmod_mat([[x] for x in syndrome], self.p)
        word = [0]*self.m
        for j, position in enumerate(self.pivots):
            word[position] = int(answer[j, 0])
        return word

    def fiber_word(self, particular, coefficients):
        particular = self.checked(particular, self.m)
        coefficients = self.checked(coefficients, len(self.kernel))
        return [(particular[i]+sum(a*v[i] for a, v in zip(coefficients, self.kernel))) % self.p
                for i in range(self.m)]

    def verifies(self, word, syndrome):
        word, syndrome = self.checked(word, self.m), self.checked(syndrome, self.k)
        return all(word) and all(sum(int(self.B[r, i])*word[i] for i in range(self.m)) % self.p
                                == syndrome[r] for r in range(self.k))

    def sample(self, syndrome, *, seed, attempts=128):
        syndrome = self.checked(syndrome, self.k)
        if type(attempts) is not int or attempts < 1 or type(seed) is not int:
            raise ValueError("positive integer cap and integer replay seed required")
        particular = self.particular(syndrome)
        rng = random.Random(seed)
        for attempt in range(1, attempts+1):
            coefficients = [rng.randrange(self.p) for _ in self.kernel]
            word = self.fiber_word(particular, coefficients)
            if all(word):
                if not self.verifies(word, syndrome):
                    raise ArithmeticError("sample failed the ORIGINAL parity equation")
                return {"status": "VERIFIED_FULL_SUPPORT_WITNESS", "witness": word,
                        "attempts": attempt, "field_draws": attempt*len(self.kernel),
                        "ideal_conditional_law": "uniform_on_original_full_support_fiber",
                        "seeded_replay_is_not_distributional_evidence": True}
        return {"status": "UNKNOWN_ATTEMPT_CAP", "witness": None, "attempts": attempts,
                "field_draws": attempts*len(self.kernel), "hardness_evidence": False}
