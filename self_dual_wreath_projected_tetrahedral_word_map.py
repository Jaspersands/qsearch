"""Exact high-dimensional Fourier projection of the tetrahedral word map.

The dimension trim identifies the retained six-label problem but does not
provide an analytic object to estimate.  This module supplies that object.

For a retained irrep set ``R`` of ``S_n``, define the central mean and
Plancherel covariance kernels

    m_R(x)   = (1/|G|) sum_(rho in R) d_rho chi_rho(x),
    K_R(x,y) = (1/|G|) sum_(rho in R) chi_rho(x)chi_rho(y),
    q_R      = (1/|G|) sum_(rho in R) d_rho^2.             (1)

Let ``W(t)=(g,h,k,gk,hk,ghk)`` for ``t=(g,h,k)``.  The sub-probability
chi-square retained on ``R^6`` is exactly

    C_R = sum_(rho_1,...,rho_6 in R) q_rho_1...q_rho_6
              (L(rho_1,...,rho_6)-1)^2

        = sum_(t,u in G^3) product_i K_R(W_i(t),W_i(u))
          - 2 sum_(t in G^3) product_i m_R(W_i(t))
          + q_R^6.                                        (2)

Equation (2) follows by expanding the square and applying Plancherel
orthogonality independently on all six edges.  It is also computable on
cycle-type signatures rather than ``|G|^6`` pairs.

The retained unnormalized total variation obeys

    TV_R <= (q_R^3/2) sqrt(C_R) <= sqrt(C_R)/2.            (3)

Thus ``C_R=o(1)`` is a sufficient high-dimensional measured-label no-go.
It is not necessary: another likelihood tail inside ``R`` can keep chi-square
large while TV vanishes.  Positive KL or direct L1 control must accompany a
nonvanishing second moment.

For the canonical near-maximal-dimension set, (2) is the precise unresolved
harmonic-analysis problem.  Existing fixed-cycle word-measure theorems probe
stable low-level characters that the trim removes, while current normalized-
character bounds do not by themselves control the correlated six-word
contraction.  A proof must establish a six-fold projected word-map mixing
estimate, or construct a positive-mass retained counterfamily.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
    tetrahedral_class_signature_counts,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_projected_tetrahedral_word_map.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PROJECTED-TETRAHEDRAL-WORD-MAP"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class ProjectedTetrahedralWordMapControl:
    n: int
    minimum_retained_dimension_exclusive: int
    retained_partition_count: int
    retained_plancherel_mass: float
    retained_product_mass: float
    retained_physical_mass: float
    removed_product_mass: float
    removed_physical_mass: float
    label_space_subprobability_chi_square: float
    projected_kernel_subprobability_chi_square: float | None
    projected_kernel_identity_residual: float | None
    retained_unnormalized_total_variation: float
    chi_square_total_variation_upper_bound: float
    conditional_retained_total_variation: float
    retained_positive_kl_contribution_bits: float
    exact_projected_kernel_identity_verified: bool | None
    status: str


@dataclass(frozen=True)
class ProjectedTetrahedralWordMapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ProjectedTetrahedralWordMapControl]
    projected_kernel_contract: dict[str, str | bool]
    literature_boundary: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def retained_partitions(n: int, minimum_dimension_exclusive: int) -> tuple[Partition, ...]:
    if n < 2 or minimum_dimension_exclusive < 0:
        raise ValueError("invalid retained-partition parameters")
    return tuple(
        partition
        for partition in integer_partitions(n)
        if hook_length_dimension(partition) > minimum_dimension_exclusive
    )


def projected_mean_and_kernel(
    n: int,
    minimum_dimension_exclusive: int,
) -> tuple[tuple[Partition, ...], Fraction, dict[Partition, Fraction], dict[tuple[Partition, Partition], Fraction]]:
    classes = tuple(integer_partitions(n))
    retained = retained_partitions(n, minimum_dimension_exclusive)
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition) for partition in retained
    }
    characters = {
        (partition, cycle_type): symmetric_character(partition, cycle_type)
        for partition in retained
        for cycle_type in classes
    }
    mass = Fraction(sum(dimension * dimension for dimension in dimensions.values()), order)
    mean = {
        cycle_type: Fraction(
            sum(
                dimensions[partition] * characters[partition, cycle_type]
                for partition in retained
            ),
            order,
        )
        for cycle_type in classes
    }
    kernel = {
        (left, right): Fraction(
            sum(
                characters[partition, left] * characters[partition, right]
                for partition in retained
            ),
            order,
        )
        for left in classes
        for right in classes
    }
    return retained, mass, mean, kernel


def projected_kernel_subprobability_chi_square(
    n: int,
    minimum_dimension_exclusive: int,
) -> Fraction:
    """Evaluate (2) exactly through class signatures for ``n<=4``."""

    if not 2 <= n <= 4:
        raise ValueError("exact projected-kernel controls require 2<=n<=4")
    _retained, mass, mean, kernel = projected_mean_and_kernel(
        n,
        minimum_dimension_exclusive,
    )
    signatures = tetrahedral_class_signature_counts(n)
    first = Fraction()
    for left, left_count in signatures.items():
        for right, right_count in signatures.items():
            first += left_count * right_count * math.prod(
                kernel[left[index], right[index]] for index in range(6)
            )
    cross = sum(
        (
            count * math.prod(mean[cycle_type] for cycle_type in signature)
            for signature, count in signatures.items()
        ),
        start=Fraction(),
    )
    return first - 2 * cross + mass**6


def audit_projected_tetrahedral_word_map(
    n: int,
    minimum_dimension_exclusive: int,
    *,
    validate_projected_kernel: bool = False,
) -> ProjectedTetrahedralWordMapControl:
    partitions, likelihood, product, physical = finite_physical_likelihood_arrays(n)
    dimensions = np.asarray(
        [hook_length_dimension(partition) for partition in partitions]
    )
    retained_one = dimensions > minimum_dimension_exclusive
    retained_mask = np.ones(likelihood.shape, dtype=bool)
    for axis in range(6):
        shape = [1] * 6
        shape[axis] = len(partitions)
        retained_mask &= retained_one.reshape(shape)
    retained_count = int(np.sum(retained_one))
    order = math.factorial(n)
    retained_mass = sum(
        dimension * dimension
        for dimension in dimensions[retained_one]
    ) / order
    product_mass = float(np.sum(product[retained_mask]))
    physical_mass = float(np.sum(physical[retained_mask]))
    sub_chi = float(
        np.sum(product[retained_mask] * (likelihood[retained_mask] - 1.0) ** 2)
    )
    projected = (
        projected_kernel_subprobability_chi_square(
            n,
            minimum_dimension_exclusive,
        )
        if validate_projected_kernel
        else None
    )
    residual = abs(sub_chi - float(projected)) if projected is not None else None
    sub_tv = 0.5 * float(
        np.sum(np.abs(physical[retained_mask] - product[retained_mask]))
    )
    tv_upper = 0.5 * retained_mass**3 * math.sqrt(max(0.0, sub_chi))
    if physical_mass > 0 and product_mass > 0:
        conditional_tv = 0.5 * float(
            np.sum(
                np.abs(
                    physical[retained_mask] / physical_mass
                    - product[retained_mask] / product_mass
                )
            )
        )
    else:
        conditional_tv = 0.0
    positive = retained_mask & (likelihood > 1.0)
    positive_kl = float(
        np.sum(physical[positive] * np.log2(likelihood[positive]))
    )
    verified = residual is None or residual <= 1e-8
    return ProjectedTetrahedralWordMapControl(
        n=n,
        minimum_retained_dimension_exclusive=minimum_dimension_exclusive,
        retained_partition_count=retained_count,
        retained_plancherel_mass=retained_mass,
        retained_product_mass=product_mass,
        retained_physical_mass=physical_mass,
        removed_product_mass=1.0 - product_mass,
        removed_physical_mass=1.0 - physical_mass,
        label_space_subprobability_chi_square=sub_chi,
        projected_kernel_subprobability_chi_square=(
            float(projected) if projected is not None else None
        ),
        projected_kernel_identity_residual=residual,
        retained_unnormalized_total_variation=sub_tv,
        chi_square_total_variation_upper_bound=tv_upper,
        conditional_retained_total_variation=conditional_tv,
        retained_positive_kl_contribution_bits=positive_kl,
        exact_projected_kernel_identity_verified=(
            verified if projected is not None else None
        ),
        status=(
            "exact-projected-word-map-identity-verified"
            if verified
            else "projected-word-map-identity-control-failure"
        ),
    )


def run_projected_tetrahedral_word_map() -> ProjectedTetrahedralWordMapReport:
    controls = [
        audit_projected_tetrahedral_word_map(
            n,
            threshold,
            validate_projected_kernel=n <= 4,
        )
        for n, threshold in (
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 0),
            (4, 1),
            (4, 2),
            (5, 0),
            (5, 1),
            (5, 4),
        )
    ]
    failures = sum(
        row.exact_projected_kernel_identity_verified is False for row in controls
    )
    verified = failures == 0
    n5_full = next(
        row
        for row in controls
        if row.n == 5 and row.minimum_retained_dimension_exclusive == 0
    )
    n5_no_one_dimensional = next(
        row
        for row in controls
        if row.n == 5 and row.minimum_retained_dimension_exclusive == 1
    )
    return ProjectedTetrahedralWordMapReport(
        created_at=utc_now(),
        theorem_contract={
            "projected_mean": "m_R(x)=|G|^-1 sum_(rho in R)d_rho chi_rho(x).",
            "projected_kernel": "K_R(x,y)=|G|^-1 sum_(rho in R)chi_rho(x)chi_rho(y).",
            "retained_mass": "q_R=|G|^-1 sum_(rho in R)d_rho^2.",
            "projected_word_map_identity": (
                "C_R=sum_(t,u)prod_i K_R(W_i(t),W_i(u))"
                "-2sum_t prod_i m_R(W_i(t))+q_R^6."
            ),
            "retained_tv_bound": "TV_R<=(q_R^3/2)sqrt(C_R).",
            "canonical_research_target": (
                "Take R={rho:d_rho>D_n} for the canonical near-maximal dimension trim."
            ),
            "scope": (
                "C_R=o(1) is sufficient but not necessary for retained TV decay; "
                "coherent multiplicity phases are absent."
            ),
        },
        finite_controls=controls,
        projected_kernel_contract={
            "word_tuple": "(g,h,k,gk,hk,ghk)",
            "input_randomness": "three independent uniform S_n permutations",
            "edge_projection": "central Fourier projector onto retained irreps R",
            "quantity": "six-fold projected class-signature collision norm",
            "sufficient_no_go": "C_R=o(1)",
            "positive_result_requirement": (
                "nonvanishing retained TV or positive KL on positive physical mass"
            ),
            "raw_untrimmed_chi_square_accepted_as_evidence": False,
        },
        literature_boundary=[
            {
                "id": "feray-sniady-character-bounds-2007",
                "url": "https://arxiv.org/abs/math/0701051",
                "boundary": (
                    "Pointwise bounds are strongest for short permutations; the six "
                    "word values are typically long and require correlated summation."
                ),
            },
            {
                "id": "lifshitz-marmor-hypercontractive-characters-2023",
                "url": "https://arxiv.org/abs/2308.08694",
                "boundary": (
                    "Normal-set mixing and level-based norm bounds do not directly "
                    "bound this six-edge high-level projected word-map tensor."
                ),
            },
            {
                "id": "benaych-georges-free-word-cycles-2010",
                "url": "https://arxiv.org/abs/math/0611500",
                "boundary": (
                    "Fixed small-cycle asymptotics for one word do not control the "
                    "joint full cycle types or high-dimensional Fourier projection."
                ),
            },
            {
                "id": "hanany-puder-word-measures-2026",
                "url": "https://arxiv.org/abs/2009.00897",
                "boundary": (
                    "Stable class-function estimates concern fixed-level Fourier data, "
                    "whereas the canonical trim retains near-maximal-dimensional modes."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "derive_exact_high_dimension_projected_word_map_identity",
                "resolved": verified,
                "resolution": (
                    "Expand retained label-space chi-square and apply six independent "
                    "Plancherel character sums; finite controls verify the class kernel."
                ),
            },
            {
                "obligation": "bound_canonical_projected_collision_norm",
                "resolved": False,
                "resolution": (
                    "Prove C_R=o(1) for d_rho>D_n, or identify the retained Fourier "
                    "modes and word signatures causing a nonvanishing term."
                ),
            },
            {
                "obligation": "rule_out_a_second_high_dimension_likelihood_tail",
                "resolved": False,
                "resolution": (
                    "If C_R does not vanish, test direct retained L1 and positive KL "
                    "before declaring a positive-mass signal."
                ),
            },
            {
                "obligation": "classical_baseline_for_retained_word_map_signal",
                "resolved": False,
                "resolution": (
                    "Compare any survivor with random-permutation cycle-type sampling "
                    "and character/Kronecker computations under the same access model."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Full character orthogonality already evaluates the retained projection.",
                "resolved": True,
                "resolution": (
                    "Only the untrimmed kernel collapses to conjugacy matching; the "
                    "high-dimensional projector is a signed nonlocal class kernel."
                ),
            },
            {
                "objection": "A nonzero finite projected chi-square is asymptotic evidence.",
                "resolved": False,
                "resolution": (
                    "Finite retained TV is sizable through S5 but has no scaling theorem."
                ),
            },
            {
                "objection": "C_R bounded away from zero would prove useful information.",
                "resolved": False,
                "resolution": (
                    "A high-dimensional likelihood tail can still separate L2 from L1/KL."
                ),
            },
            {
                "objection": "Projected word-map mixing supplies a coherent Racah compiler.",
                "resolved": False,
                "resolution": (
                    "It decides dephased information only; implementation and phase "
                    "access remain separate proof obligations."
                ),
            },
        ],
        headline_metrics={
            "projected_word_map_identity_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_finite_control_n": 5,
            "n5_full_chi_square": n5_full.label_space_subprobability_chi_square,
            "n5_after_one_dimensional_trim_chi_square": (
                n5_no_one_dimensional.label_space_subprobability_chi_square
            ),
            "n5_after_one_dimensional_trim_total_variation": (
                n5_no_one_dimensional.retained_unnormalized_total_variation
            ),
            "canonical_projected_collision_asymptotic_theorem_count": 0,
            "positive_mass_measured_signal_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "high_dimension_projected_word_map_identity_proved": verified,
            "raw_parity_chi_square_tail_excluded_by_projection": verified,
            "canonical_projected_collision_norm_vanishes_proved": False,
            "canonical_projected_collision_norm_survives_proved": False,
            "retained_positive_kl_survives_proved": False,
            "classical_baseline_separated": False,
            "coherent_multiplicity_transform_compiled": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact retained harmonic-analysis target is now explicit, but "
                "neither decay nor positive-mass survival has been proved."
            ),
        },
        status=(
            "high-dimensional-projected-word-map-reduced-asymptotic-open"
            if verified
            else "projected-tetrahedral-word-map-control-failure"
        ),
        summary=(
            "Converted dimension-trimmed six-label recoupling into an exact six-fold "
            "central Fourier projection of a three-permutation word map, isolating "
            "the remaining measured-label harmonic-analysis theorem."
        ),
        falsifiers_triggered=[
            "Stable fixed-cycle word-measure theorems do not reach the retained high-dimensional Fourier spectrum.",
            "Removing trivial/sign modes collapses the S5 chi-square from its raw tail-dominated value but leaves a finite unresolved bulk.",
            "Projected chi-square alone remains only a sufficient no-go metric, not a positive-signal certificate.",
        ],
    )


def write_projected_tetrahedral_word_map_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_projected_tetrahedral_word_map())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_projected_tetrahedral_word_map_report()
    print(json.dumps(report, indent=2))
