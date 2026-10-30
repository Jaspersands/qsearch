"""Systematic rejection for the original explicit full-support relation.

Distance-based numbers are conditional certificates, never verified promises.
The existing frozen affine sampler supplies matrix and native verification APIs.
"""

from fractions import Fraction
from pathlib import Path
import random
import sys

from flint import fmpz, nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "ag-affine-sampling-2026-10-26"))
from affine_sampling import AffineFiber


def distance_bound(prime, length, rank, delta):
    if (type(prime) is not int or not 3 <= prime < 2**63
            or not fmpz(prime).is_prime()):
        raise ValueError("odd prime below 2^63 required")
    if (any(type(x) is not int for x in (length, rank, delta))
            or not 1 <= rank <= length or not 1 <= delta <= length):
        raise ValueError("positive length, full row rank and distance required")
    alpha = Fraction(prime**rank-1, (prime-1)**delta)
    pivot_factor = Fraction(prime-1, prime)**rank
    success = max(Fraction(0), pivot_factor*(1-alpha))
    return {
        "tail_upper": alpha,
        "systematic_success_lower": success,
        "affine_success_lower": max(Fraction(0),
                                     Fraction(prime-1, prime)**length*(1-alpha)),
        "expected_trials_upper": 1/success if success else None,
        "exact_success_ratio_if_nonempty": Fraction(prime, prime-1)**(length-rank),
        "distance_promise": delta,
        "distance_verified_by_helper": False,
        "quantum_advantage_established": False,
    }


class SystematicFiber(AffineFiber):
    def __init__(self, prime, parity_rows, *, relation):
        super().__init__(prime, parity_rows, relation=relation)
        pivot_set = set(self.pivots)
        self.free = tuple(j for j in range(self.m) if j not in pivot_set)
        self.transition = self.pivot_inverse * nmod_mat(
            self.k, len(self.free),
            [int(self.B[i, j]) for i in range(self.k) for j in self.free], self.p)

    def from_free(self, syndrome, values):
        syndrome = self.checked(syndrome, self.k)
        values = self.checked(values, len(self.free))
        if not all(values):
            raise ValueError("systematic proposals require nonzero free coordinates")
        return self._complete(self.particular(syndrome), values)

    def _complete(self, particular, values):
        word = list(particular)
        for j, value in zip(self.free, values):
            word[j] = value
        for i, position in enumerate(self.pivots):
            word[position] = (word[position] - sum(
                int(self.transition[i, j])*value for j, value in enumerate(values))) % self.p
        return word

    def sample(self, syndrome, *, seed, attempts=128):
        syndrome = self.checked(syndrome, self.k)
        if type(attempts) is not int or attempts < 1 or type(seed) is not int:
            raise ValueError("positive integer cap and integer replay seed required")
        particular = self.particular(syndrome)
        rng = random.Random(seed)
        for attempt in range(1, attempts+1):
            values = [rng.randrange(1, self.p) for _ in self.free]
            word = self._complete(particular, values)
            if all(word):
                if not self.verifies(word, syndrome):
                    raise ArithmeticError("proposal failed ORIGINAL Bz=s")
                return {
                    "status": "VERIFIED_FULL_SUPPORT_WITNESS", "witness": word,
                    "attempts": attempt, "field_draws": attempt*len(self.free),
                    "ideal_conditional_law": "uniform_on_original_full_support_fiber",
                    "seeded_replay_is_not_distributional_evidence": True,
                }
        return {"status": "UNKNOWN_ATTEMPT_CAP", "witness": None,
                "attempts": attempts, "field_draws": attempts*len(self.free),
                "hardness_evidence": False}
