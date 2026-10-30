"""Uniform BCH arithmetic and scalar-line Rees resource bounds.

These are public algebra/resource controls, NOT an HSP receiver or diagonal
equation solver. The caller supplies a genuine Lie bracket over a verified
prime field and a valid nilpotency-class bound below the characteristic.
Shape checks do not certify those mathematical promises. No field table,
free-Lie word expansion, hidden subgroup, or cloud-offloaded import is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial, gcd
from typing import Callable, Sequence


Vector = tuple[int, ...]
Bracket = Callable[[Vector, Vector], Sequence[int]]


def _field_contract(prime: int, nilpotency_class: int) -> None:
    if type(prime) is not int or prime < 2:
        raise ValueError("a supplied verified prime is required")
    if (type(nilpotency_class) is not int
            or not 1 <= nilpotency_class < prime):
        raise ValueError("require 1 <= nilpotency_class < prime")


def _vector(value: Sequence[int], dimension: int, prime: int) -> Vector:
    result = tuple(value)
    if len(result) != dimension or any(
        type(x) is not int or not 0 <= x < prime for x in result
    ):
        raise ValueError("canonical field vector of the stated dimension required")
    return result


def inverse_left_dexp_coefficients(prime: int, nilpotency_class: int) -> Vector:
    """Coefficients of z/(1-exp(-z)) modulo z**c, with c < prime.

    The inverse power-series recurrence only divides by integers at most c.
    Primality is an input promise, not inferred from invertible denominators.
    """
    _field_contract(prime, nilpotency_class)
    factorial = 1
    f = []
    for k in range(nilpotency_class):
        factorial = factorial * (k + 1) % prime
        f.append((-1)**k * pow(factorial, -1, prime) % prime)
    b = [1]
    for k in range(1, nilpotency_class):
        b.append(-sum(f[j] * b[k-j] for j in range(1, k+1)) % prime)
    return tuple(b)


def bch_via_ode(
    x: Sequence[int], y: Sequence[int], *, prime: int,
    nilpotency_class: int, bracket: Bracket,
) -> Vector:
    """Return log(exp(x) exp(y)) for the promised class-<p Lie algebra.

    Solve Z'=ad_Z/(1-exp(-ad_Z)) y, Z(0)=x, coefficientwise through
    degree c. Polynomial bracket convolution avoids enumerating Lie words.
    At most (c-1)*c*(c+1)*(c+2)/6 calls to the supplied bracket are made.
    An understated class or a non-Lie callback can give a wrong answer;
    callers must obtain the class from validated public structure constants.
    """
    coefficients = inverse_left_dexp_coefficients(prime, nilpotency_class)
    x = tuple(x)
    if not x:
        raise ValueError("positive vector dimension required")
    dimension = len(x)
    x, y = _vector(x, dimension, prime), _vector(y, dimension, prime)
    zero = (0,) * dimension
    z = [x]
    for degree in range(nilpotency_class):
        ad = [y] + [zero] * degree
        rhs = list(ad[degree])
        for power in range(1, nilpotency_class):
            next_ad = []
            for order in range(degree + 1):
                total = [0] * dimension
                for i in range(order + 1):
                    value = _vector(bracket(z[i], ad[order-i]), dimension, prime)
                    for j, entry in enumerate(value):
                        total[j] += entry
                next_ad.append(tuple(entry % prime for entry in total))
            ad = next_ad
            weight = coefficients[power]
            rhs = [(a + weight*b) % prime for a, b in zip(rhs, ad[degree])]
        inverse = pow(degree + 1, -1, prime)
        z.append(tuple(inverse * entry % prime for entry in rhs))
    return tuple(sum(row[i] for row in z) % prime for i in range(dimension))


def lift_scalar_witness(
    labels: Sequence[int], witness: Sequence[int], *, prime: int, degree: int,
) -> Vector:
    """Check a gcd(d,p-1)-power witness and lift it to a d-power witness.

    This verifies/converts an existing witness; it does not find one.
    Zero entries stay zero, even when the reduced exponent inverse is zero.
    """
    _field_contract(prime, degree)
    labels = tuple(labels)
    labels = _vector(labels, len(labels), prime)
    witness = _vector(witness, len(labels), prime)
    delta = gcd(degree, prime-1)
    if not any(witness) or sum(a*pow(x, delta, prime) for a, x in zip(labels, witness)) % prime:
        raise ValueError("a nonzero valid reduced-power witness is required")
    exponent = pow(degree // delta, -1, (prime-1) // delta)
    return tuple(pow(x, exponent, prime) if x else 0 for x in witness)


@dataclass(frozen=True)
class ScalarLineStage:
    grade: int
    line: int
    arity: int
    conversions: int
    consumed_targets: int


@dataclass(frozen=True)
class ScalarLineBudget:
    lower_central_dimensions: tuple[int, ...]
    terminal_samples: int
    prime: int | None
    cover_dimension: int
    lifted_sources: int
    original_inputs: int
    scalar_solves: int
    central_character_measurements: int
    stages: tuple[ScalarLineStage, ...]

    @property
    def derived_dimension(self) -> int:
        return self.lower_central_dimensions[1] if len(self.lower_central_dimensions) > 1 else 0

    @property
    def leaves_per_terminal(self) -> int:
        return self.lifted_sources // self.terminal_samples

    @property
    def derived_parameter_leaf_bound(self) -> int:
        r = self.derived_dimension
        return (r + 2)**(r * (r + 1) // 2)


def scalar_line_budget(
    lower_central_dimensions: Sequence[int], terminal_samples: int, *, prime: int | None = None,
) -> ScalarLineBudget:
    """Worst-case fresh-source tree, using d+1 inputs per grade-d line.

    The profile is (dim L, dim gamma_2, ..., dim gamma_c), without trailing
    zeros. Necessary profile checks are not a Lie-algebra existence proof.
    Each conversion calls a published scalar diagonal solver once and
    consumes/measures ALL its d+1 targets, including zero-scale branches.
    With a supplied verified prime, arity is gcd(d,p-1)+1 instead of d+1.
    Initial lift calls consume c ordinary f queries OR c original copies.
    State preparation, gates, final Fourier sampling and errors remain paid
    separately; this function does not claim to count them as scalar solves.
    """
    dimensions = tuple(lower_central_dimensions)
    if not dimensions or any(type(x) is not int or x < 1 for x in dimensions):
        raise ValueError("positive lower-central dimensions without trailing zero required")
    if any(a <= b for a, b in zip(dimensions, dimensions[1:])):
        raise ValueError("nonzero lower-central dimensions must strictly decrease")
    if len(dimensions) > 1 and dimensions[0] - dimensions[1] < 2:
        raise ValueError("nonabelian nilpotent Lie algebra needs abelianization dimension >= 2")
    if type(terminal_samples) is not int or terminal_samples < 1:
        raise ValueError("positive integer terminal sample count required")
    if prime is not None:
        _field_contract(prime, len(dimensions))
    need = terminal_samples
    stages = []
    # Work backward from the final quotient; never reuse a consumed target.
    for grade, rank in enumerate(dimensions[1:], start=2):
        arity = gcd(grade, prime-1) + 1 if prime is not None else grade + 1
        for line in range(rank - 1, -1, -1):
            consumed = arity * need
            stages.append(ScalarLineStage(grade, line, arity, need, consumed))
            need = consumed
    stages.reverse()
    return ScalarLineBudget(
        dimensions, terminal_samples, prime, sum(dimensions), need,
        len(dimensions) * need, sum(stage.conversions for stage in stages),
        sum(stage.consumed_targets for stage in stages), tuple(stages),
    )


def symmetric_recovery_budget(lower_central_dimensions, *, prime, error=Fraction(1, 3)):
    """Conditional whole-grade Rees forest and bounded classical randomness.

    Requires a VERIFIED prime and actual lower-central profile, not merely
    these shape checks. No quantum receiver or physical gate clock is run.
    Nonlinear grades must satisfy the reduced-degree symmetric field guard;
    small fields reject, without silently using an unbudgeted fallback.
    """
    from theorems.power_sde import field_threshold, power_arity
    from theorems.power_sde_budget import randomness_budget

    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    if prime is None:
        raise ValueError("a supplied verified prime is required")
    scalar = scalar_line_budget(lower_central_dimensions, 1, prime=prime)
    dimensions = scalar.lower_central_dimensions
    c, r = len(dimensions), scalar.derived_dimension

    def ceil_log2(value):
        rounded = (value.numerator+value.denominator-1)//value.denominator
        return (rounded-1).bit_length()

    slack = ceil_log2(3/error)
    samples = dimensions[0]+slack
    need, stages = samples, []
    for grade, rank in enumerate(dimensions[1:], start=2):
        degree = gcd(grade, prime-1)
        if degree > 1 and prime < field_threshold(degree):
            raise ValueError(f"grade {grade}, reduced degree {degree}: symmetric field guard fails")
        arity = rank+1 if degree == 1 else power_arity(rank, degree)
        stages.append(dict(grade=grade, rank=rank, reduced_degree=degree,
                           arity=arity, conversions=need, consumed_targets=arity*need))
        need *= arity
    merges = sum(stage["conversions"] for stage in stages)
    instruments = need+merges+samples
    nonlinear_calls = sum(stage["conversions"] for stage in stages if stage["reduced_degree"] > 1)
    bits = ceil_log2(3*nonlinear_calls/error) if nonlinear_calls else None
    uniform_calls = random_bits = root_pairs = 0
    for stage in stages:
        degree = stage["reduced_degree"]
        if degree == 1:
            stage["randomness"] = None
            continue
        budget = randomness_budget(stage["rank"], degree, bits)
        pairs = budget.root_call_cap*(degree-1)*budget.root_split_attempt_cap
        bit_cap = budget.uniform_call_cap*budget.integer_rejection_cap*(prime-1).bit_length()
        stage["randomness"] = dict(failure_bits=bits, root_calls=budget.root_call_cap,
                                   polynomial_pow_gcd_pairs=pairs,
                                   uniform_calls=budget.uniform_call_cap,
                                   bit_rejection_attempts=budget.integer_rejection_cap,
                                   fair_bits=bit_cap, abort_bound=budget.total_abort_bound)
        uniform_calls += stage["conversions"]*budget.uniform_call_cap
        random_bits += stage["conversions"]*bit_cap
        root_pairs += stage["conversions"]*pairs
    leaves_per_terminal = need//samples
    leaf_bound = factorial(c-1)*(factorial(r+1)//factorial(r-c+2))**2
    if leaves_per_terminal > leaf_bound:
        raise ArithmeticError("whole-grade product exceeds the derived-dimension envelope")
    solver_error = Fraction(nonlinear_calls, 2**bits) if nonlinear_calls else Fraction(0)
    rank_error = Fraction(1, (prime-1)*prime**slack)
    return dict(status="CONDITIONAL_REES_RESOURCE_BOUND_NOT_RECEIVER_EXECUTION",
                error_model="Exact independent sources; each complete flagged instrument has the stated error bound.",
                lower_central_dimensions=dimensions, supplied_prime=prime,
                actual_class=c, derived_dimension=r, cover_dimension=sum(dimensions),
                error_target=error, final_fourier_samples=samples, fourier_slack=slack,
                stages_top_down=list(reversed(stages)), leaves_per_terminal=leaves_per_terminal,
                derived_parameter_leaf_bound=leaf_bound,
                scalar_flag_leaves_per_terminal=scalar.leaves_per_terminal,
                source_preparations=need, original_inputs=c*need, sde_calls=merges,
                nonlinear_sde_calls=nonlinear_calls, complete_instrument_calls=instruments,
                central_character_measurements=sum(stage["consumed_targets"] for stage in stages),
                solver_failure_bits_per_call=bits, solver_abort_bound=solver_error,
                rank_failure_bound=rank_error, instrument_error_per_call=error/(3*instruments),
                total_error_bound=rank_error+solver_error+error/3,
                classical_uniform_draw_cap=uniform_calls, classical_fair_bit_cap=random_bits,
                classical_root_pow_gcd_pair_cap=root_pairs,
                depth_first_group_register_bound=1 if c == 1 else 2+sum(stage["arity"]-1 for stage in stages),
                depth_first_bound_excludes_leaf_workspaces_and_arithmetic_ancillas=True,
                classical_retry_extra_source_copies=0,
                prime_validation_included=False, profile_existence_certified=False,
                deterministic_arithmetic_step_counter=False, physical_gate_clock=False,
                quantum_receiver_implemented=False, formal_total_policy_instantiated=False,
                novelty_established=False, speedup_claim_allowed=False)


def symmetric_rees_report():
    cases = [symmetric_recovery_budget(profile, prime=prime)
             for profile, prime in (((4,), 2), ((6, 3, 1), 65537),
                                    ((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), 2**127-1))]
    return dict(status="CONDITIONAL_DERIVED_DIMENSION_IMPROVEMENT",
                proof_note="research/REES_FULL_GRADE_PARAMETER_BOUND.md", cases=cases,
                note="Source and randomness bounds only; no receiver or arithmetic wall-clock execution.",
                speedup_claim_allowed=False, novelty_established=False)
