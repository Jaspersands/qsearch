"""Regular SDE witnesses from IID measured-label blocks, not a receiver.

Random kernel relations replace the first-free-variable relations. Every
attempt and random loop is capped. Correctness is checked on supplied data;
success probabilities additionally require fresh IID uniform intrinsic
module labels and independent fair bits. No source or pilot is synthesized.
"""
from fractions import Fraction
from math import comb, gcd, prod
import random

from theorems.power_sde import validate_family
from theorems.power_sde_budget import (
    CappedUniformRandom, RandomnessExhausted, budgeted_power_weights, randomness_budget,
)
from theorems.prime_character_opi import ring
from theorems.prime_power_rees_descent import _module_contract, lift_regular_module_witness
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis, _fmpz_rref
from theorems.weighted_two_erasure_cascade import bezout_reduced_exponent


def _rank_contract(prime, rank):
    ring(prime)
    if prime < 3 or type(rank) is not int or rank < 1:
        raise ValueError("odd prime and positive cyclic rank required")


def _pair(value):
    return [value.numerator, value.denominator]


def kernel_block_success_probability(prime, rank, width=None):
    """Exact JOINT IID-matrix/uniform-kernel success, not a fixed-A bound."""
    _rank_contract(prime, rank)
    width = 2*(rank+1) if width is None else width
    if type(width) is not int or width <= rank:
        raise ValueError("block width must exceed rank")
    return sum((Fraction(comb(width, t)*(prime-1)**t, prime**width)
                * prod(Fraction(prime**(t-1)-prime**i, prime**(t-1)) for i in range(rank))
                for t in range(rank+1, width+1)), Fraction(0))


def random_kernel_plan(*, prime, cyclic_rank, degree, failure_bits=8, ambient_cyclic_rank=None):
    """Conditional whole-episode bound; pilot compilation is not implemented."""
    _rank_contract(prime, cyclic_rank)
    if type(degree) is not int or not 1 <= degree < prime:
        raise ValueError("require 1 <= degree < prime")
    if type(failure_bits) is not int or failure_bits < 4:
        raise ValueError("failure_bits must be an integer at least four")
    ambient = cyclic_rank if ambient_cyclic_rank is None else ambient_cyclic_rank
    if type(ambient) is not int or ambient < cyclic_rank:
        raise ValueError("ambient cyclic rank must bound the intrinsic rank")
    reduced = gcd(degree, prime-1)
    if reduced > 1:
        validate_family(prime, reduced)
    width = 2*(cyclic_rank+1)
    blocks = 1 if reduced == 1 else (reduced-1)*cyclic_rank+1
    trials = 4*(failure_bits+(blocks-1).bit_length())
    draws = blocks*trials*(width-cyclic_rank)
    rejections = failure_bits+(draws-1).bit_length()
    exhaustion = blocks*Fraction(3,4)**trials
    bit_failure = Fraction(draws, 2**rejections)
    arithmetic = Fraction(0) if reduced == 1 else Fraction(1, 2**failure_bits)
    pilots = Fraction(1, prime*prime*(prime-1))
    total_failure = pilots+exhaustion+bit_failure+arithmetic
    if max(exhaustion, bit_failure, arithmetic) > Fraction(1, 2**failure_bits):
        raise ArithmeticError("local failure allocation exceeded")
    if total_failure > Fraction(1,4):
        raise ArithmeticError("whole-episode failure allocation exceeded")
    bank_cap = blocks*trials*width
    ambient_blocks = 1 if reduced == 1 else (reduced-1)*ambient+1
    ambient_trials = 4*(failure_bits+(ambient_blocks-1).bit_length())
    ambient_bank_cap = ambient_blocks*ambient_trials*2*(ambient+1)
    source_cap = ambient+2+ambient_bank_cap
    lower = (1-Fraction(2,prime))*(1-Fraction(1,prime*(prime-1)))
    symmetric_caps = None
    if reduced > 1:
        budget = randomness_budget(cyclic_rank,reduced,failure_bits,first_level_width=width)
        symmetric_caps = {"root_call_cap":budget.root_call_cap,
                          "uniform_call_cap":budget.uniform_call_cap,
                          "random_bit_cap":budget.uniform_call_cap*budget.integer_rejection_cap*(prime-1).bit_length()}
    return {"prime": prime, "cyclic_rank": cyclic_rank, "ambient_cyclic_rank": ambient, "degree": degree,
            "reduced_degree": reduced, "failure_bits": failure_bits,
            "block_width": width, "required_blocks": blocks, "attempts_per_block": trials,
            "kernel_uniform_call_cap": draws, "kernel_integer_rejection_cap": rejections,
            "kernel_random_bit_cap": draws*rejections*(prime-1).bit_length(),
            "iid_trial_success_lower": _pair(lower),
            "block_exhaustion_upper": _pair(exhaustion),
            "kernel_bit_abort_upper": _pair(bit_failure),
            "symmetric_arithmetic_abort_upper": _pair(arithmetic),
            "symmetric_randomness_caps": symmetric_caps,
            "pilot_incompleteness_upper": _pair(pilots),
            "episode_abort_upper": _pair(total_failure),
            "bank_sources_upper": bank_cap, "pilot_sources": ambient+2,
            "whole_episode_bank_sources_upper": ambient_bank_cap,
            "predecessors_per_episode_upper": source_cap,
            "expected_predecessors_upper": 2*source_cap,
            "rank_dependent_prime_guard_required": False,
            "fresh_pilots_each_episode_required": True,
            "iid_intrinsic_label_source_required": True,
            "pilot_coordinate_acquisition_implemented": False}


