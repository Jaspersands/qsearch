"""Prime-power central cancellation controls, not an HSP receiver.

The scalar route imports a published field-solver guarantee; the simultaneous
route uses the separately implemented bounded power-SDE solver. This module
verifies/lifts supplied witnesses and bounds retries under an IDEAL source
promise. The simultaneous API checks primality, not genuine Lie/source
contracts. Pilot-coordinate acquisition and a quantum receiver are absent.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import comb, gcd, prod
from typing import Sequence

from theorems.uniform_bch_rees import lift_scalar_witness


def _contract(prime, exponent, degree):
    if type(prime) is not int or prime < 3:
        raise ValueError("a supplied verified odd prime is required")
    if type(exponent) is not int or exponent < 1:
        raise ValueError("positive exponent required")
    if type(degree) is not int or not 1 <= degree < prime:
        raise ValueError("require 1 <= degree < prime")


def _valuation(value, prime):
    valuation = 0
    while value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


@dataclass(frozen=True)
class BatchPlan:
    action: str
    valuation: int | None = None
    field_labels: tuple[int, ...] = ()
    zero_witness: tuple[int, ...] = ()


def plan_batch(labels: Sequence[int], *, prime: int, exponent: int, degree: int) -> BatchPlan:
    """Accept a zero label or one equal-valuation batch; otherwise retry.

    All batch inputs were already consumed. A retry is NOT a proof that
    no other unit-scale witness exists for the mixed-valuation labels.
    """
    _contract(prime, exponent, degree)
    labels = tuple(labels)
    modulus = prime**exponent
    if len(labels) != gcd(degree, prime-1) + 1:
        raise ValueError("the scalar power-index arity is required")
    if any(type(x) is not int or not 0 <= x < modulus for x in labels):
        raise ValueError("canonical labels modulo the stated prime power required")
    if 0 in labels:
        index = labels.index(0)
        return BatchPlan("zero", zero_witness=tuple(int(i == index) for i in range(len(labels))))
    valuations = tuple(_valuation(x, prime) for x in labels)
    if len(set(valuations)) != 1:
        return BatchPlan("retry")
    valuation = valuations[0]
    return BatchPlan("hensel", valuation,
                     tuple((x // prime**valuation) % prime for x in labels))


def lift_batch_witness(
    labels: Sequence[int], field_witness: Sequence[int], *,
    prime: int, exponent: int, degree: int,
) -> tuple[int, ...]:
    """Verify a reduced-degree field witness, then lift one unit coordinate.

    The supplied witness solves degree gcd(d,p-1) on the normalized labels.
    No search over the field or prime-power ring is performed. Active scales
    remain units; inactive scales remain EXACT zero, never nonzero nonunits.
    """
    labels = tuple(labels)
    plan = plan_batch(labels, prime=prime, exponent=exponent, degree=degree)
    if plan.action != "hensel":
        raise ValueError("equal-valuation nonzero batch required for Hensel lifting")
    scales = list(lift_scalar_witness(plan.field_labels, field_witness,
                                     prime=prime, degree=degree))
    normalized = tuple(x // prime**plan.valuation for x in labels)
    pivot = next(i for i, x in enumerate(scales) if x)
    derivative = normalized[pivot] * degree * pow(scales[pivot], degree-1, prime) % prime
    inverse = pow(derivative, -1, prime)
    power = prime
    for _ in range(1, exponent - plan.valuation):
        next_power = power * prime
        residual = sum(a * pow(x, degree, next_power)
                       for a, x in zip(normalized, scales)) % next_power
        if residual % power:
            raise ArithmeticError("Hensel invariant failed")
        correction = -(residual // power) * inverse % prime
        scales[pivot] += correction * power
        power = next_power
    if (not any(scales) or any(x and x % prime == 0 for x in scales)
            or sum(a * pow(x, degree, prime**exponent)
                   for a, x in zip(labels, scales)) % (prime**exponent)):
        raise ArithmeticError("invalid lifted unit-scale witness")
    return tuple(scales)


def _module_contract(columns, exponents, prime, degree):
    from theorems.prime_character_opi import ring
    ring(prime)
    exponents = tuple(exponents)
    if not exponents:
        raise ValueError("nonempty cyclic module required")
    for exponent in exponents:
        _contract(prime, exponent, degree)
    columns = tuple(tuple(col) for col in columns)
    moduli = tuple(prime**e for e in exponents)
    if not columns or any(len(col) != len(exponents) for col in columns):
        raise ValueError("one coordinate per cyclic factor required")
    if any(type(a) is not int or not 0 <= a < modulus
           for col in columns for a, modulus in zip(col, moduli)):
        raise ValueError("canonical mixed-modulus label coordinates required")
    return columns, exponents, moduli


def verify_module_witness(columns, scales, *, prime, exponents, degree):
    """Check ORIGINAL mixed moduli and unit-or-exact-zero dilations."""
    columns, exponents, moduli = _module_contract(columns, exponents, prime, degree)
    scales = tuple(scales)
    bound = prime**max(exponents)
    if (len(scales) != len(columns) or not any(scales)
            or any(type(s) is not int or not 0 <= s < bound or (s and s % prime == 0)
                   for s in scales)):
        return False
    return not any(sum(col[j]*pow(s, degree, modulus) for col, s in zip(columns, scales)) % modulus
                   for j, modulus in enumerate(moduli))


def lift_regular_module_witness(columns, field_witness, *, prime, exponents, degree):
    """Lift a nonsingular degree-d witness on a full cyclic module at once.

    This expects degree d, NOT a reduced-degree witness. Singular output is
    inconclusive; other witnesses or lifts can exist. Field coefficients
    must be coordinates in the actual module, not unnormalized ambient rows.
    """
    from theorems.symbolic_scalar_phase_erasure import _fmpz_rref
    columns, exponents, moduli = _module_contract(columns, exponents, prime, degree)
    scales = list(field_witness)
    if (len(scales) != len(columns) or not any(scales)
            or any(type(s) is not int or not 0 <= s < prime for s in scales)):
        raise ValueError("nonzero canonical field witness required")
    rank = len(exponents)
    if any(sum(col[j]*pow(s, degree, prime) for col, s in zip(columns, scales)) % prime
           for j in range(rank)):
        raise ValueError("field witness does not solve the original degree")
    jacobian = [[degree*col[j]*pow(s, degree-1, prime) % prime if s else 0
                 for col, s in zip(columns, scales)] for j in range(rank)]
    reduced, jacobian_rank = _fmpz_rref(jacobian, prime)
    result = {"status": "SINGULAR_FIELD_WITNESS", "scales": None,
              "jacobian_rank": jacobian_rank, "cyclic_rank": rank,
              "singularity_is_unsatisfiability": False,
              "original_module_verified": False}
    if jacobian_rank != rank:
        return result
    pivots = [next(i for i, value in enumerate(row) if value) for row in reduced]
    augmented = [[row[i] for i in pivots]+[int(j == k) for k in range(rank)]
                 for j, row in enumerate(jacobian)]
    inverse_rows, inverse_rank = _fmpz_rref(augmented, prime)
    if inverse_rank != rank:
        raise ArithmeticError("regular Jacobian minor is singular")
    inverse = [row[rank:] for row in inverse_rows]
    # Solve the stronger equations modulo p^E using the canonical integer
    # row lifts. Their regular Jacobian is unchanged at every lift step.
    power = prime
    for _ in range(1, max(exponents)):
        next_power = power*prime
        residual = [sum(col[j]*pow(s, degree, next_power) for col, s in zip(columns, scales)) % next_power
                    for j in range(rank)]
        if any(value % power for value in residual):
            raise ArithmeticError("multirow Hensel invariant failed")
        rhs = [-(value//power) % prime for value in residual]
        corrections = [sum(a*b for a, b in zip(row, rhs)) % prime for row in inverse]
        for pivot, correction in zip(pivots, corrections):
            scales[pivot] += power*correction
        power = next_power
    if not verify_module_witness(columns, scales, prime=prime, exponents=exponents, degree=degree):
        raise ArithmeticError("multirow lift failed original-module verification")
    result.update(status="VERIFIED_REGULAR_MODULE_WITNESS", scales=scales,
                  pivot_indices=pivots, lift_steps=max(exponents)-1,
                  original_module_verified=True)
    return result


def iid_regularity_bound(*, prime, cyclic_rank, arity):
    """Full-spark union bound for IID uniform coordinates in C/pC only.

    Not a certificate that observed/conditioned labels have this source law.
    The algorithm tests one witness Jacobian, never enumerates all minors.
    """
    from theorems.prime_character_opi import ring
    ring(prime)
    if (type(cyclic_rank) is not int or cyclic_rank < 1 or type(arity) is not int
            or arity < cyclic_rank+1):
        raise ValueError("positive cyclic rank and at least rank+1 columns required")
    return min(Fraction(1), Fraction(comb(arity, cyclic_rank), prime-1))


def symmetric_block_regularity_bound(*, prime, cyclic_rank, reduced_degree):
    """IID failure bound for the symmetric solver's SELECTED support.

    Its nonzero contraction retains every column of a selected first-level
    block. Only M(r) block-local minors need be nonsingular, NOT all minors
    of the full bank. This guarantee is not valid for arbitrary SDE solvers.
    The caller separately checks the symmetric solver's field threshold.
    """
    from theorems.power_sde import power_arity
    from theorems.prime_character_opi import ring
    ring(prime)
    if type(cyclic_rank) is not int or cyclic_rank < 1:
        raise ValueError("positive cyclic rank required")
    if (type(reduced_degree) is not int or not 1 <= reduced_degree < prime
            or (prime-1) % reduced_degree):
        raise ValueError("reduced degree must divide prime-1")
    arity = cyclic_rank+1 if reduced_degree == 1 else power_arity(cyclic_rank, reduced_degree)
    return min(Fraction(1), Fraction(arity, prime-1))


def regular_grade_budget(*, prime, cyclic_rank, degree, field_failure_bits=24):
    """Conditional cost for FRESH pilots plus one bank on every attempt.

    Does not implement source acquisition, subgroup-coordinate learning,
    or a quantum instrument. No unbounded retry with a fixed pilot frame.
    """
    from theorems.power_sde import field_threshold, power_arity
    from theorems.prime_character_opi import ring
    ring(prime)
    _contract(prime, 1, degree)
    if type(cyclic_rank) is not int or cyclic_rank < 1:
        raise ValueError("positive ambient cyclic rank required")
    if type(field_failure_bits) is not int or field_failure_bits < 4:
        raise ValueError("field failure budget needs at least four bits")
    reduced = gcd(degree, prime-1)
    arity = cyclic_rank+1 if reduced == 1 else power_arity(cyclic_rank, reduced)
    regularity = symmetric_block_regularity_bound(prime=prime, cyclic_rank=cyclic_rank,
                                                  reduced_degree=reduced)
    pilot = Fraction(1, prime*prime*(prime-1))
    arithmetic = Fraction(0) if reduced == 1 else Fraction(1, 1 << field_failure_bits)
    failure = min(Fraction(1), regularity+pilot+arithmetic)
    field_guard = reduced == 1 or prime >= field_threshold(reduced)
    certified = field_guard and regularity <= Fraction(1, 4)
    cost = cyclic_rank+2+arity
    pair = lambda value: [value.numerator, value.denominator]
    return {"status": "CERTIFIED_CONDITIONAL_EPISODE_BOUND" if certified else "BOUND_INCONCLUSIVE",
            "ambient_cyclic_rank": cyclic_rank,
            "pilot_samples": cyclic_rank+2, "bank_columns_upper": arity,
            "bank_arity_policy": "M(observed_pilot_subgroup_rank), not M(ambient_rank)",
            "regularity_mechanism": "nonzero symmetric contraction preserves a complete selected block",
            "arbitrary_sde_solver_supported": False,
            "fresh_pilots_each_attempt": True, "predecessors_per_episode_upper": cost,
            "degree_field_guard": field_guard, "rank_field_guard": regularity <= Fraction(1, 4),
            "pilot_incompleteness_upper": pair(pilot), "rank_failure_upper": pair(regularity),
            "arithmetic_abort_upper": pair(arithmetic),
            "episode_abort_upper": pair(failure) if field_guard else None,
            "expected_predecessors_upper": 2*cost if certified else None,
            "ideal_independent_source_required": True,
            "pilot_coordinate_acquisition_implemented": False}


def regular_module_report():
    """Fixed-seed arithmetic controls, not physical IID source executions."""
    from random import Random
    from theorems.power_sde import power_arity
    from theorems.symbolic_scalar_phase_erasure import _fmpz_rref
    from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights
    degree, failure_bits = 3, 24
    cases = []
    for prime, exponents in ((2**127-1, (2, 5)), (2**127-1, (2, 3, 4, 5)),
                             (2**127-1, (1, 2, 4, 8, 2, 3, 5, 6)),
                             (105037, (1, 2, 4, 8, 2, 3, 5, 6))):
        rank = len(exponents)
        seed, arity = 1028+rank, power_arity(rank, degree)
        rng = Random(seed)
        columns = tuple(tuple(rng.randrange(prime**e) for e in exponents) for _ in range(arity))
        field_columns = [[a % prime for a in col] for col in columns]
        weights, _, reduced_degree, _ = solve_bezout_sde_weights(
            prime, field_columns, degree, rng=rng, bounded_randomness_bits=failure_bits)
        lift = lift_regular_module_witness(columns, weights, prime=prime,
                                           exponents=exponents, degree=degree)
        generic_bad = iid_regularity_bound(prime=prime, cyclic_rank=rank, arity=arity)
        bad = symmetric_block_regularity_bound(prime=prime, cyclic_rank=rank,
                                               reduced_degree=reduced_degree)
        block_certificate = None
        for start in range(0, arity, rank+1):
            if not all(weights[start:start+rank+1]):
                continue
            _, block_rank = _fmpz_rref(list(map(list, zip(*field_columns[start:start+rank+1]))), prime)
            if block_rank == rank:
                block_certificate = {"indices": list(range(start, start+rank+1)), "rank": rank}
                break
        cases.append({"prime": prime, "degree": degree, "exponents": exponents,
                      "seed": seed, "columns": columns, "field_witness": weights,
                      "reduced_degree": reduced_degree, "field_failure_bits": failure_bits,
                      "required_columns": arity, "regularity_failure_bound": [bad.numerator, bad.denominator],
                      "generic_all_witnesses_failure_bound": [generic_bad.numerator, generic_bad.denominator],
                      "regular_block_certificate": block_certificate,
                      "ideal_uniform_source_assumed_for_bound": True,
                      "sequential_cyclic_expected_child_bound": (4*(degree+1))**rank,
                      "whole_grade_budget": regular_grade_budget(prime=prime, cyclic_rank=rank,
                                                                  degree=degree, field_failure_bits=failure_bits),
                      "lift": lift})
    return {"status": "EXACT_MODULE_ARITHMETIC_CONTROLS_NOT_QUANTUM_RECEIVER",
            "cases": cases, "seeded_runs_certify_iid_source": False,
            "pilot_subgroup_coordinates_implemented": False,
            "quantum_receiver_executed": False, "speedup_established": False,
            "whole_workflow_wall_clock_cap_enforced": False}


def batch_success_probability(*, prime: int, exponent: int, degree: int,
                              intersection_exponent: int) -> Fraction:
    """Exact IDEAL acceptance probability when |H intersect Z|=p**b.

    This probability assumes fresh independent uniform characters on K^perp.
    It neither infers b nor certifies a physical source from label marginals.
    """
    _contract(prime, exponent, degree)
    b = intersection_exponent
    if type(b) is not int or not 0 <= b <= exponent:
        raise ValueError("intersection exponent must lie between zero and exponent")
    if b == exponent:
        return Fraction(1)
    length = exponent - b
    arity = gcd(degree, prime-1) + 1
    zero = 1 - (1 - Fraction(1, prime**length))**arity
    same_nonzero = (Fraction((prime-1)**arity, prime**arity-1)
                    * (1 - Fraction(1, prime**(length*arity))))
    return zero + same_nonzero


def retry_tree_budget(*, prime: int, nilpotency_class: int,
                      higher_grade_cyclic_ranks: Sequence[int], terminal_samples: int) -> dict:
    """Conservative EXPECTATION and per-run Markov cap, not a measured run.

    Each cyclic factor has per-attempt acceptance at least1/4. A whole-run
    cap at16 times the expected leaf bound fails with probability <=1/16.
    Do not instead truncate every node at constant retries: there can be
    exponentially many nodes. Exponent sizes affect public arithmetic, not
    the number of copies in this bound. Profile checks are only necessary.
    """
    _contract(prime, 1, nilpotency_class)
    ranks = tuple(higher_grade_cyclic_ranks)
    if len(ranks) != nilpotency_class-1 or any(type(r) is not int or r < 1 for r in ranks):
        raise ValueError("one positive cyclic rank per actual higher grade required")
    if any(a < b for a, b in zip(ranks, ranks[1:])):
        raise ValueError("cyclic ranks of nested finite abelian p-groups cannot increase")
    if type(terminal_samples) is not int or terminal_samples < 1:
        raise ValueError("positive integer terminal count required")
    factor = prod((4*(gcd(d, prime-1)+1))**r for d, r in enumerate(ranks, start=2))
    mean = terminal_samples * factor
    cap = 16 * mean
    return {
        "cyclic_stages": sum(ranks),
        "expected_lifted_leaves_upper": mean,
        "expected_original_inputs_upper": nilpotency_class*mean,
        "hard_lifted_leaf_cap": cap,
        "hard_original_input_cap": nilpotency_class*cap,
        "full_instrument_cap": 2*cap + terminal_samples,
        "clock_failure_upper": "1/16",
        "status": "conditional_bound_not_receiver_execution",
    }
