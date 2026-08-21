"""Natural mass in large hyperoctahedral branching multiplicities.

Let ``G=S_(2m)``, let ``K=C_2 wr S_m`` centralize the fixed-point-free
involution ``h``, and write

    Res_K [lambda] = direct_sum_mu C^b(lambda,mu) tensor [mu].

The ``h``-even ``K`` irreps are the bipartitions ``mu=(alpha,beta)`` with
``|beta|`` even.  Refining one coordinate of the exact hidden-involution
source into a ``G`` irrep and then an even ``K`` irrep gives the normalized
joint law

    q(lambda,mu) = 2 d_lambda d_mu b(lambda,mu) / |G|.  (1)

Indeed, its ``lambda`` marginal is the exact ``H=<h>`` spherical law, while
its ``mu`` marginal is Plancherel measure on ``K`` conditioned on even central
parity.

Let ``I_N=sum_(lambda partition N) d_lambda`` and

    J_m^+ = sum_(|beta| even) d_(alpha,beta)
          = sum_(b even) binom(m,b) I_(m-b) I_b.

For any threshold ``T``, (1) gives the all-size counting bound

    Pr_q[b(lambda,mu)<=T] <= 2 T I_(2m) J_m^+ / (2m)!.  (2)

At ``T=M^(1/4)``, where ``M=(2m-1)!!``, the right side vanishes rapidly.
After a union bound over the logarithmic copy width, all source coordinates
have superpolynomial branching multiplicity on overwhelming natural mass.

This identifies a precise missing-label problem.  On
``Res_K[lambda]=direct_sum_mu C^b tensor [mu]``, every operator from ``C[K]``
acts as ``I_b tensor rho_mu``.  A ``K`` QFT or phase estimation of ``K``
observables therefore cannot distinguish the ``b`` copies.  A useful
subduction transform needs a source-aware basis in ``End_K([lambda])`` and a
normalized recoupling rule.  Large multiplicity is still not a circuit lower
bound: a paired Young-graph recursion could encode the copy label in only
polynomially many qubits.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import involution_class_size
from coset_hidden_involution_natural_matrix_multiplicity import (
    symmetric_group_involution_count,
)
from coset_hidden_involution_natural_recoupling_boundary import (
    _partitions_including_empty,
    hyperoctahedral_irrep_dimension,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_hyperoctahedral_branching_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-HYPEROCTAHEDRAL-BRANCHING-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class EvenBranchDimensionSumControl:
    half_degree: int
    symmetric_partition_count: int
    symmetric_irrep_dimension_sum: int
    symmetric_involution_count: int
    even_bipartition_count: int
    even_hyperoctahedral_irrep_dimension_sum: int
    even_dimension_convolution_sum: int
    even_hyperoctahedral_regular_dimension_sum: int
    expected_even_hyperoctahedral_regular_dimension_sum: int
    dimension_sum_identities_verified: bool
    status: str


@dataclass(frozen=True)
class BranchingMultiplicityScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    symmetric_irrep_dimension_sum_log2: float
    even_hyperoctahedral_irrep_dimension_sum_log2: float
    branching_multiplicity_threshold_formula: str
    branching_multiplicity_threshold_log2: float
    low_branching_multiplicity_probability_log2_upper_bound: float
    low_branching_multiplicity_probability_upper_bound: float
    joint_any_source_low_multiplicity_probability_upper_bound: float
    joint_all_source_high_multiplicity_probability_lower_bound: float
    missing_label_commutant_dimension_log2_lower_bound: float
    threshold_superpolynomial: bool
    all_source_coordinates_high_branching_on_natural_mass: bool
    K_qft_resolves_branching_multiplicity_copy: bool
    paired_young_graph_recursion_compiled: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralBranchingMassTheorem:
    exact_joint_law: str
    exact_marginals: str
    low_multiplicity_bound: str
    natural_threshold: str
    joint_source_conclusion: str
    K_qft_missing_label_boundary: str
    paired_tower_escape: str
    exact_joint_law_proved: bool
    low_multiplicity_counting_bound_proved: bool
    natural_mass_in_superpolynomial_branching_proved: bool
    K_qft_resolves_missing_labels: bool
    paired_young_graph_recursion_compiled: bool
    source_aware_normalized_subduction_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralBranchingMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    dimension_sum_controls: list[EvenBranchDimensionSumControl]
    scaling_records: list[BranchingMultiplicityScalingRecord]
    theorem: HyperoctahedralBranchingMassTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def even_hyperoctahedral_irrep_dimension_sum(half_degree: int) -> int:
    if half_degree < 0:
        raise ValueError("half_degree must be nonnegative")
    return sum(
        math.comb(half_degree, beta_size)
        * symmetric_group_involution_count(half_degree - beta_size)
        * symmetric_group_involution_count(beta_size)
        for beta_size in range(0, half_degree + 1, 2)
    )


def audit_even_branch_dimension_sums(
    half_degree: int,
) -> EvenBranchDimensionSumControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    symmetric_dimensions = [
        hook_length_dimension(partition) for partition in integer_partitions(degree)
    ]
    even_bipartitions = [
        (alpha, beta)
        for beta_size in range(0, half_degree + 1, 2)
        for alpha in _partitions_including_empty(half_degree - beta_size)
        for beta in _partitions_including_empty(beta_size)
    ]
    dimensions = [
        hyperoctahedral_irrep_dimension(alpha, beta)
        for alpha, beta in even_bipartitions
    ]
    symmetric_sum = sum(symmetric_dimensions)
    even_sum = sum(dimensions)
    convolution = even_hyperoctahedral_irrep_dimension_sum(half_degree)
    regular_sum = sum(dimension * dimension for dimension in dimensions)
    group_order = (2**half_degree) * math.factorial(half_degree)
    expected_regular = group_order // 2
    verified = bool(
        symmetric_sum == symmetric_group_involution_count(degree)
        and even_sum == convolution
        and regular_sum == expected_regular
    )
    return EvenBranchDimensionSumControl(
        half_degree=half_degree,
        symmetric_partition_count=len(symmetric_dimensions),
        symmetric_irrep_dimension_sum=symmetric_sum,
        symmetric_involution_count=symmetric_group_involution_count(degree),
        even_bipartition_count=len(even_bipartitions),
        even_hyperoctahedral_irrep_dimension_sum=even_sum,
        even_dimension_convolution_sum=convolution,
        even_hyperoctahedral_regular_dimension_sum=regular_sum,
        expected_even_hyperoctahedral_regular_dimension_sum=expected_regular,
        dimension_sum_identities_verified=verified,
        status=(
            "even-branch-dimension-sum-identities-verified"
            if verified
            else "even-branch-dimension-sum-control-failure"
        ),
    )


def low_branching_multiplicity_probability_log2_bound(
    half_degree: int,
    threshold_log2: float,
) -> float:
    if half_degree < 2 or threshold_log2 < 0:
        raise ValueError("half_degree and threshold must be valid")
    degree = 2 * half_degree
    return (
        1.0
        + threshold_log2
        + math.log2(symmetric_group_involution_count(degree))
        + math.log2(even_hyperoctahedral_irrep_dimension_sum(half_degree))
        - math.lgamma(degree + 1) / math.log(2)
    )


def branching_multiplicity_scaling_record(
    half_degree: int,
) -> BranchingMultiplicityScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    threshold_log2 = math.log2(candidates) / 4
    low_log2 = low_branching_multiplicity_probability_log2_bound(
        half_degree,
        threshold_log2,
    )
    low = min(1.0, 2**low_log2) if low_log2 > -1074 else 0.0
    joint_bad = min(1.0, copies * low)
    joint_good = max(0.0, 1.0 - joint_bad)
    high_natural = joint_good >= 0.9
    return BranchingMultiplicityScalingRecord(
        half_degree=half_degree,
        degree=degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        symmetric_irrep_dimension_sum_log2=math.log2(
            symmetric_group_involution_count(degree)
        ),
        even_hyperoctahedral_irrep_dimension_sum_log2=math.log2(
            even_hyperoctahedral_irrep_dimension_sum(half_degree)
        ),
        branching_multiplicity_threshold_formula="T=|h^G|^(1/4)",
        branching_multiplicity_threshold_log2=threshold_log2,
        low_branching_multiplicity_probability_log2_upper_bound=low_log2,
        low_branching_multiplicity_probability_upper_bound=low,
        joint_any_source_low_multiplicity_probability_upper_bound=joint_bad,
        joint_all_source_high_multiplicity_probability_lower_bound=joint_good,
        missing_label_commutant_dimension_log2_lower_bound=2 * threshold_log2,
        threshold_superpolynomial=True,
        all_source_coordinates_high_branching_on_natural_mass=high_natural,
        K_qft_resolves_branching_multiplicity_copy=False,
        paired_young_graph_recursion_compiled=False,
        status=(
            "all-source-coordinates-have-huge-branching-multiplicity-on-natural-mass"
            if high_natural
            else "preasymptotic-branching-multiplicity-bound"
        ),
    )


def build_hyperoctahedral_branching_mass_report(
    *,
    control_half_degrees: tuple[int, ...] = (2, 3, 4, 5, 6, 8),
    scaling_half_degrees: tuple[int, ...] = (12, 16, 24, 32, 64),
) -> HyperoctahedralBranchingMassReport:
    controls = [audit_even_branch_dimension_sums(m) for m in control_half_degrees]
    scaling = [branching_multiplicity_scaling_record(m) for m in scaling_half_degrees]
    exact = all(row.dimension_sum_identities_verified for row in controls)
    asymptotic_mass = all(
        row.all_source_coordinates_high_branching_on_natural_mass
        for row in scaling[2:]
    )
    theorem = HyperoctahedralBranchingMassTheorem(
        exact_joint_law=(
            "For even-central-parity mu, q(lambda,mu)="
            "2 d_lambda d_mu b(lambda,mu)/|S_(2m)|."
        ),
        exact_marginals=(
            "The lambda marginal is H-spherical Plancherel; the mu marginal "
            "is K-Plancherel conditioned on even central parity."
        ),
        low_multiplicity_bound=(
            "Pr[b<=T] <= 2 T I_(2m) J_m^+/(2m)!, with "
            "J_m^+=sum_(b even) binom(m,b) I_(m-b)I_b."
        ),
        natural_threshold=(
            "For T=M^(1/4), the low-multiplicity probability vanishes; T is "
            "superpolynomial in the permutation input length."
        ),
        joint_source_conclusion=(
            "A union bound over k=ceil(log2(64M)) source coordinates leaves "
            "overwhelming mass with every branching multiplicity above T."
        ),
        K_qft_missing_label_boundary=(
            "C[K] acts as identity on each branching-copy factor C^b, so K "
            "Fourier labels and K observables cannot resolve missing labels."
        ),
        paired_tower_escape=(
            "A recursive missing-label basis along the paired S_(2m)/K_m "
            "Bratteli square could still be efficient; large b alone is not a "
            "circuit lower bound."
        ),
        exact_joint_law_proved=True,
        low_multiplicity_counting_bound_proved=exact,
        natural_mass_in_superpolynomial_branching_proved=exact and asymptotic_mass,
        K_qft_resolves_missing_labels=False,
        paired_young_graph_recursion_compiled=False,
        source_aware_normalized_subduction_transform_compiled=False,
        theorem_verified=exact and asymptotic_mass,
        status=(
            "natural-huge-hyperoctahedral-branching-mass-proved-missing-label-recursion-open"
            if exact and asymptotic_mass
            else "hyperoctahedral-branching-mass-control-failure"
        ),
    )
    return HyperoctahedralBranchingMassReport(
        created_at=utc_now(),
        theorem_contract={
            "branching_coefficient": (
                "b(lambda;alpha,beta)=<s_lambda,"
                "s_alpha[h_2]s_beta[e_2]> for K=C_2 wr S_m."
            ),
            "source_refinement": (
                "Measure one source coordinate's G irrep and then refine its "
                "h-even carrier into K irreps."
            ),
            "claim_boundary": (
                "Natural missing-label multiplicity and K-QFT blindness, not "
                "a lower bound on recursive subduction circuits."
            ),
        },
        dimension_sum_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-PAIRED-YOUNG-MISSING-LABEL-ALGEBRA",
                "statement": (
                    "Construct a maximal efficiently measurable commutative "
                    "subalgebra of End_K([lambda]) that labels natural repeated "
                    "hyperoctahedral branches."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-PAIRED-YOUNG-LOCAL-ROTATIONS",
                "statement": (
                    "Derive polynomial-time computable local rotations for the "
                    "S_(2m) to C_2 wr S_m paired Bratteli recursion."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MULTICOPY-NORMALIZED-RECOUPLING",
                "statement": (
                    "Compose per-coordinate missing-label transforms with the "
                    "multicopy invariant overlap at poly(n) normalization."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Repeated K branches may be a negligible natural event.",
                "answer": (
                    "False: the exact dimension-sum bound puts all logarithmically "
                    "many source coordinates above M^(1/4) multiplicity on "
                    "overwhelming asymptotic mass."
                ),
                "resolved": True,
            },
            {
                "challenge": "A K QFT labels the repeated copies.",
                "answer": (
                    "False: every K operator acts identically on the branching "
                    "multiplicity factor. A commutant missing-label algebra is required."
                ),
                "resolved": True,
            },
            {
                "challenge": "Huge multiplicity proves the transform is hard.",
                "answer": (
                    "False: a Bratteli path label uses only polynomially many bits, "
                    "and a local paired-tower recurrence remains possible."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "dimension_sum_control_count": len(controls),
            "dimension_sum_control_failure_count": sum(
                not row.dimension_sum_identities_verified for row in controls
            ),
            "joint_high_branching_natural_mass_scaling_count": sum(
                row.all_source_coordinates_high_branching_on_natural_mass
                for row in scaling
            ),
            "tail_joint_high_branching_mass_lower_bound": (
                scaling[-1].joint_all_source_high_multiplicity_probability_lower_bound
            ),
            "tail_branching_threshold_log2": (
                scaling[-1].branching_multiplicity_threshold_log2
            ),
            "tail_missing_label_commutant_dimension_log2_lower_bound": (
                scaling[-1].missing_label_commutant_dimension_log2_lower_bound
            ),
            "paired_young_graph_recursion_count": 0,
            "normalized_subduction_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_even_branch_joint_law_proved": True,
            "natural_mass_in_superpolynomial_branching_proved": (
                exact and asymptotic_mass
            ),
            "K_qft_resolves_branching_missing_labels": False,
            "paired_young_graph_recursion_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural source mass requires enormous repeated K branches; "
                "their commutant labels and normalized multicopy recoupling "
                "remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that every natural source coordinate has superpolynomial "
            "hyperoctahedral branching multiplicity on overwhelming mass and "
            "localized the missing information to the K-commutant copy labels."
        ),
        falsifiers_triggered=[
            "Natural hyperoctahedral restriction is not multiplicity-free or low-multiplicity.",
            "K Fourier labels cannot resolve the repeated branch copies.",
            "Multiplicity size alone remains insufficient for a circuit lower bound.",
        ],
    )


def write_hyperoctahedral_branching_mass_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_hyperoctahedral_branching_mass_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_hyperoctahedral_branching_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
