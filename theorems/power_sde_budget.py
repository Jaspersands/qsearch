"""Finite randomness budget for the symmetric SDE, not a quantum clock proof.

Prime validation and deterministic arithmetic have separate dependencies.
All stochastic loops in this mode are capped, including integer rejection
and polynomial-root splitting. No new root-finding algorithm is claimed.
"""
from dataclasses import dataclass
from fractions import Fraction
import random

from theorems.nil3_guarded_cyclic_dispatch import independent_columns_exact
from theorems.power_sde import PowerWitness, power_arity, power_weights, validate_family


class RandomnessExhausted(RuntimeError):
    """A declared stochastic cap, not malformed input or a backend failure."""


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")


def _ceil_log2(value):
    _positive(value, "logarithm input")
    return (value-1).bit_length()


@dataclass(frozen=True)
class RandomnessBudget:
    rank: int
    degree: int
    failure_bits: int
    root_call_cap: int
    internal_bits: int
    generator_attempt_cap: int
    root_split_attempt_cap: int
    uniform_call_cap: int
    integer_rejection_cap: int
    algebraic_sampling_abort_bound: Fraction
    integer_sampling_abort_bound: Fraction

    @property
    def total_abort_bound(self):
        return self.algebraic_sampling_abort_bound+self.integer_sampling_abort_bound


def randomness_budget(rank, degree, failure_bits=32, *, first_level_width=None):
    power_arity(rank, degree)
    _positive(failure_bits, "failure_bits")
    width = rank+1 if first_level_width is None else first_level_width
    if type(width) is not int or width < rank+1:
        raise ValueError("first-level width must be at least rank+1")
    blocks = (degree-1)*rank+1
    roots = blocks*(width+2)+degree*(degree+1)//2 if rank else 0
    union_terms = degree+roots*(degree-1)
    bits = failure_bits+1+_ceil_log2(union_terms)
    generator_cap, split_cap = degree*bits, 3*bits
    scalar_calls = sum(2*degree**k*bits for k in range(2, degree+1))
    calls = generator_cap+scalar_calls+roots*degree*(degree-1)*split_cap
    rejection_cap = failure_bits+1+_ceil_log2(calls)
    result = RandomnessBudget(rank, degree, failure_bits, roots, bits,
                              generator_cap, split_cap, calls, rejection_cap,
                              Fraction(union_terms, 2**bits), Fraction(calls, 2**rejection_cap))
    if result.total_abort_bound > Fraction(1, 2**failure_bits):
        raise ArithmeticError("failure budget allocation exceeded the request")
    return result


class CappedUniformRandom:
    """Uniform accepted integer draws with finite bit/call budgets.

    Guarantees assume fresh uniform getrandbits output. Injecting a seeded
    or adversarial source does not certify this distributional assumption.
    """

    def __init__(self, bit_source, *, call_cap, rejection_cap, max_interval):
        for value, name in ((call_cap, "call_cap"), (rejection_cap, "rejection_cap"),
                            (max_interval, "max_interval")):
            _positive(value, name)
        if not callable(getattr(bit_source, "getrandbits", None)):
            raise ValueError("bit source must provide getrandbits")
        self.bit_source = bit_source
        self.call_cap, self.rejection_cap, self.max_interval = call_cap, rejection_cap, max_interval
        self.calls, self.bit_draws, self.random_bits = 0, 0, 0

    def randrange(self, start, stop):
        if type(start) is not int or type(stop) is not int or not 0 < stop-start <= self.max_interval:
            raise ValueError("integer interval exceeds the configured range")
        if self.calls >= self.call_cap:
            raise RuntimeError("bounded uniform-integer call cap exhausted")
        self.calls += 1
        width = stop-start
        bits = (width-1).bit_length()
        if not bits:
            return start
        for _ in range(self.rejection_cap):
            value = self.bit_source.getrandbits(bits)
            self.bit_draws += 1
            self.random_bits += bits
            if type(value) is not int or not 0 <= value < 2**bits:
                raise ValueError("bit source returned a noncanonical bit string")
            if value < width:
                return start+value
        raise RandomnessExhausted("bounded uniform-integer rejection cap exhausted")


@dataclass(frozen=True)
class BudgetedPowerWitness:
    witness: PowerWitness
    budget: RandomnessBudget
    root_calls: int
    root_split_trials: int
    root_proper_splits: int
    uniform_calls: int
    bit_draws: int
    random_bits: int


