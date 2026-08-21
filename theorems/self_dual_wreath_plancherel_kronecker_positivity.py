"""Independent-Plancherel Kronecker coefficients are positive a.a.s.

Let ``lambda,mu,nu`` be independent Plancherel-random irreducible
representations of ``S_n``.  Put ``G=S_n``, ``g=|G|``, and

    X = sum_(s != 1) r_lambda(s) r_mu(s) r_nu(s),
    r_lambda(s)=chi_lambda(s)/d_lambda.

The character formula for the ordinary Kronecker coefficient is

    g(lambda,mu,nu)/(d_lambda d_mu d_nu) = (1+X)/g.       (1)

Plancherel first moments give ``E r_lambda(s)=0`` off the identity.  Character
column orthogonality gives, for conjugate ``s,t``,

    E[r_lambda(s)r_lambda(t)] = |C_G(s)|/|G| = 1/|Cl(s)|,

and zero otherwise.  Independence of the three partitions therefore yields
the exact variance identity

    E X^2 = sum_(nonidentity conjugacy classes C) 1/|C|.  (2)

Since Kronecker coefficients are nonnegative, (1) implies

    Pr[g(lambda,mu,nu)=0] <= Pr[|X|>=1] <= E X^2.         (3)

The right side tends to zero for ``S_n``.  Write a nonidentity cycle type as
``1^(n-k) union rho``, where ``rho`` is a fixed-point-free partition of its
support ``k``.  If

    T_k = sum_(rho fixed-point-free) z_rho/k!,

then the sum in (2) is exactly

    sum_(k=2)^n T_k/binom(n,k).                            (4)

The ``k=2`` term is ``1/binom(n,2)``.  For a fixed-point-free type, the number
of cycles is at most ``k/2`` and

    z_rho=product_i i^m_i m_i! <= k^(k/2).

There are at most ``2^k`` partitions and ``k! >= (k/e)^k``, so

    T_k <= (2e/sqrt(k))^k.                                (5)

Choose ``L=floor(log_2(n)/4)``.  The terms ``3<=k<=L`` are at most
``L 2^L/binom(n,3)=o(1)``; once ``L`` exceeds a constant, (5) makes the tail
``k>L`` geometrically vanishing.  Equations (2)-(5) prove

    Pr[g(lambda,mu,nu)>0] = 1-o(1).                       (6)

This resolves the repository's Hamming-three common-support question for the
natural independent Plancherel source law.  Conditioning all ``2K`` source
labels distinct preserves any fixed triple's conclusion because
``P_cf(n,K)=1-o(1)``.  It does not prove Sellke's stronger arbitrarily coupled
Plancherel statement, the uniformly random partition version, multiplicity
concentration, or a spectral edge for the full orientation frame.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_kronecker_positivity.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELLKE_COVERING_URL = "https://arxiv.org/abs/2004.05283"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class KroneckerPositivityControl:
    n: int
    partition_count: int
    partition_triple_count: int
    exact_zero_probability: str
    exact_normalized_remainder_mean: str
    exact_normalized_remainder_second_moment: str
    exact_reciprocal_nonidentity_class_sum: str
    zero_probability_upper_bound_residual: str
    exact_variance_identity_verified: bool
    zero_probability_bound_verified: bool
    status: str


@dataclass(frozen=True)
class ReciprocalClassScalingRecord:
    n: int
    conjugacy_class_count: int
    reciprocal_nonidentity_class_sum: float
    reciprocal_nonidentity_class_sum_log2: float
    n_squared_scaled_sum: float
    transposition_term: float
    transposition_fraction_of_sum: float
    independent_plancherel_zero_probability_upper_bound: float
    asymptotic_bound_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelKroneckerPositivityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[KroneckerPositivityControl]
    scaling_records: list[ReciprocalClassScalingRecord]
    asymptotic_proof: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def centralizer_order(cycle_type: Partition) -> int:
    counts = Counter(cycle_type)
    return math.prod(
        length**multiplicity * math.factorial(multiplicity)
        for length, multiplicity in counts.items()
    )


def reciprocal_nonidentity_class_sum(n: int) -> Fraction:
    if n < 2:
        return Fraction()
    order = math.factorial(n)
    identity = (1,) * n
    return sum(
        (
            Fraction(centralizer_order(cycle_type), order)
            for cycle_type in integer_partitions(n)
            if cycle_type != identity
        ),
        start=Fraction(),
    )


def kronecker_multiplicity(
    left: Partition,
    right: Partition,
    target: Partition,
) -> int:
    n = sum(left)
    if sum(right) != n or sum(target) != n:
        raise ValueError("all partitions must have the same size")
    return dict(tensor_product_multiplicities((left, right), n)).get(target, 0)


def normalized_kronecker_remainder(
    left: Partition,
    right: Partition,
    target: Partition,
) -> Fraction:
    n = sum(left)
    multiplicity = kronecker_multiplicity(left, right, target)
    dimensions = tuple(
        hook_length_dimension(partition)
        for partition in (left, right, target)
    )
    return Fraction(
        math.factorial(n) * multiplicity,
        math.prod(dimensions),
    ) - 1


def audit_kronecker_positivity(n: int) -> KroneckerPositivityControl:
    if not 3 <= n <= 8:
        raise ValueError("exact triple controls are restricted to 3<=n<=8")
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, plancherel_weights(n)))
    zero_probability = Fraction()
    mean = Fraction()
    second = Fraction()
    for left, right, target in itertools.product(partitions, repeat=3):
        probability = weights[left] * weights[right] * weights[target]
        multiplicity = kronecker_multiplicity(left, right, target)
        remainder = normalized_kronecker_remainder(left, right, target)
        zero_probability += probability * (multiplicity == 0)
        mean += probability * remainder
        second += probability * remainder * remainder
    class_sum = reciprocal_nonidentity_class_sum(n)
    residual = class_sum - zero_probability
    variance_verified = mean == 0 and second == class_sum
    bound_verified = residual >= 0
    return KroneckerPositivityControl(
        n=n,
        partition_count=len(partitions),
        partition_triple_count=len(partitions) ** 3,
        exact_zero_probability=str(zero_probability),
        exact_normalized_remainder_mean=str(mean),
        exact_normalized_remainder_second_moment=str(second),
        exact_reciprocal_nonidentity_class_sum=str(class_sum),
        zero_probability_upper_bound_residual=str(residual),
        exact_variance_identity_verified=variance_verified,
        zero_probability_bound_verified=bound_verified,
        status=(
            "exact-plancherel-kronecker-variance-and-positivity-bound-verified"
            if variance_verified and bound_verified
            else "plancherel-kronecker-control-failure"
        ),
    )


def reciprocal_class_scaling_record(n: int) -> ReciprocalClassScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    value = float(reciprocal_nonidentity_class_sum(n))
    transposition = 1 / math.comb(n, 2)
    return ReciprocalClassScalingRecord(
        n=n,
        conjugacy_class_count=len(integer_partitions(n)),
        reciprocal_nonidentity_class_sum=value,
        reciprocal_nonidentity_class_sum_log2=math.log2(value),
        n_squared_scaled_sum=n * n * value,
        transposition_term=transposition,
        transposition_fraction_of_sum=transposition / value,
        independent_plancherel_zero_probability_upper_bound=value,
        asymptotic_bound_proved=True,
        status="reciprocal-class-variance-bound-vanishing",
    )


def run_plancherel_kronecker_positivity() -> PlancherelKroneckerPositivityReport:
    controls = [audit_kronecker_positivity(n) for n in range(3, 9)]
    scaling = [
        reciprocal_class_scaling_record(n) for n in (10, 20, 30, 40, 50)
    ]
    failures = sum(
        not row.exact_variance_identity_verified
        or not row.zero_probability_bound_verified
        for row in controls
    )
    verified = failures == 0
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "exact_plancherel_kronecker_variance_theorem_count": 1,
        "independent_plancherel_typical_positivity_theorem_count": 1,
        "hamming_three_common_support_corollary_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_exact_control_n": max(row.n for row in controls),
        "tail_scaling_n": tail.n,
        "tail_zero_probability_upper_bound": (
            tail.independent_plancherel_zero_probability_upper_bound
        ),
        "tail_n_squared_scaled_bound": tail.n_squared_scaled_sum,
        "arbitrarily_coupled_positivity_theorem_count": 0,
        "uniform_partition_positivity_theorem_count": 0,
        "natural_node_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PlancherelKroneckerPositivityReport(
        created_at=utc_now(),
        theorem_contract={
            "normalized_remainder": (
                "g(lambda,mu,nu)/(d_lambda d_mu d_nu)=(1+X)/|S_n|."
            ),
            "exact_variance": (
                "Independent Plancherel sampling and character-column "
                "orthogonality give E X^2=sum_(C!=1)1/|C|."
            ),
            "positivity": (
                "Nonnegativity plus Chebyshev gives Pr[g=0]<=sum_(C!=1)1/|C|."
            ),
            "class_sum_asymptotic": (
                "Support decomposition and z_rho<=k^(k/2) prove the reciprocal "
                "class sum tends to zero."
            ),
            "hamming_three": (
                "A fixed globally distinct natural Hamming-three pair has "
                "left/right trivial exclusive sectors with probability 1-o(1)."
            ),
            "scope": (
                "The theorem assumes independent Plancherel partitions before "
                "global-distinct conditioning; arbitrary coupling and uniform "
                "partition sampling remain open."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        asymptotic_proof={
            "support_decomposition": (
                "sum_(C!=1)1/|C|=sum_(k=2)^n T_k/binom(n,k)"
            ),
            "transposition_term": "T_2/binom(n,2)=1/binom(n,2)",
            "fixed_point_free_centralizer_bound": "z_rho<=k^(k/2)",
            "fixed_point_free_type_count_bound": "q(k)<=2^k",
            "tail_bound": "T_k<=(2e/sqrt(k))^k",
            "split_scale": "L=floor(log_2(n)/4)",
            "small_support_bound": "L 2^L/binom(n,3)=o(1)",
            "large_support_bound": "sum_(k>L)(2e/sqrt(k))^k=o(1)",
            "reciprocal_class_sum_tends_to_zero": True,
        },
        proof_obligations=[
            {
                "obligation": "derive_exact_independent_plancherel_variance",
                "resolved": verified,
                "resolution": (
                    "Column orthogonality leaves one reciprocal class-size term "
                    "per nonidentity conjugacy class."
                ),
            },
            {
                "obligation": "prove_reciprocal_symmetric_group_class_sum_vanishes",
                "resolved": True,
                "resolution": (
                    "Moved-support decomposition, an elementary centralizer "
                    "bound, and a logarithmic support split prove o(1)."
                ),
            },
            {
                "obligation": "prove_independent_plancherel_typical_ordinary_kronecker_positivity",
                "resolved": True,
                "resolution": (
                    "Pr[g=0] is bounded by the vanishing exact variance."
                ),
            },
            {
                "obligation": "extend_to_arbitrarily_coupled_or_uniform_random_partitions",
                "resolved": False,
                "resolution": (
                    "Independence and Plancherel character moments are essential "
                    "to the present proof."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The identity term in the character sum may be cancelled with nonvanishing probability.",
                "resolved": True,
                "resolution": (
                    "The normalized nonidentity remainder has variance o(1), so "
                    "the probability of reaching -1 is o(1)."
                ),
            },
            {
                "objection": "There are exp(Theta(sqrt(n))) conjugacy classes, so reciprocal sizes need not vanish.",
                "resolved": True,
                "resolution": (
                    "Moved-support classes have binomial suppression; large "
                    "supports also have superexponentially small reciprocal size."
                ),
            },
            {
                "objection": "This resolves Sellke's full typical-positivity question.",
                "resolved": False,
                "resolution": (
                    "Only independent Plancherel sampling is proved, not "
                    "arbitrary coupling or uniformly random partitions."
                ),
            },
            {
                "objection": "Typical Kronecker positivity proves the orientation-frame edge.",
                "resolved": False,
                "resolution": (
                    "It controls support of Hamming-three intersections, not "
                    "their coherent incidence or the full projector sum."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Sellke, Covering Irrep(S_n) With Tensor Products and Powers",
                "url": SELLKE_COVERING_URL,
                "directly_proves_this_result": False,
                "reason": (
                    "It identifies typical ordinary Kronecker positivity as an "
                    "open stronger arbitrary-coupling boundary; the present "
                    "proof resolves the independent Plancherel case only."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_independent_plancherel_variance_identity_proved": verified,
            "independent_plancherel_ordinary_kronecker_positive_aas_proved": True,
            "global_distinct_fixed_triple_transfer_valid": True,
            "natural_hamming_three_common_support_aas_proved": True,
            "arbitrarily_coupled_plancherel_positivity_proved": False,
            "uniform_partition_positivity_proved": False,
            "hamming_three_incidence_rank_or_edge_controlled": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Independent natural Hamming-three support is resolved, but "
                "higher-order incidence and the complete frame spectrum are not."
            ),
        },
        status=(
            "independent-plancherel-kronecker-positivity-proved-frame-edge-open"
            if verified
            else "plancherel-kronecker-control-failure"
        ),
        summary=(
            "Proved that ordinary Kronecker coefficients of three independent "
            "Plancherel partitions are positive with probability 1-o(1)."
        ),
        falsifiers_triggered=[
            "Exponential conjugacy-class count does not prevent the reciprocal class-size variance from vanishing.",
            "The independent Plancherel theorem must not be stated for arbitrary couplings or uniform partitions.",
            "Typical Hamming-three support does not determine the natural frame edge.",
        ],
    )


def write_plancherel_kronecker_positivity_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_plancherel_kronecker_positivity())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_plancherel_kronecker_positivity_report()
    print(json.dumps(report, indent=2))
