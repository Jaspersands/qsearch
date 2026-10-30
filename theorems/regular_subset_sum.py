"""Bounded exact Boolean cancellation over a verified odd prime field.

Only the supplied prefix supplies a regularity basis. The suffix is searched
deterministically, with one Boolean mask per reached residue, never by random
sampling. ABORT is inconclusive for arbitrary diagonal equations, even after
exhausting this restricted search. No module lifting or source certification
is performed here.
"""
from fractions import Fraction

from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import _fmpz_rref


def _prime_contract(prime):
    # Check before the cached helper so equal noninteger cache keys cannot pass.
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("prime must be an odd prime Python integer")
    ring(prime)


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be a Python integer >= {minimum}")


def subset_sum_moments(prime, rank, width):
    """Exact conditional moments for nonempty Boolean hits on a fixed target.

    Let A have IID uniform columns in F_p**rank, and let X count nonzero
    b in {0,1}**width with A*b=t. The target must be fixed or independent of
    the suffix (for example, selected using a separate prefix). Distinct
    nonzero Boolean words cannot be scalar multiples: their common nonzero
    coordinate forces the scalar to be 1. Their images are therefore pairwise
    independent and uniform, giving the stated mean and variance.

    Chebyshev gives Pr[X=0] <= min(1, 1/mu); width zero has mu=0 and bound 1.
    The empty word is excluded even when t=0. This no-hit bound does NOT bound
    a capped search's abort probability, and no observed bank certifies IID.
    """
    _prime_contract(prime)
    _integer(rank, "rank", 0)
    _integer(width, "width", 0)
    state_bound = prime**rank
    words = 2**width - 1
    probability = Fraction(1, state_bound)
    mean = words * probability
    return dict(
        prime=prime, rank=rank, width=width, state_bound=state_bound,
        nonzero_boolean_words=words, single_word_hit_probability=probability,
        mu=mean, variance=mean * (1 - probability),
        no_hit_upper=min(Fraction(1), 1 / mean) if mean else Fraction(1),
        distinct_word_images_pairwise_independent=True,
        iid_uniform_columns_required=True, iid_uniform_columns_verified=False,
        target_independent_of_suffix_required=True,
        state_cap_exhaustion_included=False,
    )


def _subset_sum(columns, target, *, prime, max_states):
    """Internal DP on validated canonical columns and a matching target.

    states_visited counts distinct stored residues, including the initial
    empty subset; it equals peak_states because states are never evicted.
    transitions counts attempted include-column transitions, including
    collisions and a cap-blocked insertion. columns_processed counts suffix
    columns started, including a column interrupted by success or the cap.
    """
    states = {(0,) * len(target): 0}
    result = dict(mask=None, reason="TARGET_NOT_FOUND", states_visited=1,
                  peak_states=1, transitions=0, columns_processed=0,
                  cap_truncated=False)
    if target in states:
        result.update(mask=0, reason="TARGET_FOUND")
        return result
    for index, column in enumerate(columns):
        result["columns_processed"] += 1
        # Only pre-column masks may be extended, so each column is used once.
        for residue, mask in tuple(states.items()):
            result["transitions"] += 1
            reached = tuple((x + y) % prime for x, y in zip(residue, column))
            if reached in states:
                continue
            if len(states) >= max_states:
                result.update(reason="STATE_CAP", cap_truncated=True)
                return result
            states[reached] = mask | (1 << index)
            result["states_visited"] += 1
            result["peak_states"] = len(states)
            if reached == target:
                result.update(mask=states[reached], reason="TARGET_FOUND")
                return result
    return result


