"""Character-ratio proof contract for collision-free wreath frames.

For an unequal physical irrep induced from distinct S_n irreps lambda, mu,
the normalized character of a base element (a,b,0) is

    r_{lambda,mu}(a,b)
      = [r_lambda(a)r_mu(b)+r_mu(a)r_lambda(b)]/2,

and its character vanishes on the swap coset.  Therefore every fixed
collision-free frame moment can be expanded into products of ordinary
symmetric-group character ratios evaluated on subset bridge words.

Féray-Sniady bound those ratios in terms of diagram rows/columns and the
transposition length of the word.  Hypercontractive and sharp class-walk
bounds offer stronger aggregate tools.  To prove the sufficient frame bound

    ||B|| <= poly(n) 2^{-k},

the missing step is not another character identity.  It is a joint
anti-concentration theorem showing that correlated subset words with short
transposition length contribute little after multiplying ratios from all k
globally distinct source partitions.

This module formalizes that proof contract, validates the unequal-character
factorization exactly, and stress-tests the finite constants.  It does not
claim the missing short-word or all-n norm theorem.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_character_moments import (
    permutation_cycle_type,
    physical_wreath_character,
    unequal_pair_descriptor,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_character_ratio_contract.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

CHARACTER_BOUND_LITERATURE = (
    {
        "id": "feray-sniady-character-bounds-2007",
        "url": "https://arxiv.org/abs/math/0701051",
        "role": (
            "pointwise normalized-character decay from diagram geometry and "
            "transposition length"
        ),
    },
    {
        "id": "lifshitz-marmor-hypercontractive-characters-2023",
        "url": "https://arxiv.org/abs/2308.08694",
        "role": (
            "character Lp bounds, Fourier coefficients, and product mixing"
        ),
    },
    {
        "id": (
            "olesker-taylor-teyssier-thevenin-"
            "character-cutoff-2025"
        ),
        "url": "https://arxiv.org/abs/2503.12735",
        "role": "sharp uniform character bounds and class-walk cutoff",
    },
)


@dataclass(frozen=True)
class CharacterFactorizationValidationRecord:
    n: int
    unequal_irrep_count: int
    wreath_element_count: int
    maximum_absolute_residual: float
    failed_element_count: int
    exact_factorization_verified: bool


@dataclass(frozen=True)
class CharacterRatioStressRecord:
    n: int
    partition: tuple[int, ...]
    dimension: int
    row_count: int
    column_count: int
    maximum_nonidentity_character_ratio: float
    maximum_required_feray_sniady_constant_proxy: float
    maximizing_cycle_type: tuple[int, ...]
    finite_constant_probe_only: bool
    status: str


@dataclass(frozen=True)
class CharacterRatioScalingRequirement:
    n: int
    copy_count: int
    required_moment_order: int
    log2_exact_frame_scale_target: float
    log2_quadratic_polynomial_slack_target: float
    source_partition_draw_count: int
    required_joint_short_word_tail_bound: str
    simultaneous_typical_shape_tail_proved: bool
    joint_short_word_anticoncentration_proved: bool
    collision_free_polynomial_factor_norm_proved: bool
    status: str


@dataclass(frozen=True)
class CharacterRatioProofObligation:
    id: str
    statement: str
    status: str
    dependencies: tuple[str, ...]
    falsifier: str


@dataclass(frozen=True)
class CharacterRatioContractReport:
    created_at: str
    literature: tuple[dict[str, str], ...]
    theorem_contract: dict[str, Any]
    factorization_validations: list[
        CharacterFactorizationValidationRecord
    ]
    stress_records: list[CharacterRatioStressRecord]
    scaling_requirements: list[CharacterRatioScalingRequirement]
    proof_obligations: list[CharacterRatioProofObligation]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def transposition_length(cycle_type: tuple[int, ...]) -> int:
    return sum(cycle_type) - len(cycle_type)


def normalized_symmetric_character(
    partition: tuple[int, ...],
    cycle_type: tuple[int, ...],
) -> Fraction:
    return Fraction(
        symmetric_character(partition, cycle_type),
        hook_length_dimension(partition),
    )


def factorized_unequal_character_ratio(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    left_permutation: tuple[int, ...],
    right_permutation: tuple[int, ...],
    swap: int,
) -> Fraction:
    if swap:
        return Fraction()
    left_cycle = permutation_cycle_type(left_permutation)
    right_cycle = permutation_cycle_type(right_permutation)
    return (
        normalized_symmetric_character(left_partition, left_cycle)
        * normalized_symmetric_character(right_partition, right_cycle)
        + normalized_symmetric_character(right_partition, left_cycle)
        * normalized_symmetric_character(left_partition, right_cycle)
    ) / 2


def validate_unequal_character_factorization(
    n: int,
    tolerance: float = 1e-12,
) -> CharacterFactorizationValidationRecord:
    partitions = integer_partitions(n)
    descriptors = tuple(
        unequal_pair_descriptor(left, right)
        for left_index, left in enumerate(partitions)
        for right in partitions[left_index + 1 :]
    )
    permutations = tuple(itertools.permutations(range(n)))
    failures = 0
    maximum_residual = 0.0
    for descriptor in descriptors:
        for left in permutations:
            for right in permutations:
                for swap in (0, 1):
                    element = (left, right, swap)
                    direct = Fraction(
                        physical_wreath_character(descriptor, element),
                        descriptor.dimension,
                    )
                    factorized = factorized_unequal_character_ratio(
                        descriptor.left_partition,
                        descriptor.right_partition,
                        left,
                        right,
                        swap,
                    )
                    residual = abs(float(direct - factorized))
                    maximum_residual = max(maximum_residual, residual)
                    failures += residual > tolerance
    return CharacterFactorizationValidationRecord(
        n=n,
        unequal_irrep_count=len(descriptors),
        wreath_element_count=2 * math.factorial(n) ** 2,
        maximum_absolute_residual=maximum_residual,
        failed_element_count=failures,
        exact_factorization_verified=failures == 0,
    )


def character_ratio_stress_record(
    n: int,
    partition: tuple[int, ...],
) -> CharacterRatioStressRecord:
    maximum_ratio = 0.0
    maximum_proxy = 0.0
    maximizing = (1,) * n
    rows = len(partition)
    columns = partition[0]
    for cycle_type in integer_partitions(n):
        length = transposition_length(cycle_type)
        if length == 0:
            continue
        ratio = abs(float(normalized_symmetric_character(
            partition,
            cycle_type,
        )))
        geometric_base = max(
            rows / n,
            columns / n,
            length / n,
        )
        proxy = (
            ratio ** (1 / length) / geometric_base
            if ratio > 0 and geometric_base > 0
            else 0.0
        )
        if ratio > maximum_ratio:
            maximum_ratio = ratio
            maximizing = cycle_type
        maximum_proxy = max(maximum_proxy, proxy)
    return CharacterRatioStressRecord(
        n=n,
        partition=partition,
        dimension=hook_length_dimension(partition),
        row_count=rows,
        column_count=columns,
        maximum_nonidentity_character_ratio=maximum_ratio,
        maximum_required_feray_sniady_constant_proxy=maximum_proxy,
        maximizing_cycle_type=maximizing,
        finite_constant_probe_only=True,
        status="finite-character-ratio-constant-stress",
    )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def run_character_ratio_contract() -> CharacterRatioContractReport:
    validations = [
        validate_unequal_character_factorization(n) for n in (2, 3, 4)
    ]
    stress_records = [
        character_ratio_stress_record(n, partition)
        for n in (5, 6, 7, 8)
        for partition in integer_partitions(n)
    ]
    wreath = _read_json(WREATH_PGM_PATH)
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    scaling = [
        CharacterRatioScalingRequirement(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            required_moment_order=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
            log2_exact_frame_scale_target=(
                1 - int(record["copy_count"])
            ),
            log2_quadratic_polynomial_slack_target=(
                1
                - int(record["copy_count"])
                + 2 * math.log2(int(record["n"]))
            ),
            source_partition_draw_count=2 * int(record["copy_count"]),
            required_joint_short_word_tail_bound=(
                "sum of collision-free subset-word terms not controlled by "
                "typical character decay <=poly(n) times the fully mixed term"
            ),
            simultaneous_typical_shape_tail_proved=False,
            joint_short_word_anticoncentration_proved=False,
            collision_free_polynomial_factor_norm_proved=False,
            status=(
                "character-bound-imported-short-word-"
                "anticoncentration-open"
            ),
        )
        for record in wreath.get("records", [])
    ]
    obligations = [
        CharacterRatioProofObligation(
            id="CR-UNEQUAL-FACTORIZATION",
            statement=(
                "Every unequal physical normalized character factors into "
                "two products of S_n normalized characters."
            ),
            status="proved",
            dependencies=("physical wreath induction formula",),
            falsifier="Any complete small-group element has nonzero residual.",
        ),
        CharacterRatioProofObligation(
            id="CR-SIMULTANEOUS-TYPICAL-SHAPE",
            statement=(
                "All 2k collision-free Plancherel source diagrams satisfy a "
                "uniform row/column bound strong enough for character decay."
            ),
            status="blocked-tail-not-quantified-in-registry",
            dependencies=(
                "Plancherel limit-shape concentration",
                "global source collision theorem",
            ),
            falsifier=(
                "The exceptional shape probability is not o(1/k)."
            ),
        ),
        CharacterRatioProofObligation(
            id="CR-SHORT-WORD-ANTICONCENTRATION",
            statement=(
                "Correlated bridge subset words with insufficient "
                "transposition length have total weighted contribution at "
                "most poly(n) times the mixed frame scale."
            ),
            status="open-critical",
            dependencies=(
                "feray-sniady-character-bounds-2007",
                "lifshitz-marmor-hypercontractive-characters-2023",
                "olesker-taylor-teyssier-thevenin-character-cutoff-2025",
            ),
            falsifier=(
                "A collision-free source family has a superpolynomial excess "
                "of low-length subset words with aligned character signs."
            ),
        ),
        CharacterRatioProofObligation(
            id="CR-COLLISION-FREE-NORM",
            statement=(
                "Every collision-free typical tuple obeys "
                "||B||<=poly(n)2^-k."
            ),
            status="open-critical",
            dependencies=(
                "CR-SIMULTANEOUS-TYPICAL-SHAPE",
                "CR-SHORT-WORD-ANTICONCENTRATION",
                "trace-moment certificate",
            ),
            falsifier=(
                "Verified growing-n collision-free spectra have "
                "superpolynomial top-to-2^-k ratio."
            ),
        ),
    ]
    failures = sum(
        record.failed_element_count for record in validations
    )
    maximum_proxy = max(
        record.maximum_required_feray_sniady_constant_proxy
        for record in stress_records
    )
    metrics: dict[str, int | float] = {
        "character_factorization_validation_count": len(validations),
        "character_factorization_failure_count": failures,
        "character_ratio_stress_record_count": len(stress_records),
        "maximum_character_ratio_stress_n": max(
            record.n for record in stress_records
        ),
        "maximum_finite_feray_sniady_constant_proxy": maximum_proxy,
        "literature_linked_character_bound_count": len(
            CHARACTER_BOUND_LITERATURE
        ),
        "exact_unequal_character_factorization_theorem_count": 1,
        "simultaneous_typical_shape_tail_theorem_count": 0,
        "joint_short_word_anticoncentration_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "collision_free_growing_moment_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = failures == 0
    return CharacterRatioContractReport(
        created_at=utc_now(),
        literature=CHARACTER_BOUND_LITERATURE,
        theorem_contract={
            "unequal_character_factorization": (
                "r_lam,mu(a,b,0)="
                "(r_lam(a)r_mu(b)+r_mu(a)r_lam(b))/2"
            ),
            "feray_sniady_input": (
                "|r_lambda(sigma)|<=[A max(rows/n,columns/n,"
                "|sigma|/n)]^|sigma|"
            ),
            "sufficient_norm_target": "||B||<=poly(n)2^-k",
            "moment_route": (
                "expand Tr(B^m), factor every unequal character, split subset "
                "words by transposition length, and control the short-word "
                "exception jointly across k distinct source partitions"
            ),
            "success_route": (
                "combine the norm upper bound with a typical second-moment "
                "lower bound and the projector-sub-POVM moment certificate"
            ),
        },
        factorization_validations=validations,
        stress_records=stress_records,
        scaling_requirements=scaling,
        proof_obligations=obligations,
        headline_metrics=metrics,
        claim_gate={
            "exact_unequal_character_factorization_proved": verified,
            "character_bound_literature_linked": True,
            "simultaneous_typical_shape_tail_proved": False,
            "joint_short_word_anticoncentration_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "collision_free_growing_moment_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact reduction to ordinary character ratios is proved "
                "and linked to sharp literature, but no joint short-word "
                "anti-concentration or all-n frame-norm theorem exists."
            ),
        },
        status=(
            "character-ratio-contract-formalized-"
            "short-word-anticoncentration-open"
        ),
        summary=(
            "Validated the unequal character-ratio factorization and linked "
            f"{len(CHARACTER_BOUND_LITERATURE)} primary proof tools; the "
            "critical short-word anti-concentration and collision-free "
            "poly(n)2^-k norm theorems remain open."
        ),
        falsifiers_triggered=[
            "Unequal physical characters reduce exactly to ordinary S_n character ratios.",
            "Pointwise character decay does not count correlated short subset words.",
            "Typical-shape concentration must hold simultaneously over 2k source draws.",
            "Finite character constants and frame spectra are not an all-n norm theorem.",
            "A norm theorem would still not implement a maximal-effect circuit or hidden-permutation decoder.",
        ],
    )


def write_character_ratio_contract_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_character_ratio_contract())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-WREATH-POINTWISE-CHARACTER-"
                    "BOUND-NOT-MOMENT"
                ),
                source=str(path),
                claim=(
                    "A pointwise symmetric-group character-ratio bound alone "
                    "proves collision-free wreath-frame contraction."
                ),
                reason_invalid=(
                    "The moment expansion contains correlated subset words; "
                    "their low-transposition-length contribution and aligned "
                    "signs require a separate joint anti-concentration theorem."
                ),
                lesson=(
                    "Build a short-word profile and prove aggregate product "
                    "mixing across all globally distinct source partitions."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_character_ratio_contract": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_character_ratio_contract_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
