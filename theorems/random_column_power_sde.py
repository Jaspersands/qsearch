"""Bounded classical power-kernel search on a fixed public column bank.

The prime is supplied with an external verification promise. This module
does not provide a primality certificate or a clock for prime validation.
The existing odd-prime nullspace helper may itself perform a library prime
check. No symmetric-SDE family validation or large-field guard is used.

Projective moment bounds concern UNVERIFIED IID uniform columns in an
a-dimensional subspace, not arbitrary fixed banks. Repeating kernel draws
cannot repair a bad bank. Seeded bit sources are reproducibility controls,
not IID certificates. No field enumeration, input-label resampling, HSP,
quantum implementation, novelty, or speedup claim is made here.
"""
from fractions import Fraction
import random

from theorems.bounded_power_roots import bounded_power_root
from theorems.power_sde_budget import CappedUniformRandom, RandomnessExhausted
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis, _fmpz_rref


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _field_contract(p, d):
    _integer(p, "supplied prime p", 2)
    if p != 2 and p % 2 == 0:
        raise ValueError("supplied prime p must be 2 or odd")
    _integer(d, "reduced degree d", 1)
    if (p-1) % d:
        raise ValueError("reduced degree d must divide p-1")


def _shape_contract(rank_bound, width):
    _integer(rank_bound, "rank_bound", 0)
    _integer(width, "width", 1)
    if width <= rank_bound:
        raise ValueError("width must exceed rank_bound")


def projective_bank_bounds(p, d, rank_bound, width):
    """Exact conditional moments and good-bank bounds, not a source audit.

    X counts projective classes in (H union {0})**width minus {0} killed
    by a uniform rank_bound-by-width matrix (including deficient matrices).
    H is the nonzero dth-power subgroup. Distinct classes give pairwise
    independent kernel events; each class has h representatives.

    The bad-bank bound combines X < E[X]/2 with row-rank deficiency. On
    the complementary good-bank event, uniform full-kernel sampling has
    at least the reported power density. Rank zero is deterministic.
    These hypotheses are not certified by calling this function, even if
    rank_bound happens to equal the observed rank of a supplied bank.
    """
    _field_contract(p, d)
    _shape_contract(rank_bound, width)
    h = (p-1)//d
    size = (h+1)**width-1
    classes = size//h
    probability = Fraction(1, p**rank_bound)
    mean = classes*probability
    variance = classes*probability*(1-probability)
    bad = (min(Fraction(1), 4/mean+Fraction(2, p**(width-rank_bound)))
           if rank_bound else Fraction(0))
    return {
        "p": p, "d": d, "rank_bound": rank_bound, "width": width,
        "h": h, "S": size, "D": classes, "mu": mean, "variance": variance,
        "bad_bank_upper": bad,
        "good_bank_kernel_power_density_lower": Fraction(size, 2*p**width),
        "weaker_density_lower": (Fraction(1, 4*d**width)
                                 if p**width >= 2*d**width else None),
        "rank_zero_kernel_power_density": (Fraction(size, p**width)
                                            if rank_bound == 0 else None),
        "rank_zero_deterministic": rank_bound == 0,
        "iid_uniform_columns_required": True,
        "iid_uniform_columns_verified": False,
        "supplied_prime_verified_by_this_api": False,
        "arbitrary_fixed_bank_guarantee": False,
        "fixed_bank_repetitions_repair_bad_banks": False,
    }


def random_column_budget(p, d, width, *, attempt_cap, failure_bits=32):
    """Auxiliary root/bit abort budget ONLY; attempts may all miss forever.

    Under fresh IID fair bits the sum of the root-splitting and integer
    rejection bounds is <= 2**(-failure_bits). The caller must separately
    justify any kernel-hitting probability and choose its own attempt cap.
    """
    _field_contract(p, d)
    _integer(width, "width", 1)
    _integer(attempt_cap, "attempt_cap", 1)
    _integer(failure_bits, "failure_bits", 1)
    terms = width*(d-1)
    split_cap = 3*(failure_bits+(max(1, terms)-1).bit_length()+2)
    root_calls = width if d > 1 else 0
    kernel_calls = width*attempt_cap
    root_draws = root_calls*d*(d-1)*split_cap
    calls = kernel_calls+root_draws
    rejection_cap = failure_bits+1+(calls-1).bit_length()
    root_abort = terms*Fraction(2, 3)**split_cap
    bit_abort = Fraction(calls, 2**rejection_cap)
    if root_abort+bit_abort > Fraction(1, 2**failure_bits):
        raise ArithmeticError("auxiliary failure allocation exceeded")
    return {
        "attempt_cap": attempt_cap, "failure_bits": failure_bits,
        "kernel_uniform_call_cap": kernel_calls,
        "root_call_cap": root_calls,
        "root_split_attempt_cap": split_cap,
        "root_split_trial_cap": root_calls*(d-1)*split_cap,
        "root_uniform_call_cap": root_draws,
        "uniform_call_cap": calls,
        "integer_rejection_cap": rejection_cap,
        "bit_draw_cap": calls*rejection_cap,
        "random_bit_cap": calls*rejection_cap*(p-1).bit_length(),
        "root_abort_upper": root_abort, "bit_abort_upper": bit_abort,
        "auxiliary_abort_upper": root_abort+bit_abort,
        "attempt_exhaustion_included": False,
        "iid_fair_bits_required": True,
    }


