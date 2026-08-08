"""Relative-rank bridge from scalar spectral mass to block events.

For source block ``omega`` let ``Q_omega`` be a bad spectral projection and

    r_omega = rank(Q_omega) / dim(H_omega).

If every nonzero bad projection has ``r_omega >= r_min``, then

    Pr[Q_omega != 0]
      <= E r_omega / r_min
      = tr_reg(Q) / r_min.                                 (1)

Thus a polynomial relative-rank theorem would bypass the enormous physical
carrier dimension.  If ``r_min >= |G|^-c``, an interval-uniform Chebyshev
witness need only drive scalar bad mass below ``delta |G|^-c``.  Its degree is
``O(log |G|)`` for fixed ``c``, rather than
``Theta((log |G|)^2)``.  At n=48, 25 percent slack and ``c=1``, the upper-edge
degree drops from 13,094 to 167 and the support-aware lower-edge degree drops
from 72,449 to 921.

Global diagonal covariance does not prove such a rank floor.  Every node
frame commutes with

    rho_nu(t) tensor product_j rho_(Lambda_j)(t),

so Schur decomposition has the form

    A = direct_sum_alpha I_(d_alpha) tensor M_alpha.       (2)

Equation (2) forces eigenvalue multiplicity ``d_alpha`` but leaves the
multiplicity operator ``M_alpha`` unrestricted.  Trivial and sign sectors
have ``d_alpha=1`` and can occur with large multiplicity.  The commutant of
the global action therefore contains rank-one projections in those
multiplicity spaces.  Any natural relative-rank theorem must use the specific
subgroup-projector sum, source typicality, or a center-valued local law; global
symmetry alone is categorically insufficient.

The finite collision-free S4 control satisfies (1) with
``r_min=1/18``.  This is evidence that the bridge is numerically meaningful,
not an all-n rank theorem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_collision_free_event_transfer import (
    hierarchy_event_transfer_scaling_record,
)
from self_dual_wreath_multiscale_polar_schedule import (
    MIXED_SCHEDULE_CONDITION_UPPER,
)
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_regular_master_central_support import (
    audit_collision_free_central_support_dilution,
)
from self_dual_wreath_trace_polynomial_edge_burden import (
    minimum_chebyshev_degree,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_central_support_rank_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class RelativeRankBridgeControl:
    control_id: str
    bad_block_probability: str
    scalar_bad_spectral_mass: str
    minimum_nonzero_bad_projection_relative_rank: str
    rank_bridge_probability_upper_bound: str
    bridge_slack: str
    exact_rank_bridge_inequality_verified: bool
    status: str


@dataclass(frozen=True)
class PolynomialRankBridgeScalingRecord:
    n: int
    group_order_log2: float
    selected_copy_count: int
    assumed_group_rank_exponent: int
    assumed_relative_rank_lower_bound_log2: float
    log2_required_per_node_failure: float
    relative_edge_slack: float
    upper_edge_minimum_degree: int
    lower_edge_minimum_degree: int
    upper_degree_to_copy_count_ratio: float
    lower_degree_to_copy_count_ratio: float
    degree_is_order_log_group: bool
    natural_relative_rank_bound_proved: bool
    status: str


@dataclass(frozen=True)
class GlobalCovarianceMultiplicityControl:
    n: int
    target_partition: Partition
    source_partitions: tuple[Partition, ...]
    copy_count: int
    carrier_dimension: int
    globally_distinct_source_partitions: bool
    maximum_global_diagonal_commutator_norm: float
    trivial_isotypic_multiplicity: int
    sign_isotypic_multiplicity: int
    smallest_forced_eigenvalue_multiplicity: int
    rank_one_commutant_projection_relative_rank: str
    inverse_group_order: str
    global_covariance_forces_inverse_group_relative_rank: bool
    exact_global_covariance_verified: bool
    status: str


@dataclass(frozen=True)
class CentralSupportRankBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    rank_bridge_controls: list[RelativeRankBridgeControl]
    scaling_records: list[PolynomialRankBridgeScalingRecord]
    covariance_controls: list[GlobalCovarianceMultiplicityControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def relative_rank_bridge_control(
    control_id: str,
    bad_block_probability: Fraction,
    scalar_bad_spectral_mass: Fraction,
    minimum_relative_rank: Fraction,
) -> RelativeRankBridgeControl:
    if not 0 < bad_block_probability <= 1:
        raise ValueError("bad block probability must lie in (0,1]")
    if not 0 < scalar_bad_spectral_mass <= bad_block_probability:
        raise ValueError("invalid scalar bad spectral mass")
    if not 0 < minimum_relative_rank <= 1:
        raise ValueError("relative rank must lie in (0,1]")
    upper = scalar_bad_spectral_mass / minimum_relative_rank
    slack = upper - bad_block_probability
    verified = slack >= 0
    return RelativeRankBridgeControl(
        control_id=control_id,
        bad_block_probability=str(bad_block_probability),
        scalar_bad_spectral_mass=str(scalar_bad_spectral_mass),
        minimum_nonzero_bad_projection_relative_rank=str(minimum_relative_rank),
        rank_bridge_probability_upper_bound=str(upper),
        bridge_slack=str(slack),
        exact_rank_bridge_inequality_verified=verified,
        status=(
            "exact-relative-rank-central-support-bridge-verified"
            if verified
            else "relative-rank-bridge-control-failure"
        ),
    )


def collision_free_s4_rank_bridge_control() -> RelativeRankBridgeControl:
    control = audit_collision_free_central_support_dilution()
    return relative_rank_bridge_control(
        "globally-distinct-s4-two-copy-root",
        Fraction(control.bad_block_conditional_probability),
        Fraction(control.scalar_bad_spectral_mass_conditional),
        Fraction(control.minimum_bad_projection_relative_rank),
    )


def polynomial_rank_bridge_scaling_record(
    n: int,
    group_rank_exponent: int,
    *,
    relative_edge_slack: float = 0.25,
) -> PolynomialRankBridgeScalingRecord:
    if n < 3 or group_rank_exponent < 1:
        raise ValueError("invalid n or rank exponent")
    order = math.factorial(n)
    log2_order = math.log2(order)
    copies = (order - 1).bit_length() + 2
    event = hierarchy_event_transfer_scaling_record(n)
    log2_rank = -group_rank_exponent * log2_order
    effective_log_dimension = -log2_rank
    upper_coordinate = 1.0 + 2.0 * relative_edge_slack
    lower_coordinate = 1.0 + (
        2.0
        * relative_edge_slack
        / (MIXED_SCHEDULE_CONDITION_UPPER - 1.0)
    )
    upper_degree = minimum_chebyshev_degree(
        effective_log_dimension,
        event.log2_required_per_node_failure_upper_bound,
        upper_coordinate,
    )
    lower_degree = minimum_chebyshev_degree(
        effective_log_dimension,
        event.log2_required_per_node_failure_upper_bound,
        lower_coordinate,
    )
    return PolynomialRankBridgeScalingRecord(
        n=n,
        group_order_log2=log2_order,
        selected_copy_count=copies,
        assumed_group_rank_exponent=group_rank_exponent,
        assumed_relative_rank_lower_bound_log2=log2_rank,
        log2_required_per_node_failure=(
            event.log2_required_per_node_failure_upper_bound
        ),
        relative_edge_slack=relative_edge_slack,
        upper_edge_minimum_degree=upper_degree,
        lower_edge_minimum_degree=lower_degree,
        upper_degree_to_copy_count_ratio=upper_degree / copies,
        lower_degree_to_copy_count_ratio=lower_degree / copies,
        degree_is_order_log_group=(
            upper_degree <= 20 * copies and lower_degree <= 20 * copies
        ),
        natural_relative_rank_bound_proved=False,
        status="conditional-polynomial-rank-bridge-degree-reduction",
    )


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = np.asarray([[1.0]])
    for matrix in matrices:
        output = np.kron(output, matrix)
    return output


def audit_global_covariance_multiplicity() -> GlobalCovarianceMultiplicityControl:
    n = 4
    target = (3, 1)
    sources = ((4,), (2, 2), (3, 1), (2, 1, 1))
    labels = ((sources[0], sources[1]), (sources[2], sources[3]))
    projectors = tuple(
        orientation_invariant_projector(target, labels, mask)
        for mask in range(4)
    )
    frame = sum(projectors, np.zeros_like(projectors[0]))
    factors = (target, *sources)
    rows = [dict(permutation_representation_matrices(factor)) for factor in factors]
    group = tuple(rows[0])
    commutator = max(
        float(
            np.linalg.norm(
                frame @ _kron_all(tuple(table[element] for table in rows))
                - _kron_all(tuple(table[element] for table in rows)) @ frame,
                ord=2,
            )
        )
        for element in group
    )
    multiplicities = dict(tensor_product_multiplicities(factors, n))
    trivial = multiplicities.get((n,), 0)
    sign = multiplicities.get((1,) * n, 0)
    carrier = frame.shape[0]
    rank_one_relative = Fraction(1, carrier)
    inverse_order = Fraction(1, math.factorial(n))
    verified = bool(
        len(set(sources)) == len(sources)
        and commutator <= 1e-10
        and trivial >= 2
        and sign >= 2
        and rank_one_relative < inverse_order
    )
    return GlobalCovarianceMultiplicityControl(
        n=n,
        target_partition=target,
        source_partitions=sources,
        copy_count=2,
        carrier_dimension=carrier,
        globally_distinct_source_partitions=len(set(sources)) == len(sources),
        maximum_global_diagonal_commutator_norm=commutator,
        trivial_isotypic_multiplicity=trivial,
        sign_isotypic_multiplicity=sign,
        smallest_forced_eigenvalue_multiplicity=1,
        rank_one_commutant_projection_relative_rank=str(rank_one_relative),
        inverse_group_order=str(inverse_order),
        global_covariance_forces_inverse_group_relative_rank=False,
        exact_global_covariance_verified=verified,
        status=(
            "global-covariance-verified-relative-rank-symmetry-no-go"
            if verified
            else "global-covariance-multiplicity-control-failure"
        ),
    )


def run_central_support_rank_bridge() -> CentralSupportRankBridgeReport:
    bridge_controls = [collision_free_s4_rank_bridge_control()]
    scaling = [
        polynomial_rank_bridge_scaling_record(n, exponent)
        for n in (20, 32, 48)
        for exponent in (1, 2, 4)
    ]
    covariance = [audit_global_covariance_multiplicity()]
    failures = sum(
        not row.exact_rank_bridge_inequality_verified for row in bridge_controls
    ) + sum(not row.exact_global_covariance_verified for row in covariance)
    tail = [row for row in scaling if row.n == 48 and row.assumed_group_rank_exponent == 1][0]
    metrics: dict[str, int | float] = {
        "relative_rank_central_support_bridge_theorem_count": 1,
        "polynomial_rank_degree_reduction_theorem_count": 1,
        "global_covariance_symmetry_no_go_theorem_count": 1,
        "rank_bridge_control_count": len(bridge_controls),
        "covariance_control_count": len(covariance),
        "finite_control_failure_count": failures,
        "conditional_scaling_row_count": len(scaling),
        "tail_n": tail.n,
        "tail_group_rank_exponent": tail.assumed_group_rank_exponent,
        "tail_conditional_upper_edge_degree": tail.upper_edge_minimum_degree,
        "tail_conditional_lower_edge_degree": tail.lower_edge_minimum_degree,
        "natural_polynomial_relative_rank_theorem_count": 0,
        "center_valued_local_law_theorem_count": 0,
        "natural_all_depth_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CentralSupportRankBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "relative_rank_bridge": (
                "If every nonzero bad block projection has relative rank at "
                "least r_min, bad-block probability is at most scalar bad "
                "spectral mass divided by r_min."
            ),
            "degree_reduction": (
                "A natural bound r_min>=|G|^-c for fixed c changes the "
                "interval-uniform polynomial burden from quadratic to linear "
                "in log |G|."
            ),
            "global_covariance": (
                "Every orientation node frame commutes with the global "
                "diagonal G action."
            ),
            "symmetry_boundary": (
                "Schur multiplicity spaces contain rank-one commutant "
                "projections in one-dimensional isotypic sectors, so global "
                "covariance alone proves no |G|^-c relative-rank floor."
            ),
            "scope": (
                "No relative-rank lower bound for the natural bad spectral "
                "projection is proved."
            ),
        },
        rank_bridge_controls=bridge_controls,
        scaling_records=scaling,
        covariance_controls=covariance,
        proof_obligations=[
            {
                "obligation": "derive_relative_rank_to_central_support_bridge",
                "resolved": failures == 0,
                "resolution": "Equation (1) is exact and the collision-free S4 control respects it.",
            },
            {
                "obligation": "prove_natural_bad_projection_polynomial_relative_rank",
                "resolved": False,
                "resolution": (
                    "This would reduce the required degree to O(log |G|), but "
                    "global covariance and Schur multiplicity do not imply it."
                ),
            },
            {
                "obligation": "bound_bad_central_support_without_relative_rank",
                "resolved": False,
                "resolution": "The alternative is a direct center-valued local law.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A polynomial relative-rank bound would not materially change the moment burden.",
                "resolved": True,
                "resolution": (
                    "At n=48 and exponent one, the upper/lower degrees become "
                    "167/921 instead of 13094/72449."
                ),
            },
            {
                "objection": "Global diagonal covariance supplies the needed eigenvalue multiplicity.",
                "resolved": True,
                "resolution": (
                    "False: one-dimensional isotypic sectors with multiplicity "
                    "at least two admit rank-one commutant projections."
                ),
            },
            {
                "objection": "The collision-free S4 rank floor proves the all-n bound.",
                "resolved": True,
                "resolution": "It is one finite control and is not promoted asymptotically.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "relative_rank_central_support_bridge_proved": failures == 0,
            "polynomial_relative_rank_would_reduce_degree_to_order_log_group": True,
            "global_covariance_proves_polynomial_relative_rank": False,
            "natural_bad_projection_polynomial_relative_rank_proved": False,
            "center_valued_local_law_proved": False,
            "natural_all_depth_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The high-leverage rank bridge is exact, but its natural "
                "relative-rank premise remains unproved and is not a symmetry consequence."
            ),
        },
        status=(
            "rank-bridge-proved-natural-relative-rank-or-central-law-open"
            if failures == 0
            else "central-support-rank-bridge-control-failure"
        ),
        summary=(
            "Quantified the decisive polynomial relative-rank bypass and proved "
            "that global diagonal symmetry cannot establish its premise."
        ),
        falsifiers_triggered=[
            "Global diagonal covariance does not remove the central-support problem.",
            "Finite collision-free relative-rank data is not an asymptotic rank theorem.",
            "Without polynomial bad-projection rank, scalar spectral mass still need not control bad source blocks.",
        ],
    )


def write_central_support_rank_bridge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_central_support_rank_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_central_support_rank_bridge_report()
    print(json.dumps(report, indent=2))
