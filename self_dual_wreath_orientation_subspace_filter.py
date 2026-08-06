"""Orientation-subspace Fourier filter for exact common-core rejection.

Let ``E_h`` be orientation invariant-subspace projectors indexed by
``h in H = F_2^r`` and put ``F_H=|H|^-1 sum_h E_h``.  Coherently prepare a
uniform ``h``, apply the controlled projector, and Fourier transform the
control.  The Kraus operator for character ``z`` is

    G_z = |H|^-1 sum_h (-1)^(z.h) E_h.

Character orthogonality gives

    sum_z G_z^* G_z = F_H,
    G_0 = F_H,
    sum_{z != 0} G_z^* G_z = F_H - F_H^2.

Thus accepting a nontrivial Fourier character exactly annihilates the common
range ``intersection_h Ran(E_h)``: on that range ``F_H=I``.  The operation
works at unit spectral scale even when the same common family contributes
only ``|H|/2^k`` to the full orientation frame.  It therefore bypasses both
the disjoint local-filter no-go and the generic ``Theta(1/n!)`` spectral
resolution barrier at the algebraic level.

The companion invariant-projector circuit theorem implements controlled
``E_h`` in polynomial time through coherent group averaging and the efficient
``S_n`` QFT.  What remains open is not this local primitive but an all-n proof
that a polynomial composition of such filters retains constant hidden-label
information, followed by an efficient decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_subspace_filter.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class OrientationSubspaceFilterControl:
    control_id: str
    source: str
    n: int | None
    target_partition: Partition | None
    labels: tuple[Label, ...]
    orientation_subspace_dimension: int
    orientation_projector_count: int
    carrier_dimension: int
    minimum_projector_rank: int
    maximum_projector_rank: int
    common_range_dimension: int
    average_frame_top_eigenvalue: float
    nontrivial_character_effect_top_eigenvalue: float
    retained_trace_fraction: float
    maximum_projector_idempotence_residual: float
    fourier_kraus_completeness_residual: float
    nontrivial_effect_identity_residual: float
    common_range_annihilation_residual: float
    exact_filter_identity_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationSubspaceFilterReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[OrientationSubspaceFilterControl]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def orientation_fourier_kraus(
    projectors: tuple[np.ndarray, ...],
) -> tuple[np.ndarray, ...]:
    if not projectors:
        raise ValueError("at least one projector is required")
    count = len(projectors)
    if count & (count - 1):
        raise ValueError("projector count must be a power of two")
    shape = projectors[0].shape
    if len(shape) != 2 or shape[0] != shape[1]:
        raise ValueError("projectors must be square matrices")
    if any(projector.shape != shape for projector in projectors):
        raise ValueError("projector dimensions must agree")
    output = []
    for character in range(count):
        operator = np.zeros(shape, dtype=np.result_type(*projectors))
        for orientation, projector in enumerate(projectors):
            sign = -1 if (character & orientation).bit_count() % 2 else 1
            operator += sign * projector
        output.append(operator / count)
    return tuple(output)


def audit_orientation_subspace_filter(
    projectors: tuple[np.ndarray, ...],
    *,
    control_id: str,
    source: str,
    n: int | None = None,
    target_partition: Partition | None = None,
    labels: tuple[Label, ...] = (),
    tolerance: float = 1e-10,
) -> OrientationSubspaceFilterControl:
    kraus = orientation_fourier_kraus(projectors)
    count = len(projectors)
    dimension = projectors[0].shape[0]
    frame = sum(projectors) / count
    frame = (frame + frame.T.conj()) / 2
    effects = tuple(operator.T.conj() @ operator for operator in kraus)
    effect_sum = sum(effects, np.zeros_like(frame))
    nontrivial_effect = sum(effects[1:], np.zeros_like(frame))
    expected_nontrivial = frame - frame @ frame
    eigenvalues, eigenvectors = np.linalg.eigh(frame)
    common = eigenvalues >= 1 - 100 * tolerance
    common_basis = eigenvectors[:, common]
    annihilation = (
        float(np.linalg.norm(nontrivial_effect @ common_basis, ord=2))
        if common_basis.shape[1]
        else 0.0
    )
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    completeness = float(np.linalg.norm(effect_sum - frame, ord=2))
    identity_residual = float(
        np.linalg.norm(nontrivial_effect - expected_nontrivial, ord=2)
    )
    trace_frame = float(np.trace(frame).real)
    trace_nontrivial = float(np.trace(nontrivial_effect).real)
    retained = trace_nontrivial / trace_frame if trace_frame > tolerance else 0.0
    nontrivial_eigenvalues = np.linalg.eigvalsh(
        (nontrivial_effect + nontrivial_effect.T.conj()) / 2
    )
    ranks = [round(float(np.trace(projector).real)) for projector in projectors]
    verified = (
        idempotence <= 100 * tolerance
        and completeness <= 100 * tolerance
        and identity_residual <= 100 * tolerance
        and annihilation <= 100 * tolerance
        and float(nontrivial_eigenvalues[0]) >= -100 * tolerance
        and float(nontrivial_eigenvalues[-1]) <= 0.25 + 100 * tolerance
    )
    return OrientationSubspaceFilterControl(
        control_id=control_id,
        source=source,
        n=n,
        target_partition=target_partition,
        labels=labels,
        orientation_subspace_dimension=int(math.log2(count)),
        orientation_projector_count=count,
        carrier_dimension=dimension,
        minimum_projector_rank=min(ranks),
        maximum_projector_rank=max(ranks),
        common_range_dimension=int(np.sum(common)),
        average_frame_top_eigenvalue=float(eigenvalues[-1]),
        nontrivial_character_effect_top_eigenvalue=float(
            nontrivial_eigenvalues[-1]
        ),
        retained_trace_fraction=retained,
        maximum_projector_idempotence_residual=idempotence,
        fourier_kraus_completeness_residual=completeness,
        nontrivial_effect_identity_residual=identity_residual,
        common_range_annihilation_residual=annihilation,
        exact_filter_identity_verified=verified,
        status=(
            "exact-orientation-subspace-fourier-filter"
            if verified
            else "orientation-subspace-filter-validation-failure"
        ),
    )


def synthetic_common_core_control() -> OrientationSubspaceFilterControl:
    vectors = (
        np.asarray([0.0, 1.0, 0.0, 0.0]),
        np.asarray([0.0, 0.0, 1.0, 0.0]),
        np.asarray([0.0, 0.0, 0.0, 1.0]),
        np.asarray([0.0, 1.0, 1.0, 1.0]) / math.sqrt(3),
    )
    common = np.asarray([1.0, 0.0, 0.0, 0.0])
    projectors = tuple(
        np.outer(common, common) + np.outer(vector, vector)
        for vector in vectors
    )
    return audit_orientation_subspace_filter(
        projectors,
        control_id="SYNTHETIC-F2-2-COMMON-CORE",
        source="synthetic-equal-rank-projectors",
    )


def physical_w4_controls() -> list[OrientationSubspaceFilterControl]:
    controls = []
    for tuple_index, labels in enumerate(_w4_collision_free_labels()):
        for target in integer_partitions(4):
            projectors = tuple(
                orientation_invariant_projector(target, labels, mask)
                for mask in range(1 << len(labels))
            )
            controls.append(
                audit_orientation_subspace_filter(
                    projectors,
                    control_id=f"W4-{tuple_index}-{'-'.join(map(str, target))}",
                    source="physical-collision-free-wreath-fourier-block",
                    n=4,
                    target_partition=target,
                    labels=labels,
                )
            )
    return controls


def run_orientation_subspace_filter() -> OrientationSubspaceFilterReport:
    controls = [synthetic_common_core_control(), *physical_w4_controls()]
    failures = sum(not row.exact_filter_identity_verified for row in controls)
    physical = [row for row in controls if row.n is not None]
    common_controls = [row for row in controls if row.common_range_dimension > 0]
    verified = failures == 0 and bool(common_controls)
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "fourier_kraus_completeness",
            "resolved": verified,
            "resolution": (
                "Character orthogonality gives sum_z G_z^*G_z=|H|^-1 "
                "sum_h E_h=F_H exactly."
            ),
        },
        {
            "obligation": "nontrivial_character_effect",
            "resolved": verified,
            "resolution": (
                "The trivial Kraus operator is G_0=F_H, hence accepting all "
                "other characters has effect F_H-F_H^2."
            ),
        },
        {
            "obligation": "common_core_annihilation",
            "resolved": verified,
            "resolution": (
                "Every common vector has F_H eigenvalue one and is in the "
                "kernel of F_H-F_H^2."
            ),
        },
        {
            "obligation": "coherent_controlled_invariant_projector",
            "resolved": True,
            "resolution": (
                "self_dual_wreath_invariant_projector_circuit.py proves a "
                "polynomial projected encoding using uniform group averaging, "
                "reversible left multiplication, and Beals' S_n QFT."
            ),
        },
        {
            "obligation": "end_to_end_hidden_label_success",
            "resolved": False,
            "resolution": (
                "The local block effect is not yet composed with a complete "
                "covariant hidden-permutation measurement and decoder."
            ),
        },
    ]
    return OrientationSubspaceFilterReport(
        created_at=utc_now(),
        theorem_contract={
            "orientation_family": "H=F_2^r with projectors E_h.",
            "coherent_kraus": (
                "G_z=|H|^-1 sum_h (-1)^(z.h)E_h after a binary Fourier "
                "transform of the orientation control."
            ),
            "completeness": "sum_z G_z^*G_z=F_H.",
            "accepted_effect": (
                "Accepting z!=0 implements D_H=F_H-F_H^2, with spectrum "
                "lambda(1-lambda) in [0,1/4]."
            ),
            "common_core": (
                "intersection_h Ran(E_h) is the eigenvalue-one space of F_H "
                "and is annihilated exactly by D_H."
            ),
            "scale_bypass": (
                "The selected family is normalized internally, so its common "
                "core sits at eigenvalue one rather than |H|/2^k."
            ),
            "implementation_boundary": (
                "Efficient uniform-mask preparation and binary Fourier "
                "transform are elementary; controlled E_h has a polynomial "
                "projected circuit. Postfilter information is the boundary."
            ),
        },
        controls=controls,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "The accepted effect may fail positivity because E_h do not commute.",
                "resolved": True,
                "resolution": (
                    "It is a sum of Kraus squares. The identity with "
                    "F_H-F_H^2 also proves positivity since 0<=F_H<=I."
                ),
            },
            {
                "objection": "This is merely the forbidden tiny-scale global spectral filter.",
                "resolved": True,
                "resolution": (
                    "No eigenvalue estimation is used. Coherent interference "
                    "within H rescales the selected common mode to one."
                ),
            },
            {
                "objection": "Removing exact common cores controls every near-common spike.",
                "resolved": False,
                "resolution": (
                    "No. Eigenvalues near one are attenuated, but an all-n "
                    "bound after composing multiple families is still needed."
                ),
            },
            {
                "objection": "The invariant projectors are already efficiently implementable from an S_n QFT.",
                "resolved": True,
                "resolution": (
                    "Yes. One does not need a Kronecker basis: uniform group "
                    "averaging gives E_h as a Kraus block, while QFT-conjugated "
                    "left multiplication implements every irrep action."
                ),
            },
        ],
        headline_metrics={
            "orientation_subspace_fourier_filter_theorem_count": 1,
            "exact_common_core_annihilation_theorem_count": 1,
            "finite_control_count": len(controls),
            "physical_w4_control_count": len(physical),
            "finite_validation_failure_count": failures,
            "common_range_control_count": len(common_controls),
            "maximum_common_range_dimension": max(
                row.common_range_dimension for row in controls
            ),
            "minimum_retained_trace_fraction": min(
                row.retained_trace_fraction for row in controls
            ),
            "maximum_retained_trace_fraction": max(
                row.retained_trace_fraction for row in controls
            ),
            "maximum_common_range_annihilation_residual": max(
                row.common_range_annihilation_residual for row in controls
            ),
            "polynomial_controlled_invariant_projector_count": 1,
            "all_n_postfilter_norm_theorem_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_fourier_filter_identity_proved": verified,
            "exact_selected_common_cores_annihilated": verified,
            "generic_factorial_spectral_resolution_required": False,
            "polynomial_controlled_invariant_projector_proved": True,
            "all_n_near_common_spectrum_controlled": False,
            "end_to_end_hidden_label_measurement_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first genuinely nonlocal unit-scale common-core filter "
                "has a polynomial invariant-projector circuit schema, but its "
                "all-n postfilter spectrum, retained information, and decoder "
                "are open."
            ),
        },
        status=(
            "unit-scale-common-core-filter-circuit-schema-postfilter-open"
            if verified
            else "orientation-subspace-filter-validation-failure"
        ),
        summary=(
            "Constructed a coherent orientation-character filter with effect "
            "F_H-F_H^2 that exactly removes selected common cores without "
            "factorial-scale spectral estimation."
        ),
        falsifiers_triggered=[
            (
                "The common-core spike can be addressed at unit scale by "
                "coherent orientation interference; generic low-pass phase "
                "estimation is not the only algebraic route."
            ),
            (
                "Disjoint branchwise isotypic deletion is unnecessary for "
                "the filter identity, so the local-filter no-go does not apply."
            ),
            (
                "No speedup is claimed until postfilter scaling, retained "
                "hidden-label information, and decoding are proved."
            ),
        ],
    )


def write_orientation_subspace_filter_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_subspace_filter())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_subspace_filter_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
