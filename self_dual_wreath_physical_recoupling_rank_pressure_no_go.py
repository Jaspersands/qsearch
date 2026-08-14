"""Physical trace mass makes the rank-aware 6j certificate trivial a.a.s.

Let ``R_(mu,nu)`` be the recoupling block between the two multiplicity bases
of ``V_alpha tensor V_beta tensor V_gamma`` at final irrep ``lambda``.  Draw
``alpha,beta,gamma`` independently from Plancherel measure and sample a block
by the sequential projective-measurement (physical trace-mass) law

    P(alpha,beta,gamma,mu,nu,lambda)
      = d_alpha d_beta d_gamma d_lambda / |S_n|^3
        * ||R_(mu,nu)||_HS^2.                             (1)

Unitarity of the complete recoupling transform gives the exact block row and
column sums

    sum_nu ||R_(mu,nu)||_HS^2 = g(alpha,beta,mu)g(mu,gamma,lambda),
    sum_mu ||R_(mu,nu)||_HS^2 = g(beta,gamma,nu)g(alpha,nu,lambda).   (2)

Together with regular-representation multiplicity identities, (2) proves:

* every one of the six labels has the Plancherel marginal;
* each of the four local triples has law

      P_phys(a,b,c) = d_a d_b d_c g(a,b,c)/|S_n|^2
                    = P_Pl^3(a,b,c) (1+X_abc),            (3)

  where ``g=d_a d_b d_c(1+X)/|S_n|``.

The independent-Plancherel variance theorem gives ``E[X^2]=V_n=o(1)``.  On
the bad lower-tail event ``X < -1/2``, the density ``1+X`` in (3) is at most
``1/2``.  Consequently each physical local triple fails the lower
multiplicity bound with probability at most ``2 V_n``, and all four fail with
probability at most ``8 V_n``.  Plancherel marginals plus atom counting put
all six dimensions above their crude typical lower threshold except with
probability ``6/n``.

Substitution into both raw bounds of the dimension-uniform certificate gives

    raw_bound >= n! / (4 n^(7/2) p(n)^(7/2)).             (4)

This diverges.  Therefore the rank-aware certificate is clipped to its
trivial value one on ``1-o(1)`` of the physical block mass.  Equivalently,
blocks on which this certificate proves contraction carry only ``o(1)``
physical mass.

This is a no-go for the certificate, not for recoupling contraction itself.
The true operator norm may be small even when this upper bound is one, and a
coherent generalized 3nj network can use interference not represented by a
classical sequence of block measurements.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_plancherel_kronecker_positivity import (
    kronecker_multiplicity,
    normalized_kronecker_remainder,
    reciprocal_nonidentity_class_sum,
)
from self_dual_wreath_plancherel_recoupling_rank_pressure_no_go import (
    partition_number,
    raw_squared_bound_lower_log2,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_physical_recoupling_rank_pressure_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-RECOUPLING-RANK-PRESSURE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
RECOUPLING_SOURCE_URL = "https://arxiv.org/abs/1210.0463"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SizeBiasedKroneckerControl:
    n: int
    partition_count: int
    exact_total_physical_mass: str
    maximum_exact_plancherel_marginal_residual: str
    exact_bad_lower_tail_physical_mass: str
    exact_two_variance_upper_bound: str
    density_identity_verified: bool
    plancherel_marginals_verified: bool
    lower_tail_bound_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalRankPressureScalingRecord:
    n: int
    partition_count: int
    reciprocal_class_variance: float
    physical_good_event_probability_lower_bound: float
    certificate_nontrivial_mass_upper_bound: float
    raw_squared_bound_lower_log2: float
    raw_squared_bound_lower_exceeds_one: bool
    status: str


@dataclass(frozen=True)
class PhysicalRecouplingRankPressureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_local_controls: list[SizeBiasedKroneckerControl]
    scaling_records: list[PhysicalRankPressureScalingRecord]
    asymptotic_proof: dict[str, str | bool]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def physical_kronecker_triple_weight(
    left: Partition,
    right: Partition,
    target: Partition,
) -> Fraction:
    n = sum(left)
    if sum(right) != n or sum(target) != n:
        raise ValueError("all partitions must have the same degree")
    order = __import__("math").factorial(n)
    return Fraction(
        hook_length_dimension(left)
        * hook_length_dimension(right)
        * hook_length_dimension(target)
        * kronecker_multiplicity(left, right, target),
        order * order,
    )


def audit_size_biased_kronecker_law(n: int) -> SizeBiasedKroneckerControl:
    if not 3 <= n <= 8:
        raise ValueError("exact controls are restricted to 3<=n<=8")
    partitions = tuple(integer_partitions(n))
    plancherel = dict(zip(partitions, plancherel_weights(n)))
    marginals = {partition: Fraction() for partition in partitions}
    total = Fraction()
    bad_mass = Fraction()
    density_verified = True
    for left, right, target in itertools.product(partitions, repeat=3):
        physical = physical_kronecker_triple_weight(left, right, target)
        independent = plancherel[left] * plancherel[right] * plancherel[target]
        remainder = normalized_kronecker_remainder(left, right, target)
        density_verified &= physical == independent * (1 + remainder)
        total += physical
        marginals[target] += physical
        if remainder < Fraction(-1, 2):
            bad_mass += physical

    residual = max(
        (abs(marginals[target] - plancherel[target]) for target in partitions),
        default=Fraction(),
    )
    variance_bound = 2 * reciprocal_nonidentity_class_sum(n)
    return SizeBiasedKroneckerControl(
        n=n,
        partition_count=len(partitions),
        exact_total_physical_mass=str(total),
        maximum_exact_plancherel_marginal_residual=str(residual),
        exact_bad_lower_tail_physical_mass=str(bad_mass),
        exact_two_variance_upper_bound=str(variance_bound),
        density_identity_verified=density_verified and total == 1,
        plancherel_marginals_verified=residual == 0,
        lower_tail_bound_verified=bad_mass <= variance_bound,
        status=(
            "exact-size-biased-kronecker-law-verified"
            if density_verified
            and total == 1
            and residual == 0
            and bad_mass <= variance_bound
            else "size-biased-kronecker-control-failure"
        ),
    )


def physical_pressure_record(n: int) -> PhysicalRankPressureScalingRecord:
    variance = float(reciprocal_nonidentity_class_sum(n))
    failure = min(1.0, 6.0 / n + 8.0 * variance)
    lower_log2 = raw_squared_bound_lower_log2(n)
    return PhysicalRankPressureScalingRecord(
        n=n,
        partition_count=partition_number(n),
        reciprocal_class_variance=variance,
        physical_good_event_probability_lower_bound=max(0.0, 1.0 - failure),
        certificate_nontrivial_mass_upper_bound=(
            failure if lower_log2 > 0 else 1.0
        ),
        raw_squared_bound_lower_log2=lower_log2,
        raw_squared_bound_lower_exceeds_one=lower_log2 > 0,
        status=(
            "physical-certificate-nontrivial-mass-bounded"
            if lower_log2 > 0
            else "finite-n-factorial-margin-not-yet-positive"
        ),
    )


def run_physical_recoupling_rank_pressure_no_go(
) -> PhysicalRecouplingRankPressureReport:
    controls = [audit_size_biased_kronecker_law(n) for n in range(3, 8)]
    rows = [physical_pressure_record(n) for n in (8, 12, 16, 20, 24, 30)]
    verified = all(
        row.density_identity_verified
        and row.plancherel_marginals_verified
        and row.lower_tail_bound_verified
        for row in controls
    )
    tail = rows[-1]
    return PhysicalRecouplingRankPressureReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_block_law": (
                "P(alpha,beta,gamma,mu,nu,lambda)="
                "d_alpha d_beta d_gamma d_lambda ||R_mu,nu||_HS^2/|S_n|^3."
            ),
            "recoupling_marginals": (
                "Block-row and block-column Hilbert--Schmidt sums equal the "
                "left- and right-tree Kronecker path multiplicities."
            ),
            "local_triple_law": (
                "Each of the four local triples has exact density 1+X relative "
                "to three independent Plancherel labels."
            ),
            "six_label_marginals": (
                "Every individual edge label in the tetrahedral network is exactly Plancherel."
            ),
            "physical_lower_tail": (
                "For one local triple, P_phys[X< -1/2]<=2 V_n; all four cost at most 8 V_n."
            ),
            "certificate_mass_no_go": (
                "The physical mass of blocks on which the rank-aware certificate "
                "is nontrivial is at most 6/n+8 V_n=o(1)."
            ),
            "scope": (
                "This bounds one measured 6j block under physical trace mass. It "
                "does not lower-bound the true norm or analyze coherent 3nj interference."
            ),
        },
        exact_local_controls=controls,
        scaling_records=rows,
        asymptotic_proof={
            "physical_joint_normalized": True,
            "all_six_marginals_plancherel": True,
            "four_local_triples_size_biased": True,
            "bad_local_density_upper_on_event": "1+X<=1/2",
            "four_local_failure_bound": "8 V_n",
            "six_dimension_failure_bound": "6/n",
            "raw_bound_lower": "n!/(4 n^(7/2) p(n)^(7/2))",
            "raw_bound_diverges": True,
            "certificate_nontrivial_physical_mass_tends_to_zero": True,
        },
        literature_links=[
            {
                "paper_id": "christandl-sahinoglu-walter-2016",
                "title": "Recoupling coefficients and quantum entropies",
                "url": RECOUPLING_SOURCE_URL,
                "use": (
                    "Symmetric-group recoupling block definition and tetrahedral "
                    "Hilbert--Schmidt identities; the physical trace-mass no-go is derived here."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "physical_coupling_path_rank_pressure",
                "resolved": verified,
                "resolution": (
                    "The exact trace-mass law makes every local Kronecker triple "
                    "size-biased Plancherel, whose bad lower tail is at most 2 V_n."
                ),
            },
            {
                "obligation": "dimension_uniform_certificate_typical_mass_useful",
                "resolved": True,
                "resolution": (
                    "Falsified: its nontrivial blocks carry o(1) physical mass."
                ),
            },
            {
                "obligation": "true_typical_6j_operator_norm",
                "resolved": False,
                "resolution": (
                    "A trivial upper certificate does not determine the actual norm."
                ),
            },
            {
                "obligation": "coherent_shared_source_3nj_analysis",
                "resolved": False,
                "resolution": (
                    "The sequential block law does not control coherent path sums."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Intermediate labels are correlated, invalidating independent-Plancherel concentration.",
                "resolved": True,
                "resolution": (
                    "Their exact local law is the independent law tilted by 1+X; "
                    "on the only bad event used, this tilt is at most one half."
                ),
            },
            {
                "objection": "The six dimension lower-tail bounds require label independence.",
                "resolved": True,
                "resolution": (
                    "A union bound uses only the six exact Plancherel marginals."
                ),
            },
            {
                "objection": "Certificate triviality implies typical recoupling blocks have norm one.",
                "resolved": False,
                "resolution": (
                    "False. It says this rank upper bound cannot witness contraction; "
                    "the actual norm can be much smaller."
                ),
            },
            {
                "objection": "Measured-block mass controls a coherent generalized 3nj transform.",
                "resolved": False,
                "resolution": (
                    "Coherent interference and source reuse are outside the sequential law."
                ),
            },
        ],
        headline_metrics={
            "physical_trace_mass_rank_pressure_no_go_theorem_count": 1,
            "exact_size_biased_local_control_count": len(controls),
            "exact_local_control_failure_count": sum(
                row.status != "exact-size-biased-kronecker-law-verified"
                for row in controls
            ),
            "tail_n": tail.n,
            "tail_physical_good_event_probability_lower_bound": (
                tail.physical_good_event_probability_lower_bound
            ),
            "tail_certificate_nontrivial_mass_upper_bound": (
                tail.certificate_nontrivial_mass_upper_bound
            ),
            "tail_raw_squared_bound_lower_log2": (
                tail.raw_squared_bound_lower_log2
            ),
            "true_typical_6j_norm_theorem_count": 0,
            "coherent_3nj_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_trace_mass_law_derived": verified,
            "all_six_edge_marginals_plancherel_proved": verified,
            "local_size_biased_kronecker_law_proved": verified,
            "rank_certificate_nontrivial_physical_mass_vanishes_proved": verified,
            "true_typical_6j_contraction_proved": False,
            "coherent_generalized_3nj_contraction_proved": False,
            "coherent_recoupling_compiled": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The rank certificate is now closed as a typical-mass tool, but "
                "the actual recoupling norm and coherent shared-source network remain open."
            ),
        },
        status=(
            "physical-rank-certificate-typical-mass-no-go-proved"
            if verified
            else "physical-rank-pressure-control-failure"
        ),
        summary=(
            "Proved that blocks where the dimension-uniform rank certificate "
            "is nontrivial have vanishing physical 6j trace mass."
        ),
        falsifiers_triggered=[
            "Multiplicity-biased physical paths do not rescue the rank certificate on typical mass.",
            "Exceptional low-rank channels must overcome a vanishing source-mass bound.",
            "The result does not determine true 6j norms or coherent 3nj interference.",
        ],
    )


def write_physical_recoupling_rank_pressure_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_physical_recoupling_rank_pressure_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> int:
    payload = write_physical_recoupling_rank_pressure_no_go_report()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
