"""Public controller for a class-three filiform coherent Gram instrument.

Only central labels enter frame construction. The final controller consumes
a measured 3x3 Gram matrix, NEVER the individual noncentral characters.
This is exact classical arithmetic and a measurement descriptor, not an
emitted quantum circuit or a general nilpotent HSP implementation.
"""

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import gcd
from pathlib import Path
import random

from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.bounded_power_roots import bounded_power_root
from theorems.power_sde_budget import CappedUniformRandom, RandomnessExhausted
from theorems.prime_character_opi import ring


def _word(values, size, p):
    if not isinstance(values, (tuple, list)) or len(values) != size:
        raise ValueError("field vector has the wrong shape")
    if any(type(x) is not int or not 0 <= x < p for x in values):
        raise ValueError("canonical integer field entries required")
    return tuple(values)


def _matrix(values, size, p):
    if not isinstance(values, (tuple, list)) or len(values) != size:
        raise ValueError("square Gram matrix required")
    result = tuple(_word(row, size, p) for row in values)
    if any(result[i][j] != result[j][i] for i in range(size) for j in range(size)):
        raise ValueError("symmetric Gram matrix required")
    return result


def _combine(coefficients, rows, p):
    return tuple(sum(a * row[j] for a, row in zip(coefficients, rows)) % p
                 for j in range(len(rows[0])))


def _basis(rows, p):
    if not rows:
        return ()
    reduced, rank = fmpz_mod_mat(list(map(list, rows)), fmpz_mod_ctx(p)).rref()
    return tuple(tuple(int(reduced[i, j]) for j in range(len(rows[0])))
                 for i in range(int(rank)))


def _bilinear(gram, x, y, p):
    return sum(x[i] * gram[i][j] * y[j]
               for i in range(len(gram)) for j in range(len(gram))) % p


def _identity(size):
    return tuple(tuple(int(i == j) for i in range(size)) for j in range(size))


def _diagonalize(gram, p):
    remaining, result = _identity(len(gram)), []
    while remaining:
        v = next((x for x in remaining if _bilinear(gram, x, x, p)), None)
        if v is None:
            pair = next(((x, y) for x in remaining for y in remaining
                         if _bilinear(gram, x, y, p)), None)
            if pair is None:
                return tuple(result) + tuple((0, x) for x in remaining)
            v = tuple((x + y) % p for x, y in zip(*pair))
        value = _bilinear(gram, v, v, p)
        result.append((value, v))
        inverse = pow(value, -1, p)
        remaining = _basis([
            tuple((xj - _bilinear(gram, x, v, p) * inverse * vj) % p
                  for xj, vj in zip(x, v)) for x in remaining
        ], p)
    return tuple(result)


@dataclass(frozen=True)
class SelectorWitness:
    coordinates: tuple[int, ...]
    scales: tuple[int, ...]
    uniform_calls: int
    random_bits: int


