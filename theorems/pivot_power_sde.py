"""Bounded, fixed-bank SDE using power-valued free coordinates.

Only a disjoint pilot prefix selects the basis. The conditional probability
API assumes IID uniform labels in a fixed subspace; execution never certifies
that promise. Every success is verified in the original ambient coordinates.
No field tables, label resampling, or quantum receiver are implemented.
This is prime-field-only: active support need not span, so this is NOT a
regular mixed-order Hensel witness. Root arithmetic is polynomial in d,
not merely log(d).
"""
from fractions import Fraction
from math import gcd
import random

from theorems.bounded_power_roots import bounded_power_root
from theorems.power_sde_budget import CappedUniformRandom, RandomnessExhausted
from theorems.symbolic_scalar_phase_erasure import _fmpz_rref, _fmpz_solve_coordinates
from theorems.weighted_two_erasure_cascade import (
    bezout_reduced_exponent, verify_general_degree_witness,
)


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _parameters(p, e):
    _integer(p, "supplied odd prime", 3)
    if p % 2 == 0:
        raise ValueError("an odd supplied prime is required")
    _integer(e, "original exponent", 1)
    return gcd(e, p-1)


def pivot_conditional_moments(p, e, rank, suffix_count):
    """Exact moments conditional on a COMPLETE, independently chosen pilot.

    Here rank is the TRUE source dimension, not an empirical certificate.
    X counts x in {1} x S**(suffix_count-1) with -C*x in S**rank.
    Distinct candidates are linearly independent, so their hit indicators
    are pairwise independent for an IID uniform C. No candidates are listed.
    """
    d = _parameters(p, e)
    _integer(rank, "rank", 0)
    _integer(suffix_count, "suffix_count", 1)
    q = 1+(p-1)//d
    count = q**(suffix_count-1)
    hit = Fraction(q, p)**rank
    mean = count*hit
    variance = mean*(1-hit)
    bad = min(Fraction(1), 4*variance/mean**2)
    return {
        "p": p, "e": e, "d": d, "source_rank": rank,
        "suffix_count": suffix_count, "power_alphabet_size": q,
        "candidate_count": count, "candidate_hit_probability": hit,
        "mean": mean, "variance": variance,
        "tail_bad_bank_upper": bad,
        "fixed_good_bank_density_lower": hit/2 if hit < 1 else Fraction(1),
        "complete_pilot_required": True,
        "moment_conditioned_on_suffix_membership": False,
        "iid_uniform_columns_required": True, "iid_uniform_columns_verified": False,
        "arbitrary_fixed_bank_guarantee": False,
        "prime_field_only": True, "regularity_not_guaranteed": True,
    }


