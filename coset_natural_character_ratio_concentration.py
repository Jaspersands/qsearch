"""Natural-source character-ratio concentration for involution coset states.

Let ``C`` be a nonidentity conjugacy class of ``S_n`` and
``r_lambda = chi_lambda(C)/d_lambda``.  The weak-Fourier source law of the
order-two coset state is

    p_C(lambda) = d_lambda^2 (1 + r_lambda) / |S_n|.

Under Plancherel measure, column orthogonality gives

    E_Pl[r_lambda^2] = |C_G(g)|/|G| = 1/|C|.

Since ``|r_lambda| <= 1``,

    E_p[r_lambda^2]
      = E_Pl[r_lambda^2 + r_lambda^3]
      <= 2/|C|,

and therefore

    Pr_p(|r_lambda| > epsilon) <= 2/(|C| epsilon^2).

Weak source labels from independent coset states are iid under this law, so a
union bound controls every label in a growing-width source tuple.  For the
fixed-point-free involution class and ``k=ceil(n log2 n)``, the complete tuple
obeys ``|r_lambda| <= 1/sqrt(n)`` except with probability at most
``2 k n / |C|``, which is superpolynomially small.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    upsert_experiment_result,
    utc_now,
)
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "coset_natural_character_ratio_concentration.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CharacterRatioFiniteControl:
    n: int
    transposition_count: int
    conjugacy_class_size: int
    source_partition_count: int
    natural_source_mass: float
    plancherel_second_moment: float
    column_orthogonality_target: float
    column_orthogonality_residual: float
    natural_second_moment: float
    natural_second_moment_upper_bound: float
    epsilon: float
    exact_single_source_tail_probability: float
    markov_single_source_tail_bound: float
    required_joint_copy_count: int
    exact_tuple_tail_union_bound: float
    theorem_tuple_tail_union_bound: float
    status: str


@dataclass(frozen=True)
class CharacterRatioScalingRecord:
    n: int
    required_joint_copy_count: int
    epsilon: float
    conjugacy_class_log2_size: float
    theorem_tuple_failure_probability_upper_bound: float
    theorem_tuple_failure_log2_upper_bound: float
    inverse_polynomial_failure_upper_bound: bool
    status: str


@dataclass(frozen=True)
class NaturalCharacterRatioConcentrationReport:
    created_at: str
    theorem_contract: dict[str, object]
    finite_controls: list[CharacterRatioFiniteControl]
    scaling_records: list[CharacterRatioScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def involution_class_size(n: int, transposition_count: int) -> int:
    if transposition_count < 0 or 2 * transposition_count > n:
        raise ValueError("invalid transposition count")
    return math.factorial(n) // (
        (2**transposition_count)
        * math.factorial(transposition_count)
        * math.factorial(n - 2 * transposition_count)
    )


def _finite_control(
    n: int,
    transposition_count: int,
) -> CharacterRatioFiniteControl:
    order = math.factorial(n)
    class_size = involution_class_size(n, transposition_count)
    epsilon = 1 / math.sqrt(n)
    source_mass = 0.0
    plancherel_second = 0.0
    natural_second = 0.0
    exact_tail = 0.0
    partitions = integer_partitions(n)
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        character = character_on_involution(
            partition,
            transposition_count,
        )
        ratio = character / dimension
        plancherel = dimension * dimension / order
        natural = plancherel * (1.0 + ratio)
        source_mass += natural
        plancherel_second += plancherel * ratio * ratio
        natural_second += natural * ratio * ratio
        if abs(ratio) > epsilon:
            exact_tail += natural
    target = 1 / class_size
    single_bound = min(1.0, 2 / (class_size * epsilon * epsilon))
    copies = math.ceil(n * math.log2(n))
    return CharacterRatioFiniteControl(
        n=n,
        transposition_count=transposition_count,
        conjugacy_class_size=class_size,
        source_partition_count=len(partitions),
        natural_source_mass=source_mass,
        plancherel_second_moment=plancherel_second,
        column_orthogonality_target=target,
        column_orthogonality_residual=abs(plancherel_second - target),
        natural_second_moment=natural_second,
        natural_second_moment_upper_bound=2 / class_size,
        epsilon=epsilon,
        exact_single_source_tail_probability=exact_tail,
        markov_single_source_tail_bound=single_bound,
        required_joint_copy_count=copies,
        exact_tuple_tail_union_bound=min(1.0, copies * exact_tail),
        theorem_tuple_tail_union_bound=min(1.0, copies * single_bound),
        status="exact-natural-source-character-ratio-control",
    )


def _scaling_record(n: int) -> CharacterRatioScalingRecord:
    transpositions = n // 2
    class_size = involution_class_size(n, transpositions)
    copies = math.ceil(n * math.log2(n))
    epsilon = 1 / math.sqrt(n)
    bound = min(1.0, 2 * copies * n / class_size)
    log_bound = math.log2(bound) if bound > 0 else -math.inf
    inverse_polynomial = bound <= n**-3
    return CharacterRatioScalingRecord(
        n=n,
        required_joint_copy_count=copies,
        epsilon=epsilon,
        conjugacy_class_log2_size=math.log2(class_size),
        theorem_tuple_failure_probability_upper_bound=bound,
        theorem_tuple_failure_log2_upper_bound=log_bound,
        inverse_polynomial_failure_upper_bound=inverse_polynomial,
        status=(
            "natural-growing-width-character-envelope-overwhelming"
            if inverse_polynomial
            else "finite-bound-not-yet-inverse-polynomial"
        ),
    )


def build_natural_character_ratio_concentration_report(
    finite_n_values: tuple[int, ...] = (6, 8, 10, 12, 14, 16),
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64, 128),
) -> NaturalCharacterRatioConcentrationReport:
    finite = [
        _finite_control(n, n // 2)
        for n in finite_n_values
    ]
    scaling = [_scaling_record(n) for n in scaling_n_values]
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "finite_control_count": len(finite),
        "column_orthogonality_identity_count": 1,
        "natural_second_moment_bound_theorem_count": 1,
        "iid_growing_width_union_bound_theorem_count": 1,
        "uniform_natural_source_character_ratio_theorem_count": 1,
        "finite_column_orthogonality_failure_count": sum(
            record.column_orthogonality_residual > 1e-10
            for record in finite
        ),
        "finite_natural_source_mass_failure_count": sum(
            abs(record.natural_source_mass - 1.0) > 1e-10
            for record in finite
        ),
        "finite_natural_second_moment_bound_failure_count": sum(
            record.natural_second_moment
            > record.natural_second_moment_upper_bound + 1e-12
            for record in finite
        ),
        "maximum_column_orthogonality_residual": max(
            record.column_orthogonality_residual for record in finite
        ),
        "scaling_record_count": len(scaling),
        "inverse_polynomial_tuple_envelope_row_count": sum(
            record.inverse_polynomial_failure_upper_bound
            for record in scaling
        ),
        "tail_n": tail.n,
        "tail_tuple_failure_log2_upper_bound": (
            tail.theorem_tuple_failure_log2_upper_bound
        ),
        "pgm_measurement_circuit_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
    }
    return NaturalCharacterRatioConcentrationReport(
        created_at=utc_now(),
        theorem_contract={
            "source_law": (
                "p_C(lambda)=d_lambda^2(1+r_lambda)/|S_n| for "
                "r_lambda=chi_lambda(C)/d_lambda."
            ),
            "column_orthogonality": (
                "E_Plancherel[r_lambda^2]=1/|C| for real symmetric-group "
                "characters."
            ),
            "natural_second_moment": (
                "E_p[r^2]=E_Pl[r^2+r^3] <= 2/|C| because |r|<=1."
            ),
            "tuple_bound": (
                "For k iid weak source labels, "
                "Pr[max_i |r_i|>epsilon] <= 2k/(|C|epsilon^2)."
            ),
            "fixed_point_free_specialization": (
                "|C|=n!/(2^(n/2)(n/2)!), k=ceil(n log2 n), "
                "epsilon=1/sqrt(n), failure <=2kn/|C|."
            ),
            "scope": (
                "This proves a natural-source character-ratio envelope. It "
                "does not implement the PGM frame inverse or decoder."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "natural_source_character_ratio_envelope_proved": True,
            "growing_width_iid_source_tuple_controlled": True,
            "average_frame_generic_normalization_barrier_unconditional_on_tail": True,
            "pgm_measurement_circuit_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural source law now validates the small-character-ratio "
                "envelope with overwhelming probability, strengthening the "
                "direct frame-normalization obstruction rather than providing "
                "a measurement."
            ),
        },
        status="natural-character-ratio-envelope-proved-pgm-still-blocked",
        summary=(
            "Proved the complete natural-source character-ratio concentration "
            "bound and growing-width union bound. At "
            f"n={tail.n}, the tuple failure upper bound has log2 at most "
            f"{tail.theorem_tuple_failure_log2_upper_bound:.3f}; direct "
            "average-frame normalization is no longer blocked on a "
            "conditional source assumption."
        ),
        falsifiers_triggered=[
            (
                "The hard-sector small-character-ratio envelope is not a "
                "selected-source assumption; it holds with overwhelming "
                "probability under the complete natural source law."
            ),
            (
                "Weak source labels are iid because their distribution is "
                "constant across the hidden conjugacy class."
            ),
            (
                "Character-ratio concentration strengthens the direct "
                "normalization barrier; it does not solve frame inversion."
            ),
            (
                "The theorem does not lower-bound every possible collective "
                "measurement or direct covariant implementation."
            ),
        ],
    )


def write_natural_character_ratio_concentration_report(
    output_path: Path = REPORT_PATH,
    *,
    finite_n_values: tuple[int, ...] = (6, 8, 10, 12, 14, 16),
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64, 128),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_natural_character_ratio_concentration_report(
            finite_n_values=finite_n_values,
            scaling_n_values=scaling_n_values,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_natural_character_ratio_concentration_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
