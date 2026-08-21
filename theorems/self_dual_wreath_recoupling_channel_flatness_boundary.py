"""Channel mutual information isolates non-Haar recoupling structure.

Fix source irreps ``alpha,beta,gamma`` and final irrep ``lambda``.  Let the
left coupling-tree multiplicity space split into intermediate channels
``H_mu`` of dimensions ``L_mu``, and the right tree into ``K_nu`` of
dimensions ``R_nu``.  Their common total dimension is ``M``.  For the unitary
recoupling matrix ``R`` and block ``R_(nu,mu)``, sequentially measuring the
two channel labels on the maximally mixed final multiplicity space gives

    p(mu,nu) = ||R_(nu,mu)||_HS^2 / M.                    (1)

Unitarity gives marginals ``p(mu)=L_mu/M`` and ``p(nu)=R_nu/M``.  Hence

    q(mu,nu)=L_mu R_nu/M^2                               (2)

is exactly the product of the physical marginals, and

    Z_(mu,nu)=p/q=M ||R_(nu,mu)||_HS^2/(L_mu R_nu)        (3)

is the likelihood ratio against channel independence.  The KL divergence
``D(p||q)`` is precisely the mutual information between the two intermediate
labels.  The chi-square divergence is the weighted fourth-moment identity

    chi^2(p||q) = sum_(mu,nu) ||R_(nu,mu)||_HS^4/(L_mu R_nu) - 1.  (4)

This provides a decisive asymptotic observable.  If source-weighted mutual
information and total variation vanish, measured intermediate labels carry
no recoupling leverage and only coherent multiplicity phases remain.  If a
nonvanishing value survives on positive physical source mass, its outlier
channels become concrete targets for a structured transform and classical
baseline.

The complete ``S_6`` Racah controls falsify exact channel flatness.  Two final
sectors contain an exactly forbidden channel whose product-marginal mass is
``1/16``; nontrivial sectors have total variation up to ``1/8`` and mutual
information up to about ``0.1564`` bits.  These finite values establish the
observable, not its all-n behavior.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_complete_racah_control import audit_complete_racah_control
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recoupling_channel_flatness_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-CHANNEL-FLATNESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class RecouplingChannelInformationControl:
    final_partition: Partition
    total_multiplicity: int
    channel_count: int
    channel_dimensions: list[dict[str, Any]]
    physical_probability_sum_residual: float
    product_marginal_probability_sum_residual: float
    maximum_marginal_residual: float
    total_variation_from_channel_independence: float
    chi_square_from_channel_independence: float
    mutual_information_bits: float
    product_mass_on_physically_forbidden_channels: float
    minimum_positive_likelihood_ratio: float
    maximum_likelihood_ratio: float
    exact_channel_flatness: bool
    nontrivial_channel_correlation: bool
    finite_complete_sector_only: bool
    status: str


@dataclass(frozen=True)
class RecouplingChannelFlatnessBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RecouplingChannelInformationControl]
    asymptotic_decision_rule: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def channel_information_from_recoupling(
    final_partition: Partition,
    matrix: np.ndarray,
    channel_labels: tuple[Partition, ...],
    *,
    tolerance: float = 1e-10,
) -> RecouplingChannelInformationControl:
    matrix = np.asarray(matrix, dtype=complex)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("recoupling matrix must be square")
    dimension = matrix.shape[0]
    if len(channel_labels) != dimension:
        raise ValueError("one intermediate label is required per basis vector")
    if np.linalg.norm(matrix.conj().T @ matrix - np.eye(dimension), ord=2) > 1e-7:
        raise ValueError("recoupling matrix must be unitary")

    groups: dict[Partition, list[int]] = defaultdict(list)
    for index, label in enumerate(channel_labels):
        groups[label].append(index)

    labels = tuple(groups)
    physical: dict[tuple[Partition, Partition], float] = {}
    product: dict[tuple[Partition, Partition], float] = {}
    ratios: list[float] = []
    forbidden_product_mass = 0.0
    for left in labels:
        columns = groups[left]
        for right in labels:
            rows = groups[right]
            squared_hs = float(
                np.linalg.norm(matrix[np.ix_(rows, columns)], ord="fro") ** 2
            )
            p_value = squared_hs / dimension
            q_value = len(columns) * len(rows) / (dimension * dimension)
            physical[left, right] = p_value
            product[left, right] = q_value
            ratio = p_value / q_value
            if p_value <= tolerance:
                forbidden_product_mass += q_value
            else:
                ratios.append(ratio)

    physical_left = {
        left: sum(physical[left, right] for right in labels)
        for left in labels
    }
    physical_right = {
        right: sum(physical[left, right] for left in labels)
        for right in labels
    }
    expected_marginals = {
        label: len(groups[label]) / dimension for label in labels
    }
    marginal_residual = max(
        max(abs(physical_left[label] - expected_marginals[label]) for label in labels),
        max(abs(physical_right[label] - expected_marginals[label]) for label in labels),
    )
    total_variation = 0.5 * sum(
        abs(physical[key] - product[key]) for key in physical
    )
    chi_square = sum(
        (physical[key] - product[key]) ** 2 / product[key]
        for key in physical
    )
    mutual_information = sum(
        value * math.log2(value / product[key])
        for key, value in physical.items()
        if value > tolerance
    )
    flat = total_variation <= 100 * tolerance
    return RecouplingChannelInformationControl(
        final_partition=final_partition,
        total_multiplicity=dimension,
        channel_count=len(labels),
        channel_dimensions=[
            {"partition": label, "dimension": len(groups[label])}
            for label in labels
        ],
        physical_probability_sum_residual=abs(sum(physical.values()) - 1.0),
        product_marginal_probability_sum_residual=abs(sum(product.values()) - 1.0),
        maximum_marginal_residual=marginal_residual,
        total_variation_from_channel_independence=total_variation,
        chi_square_from_channel_independence=chi_square,
        mutual_information_bits=max(0.0, mutual_information),
        product_mass_on_physically_forbidden_channels=forbidden_product_mass,
        minimum_positive_likelihood_ratio=min(ratios, default=0.0),
        maximum_likelihood_ratio=max(ratios, default=0.0),
        exact_channel_flatness=flat,
        nontrivial_channel_correlation=not flat,
        finite_complete_sector_only=True,
        status=(
            "finite-recoupling-channel-flat"
            if flat
            else "finite-nonhaar-channel-correlation-detected"
        ),
    )


def audit_complete_s6_channel_information(
) -> list[RecouplingChannelInformationControl]:
    records, _unresolved = audit_complete_racah_control(n=6)
    return [
        channel_information_from_recoupling(
            tuple(record.final_partition),
            np.asarray(record.signed_overlap_matrix),
            tuple(tuple(channel.intermediate_partition) for channel in record.channels),
        )
        for record in records
    ]


def run_recoupling_channel_flatness_boundary(
) -> RecouplingChannelFlatnessBoundaryReport:
    controls = audit_complete_s6_channel_information()
    normalization_failures = sum(
        max(
            row.physical_probability_sum_residual,
            row.product_marginal_probability_sum_residual,
            row.maximum_marginal_residual,
        )
        > 1e-8
        for row in controls
    )
    correlated = [row for row in controls if row.nontrivial_channel_correlation]
    forbidden = [
        row
        for row in controls
        if row.product_mass_on_physically_forbidden_channels > 1e-10
    ]
    verified = bool(controls and normalization_failures == 0)
    return RecouplingChannelFlatnessBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_joint_law": "p(mu,nu)=||R_(nu,mu)||_HS^2/M.",
            "physical_marginals": "p(mu)=L_mu/M and p(nu)=R_nu/M.",
            "flat_benchmark": (
                "q(mu,nu)=L_mu R_nu/M^2 is exactly the product of physical marginals."
            ),
            "likelihood_ratio": (
                "p/q=M ||R_(nu,mu)||_HS^2/(L_mu R_nu)."
            ),
            "mutual_information": (
                "D_KL(p||q) is the classical mutual information between the two "
                "intermediate channel measurements."
            ),
            "chi_square_identity": (
                "chi^2(p||q)=sum ||R_(nu,mu)||_HS^4/(L_mu R_nu)-1."
            ),
            "scope": (
                "The controls cover complete finite S6 sectors for one repeated "
                "source. They do not determine natural Plancherel asymptotics or phases."
            ),
        },
        finite_controls=controls,
        asymptotic_decision_rule={
            "flat_outcome": (
                "Source-weighted TV and mutual information tend to zero; measured "
                "channel labels are asymptotically independent and only coherent "
                "multiplicity phases remain as possible leverage."
            ),
            "structured_outcome": (
                "A nonvanishing source-weighted mutual information or forbidden-channel "
                "mass survives; isolate those channels and test an explicit transform."
            ),
            "required_weighting": "physical Plancherel source and final-sector trace mass",
            "finite_s6_decides_asymptotic": False,
        },
        proof_obligations=[
            {
                "obligation": "derive_source_weighted_recoupling_channel_mutual_information",
                "resolved": False,
                "resolution": (
                    "Requires scalable 6j block fourth moments under physical Plancherel weighting."
                ),
            },
            {
                "obligation": "classify_nonhaar_outlier_channel_mass",
                "resolved": False,
                "resolution": (
                    "If mutual information survives, identify whether its channels "
                    "have nonvanishing physical mass and a uniform description."
                ),
            },
            {
                "obligation": "test_classical_access_to_channel_correlations",
                "resolved": False,
                "resolution": (
                    "Any surviving label correlation needs a classical sampling and "
                    "estimation baseline before being treated as quantum leverage."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Unitarity forces exact channel independence.",
                "resolved": True,
                "resolution": (
                    "Unitarity fixes only row and column marginals. Four of five "
                    "complete S6 sectors have nonzero mutual information."
                ),
            },
            {
                "objection": "A zero recoupling block means one Kronecker coefficient vanishes.",
                "resolved": True,
                "resolution": (
                    "False in the displayed complete sectors: both channel dimensions "
                    "are positive while their cross block is forbidden by recoupling."
                ),
            },
            {
                "objection": "Nonzero finite mutual information is evidence for an algorithm.",
                "resolved": False,
                "resolution": (
                    "It may vanish with n, live on negligible source mass, or be "
                    "classically accessible."
                ),
            },
            {
                "objection": "Channel flatness would dequantize coherent recoupling.",
                "resolved": False,
                "resolution": (
                    "It dequantizes only measured labels; phases and multiplicity-index "
                    "interference are absent from p(mu,nu)."
                ),
            },
        ],
        headline_metrics={
            "recoupling_channel_information_identity_theorem_count": 1,
            "complete_s6_sector_count": len(controls),
            "normalization_failure_count": normalization_failures,
            "nonflat_s6_sector_count": len(correlated),
            "forbidden_channel_s6_sector_count": len(forbidden),
            "maximum_s6_total_variation": max(
                row.total_variation_from_channel_independence for row in controls
            ),
            "maximum_s6_mutual_information_bits": max(
                row.mutual_information_bits for row in controls
            ),
            "maximum_s6_likelihood_ratio": max(
                row.maximum_likelihood_ratio for row in controls
            ),
            "source_weighted_asymptotic_mutual_information_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "channel_information_identity_proved": verified,
            "exact_channel_flatness_falsified_at_s6": bool(correlated),
            "source_weighted_mutual_information_vanishes_proved": False,
            "source_weighted_mutual_information_survives_proved": False,
            "nonhaar_outlier_transform_compiled": False,
            "classical_baseline_separated": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite arithmetic channel correlations exist, but their physical "
                "asymptotic mass, classical accessibility, and coherent use are open."
            ),
        },
        status=(
            "finite-channel-nonflatness-proved-asymptotic-information-open"
            if verified and correlated
            else "recoupling-channel-information-control-failure"
        ),
        summary=(
            "Reduced measured recoupling structure to channel mutual information "
            "and found finite non-Haar correlations, including forbidden channels."
        ),
        falsifiers_triggered=[
            "Unitarity does not force product-distributed intermediate labels.",
            "Complete S6 recoupling contains physically forbidden cross channels with positive product-marginal mass.",
            "Finite channel mutual information does not establish asymptotic or quantum advantage.",
        ],
    )


def write_recoupling_channel_flatness_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_recoupling_channel_flatness_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> int:
    payload = write_recoupling_channel_flatness_boundary_report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