def regular_subset_witness(columns, *, prime, degree, prefix_count, max_states=None):
    """Find a nonzero regular 0/1 degree-d cancellation, or return ABORT.

    columns must be a nonempty finite list/tuple of equally sized list/tuple
    columns with canonical Python integer coordinates (no bools). The row
    dimension a is returned as rank, NOT reduced to the observed column rank.
    Require a verified odd prime, 1 <= degree < prime, 0 <= prefix_count <=
    len(columns), and a positive integer max_states when supplied.

    Choose a independent prefix columns by exact elimination, fix their
    scales to 1 and all other prefix scales to 0, and search only the suffix
    for minus their sum. Verify the original degree and the rank-a Jacobian
    restricted to active coordinates. Boolean scales need no degree reduction.

    max_states=None means exactly prime**a, potentially expensive but finite;
    only reached residues are allocated, not an enumerated field-sized table.
    state_cap_met means the configured cap is at least prime**a. A smaller cap
    can still return a verified witness, but truncation immediately aborts and
    carries no probabilistic confidence. DP counters have _subset_sum's
    definitions and exclude prefix elimination and final verification.

    If a=0, every column must be empty and at least one column must exist.
    Return (1,0,...) with vacuous cancellation and Jacobian rank zero, without
    running the DP (all its counters are zero). Nonempty all-zero rows instead
    fail the prefix-rank check; they are NOT treated as dimension zero.
    """
    _prime_contract(prime)
    _integer(degree, "degree", 1)
    if degree >= prime:
        raise ValueError("require 1 <= degree < prime")
    if not isinstance(columns, (list, tuple)) or not columns:
        raise ValueError("nonempty finite list/tuple of columns required")
    if any(not isinstance(column, (list, tuple)) for column in columns):
        raise ValueError("each column must be a finite list/tuple")
    bank = tuple(tuple(column) for column in columns)
    rank, width = len(bank[0]), len(bank)
    if any(len(column) != rank for column in bank):
        raise ValueError("rectangular columns required")
    if any(type(x) is not int or not 0 <= x < prime for column in bank for x in column):
        raise ValueError("canonical Python integer field coordinates required")
    _integer(prefix_count, "prefix_count", 0)
    if prefix_count > width:
        raise ValueError("prefix_count cannot exceed the number of columns")
    state_bound = prime**rank
    cap = state_bound if max_states is None else max_states
    _integer(cap, "max_states", 1)

    prefix_rows = [[column[j] for column in bank[:prefix_count]] for j in range(rank)]
    reduced, prefix_rank = _fmpz_rref(prefix_rows, prime)
    basis = tuple(next(i for i, x in enumerate(row) if x) for row in reduced)
    result = dict(
        status="ABORT", reason="PREFIX_RANK_DEFICIENT", scales=None,
        prime=prime, degree=degree, rank=rank, width=width,
        prefix_count=prefix_count, prefix_rank=prefix_rank, basis_indices=basis,
        suffix_width=width - prefix_count, target=None, suffix_mask=None,
        max_states=cap, state_bound=state_bound, state_cap_met=cap >= state_bound,
        states_visited=0, peak_states=0, transitions=0, columns_processed=0,
        cap_truncated=False, jacobian_rank=None, exact_verified=False,
        zero_rank_branch=rank == 0, abort_is_unsatisfiability=False,
        iid_uniform_columns_verified=False, arbitrary_fixed_bank_success_bound=None,
    )
    if prefix_rank != rank:
        return result

    scales = [0] * width
    if rank == 0:
        scales[0] = 1
        result.update(target=(), reason="ZERO_DIMENSION_NONZERO_WITNESS")
    else:
        target = tuple(-sum(bank[i][j] for i in basis) % prime for j in range(rank))
        search = _subset_sum(bank[prefix_count:], target, prime=prime, max_states=cap)
        mask = search.pop("mask")
        result.update(search, target=target, suffix_mask=mask)
        if mask is None:
            return result
        for index in basis:
            scales[index] = 1
        for index in range(width - prefix_count):
            scales[prefix_count + index] = (mask >> index) & 1

    residual = tuple(sum(pow(s, degree, prime) * column[j]
                         for s, column in zip(scales, bank)) % prime
                     for j in range(rank))
    active_jacobian = [[degree * pow(s, degree - 1, prime) * column[j] % prime
                        for s, column in zip(scales, bank) if s]
                       for j in range(rank)]
    _, jacobian_rank = _fmpz_rref(active_jacobian, prime)
    if (not any(scales) or any(type(s) is not int or s not in (0, 1) for s in scales)
            or any(residual) or jacobian_rank != rank):
        raise ArithmeticError("Boolean cancellation or active Jacobian verification failed")
    result.update(status="VERIFIED_REGULAR_SUBSET_WITNESS", scales=scales,
                  jacobian_rank=jacobian_rank, exact_verified=True)
    return result
