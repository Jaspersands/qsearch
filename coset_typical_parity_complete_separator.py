"""Parity-complete all-source separator search.

The one-sided transposition--cycle portfolio is exactly scalar on two
unequal-source ``S_6`` blocks.  Swapping tensor factors supplies the missing
cycle--transposition orientations.  This module searches primitive integer
coefficient vectors of support at most three and magnitude at most two over

    TT0, TT1, TC0, TC1, TC2, CT0, CT1, CT2.

The finite discovery rule

    H_pc = TC2 + CT1 - 2 CT2

has no numerical collision on every ordered-source nontrivial block through
``n=7``.  Exact unequal-source character moments prove that it repairs the two
former multiplicity-two scalar blocks.  The ``n=7`` exhaustive search is
stored as a dependency-hash-gated certificate because recomputing all dense
source pairs is intentionally expensive.

This remains finite evidence.  It does not prove all-``n`` square-freeness,
inverse-polynomial normalized gaps, coherent coefficient selection, the
same-hidden-involution target law, or decoding.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    bounded_support_orbit_generators,
)
from coset_typical_commutant_moment_audit import (
    TC_INTERSECTION_ONE,
    TC_INTERSECTION_TWO,
    TT_DISJOINT,
    TT_INTERSECTION_ONE,
    _compose,
    _generator_orbit,
    _group_workspace,
    _right_product_type_ids,
)
from coset_typical_uniform_source_probe import _bicharacter_contraction
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
from symmetric_character import kronecker_coefficient


REPORT_PATH = Path(
    "research/representation/coset_typical_parity_complete_separator.json"
)
CERTIFICATE_PATH = Path(
    "research/certificates/"
    "coset_typical_parity_complete_separator_n7.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

GENERATOR_NAMES = (
    "TT0",
    "TT1",
    "TC0",
    "TC1",
    "TC2",
    "CT0",
    "CT1",
    "CT2",
)
BASE_GENERATOR_IDS = {
    "TT0": "ORB-TT-DISJOINT",
    "TT1": "ORB-TT-INTERSECTION-1",
    "TC0": "ORB-TC-INTERSECTION-0",
    "TC1": "ORB-TC-INTERSECTION-1",
    "TC2": "ORB-TC-INTERSECTION-2",
}
SWAPPED_GENERATOR_IDS = {
    "CT0": "ORB-TC-INTERSECTION-0",
    "CT1": "ORB-TC-INTERSECTION-1",
    "CT2": "ORB-TC-INTERSECTION-2",
}
DISCOVERY_COEFFICIENTS = (0, 0, 0, 0, 1, 0, 1, -2)
DEPENDENCY_PATHS = (
    Path("coset_typical_parity_complete_separator.py"),
    Path("coset_multiplicity_commutant_search.py"),
    Path("coset_jucys_murphy_label_transform.py"),
    Path("coset_typical_commutant_moment_audit.py"),
    Path("coset_typical_uniform_source_probe.py"),
)


@dataclass(frozen=True)
class SeparatorSearchCandidateRecord:
    coefficients: tuple[int, ...]
    coefficient_map: dict[str, int]
    collision_count: int
    minimum_numerical_raw_gap: float
    minimum_gap_n: int
    minimum_gap_left_source: tuple[int, ...]
    minimum_gap_right_source: tuple[int, ...]
    minimum_gap_target: tuple[int, ...]
    minimum_gap_multiplicity: int


@dataclass(frozen=True)
class ExactRepairRecord:
    n: int
    left_source: tuple[int, ...]
    right_source: tuple[int, ...]
    target: tuple[int, ...]
    multiplicity: int
    old_separator_exact_variance: str
    parity_complete_exact_mean: str
    parity_complete_exact_variance: str
    exact_multiplicity_two_repair_proved: bool


@dataclass(frozen=True)
class ParityCompleteSeparatorReport:
    created_at: str
    architecture_contract: dict[str, object]
    search_contract: dict[str, object]
    best_candidate: SeparatorSearchCandidateRecord
    exact_repair_records: list[ExactRepairRecord]
    n7_certificate_contract: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class _DenseBlock:
    n: int
    left_source: tuple[int, ...]
    right_source: tuple[int, ...]
    target: tuple[int, ...]
    multiplicity: int
    generator_blocks: tuple[np.ndarray, ...]


def _dependency_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {
        str(path): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def primitive_coefficient_vectors(
    *,
    maximum_support: int = 3,
    maximum_absolute_coefficient: int = 2,
) -> tuple[tuple[int, ...], ...]:
    if maximum_support < 1:
        raise ValueError("maximum support must be positive")
    if maximum_absolute_coefficient < 1:
        raise ValueError("coefficient magnitude must be positive")
    values = tuple(
        value
        for value in range(
            -maximum_absolute_coefficient,
            maximum_absolute_coefficient + 1,
        )
        if value
    )
    vectors: list[tuple[int, ...]] = []
    for support_size in range(
        1,
        min(maximum_support, len(GENERATOR_NAMES)) + 1,
    ):
        for indices in itertools.combinations(
            range(len(GENERATOR_NAMES)),
            support_size,
        ):
            for nonzero_values in itertools.product(
                values,
                repeat=support_size,
            ):
                coefficients = [0] * len(GENERATOR_NAMES)
                for index, value in zip(indices, nonzero_values):
                    coefficients[index] = value
                first = next(value for value in coefficients if value)
                if first < 0:
                    continue
                if math.gcd(
                    *(abs(value) for value in coefficients if value)
                ) != 1:
                    continue
                vectors.append(tuple(coefficients))
    return tuple(vectors)


def _swap_tensor_operator(
    operator: np.ndarray,
    left_dimension: int,
    right_dimension: int,
) -> np.ndarray:
    expected = left_dimension * right_dimension
    if operator.shape != (expected, expected):
        raise ValueError("operator dimension does not match tensor factors")
    return (
        operator.reshape(
            right_dimension,
            left_dimension,
            right_dimension,
            left_dimension,
        )
        .transpose(1, 0, 3, 2)
        .reshape(expected, expected)
    )


def oriented_generator_operators(
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
) -> tuple[np.ndarray, ...]:
    left_dimension = hook_length_dimension(left_source)
    right_dimension = hook_length_dimension(right_source)
    names, operators, records = bounded_support_orbit_generators(
        left_source,
        right_source,
    )
    normalized = {
        short_name: (
            operators[names.index(generator_id)]
            / records[names.index(generator_id)].term_count
        )
        for short_name, generator_id in BASE_GENERATOR_IDS.items()
    }
    swapped_names, swapped_operators, swapped_records = (
        bounded_support_orbit_generators(
            right_source,
            left_source,
        )
    )
    for short_name, generator_id in SWAPPED_GENERATOR_IDS.items():
        index = swapped_names.index(generator_id)
        normalized[short_name] = _swap_tensor_operator(
            swapped_operators[index] / swapped_records[index].term_count,
            left_dimension,
            right_dimension,
        )
    return tuple(normalized[name] for name in GENERATOR_NAMES)


@lru_cache(maxsize=None)
def dense_portfolio_blocks(n: int) -> tuple[_DenseBlock, ...]:
    partitions = integer_partitions(n)
    base = 2 * n + 1
    target_by_label = _encoded_label_targets(n, base)
    blocks: list[_DenseBlock] = []
    for left_source in partitions:
        for right_source in partitions:
            targets = {
                target
                for target in partitions
                if kronecker_coefficient(
                    left_source,
                    right_source,
                    target,
                )
                > 1
            }
            if not targets:
                continue
            generators = oriented_generator_operators(
                left_source,
                right_source,
            )
            encoded = encoded_jucys_murphy_operator(
                diagonal_jucys_murphy_operators(
                    left_source,
                    right_source,
                ),
                base,
                n,
            )
            values, vectors = np.linalg.eigh(encoded)
            label_indices: dict[int, list[int]] = {}
            for index, value in enumerate(values):
                label_indices.setdefault(round(float(value)), []).append(index)
            seen: set[tuple[int, ...]] = set()
            for label, indices in label_indices.items():
                target = target_by_label[label]
                if target not in targets or target in seen:
                    continue
                seen.add(target)
                fiber = vectors[:, indices]
                blocks.append(
                    _DenseBlock(
                        n=n,
                        left_source=left_source,
                        right_source=right_source,
                        target=target,
                        multiplicity=len(indices),
                        generator_blocks=tuple(
                            fiber.T @ generator @ fiber
                            for generator in generators
                        ),
                    )
                )
            if seen != targets:
                raise ArithmeticError("portfolio extraction missed a target")
    return tuple(blocks)


def evaluate_candidate(
    coefficients: tuple[int, ...],
    blocks: tuple[_DenseBlock, ...],
) -> SeparatorSearchCandidateRecord:
    if len(coefficients) != len(GENERATOR_NAMES):
        raise ValueError("coefficient vector has the wrong length")
    minimum_gap = math.inf
    minimum_block: _DenseBlock | None = None
    collisions = 0
    for block in blocks:
        operator = sum(
            coefficient * generator
            for coefficient, generator in zip(
                coefficients,
                block.generator_blocks,
            )
        )
        eigenvalues = np.linalg.eigvalsh(operator)
        gap = float(min(np.diff(eigenvalues), default=math.inf))
        if gap < minimum_gap:
            minimum_gap = gap
            minimum_block = block
        collisions += int(gap < 1e-9)
    if minimum_block is None:
        raise ArithmeticError("candidate evaluation received no blocks")
    return SeparatorSearchCandidateRecord(
        coefficients=coefficients,
        coefficient_map=dict(zip(GENERATOR_NAMES, coefficients)),
        collision_count=collisions,
        minimum_numerical_raw_gap=minimum_gap,
        minimum_gap_n=minimum_block.n,
        minimum_gap_left_source=minimum_block.left_source,
        minimum_gap_right_source=minimum_block.right_source,
        minimum_gap_target=minimum_block.target,
        minimum_gap_multiplicity=minimum_block.multiplicity,
    )


def search_coefficients(
    n_values: tuple[int, ...],
) -> tuple[SeparatorSearchCandidateRecord, ...]:
    blocks = tuple(
        block
        for n in n_values
        for block in dense_portfolio_blocks(n)
    )
    records = [
        evaluate_candidate(coefficients, blocks)
        for coefficients in primitive_coefficient_vectors()
    ]
    records.sort(
        key=lambda record: (
            record.collision_count,
            -record.minimum_numerical_raw_gap,
            record.coefficients,
        )
    )
    return tuple(records)


def _oriented_orbit(
    n: int,
    generator_name: str,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
]:
    source_name = generator_name
    swapped = source_name.startswith("CT")
    if swapped:
        source_name = "TC" + source_name[2:]
    generator_id = {
        "TT0": TT_DISJOINT,
        "TT1": TT_INTERSECTION_ONE,
        "TC1": TC_INTERSECTION_ONE,
        "TC2": TC_INTERSECTION_TWO,
    }.get(source_name)
    if generator_id is None:
        raise ValueError(
            "exact oriented moments currently support TT0,TT1,TC1,TC2 "
            "and their CT swaps"
        )
    base_left, base_right, orbit = _generator_orbit(n, generator_id)
    if not swapped:
        return base_left, base_right, orbit
    return (
        base_right,
        base_left,
        tuple((right, left) for left, right in orbit),
    )


@lru_cache(maxsize=None)
def _oriented_first_second_counts(
    n: int,
    generator_name: str,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, np.ndarray, int]:
    cycle_types, permutations, _, group_type_ids = _group_workspace(n)
    base_left, base_right, orbit = _oriented_orbit(n, generator_name)
    type_count = len(cycle_types)
    code_count = type_count**3
    first_codes = (
        group_type_ids.astype(np.int64) * type_count * type_count
        + _right_product_type_ids(n, base_left).astype(np.int64)
        * type_count
        + _right_product_type_ids(n, base_right).astype(np.int64)
    )
    first = np.bincount(first_codes, minlength=code_count).astype(np.int64)
    second = np.zeros(code_count, dtype=np.int64)
    group_codes = group_type_ids.astype(np.int64) * type_count * type_count
    for orbit_left, orbit_right in orbit:
        relative_left = _compose(base_left, orbit_left)
        relative_right = _compose(base_right, orbit_right)
        codes = (
            group_codes
            + _right_product_type_ids(n, relative_left).astype(np.int64)
            * type_count
            + _right_product_type_ids(n, relative_right).astype(np.int64)
        )
        second += np.bincount(codes, minlength=code_count)
    if int(first.sum()) != len(permutations):
        raise ArithmeticError("oriented first counts do not sum to |S_n|")
    if int(second.sum()) != len(permutations) * len(orbit):
        raise ArithmeticError(
            "oriented second counts do not sum to |S_n||O|"
        )
    return cycle_types, first, second, len(orbit)


@lru_cache(maxsize=None)
def _oriented_cross_counts(
    n: int,
    left_generator: str,
    right_generator: str,
) -> tuple[tuple[tuple[int, ...], ...], np.ndarray, int]:
    if left_generator == right_generator:
        cycle_types, _, second, orbit_size = (
            _oriented_first_second_counts(n, left_generator)
        )
        return cycle_types, second, orbit_size
    cycle_types, permutations, _, group_type_ids = _group_workspace(n)
    base_left, base_right, _ = _oriented_orbit(n, left_generator)
    _, _, right_orbit = _oriented_orbit(n, right_generator)
    type_count = len(cycle_types)
    code_count = type_count**3
    group_codes = group_type_ids.astype(np.int64) * type_count * type_count
    counts = np.zeros(code_count, dtype=np.int64)
    for orbit_left, orbit_right in right_orbit:
        relative_left = _compose(base_left, orbit_left)
        relative_right = _compose(base_right, orbit_right)
        codes = (
            group_codes
            + _right_product_type_ids(n, relative_left).astype(np.int64)
            * type_count
            + _right_product_type_ids(n, relative_right).astype(np.int64)
        )
        counts += np.bincount(codes, minlength=code_count)
    if int(counts.sum()) != len(permutations) * len(right_orbit):
        raise ArithmeticError(
            "oriented cross counts do not sum to |S_n||O|"
        )
    return cycle_types, counts, len(right_orbit)


@lru_cache(maxsize=None)
def exact_portfolio_mean_variance(
    n: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
    coefficients: tuple[int, ...] = DISCOVERY_COEFFICIENTS,
) -> tuple[Fraction, Fraction]:
    multiplicity = kronecker_coefficient(
        left_source,
        right_source,
        target,
    )
    if multiplicity <= 1:
        raise ValueError("portfolio moments require nontrivial multiplicity")
    active = [
        (name, coefficient)
        for name, coefficient in zip(GENERATOR_NAMES, coefficients)
        if coefficient
    ]
    group_order = math.factorial(n)
    traces: dict[str, Fraction] = {}
    for name, _ in active:
        cycle_types, first, _, _ = _oriented_first_second_counts(n, name)
        traces[name] = Fraction(
            _bicharacter_contraction(
                first,
                cycle_types,
                left_source,
                right_source,
                target,
            ),
            group_order,
        )
    trace = sum(
        (coefficient * traces[name] for name, coefficient in active),
        Fraction(),
    )
    trace_square = Fraction()
    for left_index, (left_name, left_coefficient) in enumerate(active):
        for right_index in range(left_index, len(active)):
            right_name, right_coefficient = active[right_index]
            cycle_types, counts, orbit_size = _oriented_cross_counts(
                n,
                left_name,
                right_name,
            )
            cross_trace = Fraction(
                _bicharacter_contraction(
                    counts,
                    cycle_types,
                    left_source,
                    right_source,
                    target,
                ),
                group_order * orbit_size,
            )
            factor = 1 if left_index == right_index else 2
            trace_square += (
                factor
                * left_coefficient
                * right_coefficient
                * cross_trace
            )
    mean = trace / multiplicity
    variance = trace_square / multiplicity - mean * mean
    if variance < 0:
        raise ArithmeticError("exact parity-complete variance is negative")
    return mean, variance


def _exact_repair_records() -> list[ExactRepairRecord]:
    rows = (
        ((3, 2, 1), (3, 3), (3, 2, 1)),
        ((3, 2, 1), (2, 2, 2), (3, 2, 1)),
    )
    records = []
    for left, right, target in rows:
        mean, variance = exact_portfolio_mean_variance(
            6,
            left,
            right,
            target,
        )
        multiplicity = kronecker_coefficient(left, right, target)
        records.append(
            ExactRepairRecord(
                n=6,
                left_source=left,
                right_source=right,
                target=target,
                multiplicity=multiplicity,
                old_separator_exact_variance="0",
                parity_complete_exact_mean=str(mean),
                parity_complete_exact_variance=str(variance),
                exact_multiplicity_two_repair_proved=(
                    multiplicity == 2 and variance > 0
                ),
            )
        )
    return records


def write_n7_search_certificate(
    path: Path = CERTIFICATE_PATH,
) -> dict[str, object]:
    records = search_coefficients((5, 6, 7))
    collision_free = [
        record for record in records if record.collision_count == 0
    ]
    discovery = next(
        record
        for record in records
        if record.coefficients == DISCOVERY_COEFFICIENTS
    )
    payload = {
        "certificate_contract": {
            "dependency_sha256": _dependency_hashes(),
            "search_space": (
                "all primitive coefficient vectors over eight oriented "
                "generators with support<=3 and |coefficient|<=2"
            ),
            "numerical_tolerance": 1e-9,
            "finite_scope_only": True,
        },
        "search": {
            "coefficient_vector_count": len(records),
            "block_count_by_n": {
                str(n): len(dense_portfolio_blocks(n))
                for n in (5, 6, 7)
            },
            "collision_free_candidate_count": len(collision_free),
            "best_candidate": asdict(records[0]),
            "discovery_candidate": asdict(discovery),
            "top_candidates": [
                asdict(record) for record in records[:30]
            ],
        },
        "exact_repair_records": [
            asdict(record) for record in _exact_repair_records()
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def load_n7_search_certificate(
    path: Path = CERTIFICATE_PATH,
) -> dict[str, object]:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    if not resolved.exists():
        raise FileNotFoundError(
            "n=7 parity-complete certificate is missing; rerun with "
            "--recompute-n7"
        )
    payload = json.loads(resolved.read_text())
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256"
    ) != _dependency_hashes():
        raise ArithmeticError(
            "n=7 parity-complete certificate dependency hash changed"
        )
    return payload


def build_parity_complete_separator_report(
    *,
    recompute_n7: bool = False,
) -> ParityCompleteSeparatorReport:
    certificate = (
        write_n7_search_certificate()
        if recompute_n7
        else load_n7_search_certificate()
    )
    search = certificate["search"]
    best = SeparatorSearchCandidateRecord(**search["best_candidate"])
    repair_records = [
        ExactRepairRecord(**record)
        for record in certificate["exact_repair_records"]
    ]
    block_counts = {
        int(n): int(count)
        for n, count in search["block_count_by_n"].items()
    }
    metrics: dict[str, int | float] = {
        "finite_n_count": len(block_counts),
        "minimum_n": min(block_counts),
        "maximum_n": max(block_counts),
        "all_source_nontrivial_block_count": sum(block_counts.values()),
        "coefficient_vector_count": int(search["coefficient_vector_count"]),
        "collision_free_finite_candidate_count": int(
            search["collision_free_candidate_count"]
        ),
        "best_candidate_collision_count": best.collision_count,
        "best_candidate_minimum_numerical_raw_gap": (
            best.minimum_numerical_raw_gap
        ),
        "former_scalar_block_exact_repair_count": sum(
            record.exact_multiplicity_two_repair_proved
            for record in repair_records
        ),
        "parity_complete_orientation_count": 1,
        "all_n_square_free_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "coherent_partition_adaptive_separator_count": 0,
        "same_hidden_involution_target_outcome_law_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return ParityCompleteSeparatorReport(
        created_at=utc_now(),
        architecture_contract={
            "generator_order": list(GENERATOR_NAMES),
            "best_coefficients": list(best.coefficients),
            "best_coefficient_map": best.coefficient_map,
            "orientation_completion": (
                "CTk is obtained from TCk by swapping tensor factors, adding "
                "the cycle-left/transposition-right parity missing from the "
                "original portfolio."
            ),
            "lcu_normalization": sum(
                abs(value) for value in best.coefficients
            ),
            "uniform_finite_coefficient_rule": True,
            "partition_dependent_coefficients_used": False,
        },
        search_contract={
            "finite_sizes": sorted(block_counts),
            "ordered_source_pairs": True,
            "all_nontrivial_kronecker_targets": True,
            "coefficient_vector_count": search["coefficient_vector_count"],
            "search_space": certificate["certificate_contract"][
                "search_space"
            ],
            "dense_spectra": "floating-point Young-basis controls",
            "exact_scope": (
                "The two former multiplicity-two scalar blocks are repaired "
                "by exact character-moment variance. Other simple spectra "
                "remain finite numerical evidence."
            ),
            "n7_certificate_hash_gated": True,
        },
        best_candidate=best,
        exact_repair_records=repair_records,
        n7_certificate_contract=certificate["certificate_contract"],
        headline_metrics=metrics,
        claim_gate={
            "one_sided_fixed_separator_uniform": False,
            "parity_complete_finite_all_source_candidate_found": (
                best.collision_count == 0
            ),
            "former_exact_scalar_blocks_repaired": all(
                record.exact_multiplicity_two_repair_proved
                for record in repair_records
            ),
            "all_finite_simple_spectra_exactly_certified": False,
            "adjacent_n8_all_source_tested": False,
            "all_n_square_free_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_uniform_implementation_proved": False,
            "same_hidden_involution_target_outcome_law_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Parity completion repairs the known exact collisions and a "
                "single finite coefficient vector numerically splits all "
                "blocks through n=7. No n=8 holdout, exact all-block "
                "certificate, all-n gap, coherent transform, target outcome "
                "law, or decoder follows."
            ),
        },
        status=(
            "parity-complete-all-source-finite-candidate-survives-"
            "n5-through-n7-awaits-n8-and-all-n-proof"
        ),
        summary=(
            f"Searched {search['coefficient_vector_count']} primitive rules "
            f"over {sum(block_counts.values())} all-source blocks through n=7. "
            f"The best parity-complete rule has zero finite collisions and "
            f"minimum numerical raw gap {best.minimum_numerical_raw_gap:.6g}; "
            "the former scalar blocks are exactly repaired."
        ),
        falsifiers_triggered=[
            (
                "Coefficient tuning inside the one-sided portfolio cannot "
                "repair the exact n=6 scalar blocks."
            ),
            (
                "The first parity-complete rule selected on n=5,6 fails on "
                "two n=7 blocks, so adjacent-size validation is mandatory."
            ),
            (
                "A different three-term parity-complete rule survives the "
                "finite n=5,6,7 discovery set but has no independent n=8 holdout."
            ),
            (
                "Finite floating-point simple spectra are not an all-n "
                "square-free or inverse-gap theorem."
            ),
            (
                "A separator spectrum alone supplies neither the correlated "
                "target outcome law nor a hidden-involution decoder."
            ),
        ],
    )


def write_parity_complete_separator_report(
    output_path: Path = REPORT_PATH,
    *,
    recompute_n7: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_parity_complete_separator_report(
            recompute_n7=recompute_n7,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-ONE-SIDED-PORTFOLIO-PARITY-INCOMPLETE",
                source=str(output_path),
                claim=(
                    "More coefficient search within the original one-sided "
                    "TT/TC portfolio can repair its all-source scalar blocks."
                ),
                reason_invalid=(
                    "Every original generator is exactly scalar on the same "
                    "two n=6 multiplicity-two blocks; cycle-left CT "
                    "orientations are structurally required."
                ),
                lesson=(
                    "Require parity/orientation completeness before coefficient "
                    "search and test every sampled source ordering."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "coset_typical_parity_complete_separator": str(
                        output_path
                    ),
                    "n7_search_certificate": str(CERTIFICATE_PATH),
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_parity_complete_separator_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