def random_kernel_trial(prime, columns, *, rng):
    """One exact rank/relation test. RNG must supply uniform accepted draws."""
    columns = tuple(tuple(col) for col in columns)
    if not columns or not columns[0]:
        raise ValueError("nonempty coefficient columns required")
    rank, width = len(columns[0]), len(columns)
    _rank_contract(prime, rank)
    if width <= rank or any(len(col) != rank for col in columns):
        raise ValueError("equal-width columns and more columns than rows required")
    if any(type(a) is not int or not 0 <= a < prime for col in columns for a in col):
        raise ValueError("canonical prime-field columns required")
    rows = list(map(list, zip(*columns)))
    _, matrix_rank = _fmpz_rref(rows, prime)
    result = {"status": "MATRIX_RANK_REJECT", "matrix_rank": matrix_rank,
              "active_rank": 0, "relation": None, "uniform_calls": 0}
    if matrix_rank != rank:
        return result
    basis = _fmpz_nullspace_basis(rows, width, prime)
    if len(basis) != width-rank:
        raise ArithmeticError("kernel dimension mismatch")
    coefficients = [rng.randrange(0,prime) for _ in basis]
    if any(type(a) is not int or not 0 <= a < prime for a in coefficients):
        raise ValueError("noncanonical kernel coefficient")
    relation = [sum(a*v[i] for a,v in zip(coefficients,basis)) % prime for i in range(width)]
    if any(sum(a*col[j] for a,col in zip(relation,columns)) % prime for j in range(rank)):
        raise ArithmeticError("sampled kernel relation is invalid")
    active = [col for a,col in zip(relation,columns) if a]
    active_rank = _fmpz_rref(list(map(list,zip(*active))),prime)[1] if active else 0
    result.update(status="ACCEPTED" if active_rank == rank else "ACTIVE_RANK_REJECT",
                  relation=relation, active_rank=active_rank, uniform_calls=len(basis))
    return result


