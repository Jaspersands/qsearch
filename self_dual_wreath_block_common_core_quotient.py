"""Algebraic quotient of the thin block-common-core channels.

For a block of unequal labels ``(lambda_i,mu_i)``, define the diagonal
trivial/sign projectors on all lambda factors and all mu factors:

    T_lambda^delta = (1/n!) sum_s delta(s) tensor_i rho_lambda_i(s),
    T_mu^delta     = (1/n!) sum_s delta(s) tensor_i rho_mu_i(s).

Inside the compressed orientation Fourier carrier
``tensor_i(V_lambda_i tensor V_mu_i)``, lift these projectors by identities on
the opposite factors.  The block quotient

    C_block = (I-T_lambda^triv-T_lambda^sign)
              (I-T_mu^triv-T_mu^sign)

is an orthogonal projector.  Every replicated-block common-core vector uses
the same one-dimensional character on both sides, so ``C_block`` annihilates
it exactly.

Under independent Plancherel labels, each one-dimensional side sector has
expected normalized dimension ``1/n!``.  For disjoint blocks, the expected
retained quotient dimension is ``(1-2/n!)^(2b)=1-o(1)`` for every polynomial
number ``b`` of blocks.  Thus this quotient removes the known high-frame
spike at negligible expected carrier cost.

This is an algebraic Fourier-block construction, not yet a physical
measurement.  A coherent lift from the unknown hidden-state carrier, a
polynomial diagonal-irrep transform on the induced representation registers,
and a residual frame-norm/success theorem are all still missing.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    _orientation_representation_matrix,
    _source_representation_rows,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_block_common_core_quotient.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class BlockQuotientFiniteControl:
    n: int
    labels: tuple[Label, ...]
    compressed_carrier_dimension: int
    replicated_orientation_masks: tuple[int, int]
    common_range_dimension: int
    lambda_trivial_rank: int
    lambda_sign_rank: int
    mu_trivial_rank: int
    mu_sign_rank: int
    quotient_rank: int
    quotient_retained_dimension_fraction: float
    maximum_one_dimensional_projector_idempotence_residual: float
    maximum_one_dimensional_projector_orthogonality_residual: float
    quotient_projector_idempotence_residual: float
    common_range_annihilation_residual: float
    maximum_replicated_orientation_action_commutator_norm: float
    maximum_mixed_orientation_action_commutator_norm: float
    naive_branchwise_physical_lift_covariant: bool
    exact_block_common_core_quotient_validation: bool
    status: str


@dataclass(frozen=True)
class BlockQuotientScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    illustrative_fixed_block_size: int
    complete_block_count: int
    expected_single_side_removed_fraction: float
    expected_retained_quotient_fraction: float
    expected_removed_quotient_fraction_upper_bound: float
    retained_fraction_tends_to_one: bool
    physical_carrier_quotient_circuit_known: bool
    residual_polynomial_frame_norm_proved: bool
    status: str


@dataclass(frozen=True)
class BlockCommonCoreQuotientReport:
    created_at: str
    theorem_contract: dict[str, str]
    finite_controls: list[BlockQuotientFiniteControl]
    scaling_records: list[BlockQuotientScalingRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _permutation_sign(permutation: Permutation) -> int:
    visited = [False] * len(permutation)
    cycle_count = 0
    for start in range(len(permutation)):
        if visited[start]:
            continue
        cycle_count += 1
        position = start
        while not visited[position]:
            visited[position] = True
            position = permutation[position]
    return -1 if (len(permutation) - cycle_count) % 2 else 1


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = matrices[0]
    for matrix in matrices[1:]:
        output = np.kron(output, matrix)
    return output


@lru_cache(maxsize=None)
def block_one_dimensional_projector(
    labels: tuple[Label, ...],
    side: Literal["lambda", "mu"],
    character: Literal["trivial", "sign"],
) -> np.ndarray:
    if not labels:
        raise ValueError("at least one label is required")
    n = sum(labels[0][0])
    if any(sum(partition) != n for label in labels for partition in label):
        raise ValueError("all partitions must have the same degree")
    tables = [
        dict(_source_representation_rows(partition))
        for label in labels
        for partition in label
    ]
    permutations = tuple(tables[0])
    terms = []
    for permutation in permutations:
        factors = []
        for index, (left, right) in enumerate(labels):
            left_table = tables[2 * index]
            right_table = tables[2 * index + 1]
            if side == "lambda":
                factors.extend(
                    (
                        left_table[permutation],
                        np.eye(hook_length_dimension(right)),
                    )
                )
            elif side == "mu":
                factors.extend(
                    (
                        np.eye(hook_length_dimension(left)),
                        right_table[permutation],
                    )
                )
            else:
                raise ValueError("side must be 'lambda' or 'mu'")
        weight = (
            _permutation_sign(permutation)
            if character == "sign"
            else 1
        )
        if character not in ("trivial", "sign"):
            raise ValueError("unknown one-dimensional character")
        terms.append(weight * _kron_all(tuple(factors)))
    projector = sum(terms) / len(terms)
    return (projector + projector.T) / 2


@lru_cache(maxsize=None)
def block_common_core_quotient_projector(
    labels: tuple[Label, ...],
) -> np.ndarray:
    one_dimensional = {
        side: sum(
            block_one_dimensional_projector(labels, side, character)
            for character in ("trivial", "sign")
        )
        for side in ("lambda", "mu")
    }
    dimension = next(iter(one_dimensional.values())).shape[0]
    identity = np.eye(dimension)
    quotient = (
        (identity - one_dimensional["lambda"])
        @ (identity - one_dimensional["mu"])
    )
    return (quotient + quotient.T) / 2


@lru_cache(maxsize=None)
def validate_block_common_core_quotient() -> BlockQuotientFiniteControl:
    n = 5
    labels: tuple[Label, ...] = (
        ((4, 1), (3, 2)),
        ((4, 1), (3, 2)),
    )
    projectors = {
        (side, character): block_one_dimensional_projector(
            labels,
            side,
            character,
        )
        for side in ("lambda", "mu")
        for character in ("trivial", "sign")
    }
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors.values()
    )
    orthogonality = max(
        float(
            np.linalg.norm(
                projectors[(side, "trivial")]
                @ projectors[(side, "sign")],
                ord=2,
            )
        )
        for side in ("lambda", "mu")
    )
    quotient = block_common_core_quotient_projector(labels)
    quotient_residual = float(
        np.linalg.norm(quotient @ quotient - quotient, ord=2)
    )
    orientation_masks = (0, (1 << len(labels)) - 1)
    orientation_projectors = tuple(
        orientation_invariant_projector((n,), labels, mask)
        for mask in orientation_masks
    )
    average = sum(orientation_projectors) / len(orientation_projectors)
    eigenvalues, eigenvectors = np.linalg.eigh(average)
    common_basis = eigenvectors[:, eigenvalues > 1 - 1e-8]
    common_dimension = common_basis.shape[1]
    annihilation = (
        float(np.linalg.norm(quotient @ common_basis, ord=2))
        if common_dimension
        else math.inf
    )
    ranks = {
        key: round(float(np.trace(projector).real))
        for key, projector in projectors.items()
    }
    quotient_rank = round(float(np.trace(quotient).real))
    permutations = tuple(_source_representation_rows((n,)))
    commutators = {
        mask: max(
            float(
                np.linalg.norm(
                    quotient
                    @ _orientation_representation_matrix(
                        labels,
                        permutation,
                        mask,
                    )
                    - _orientation_representation_matrix(
                        labels,
                        permutation,
                        mask,
                    )
                    @ quotient,
                    ord=2,
                )
            )
            for permutation in permutations
        )
        for mask in range(1 << len(labels))
    }
    replicated_commutator = max(
        commutators[orientation_masks[0]],
        commutators[orientation_masks[1]],
    )
    mixed_commutator = max(
        value
        for mask, value in commutators.items()
        if mask not in orientation_masks
    )
    naive_covariant = mixed_commutator < 1e-8
    verified = (
        common_dimension > 0
        and idempotence < 1e-8
        and orthogonality < 1e-8
        and quotient_residual < 1e-8
        and annihilation < 1e-8
    )
    return BlockQuotientFiniteControl(
        n=n,
        labels=labels,
        compressed_carrier_dimension=quotient.shape[0],
        replicated_orientation_masks=orientation_masks,
        common_range_dimension=common_dimension,
        lambda_trivial_rank=ranks[("lambda", "trivial")],
        lambda_sign_rank=ranks[("lambda", "sign")],
        mu_trivial_rank=ranks[("mu", "trivial")],
        mu_sign_rank=ranks[("mu", "sign")],
        quotient_rank=quotient_rank,
        quotient_retained_dimension_fraction=quotient_rank / quotient.shape[0],
        maximum_one_dimensional_projector_idempotence_residual=idempotence,
        maximum_one_dimensional_projector_orthogonality_residual=orthogonality,
        quotient_projector_idempotence_residual=quotient_residual,
        common_range_annihilation_residual=annihilation,
        maximum_replicated_orientation_action_commutator_norm=(
            replicated_commutator
        ),
        maximum_mixed_orientation_action_commutator_norm=mixed_commutator,
        naive_branchwise_physical_lift_covariant=naive_covariant,
        exact_block_common_core_quotient_validation=verified,
        status=(
            "exact-block-common-core-quotient-validation"
            if verified
            else "block-common-core-quotient-validation-failure"
        ),
    )


def block_quotient_scaling_record(
    n: int,
    illustrative_fixed_block_size: int = 8,
) -> BlockQuotientScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if illustrative_fixed_block_size < 1:
        raise ValueError("block size must be positive")
    hidden_count = math.factorial(n)
    copies = math.ceil(math.log2(hidden_count))
    blocks = copies // illustrative_fixed_block_size
    side_removed = 2 / hidden_count
    retained = (1 - side_removed) ** (2 * blocks)
    union_removed = min(1.0, 4 * blocks / hidden_count)
    return BlockQuotientScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        illustrative_fixed_block_size=illustrative_fixed_block_size,
        complete_block_count=blocks,
        expected_single_side_removed_fraction=side_removed,
        expected_retained_quotient_fraction=retained,
        expected_removed_quotient_fraction_upper_bound=union_removed,
        retained_fraction_tends_to_one=True,
        physical_carrier_quotient_circuit_known=False,
        residual_polynomial_frame_norm_proved=False,
        status="negligible-expected-quotient-dimension-loss-physical-lift-open",
    )


def run_block_common_core_quotient() -> BlockCommonCoreQuotientReport:
    controls = [validate_block_common_core_quotient()]
    scaling = [
        block_quotient_scaling_record(n)
        for n in (5, 6, 8, 10, 16, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not record.exact_block_common_core_quotient_validation
        for record in controls
    )
    metrics: dict[str, int | float] = {
        "block_one_dimensional_isotypic_projector_theorem_count": 1,
        "block_common_core_annihilation_theorem_count": 1,
        "finite_quotient_control_count": len(controls),
        "finite_quotient_validation_failure_count": failures,
        "maximum_common_range_annihilation_residual": max(
            record.common_range_annihilation_residual for record in controls
        ),
        "maximum_quotient_projector_idempotence_residual": max(
            record.quotient_projector_idempotence_residual
            for record in controls
        ),
        "maximum_replicated_orientation_action_commutator_norm": max(
            record.maximum_replicated_orientation_action_commutator_norm
            for record in controls
        ),
        "maximum_mixed_orientation_action_commutator_norm": max(
            record.maximum_mixed_orientation_action_commutator_norm
            for record in controls
        ),
        "naive_branchwise_physical_lift_covariance_count": sum(
            record.naive_branchwise_physical_lift_covariant
            for record in controls
        ),
        "scaling_record_count": len(scaling),
        "plancherel_expected_retained_fraction_one_minus_o_one_theorem_count": 1,
        "tail_n": scaling[-1].n,
        "tail_complete_block_count": scaling[-1].complete_block_count,
        "tail_expected_removed_fraction_upper_bound": (
            scaling[-1].expected_removed_quotient_fraction_upper_bound
        ),
        "physical_carrier_quotient_circuit_count": 0,
        "residual_polynomial_frame_norm_theorem_count": 0,
        "compressed_covariant_outcome_transform_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem_verified = failures == 0
    return BlockCommonCoreQuotientReport(
        created_at=utc_now(),
        theorem_contract={
            "side_projectors": (
                "T_side^delta is the diagonal S_n group average weighted by "
                "delta in {trivial,sign}; these are orthogonal projectors."
            ),
            "block_quotient": (
                "C_block removes trivial and sign sectors independently from "
                "all lambda factors and all mu factors in the block."
            ),
            "common_core_annihilation": (
                "Every replicated-bit block common-core vector occupies a "
                "matched one-dimensional sector on both sides, hence is in "
                "the kernel of C_block."
            ),
            "expected_cost": (
                "For b disjoint iid Plancherel blocks, expected retained "
                "normalized quotient dimension is (1-2/n!)^(2b), which tends "
                "to one for polynomial b."
            ),
            "physical_boundary": (
                "The quotient is defined after orientation-Fourier "
                "compression. It commutes with replicated all-lambda/all-mu "
                "actions but not mixed orientation actions, so the naive "
                "branchwise lift to unknown P_s inputs is not covariant."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        adversarial_audit=[
            {
                "objection": (
                    "Removing both one-dimensional side sectors still leaves "
                    "the replicated-bit common vector."
                ),
                "resolved": True,
                "resolution": (
                    "The fixed-family parity theorem constructs that vector "
                    "inside exactly those side sectors; an explicit 400-"
                    "dimensional control is annihilated to numerical zero."
                ),
            },
            {
                "objection": (
                    "Deleting the known common cores costs a constant fraction "
                    "of the natural carrier."
                ),
                "resolved": True,
                "resolution": (
                    "Exact Plancherel stationarity gives expected loss at most "
                    "4b/n!, which vanishes for polynomial b."
                ),
            },
            {
                "objection": (
                    "The Fourier-block quotient is already a legal efficient "
                    "measurement on the unknown coset-state input."
                ),
                "resolved": False,
                "resolution": (
                    "The finite quotient has norm-one commutators with mixed "
                    "orientation actions. A naive branchwise induced-carrier "
                    "lift is therefore noncovariant; a coherent harmonic "
                    "transform or larger invariant quotient is required."
                ),
            },
            {
                "objection": (
                    "Killing the explicit Sellke common cores proves the "
                    "residual frame has polynomial norm."
                ),
                "resolved": False,
                "resolution": (
                    "Other correlated families, near-common channels, or "
                    "higher-dimensional shared sectors may still produce a "
                    "large residual norm."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "block_one_dimensional_projectors_explicit": theorem_verified,
            "replicated_bit_common_cores_annihilated": theorem_verified,
            "expected_quotient_dimension_retained_one_minus_o_one": True,
            "naive_branchwise_physical_lift_covariant": False,
            "physical_carrier_quotient_circuit_proved": False,
            "residual_polynomial_frame_norm_proved": False,
            "all_high_frame_spikes_removed": False,
            "compressed_covariant_outcome_transform_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A thin algebraic quotient removes the explicit Sellke block "
                "common cores at negligible expected dimension cost. The "
                "physical lift, residual spectrum, outcome transform, and "
                "decoder remain unproved."
            ),
        },
        status=(
            "algebraic-common-core-quotient-physical-lift-open"
            if theorem_verified
            else "block-common-core-quotient-validation-failure"
        ),
        summary=(
            "Constructed an exact block-local quotient that annihilates the "
            "known replicated-orientation common cores while retaining "
            "expected Plancherel carrier fraction 1-o(1). A physical coherent "
            "lift and residual norm theorem are the next gates."
        ),
        falsifiers_triggered=[
            (
                "The typical frame-norm counterexample is not robust to "
                "deleting its explicitly characterized one-dimensional block "
                "channels."
            ),
            (
                "Support-rich common cores can be algebraically removed with "
                "negligible expected dimension loss, but this is not yet a "
                "measurement circuit."
            ),
            (
                "The naive branchwise physical lift fails covariance: mixed "
                "orientation actions have norm-one commutators with the "
                "algebraic quotient."
            ),
            (
                "Residual high-dimensional and near-common channels must be "
                "audited before any restored norm or success claim."
            ),
        ],
    )


def write_block_common_core_quotient_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_block_common_core_quotient())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_block_common_core_quotient_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
