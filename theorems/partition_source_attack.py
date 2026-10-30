"""Classical callable-f recovery of partition-source Pauli symmetries.

For K(x,y)=1[f(x)=f(y)] and rho=K/p**n, the supplied promises are exact
diagonality in ONE common maximal Pauli eigenbasis, purity >= 1/R,
and every positive ABSOLUTE Pauli conjugation
loss >= delta. They are never certified here. Under these promises and IID
uniform random bits, recovery succeeds with probability at least 1-error
unless an optional query cap truncates execution. Seeded bits are controls,
not a certification of the randomness assumption.

D is spanned by equal-label differences, T preserves K under translation,
and the target is T x D-perp in global (x,z) coordinates. Diagonality gives
D subset T; purity <= |D|/p**n bounds the quotient by R. Sampling extends
every proper D subspace with probability >= delta/2. Translation mismatch
has mean twice the X_t loss, hence is zero on T and >= 2*delta otherwise.
No density matrix, hidden subspace, or full field list is used.
"""
from dataclasses import dataclass
from fractions import Fraction
from random import SystemRandom

from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _basis


def _ceil(value):
    return -(-value.numerator // value.denominator)


def _caps(p, n, R, delta, error):
    """Exact public clocks; delta and error must be exact Fractions."""
    if type(p) is not int:
        raise ValueError("prime integer required")
    if p != 2:
        ring(p)
    if any(type(v) is not int or v < 1 for v in (n, R)):
        raise ValueError("n and R must be positive integers")
    if not isinstance(delta, Fraction) or not 0 < delta <= 1:
        raise ValueError("delta must be a Fraction in (0,1]")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("error must be a Fraction in (0,1)")
    beta = error / 3
    C = _ceil(16 * (n + ceil_log(2, 1 / beta)) / delta)
    V = _ceil(Fraction(ceil_log(2, R / beta), 1) / (2 * delta))
    M = 2 * n * (C + R * V)
    L = ceil_log(2, M / beta)
    bits = (p - 1).bit_length()
    return {
        "beta": beta,
        "collision_pair_cap": C,
        "verification_pairs_per_representative": V,
        "quotient_cap": R,
        "field_draw_cap": M,
        "field_rejection_attempt_cap": L,
        "bits_per_attempt": bits,
        "random_bit_cap": M * L * bits,
        "query_bound": 2 * C + 4 * R * V,
        "randomness_abort_bound": Fraction(M, 2**L),
        "source_promises_certified": False,
    }


@dataclass(frozen=True)
class PartitionSourcePlan:
    """Public resource parameters and unverified source promises."""

    prime: int
    width: int
    inverse_purity: int
    gap: Fraction
    error: Fraction = Fraction(1, 3)

    def __post_init__(self):
        self.caps()

    def caps(self):
        return _caps(self.prime, self.width, self.inverse_purity, self.gap, self.error)


def _insert(rows, vector, p):
    """Maintain at most n independent RREF rows, never a collision history."""
    residual = list(vector)
    for row in rows:
        pivot = next(i for i, x in enumerate(row) if x)
        coefficient = residual[pivot]
        residual = [(x - coefficient * y) % p for x, y in zip(residual, row)]
    return _basis(rows + [residual], p) if any(residual) else rows


def _quotient_representatives(p, n, free, size):
    # Base-p digits avoid itertools.product's materialized range(p) pools.
    for index in range(size):
        vector = [0] * n
        for column in free:
            index, vector[column] = divmod(index, p)
        yield tuple(vector)


class _Abort(Exception):
    pass


def recover_partition_symmetry(plan, evaluator, *, rng=None, query_cap=None):
    """Query deterministic equality-comparable labels on canonical tuples.

    Only equality is used: labels need not be numeric, ordered, or hashable.
    Returns SUCCESS or ABORT_{QUOTIENT_CAP,RANDOMNESS_CAP,QUERY_CAP}, with
    actual counters on every path. Aborts expose no symmetry generators.
    SUCCESS is conditional recovery, not certification of the promises.
    rng must supply getrandbits(k); None selects a fresh SystemRandom.
    Caller/RNG exceptions propagate; malformed random outputs raise ValueError.
    """
    if not isinstance(plan, PartitionSourcePlan):
        raise ValueError("PartitionSourcePlan required")
    caps = plan.caps()
    p, n, R = plan.prime, plan.width, plan.inverse_purity
    if not callable(evaluator):
        raise ValueError("evaluator must be callable")
    if query_cap is not None and (type(query_cap) is not int or query_cap < 0):
        raise ValueError("query_cap must be a nonnegative integer or None")
    if rng is None:
        rng = SystemRandom()
    getrandbits = getattr(rng, "getrandbits", None)
    if not callable(getrandbits):
        raise ValueError("getrandbits must be callable")
    counts = dict(queries=0, random_bits=0, random_bit_calls=0, field_draws=0,
                  collision_pairs=0, verification_pairs=0,
                  representatives_tested=0, representatives_accepted=0,
                  peak_collision_rows=0)
    rows, translations, phases = [], [], []
    quotient_size = None

    def field():
        bits = caps["bits_per_attempt"]
        for _ in range(caps["field_rejection_attempt_cap"]):
            counts["random_bits"] += bits
            counts["random_bit_calls"] += 1
            value = getrandbits(bits)
            if type(value) is not int or not 0 <= value < 1 << bits:
                raise ValueError("getrandbits returned an invalid bit string")
            if value < p:
                counts["field_draws"] += 1
                return value
        raise _Abort("ABORT_RANDOMNESS_CAP")

    def point():
        return tuple(field() for _ in range(n))

    def query(x):
        if query_cap is not None and counts["queries"] >= query_cap:
            raise _Abort("ABORT_QUERY_CAP")
        counts["queries"] += 1
        return evaluator(x)

    def result(status):
        success = status == "SUCCESS"
        zero = (0,) * n
        t_basis = tuple(map(tuple, translations)) if success else ()
        z_basis = tuple(map(tuple, phases)) if success else ()
        return {
            "status": status,
            "source_promises_certified": False,
            "caps": caps,
            "counts": counts.copy(),
            "collision_basis": tuple(map(tuple, rows)),
            "quotient_size": quotient_size,
            "translation_basis": t_basis,
            "phase_basis": z_basis,
            "pauli_generators": tuple(t + zero for t in t_basis)
                                + tuple(zero + z for z in z_basis),
        }

    try:
        for _ in range(caps["collision_pair_cap"]):
            x, y = point(), point()
            equal = query(x) == query(y)
            counts["collision_pairs"] += 1
            if equal:
                rows = _insert(rows, [(a - b) % p for a, b in zip(x, y)], p)
                counts["peak_collision_rows"] = max(counts["peak_collision_rows"], len(rows))
        quotient_size = p ** (n - len(rows))
        if quotient_size > R:
            return result("ABORT_QUOTIENT_CAP")

        pivots = [next(i for i, x in enumerate(row) if x) for row in rows]
        free = [i for i in range(n) if i not in pivots]
        for column in free:
            vector = [int(i == column) for i in range(n)]
            for pivot, row in zip(pivots, rows):
                vector[pivot] = -row[column] % p
            phases.append(vector)
        translations = [row[:] for row in rows]
        for t in _quotient_representatives(p, n, free, quotient_size):
            counts["representatives_tested"] += 1
            for _ in range(caps["verification_pairs_per_representative"]):
                x, y = point(), point()
                before = query(x) == query(y)
                after = (query(tuple((a + b) % p for a, b in zip(x, t)))
                         == query(tuple((a + b) % p for a, b in zip(y, t))))
                counts["verification_pairs"] += 1
                if before != after:
                    break
            else:
                counts["representatives_accepted"] += 1
                translations = _insert(translations, t, p)
        return result("SUCCESS")
    except _Abort as exc:
        return result(str(exc))
