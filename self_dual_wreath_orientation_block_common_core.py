"""Structured exponential common-core families of orientation projectors.

The fixed-family common-range theorem can be used constructively.  Partition
the ``k`` source labels into blocks.  In each block require that the tensor
product of all left partitions and the tensor product of all right partitions
contain the same one-dimensional character ``delta_j`` (trivial or sign).
Choose one orientation bit per block and replicate it on every label in that
block.  The resulting ``2^r`` orientations, where ``r`` is the number of
blocks, have membership patterns ``S_j`` and their complements.

The parity-kernel conditions reduce to

    delta_left_j = delta_right_j for every block j,
    delta_target + sum_j delta_j = 0 mod 2.

For the trivial target and even total sign parity, all ``2^r`` projectors have
an exact common vector.  Therefore

    ||sum_e E_e|| >= 2^r,
    ||F_nu|| >= 2^(r-k).

If such block packings exist with ``r=Omega(k)`` on an asymptotic natural
portfolio family, the desired ``poly(n)2^-k`` norm bound is false.  The exact
finite witnesses here establish the mechanism and search boundary; they do
not prove that the deterministic portfolios carry constant natural mass or
that the packing rate persists for all ``n``.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_orientation_triple_range import (
    _one_dimensional_support,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_block_common_core.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CommonCoreBlockRecord:
    label_indices: tuple[int, ...]
    block_size: int
    one_dimensional_character: str
    left_multiplicity: int
    right_multiplicity: int


@dataclass(frozen=True)
class BlockCommonCoreScalingRecord:
    n: int
    partition_count: int
    copy_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    block_count: int
    block_sizes: tuple[int, ...]
    covered_label_count: int
    all_labels_covered: bool
    block_rate: float
    common_orientation_family_size: int
    common_core_dimension_lower_bound: int
    log2_common_core_dimension_lower_bound: float
    projector_sum_norm_lower_bound: int
    averaged_fourier_norm_lower_bound: float
    target_two_to_one_minus_k: float
    norm_lower_bound_to_target_ratio: float
    exact_finite_block_common_core_witness: bool
    asymptotic_linear_rate_persistence_proved: bool
    natural_constant_mass_persistence_proved: bool
    blocks: list[CommonCoreBlockRecord]
    status: str


@dataclass(frozen=True)
class OrientationBlockCommonCoreReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[BlockCommonCoreScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class _BlockCandidate:
    mask: int
    indices: tuple[int, ...]
    common_support: int


def _one_dimensional_multiplicity(
    n: int,
    partitions: tuple[Partition, ...],
    sign_bit: int,
) -> int:
    target = (1,) * n if sign_bit else (n,)
    return dict(tensor_product_multiplicities(partitions, n)).get(target, 0)


@lru_cache(maxsize=None)
def _block_candidates(
    n: int,
    labels: tuple[Label, ...],
    block_size: int,
) -> tuple[_BlockCandidate, ...]:
    rows = []
    for indices in itertools.combinations(range(len(labels)), block_size):
        left_parts = tuple(
            sorted((labels[index][0] for index in indices), reverse=True)
        )
        right_parts = tuple(
            sorted((labels[index][1] for index in indices), reverse=True)
        )
        common_support = (
            _one_dimensional_support(n, left_parts)
            & _one_dimensional_support(n, right_parts)
        )
        if common_support:
            rows.append(
                _BlockCandidate(
                    mask=sum(1 << index for index in indices),
                    indices=indices,
                    common_support=common_support,
                )
            )
    return tuple(rows)


def _block_count_profiles(copy_count: int) -> tuple[tuple[int, int], ...]:
    rows = []
    for triple_count in range(copy_count // 3 + 1):
        remainder = copy_count - 3 * triple_count
        if remainder >= 0 and remainder % 4 == 0:
            rows.append((triple_count, remainder // 4))
    return tuple(
        sorted(rows, key=lambda row: (sum(row), row[0]), reverse=True)
    )


def find_block_common_core(
    n: int,
) -> tuple[tuple[_BlockCandidate, int], ...]:
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    by_size_and_index = {
        size: [[] for _ in range(copy_count)] for size in (3, 4)
    }
    for size in (3, 4):
        for candidate in _block_candidates(n, labels, size):
            for index in candidate.indices:
                by_size_and_index[size][index].append(candidate)

    full_mask = (1 << copy_count) - 1
    for triple_count, quadruple_count in _block_count_profiles(copy_count):
        @lru_cache(maxsize=None)
        def search(
            remaining_mask: int,
            triples_left: int,
            quadruples_left: int,
            sign_parity: int,
        ) -> tuple[tuple[_BlockCandidate, int], ...] | None:
            if not remaining_mask:
                if not triples_left and not quadruples_left and not sign_parity:
                    return ()
                return None
            if 3 * triples_left + 4 * quadruples_left != remaining_mask.bit_count():
                return None
            first_index = (remaining_mask & -remaining_mask).bit_length() - 1
            for size, count in (
                (3, triples_left),
                (4, quadruples_left),
            ):
                if not count:
                    continue
                for candidate in by_size_and_index[size][first_index]:
                    if candidate.mask & remaining_mask != candidate.mask:
                        continue
                    for sign_bit in (0, 1):
                        if not candidate.common_support & (1 << sign_bit):
                            continue
                        tail = search(
                            remaining_mask ^ candidate.mask,
                            triples_left - (size == 3),
                            quadruples_left - (size == 4),
                            sign_parity ^ sign_bit,
                        )
                        if tail is not None:
                            return ((candidate, sign_bit), *tail)
            return None

        solution = search(
            full_mask,
            triple_count,
            quadruple_count,
            0,
        )
        if solution is not None:
            return solution
    return ()


def block_common_core_scaling_record(
    n: int,
) -> BlockCommonCoreScalingRecord:
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    solution = find_block_common_core(n)
    blocks = []
    common_dimension = 1
    covered = 0
    for candidate, sign_bit in solution:
        left_parts = tuple(
            sorted(
                (labels[index][0] for index in candidate.indices),
                reverse=True,
            )
        )
        right_parts = tuple(
            sorted(
                (labels[index][1] for index in candidate.indices),
                reverse=True,
            )
        )
        left_multiplicity = _one_dimensional_multiplicity(
            n,
            left_parts,
            sign_bit,
        )
        right_multiplicity = _one_dimensional_multiplicity(
            n,
            right_parts,
            sign_bit,
        )
        if not left_multiplicity or not right_multiplicity:
            raise ArithmeticError("selected block has zero claimed multiplicity")
        common_dimension *= left_multiplicity * right_multiplicity
        covered += len(candidate.indices)
        blocks.append(
            CommonCoreBlockRecord(
                label_indices=candidate.indices,
                block_size=len(candidate.indices),
                one_dimensional_character=(
                    "sign" if sign_bit else "trivial"
                ),
                left_multiplicity=left_multiplicity,
                right_multiplicity=right_multiplicity,
            )
        )
    block_count = len(blocks)
    family_size = 1 << block_count
    target_scale = 2 ** (1 - copy_count)
    averaged_lower_bound = family_size / (1 << copy_count)
    exact = bool(blocks) and covered == copy_count
    return BlockCommonCoreScalingRecord(
        n=n,
        partition_count=len(partitions),
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        block_count=block_count,
        block_sizes=tuple(block.block_size for block in blocks),
        covered_label_count=covered,
        all_labels_covered=covered == copy_count,
        block_rate=block_count / copy_count if copy_count else 0.0,
        common_orientation_family_size=family_size,
        common_core_dimension_lower_bound=common_dimension if exact else 0,
        log2_common_core_dimension_lower_bound=(
            math.log2(common_dimension) if exact and common_dimension else 0.0
        ),
        projector_sum_norm_lower_bound=family_size if exact else 0,
        averaged_fourier_norm_lower_bound=(
            averaged_lower_bound if exact else 0.0
        ),
        target_two_to_one_minus_k=target_scale,
        norm_lower_bound_to_target_ratio=(
            averaged_lower_bound / target_scale if exact else 0.0
        ),
        exact_finite_block_common_core_witness=exact,
        asymptotic_linear_rate_persistence_proved=False,
        natural_constant_mass_persistence_proved=False,
        blocks=blocks,
        status=(
            "exact-finite-exponential-block-common-core"
            if exact
            else "block-common-core-cover-not-found"
        ),
    )


def run_orientation_block_common_core() -> OrientationBlockCommonCoreReport:
    scaling = [block_common_core_scaling_record(n) for n in range(7, 13)]
    witnesses = [
        record for record in scaling if record.exact_finite_block_common_core_witness
    ]
    metrics: dict[str, int | float] = {
        "block_common_core_construction_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "exact_finite_block_common_core_witness_count": len(witnesses),
        "information_threshold_witness_count": sum(
            record.reaches_information_threshold for record in witnesses
        ),
        "minimum_observed_block_rate": min(
            record.block_rate for record in witnesses
        ),
        "maximum_observed_block_rate": max(
            record.block_rate for record in witnesses
        ),
        "tail_n": scaling[-1].n,
        "tail_copy_count": scaling[-1].copy_count,
        "tail_block_count": scaling[-1].block_count,
        "tail_common_orientation_family_size": (
            scaling[-1].common_orientation_family_size
        ),
        "tail_log2_common_core_dimension_lower_bound": (
            scaling[-1].log2_common_core_dimension_lower_bound
        ),
        "tail_projector_sum_norm_lower_bound": (
            scaling[-1].projector_sum_norm_lower_bound
        ),
        "tail_averaged_fourier_norm_lower_bound": (
            scaling[-1].averaged_fourier_norm_lower_bound
        ),
        "tail_norm_lower_bound_to_target_ratio": (
            scaling[-1].norm_lower_bound_to_target_ratio
        ),
        "finite_exact_target_violation_count": sum(
            record.norm_lower_bound_to_target_ratio > 1 for record in witnesses
        ),
        "asymptotic_linear_block_rate_theorem_count": 0,
        "natural_constant_mass_block_packing_theorem_count": 0,
        "uniform_polynomial_factor_norm_counterexample_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
    }
    tail = scaling[-1]
    return OrientationBlockCommonCoreReport(
        created_at=utc_now(),
        theorem_contract={
            "block_construction": (
                "r disjoint label blocks with matched left/right one-"
                "dimensional characters and global even sign parity produce "
                "2^r orientations with an exact common core"
            ),
            "norm_lower_bound": (
                "the projector sum norm is at least 2^r and the averaged "
                "Fourier block norm is at least 2^(r-k)"
            ),
            "asymptotic_falsifier": (
                "a natural or worst-sector family with r=Omega(k) falsifies "
                "every poly(n)2^-k upper bound"
            ),
            "remaining_boundary": (
                "prove linear-rate block packings on an asymptotic portfolio "
                "family and determine their natural mass, or prove that the "
                "finite top-dimension witnesses disappear asymptotically"
            ),
        },
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "block_common_core_construction_proved": True,
            "tail_exact_finite_exponential_common_family_found": (
                tail.exact_finite_block_common_core_witness
            ),
            "asymptotic_linear_block_rate_proved": False,
            "natural_constant_mass_persistence_proved": False,
            "uniform_polynomial_factor_norm_counterexample_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite threshold portfolios contain exponentially large "
                "structured common-core orientation families, but neither "
                "linear-rate persistence nor constant natural mass is proved "
                "asymptotically. The mechanism is a high-priority potential "
                "counterexample to the uniform frame-norm route."
            ),
        },
        status="finite-exponential-common-core-asymptotic-persistence-open",
        summary=(
            f"Constructed exact block common-core witnesses on {len(witnesses)}"
            f"/{len(scaling)} portfolios; the tail n={tail.n}, k={tail.copy_count} "
            f"witness contains {tail.common_orientation_family_size} "
            "orientation projectors sharing a nonzero vector."
        ),
        falsifiers_triggered=[
            (
                "Random-family disappearance at depth five does not preclude "
                "exponentially large structured orientation families with an "
                "exact common core."
            ),
            (
                "Pairwise 1/(n-1) contraction off common ranges cannot bound "
                "a structured family that remains entirely in common ranges."
            ),
            (
                "Finite linear-looking block rates do not prove asymptotic or "
                "natural-mass persistence."
            ),
        ],
    )


def write_orientation_block_common_core_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_block_common_core())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_block_common_core_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