def unit_projective_bank_bounds(p, d, rank_bound, width):
    """Conditional IID-bank bounds for vectors in H**width, with no zeros.

    H is the nonzero dth-power subgroup. Its h**width vectors form
    h**(width-1) projective classes, each with h representatives. For an
    IID uniform rank_bound-by-width matrix, distinct classes have pairwise
    independent kernel events. The good event requires full row rank and
    at least half the mean class count. Rank zero has bad probability zero.

    These are source-conditional field bounds, not a certificate for fixed
    columns or a success guarantee for repeated draws from a bad bank.
    The bounds include p=2; the all-nonzero sampler is odd-prime only.
    """
    _field_contract(p, d)
    _shape_contract(rank_bound, width)
    h = (p-1)//d
    size = h**width
    classes = h**(width-1)
    probability = Fraction(1, p**rank_bound)
    mean = classes*probability
    variance = mean*(1-probability)
    bad = (min(Fraction(1), 4/mean+Fraction(2, p**(width-rank_bound)))
           if rank_bound else Fraction(0))
    return {
        "p": p, "d": d, "rank_bound": rank_bound, "width": width,
        "h": h, "S": size, "D": classes, "mu": mean, "variance": variance,
        "bad_bank_upper": bad,
        "good_bank_kernel_power_density_lower": Fraction(size, 2*p**width),
        "weaker_density_lower": Fraction(1, 2*(2*d)**width),
        "rank_zero_kernel_power_density": (Fraction(size, p**width)
                                            if rank_bound == 0 else None),
        "rank_zero_deterministic": rank_bound == 0,
        "require_nonzero": True,
        "iid_uniform_columns_required": True,
        "iid_uniform_columns_verified": False,
        "supplied_prime_verified_by_this_api": False,
        "arbitrary_fixed_bank_guarantee": False,
        "fixed_bank_repetitions_repair_bad_banks": False,
    }