def budgeted_power_weights(prime, degree, columns, *, failure_bits=32, bit_source=None,
                           first_level_width=None, first_level_relations=None):
    """Same arithmetic witness with total RANDOMNESS exhaustion <=2^-failure_bits.

    Exceptions/ABORT are retained, never retried by this wrapper. Library
    primality validation and deterministic arithmetic are not timed here.
    """
    from theorems.bounded_power_roots import bounded_power_root
    validate_family(prime, degree)
    _, rank = independent_columns_exact(columns, prime)
    budget = randomness_budget(rank, degree, failure_bits, first_level_width=first_level_width)
    source = random.SystemRandom() if bit_source is None else bit_source
    rng = CappedUniformRandom(source, call_cap=budget.uniform_call_cap,
                             rejection_cap=budget.integer_rejection_cap, max_interval=prime)
    root_calls = split_trials = proper_splits = 0

    def root_solver(p, d, value):
        nonlocal root_calls, split_trials, proper_splits
        if (p, d) != (prime, degree) or root_calls >= budget.root_call_cap:
            raise ArithmeticError("root-call budget or field invariant violated")
        root_calls += 1
        result = bounded_power_root(p, d, value, rng=rng,
                                    split_attempt_cap=budget.root_split_attempt_cap)
        split_trials += result.split_trials
        proper_splits += result.proper_splits
        if result.root is None:
            raise RandomnessExhausted("bounded root splitting exhausted")
        return result.root

    try:
        witness = power_weights(prime, degree, columns, rng=rng,
                                generator_attempt_cap=budget.generator_attempt_cap,
                                sampler_bits=budget.internal_bits, root_solver=root_solver,
                                first_level_width=first_level_width,
                                first_level_relations=first_level_relations)
    except RuntimeError as error:
        if (str(error) == "bounded power-coset generator sampler exhausted"
                or str(error).startswith("bounded symmetric scalar sampler exhausted at stage ")):
            raise RandomnessExhausted(str(error)) from error
        raise
    if root_calls != witness.root_calls:
        raise ArithmeticError("root-call accounting mismatch")
    return BudgetedPowerWitness(witness, budget, root_calls, split_trials, proper_splits,
                                rng.calls, rng.bit_draws, rng.random_bits)


def report():
    cases = []
    for prime, degree, rank in ((2**61-1, 5, 8), (2**128-275, 4, 3), (65537, 2, 3)):
        fixture = random.Random(20261028)
        count = power_arity(rank, degree)
        columns = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
        columns += [tuple(fixture.randrange(prime) for _ in range(rank)) for _ in range(count-rank)]
        result = budgeted_power_weights(prime, degree, columns, bit_source=random.Random(928))
        budget = result.budget
        cases.append(dict(prime=prime, degree=degree, rank=rank, columns=count,
                          root_calls=result.root_calls, root_call_cap=budget.root_call_cap,
                          root_split_trials=result.root_split_trials,
                          root_split_trial_cap=budget.root_call_cap*(degree-1)*budget.root_split_attempt_cap,
                          root_proper_splits=result.root_proper_splits,
                          uniform_calls=result.uniform_calls, uniform_call_cap=budget.uniform_call_cap,
                          bit_draws=result.bit_draws,
                          bit_draw_cap=budget.uniform_call_cap*budget.integer_rejection_cap,
                          random_bits=result.random_bits,
                          random_bit_cap=budget.uniform_call_cap*budget.integer_rejection_cap*(prime-1).bit_length(),
                          total_sampling_abort_bound=str(budget.total_abort_bound),
                          requested_failure_bound=str(Fraction(1, 2**budget.failure_bits)),
                          exact_original_moment_verified=True))
    return dict(status="BOUNDED_RANDOMNESS_NOT_FULL_RECEIVER_CLOCK",
                proof_note="research/POWER_SDE_RANDOMNESS_BUDGET.md", cases=cases,
                every_randomized_loop_capped=True, input_labels_resampled=False,
                root_factorization_black_box_used=False, field_enumeration_used=False,
                fixed_degree_required=True, prime_validation_locally_clocked=False,
                deterministic_arithmetic_step_counter=False, os_wallclock_bound=False,
                formal_total_policy_instantiated=False, quantum_receiver_implemented=False,
                novelty_established=False, speedup_claim_allowed=False)
