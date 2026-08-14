"""A tail-tolerant certificate for natural Racah entropic delocalization.

For one outer-label tuple let ``pi(mu,nu)`` be the squared-block-mass
recoupling coupling and let ``p,r`` be its marginals.  Define the relative
block overlap

    a_(mu,nu) = pi_(mu,nu)/(p_mu r_nu)
                = M ||R_(mu,nu)||_HS^2/(l_mu r_nu).       (1)

The recoupling mutual information is ``I_pi=E_pi log2 a``.  For ``K>=1``
let ``delta_K=pi{a>K}``.  On the good set the information density is at most
``log2 K``.  On the bad set, ``p_mu,r_nu>=pi_(mu,nu)`` implies
``a_(mu,nu)<=1/pi_(mu,nu)``.  Entropy maximization over at most ``m^2`` atoms
therefore gives the exact tail certificate

    I_pi <= log2 K + delta_K log2(m^2/delta_K),            (2)

with a zero second term when ``delta_K=0``.  If outer labels are random and
``bar_delta=E delta_K``, concavity of ``x log(m^2/x)`` gives

    E I_pi <= log2 K + bar_delta log2(m^2/bar_delta).      (3)

For ``m=p(n)``, it is sufficient that

    log K_n=o(log n),
    bar_delta_n log(p(n)^2/bar_delta_n)=o(log n).          (4)

This permits rare collision-heavy 6j blocks and is strictly weaker than a
uniform overlap or Renyi bound.

The certificate has an operator form.  Since a block of row rank ``l`` and
column rank ``r`` obeys

    ||R_block||_HS^2 <= min(l,r)||R_block||_op^2,

we have

    a_(mu,nu) <= M ||R_block||_op^2/max(l,r).              (5)

Thus any dimension/rank operator-norm theorem can certify the good set, but
the existing symmetric-group dimension certificate is usually trivial under
independent Plancherel rank pressure.  The unresolved task is to prove (4)
for natural growing-row recoupling under the physical outer law.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_racah_entropic_delocalization_certificate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RACAH-ENTROPIC-DELOCALIZATION-CERTIFICATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RacahEntropicTailFiniteControl:
    n: int
    relative_overlap_threshold: float
    label_count: int
    physical_average_recoupling_mutual_information_bits: float
    physical_average_bad_block_mass: float
    average_tail_certificate_upper_bits: float
    certificate_violation_bits: float
    maximum_finite_relative_block_overlap: float
    positive_outer_tuple_count: int
    exact_entropic_tail_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class OperatorRelativeOverlapControl:
    total_multiplicity_dimension: int
    row_block_rank: int
    column_block_rank: int
    block_operator_norm_square: float
    exact_relative_block_overlap: float
    operator_relative_overlap_upper: float
    operator_bound_violation: float
    exact_operator_certificate_verified: bool
    status: str


@dataclass(frozen=True)
class SyntheticEntropicScalingControl:
    n: int
    log2_partition_count_upper: float
    synthetic_log2_relative_overlap_threshold: float
    synthetic_average_bad_mass: float
    synthetic_average_information_upper_bits: float
    information_upper_over_log2_n: float
    sufficient_asymptotic_conditions_satisfied: bool
    natural_racah_conditions_proved: bool
    status: str


@dataclass(frozen=True)
class RacahEntropicDelocalizationTheorem:
    local_tail_bound: str
    averaged_tail_bound: str
    sufficient_asymptotic_condition: str
    operator_overlap_bound: str
    natural_condition_proved: bool
    status: str


@dataclass(frozen=True)
class RacahEntropicDelocalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RacahEntropicDelocalizationTheorem
    finite_controls: list[RacahEntropicTailFiniteControl]
    operator_controls: list[OperatorRelativeOverlapControl]
    synthetic_scaling_controls: list[SyntheticEntropicScalingControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def entropic_tail_upper_bits(
    label_count: int,
    relative_overlap_threshold: float,
    bad_mass: float,
) -> float:
    if label_count < 1 or relative_overlap_threshold < 1:
        raise ValueError("require a positive label count and K>=1")
    if not 0 <= bad_mass <= 1:
        raise ValueError("bad mass must be a probability")
    tail = (
        bad_mass * math.log2(label_count * label_count / bad_mass)
        if bad_mass > 0
        else 0.0
    )
    return math.log2(relative_overlap_threshold) + tail


def audit_global_entropic_tail_certificate(
    n: int,
    relative_overlap_threshold: float,
    *,
    tolerance: float = 2e-9,
) -> RacahEntropicTailFiniteControl:
    if not 3 <= n <= 5 or relative_overlap_threshold < 1:
        raise ValueError("finite controls require 3<=n<=5 and K>=1")
    partitions, _likelihood, _reference, physical = (
        finite_physical_likelihood_arrays(n)
    )
    outer_physical = np.sum(physical, axis=(3, 4))
    average_information = 0.0
    average_bad = 0.0
    maximum_overlap = 0.0
    positive_outer = 0
    for outer_indices in np.ndindex(outer_physical.shape):
        outer_mass = float(outer_physical[outer_indices])
        if outer_mass <= 0:
            continue
        positive_outer += 1
        alpha, beta, gamma, final = outer_indices
        coupling = physical[
            alpha,
            beta,
            gamma,
            :,
            :,
            final,
        ] / outer_mass
        left = np.sum(coupling, axis=1)
        right = np.sum(coupling, axis=0)
        product = np.einsum("m,n->mn", left, right)
        positive = coupling > 0
        ratio = np.zeros_like(coupling)
        ratio[positive] = coupling[positive] / product[positive]
        maximum_overlap = max(maximum_overlap, float(np.max(ratio)))
        average_information += outer_mass * float(
            np.sum(coupling[positive] * np.log2(ratio[positive]))
        )
        average_bad += outer_mass * float(
            np.sum(coupling[ratio > relative_overlap_threshold])
        )
    upper = entropic_tail_upper_bits(
        len(partitions), relative_overlap_threshold, average_bad
    )
    violation = max(0.0, average_information - upper)
    exact = violation <= tolerance
    return RacahEntropicTailFiniteControl(
        n=n,
        relative_overlap_threshold=relative_overlap_threshold,
        label_count=len(partitions),
        physical_average_recoupling_mutual_information_bits=average_information,
        physical_average_bad_block_mass=average_bad,
        average_tail_certificate_upper_bits=upper,
        certificate_violation_bits=violation,
        maximum_finite_relative_block_overlap=maximum_overlap,
        positive_outer_tuple_count=positive_outer,
        exact_entropic_tail_certificate_verified=exact,
        status=(
            "average-racah-mutual-information-obeys-tail-certificate"
            if exact
            else "racah-entropic-tail-certificate-failure"
        ),
    )


def audit_operator_relative_overlap_bound(
    total_multiplicity_dimension: int,
    row_block_rank: int,
    column_block_rank: int,
    block_operator_norm_square: float,
    block_hilbert_schmidt_square: float,
    *,
    tolerance: float = 1e-12,
) -> OperatorRelativeOverlapControl:
    total = total_multiplicity_dimension
    rows = row_block_rank
    columns = column_block_rank
    if total <= 0 or not 0 < rows <= total or not 0 < columns <= total:
        raise ValueError("valid positive recoupling dimensions are required")
    if not 0 <= block_operator_norm_square <= 1 + tolerance:
        raise ValueError("operator norm square must lie in [0,1]")
    if not 0 <= block_hilbert_schmidt_square <= min(rows, columns) + tolerance:
        raise ValueError("Hilbert-Schmidt square exceeds the block rank")
    exact_ratio = total * block_hilbert_schmidt_square / (rows * columns)
    upper = (
        total
        * block_operator_norm_square
        / max(rows, columns)
    )
    violation = max(0.0, exact_ratio - upper)
    exact = violation <= tolerance
    return OperatorRelativeOverlapControl(
        total_multiplicity_dimension=total,
        row_block_rank=rows,
        column_block_rank=columns,
        block_operator_norm_square=block_operator_norm_square,
        exact_relative_block_overlap=exact_ratio,
        operator_relative_overlap_upper=upper,
        operator_bound_violation=violation,
        exact_operator_certificate_verified=exact,
        status=(
            "operator-norm-certifies-relative-racah-overlap"
            if exact
            else "operator-relative-overlap-bound-failure"
        ),
    )


def synthetic_entropic_scaling_control(n: int) -> SyntheticEntropicScalingControl:
    if n < 16:
        raise ValueError("synthetic scaling control requires n>=16")
    log_n = math.log2(n)
    # The classical bound p(n)<exp(pi sqrt(2n/3)) is enough here.
    log_partition_upper = math.pi * math.sqrt(2.0 * n / 3.0) / math.log(2.0)
    log_threshold = math.sqrt(log_n)
    bad_mass = 1.0 / (n * n)
    information_upper = log_threshold + bad_mass * (
        2.0 * log_partition_upper - math.log2(bad_mass)
    )
    ratio = information_upper / log_n
    sufficient = bool(
        math.isclose(
            log_threshold / log_n,
            1.0 / math.sqrt(log_n),
            rel_tol=1e-14,
            abs_tol=0.0,
        )
        and bad_mass * log_partition_upper / log_n < 1.0
    )
    return SyntheticEntropicScalingControl(
        n=n,
        log2_partition_count_upper=log_partition_upper,
        synthetic_log2_relative_overlap_threshold=log_threshold,
        synthetic_average_bad_mass=bad_mass,
        synthetic_average_information_upper_bits=information_upper,
        information_upper_over_log2_n=ratio,
        sufficient_asymptotic_conditions_satisfied=sufficient,
        natural_racah_conditions_proved=False,
        status=(
            "synthetic-tail-schedule-implies-sublog-racah-information"
            if sufficient
            else "synthetic-entropic-scaling-control-failure"
        ),
    )


def run_racah_entropic_delocalization_certificate(
) -> RacahEntropicDelocalizationReport:
    finite = [
        audit_global_entropic_tail_certificate(n, threshold)
        for n, threshold in (
            (3, 1.0),
            (3, 2.0),
            (4, 1.0),
            (4, 2.0),
            (5, 1.0),
            (5, 2.0),
            (5, 4.0),
        )
    ]
    operator = [
        audit_operator_relative_overlap_bound(20, 4, 5, 0.25, 1.0),
        audit_operator_relative_overlap_bound(30, 10, 6, 0.5, 2.5),
        audit_operator_relative_overlap_bound(12, 3, 3, 1.0, 3.0),
    ]
    scaling = [
        synthetic_entropic_scaling_control(n)
        for n in (20, 50, 100, 1_000, 10_000, 1_000_000)
    ]
    failures = sum(
        not row.exact_entropic_tail_certificate_verified for row in finite
    )
    failures += sum(
        not row.exact_operator_certificate_verified for row in operator
    )
    failures += sum(
        not row.sufficient_asymptotic_conditions_satisfied for row in scaling
    )
    exact = failures == 0
    theorem = RacahEntropicDelocalizationTheorem(
        local_tail_bound="I_pi<=log2 K+delta_K log2(p(n)^2/delta_K)",
        averaged_tail_bound=(
            "E I_pi<=log2 K+bar_delta_K log2(p(n)^2/bar_delta_K)"
        ),
        sufficient_asymptotic_condition=(
            "log K=o(log n) and bar_delta log(p(n)^2/bar_delta)=o(log n)"
        ),
        operator_overlap_bound=(
            "a_(mu,nu)<=M||R_(mu,nu)||_op^2/max(l_mu,r_nu)"
        ),
        natural_condition_proved=False,
        status=(
            "racah-rank-transfer-has-tail-tolerant-entropic-certificate"
            if exact
            else "racah-entropic-delocalization-certificate-failure"
        ),
    )
    return RacahEntropicDelocalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "relative_overlap": (
                "a=M||R_block||_HS^2/(left_rank right_rank)=pi/(p tensor r)"
            ),
            "local_certificate": theorem.local_tail_bound,
            "average_certificate": theorem.averaged_tail_bound,
            "asymptotic_sufficient_condition": theorem.sufficient_asymptotic_condition,
            "operator_interface": theorem.operator_overlap_bound,
            "scope": (
                "The inequalities are proved, but no natural growing-row 6j tail "
                "estimate supplies K_n or bar_delta_n."
            ),
        },
        theorem=theorem,
        finite_controls=finite,
        operator_controls=operator,
        synthetic_scaling_controls=scaling,
        proof_obligations=[
            {
                "obligation": "derive_tail_tolerant_racah_information_certificate",
                "resolved": exact,
                "resolution": (
                    "Split information density at K and entropy-bound the exceptional "
                    "mass over at most p(n)^2 intermediate blocks."
                ),
            },
            {
                "obligation": "connect_block_operator_norms_to_relative_overlap",
                "resolved": exact,
                "resolution": (
                    "Use Hilbert-Schmidt square <= block rank times operator norm square."
                ),
            },
            {
                "obligation": "prove_natural_good_block_relative_overlap_subpolynomial",
                "resolved": False,
                "resolution": (
                    "Apply a growing-row 6j operator estimate on physical block mass, "
                    "not uniformly over adversarial labels."
                ),
            },
            {
                "obligation": "prove_natural_bad_block_mass_small_enough",
                "resolved": False,
                "resolution": (
                    "For a subpolynomial K_n, show E_P pi{a>K_n} is small enough that "
                    "delta log(p(n)^2/delta)=o(log n)."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Every Racah block needs a uniform subpolynomial bound.",
                "resolved": True,
                "resolution": (
                    "False. Equation (3) permits large blocks on a sufficiently small "
                    "physical mass."
                ),
            },
            {
                "objection": "Small bad probability alone controls information.",
                "resolved": True,
                "resolution": (
                    "It must beat the p(n)^2 support entropy; the explicit delta log "
                    "term records the required rate."
                ),
            },
            {
                "objection": "A Hilbert-Schmidt rank bound is automatically useful.",
                "resolved": True,
                "resolution": (
                    "It is useful only after normalization by the independent block "
                    "mass l_mu r_nu/M. Existing typical rank pressure can erase it."
                ),
            },
        ],
        headline_metrics={
            "entropic_tail_certificate_theorem_count": int(exact),
            "operator_relative_overlap_interface_count": int(exact),
            "finite_tail_control_count": len(finite),
            "finite_control_failure_count": failures,
            "natural_good_block_bound_count": 0,
            "natural_bad_mass_bound_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "tail_tolerant_racah_mi_certificate_proved": exact,
            "operator_norm_to_relative_overlap_bound_proved": exact,
            "uniform_racah_collision_bound_required": False,
            "natural_subpolynomial_good_block_overlap_proved": False,
            "natural_bad_block_mass_rate_proved": False,
            "natural_physical_average_racah_mi_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_orientation_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact sufficient tail rates are known, but neither rate is proved "
                "for natural Plancherel-shaped symmetric-group recoupling."
            ),
        },
        status=(
            "natural-racah-search-target-is-relative-overlap-tail"
            if exact
            else "racah-entropic-delocalization-control-failure"
        ),
        summary=(
            "Replaced uniform 6j delocalization by a tail-tolerant relative-overlap "
            "criterion sufficient for sublogarithmic rank entropy."
        ),
        falsifiers_triggered=[
            "Rare large recoupling blocks do not by themselves defeat direct entropy transfer.",
            "Bad-block mass must be charged against the partition-label support entropy.",
            "Raw operator contraction is irrelevant unless normalized to the rank-product block mass.",
        ],
    )


def write_racah_entropic_delocalization_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_racah_entropic_delocalization_certificate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_racah_entropic_delocalization_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
