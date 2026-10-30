"""Known Cantor-Zassenhaus splitting with explicitly capped random trials.

Precondition: p is an odd PRIME. This module does not validate primality.
For d >= 2 dividing p-1 and a nonzero dth power a, X**d-a has d distinct
roots in F_p. Evaluation at the m distinct roots of a current factor is a
Vandermonde bijection, so m independent uniform coefficients give independent
uniform evaluations. The nonzero-square class has mass q = (p-1)/(2*p);
zero belongs to its complement. Thus a trial splits properly with probability
1-q**m-(1-q)**m >= 2*q*(1-q) >= 4/9 > 1/3 for m >= 2.

At most d-1 proper descents occur. With K attempts per stage the union abort
bound is (d-1)*(2/3)**K, conditional on independent uniform RNG outputs.
There are at most (d-1)*K deterministic polynomial pow_mod/gcd pairs and
K*(d*(d+1)//2-1) field draws, plus deterministic setup and scalar power checks.
These are operation/random-loop bounds, NOT an OS wall-clock deadline or a
bound on the supplied RNG's internal bit rejection. External primality
validation, global error budgets, and downstream quantum correctness are
outside this classical primitive. This is not a novelty or speedup claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from flint import fq_default_ctx, fq_default_poly_ctx


@dataclass(frozen=True)
class BoundedPowerRoot:
    """A verified root, or root=None when a stage exhausts its attempt cap.

    Counts are actual work on this call. abort_bound is the a priori,
    unclipped union bound under the stated randomness/prime promises, even
    when a root is found; it does not certify the supplied RNG's distribution.
    """

    root: int | None
    split_trials: int
    proper_splits: int
    random_field_elements: int
    abort_bound: Fraction


def bounded_power_root(p, d, a, *, rng, split_attempt_cap=64):
    """Return a bounded classical dth-root sample under the prime promise.

    Inputs must be Python integers (not bool), with 1 <= a < p. A failed
    power-residue check or malformed RNG output raises ValueError. rng must
    supply randrange(0, p); RNG exceptions propagate without retry, allowing
    the caller to enforce its own bit budget. Uniformity/independence cannot
    be checked here. A cap exhaustion returns a result with root=None.
    Every returned integer root is verified by exact modular exponentiation.
    """
    if type(p) is not int or p < 3 or p % 2 == 0:
        raise ValueError("p must be an odd integer >= 3; primality is a precondition")
    if type(d) is not int or not 2 <= d < p or (p-1) % d:
        raise ValueError("d must be an integer >= 2 dividing p-1")
    if type(a) is not int or not 1 <= a < p:
        raise ValueError("a must be a nonzero canonical field integer")
    if type(split_attempt_cap) is not int or split_attempt_cap < 1:
        raise ValueError("split_attempt_cap must be a positive integer")
    randrange = getattr(rng, "randrange", None)
    if isinstance(rng, type) or not callable(randrange):
        raise ValueError("rng must supply a callable randrange(0, p)")
    if pow(a, (p-1)//d, p) != 1:
        raise ValueError("a is not a certified dth-power residue")

    # fmpz_mod_poly_ctx(p) implicitly tests primality in python-flint 0.9.
    # Force the prime-field backend: no prime test or extension-field search.
    field = fq_default_ctx(p, 1, fq_type="FMPZ_MOD", check_prime=False)
    ring = fq_default_poly_ctx(field)
    factor = ring([-a]+[0]*(d-1)+[1])
    abort_bound = (d-1)*Fraction(2, 3)**split_attempt_cap
    split_trials = proper_splits = random_field_elements = 0

    for _stage in range(d-1):
        m = factor.degree()
        if m == 1:
            break
        for _trial in range(split_attempt_cap):
            coefficients = []
            for _coefficient in range(m):
                value = randrange(0, p)
                if type(value) is not int or not 0 <= value < p:
                    raise ValueError("rng returned a noncanonical field integer")
                coefficients.append(value)
                random_field_elements += 1
            split_trials += 1
            h = ring(coefficients)
            candidate = factor.gcd(h.pow_mod((p-1)//2, factor)-1)
            if 0 < candidate.degree() < m:
                factor = candidate
                proper_splits += 1
                break
        else:
            return BoundedPowerRoot(None, split_trials, proper_splits,
                                    random_field_elements, abort_bound)

    if factor.degree() != 1 or int(factor[1]) != 1:
        raise ArithmeticError("arithmetic backend did not return a monic linear factor")
    root = -int(factor[0]) % p
    if not 0 < root < p or pow(root, d, p) != a:
        raise ArithmeticError("arithmetic backend returned an invalid root")
    return BoundedPowerRoot(root, split_trials, proper_splits,
                            random_field_elements, abort_bound)
