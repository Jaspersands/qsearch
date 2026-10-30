"""Uniform public-operation certificates, not a gate compiler or HSP solver.

Primality and the genuine Rees coordinate representation are input promises.
No loop enumerates F_p, a group, measurement labels, or a source tree here.
All accuracy bounds use half diamond distance for complete instruments.
"""

from dataclasses import asdict, dataclass
from fractions import Fraction


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _accuracy(value):
    if not isinstance(value, (int, Fraction)) or isinstance(value, bool):
        raise ValueError("use an exact rational accuracy")
    value = Fraction(value)
    if not 0 < value < 1:
        raise ValueError("accuracy must lie strictly between zero and one")
    return value


def _power_two_at_least(value):
    ceiling = (value.numerator + value.denominator - 1) // value.denominator
    return max(0, (ceiling - 1).bit_length())


@dataclass(frozen=True)
class CharacterPlan:
    prime: int
    rank: int
    accuracy: Fraction
    phase_bits_per_coordinate: int

    @property
    def phase_grid(self):
        return 1 << self.phase_bits_per_coordinate

    @property
    def powers(self):
        return tuple(pow(2, k, self.prime) for k in range(self.phase_bits_per_coordinate))

    @property
    def controlled_public_translations(self):
        return 2 * self.rank * self.phase_bits_per_coordinate

    @property
    def qft_blocks(self):
        return 2 * self.rank

    @property
    def controlled_rotations(self):
        t = self.phase_bits_per_coordinate
        return self.rank * t * (t - 1)

    @property
    def per_qft_operator_error(self):
        return self.accuracy / (4 * self.rank)

    @property
    def rounding_failure_bound(self):
        return Fraction(4 * self.rank * self.prime, self.phase_grid)

    @property
    def instrument_error_squared(self):
        # Ideal power-of-two QFTs, before the separate synthesis allocation.
        return 2 * self.rounding_failure_bound

    @property
    def phase_and_label_qubits(self):
        return self.rank * (self.phase_bits_per_coordinate + (self.prime - 1).bit_length())

    def report(self):
        return {
            **asdict(self),
            "accuracy": str(self.accuracy),
            "phase_grid": str(self.phase_grid),
            "public_power_constants": list(self.powers),
            "controlled_public_translations": self.controlled_public_translations,
            "power_two_qft_blocks": self.qft_blocks,
            "controlled_rotation_count_before_synthesis": self.controlled_rotations,
            "per_qft_operator_norm_error": str(self.per_qft_operator_error),
            "rounding_failure_bound": str(self.rounding_failure_bound),
            "ideal_qft_instrument_error_squared_bound": str(self.instrument_error_squared),
            "phase_and_label_qubits_excluding_target_and_decoder_work": self.phase_and_label_qubits,
            "hidden_source_inverse_calls": 0,
            "hidden_source_preparations_by_measurement": 0,
            "group_or_field_enumeration": False,
            "gate_level_compiler": False,
            "primality_certified": False,
        }


def character_plan(prime, rank, accuracy, *, public_fast_powers):
    """Compute--decode--uncompute, using R(e_j)^(2^k)=R(2^k e_j).

    The boolean is a contract declaration, NOT a verifier of an external
    circuit. Mere black-box access to U does not satisfy this contract.
    """
    _positive(prime, "promised prime")
    if prime < 3 or prime % 2 == 0:
        raise ValueError("this pass requires a promised odd prime")
    _positive(rank, "central rank")
    accuracy = _accuracy(accuracy)
    if public_fast_powers is not True:
        raise ValueError("public fast powers are required; repeated U calls are not free")
    bits = _power_two_at_least(Fraction(32 * rank * prime) / accuracy**2)
    return CharacterPlan(prime, rank, accuracy, bits)


def decode_phase(index, phase_bits, prime):
    """Nearest field residue on the circle; exact integer arithmetic."""
    _positive(phase_bits, "phase bits")
    _positive(prime, "modulus")
    grid = 1 << phase_bits
    if type(index) is not int or not 0 <= index < grid:
        raise ValueError("canonical phase index required")
    return ((2 * prime * index + grid) // (2 * grid)) % prime


def address_plan(prime, dimension, accuracy):
    """Capped public rejection prepares exact uniform coordinates on success.

    All attempts occur before native targets are acquired. Failure is an
    explicit abort, not postselection on hidden information.
    """
    _positive(prime, "promised prime")
    if prime < 3 or prime % 2 == 0:
        raise ValueError("this pass requires a promised odd prime")
    _positive(dimension, "address dimension")
    accuracy = _accuracy(accuracy)
    bits = (prime - 1).bit_length()
    attempts = _power_two_at_least(Fraction(dimension) / accuracy)
    failure = dimension * (1 - Fraction(prime, 1 << bits))**attempts
    return {
        "coordinate_bits": bits,
        "dimension": dimension,
        "attempts_per_coordinate_cap": attempts,
        "public_attempts_cap": dimension * attempts,
        "complete_channel_abort_bound": str(failure),
        "accuracy": str(accuracy),
        "uniform_on_every_successful_record": True,
        "native_copies_consumed_before_success": 0,
        "source_inverse_calls": 0,
        "primality_certified": False,
    }


def terminal_sampling_plan(prime, dimension, rank_failure_budget):
    """Worst-case span bound; measurement/source errors are paid separately."""
    _positive(prime, "promised prime")
    if prime < 3 or prime % 2 == 0:
        raise ValueError("this pass requires a promised odd prime")
    _positive(dimension, "terminal dimension")
    budget = _accuracy(rank_failure_budget)
    samples = dimension
    hyperplanes = (prime**dimension - 1) // (prime - 1)
    bound = Fraction(hyperplanes, prime**samples)
    while bound > budget:
        samples += 1
        bound /= prime
    return {
        "terminal_samples": samples,
        "ambient_dimension": dimension,
        "span_failure_union_bound": str(bound),
        "rank_failure_budget": str(budget),
        "unknown_hidden_dimension_used": False,
        "requires_independent_terminal_sources": True,
        "measurement_and_source_error_included": False,
    }
