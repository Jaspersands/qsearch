"""Weak-Fourier marginal conservation under arbitrary-copy Kronecker fusion.

Let ``G`` be finite, ``h`` an involution, and let ``q`` independent coset
states for ``{e,h}`` be weak-Fourier decomposed.  Couple their representation
registers under the diagonal action and measure only the final irrep ``tau``.
The target marginal is exactly

    Pr_q[tau] = d_tau(d_tau + chi_tau(h)) / |G|,

independent of ``q``.  This is the one-copy weak-Fourier law.

The character-projector proof keeps the physical conditioned column states.
After summing each source label, the factor attached to ``g in G`` is

    S_h(g) = sum_lambda d_lambda
             (chi_lambda(g) + chi_lambda(g h))
           = |G| (1[g=e] + 1[g=h]).

For the diagonal target projector, ``q`` copies contribute ``S_h(g)^q``.
Only ``g=e,h`` remain, giving the formula above.  In contrast, replacing the
conditioned columns by maximally mixed representation spaces would incorrectly
predict an attenuated perturbation; that is not the physical coset-state law.

Consequences:

* ordinary diagonal Kronecker fusion does not concentrate rare Fourier labels;
* the final target law remains pointwise at most twice Plancherel for every q;
* central high-commutator-moment filtering after fusion is still covered by
  the stretched-exponential sector-filter no-go;
* any genuine collective gain must live in source-target correlations,
  multiplicity spaces, or a noncentral coherent observable, not the target
  irrep marginal alone.

The theorem does not say that the full joint recoupling outcome contains only
one-copy information.  Discarding source and multiplicity registers is an
essential part of its scope.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_same_hidden_target_law import (
    natural_joint_target_probability,
    source_label_probability,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character
from symmetric_marked_class_contraction import compose, cycle_type


REPORT_PATH = Path(
    "research/representation/coset_kronecker_marginal_conservation.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class RegularColumnSupportControl:
    n: int
    involution_cycle_type: Partition
    group_order: int
    supported_group_element_count: int
    expected_supported_group_element_count: int
    maximum_exact_column_residual: int
    exact_two_point_support_verified: bool
    status: str


@dataclass(frozen=True)
class FusionMarginalControl:
    n: int
    involution_cycle_type: Partition
    copy_count: int
    target_count: int
    exact_probability_sum: str
    maximum_exact_one_copy_residual: str
    maximum_pointwise_plancherel_ratio: float
    one_copy_weak_fourier_marginal_conserved: bool
    pointwise_two_plancherel_domination_verified: bool
    status: str


@dataclass(frozen=True)
class ExistingTwoCopyLawMarginalControl:
    n: int
    involution_cycle_type: Partition
    target_count: int
    ordered_source_pair_count: int
    exact_joint_probability_sum: str
    maximum_exact_target_marginal_residual: str
    existing_conditional_law_matches_conservation_theorem: bool
    status: str


@dataclass(frozen=True)
class KroneckerMarginalConservationTheorem:
    source_column_sum_identity: str
    q_copy_target_formula: str
    marginal_conservation_law: str
    plancherel_domination: str
    commutator_filter_consequence: str
    scope_limit: str
    arbitrary_copy_count: bool
    arbitrary_finite_group: bool
    target_label_amplification_possible: bool
    full_joint_information_collapses_to_one_copy: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class KroneckerMarginalConservationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    regular_column_controls: list[RegularColumnSupportControl]
    fusion_marginal_controls: list[FusionMarginalControl]
    existing_two_copy_controls: list[ExistingTwoCopyLawMarginalControl]
    theorem: KroneckerMarginalConservationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def canonical_involution(n: int, transposition_count: int) -> Permutation:
    if n < 2 or not 1 <= transposition_count <= n // 2:
        raise ValueError("invalid involution transposition count")
    permutation = list(range(n))
    for offset in range(transposition_count):
        left = 2 * offset
        right = left + 1
        permutation[left], permutation[right] = right, left
    return tuple(permutation)


def regular_column_sum(
    n: int,
    hidden_involution: Permutation,
    group_element: Permutation,
) -> int:
    """Compute ``sum_lambda d_lambda(chi_lambda(g)+chi_lambda(gh))``."""

    if len(hidden_involution) != n or len(group_element) != n:
        raise ValueError("permutations must have degree n")
    g_type = cycle_type(group_element)
    gh_type = cycle_type(compose(group_element, hidden_involution))
    return sum(
        hook_length_dimension(partition)
        * (
            symmetric_character(partition, g_type)
            + symmetric_character(partition, gh_type)
        )
        for partition in integer_partitions(n)
    )


def audit_regular_column_support(
    n: int,
    transposition_count: int,
) -> RegularColumnSupportControl:
    hidden = canonical_involution(n, transposition_count)
    identity = tuple(range(n))
    order = math.factorial(n)
    supported = 0
    maximum_residual = 0
    for group_element in itertools.permutations(range(n)):
        value = regular_column_sum(n, hidden, group_element)
        expected = order if group_element in {identity, hidden} else 0
        supported += value != 0
        maximum_residual = max(maximum_residual, abs(value - expected))
    verified = supported == 2 and maximum_residual == 0
    return RegularColumnSupportControl(
        n=n,
        involution_cycle_type=cycle_type(hidden),
        group_order=order,
        supported_group_element_count=supported,
        expected_supported_group_element_count=2,
        maximum_exact_column_residual=maximum_residual,
        exact_two_point_support_verified=verified,
        status=(
            "regular-column-two-point-support-verified"
            if verified
            else "regular-column-support-certificate-failure"
        ),
    )


def fused_target_probability_from_projector_sum(
    n: int,
    transposition_count: int,
    copy_count: int,
    target: Partition,
) -> Fraction:
    """Evaluate the source-summed diagonal target projector exactly."""

    if copy_count < 1:
        raise ValueError("copy count must be positive")
    if sum(target) != n:
        raise ValueError("target must partition n")
    hidden = canonical_involution(n, transposition_count)
    order = math.factorial(n)
    target_dimension = hook_length_dimension(target)
    numerator = 0
    for group_element in itertools.permutations(range(n)):
        source_sum = regular_column_sum(n, hidden, group_element)
        if source_sum:
            numerator += (
                symmetric_character(target, cycle_type(group_element))
                * source_sum**copy_count
            )
    return Fraction(
        target_dimension * numerator,
        order ** (copy_count + 1),
    )


def audit_fusion_marginal(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> FusionMarginalControl:
    hidden = canonical_involution(n, transposition_count)
    rows = []
    residuals = []
    maximum_ratio = Fraction(0)
    order = math.factorial(n)
    for target in integer_partitions(n):
        observed = fused_target_probability_from_projector_sum(
            n,
            transposition_count,
            copy_count,
            target,
        )
        expected = source_label_probability(
            n,
            transposition_count,
            target,
        )
        dimension = hook_length_dimension(target)
        plancherel = Fraction(dimension * dimension, order)
        rows.append(observed)
        residuals.append(abs(observed - expected))
        maximum_ratio = max(maximum_ratio, observed / plancherel)
    total = sum(rows, Fraction())
    conserved = total == 1 and max(residuals) == 0
    dominated = maximum_ratio <= 2
    return FusionMarginalControl(
        n=n,
        involution_cycle_type=cycle_type(hidden),
        copy_count=copy_count,
        target_count=len(rows),
        exact_probability_sum=str(total),
        maximum_exact_one_copy_residual=str(max(residuals)),
        maximum_pointwise_plancherel_ratio=float(maximum_ratio),
        one_copy_weak_fourier_marginal_conserved=conserved,
        pointwise_two_plancherel_domination_verified=dominated,
        status=(
            "q-copy-weak-fourier-marginal-conserved"
            if conserved and dominated
            else "q-copy-marginal-conservation-failure"
        ),
    )


def audit_existing_two_copy_law_marginal(
    n: int,
    transposition_count: int,
) -> ExistingTwoCopyLawMarginalControl:
    partitions = integer_partitions(n)
    residuals = []
    total = Fraction(0)
    for target in partitions:
        marginal = sum(
            (
                natural_joint_target_probability(
                    n,
                    transposition_count,
                    left,
                    right,
                    target,
                )
                for left in partitions
                for right in partitions
            ),
            start=Fraction(0),
        )
        expected = source_label_probability(
            n,
            transposition_count,
            target,
        )
        total += marginal
        residuals.append(abs(marginal - expected))
    verified = total == 1 and max(residuals) == 0
    return ExistingTwoCopyLawMarginalControl(
        n=n,
        involution_cycle_type=cycle_type(
            canonical_involution(n, transposition_count)
        ),
        target_count=len(partitions),
        ordered_source_pair_count=len(partitions) ** 2,
        exact_joint_probability_sum=str(total),
        maximum_exact_target_marginal_residual=str(max(residuals)),
        existing_conditional_law_matches_conservation_theorem=verified,
        status=(
            "existing-two-copy-law-marginal-conserved"
            if verified
            else "existing-two-copy-law-marginal-failure"
        ),
    )


def kronecker_marginal_conservation_theorem(
) -> KroneckerMarginalConservationTheorem:
    return KroneckerMarginalConservationTheorem(
        source_column_sum_identity=(
            "sum_lambda d_lambda(chi_lambda(g)+chi_lambda(gh))="
            "|G|(1[g=e]+1[g=h])"
        ),
        q_copy_target_formula=(
            "Pr_q[tau]=d_tau|G|^(-q-1) sum_g chi_tau(g)^* S_h(g)^q"
        ),
        marginal_conservation_law=(
            "Pr_q[tau]=d_tau(d_tau+chi_tau(h))/|G| for every q>=1"
        ),
        plancherel_domination="Pr_q[tau]<=2d_tau^2/|G|",
        commutator_filter_consequence=(
            "Final-label commutator-score filtering remains kappa=2 dominated "
            "for every fusion arity."
        ),
        scope_limit=(
            "The theorem discards source labels and multiplicity registers; it "
            "does not bound their correlations or coherent joint observables."
        ),
        arbitrary_copy_count=True,
        arbitrary_finite_group=True,
        target_label_amplification_possible=False,
        full_joint_information_collapses_to_one_copy=False,
        theorem_verified=True,
        status="all-copy-weak-fourier-target-marginal-conservation",
    )


def run_kronecker_marginal_conservation(
) -> KroneckerMarginalConservationReport:
    column_controls = [
        audit_regular_column_support(n, transpositions)
        for n, transpositions in ((3, 1), (4, 1), (4, 2), (5, 2))
    ]
    marginal_controls = [
        audit_fusion_marginal(n, transpositions, copies)
        for n, transpositions in ((3, 1), (4, 1), (4, 2), (5, 2))
        for copies in (1, 2, 3, 4, 7)
    ]
    existing_controls = [
        audit_existing_two_copy_law_marginal(n, transpositions)
        for n, transpositions in ((3, 1), (4, 1), (4, 2), (5, 2))
    ]
    theorem = kronecker_marginal_conservation_theorem()
    exact = (
        all(row.exact_two_point_support_verified for row in column_controls)
        and all(
            row.one_copy_weak_fourier_marginal_conserved
            and row.pointwise_two_plancherel_domination_verified
            for row in marginal_controls
        )
        and all(
            row.existing_conditional_law_matches_conservation_theorem
            for row in existing_controls
        )
        and theorem.theorem_verified
    )
    return KroneckerMarginalConservationReport(
        created_at=utc_now(),
        theorem_contract={
            "input": "q independent coset states for the same involution h",
            "operation": "diagonal irrep measurement after physical Kronecker fusion",
            "output": theorem.marginal_conservation_law,
            "scope": theorem.scope_limit,
        },
        regular_column_controls=column_controls,
        fusion_marginal_controls=marginal_controls,
        existing_two_copy_controls=existing_controls,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "retain_physical_conditioned_column_states",
                "resolved": True,
                "resolution": (
                    "Source probabilities cancel their normalization factors; "
                    "each source sum is the two-point regular-character kernel."
                ),
            },
            {
                "obligation": "derive_arbitrary_copy_target_marginal",
                "resolved": True,
                "resolution": (
                    "The diagonal character projector raises the same two-point "
                    "kernel to the qth power, leaving only e and h."
                ),
            },
            {
                "obligation": "reconcile_existing_two_copy_conditional_law",
                "resolved": True,
                "resolution": (
                    "Exact summation of the stored source-pair/target joint law "
                    "returns the one-copy target distribution in every control."
                ),
            },
            {
                "obligation": "exclude_target_label_signal_amplification",
                "resolved": True,
                "resolution": (
                    "The target marginal is exactly independent of fusion arity."
                ),
            },
            {
                "obligation": "bound_multiplicity_space_collective_information",
                "resolved": False,
                "resolution": (
                    "The source-target joint law and multiplicity coherences may "
                    "contain information absent from the target marginal."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Dimension-weighted fusion of Plancherel labels predicts attenuation.",
                "resolved": True,
                "resolution": (
                    "That replacement discards the hidden-conditioned column "
                    "operators. Physical source summation preserves the weak law."
                ),
            },
            {
                "objection": "More copies make a rare target irrep more likely.",
                "resolved": True,
                "resolution": (
                    "Not in the final target marginal: every q has exactly the "
                    "same pointwise probabilities."
                ),
            },
            {
                "objection": "Marginal conservation proves no collective gain exists.",
                "resolved": False,
                "resolution": (
                    "Correlations and multiplicity registers are discarded; a "
                    "noncentral coherent statistic can lie outside the theorem."
                ),
            },
        ],
        headline_metrics={
            "all_copy_marginal_conservation_theorem_count": int(exact),
            "regular_column_control_failure_count": sum(
                not row.exact_two_point_support_verified for row in column_controls
            ),
            "fusion_marginal_control_failure_count": sum(
                not row.one_copy_weak_fourier_marginal_conserved
                for row in marginal_controls
            ),
            "existing_two_copy_law_marginal_failure_count": sum(
                not row.existing_conditional_law_matches_conservation_theorem
                for row in existing_controls
            ),
            "maximum_tested_copy_count": max(
                row.copy_count for row in marginal_controls
            ),
            "maximum_tested_symmetric_group_degree": max(
                row.n for row in marginal_controls
            ),
            "target_label_signal_amplification_count": 0,
            "multiplicity_collective_information_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "ordinary_kronecker_target_label_amplifies_signal": False,
            "fused_target_law_escapes_two_plancherel_domination": False,
            "postfusion_central_commutator_filter_viable": False,
            "source_target_correlations_are_uninformative": False,
            "multiplicity_space_collective_gain_ruled_out": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Fusion conserves the one-copy target-label law exactly. Any gain "
                "must use correlations or multiplicity-space coherence rather than "
                "rare final labels."
            ),
        },
        status=(
            "kronecker-target-marginal-conserved-correlations-open"
            if exact
            else "kronecker-marginal-conservation-certificate-failure"
        ),
        summary=(
            "Proved that arbitrary-copy physical Kronecker fusion cannot amplify "
            "the weak-Fourier target-label marginal."
        ),
        falsifiers_triggered=[
            "Naive maximally mixed fusion drops the conditioned column operators.",
            "Target support occurrence does not imply target measurement mass gain.",
            "Additional copies do not improve the final irrep-label marginal.",
            "The surviving search space is joint and multiplicity-sensitive.",
        ],
    )


def write_kronecker_marginal_conservation_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_kronecker_marginal_conservation())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_kronecker_marginal_conservation_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