class FiliformGramController:
    """One bounded controller run; the supplied prime must be >3.

    Fresh uniform getrandbits is an assumption, not certified by seeded tests.
    Public root/conic/bit rejection can raise RandomnessExhausted: the whole
    run must then report ABORT. Other errors are not silently converted to
    valid witnesses. Runtime of primality/backend arithmetic is separate.
    """

    def __init__(self, prime, ell, beta, *, failure_bits=32, bit_source=None):
        ring(prime)
        if prime <= 3:
            raise ValueError("class-three construction needs prime >3")
        if type(failure_bits) is not int or failure_bits < 1:
            raise ValueError("positive integer failure_bits required")
        self.prime = prime
        self.arity = 13 + gcd(3, prime - 1)
        self.ell = _word(ell, self.arity, prime)
        self.beta = _word(beta, self.arity, prime)
        self.failure_bits = failure_bits
        self.attempt_cap = 3 * (failure_bits + 6)
        calls = 50 * self.attempt_cap
        rejection = failure_bits + 2 + (calls - 1).bit_length()
        self.abort_bound = (22 * Fraction(2, 3) ** self.attempt_cap
                            + Fraction(calls, 2 ** rejection))
        if self.abort_bound > Fraction(1, 2 ** failure_bits):
            raise ArithmeticError("failure allocation exceeded")
        self.rng = CappedUniformRandom(
            random.SystemRandom() if bit_source is None else bit_source,
            call_cap=calls, rejection_cap=rejection, max_interval=prime,
        )
        self.root_calls = self.conic_calls = 0
        self._used = False
        cubic = self._cubic_frame()
        beta_gram = tuple(tuple(sum(b * x * y for b, x, y in
                                    zip(self.beta, u, v)) % prime
                                for v in cubic) for u in cubic)
        coefficients = self._totally_isotropic(beta_gram, 3)
        self.frame = tuple(_combine(v, cubic, prime) for v in coefficients)
        self.verify_frame()
        self.gram_entries = tuple(combinations_with_replacement(range(3), 2))
        self.measurement_rows = tuple(tuple(u * v % prime for u, v in
                                            zip(self.frame[j], self.frame[k]))
                                      for j, k in self.gram_entries)

    def _root(self, degree, value):
        p = self.prime
        if not value:
            return 0
        if gcd(degree, p - 1) == 1:
            return pow(value, pow(degree, -1, p - 1), p)
        self.root_calls += 1
        if self.root_calls > 11:
            raise ArithmeticError("root-call budget violated")
        result = bounded_power_root(p, degree, value, rng=self.rng,
                                    split_attempt_cap=self.attempt_cap)
        if result.root is None:
            raise RandomnessExhausted("bounded root splitting exhausted")
        return result.root

    def _cubic_frame(self):
        p, rows, waiting = self.prime, [], {}
        degree = gcd(3, p - 1)
        for i, value in enumerate(self.ell):
            row = [0] * self.arity
            if not value:
                row[i] = 1
            else:
                key = pow(value, (p - 1) // degree, p)
                if key not in waiting:
                    waiting[key] = i
                    continue
                j = waiting.pop(key)
                row[j] = 1
                row[i] = self._root(3, -self.ell[j] * pow(value, -1, p) % p)
            rows.append(tuple(row))
            if len(rows) == 7:
                return tuple(rows)
        raise ArithmeticError("cubic class packing did not supply seven directions")

    def _isotropic(self, gram):
        p = self.prime
        diagonal = _diagonalize(gram, p)
        zero = next((v for a, v in diagonal if not a), None)
        if zero is not None:
            return zero
        if len(diagonal) < 3:
            raise ValueError("nondegenerate quadratic search requires dimension >=3")
        (a, u), (b, v), (c, w) = diagonal[:3]
        self.conic_calls += 1
        if self.conic_calls > 4:
            raise ArithmeticError("conic-call budget violated")
        for _ in range(self.attempt_cap):
            x = self.rng.randrange(0, p)
            square = (-c - a * x * x) * pow(b, -1, p) % p
            if not square or pow(square, (p - 1) // 2, p) == 1:
                y = self._root(2, square)
                result = tuple((x * ui + y * vi + wi) % p
                               for ui, vi, wi in zip(u, v, w))
                if not any(result) or _bilinear(gram, result, result, p):
                    raise ArithmeticError("invalid quadratic witness")
                return result
        raise RandomnessExhausted("bounded conic search exhausted")

    def _totally_isotropic(self, gram, size):
        p, space, selected = self.prime, _identity(len(gram)), []
        for _ in range(size):
            restricted = tuple(tuple(_bilinear(gram, x, y, p) for y in space)
                               for x in space)
            coefficients = self._isotropic(restricted)
            v = _combine(coefficients, space, p)
            selected.append(v)
            row = tuple(_bilinear(gram, v, x, p) for x in space)
            pivot = next((i for i, x in enumerate(row) if x), None)
            if pivot is None:
                orthogonal = space
            else:
                orthogonal = tuple(
                    tuple((xj - row[i] * pow(row[pivot], -1, p) * yj) % p
                          for xj, yj in zip(x, space[pivot]))
                    for i, x in enumerate(space) if i != pivot
                )
            # Choose a complement to v inside v-perp; do not discard the radical.
            independent = [v]
            for x in orthogonal:
                if len(_basis(independent + [x], p)) > len(independent):
                    independent.append(x)
            space = tuple(independent[1:])
        return tuple(selected)

    def verify_frame(self):
        p = self.prime
        if len(_basis(self.frame, p)) != 3:
            raise ArithmeticError("scale frame lost rank")
        for u, v in product(self.frame, repeat=2):
            if sum(b * x * y for b, x, y in zip(self.beta, u, v)) % p:
                raise ArithmeticError("beta quadratic restriction is nonzero")
        for u, v, w in product(self.frame, repeat=3):
            if sum(e * x * y * z for e, x, y, z in zip(self.ell, u, v, w)) % p:
                raise ArithmeticError("top trilinear restriction is nonzero")

    def select(self, measured_gram):
        """Consume ONE symmetric Gram outcome; no noncentral label vector accepted."""
        if self._used:
            raise ValueError("a controller run may consume only one Gram outcome")
        gram = _matrix(measured_gram, 3, self.prime)
        self._used = True
        t = self._isotropic(gram)
        scales = _combine(t, self.frame, self.prime)
        p = self.prime
        if (not any(scales)
                or sum(e * s ** 3 for e, s in zip(self.ell, scales)) % p
                or sum(b * s * s for b, s in zip(self.beta, scales)) % p
                or _bilinear(gram, t, t, p)):
            raise ArithmeticError("selected scale failed its public certificate")
        return SelectorWitness(t, scales, self.rng.calls, self.rng.random_bits)


def report():
    """Replay arithmetic/covariance controls; alpha is a reference fixture only."""
    cases = []
    for p, zero_top, zero_beta in ((5, False, False), (7, False, False),
                                  (13, False, False), ((1 << 127)-1, False, False),
                                  (7, True, False), (5, True, True)):
        fixture = random.Random(20261030)
        arity = 13 + gcd(3, p-1)
        ell = tuple(0 if zero_top else fixture.randrange(p) for _ in range(arity))
        beta = tuple(0 if zero_beta else fixture.randrange(p) for _ in range(arity))
        alpha = tuple(fixture.randrange(p) for _ in range(arity))
        controller = FiliformGramController(p, ell, beta, bit_source=fixture)
        frame = controller.frame
        gram = tuple(tuple(sum(a*x*y for a, x, y in zip(alpha, u, v)) % p
                           for v in frame) for u in frame)
        witness = controller.select(gram)
        s = witness.scales
        moments = (sum(a*x*x for a, x in zip(alpha, s)) % p,
                   sum(b*x*x for b, x in zip(beta, s)) % p,
                   sum(e*x**3 for e, x in zip(ell, s)) % p)
        moved = tuple((a+e*x) % p for a, e, x in zip(alpha, ell, s))
        moved_gram = tuple(tuple(sum(a*x*y for a, x, y in zip(moved, u, v)) % p
                                 for v in frame) for u in frame)
        if any(moments) or moved_gram != gram:
            raise ArithmeticError("live Gram reference control failed")
        cases.append(dict(
            prime=p, zero_top=zero_top, zero_beta=zero_beta,
            lifted_source_count=arity, original_hiding_queries_per_bank=3*arity,
            matched_sequential_sufficient_count=6*(2 if p % 3 == 2 else 3),
            sequential_quadratic_arity=6,
            sequential_scalar_cubic_arity=2 if p % 3 == 2 else 3,
            fewer_sources_than_this_comparator=arity < 6*(2 if p % 3 == 2 else 3),
            central_ell=ell, central_beta=beta,
            reference_alpha=alpha, frame=frame, measurement_rows=controller.measurement_rows,
            gram_outcome=gram, coordinates=witness.coordinates, scales=s,
            moments=moments, gram_covariance_checked=True,
            root_calls=controller.root_calls, root_call_cap=11,
            conic_calls=controller.conic_calls, conic_call_cap=4,
            uniform_calls=witness.uniform_calls, uniform_call_cap=controller.rng.call_cap,
            random_bits=witness.random_bits,
            random_bit_cap=(controller.rng.call_cap*controller.rng.rejection_cap
                            *(p-1).bit_length()),
            failure_bits=controller.failure_bits, arithmetic_abort_bound=controller.abort_bound,
        ))
    root = Path(__file__).resolve().parents[1]
    sources = ("theorems/invariant_gram_selector.py", "theorems/bounded_power_roots.py",
               "theorems/power_sde_budget.py", "theorems/prime_character_opi.py",
               "theorems/cubic_diagonal_solver.py",
               "research/INVARIANT_GRAM_REES_RECEIVER.md",
               "research/HIGH_RANK_GRAM_DECISION.md",
               "research/GRAM_FRAME_SEARCH_BOUNDARY.md",
               "research/CUBIC_COLLISION_FRAME_OBSTRUCTION.md")
    return dict(
        status="PUBLIC_CONTROLLER_AND_EXACT_ARITHMETIC_CONTROLS_ONLY",
        public_controller_implemented=True, quantum_measurement_descriptor_implemented=True,
        quantum_receiver_implemented=False, quantum_execution_performed=False,
        gram_outcomes_are_classical_reference_inputs=True,
        general_rank_improvement_established=False, novelty_established=False,
        uniform_source_improvement_established=False,
        sequential_comparator_implemented_end_to_end=False,
        sequential_comparator_source="ISS2012 Section 5 Claim 1 plus scalar cubic root/curve solving",
        sequential_comparator_url="https://www.irif.fr/~santha/Papers/iss12.pdf#page=13",
        sequential_comparator_is_optimal=False,
        speedup_claim_allowed=False, candidate_promoted=False,
        complete_channel_proof="research/INVARIANT_GRAM_REES_RECEIVER.md",
        high_rank_follow_up="research/HIGH_RANK_GRAM_DECISION.md",
        high_rank_direction_promoted=False,
        source_sha256={path: sha256((root/path).read_bytes()).hexdigest() for path in sources},
        source_hash_scope="Selected direct sources, NOT a transitive dependency closure or proof",
        randomness_assumption="Fresh independent uniform bits; seeded fixtures do not certify this",
        compiled_quantum_precision_budget_available=False,
        cases=cases,
    )