def random_column_power_sde(p, d, columns, *, rank_bound, attempt_cap,
                            failure_bits=32, bit_source=None, require_nonzero=False):
    """Return a verified witness or explicit bounded ABORT on fixed columns.

    Columns must be a nonempty, finite rectangular list/tuple of canonical
    Python integers. Empty ambient coordinates are allowed (the zero bank).
    rank_bound bounds the promised intrinsic rank, not the ambient dimension.
    A canonical observed bank exceeding it emits a bounded ABORT, so this
    record does not make a future complete receiver policy undefined.
    attempt_cap is mandatory, positive, and never automatically exponential.

    With IID bits, each completed kernel draw is uniform using independent
    F_p coefficients for EVERY vector in the full nullspace basis. Zero is
    rejected. A power vector is rooted once; any root or bit exhaustion
    immediately aborts without partial witnesses or hidden retries.

    require_nonzero must be a bool. When true, EVERY coordinate must be
    nonzero: rank zero returns all ones, and even d=1 uses bounded full-
    kernel sampling (without root calls). This mode supports supplied odd
    primes only; p=2 is rejected before backend arithmetic. By default the
    existing deterministic linear shortcut and zero coordinates are allowed.
    Zero-vector, partial-zero, and nonpower rejection counters are disjoint.

    root_split_trials/proper_splits count returned root calls. If bit
    rejection interrupts a root call, root_split_counts_complete is false;
    uniform/bit counts still include that interrupted call exactly.
    """
    if type(require_nonzero) is not bool:
        raise ValueError("require_nonzero must be a bool")
    _field_contract(p, d)
    if require_nonzero and p == 2:
        raise ValueError("require_nonzero mode requires an odd supplied prime")
    if not isinstance(columns, (list, tuple)) or not columns:
        raise ValueError("nonempty finite list/tuple of columns required")
    if any(not isinstance(col, (list, tuple)) for col in columns):
        raise ValueError("each column must be a finite list/tuple")
    bank = tuple(tuple(col) for col in columns)
    width, ambient = len(bank), len(bank[0])
    _shape_contract(rank_bound, width)
    if any(len(col) != ambient for col in bank):
        raise ValueError("rectangular columns required")
    if any(type(x) is not int or not 0 <= x < p for col in bank for x in col):
        raise ValueError("canonical integer field coordinates required")
    budget = random_column_budget(p, d, width, attempt_cap=attempt_cap,
                                  failure_bits=failure_bits)
    source = random.SystemRandom() if bit_source is None else bit_source
    if isinstance(source, type):
        raise ValueError("bit_source must be an instance with getrandbits")
    rng = CappedUniformRandom(source, call_cap=budget["uniform_call_cap"],
                             rejection_cap=budget["integer_rejection_cap"], max_interval=p)
    rows = list(map(list, zip(*bank)))
    reduced, rank = _fmpz_rref(rows, p)
    result = {
        "status": "ABORT", "reason": None, "weights": None, "power_vector": None,
        "p": p, "d": d, "columns": bank, "rank": rank,
        "require_nonzero": require_nonzero,
        "rank_bound": rank_bound, "kernel_dimension": width-rank, "budget": budget,
        "attempts": 0, "completed_kernel_draws": 0,
        "zero_rejections": 0, "zero_coordinate_rejections": 0, "nonpower_rejections": 0,
        "kernel_uniform_calls": 0, "root_uniform_calls": 0, "root_calls": 0,
        "root_split_trials": 0, "root_proper_splits": 0,
        "root_split_counts_complete": True, "exact_verified": False,
        "input_labels_resampled": False, "field_enumeration_used": False,
        "iid_uniform_columns_verified": False, "iid_fair_bits_verified": False,
        "supplied_prime_verified_by_this_api": False,
        "prime_validation_locally_clocked": False,
        "arbitrary_fixed_bank_success_bound": None,
        "quantum_receiver_implemented": False, "hsp_claim": False,
        "speedup_claim": False,
    }

    def finish(reason, weights=None, power_vector=None):
        result.update(reason=reason, uniform_calls=rng.calls, bit_draws=rng.bit_draws,
                      random_bits=rng.random_bits)
        if weights is not None:
            if (len(weights) != width or not any(weights)
                    or (require_nonzero and any(s == 0 for s in weights))
                    or any(type(s) is not int or not 0 <= s < p for s in weights)
                    or tuple(pow(s, d, p) for s in weights) != tuple(power_vector)
                    or any(sum(pow(s, d, p)*col[j] for s, col in zip(weights, bank)) % p
                           for j in range(ambient))):
                raise ArithmeticError("invalid exact power-kernel witness")
            result.update(status="VERIFIED", weights=tuple(weights),
                          power_vector=tuple(power_vector), exact_verified=True)
        return result

    if rank > rank_bound:
        return finish("OBSERVED_RANK_EXCEEDS_PROMISE")
    if rank == 0:
        vector = (1,)*width if require_nonzero else (1,)+(0,)*(width-1)
        return finish("ZERO_BANK_DETERMINISTIC", vector, vector)
    if p == 2:
        # d=1 here. The existing nullspace helper only accepts odd primes;
        # its RREF backend still gives this deterministic binary witness.
        pivots = [next(i for i, x in enumerate(row) if x) for row in reduced]
        free = next(i for i in range(width) if i not in pivots)
        vector = [0]*width
        vector[free] = 1
        for pivot, row in zip(pivots, reduced):
            vector[pivot] = (-row[free]) % p
        return finish("LINEAR_DETERMINISTIC", vector, vector)
    basis = _fmpz_nullspace_basis(rows, width, p)
    if len(basis) != width-rank:
        raise ArithmeticError("full kernel dimension mismatch")
    if d == 1 and not require_nonzero:
        return finish("LINEAR_DETERMINISTIC", basis[0], basis[0])

    for _ in range(attempt_cap):
        result["attempts"] += 1
        before = rng.calls
        try:
            coefficients = [rng.randrange(0, p) for _ in basis]
        except RandomnessExhausted:
            return finish("BIT_REJECTION_CAP")
        finally:
            result["kernel_uniform_calls"] += rng.calls-before
        vector = tuple(sum(c*b[i] for c, b in zip(coefficients, basis)) % p
                       for i in range(width))
        result["completed_kernel_draws"] += 1
        if not any(vector):
            result["zero_rejections"] += 1
            continue
        if require_nonzero and any(x == 0 for x in vector):
            result["zero_coordinate_rejections"] += 1
            continue
        if any(x and pow(x, (p-1)//d, p) != 1 for x in vector):
            result["nonpower_rejections"] += 1
            continue
        if d == 1:
            return finish("EXACT_POWER_KERNEL", vector, vector)
        weights = [0]*width
        for i, x in enumerate(vector):
            if x == 0:
                continue
            result["root_calls"] += 1
            before = rng.calls
            try:
                root = bounded_power_root(p, d, x, rng=rng,
                                          split_attempt_cap=budget["root_split_attempt_cap"])
            except RandomnessExhausted:
                result["root_split_counts_complete"] = False
                return finish("BIT_REJECTION_CAP")
            finally:
                result["root_uniform_calls"] += rng.calls-before
            result["root_split_trials"] += root.split_trials
            result["root_proper_splits"] += root.proper_splits
            if root.root is None:
                return finish("ROOT_SPLIT_CAP")
            if type(root.root) is not int or not 0 < root.root < p or pow(root.root, d, p) != x:
                raise ArithmeticError("root backend returned an invalid nonzero root")
            weights[i] = root.root
        return finish("EXACT_POWER_KERNEL", weights, vector)
    return finish("ATTEMPT_CAP")