def random_regular_module_witness(*, prime, exponents, degree, draw_block,
                                  bit_source=None, failure_bits=8, ambient_cyclic_rank=None):
    """Capped arithmetic policy on supplied intrinsic-module label blocks.

    draw_block(width) must return FRESH measured-label coordinates. Its
    source law/cost cannot be certified by this classical API. Failure and
    rejected records remain explicit; a wrong contract raises rather than
    being reported as an ordinary statistical ABORT.
    """
    exponents = tuple(exponents)
    _module_contract([(0,)*len(exponents)], exponents, prime, degree)
    plan = random_kernel_plan(prime=prime, cyclic_rank=len(exponents), degree=degree,
                              failure_bits=failure_bits, ambient_cyclic_rank=ambient_cyclic_rank)
    if not callable(draw_block):
        raise ValueError("draw_block callback required")
    source = random.SystemRandom() if bit_source is None else bit_source
    rng = CappedUniformRandom(source, call_cap=plan["kernel_uniform_call_cap"],
                             rejection_cap=plan["kernel_integer_rejection_cap"], max_interval=prime)
    records, accepted = [], []
    result = {"status": "ABORT", "prime": prime, "exponents": exponents,
              "degree": degree, "plan": plan, "trials": records,
              "accepted_trial_indices": accepted, "source_columns_consumed": 0,
              "pilots_executed": False, "quantum_receiver_executed": False}

    def finish(reason):
        result.update(reason=reason, kernel_uniform_calls=rng.calls,
                      kernel_bit_draws=rng.bit_draws, kernel_random_bits=rng.random_bits)
        return result

    for block_index in range(plan["required_blocks"]):
        for attempt in range(plan["attempts_per_block"]):
            raw = draw_block(plan["block_width"])
            columns, _, _ = _module_contract(raw, exponents, prime, degree)
            if len(columns) != plan["block_width"]:
                raise ValueError("source returned the wrong number of columns")
            result["source_columns_consumed"] += len(columns)
            record = {"block": block_index, "attempt": attempt, "columns": columns}
            records.append(record)
            field_columns = [tuple(a % prime for a in col) for col in columns]
            try:
                record.update(random_kernel_trial(prime, field_columns, rng=rng))
            except RandomnessExhausted as error:
                record.update(status="KERNEL_RANDOMNESS_ABORT", error=str(error))
                return finish("kernel randomness budget exhausted")
            if record["status"] == "ACCEPTED":
                accepted.append(len(records)-1)
                break
        else:
            return finish("regular block attempt budget exhausted")

    selected = [col for index in accepted for col in records[index]["columns"]]
    relations = [records[index]["relation"] for index in accepted]
    g, exponent = bezout_reduced_exponent(prime, degree)
    if g == 1:
        gamma = relations[0]
        result["symmetric_randomness"] = None
    else:
        try:
            solved = budgeted_power_weights(
                prime, g, [tuple(a % prime for a in col) for col in selected],
                failure_bits=failure_bits, bit_source=source,
                first_level_width=plan["block_width"], first_level_relations=relations)
        except RandomnessExhausted as error:
            result["symmetric_error"] = str(error)
            return finish("symmetric arithmetic budget exhausted")
        gamma = solved.witness.weights
        result["symmetric_randomness"] = {
            "root_calls": solved.root_calls, "root_call_cap": solved.budget.root_call_cap,
            "uniform_calls": solved.uniform_calls, "uniform_call_cap": solved.budget.uniform_call_cap,
            "random_bits": solved.random_bits,
            "random_bit_cap": solved.budget.uniform_call_cap*solved.budget.integer_rejection_cap*(prime-1).bit_length(),
            "abort_upper": _pair(solved.budget.total_abort_bound)}
    weights = [pow(a,exponent,prime) if a else 0 for a in gamma]
    lift = lift_regular_module_witness(selected, weights, prime=prime, exponents=exponents, degree=degree)
    if not lift["original_module_verified"]:
        raise ArithmeticError("regular-block contraction lost active rank")
    result.update(status="VERIFIED_REGULAR_MODULE_WITNESS", selected_columns=selected,
                  field_witness=weights, lift=lift)
    return finish("verified exact arithmetic; source promise remains external")


def report():
    """Seeded public arithmetic controls, not an execution of pilot sources."""
    from theorems.prime_power_rees_descent import regular_grade_budget
    cases = []
    profiles = [(3,1,(2,3,4)), (1031,2,tuple([1,2,4,3]*4)),
                (105037,3,(2,3,4,5)), (2**128-275,12,(2,4))]
    for index,(prime,degree,exponents) in enumerate(profiles):
        labels = random.Random(20261029+index)
        def draw(width):
            return [tuple(labels.randrange(prime**e) for e in exponents) for _ in range(width)]
        case = random_regular_module_witness(prime=prime, exponents=exponents, degree=degree,
                                             draw_block=draw, bit_source=random.Random(1029+index))
        case["seed"] = 20261029+index
        case["kernel_seed"] = 1029+index
        case["iid_exact_trial_success"] = _pair(kernel_block_success_probability(prime,len(exponents)))
        case["prior_selected_block_budget"] = regular_grade_budget(
            prime=prime, cyclic_rank=len(exponents), degree=degree)
        cases.append(case)
    fixed_columns = [(1,0),(0,1)]+[(0,0)]*4
    fixed = random_regular_module_witness(prime=3,exponents=(2,3),degree=1,
        draw_block=lambda width:fixed_columns,bit_source=random.Random(29),failure_bits=4)
    return {"status": "RANDOM_REGULAR_ARITHMETIC_NOT_QUANTUM_RECEIVER",
            "proof_note": "research/RANDOM_KERNEL_REGULAR_SDE.md", "cases": cases,
            "fixed_matrix_falsifier": {"iid_source_promise_satisfied":False, "run":fixed},
            "rank_dependent_prime_guard_required": False,
            "symmetric_degree_only_field_guard_still_required": True,
            "seeded_controls_certify_iid_source": False,
            "pilot_coordinate_acquisition_implemented": False,
            "quantum_receiver_executed": False, "speedup_established": False,
            "os_wallclock_bound_enforced": False}
