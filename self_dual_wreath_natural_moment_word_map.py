"""All-order natural wreath-frame moments as subset word-map counts.

For the physical wreath group G=W_n and bridge conjugacy class C, the natural
weak-Fourier label law is

    p_pi=d_pi(d_pi+chi_pi(h))/|G|,  h in C.

Character column orthogonality therefore gives the exact normalized-character
average

    E_pi[chi_pi(g)/d_pi]
      = 1[g=e] + |C|^-1 1[g in C].

For a bridge sequence c_1,...,c_m define N_e as the number of subsets whose
ordered product is the identity and N_C as the number whose product lies in
C.  Expanding P_pi(c)=(I+pi(c))/2 yields

    E_pi Tr(prod_j P_pi(c_j))/d_pi
      = 2^-m (N_e + N_C/|C|).

For k iid natural irrep labels and frame block

    B_Pi=E_c tensor_i P_pi_i(c),

the complete source-averaged normalized moment is consequently

    E_Pi Tr(B_Pi^m)/prod_i d_pi
      = E_(c_1,...,c_m) [2^-m(N_e+N_C/|C|)]^k.

This removes the sum over physical irreps at every moment order.  It replaces
it with a subset word-map counting problem.  No polynomial contraction of
that count at the growing order required by the sub-POVM certificate is
claimed.
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
    PhysicalWreathIrrepDescriptor,
    bridge_element,
    equal_pair_descriptor,
    projector_word_character_sum,
    selected_bridge_word,
    unequal_pair_descriptor,
)
from self_dual_wreath_complete_w3_tuple_audit import (
    run_complete_w3_tuple_audit,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)
from self_dual_wreath_subset_carrier_algebra import (
    WreathElement,
    inverse_permutation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_moment_word_map.json"
)
W3_TUPLE_PATH = Path(
    "research/representation/self_dual_wreath_complete_w3_tuple_audit.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class CharacterColumnValidationRecord:
    n: int
    moment_order: int
    bridge_sequence_count: int
    maximum_absolute_residual: float
    failed_sequence_count: int
    exact_source_character_identity_verified: bool


@dataclass(frozen=True)
class W3SpectrumValidationRecord:
    moment_order: int
    naturally_weighted_spectral_normalized_moment: float
    exact_word_map_normalized_moment: str
    absolute_residual: float
    exact_match_within_tolerance: bool


@dataclass(frozen=True)
class FiniteWordMapRecord:
    n: int
    moment_order: int
    copy_count: int
    bridge_sequence_count: int
    subset_product_count_per_sequence: int
    distinct_identity_bridge_signature_count: int
    exact_source_averaged_normalized_moment: str
    log2_source_averaged_normalized_moment: float
    factorial_bridge_sequence_enumeration_used: bool
    polynomial_word_map_contraction_proved: bool
    status: str


@dataclass(frozen=True)
class GrowingWordMapRequirementRecord:
    n: int
    copy_count: int
    required_moment_order: int
    log2_explicit_bridge_sequence_count: float
    log2_subset_masks_per_sequence: int
    explicit_word_map_enumeration_polynomial: bool
    compressed_identity_bridge_word_recurrence_proved: bool
    concentration_to_natural_conclusive_probability_proved: bool
    status: str


@dataclass(frozen=True)
class NaturalMomentWordMapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    character_validations: list[CharacterColumnValidationRecord]
    w3_spectrum_validations: list[W3SpectrumValidationRecord]
    finite_word_map_records: list[FiniteWordMapRecord]
    scaling_requirements: list[GrowingWordMapRequirementRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def physical_irrep_descriptors(
    n: int,
) -> tuple[PhysicalWreathIrrepDescriptor, ...]:
    partitions = integer_partitions(n)
    descriptors: list[PhysicalWreathIrrepDescriptor] = []
    for partition in partitions:
        descriptors.append(equal_pair_descriptor(partition, 1))
        descriptors.append(equal_pair_descriptor(partition, -1))
    for left_index, left in enumerate(partitions):
        for right in partitions[left_index + 1 :]:
            descriptors.append(unequal_pair_descriptor(left, right))
    return tuple(descriptors)


def natural_irrep_probability(
    descriptor: PhysicalWreathIrrepDescriptor,
) -> Fraction:
    n = sum(descriptor.left_partition)
    return Fraction(
        descriptor.dimension
        * (descriptor.dimension + descriptor.bridge_character),
        2 * math.factorial(n) ** 2,
    )


def is_identity_wreath(element: WreathElement) -> bool:
    left, right, swap = element
    identity = tuple(range(len(left)))
    return not swap and left == identity and right == identity


def is_bridge_class_element(element: WreathElement) -> bool:
    left, right, swap = element
    return bool(swap) and right == inverse_permutation(left)


def subset_word_signature(
    sequence: tuple[Permutation, ...],
) -> tuple[int, int]:
    identity_count = 0
    bridge_count = 0
    for mask in range(1 << len(sequence)):
        word = selected_bridge_word(sequence, mask)
        if is_identity_wreath(word):
            identity_count += 1
        elif is_bridge_class_element(word):
            bridge_count += 1
    return identity_count, bridge_count


def word_map_single_label_factor(
    sequence: tuple[Permutation, ...],
) -> Fraction:
    if not sequence:
        raise ValueError("sequence must be nonempty")
    hidden_label_count = math.factorial(len(sequence[0]))
    identity_count, bridge_count = subset_word_signature(sequence)
    return Fraction(
        hidden_label_count * identity_count + bridge_count,
        hidden_label_count * (1 << len(sequence)),
    )


def direct_source_character_factor(
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
    sequence: tuple[Permutation, ...],
) -> Fraction:
    return sum(
        (
            natural_irrep_probability(descriptor)
            * Fraction(
                projector_word_character_sum(descriptor, sequence),
                descriptor.dimension * (1 << len(sequence)),
            )
            for descriptor in descriptors
        ),
        Fraction(),
    )


def exact_source_averaged_normalized_moment(
    n: int,
    moment_order: int,
    copy_count: int,
) -> tuple[Fraction, int]:
    if moment_order < 1:
        raise ValueError("moment_order must be positive")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    permutations = tuple(itertools.permutations(range(n)))
    signature_counts: dict[tuple[int, int], int] = {}
    for sequence in itertools.product(permutations, repeat=moment_order):
        signature = subset_word_signature(sequence)
        signature_counts[signature] = (
            signature_counts.get(signature, 0) + 1
        )
    hidden_label_count = len(permutations)
    denominator_factor = hidden_label_count * (1 << moment_order)
    numerator = sum(
        multiplicity
        * (
            hidden_label_count * identity_count + bridge_count
        )
        ** copy_count
        for (identity_count, bridge_count), multiplicity
        in signature_counts.items()
    )
    denominator = (
        hidden_label_count**moment_order
        * denominator_factor**copy_count
    )
    return Fraction(numerator, denominator), len(signature_counts)


def validate_character_column_identity(
    n: int,
    moment_order: int,
    tolerance: float = 1e-12,
) -> CharacterColumnValidationRecord:
    descriptors = physical_irrep_descriptors(n)
    probabilities = sum(
        (natural_irrep_probability(item) for item in descriptors),
        Fraction(),
    )
    if probabilities != 1:
        raise ArithmeticError("natural physical irrep law does not sum to one")
    permutations = tuple(itertools.permutations(range(n)))
    maximum_residual = 0.0
    failures = 0
    for sequence in itertools.product(permutations, repeat=moment_order):
        direct = direct_source_character_factor(descriptors, sequence)
        contracted = word_map_single_label_factor(sequence)
        residual = abs(float(direct - contracted))
        maximum_residual = max(maximum_residual, residual)
        failures += residual > tolerance
    return CharacterColumnValidationRecord(
        n=n,
        moment_order=moment_order,
        bridge_sequence_count=len(permutations) ** moment_order,
        maximum_absolute_residual=maximum_residual,
        failed_sequence_count=failures,
        exact_source_character_identity_verified=failures == 0,
    )


def _w3_spectral_normalized_moment(
    payload: dict[str, Any],
    moment_order: int,
) -> float:
    total = 0.0
    for record in payload.get("tuple_records", []):
        weight = float(record.get("aggregate_natural_probability", 0))
        if not weight:
            continue
        trace_moment = sum(
            int(cluster["multiplicity"])
            * float(cluster["eigenvalue"]) ** moment_order
            for cluster in record.get("eigenvalue_multiplicities", [])
        )
        total += (
            weight
            * trace_moment
            / int(record["block_dimension"])
        )
    return total


def _fraction_log2(value: Fraction) -> float:
    if value <= 0:
        return -math.inf
    return math.log2(value.numerator) - math.log2(value.denominator)


def run_natural_moment_word_map() -> NaturalMomentWordMapReport:
    character_validations = [
        validate_character_column_identity(n, order)
        for n, order in (
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (4, 2),
        )
    ]
    w3 = _read_json(W3_TUPLE_PATH)
    if not w3:
        w3 = asdict(run_complete_w3_tuple_audit())
    w3_validations = []
    for order in (1, 2, 3, 4):
        word_moment, _ = exact_source_averaged_normalized_moment(
            3,
            order,
            3,
        )
        spectral = _w3_spectral_normalized_moment(w3, order)
        residual = abs(spectral - float(word_moment))
        w3_validations.append(
            W3SpectrumValidationRecord(
                moment_order=order,
                naturally_weighted_spectral_normalized_moment=spectral,
                exact_word_map_normalized_moment=str(word_moment),
                absolute_residual=residual,
                exact_match_within_tolerance=residual <= 1e-10,
            )
        )
    finite_records = []
    for n, order in (
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (4, 2),
        (4, 3),
    ):
        copies = math.ceil(math.log2(math.factorial(n)))
        moment, signatures = exact_source_averaged_normalized_moment(
            n,
            order,
            copies,
        )
        finite_records.append(
            FiniteWordMapRecord(
                n=n,
                moment_order=order,
                copy_count=copies,
                bridge_sequence_count=math.factorial(n) ** order,
                subset_product_count_per_sequence=1 << order,
                distinct_identity_bridge_signature_count=signatures,
                exact_source_averaged_normalized_moment=str(moment),
                log2_source_averaged_normalized_moment=_fraction_log2(
                    moment
                ),
                factorial_bridge_sequence_enumeration_used=True,
                polynomial_word_map_contraction_proved=False,
                status="exact-finite-word-map-enumeration",
            )
        )
    wreath = _read_json(WREATH_PGM_PATH)
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    scaling = [
        GrowingWordMapRequirementRecord(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            required_moment_order=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
            log2_explicit_bridge_sequence_count=(
                math.ceil(float(record["log2_kcopy_hilbert_dimension"]))
                * float(record["log2_hidden_label_count"])
            ),
            log2_subset_masks_per_sequence=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
            explicit_word_map_enumeration_polynomial=False,
            compressed_identity_bridge_word_recurrence_proved=False,
            concentration_to_natural_conclusive_probability_proved=False,
            status="all-order-reduction-proved-growing-word-contraction-open",
        )
        for record in wreath.get("records", [])
    ]
    failed_character = sum(
        record.failed_sequence_count for record in character_validations
    )
    failed_spectra = sum(
        not record.exact_match_within_tolerance
        for record in w3_validations
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "character_column_validation_count": len(character_validations),
        "failed_character_sequence_count": failed_character,
        "w3_spectrum_validation_count": len(w3_validations),
        "failed_w3_spectrum_validation_count": failed_spectra,
        "finite_word_map_record_count": len(finite_records),
        "maximum_exact_word_map_n": max(
            record.n for record in finite_records
        ),
        "maximum_exact_word_map_moment_order": max(
            record.moment_order for record in finite_records
        ),
        "natural_character_column_identity_theorem_count": 1,
        "all_order_source_averaged_word_map_reduction_count": 1,
        "physical_irrep_sum_eliminated_count": 1,
        "tail_required_moment_order": tail.required_moment_order,
        "tail_log2_explicit_bridge_sequence_count": (
            tail.log2_explicit_bridge_sequence_count
        ),
        "growing_order_word_map_contraction_count": 0,
        "natural_tuple_moment_concentration_theorem_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = failed_character == 0 and failed_spectra == 0
    return NaturalMomentWordMapReport(
        created_at=utc_now(),
        theorem_contract={
            "natural_label_law": (
                "p_pi=d_pi(d_pi+chi_pi(h))/|W_n|"
            ),
            "column_orthogonality": (
                "E_pi chi_pi(g)/d_pi="
                "1[g=e]+1[g in C]/|C|"
            ),
            "subset_word_factor": (
                "a_m(c_1,...,c_m)=2^-m(N_e+N_C/|C|)"
            ),
            "all_order_normalized_moment": (
                "E_Pi Tr(B_Pi^m)/prod_i d_pi="
                "E_(c_1,...,c_m) a_m(c_1,...,c_m)^k"
            ),
            "remaining_problem": (
                "compress the distribution of identity and bridge-class "
                "subset-word counts at growing m, then prove concentration "
                "from source-averaged moments to natural tuple success"
            ),
        },
        character_validations=character_validations,
        w3_spectrum_validations=w3_validations,
        finite_word_map_records=finite_records,
        scaling_requirements=scaling,
        headline_metrics=metrics,
        claim_gate={
            "natural_character_column_identity_proved": verified,
            "all_order_source_averaged_word_map_reduction_proved": verified,
            "physical_irrep_sum_removed": verified,
            "growing_order_word_map_contraction_proved": False,
            "natural_tuple_moment_concentration_proved": False,
            "natural_average_inverse_polynomial_conclusive_bound_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The representation sum is eliminated exactly at all orders, "
                "but the resulting bridge word-map distribution is still "
                "exponential at the required growing order and has not been "
                "converted into a per-tuple success theorem or circuit."
            ),
        },
        status=(
            "all-order-natural-moment-word-map-reduction-proved-"
            "growing-contraction-open"
        ),
        summary=(
            "Reduced every natural source-averaged normalized wreath-frame "
            "moment to identity and bridge-class subset word counts; all "
            f"{len(character_validations)} character controls and "
            f"{len(w3_validations)} complete W3 spectral controls pass, while "
            "growing-order word-map contraction remains open."
        ),
        falsifiers_triggered=[
            "The exact physical irrep probabilities sum to one on every finite character control.",
            "Character column orthogonality matches every tested bridge sequence exactly.",
            "The all-order word-map formula reproduces complete naturally weighted W3 spectral moments through order four.",
            "Finite word-map enumeration still scales as (n!)^m times 2^m and is not an algorithm.",
            "A source-averaged normalized moment identity does not by itself prove concentration for individual natural tuples.",
            "No maximal-effect dilation, permutation decoder, or classical separation follows from the reduction.",
        ],
    )


def write_natural_moment_word_map_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_natural_moment_word_map())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-COSET"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={"self_dual_wreath_natural_moment_word_map": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-ALL-ORDER-WORD-MAP-NOT-GROWING-CONTRACTION",
                source="self_dual_wreath_natural_moment_word_map.py",
                claim="Subset word-map counting automatically proves growing-order moment contraction for natural wreath frames.",
                reason_invalid="Natural irrep averaging replaces physical irreps with word maps, but counting subset identities does not prove polynomial moment bounds at growing order.",
                lesson="Exact natural character formulas eliminate irrep summations, but explicit subset word-map bounds are required for growing-order sub-POVM certificates.",
                applies_to=["CODE-SELF-DUAL-WREATH", "DHS-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=payload["headline_metrics"],
            )
        )
    return payload




if __name__ == "__main__":
    report = write_natural_moment_word_map_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
