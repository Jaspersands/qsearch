"""Physical-access obstruction for dual orientation filters.

The orientation Fourier blocks live on the orbit-Gram (dual) domain.  Let
``V_s: C^r -> H`` be hidden-label isometries, ``P_s=V_s V_s^*``, and

    T = M^-1/2 sum_s V_s <s|,
    B = T T^* = M^-1 sum_s P_s,
    G = T^* T.

The polynomial orientation invariant-projector circuit acts after reaching
the domain of ``G``.  The direct physical-to-dual analysis map is ``T^*``.
For any dual contraction ``0 <= D <= I``, the conclusive Kraus operator
``A_D=D^(1/2)T^*`` satisfies, on the uniformly averaged hidden state,

    p_conclusive
      = Tr(D G^2) / r
      <= Tr(G^2) / r
      = Tr(B^2) / r.

For the wreath bridge ensemble this last quantity is

    (2^k + M - 1)/(M 2^k) = Theta(1/M),

with ``M=n!`` at ``k=ceil(log2 M)``.  Therefore a dual orientation filter
composed after the direct analysis map is factorially inconclusive, no matter
how efficiently the dual contraction itself is implemented.

This does not rule out the filter.  The companion physical-orientation
interference theorem now supplies the second escape: a direct branch-carrier
realization that never factors through ``T^*``.  The bound here remains the
reason that implementations must use that physical route rather than direct
orbit-Gram analysis.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import _source_data, _tensor_states
from research_registry import utc_now
from self_dual_wreath_spectral_trimmed_subpovm import (
    _projectors_from_normalized_states,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_filter_physical_access.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class DualAccessFiniteControl:
    control_id: str
    n: int
    source_partitions: tuple[Partition, ...]
    hidden_label_count: int
    physical_dimension: int
    projector_rank: int
    dual_dimension: int
    frame_second_moment_per_rank: float
    direct_analysis_average_success: float
    contracted_dual_filter_average_success: float
    dual_contraction_trace_formula: float
    maximum_allowed_dual_contraction_success: float
    synthesis_frame_identity_residual: float
    gram_spectrum_identity_residual: float
    direct_success_formula_residual: float
    contraction_bound_violation: float
    exact_physical_dual_access_bound_verified: bool
    status: str


@dataclass(frozen=True)
class DualAccessScalingRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    information_threshold_copy_count: int
    direct_dual_access_success_upper_bound: float
    direct_dual_access_success_log2_upper_bound: float
    generic_amplitude_amplification_lower_bound_log2: float
    polynomial_success_benchmark: float
    direct_dual_access_inverse_polynomial: bool
    status: str


@dataclass(frozen=True)
class OrientationFilterPhysicalAccessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[DualAccessFiniteControl]
    scaling_records: list[DualAccessScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _projector_isometries(
    projectors: tuple[np.ndarray, ...],
    rank: int,
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    output = []
    for projector in projectors:
        eigenvalues, eigenvectors = np.linalg.eigh(
            (projector + projector.T.conj()) / 2
        )
        selected = eigenvalues > 1 - 100 * tolerance
        if int(np.sum(selected)) != rank:
            raise ArithmeticError("projector rank does not match eigenspace")
        output.append(eigenvectors[:, selected])
    return tuple(output)


def audit_dual_access_bound(
    states: tuple[np.ndarray, ...],
    *,
    control_id: str,
    n: int,
    source_partitions: tuple[Partition, ...],
    tolerance: float = 1e-10,
) -> DualAccessFiniteControl:
    projectors, rank, _ = _projectors_from_normalized_states(states, tolerance)
    isometries = _projector_isometries(projectors, rank, tolerance)
    hidden_count = len(projectors)
    synthesis = np.concatenate(isometries, axis=1) / math.sqrt(hidden_count)
    frame = sum(projectors) / hidden_count
    gram = synthesis.T.conj() @ synthesis
    frame_residual = float(
        np.linalg.norm(synthesis @ synthesis.T.conj() - frame, ord=2)
    )
    physical_eigenvalues = np.linalg.eigvalsh(frame)
    gram_eigenvalues = np.linalg.eigvalsh(gram)
    physical_positive = physical_eigenvalues[physical_eigenvalues > tolerance]
    gram_positive = gram_eigenvalues[gram_eigenvalues > tolerance]
    spectrum_residual = float(
        np.max(np.abs(physical_positive - gram_positive))
        if len(physical_positive) == len(gram_positive) and len(physical_positive)
        else 0.0 if len(physical_positive) == len(gram_positive) else math.inf
    )
    second_scale = float(np.trace(frame @ frame).real / rank)
    average_state = frame / rank

    direct_effect = synthesis @ synthesis.T.conj()
    direct_success = float(np.trace(direct_effect @ average_state).real)

    # A nontrivial dual contraction chosen spectrally and bounded by identity.
    gram_values, gram_vectors = np.linalg.eigh(gram)
    contraction_values = np.where(gram_values <= second_scale, 1.0, 0.25)
    contraction = (
        gram_vectors * contraction_values
    ) @ gram_vectors.T.conj()
    contracted_effect = synthesis @ contraction @ synthesis.T.conj()
    contracted_success = float(
        np.trace(contracted_effect @ average_state).real
    )
    trace_formula = float(
        np.trace(contraction @ gram @ gram).real / rank
    )
    formula_residual = abs(contracted_success - trace_formula)
    violation = max(0.0, contracted_success - second_scale)
    verified = (
        frame_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and abs(direct_success - second_scale) <= 100 * tolerance
        and formula_residual <= 100 * tolerance
        and violation <= 100 * tolerance
    )
    return DualAccessFiniteControl(
        control_id=control_id,
        n=n,
        source_partitions=source_partitions,
        hidden_label_count=hidden_count,
        physical_dimension=frame.shape[0],
        projector_rank=rank,
        dual_dimension=gram.shape[0],
        frame_second_moment_per_rank=second_scale,
        direct_analysis_average_success=direct_success,
        contracted_dual_filter_average_success=contracted_success,
        dual_contraction_trace_formula=trace_formula,
        maximum_allowed_dual_contraction_success=second_scale,
        synthesis_frame_identity_residual=frame_residual,
        gram_spectrum_identity_residual=spectrum_residual,
        direct_success_formula_residual=formula_residual,
        contraction_bound_violation=violation,
        exact_physical_dual_access_bound_verified=verified,
        status=(
            "exact-direct-dual-access-success-bound"
            if verified
            else "physical-dual-access-validation-failure"
        ),
    )


def finite_dual_access_control(
    n: int,
    transposition_count: int,
    source_partitions: tuple[Partition, ...],
) -> DualAccessFiniteControl:
    partitions, _, state_families = _source_data(n, transposition_count)
    by_partition = dict(zip(partitions, state_families))
    states = _tensor_states(
        tuple(by_partition[partition] for partition in source_partitions)
    )
    return audit_dual_access_bound(
        states,
        control_id=(
            f"S{n}-T{transposition_count}-"
            f"{'_'.join('-'.join(map(str, row)) for row in source_partitions)}"
        ),
        n=n,
        source_partitions=source_partitions,
    )


def dual_access_scaling_record(n: int) -> DualAccessScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    hidden_count = math.factorial(n)
    copies = math.ceil(math.log2(hidden_count))
    subset_count = 1 << copies
    log_success = (
        math.log2(subset_count + hidden_count - 1)
        - math.log2(hidden_count)
        - copies
    )
    second_scale = math.exp2(log_success)
    polynomial_log_benchmark = -10 * math.log2(n)
    return DualAccessScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        log2_hidden_label_count=math.log2(hidden_count),
        information_threshold_copy_count=copies,
        direct_dual_access_success_upper_bound=second_scale,
        direct_dual_access_success_log2_upper_bound=log_success,
        generic_amplitude_amplification_lower_bound_log2=-0.5 * log_success,
        polynomial_success_benchmark=n**-10,
        direct_dual_access_inverse_polynomial=(
            log_success >= polynomial_log_benchmark
        ),
        status="factorially-inconclusive-direct-physical-to-dual-map",
    )


def run_orientation_filter_physical_access() -> OrientationFilterPhysicalAccessReport:
    controls = [
        finite_dual_access_control(3, 1, ((2, 1),)),
        finite_dual_access_control(3, 1, ((2, 1), (2, 1))),
        finite_dual_access_control(4, 1, ((3, 1), (2, 2))),
    ]
    scaling = [
        dual_access_scaling_record(n)
        for n in (16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)
    ]
    failures = sum(
        not row.exact_physical_dual_access_bound_verified for row in controls
    )
    verified = failures == 0
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "synthesis_frame_factorization",
            "resolved": verified,
            "resolution": "TT^*=B and T^*T=G by construction.",
        },
        {
            "obligation": "physical_average_state",
            "resolved": True,
            "resolution": "The uniform hidden-state mixture is B/r.",
        },
        {
            "obligation": "dual_contraction_success_identity",
            "resolved": verified,
            "resolution": (
                "Cyclicity of trace gives p=Tr(D T^*BT)/r="
                "Tr(DG^2)/r."
            ),
        },
        {
            "obligation": "universal_direct_access_upper_bound",
            "resolved": verified,
            "resolution": (
                "For 0<=D<=I, Tr(DG^2)<=Tr(G^2)=Tr(B^2)."
            ),
        },
        {
            "obligation": "structured_physical_dual_transfer",
            "resolved": False,
            "resolution": (
                "No polynomial partial isometry equivalent to the polar map "
                "T^*B^-1/2 is known on the natural support."
            ),
        },
    ]
    return OrientationFilterPhysicalAccessReport(
        created_at=utc_now(),
        theorem_contract={
            "synthesis": "T=M^-1/2 sum_s V_s<s|.",
            "frame_and_gram": "B=TT^*, G=T^*T.",
            "direct_dual_filter": (
                "A_D=D^(1/2)T^* for an arbitrary dual contraction 0<=D<=I."
            ),
            "average_success": "p_D=Tr(DG^2)/r.",
            "upper_bound": "p_D<=Tr(B^2)/r.",
            "wreath_scale": (
                "Tr(B^2)/r=(2^k+M-1)/(M2^k)=Theta(1/M) at "
                "k=ceil(log2 M), M=n!."
            ),
            "scope": (
                "The theorem covers every implementation that first reaches "
                "the orbit-Gram domain through the direct synthesis adjoint. "
                "It does not cover a structured polar transfer or a direct "
                "physical interference circuit."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "A better dual contraction D can increase direct access success.",
                "resolved": True,
                "resolution": (
                    "No positive contraction can exceed D=I in the trace "
                    "against G^2. Filtering only decreases conclusive mass."
                ),
            },
            {
                "objection": "The polynomial E_h circuit makes the full filter physical.",
                "resolved": True,
                "resolution": (
                    "It makes E_h efficient once the dual carrier is present; "
                    "it does not create the dual carrier from the hidden state."
                ),
            },
            {
                "objection": "The result rules out a structured polar isometry.",
                "resolved": False,
                "resolution": (
                    "A physical-to-dual map that divides out T's singular "
                    "values is outside the direct-analysis factorization."
                ),
            },
            {
                "objection": "A direct physical orientation-interference construction is impossible.",
                "resolved": False,
                "resolution": (
                    "The theorem does not cover a new circuit acting on the "
                    "physical multiplicity spaces without using T^*."
                ),
            },
        ],
        headline_metrics={
            "direct_physical_to_dual_success_bound_theorem_count": 1,
            "arbitrary_dual_contraction_bound_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_validation_failure_count": failures,
            "scaling_record_count": len(scaling),
            "inverse_polynomial_direct_access_row_count": sum(
                row.direct_dual_access_inverse_polynomial for row in scaling
            ),
            "tail_n": scaling[-1].n,
            "tail_direct_access_success_log2": (
                scaling[-1].direct_dual_access_success_log2_upper_bound
            ),
            "tail_amplification_lower_bound_log2": (
                scaling[-1].generic_amplitude_amplification_lower_bound_log2
            ),
            "structured_polar_transfer_count": 0,
            "direct_physical_orientation_filter_count": 1,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_filter_dual_algebra_valid": True,
            "dual_invariant_projector_circuit_polynomial": True,
            "direct_physical_to_dual_filter_polynomially_conclusive": False,
            "factorial_direct_access_obstruction_proved": verified,
            "structured_polar_transfer_ruled_out": False,
            "direct_physical_filter_ruled_out": False,
            "direct_physical_orientation_filter_constructed": True,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The dual filter is efficient only after entering the orbit-"
                "Gram domain. The direct entry map has Theta(1/n!) average "
                "success. The companion branch-interference circuit bypasses "
                "this factorization directly; its all-n information and norm "
                "theorems remain open."
            ),
        },
        status=(
            "direct-dual-filter-access-falsified-structured-transfer-open"
            if verified
            else "physical-dual-access-validation-failure"
        ),
        summary=(
            "Proved that every dual contraction composed after the direct "
            "synthesis adjoint has at most Theta(1/n!) average conclusive "
            "probability, while preserving the separately constructed direct "
            "physical branch-interference bypass."
        ),
        falsifiers_triggered=[
            (
                "Polynomial manipulation of orientation Fourier blocks does "
                "not by itself yield a polynomial physical measurement."
            ),
            (
                "Postprocessing the direct dual-analysis map cannot improve "
                "its factorially weak average success."
            ),
            (
                "The direct physical multiplicity-space interference filter "
                "must now be tested for all-n retained information and norm."
            ),
        ],
    )


def write_orientation_filter_physical_access_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_filter_physical_access())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_filter_physical_access_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