def pivot_power_budget(p, e, width, *, pilot_count, rank_bound, attempt_cap,
                       failure_bits=32):
    """Uniform caps and source-CONDITIONAL bounds, with no implicit search cap.

    Auxiliary root/bit failure is <= 2**(-failure_bits), independently of
    the separately reported bad-bank and good-bank search-exhaustion terms.
    The latter is represented as base**exponent, not expanded into a huge
    Fraction. Moments evaluated at rank_bound are exact only when the true
    rank equals that bound; the reported failure/density bounds are uniform
    over all smaller source ranks. Prime verification is an external promise.
    """
    d = _parameters(p, e)
    for value, name, minimum in ((width, "width", 1), (pilot_count, "pilot_count", 0),
                                 (rank_bound, "rank_bound", 0),
                                 (attempt_cap, "attempt_cap", 1),
                                 (failure_bits, "failure_bits", 1)):
        _integer(value, name, minimum)
    if not rank_bound <= pilot_count < width:
        raise ValueError("rank_bound <= pilot_count < width required")
    suffix = width-pilot_count
    moments = pivot_conditional_moments(p, e, rank_bound, suffix)
    pilot_success = Fraction(1)
    for i in range(rank_bound):
        pilot_success *= 1-Fraction(1, p**(pilot_count-i))
    pilot_failure = 1-pilot_success
    stochastic = d > 1 and rank_bound > 0
    roots = rank_bound if stochastic else 0
    terms = roots*(d-1)
    split_cap = 3*(failure_bits+1+(max(1, terms)-1).bit_length()) if roots else 0
    # A strict descent visits degrees at most d,d-1,...,2.
    root_draws_per_call = split_cap*(d*(d+1)//2-1) if roots else 0
    root_trials_per_call = (d-1)*split_cap if roots else 0
    sample_calls = 2*(suffix-1)*attempt_cap if stochastic else 0
    root_calls = roots*root_draws_per_call
    calls = sample_calls+root_calls
    rejection_cap = failure_bits+1+(calls-1).bit_length() if calls else 0
    root_abort = terms*Fraction(2, 3)**split_cap
    bit_abort = Fraction(calls, 2**rejection_cap)
    if root_abort+bit_abort > Fraction(1, 2**failure_bits):
        raise ArithmeticError("auxiliary failure allocation exceeded")
    density = moments["fixed_good_bank_density_lower"]
    return {
        "p": p, "e": e, "d": d, "width": width, "pilot_count": pilot_count,
        "suffix_count": suffix, "rank_bound": rank_bound,
        "attempt_cap": attempt_cap, "failure_bits": failure_bits,
        "moments_at_rank_bound": moments,
        "pilot_failure_upper": pilot_failure,
        "pilot_failure_geometric_upper": Fraction(p**rank_bound-1, (p-1)*p**pilot_count),
        "tail_bad_bank_upper": moments["tail_bad_bank_upper"],
        "bad_bank_upper": min(Fraction(1), pilot_failure+moments["tail_bad_bank_upper"]),
        "fixed_good_bank_density_lower": density,
        "good_bank_attempt_failure_bound": {"base": 1-density, "exponent": attempt_cap},
        "sample_uniform_call_cap": sample_calls,
        "root_call_cap": roots, "root_split_attempt_cap": split_cap,
        "root_split_trials_per_call_cap": root_trials_per_call,
        "root_uniform_calls_per_call_cap": root_draws_per_call,
        "root_split_trial_cap": roots*root_trials_per_call,
        "root_uniform_call_cap": root_calls, "uniform_call_cap": calls,
        "integer_rejection_cap": rejection_cap,
        "bit_draw_cap": calls*rejection_cap,
        "random_bit_cap": calls*rejection_cap*(p-1).bit_length(),
        "root_abort_upper": root_abort, "bit_abort_upper": bit_abort,
        "auxiliary_abort_upper": root_abort+bit_abort,
        "attempt_exhaustion_in_auxiliary_bound": False,
        "bad_bank_failure_in_auxiliary_bound": False,
        "iid_uniform_columns_required": True, "iid_fair_bits_required": True,
        "iid_uniform_columns_verified": False, "iid_fair_bits_verified": False,
        "arbitrary_fixed_bank_success_bound": None,
        "prime_validation_locally_clocked": False,
        "prime_field_only": True, "regularity_not_guaranteed": True,
        "moment_conditioned_on_suffix_membership": False,
    }


def pivot_power_sde(p, e, columns, *, pilot_count, rank_bound, attempt_cap,
                    failure_bits=32, bit_source=None):
    """Verified original-exponent witness or bounded ABORT on a fixed bank.

    Input is a finite rectangular list/tuple of canonical field columns.
    Even deterministic branches check EVERY suffix column against the pilot
    span. Zero coefficients never request roots and remain zero after lifting.
    All input slots are charged, including unused pilot columns.

    Calls/bits include interrupted sampling. Each started root call reserves
    its full declared allowance. The reused root API cannot expose split
    counters on interruption: those totals become None, with returned-call
    counters and exact charged caps retained separately, never fabricated.
    Backend/malformed-input errors propagate rather than becoming ABORTs.
    """
    _parameters(p, e)
    if not isinstance(columns, (list, tuple)) or not columns:
        raise ValueError("nonempty finite list/tuple of columns required")
    if any(not isinstance(col, (list, tuple)) for col in columns):
        raise ValueError("each column must be a finite list/tuple")
    bank = tuple(tuple(col) for col in columns)
    width, ambient = len(bank), len(bank[0])
    if any(len(col) != ambient for col in bank):
        raise ValueError("rectangular columns required")
    if any(type(x) is not int or not 0 <= x < p for col in bank for x in col):
        raise ValueError("canonical integer field coordinates required")
    budget = pivot_power_budget(p, e, width, pilot_count=pilot_count,
                                rank_bound=rank_bound, attempt_cap=attempt_cap,
                                failure_bits=failure_bits)
    source = random.SystemRandom() if bit_source is None else bit_source
    if isinstance(source, type) or not callable(getattr(source, "getrandbits", None)):
        raise ValueError("bit_source must be an instance with getrandbits")
    rng = (CappedUniformRandom(source, call_cap=budget["uniform_call_cap"],
                              rejection_cap=budget["integer_rejection_cap"], max_interval=p)
           if budget["uniform_call_cap"] else None)
    d, lift = bezout_reduced_exponent(p, e)
    if d != budget["d"]:
        raise ArithmeticError("exponent reduction disagrees with budget")
    pilot_rows = [list(row) for row in zip(*bank[:pilot_count])]
    reduced, rank = _fmpz_rref(pilot_rows, p)
    indices = tuple(next(i for i, x in enumerate(row) if x) for row in reduced)
    if len(indices) != rank or any(i >= pilot_count for i in indices):
        raise ArithmeticError("invalid pilot basis returned by RREF")
    basis = tuple(bank[i] for i in indices)
    result = {
        "status": "ABORT", "reason": None, "weights": None, "power_vector": None,
        "p": p, "e": e, "d": d, "lift_exponent": lift,
        "columns": bank, "ambient_dimension": ambient, "rank_bound": rank_bound,
        "pilot_rank": rank, "pilot_indices": indices, "pilot_basis": basis,
        "pilot_count": pilot_count, "suffix_coordinates": None,
        "pilot_selection_uses_suffix": False,
        "suffix_membership_checks": 0, "outside_pilot_indices": (),
        "input_labels_charged": width, "budget": budget,
        "attempts": 0, "completed_candidates": 0, "nonpower_rejections": 0,
        "sample_uniform_calls": 0, "root_uniform_calls": 0,
        "root_calls_started": 0, "root_calls_completed": 0,
        "root_uniform_call_cap_charged": 0, "root_split_trial_cap_charged": 0,
        "completed_root_split_trials": 0, "completed_root_proper_splits": 0,
        "root_split_counts_complete": True, "exact_verified": False,
        "iid_uniform_columns_verified": False, "iid_fair_bits_verified": False,
        "input_labels_resampled": False, "field_enumeration_used": False,
        "arbitrary_fixed_bank_success_bound": None,
        "prime_validation_locally_clocked": False,
        "quantum_receiver_implemented": False, "hsp_claim": False, "speedup_claim": False,
        "prime_field_only": True, "regularity_not_guaranteed": True,
    }

    def finish(reason, roots=None, coefficients=None):
        result.update(reason=reason, uniform_calls=rng.calls if rng else 0,
                      bit_draws=rng.bit_draws if rng else 0,
                      random_bits=rng.random_bits if rng else 0)
        complete = result["root_split_counts_complete"]
        result["root_split_trials"] = result["completed_root_split_trials"] if complete else None
        result["root_proper_splits"] = result["completed_root_proper_splits"] if complete else None
        if roots is not None:
            if (len(roots) != width or len(coefficients) != width or not any(roots)
                    or any(type(s) is not int or not 0 <= s < p for s in roots)
                    or tuple(pow(s, d, p) for s in roots) != tuple(coefficients)):
                raise ArithmeticError("invalid reduced-exponent witness")
            weights = tuple(pow(s, lift, p) if s else 0 for s in roots)
            if tuple(pow(s, e, p) for s in weights) != tuple(coefficients):
                raise ArithmeticError("invalid original-exponent lift")
            if ambient:
                verify_general_degree_witness(p, bank, weights, e)
            result.update(status="VERIFIED", weights=weights,
                          power_vector=tuple(coefficients), exact_verified=True)
        return result

    if rank > rank_bound:
        return finish("PILOT_RANK_EXCEEDS_PROMISE")
    coordinates, outside = [], []
    for i, col in enumerate(bank[pilot_count:], pilot_count):
        coords = _fmpz_solve_coordinates(basis, col, p)
        result["suffix_membership_checks"] += 1
        if coords is None:
            outside.append(i)
        elif (len(coords) != rank or any(type(z) is not int or not 0 <= z < p for z in coords)
              or any(sum(z*b[j] for z, b in zip(coords, basis)) % p != col[j]
                     for j in range(ambient))):
            raise ArithmeticError("invalid ambient pilot coordinates")
        coordinates.append(coords)
    result["suffix_coordinates"] = tuple(coordinates)
    result["outside_pilot_indices"] = tuple(outside)
    if outside:
        return finish("SUFFIX_OUTSIDE_PILOT_SPAN")

    if rank == 0 or d == 1:
        vector = [0]*width
        vector[pilot_count] = 1
        for i, z in zip(indices, coordinates[0]):
            vector[i] = -z % p
        return finish("ZERO_BANK_DETERMINISTIC" if rank == 0 else "LINEAR_DETERMINISTIC",
                      vector, vector)

    q = 1+(p-1)//d
    for _ in range(attempt_cap):
        result["attempts"] += 1
        suffix_roots, x = [1], [1]
        before = rng.calls
        try:
            for _ in range(len(coordinates)-1):
                z = 0 if rng.randrange(0, q) == 0 else rng.randrange(1, p)
                suffix_roots.append(z)
                x.append(pow(z, d, p))
        except RandomnessExhausted:
            return finish("BIT_REJECTION_CAP")
        finally:
            result["sample_uniform_calls"] += rng.calls-before
        y = tuple(-sum(z*col[j] for z, col in zip(x, coordinates)) % p for j in range(rank))
        result["completed_candidates"] += 1
        if any(z and pow(z, (p-1)//d, p) != 1 for z in y):
            result["nonpower_rejections"] += 1
            continue
        roots, coefficients = [0]*width, [0]*width
        roots[pilot_count:], coefficients[pilot_count:] = suffix_roots, x
        for i, value in zip(indices, y):
            coefficients[i] = value
            if not value:
                continue
            result["root_calls_started"] += 1
            result["root_uniform_call_cap_charged"] += budget["root_uniform_calls_per_call_cap"]
            result["root_split_trial_cap_charged"] += budget["root_split_trials_per_call_cap"]
            if result["root_calls_started"] > budget["root_call_cap"]:
                raise ArithmeticError("root call cap exceeded")
            before = rng.calls
            try:
                root = bounded_power_root(p, d, value, rng=rng,
                                          split_attempt_cap=budget["root_split_attempt_cap"])
            except RandomnessExhausted:
                result["root_split_counts_complete"] = False
                return finish("BIT_REJECTION_CAP")
            finally:
                result["root_uniform_calls"] += rng.calls-before
                if rng.calls-before > budget["root_uniform_calls_per_call_cap"]:
                    raise ArithmeticError("root backend exceeded its uniform draw cap")
            if (root.random_field_elements != rng.calls-before
                    or type(root.random_field_elements) is not int
                    or type(root.split_trials) is not int
                    or not 0 <= root.split_trials <= budget["root_split_trials_per_call_cap"]
                    or type(root.proper_splits) is not int
                    or not 0 <= root.proper_splits <= min(d-1, root.split_trials)):
                raise ArithmeticError("root backend accounting mismatch")
            result["root_calls_completed"] += 1
            result["completed_root_split_trials"] += root.split_trials
            result["completed_root_proper_splits"] += root.proper_splits
            if root.root is None:
                return finish("ROOT_SPLIT_CAP")
            if type(root.root) is not int or not 0 < root.root < p or pow(root.root, d, p) != value:
                raise ArithmeticError("root backend returned invalid root")
            roots[i] = root.root
        return finish("EXACT_PIVOT_POWER_WITNESS", roots, coefficients)
    return finish("ATTEMPT_CAP")


def pivot_power_report():
    """Seeded arithmetic controls only; return data without writing any files."""
    cases = []
    for p, e, a in ((5, 4, 2), (7, 6, 3), (101, 5, 3), (2**127-1, 12, 3)):
        rng = random.Random(20261030+p+e)
        embedding = [tuple(int(i == j) for i in range(a))+(j+1, 2*j+1)
                     for j in range(a)]
        def embed(v):
            return tuple(sum(v[j]*embedding[j][i] for j in range(a)) % p for i in range(a+2))
        bank = [embed([rng.randrange(p) for _ in range(a)]) for _ in range(2*a+12)]
        result = pivot_power_sde(p, e, bank, pilot_count=a+4, rank_bound=a,
                                 attempt_cap=4096, failure_bits=20,
                                 bit_source=random.Random(91))
        cases.append(result)
    cases.append(pivot_power_sde(5, 4, [(1,), (1,), (1,)], pilot_count=1,
                                 rank_bound=1, attempt_cap=12, failure_bits=12,
                                 bit_source=random.Random(12)))
    return {"status": "BOUNDED_FIXED_BANK_ARITHMETIC_ONLY", "cases": cases,
            "proof_note": "research/PIVOT_POWER_SDE.md",
            "iid_source_certified": False, "quantum_receiver_executed": False,
            "prime_field_only": True, "regularity_not_guaranteed": True,
            "new_all_prime_coverage_claim": False, "novelty_established": False,
            "scope": "Rank-exponent rejection; no field-sized table or input resampling."}
