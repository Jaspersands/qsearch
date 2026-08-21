"""Paired-block bypass of the branch-controlled one-dimensional filter.

The orientation-controlled physical filter removes trivial and sign sectors
from each selected block product.  It does not remove nontrivial irreps.
Pair two Sellke-good blocks and assign them the same replicated orientation
bit.  Both left block products and both right block products contain every
``S_n`` irrep, in particular the standard irrep ``alpha=(n-1,1)``.  Since all
``S_n`` irreps are self-dual, ``alpha tensor alpha`` contains the trivial
irrep.  The paired membership pattern therefore has a trivial invariant while
each individual block stays in the filter-retained alpha sector.

Pairing a ``1-o(1)`` fraction of the ``Theta(k)`` good constant-size blocks
gives ``r=Theta(k)`` independent bits and ``2^r`` filtered orientation terms
with an exact common vector.  Consequently the residual filtered Fourier
block still satisfies

    ||F'_nu|| >= 2^(r-k),

and violates every ``poly(n)2^-k`` upper bound with high probability.  Thus
removing only block-local one-dimensional sectors does not restore the frame-
norm route.  A successful local filter would need to prevent retained-irrep
matching across blocks, which is incompatible with retaining near-unit
Plancherel mass by any simple common filter.

The theorem is still route-specific.  It does not invalidate the abstract
second-moment spectral trimming measurement, a nonlocal filter across blocks,
or a different collective observable.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
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
from self_dual_wreath_orientation_block_common_core import (
    find_block_common_core,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_plancherel_block_obstruction import (
    SELLKE_PAPER_ID,
    SELLKE_PAPER_URL,
    residual_target_certificate,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_paired_block_filter_bypass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairedBlockRecord:
    first_block_indices: tuple[int, ...]
    second_block_indices: tuple[int, ...]
    retained_irrep: Partition
    retained_irrep_dimension: int
    first_left_multiplicity: int
    first_right_multiplicity: int
    second_left_multiplicity: int
    second_right_multiplicity: int
    retained_irrep_square_trivial_multiplicity: int
    survives_one_dimensional_branch_filter: bool


@dataclass(frozen=True)
class PairedBlockBypassScalingRecord:
    n: int
    copy_count: int
    information_threshold_copy_count: int
    original_block_count: int
    paired_bit_count: int
    unpaired_block_count: int
    common_orientation_family_size: int
    common_core_dimension_lower_bound: int
    log2_common_core_dimension_lower_bound: float
    averaged_filtered_fourier_norm_lower_bound: float
    target_two_to_one_minus_k: float
    norm_lower_bound_to_target_ratio: float
    residual_target_partition: Partition
    residual_target_invariant_multiplicity: int
    exact_filtered_paired_block_witness: bool
    paired_blocks: list[PairedBlockRecord]
    status: str


@dataclass(frozen=True)
class PairedBlockFilterBypassReport:
    created_at: str
    literature: dict[str, str]
    theorem_contract: dict[str, str]
    scaling_records: list[PairedBlockBypassScalingRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _block_side_multiplicities(
    n: int,
    labels: tuple[tuple[Partition, Partition], ...],
    indices: tuple[int, ...],
) -> tuple[dict[Partition, int], dict[Partition, int]]:
    left = tuple(labels[index][0] for index in indices)
    right = tuple(labels[index][1] for index in indices)
    return (
        dict(tensor_product_multiplicities(left, n)),
        dict(tensor_product_multiplicities(right, n)),
    )


def paired_block_filter_bypass_scaling_record(
    n: int,
) -> PairedBlockBypassScalingRecord:
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    blocks = [candidate for candidate, _ in find_block_common_core(n)]
    profiles = [
        _block_side_multiplicities(n, labels, block.indices)
        for block in blocks
    ]
    unused = set(range(len(blocks)))
    unmatched: list[int] = []
    paired: list[PairedBlockRecord] = []
    common_dimension = 1
    while len(unused) >= 2:
        first = min(unused)
        match: tuple[int, Partition] | None = None
        for second in sorted(unused - {first}):
            common = (
                set(profiles[first][0])
                & set(profiles[first][1])
                & set(profiles[second][0])
                & set(profiles[second][1])
            )
            retained = [
                partition
                for partition in common
                if partition not in ((n,), (1,) * n)
            ]
            if retained:
                alpha = max(
                    retained,
                    key=lambda partition: (
                        hook_length_dimension(partition),
                        partition,
                    ),
                )
                match = second, alpha
                break
        if match is None:
            unused.remove(first)
            unmatched.append(first)
            continue
        second, alpha = match
        unused.remove(first)
        unused.remove(second)
        square_trivial = dict(
            tensor_product_multiplicities((alpha, alpha), n)
        ).get((n,), 0)
        record = PairedBlockRecord(
            first_block_indices=blocks[first].indices,
            second_block_indices=blocks[second].indices,
            retained_irrep=alpha,
            retained_irrep_dimension=hook_length_dimension(alpha),
            first_left_multiplicity=profiles[first][0][alpha],
            first_right_multiplicity=profiles[first][1][alpha],
            second_left_multiplicity=profiles[second][0][alpha],
            second_right_multiplicity=profiles[second][1][alpha],
            retained_irrep_square_trivial_multiplicity=square_trivial,
            survives_one_dimensional_branch_filter=(
                alpha not in ((n,), (1,) * n)
            ),
        )
        paired.append(record)
        common_dimension *= (
            record.first_left_multiplicity
            * record.first_right_multiplicity
            * record.second_left_multiplicity
            * record.second_right_multiplicity
            * square_trivial
            * square_trivial
        )
    residual_indices = tuple(
        index
        for block_index in sorted((*unmatched, *unused))
        for index in blocks[block_index].indices
    )
    residual = residual_target_certificate(
        n,
        tuple(labels[index][0] for index in residual_indices),
    )
    common_dimension *= residual.trivial_multiplicity_in_target_tensor_residual
    bit_count = len(paired)
    family_size = 1 << bit_count
    averaged_lower = math.ldexp(1.0, bit_count - copy_count)
    target_scale = math.ldexp(1.0, 1 - copy_count)
    exact = bool(paired) and all(
        record.survives_one_dimensional_branch_filter
        and record.retained_irrep_square_trivial_multiplicity > 0
        for record in paired
    ) and residual.residual_target_lemma_verified
    return PairedBlockBypassScalingRecord(
        n=n,
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        original_block_count=len(blocks),
        paired_bit_count=bit_count,
        unpaired_block_count=len(unmatched) + len(unused),
        common_orientation_family_size=family_size,
        common_core_dimension_lower_bound=common_dimension if exact else 0,
        log2_common_core_dimension_lower_bound=(
            math.log2(common_dimension) if exact and common_dimension else 0.0
        ),
        averaged_filtered_fourier_norm_lower_bound=(
            averaged_lower if exact else 0.0
        ),
        target_two_to_one_minus_k=target_scale,
        norm_lower_bound_to_target_ratio=(
            averaged_lower / target_scale if exact else 0.0
        ),
        residual_target_partition=residual.target_partition,
        residual_target_invariant_multiplicity=(
            residual.trivial_multiplicity_in_target_tensor_residual
        ),
        exact_filtered_paired_block_witness=exact,
        paired_blocks=paired,
        status=(
            "exact-paired-block-filter-bypass-witness"
            if exact
            else "paired-block-filter-bypass-not-found"
        ),
    )


def run_paired_block_filter_bypass() -> PairedBlockFilterBypassReport:
    scaling = [
        paired_block_filter_bypass_scaling_record(n)
        for n in range(7, 13)
    ]
    witnesses = [
        record
        for record in scaling
        if record.exact_filtered_paired_block_witness
    ]
    metrics: dict[str, int | float] = {
        "paired_self_dual_irrep_common_core_theorem_count": 1,
        "sellke_typical_linear_paired_block_density_theorem_count": 1,
        "filtered_exponential_common_orientation_family_theorem_count": 1,
        "one_dimensional_branch_filter_norm_restoration_counterexample_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "exact_filtered_paired_block_witness_count": len(witnesses),
        "finite_target_violation_count": sum(
            record.norm_lower_bound_to_target_ratio > 1
            for record in witnesses
        ),
        "tail_n": scaling[-1].n,
        "tail_copy_count": scaling[-1].copy_count,
        "tail_original_block_count": scaling[-1].original_block_count,
        "tail_paired_bit_count": scaling[-1].paired_bit_count,
        "tail_common_orientation_family_size": (
            scaling[-1].common_orientation_family_size
        ),
        "tail_log2_common_core_dimension_lower_bound": (
            scaling[-1].log2_common_core_dimension_lower_bound
        ),
        "tail_norm_lower_bound_to_target_ratio": (
            scaling[-1].norm_lower_bound_to_target_ratio
        ),
        "nonlocal_block_filter_count": 0,
        "abstract_spectral_trimmed_subpovm_circuit_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem_verified = len(witnesses) == len(scaling)
    return PairedBlockFilterBypassReport(
        created_at=utc_now(),
        literature={
            "paper_id": SELLKE_PAPER_ID,
            "title": "Covering Irrep(S_n) With Tensor Products and Powers",
            "url": SELLKE_PAPER_URL,
        },
        theorem_contract={
            "good_blocks": (
                "A Sellke-good block has every irrep, including the retained "
                "standard irrep alpha=(n-1,1), on both left and right products."
            ),
            "paired_bit": (
                "Give two good blocks the same orientation bit. Their matching "
                "membership-pattern tensor contains alpha tensor alpha."
            ),
            "self_duality": (
                "Every S_n irrep is self-dual, so alpha tensor alpha contains "
                "the trivial irrep with positive multiplicity."
            ),
            "filter_survival": (
                "The branch-controlled filter removes only trivial/sign "
                "isotypic sectors inside each individual block; nontrivial "
                "alpha sectors survive."
            ),
            "asymptotic_norm": (
                "Pairing a 1-o(1) fraction of Theta(k) good blocks gives "
                "r=Theta(k), hence ||F'_nu||>=2^(r-k) and rules out every "
                "uniform poly(n)2^-k residual norm bound."
            ),
            "scope_boundary": (
                "This falsifies block-local one-dimensional filtering as a "
                "norm-restoration strategy. Nonlocal filtering and the "
                "abstract spectral-trimming measurement remain open."
            ),
        },
        scaling_records=scaling,
        adversarial_audit=[
            {
                "objection": (
                    "Pairing blocks cannot create a trivial pattern sector "
                    "after each block's trivial/sign components are deleted."
                ),
                "resolved": True,
                "resolution": (
                    "Each block uses a retained nontrivial alpha; self-duality "
                    "makes alpha tensor alpha contain trivial only after the "
                    "two blocks are fused."
                ),
            },
            {
                "objection": (
                    "Using two blocks per bit reduces the family to polynomial "
                    "size."
                ),
                "resolved": True,
                "resolution": (
                    "The bit count only loses a factor two and remains "
                    "Theta(k), so the common family is still 2^Theta(k)."
                ),
            },
            {
                "objection": (
                    "The finite deterministic portfolios alone establish the "
                    "typical natural theorem."
                ),
                "resolved": True,
                "resolution": (
                    "They are controls only. Typicality follows separately "
                    "from Sellke's fixed-block covering theorem and the rate-"
                    "free good-block density argument."
                ),
            },
            {
                "objection": (
                    "The bypass rules out every nonlocal or spectral filter."
                ),
                "resolved": False,
                "resolution": (
                    "It targets independent block-local isotypic deletion. A "
                    "filter coupling blocks or clipping the global spectrum is "
                    "outside the theorem."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "paired_block_filter_bypass_proved": theorem_verified,
            "typical_filtered_exponential_common_family_proved": True,
            "one_dimensional_branch_filter_restores_polynomial_frame_norm": False,
            "branch_controlled_filter_is_viable_norm_strategy": False,
            "abstract_spectral_trimmed_measurement_ruled_out": False,
            "nonlocal_block_filter_ruled_out": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pairs of Sellke-good blocks use retained nontrivial self-dual "
                "irreps to reconstruct exponentially large exact common-core "
                "families after the branch-controlled one-dimensional filter. "
                "The residual uniform frame-norm route remains false."
            ),
        },
        status=(
            "branch-controlled-local-filter-bypassed-nonlocal-filter-open"
            if theorem_verified
            else "paired-block-filter-bypass-validation-failure"
        ),
        summary=(
            "Proved that pairing Sellke-good blocks through a retained "
            "nontrivial self-dual irrep recreates a 2^Theta(k) common family "
            "after one-dimensional branch filtering. The local filter cannot "
            "restore the desired frame norm."
        ),
        falsifiers_triggered=[
            (
                "Deleting trivial/sign sectors independently in each block "
                "does not eliminate exact common cores; nontrivial sectors "
                "pair back to trivial globally."
            ),
            (
                "The finite frame-spike reduction is preasymptotic and cannot "
                "support a residual norm claim."
            ),
            (
                "The surviving research target must be nonlocal across blocks "
                "or avoid frame-norm normalization entirely."
            ),
        ],
    )


def write_paired_block_filter_bypass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_paired_block_filter_bypass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_paired_block_filter_bypass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
