"""Dimensionless PGM truncation bridge for carrier-conditioned ensembles.

Let ``rho_h`` be equiprobable density operators supported on a known
``D``-dimensional space, with average ``B`` and rank-scaled metric

    G = D B,             Tr(G)=D.                         (1)

For ``P_eps=1[G>=eps]``, the average state mass below the cutoff obeys

    delta = Tr((I-P_eps)B)
          = D^-1 sum_(lambda_i(G)<eps) lambda_i(G)
          <= eps.                                        (2)

If ``E_h`` are the ideal PGM effects, then ``P_eps E_h P_eps`` together
with a failure outcome is a legal POVM.  The gentle measurement lemma gives

    p_truncated >= p_PGM - 2 sqrt(delta)
                >= p_PGM - 2 sqrt(eps).                  (3)

Consequently, any proved PGM lower bound ``c`` can be retained at least
``c/2`` by choosing ``eps=c^2/16``.  The actual minimum positive eigenvalue
of ``G`` is not an algorithmic obligation.  A block encoding normalized by
``alpha`` only needs inverse-square-root approximation above the controlled
scale ``eps/alpha``.

For ``q`` disjoint pair-carrier pinches at the hidden-involution information
threshold, the existing certificate is

    c_q = 1/(4^q + 16^q 2^-s).                            (4)

Thus fixed ``q`` permits a constant cutoff.  For
``q=ceil(log_2 n)`` and ``s=0``, ``c_q>=1/(20 n^4)`` and
``eps>=1/(6400 n^8)``.  Truncation therefore removes the minimum-eigenvalue
barrier even at logarithmic pair depth.

This theorem does not provide a block encoding of the full information-
threshold metric.  The two-pair covariance LCU only handles its four-copy
subsystem; remaining singleton blocks and higher shared-label cumulants must
still be incorporated.  It also does not compile the PGM Naimark/output map
or a hidden-involution decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_carrier_branch_pgm_success_certificate import (
    disjoint_pair_threshold_success_lower_bound,
)
from self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary import (
    _pair_carrier_branches,
    _pgm_data,
    perfect_matching_count,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_dimensionless_pgm_truncation_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-DIMENSIONLESS-PGM-TRUNCATION-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class DimensionlessTruncationControl:
    control_id: str
    n: int
    transposition_count: int
    left_source_partitions: tuple[Partition, Partition]
    right_source_partitions: tuple[Partition, Partition]
    left_carrier_partition: Partition
    right_carrier_partition: Partition
    hidden_involution_count: int
    product_support_dimension: int
    dimensionless_metric_trace: float
    dimensionless_metric_trace_residual: float
    spectral_cutoff: float
    retained_metric_rank: int
    discarded_support_dimension: int
    discarded_positive_eigenvalue_count: int
    discarded_average_state_mass: float
    discarded_mass_dimension_bound: float
    universal_discarded_mass_bound: float
    ideal_pgm_success: float
    truncated_pgm_success: float
    gentle_success_lower_bound: float
    observed_success_loss: float
    maximum_truncated_inverse_effect_residual: float
    truncated_effect_completeness_residual: float
    truncated_effect_subpovm_eigenvalue_violation: float
    minimum_retained_metric_eigenvalue: float
    maximum_metric_eigenvalue: float
    retained_metric_condition_number: float
    nontrivial_positive_spectrum_truncation: bool
    exact_dimensionless_truncation_verified: bool
    status: str


@dataclass(frozen=True)
class ThresholdTruncationScalingRecord:
    schedule: str
    n: int
    hidden_involution_count_decimal: str
    information_threshold_copy_count: int
    disjoint_pair_count: int
    threshold_slack: int
    pgm_success_lower_bound: float
    sufficient_dimensionless_cutoff: float
    retained_success_lower_bound: float
    inverse_square_root_amplification_upper_bound: float
    conservative_condition_scale_upper_bound: float
    pair_budget_legal: bool
    cutoff_inverse_polynomial_proved: bool
    minimum_positive_eigenvalue_required: bool
    full_threshold_metric_block_encoding_compiled: bool
    status: str


@dataclass(frozen=True)
class DimensionlessPgmTruncationTheorem:
    rank_scaled_metric: str
    low_spectral_mass: str
    legal_truncated_pgm: str
    gentle_success_retention: str
    certificate_cutoff: str
    fixed_pair_depth_consequence: str
    logarithmic_pair_depth_consequence: str
    qsvt_consequence: str
    scope: str
    dimensionless_low_mass_bound_proved: bool
    mixed_state_truncated_pgm_robustness_proved: bool
    certificate_adaptive_cutoff_proved: bool
    fixed_depth_constant_cutoff_proved: bool
    logarithmic_depth_inverse_polynomial_cutoff_proved: bool
    minimum_positive_spectral_edge_required: bool
    full_threshold_metric_block_encoding_compiled: bool
    pgm_output_isometry_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DimensionlessPgmTruncationBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DimensionlessPgmTruncationTheorem
    finite_controls: list[DimensionlessTruncationControl]
    scaling_records: list[ThresholdTruncationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def sufficient_dimensionless_cutoff(success_lower_bound: float) -> float:
    if not 0 < success_lower_bound <= 1:
        raise ValueError("success lower bound must lie in (0,1]")
    return success_lower_bound * success_lower_bound / 16.0


def logarithmic_pair_success_polynomial_lower_bound(n: int) -> float:
    if n < 2:
        raise ValueError("n must be at least two")
    return 1.0 / (20.0 * n**4)


def logarithmic_pair_cutoff_polynomial_lower_bound(n: int) -> float:
    if n < 2:
        raise ValueError("n must be at least two")
    return 1.0 / (6400.0 * n**8)


def _select_carrier_branch(
    branches: tuple[Any, ...],
    target: Partition,
) -> Any:
    matches = [branch for branch in branches if branch.carrier_partition == target]
    if len(matches) != 1:
        raise ValueError(f"expected one active carrier branch for target {target}")
    return matches[0]


def audit_dimensionless_branch_truncation(
    n: int,
    transposition_count: int,
    left_pair_indices: tuple[int, int],
    right_pair_indices: tuple[int, int],
    left_carrier_partition: Partition,
    right_carrier_partition: Partition,
    *,
    spectral_cutoff: float,
    tolerance: float = 1e-9,
) -> DimensionlessTruncationControl:
    if not 0 < spectral_cutoff < 1:
        raise ValueError("spectral cutoff must lie in (0,1)")
    left_partitions, left_branches = _pair_carrier_branches(
        n,
        transposition_count,
        left_pair_indices,
    )
    right_partitions, right_branches = _pair_carrier_branches(
        n,
        transposition_count,
        right_pair_indices,
    )
    left = _select_carrier_branch(left_branches, left_carrier_partition)
    right = _select_carrier_branch(right_branches, right_carrier_partition)
    states = tuple(
        np.kron(left_state, right_state)
        for left_state, right_state in zip(
            left.states,
            right.states,
            strict=True,
        )
    )
    hidden_count = len(states)
    pgm = _pgm_data(states)
    left_rank = int(round(float(np.trace(left.pgm.support_projector).real)))
    right_rank = int(round(float(np.trace(right.pgm.support_projector).real)))
    dimension = left_rank * right_rank
    product_support = np.kron(
        left.pgm.support_projector,
        right.pgm.support_projector,
    )
    metric = dimension * pgm.average
    metric = (metric + metric.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(metric)
    retained = eigenvalues >= spectral_cutoff
    retained_vectors = eigenvectors[:, retained]
    retained_projector = retained_vectors @ retained_vectors.conj().T
    discarded_projector = product_support - retained_projector
    discarded_projector = (discarded_projector + discarded_projector.conj().T) / 2
    discarded_mass = float(np.trace(discarded_projector @ pgm.average).real)
    retained_rank = int(np.count_nonzero(retained))
    discarded_dimension = dimension - retained_rank
    discarded_positive = int(
        np.count_nonzero(
            (eigenvalues > 100 * tolerance) & (eigenvalues < spectral_cutoff)
        )
    )
    dimension_bound = spectral_cutoff * discarded_dimension / dimension

    ideal_success = float(np.trace(pgm.channel).real / hidden_count)
    truncated_effects = tuple(
        retained_projector @ effect @ retained_projector
        for effect in pgm.effects
    )
    truncated_success = sum(
        float(np.trace(effect @ state).real)
        for effect, state in zip(truncated_effects, states, strict=True)
    ) / hidden_count
    gentle_lower = ideal_success - 2.0 * math.sqrt(max(discarded_mass, 0.0))

    retained_values = eigenvalues[retained]
    inverse = (
        retained_vectors
        @ np.diag(1.0 / np.sqrt(retained_values))
        @ retained_vectors.conj().T
    )
    inverse_effects = tuple(
        inverse @ (dimension * state / hidden_count) @ inverse
        for state in states
    )
    inverse_effect_residual = max(
        float(np.linalg.norm(observed - expected, ord=2))
        for observed, expected in zip(
            inverse_effects,
            truncated_effects,
            strict=True,
        )
    )
    effect_sum = sum(truncated_effects)
    completeness = float(
        np.linalg.norm(effect_sum - retained_projector, ord=2)
    )
    violation = max(
        0.0,
        float(np.linalg.eigvalsh(effect_sum - product_support)[-1]),
    )
    trace_residual = abs(float(np.trace(metric).real) - dimension)
    verified = (
        trace_residual <= 1000 * tolerance
        and discarded_mass >= -100 * tolerance
        and discarded_mass <= dimension_bound + 1000 * tolerance
        and dimension_bound <= spectral_cutoff + 100 * tolerance
        and truncated_success + 1000 * tolerance >= gentle_lower
        and inverse_effect_residual <= 1000 * tolerance
        and completeness <= 1000 * tolerance
        and violation <= 1000 * tolerance
    )
    return DimensionlessTruncationControl(
        control_id=(
            f"S{n}-L{'-'.join(map(str, left_carrier_partition))}-"
            f"R{'-'.join(map(str, right_carrier_partition))}-"
            f"EPS-{spectral_cutoff:g}"
        ),
        n=n,
        transposition_count=transposition_count,
        left_source_partitions=left_partitions,
        right_source_partitions=right_partitions,
        left_carrier_partition=left_carrier_partition,
        right_carrier_partition=right_carrier_partition,
        hidden_involution_count=hidden_count,
        product_support_dimension=dimension,
        dimensionless_metric_trace=float(np.trace(metric).real),
        dimensionless_metric_trace_residual=trace_residual,
        spectral_cutoff=spectral_cutoff,
        retained_metric_rank=retained_rank,
        discarded_support_dimension=discarded_dimension,
        discarded_positive_eigenvalue_count=discarded_positive,
        discarded_average_state_mass=discarded_mass,
        discarded_mass_dimension_bound=dimension_bound,
        universal_discarded_mass_bound=spectral_cutoff,
        ideal_pgm_success=ideal_success,
        truncated_pgm_success=truncated_success,
        gentle_success_lower_bound=gentle_lower,
        observed_success_loss=ideal_success - truncated_success,
        maximum_truncated_inverse_effect_residual=inverse_effect_residual,
        truncated_effect_completeness_residual=completeness,
        truncated_effect_subpovm_eigenvalue_violation=violation,
        minimum_retained_metric_eigenvalue=float(retained_values[0]),
        maximum_metric_eigenvalue=float(retained_values[-1]),
        retained_metric_condition_number=float(
            retained_values[-1] / retained_values[0]
        ),
        nontrivial_positive_spectrum_truncation=discarded_positive > 0,
        exact_dimensionless_truncation_verified=verified,
        status=(
            "dimensionless-pgm-truncation-exact"
            if verified
            else "dimensionless-pgm-truncation-control-failure"
        ),
    )


def threshold_truncation_scaling_record(
    n: int,
    pair_count: int,
    *,
    threshold_slack: int = 0,
    schedule: str,
) -> ThresholdTruncationScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be an even hidden-involution degree")
    hidden_count = perfect_matching_count(n)
    copies = math.ceil(math.log2(hidden_count)) + threshold_slack
    success = disjoint_pair_threshold_success_lower_bound(
        pair_count,
        threshold_slack,
    )
    cutoff = sufficient_dimensionless_cutoff(success)
    legal = 2 * pair_count <= copies
    if schedule == "fixed-two-pair":
        inverse_polynomial = pair_count == 2
    elif schedule == "logarithmic-pair-depth":
        inverse_polynomial = (
            pair_count == math.ceil(math.log2(n))
            and success + 1e-15 >= logarithmic_pair_success_polynomial_lower_bound(n)
            and cutoff + 1e-15 >= logarithmic_pair_cutoff_polynomial_lower_bound(n)
        )
    else:
        raise ValueError("unknown pair-depth schedule")
    return ThresholdTruncationScalingRecord(
        schedule=schedule,
        n=n,
        hidden_involution_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        disjoint_pair_count=pair_count,
        threshold_slack=threshold_slack,
        pgm_success_lower_bound=success,
        sufficient_dimensionless_cutoff=cutoff,
        retained_success_lower_bound=success / 2.0,
        inverse_square_root_amplification_upper_bound=1.0 / math.sqrt(cutoff),
        conservative_condition_scale_upper_bound=1.0 / cutoff,
        pair_budget_legal=legal,
        cutoff_inverse_polynomial_proved=inverse_polynomial,
        minimum_positive_eigenvalue_required=False,
        full_threshold_metric_block_encoding_compiled=False,
        status=(
            "controlled-cutoff-polynomial-full-frame-access-open"
            if legal and inverse_polynomial
            else "threshold-truncation-schedule-invalid"
        ),
    )


def run_dimensionless_pgm_truncation_bridge(
) -> DimensionlessPgmTruncationBridgeReport:
    controls = [
        audit_dimensionless_branch_truncation(
            5,
            2,
            (1, 1),
            (1, 1),
            (4, 1),
            (4, 1),
            spectral_cutoff=0.5,
        ),
        audit_dimensionless_branch_truncation(
            5,
            2,
            (1, 1),
            (1, 1),
            (3, 2),
            (3, 2),
            spectral_cutoff=0.9,
        ),
    ]
    scaling = []
    for n in (8, 16, 32, 64, 128, 256):
        scaling.append(
            threshold_truncation_scaling_record(
                n,
                2,
                schedule="fixed-two-pair",
            )
        )
        scaling.append(
            threshold_truncation_scaling_record(
                n,
                math.ceil(math.log2(n)),
                schedule="logarithmic-pair-depth",
            )
        )
    finite_verified = all(
        control.exact_dimensionless_truncation_verified for control in controls
    )
    scaling_verified = all(
        record.pair_budget_legal
        and record.cutoff_inverse_polynomial_proved
        and not record.minimum_positive_eigenvalue_required
        for record in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = DimensionlessPgmTruncationTheorem(
        rank_scaled_metric=(
            "For any branch ensemble on D-dimensional support, G=D B has trace D."
        ),
        low_spectral_mass=(
            "The B-mass on eigenvalues of G below epsilon is at most epsilon."
        ),
        legal_truncated_pgm=(
            "P_epsilon E_h P_epsilon are positive, sum to P_epsilon, and the "
            "complement is an explicit failure effect."
        ),
        gentle_success_retention=(
            "Average PGM success decreases by at most 2 sqrt(epsilon), for mixed "
            "states and without a minimum positive eigenvalue assumption."
        ),
        certificate_cutoff=(
            "A PGM lower bound c permits epsilon=c^2/16 and retained success c/2."
        ),
        fixed_pair_depth_consequence=(
            "The all-n disjoint-pair threshold certificate makes c and epsilon "
            "constant for every fixed pair depth q."
        ),
        logarithmic_pair_depth_consequence=(
            "For q=ceil(log2 n), c>=1/(20 n^4) and epsilon>=1/(6400 n^8)."
        ),
        qsvt_consequence=(
            "Conditional on a poly-normalized full-metric block encoding, inverse "
            "square root only needs approximation above an inverse-polynomial cutoff."
        ),
        scope=(
            "The available covariance LCU covers two pair blocks, not the residual "
            "information-threshold copies or higher cumulants. No full-frame access, "
            "PGM output isometry, decoder, or classical separation is compiled."
        ),
        dimensionless_low_mass_bound_proved=True,
        mixed_state_truncated_pgm_robustness_proved=True,
        certificate_adaptive_cutoff_proved=True,
        fixed_depth_constant_cutoff_proved=scaling_verified,
        logarithmic_depth_inverse_polynomial_cutoff_proved=scaling_verified,
        minimum_positive_spectral_edge_required=False,
        full_threshold_metric_block_encoding_compiled=False,
        pgm_output_isometry_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=verified,
        status="minimum-spectral-edge-removed-full-threshold-frame-access-open",
    )
    metrics: dict[str, int | float] = {
        "dimensionless_low_spectral_mass_theorem_count": 1,
        "mixed_state_truncated_pgm_robustness_theorem_count": 1,
        "certificate_adaptive_cutoff_theorem_count": 1,
        "fixed_pair_depth_constant_cutoff_theorem_count": int(scaling_verified),
        "logarithmic_pair_depth_inverse_polynomial_cutoff_theorem_count": int(
            scaling_verified
        ),
        "minimum_positive_spectral_edge_requirement_count": 0,
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not control.exact_dimensionless_truncation_verified
            for control in controls
        ),
        "nontrivial_positive_spectrum_truncation_control_count": sum(
            control.nontrivial_positive_spectrum_truncation
            for control in controls
        ),
        "maximum_finite_discarded_mass_to_cutoff_ratio": max(
            control.discarded_average_state_mass / control.spectral_cutoff
            for control in controls
        ),
        "maximum_finite_truncated_inverse_effect_residual": max(
            control.maximum_truncated_inverse_effect_residual
            for control in controls
        ),
        "full_threshold_metric_block_encoding_compiler_count": 0,
        "pgm_output_isometry_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DimensionlessPgmTruncationBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "An equiprobable carrier-conditioned mixed-state ensemble, its "
                "D-dimensional support, and a proved ideal-PGM success lower bound c."
            ),
            "metric": "G=D times the average branch state.",
            "measurement": (
                "The ideal PGM compressed to the spectral subspace G>=c^2/16, "
                "plus an explicit failure effect."
            ),
            "output": "At least c/2 average correct probability.",
            "implementation_dependency": (
                "A poly-normalized block encoding of the full threshold metric and "
                "a coherent hypothesis-output isometry."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_actual_minimum_positive_metric_eigenvalue",
                "resolved": True,
                "resolution": (
                    "Trace(G)=D bounds discarded average mass by the dimensionless cutoff; gentle truncation controls success."
                ),
            },
            {
                "obligation": "retain_disjoint_pair_threshold_success_at_polynomial_cutoff",
                "resolved": True,
                "resolution": (
                    "The existing all-n success certificate gives constant cutoff for fixed q and at worst inverse-polynomial cutoff for q=ceil(log2 n)."
                ),
            },
            {
                "obligation": "compile_full_threshold_rank_scaled_metric_block_encoding",
                "resolved": False,
                "resolution": (
                    "Two-pair covariance access omits remaining singleton factors and all higher shared-label cumulants."
                ),
            },
            {
                "obligation": "compile_truncated_pgm_hypothesis_output_isometry",
                "resolved": False,
                "resolution": (
                    "The legal effects are formalized, but no polynomial Naimark circuit writes h without hypothesis enumeration."
                ),
            },
            {
                "obligation": "decode_hidden_involution_and_pass_classical_baselines",
                "resolved": False,
                "resolution": (
                    "Neither a decoded statistic nor a classical separation is supplied."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "An exponentially small positive eigenvalue forces superpolynomial inversion.",
                "survives": False,
                "response": (
                    "Eigenvalues below c^2/16 may be discarded while retaining at least c/2 success."
                ),
            },
            {
                "challenge": "The dimensionless cutoff secretly depends on support dimension.",
                "survives": False,
                "response": (
                    "Both Tr(G) and the support dimension equal D, so the factor cancels exactly."
                ),
            },
            {
                "challenge": "Two-pair covariance access already covers the threshold PGM.",
                "survives": False,
                "response": (
                    "Threshold ensembles retain unmeasured copies and, beyond two blocks, higher shared-label cumulants."
                ),
            },
            {
                "challenge": "A legal truncated sub-POVM is already a circuit and decoder.",
                "survives": False,
                "response": (
                    "The full metric block encoding and coherent hypothesis-output map remain independent compiler obligations."
                ),
            },
        ],
        primary_literature=[
            {
                "id": "watrous-gentle-measurement",
                "title": "The Theory of Quantum Information / gentle measurement lemma",
                "url": "https://cs.uwaterloo.ca/~watrous/TQI/",
            },
            {
                "id": "quek-rebentrost-pgm-polar-2021",
                "title": "Fast algorithm for quantum polar decomposition, pretty-good measurements, and the Procrustes problem",
                "url": "https://arxiv.org/abs/2106.07634",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "dimensionless_low_spectral_mass_bound_proved": True,
            "mixed_state_truncated_pgm_success_retention_proved": True,
            "minimum_positive_spectral_edge_required": False,
            "fixed_pair_depth_constant_cutoff_proved": scaling_verified,
            "logarithmic_pair_depth_inverse_polynomial_cutoff_proved": (
                scaling_verified
            ),
            "two_pair_covariance_metric_access_schema_available": True,
            "full_threshold_metric_block_encoding_compiled": False,
            "pgm_output_isometry_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Spectral truncation removes the minimum-positive-eigenvalue gate. "
                "The decisive remaining operators are a poly-normalized full "
                "threshold-metric block encoding and the hypothesis-output isometry."
            ),
        },
        status=theorem.status,
        summary=(
            "Removed the minimum positive covariance eigenvalue from the PGM "
            "compiler obligations: dimensionless truncation retains certified "
            "success at constant or inverse-polynomial cutoff. Full threshold-frame "
            "access and output decoding remain open."
        ),
        falsifiers_triggered=[
            "The actual minimum positive covariance eigenvalue is not required for certified average PGM success.",
            "Rank-scaled trace normalization removes support dimension from the low-spectral-mass bound.",
            "The two-pair covariance LCU is not a block encoding of the full information-threshold frame.",
            "A formal truncated PGM is not yet a coherent output circuit or hidden-involution decoder.",
        ],
    )


def write_dimensionless_pgm_truncation_bridge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_dimensionless_pgm_truncation_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Dimensionless PGM spectral-truncation bridge",
                status="completed-minimum-edge-removed-full-frame-access-open",
                hypothesis=(
                    "Rank-scaled trace normalization may permit robust PGM inversion "
                    "without an all-n minimum-positive-eigenvalue theorem."
                ),
                protocol=(
                    "Prove the dimensionless low-mass and gentle-truncation bounds, "
                    "compose them with the disjoint-pair success certificate, and "
                    "audit exact nontrivial finite truncations."
                ),
                positive_signal=(
                    "A poly-normalized block encoding of the full threshold metric "
                    "and a coherent truncated-PGM output isometry."
                ),
                falsifiers=[
                    "raw-frame and dimensionless cutoffs are conflated",
                    "two-pair covariance access is called full-threshold access",
                    "a legal sub-POVM is called a compiled Naimark circuit",
                    "finite conditioning is extrapolated all-n",
                    "classical separation is inferred from PGM existence",
                ],
                metrics=[
                    "dimensionless_low_spectral_mass_theorem_count",
                    "mixed_state_truncated_pgm_robustness_theorem_count",
                    "logarithmic_pair_depth_inverse_polynomial_cutoff_theorem_count",
                    "full_threshold_metric_block_encoding_compiler_count",
                    "pgm_output_isometry_compiler_count",
                ],
                dependencies=[
                    "self_dual_wreath_pgm_truncation_robustness.py",
                    "self_dual_wreath_disjoint_pair_covariance_polar_reduction.py",
                    "self_dual_wreath_carrier_branch_pgm_success_certificate.py",
                    "gentle measurement lemma",
                ],
                next_actions=[
                    "derive a recursive block encoding for the full rank-scaled threshold metric",
                    "control higher shared-label cumulants under natural branch truncation",
                    "compile the truncated-PGM hypothesis-output isometry",
                    "run classical representation-theoretic attacks on the decoded output statistic",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-DIMENSIONLESS-PGM-"
            "TRUNCATION-BRIDGE-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_dimensionless_pgm_truncation_bridge": str(
                        path
                    )
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="MINIMUM-COVARIANCE-EIGENVALUE-NOT-PGM-SUCCESS-OBLIGATION",
                source=registry_experiment_id,
                claim=(
                    "A polynomial PGM implementation must prove an inverse-polynomial "
                    "lower bound on every positive eigenvalue of the rank-scaled frame."
                ),
                reason_invalid=(
                    "Dimensionless spectral truncation below c^2/16 loses at most "
                    "c/2 success when the ideal PGM has certified success c."
                ),
                lesson=(
                    "Prioritize full-metric block encoding and output synthesis, not "
                    "the actual minimum positive spectral edge."
                ),
                applies_to=[
                    registry_candidate_id,
                    "dimensionless carrier-conditioned PGM metrics",
                    "spectrally truncated inverse square root",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="TWO-PAIR-COVARIANCE-ACCESS-NOT-THRESHOLD-FRAME-ACCESS",
                source=registry_experiment_id,
                claim=(
                    "The bounded-normalization two-pair covariance LCU already "
                    "encodes the information-threshold branch frame."
                ),
                reason_invalid=(
                    "The threshold ensemble includes residual singleton factors and "
                    "higher shared-label cumulants beyond two pair blocks."
                ),
                lesson=(
                    "Build a recursive full rank-scaled metric access theorem before "
                    "promoting truncation robustness to an end-to-end compiler."
                ),
                applies_to=[
                    registry_candidate_id,
                    "two-pair covariance polar",
                    "information-threshold PGM",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_dimensionless_pgm_truncation_bridge_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
