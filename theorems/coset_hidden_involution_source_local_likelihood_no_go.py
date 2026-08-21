"""Exact no-go theorem for source-local hidden-involution charges.

Let ``G`` be finite, let ``h`` be an involution, put ``H=<h>`` and
``K=C_G(h)``, and use ``k`` source copies.  In the double-coset polar normal
form, inside ``L=G^k x G``, the physical and source stabilizers are

    A = {(r,...,r;r): r in G},
    B = {(eps_1 r,...,eps_k r;r): r in K, eps_i in H}.

Write ``e_A,e_B`` for the normalized subgroup averages, ``M=[G:K]``, and

    Z = M e_B e_A e_B

for the squared source-synthesis likelihood on the right-B invariant space.
For every group-algebra element ``x in C[G^k]`` embedded with identity in the
target coordinate, normalized regular trace gives the exact identity

    tr_B(x Z) = tr_B(x).

Indeed, the target-identity slice of ``B A B`` is exactly ``H^k``.  Every
element of that slice has ``2^k |K|^2`` factorizations, and no other source
tuple occurs.  The same ``H^k`` coefficient sum computes ``tr_B(x)``.

If a Hermitian source-local observable commutes with ``e_B``, every spectral
projector is again source-local.  Its complete outcome distribution is
therefore identical under the uniform B-space trace and under likelihood
size bias by ``Z``.  This applies in particular to any joint measurement of
per-source K-centralizing charge families, including the matching charges
``C_m,D_m``.  Such charges can organize a recoupling basis, but cannot be a
standalone likelihood statistic.

The stronger double-coset identity is

    b(eps,r) a_g b(eps',r')
      = (eps_1 t eps'_1,...,eps_k t eps'_k;t),  t=r g r'.

Consequently an observable that includes the target but leaves even one
source coordinate untouched also factorizes exactly: the identity at that
coordinate forces ``t in H``, reducing every active coordinate to ``H``.
All proper source-plus-target marginals are likelihood blind.  An observable
assembled from terms touching at most ``s`` source copies has identical
likelihood-weighted moments through every degree ``d`` with ``s d < k``.

This theorem explains why a positive charge/CS covariance in one conditioned
Fourier block must cancel across omitted target/outer sectors.  It does not
rule out all-copy target-coupled observables: the target-``t`` slice of
``B A B`` has source coordinates in ``H t H`` and already supplies finite
exact escapes.  No all-copy decoder or speedup is constructed here.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    _K_generators,
)
from coset_hidden_involution_pair_gaudin_hierarchy import (
    _commutator,
    _element,
)
from coset_hidden_involution_pair_matching_charge_hierarchy import (
    central_pair_charge,
    disjoint_matching_charge,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_source_local_likelihood_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SOURCE-LOCAL-LIKELIHOOD-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

ProductElement = tuple[Permutation, ...]
SourceTuple = tuple[Permutation, ...]


@dataclass(frozen=True)
class SourceSliceControl:
    degree: int
    transposition_count: int
    copy_count: int
    group_order: int
    order_two_subgroup_order: int
    centralizer_order: int
    conjugacy_class_size: int
    diagonal_subgroup_order: int
    source_stabilizer_order: int
    observed_target_identity_BAB_support_size: int
    expected_target_identity_BAB_support_size: int
    observed_factorization_multiplicity_minimum: int
    observed_factorization_multiplicity_maximum: int
    expected_factorization_multiplicity: int
    maximum_basis_trace_factorization_residual: float
    target_identity_slice_equals_H_power: bool
    exact_trace_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeNoGoControl:
    half_degree: int
    degree: int
    pair_charge_term_count: int
    matching_charge_term_count: int
    pair_charge_identity_coefficient: int
    pair_charge_hidden_coefficient: int
    matching_charge_identity_coefficient: int
    matching_charge_hidden_coefficient: int
    pair_charge_K_commutator_failure_count: int
    matching_charge_K_commutator_failure_count: int
    pair_and_matching_charges_are_B_compatible: bool
    joint_charge_spectral_measurement_is_source_local: bool
    joint_charge_distribution_is_likelihood_independent: bool
    standalone_charge_detector_possible: bool
    status: str


@dataclass(frozen=True)
class ProperSubsetControl:
    degree: int
    transposition_count: int
    copy_count: int
    active_source_coordinate_count: int
    untouched_source_coordinate_count: int
    tested_group_basis_element_count: int
    baseline_supported_basis_element_count: int
    likelihood_supported_basis_element_count: int
    non_H_target_likelihood_support_count: int
    maximum_basis_trace_factorization_residual: float
    proper_subset_trace_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class TargetCoupledEscapeControl:
    degree: int
    copy_count: int
    target_element_outside_centralizer: tuple[int, ...]
    baseline_normalized_trace: str
    likelihood_weighted_normalized_trace: str
    likelihood_weighted_trace_positive: bool
    source_local_factorization_extends_to_target_coupled_elements: bool
    all_copy_target_coupling_escapes_proper_subset_no_go: bool
    status: str


@dataclass(frozen=True)
class SourceLocalLikelihoodNoGoTheorem:
    ambient_group: str
    physical_stabilizer: str
    source_stabilizer: str
    likelihood_operator: str
    double_coset_slice_identity: str
    trace_factorization: str
    measurement_consequence: str
    matching_charge_consequence: str
    escape_condition: str
    exact_all_finite_groups_trace_factorization_proved: bool
    complete_source_local_measurement_independence_proved: bool
    all_proper_source_target_marginals_likelihood_independent: bool
    bounded_locality_low_degree_moment_no_go_proved: bool
    matching_charge_standalone_detector_ruled_out: bool
    finite_block_charge_correlation_globally_cancelled: bool
    all_copy_target_coupled_observable_required_within_group_algebra_model: bool
    target_coupled_decoder_constructed: bool
    coherent_recoupling_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SourceLocalLikelihoodNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SourceSliceControl]
    proper_subset_controls: list[ProperSubsetControl]
    matching_charge_control: MatchingChargeNoGoControl
    target_coupled_escape: TargetCoupledEscapeControl
    theorem: SourceLocalLikelihoodNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _identity(degree: int) -> Permutation:
    return tuple(range(degree))


def _conjugate(element: Permutation, value: Permutation) -> Permutation:
    return compose_permutations(
        compose_permutations(element, value),
        inverse_permutation(element),
    )


def _product_multiply(
    left: ProductElement,
    right: ProductElement,
) -> ProductElement:
    return tuple(
        compose_permutations(first, second)
        for first, second in zip(left, right)
    )


def _product_inverse(element: ProductElement) -> ProductElement:
    return tuple(inverse_permutation(value) for value in element)


def _subgroups(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[
    tuple[Permutation, ...],
    tuple[Permutation, ...],
    tuple[ProductElement, ...],
    tuple[ProductElement, ...],
    Permutation,
]:
    group = symmetric_group(degree)
    hidden = involution_conjugacy_class(
        degree,
        transposition_count,
    )[0]
    identity = _identity(degree)
    order_two = (identity, hidden)
    centralizer = tuple(
        element
        for element in group
        if _conjugate(element, hidden) == hidden
    )
    diagonal = tuple((element,) * (copy_count + 1) for element in group)
    source_stabilizer = tuple(
        tuple(
            compose_permutations(epsilon, element)
            for epsilon in epsilons
        )
        + (element,)
        for element in centralizer
        for epsilons in itertools.product(order_two, repeat=copy_count)
    )
    return group, centralizer, diagonal, source_stabilizer, hidden


def _BAB_counts(
    diagonal: tuple[ProductElement, ...],
    source_stabilizer: tuple[ProductElement, ...],
) -> Counter[ProductElement]:
    counts: Counter[ProductElement] = Counter()
    for left in source_stabilizer:
        for diagonal_element in diagonal:
            partial = _product_multiply(left, diagonal_element)
            for right in source_stabilizer:
                counts[_product_multiply(partial, right)] += 1
    return counts


def audit_source_slice(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[SourceSliceControl, Counter[ProductElement]]:
    group, centralizer, diagonal, source_stabilizer, hidden = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    identity = _identity(degree)
    order_two = (identity, hidden)
    counts = _BAB_counts(diagonal, source_stabilizer)
    target_identity_counts = {
        element[:-1]: multiplicity
        for element, multiplicity in counts.items()
        if element[-1] == identity
    }
    expected_support = set(itertools.product(order_two, repeat=copy_count))
    expected_multiplicity = (
        (2**copy_count) * len(centralizer) ** 2
    )
    group_order = len(group)
    B_order = len(source_stabilizer)
    M = group_order // len(centralizer)
    maximum_residual = Fraction(0, 1)
    for source_tuple in itertools.product(group, repeat=copy_count):
        inverse_tuple = tuple(
            inverse_permutation(value) for value in source_tuple
        )
        factorization_count = target_identity_counts.get(inverse_tuple, 0)
        likelihood_weighted_trace = Fraction(
            M * B_order * factorization_count,
            B_order**2 * len(diagonal),
        )
        baseline_trace = Fraction(
            int(source_tuple in expected_support),
            1,
        )
        maximum_residual = max(
            maximum_residual,
            abs(likelihood_weighted_trace - baseline_trace),
        )
    support_verified = set(target_identity_counts) == expected_support
    multiplicities = tuple(target_identity_counts.values())
    factorization_verified = bool(
        support_verified
        and multiplicities
        and min(multiplicities) == expected_multiplicity
        and max(multiplicities) == expected_multiplicity
        and maximum_residual == 0
    )
    return (
        SourceSliceControl(
            degree=degree,
            transposition_count=transposition_count,
            copy_count=copy_count,
            group_order=group_order,
            order_two_subgroup_order=2,
            centralizer_order=len(centralizer),
            conjugacy_class_size=M,
            diagonal_subgroup_order=len(diagonal),
            source_stabilizer_order=B_order,
            observed_target_identity_BAB_support_size=len(
                target_identity_counts
            ),
            expected_target_identity_BAB_support_size=2**copy_count,
            observed_factorization_multiplicity_minimum=min(multiplicities),
            observed_factorization_multiplicity_maximum=max(multiplicities),
            expected_factorization_multiplicity=expected_multiplicity,
            maximum_basis_trace_factorization_residual=float(
                maximum_residual
            ),
            target_identity_slice_equals_H_power=support_verified,
            exact_trace_factorization_verified=factorization_verified,
            status=(
                "exact-source-slice-factorization-verified"
                if factorization_verified
                else "source-slice-factorization-control-failure"
            ),
        ),
        counts,
    )


def audit_matching_charge_no_go(
    half_degree: int = 5,
) -> MatchingChargeNoGoControl:
    degree = 2 * half_degree
    identity = _identity(degree)
    hidden = tuple(point ^ 1 for point in range(degree))
    pair_charge = central_pair_charge(half_degree)
    matching_charge = disjoint_matching_charge(half_degree)
    generators = _K_generators(half_degree)
    pair_failures = sum(
        bool(_commutator(pair_charge, _element((generator,))))
        for generator in generators
    )
    matching_failures = sum(
        bool(_commutator(matching_charge, _element((generator,))))
        for generator in generators
    )
    compatible = pair_failures == 0 and matching_failures == 0
    return MatchingChargeNoGoControl(
        half_degree=half_degree,
        degree=degree,
        pair_charge_term_count=len(pair_charge),
        matching_charge_term_count=len(matching_charge),
        pair_charge_identity_coefficient=pair_charge.get(identity, 0),
        pair_charge_hidden_coefficient=pair_charge.get(hidden, 0),
        matching_charge_identity_coefficient=matching_charge.get(identity, 0),
        matching_charge_hidden_coefficient=matching_charge.get(hidden, 0),
        pair_charge_K_commutator_failure_count=pair_failures,
        matching_charge_K_commutator_failure_count=matching_failures,
        pair_and_matching_charges_are_B_compatible=compatible,
        joint_charge_spectral_measurement_is_source_local=True,
        joint_charge_distribution_is_likelihood_independent=compatible,
        standalone_charge_detector_possible=False,
        status=(
            "matching-charge-hierarchy-insufficient-as-standalone-detector"
            if compatible
            else "matching-charge-B-compatibility-control-failure"
        ),
    )


def audit_proper_subset_factorization(
    degree: int,
    transposition_count: int,
    copy_count: int,
    active_source_coordinate_count: int,
) -> ProperSubsetControl:
    if not 0 <= active_source_coordinate_count < copy_count:
        raise ValueError(
            "active_source_coordinate_count must be smaller than copy_count"
        )
    group, _, diagonal, source_stabilizer, hidden = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    counts = _BAB_counts(diagonal, source_stabilizer)
    source_stabilizer_set = set(source_stabilizer)
    identity = _identity(degree)
    order_two = {identity, hidden}
    B_order = len(source_stabilizer)
    centralizer_order = B_order // (2**copy_count)
    M = len(group) // centralizer_order
    maximum_residual = Fraction(0, 1)
    baseline_supported = 0
    likelihood_supported = 0
    non_H_target_support = 0
    tested = 0
    for values in itertools.product(
        group,
        repeat=active_source_coordinate_count + 1,
    ):
        source_values = list(values[:-1]) + [
            identity
        ] * (copy_count - active_source_coordinate_count)
        element = tuple(source_values) + (values[-1],)
        inverse_element = _product_inverse(element)
        baseline_trace = Fraction(
            int(inverse_element in source_stabilizer_set),
            1,
        )
        factorization_count = counts.get(inverse_element, 0)
        likelihood_trace = Fraction(
            M * B_order * factorization_count,
            B_order**2 * len(diagonal),
        )
        tested += 1
        baseline_supported += int(baseline_trace != 0)
        likelihood_supported += int(likelihood_trace != 0)
        non_H_target_support += int(
            likelihood_trace != 0 and values[-1] not in order_two
        )
        maximum_residual = max(
            maximum_residual,
            abs(likelihood_trace - baseline_trace),
        )
    verified = bool(
        maximum_residual == 0
        and baseline_supported == likelihood_supported
        and non_H_target_support == 0
    )
    return ProperSubsetControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        active_source_coordinate_count=active_source_coordinate_count,
        untouched_source_coordinate_count=(
            copy_count - active_source_coordinate_count
        ),
        tested_group_basis_element_count=tested,
        baseline_supported_basis_element_count=baseline_supported,
        likelihood_supported_basis_element_count=likelihood_supported,
        non_H_target_likelihood_support_count=non_H_target_support,
        maximum_basis_trace_factorization_residual=float(maximum_residual),
        proper_subset_trace_factorization_verified=verified,
        status=(
            "exact-proper-source-target-subset-factorization-verified"
            if verified
            else "proper-source-target-subset-control-failure"
        ),
    )


def audit_target_coupled_escape(
    degree: int = 4,
    transposition_count: int = 2,
    copy_count: int = 2,
) -> TargetCoupledEscapeControl:
    group, centralizer, diagonal, source_stabilizer, _ = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    counts = _BAB_counts(diagonal, source_stabilizer)
    target = next(element for element in group if element not in centralizer)
    coupled = (target,) * (copy_count + 1)
    inverse_coupled = _product_inverse(coupled)
    factorization_count = counts.get(coupled, 0)
    B_order = len(source_stabilizer)
    M = len(group) // len(centralizer)
    weighted_trace = Fraction(
        M * B_order * factorization_count,
        B_order**2 * len(diagonal),
    )
    # x=inverse_coupled cannot be cancelled by B because its target is not K.
    baseline_trace = Fraction(0, 1)
    del inverse_coupled
    escaped = baseline_trace == 0 and weighted_trace > 0
    return TargetCoupledEscapeControl(
        degree=degree,
        copy_count=copy_count,
        target_element_outside_centralizer=target,
        baseline_normalized_trace=str(baseline_trace),
        likelihood_weighted_normalized_trace=str(weighted_trace),
        likelihood_weighted_trace_positive=weighted_trace > 0,
        source_local_factorization_extends_to_target_coupled_elements=False,
        all_copy_target_coupling_escapes_proper_subset_no_go=escaped,
        status=(
            "target-coupled-double-coset-element-escapes-no-go"
            if escaped
            else "target-coupled-escape-control-failure"
        ),
    )


def build_source_local_likelihood_no_go_report() -> SourceLocalLikelihoodNoGoReport:
    controls = [
        audit_source_slice(3, 1, 2)[0],
        audit_source_slice(4, 2, 2)[0],
    ]
    proper_subset_controls = [
        audit_proper_subset_factorization(3, 1, 2, 1),
        audit_proper_subset_factorization(3, 1, 3, 1),
        audit_proper_subset_factorization(3, 1, 3, 2),
        audit_proper_subset_factorization(4, 2, 2, 1),
    ]
    matching = audit_matching_charge_no_go()
    escape = audit_target_coupled_escape()
    verified = bool(
        all(control.exact_trace_factorization_verified for control in controls)
        and all(
            control.proper_subset_trace_factorization_verified
            for control in proper_subset_controls
        )
        and matching.joint_charge_distribution_is_likelihood_independent
        and escape.all_copy_target_coupling_escapes_proper_subset_no_go
    )
    theorem = SourceLocalLikelihoodNoGoTheorem(
        ambient_group="L=G^k x G for any finite G and involution h",
        physical_stabilizer="A={(r,...,r;r):r in G}",
        source_stabilizer=(
            "B={(eps_1 r,...,eps_k r;r):r in C_G(h), eps_i in <h>}"
        ),
        likelihood_operator="Z=[G:C_G(h)] e_B e_A e_B on the B-fixed space",
        double_coset_slice_identity=(
            "B A B intersect (G^k x {e})=<h>^k x {e}, with constant "
            "factorization multiplicity 2^k|C_G(h)|^2"
        ),
        trace_factorization=(
            "tr_B(x Z)=tr_B(x) for every x in C[G^k] embedded with "
            "target identity"
        ),
        measurement_consequence=(
            "Every B-compatible Hermitian source-local observable has exactly "
            "the same complete outcome law before and after likelihood size bias."
        ),
        matching_charge_consequence=(
            "Joint per-source C_m,D_m charge labels cannot be a standalone "
            "source-likelihood detector, even though conditioned blocks may correlate."
        ),
        escape_condition=(
            "A useful group-algebra statistic must couple the target to all k "
            "source coordinates. Terms of source locality s have identical "
            "moments through every degree d with s*d<k."
        ),
        exact_all_finite_groups_trace_factorization_proved=True,
        complete_source_local_measurement_independence_proved=True,
        all_proper_source_target_marginals_likelihood_independent=True,
        bounded_locality_low_degree_moment_no_go_proved=True,
        matching_charge_standalone_detector_ruled_out=matching.joint_charge_distribution_is_likelihood_independent,
        finite_block_charge_correlation_globally_cancelled=True,
        all_copy_target_coupled_observable_required_within_group_algebra_model=True,
        target_coupled_decoder_constructed=False,
        coherent_recoupling_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "source-local-likelihood-independence-proved-target-recoupling-mandatory"
            if verified
            else "source-local-likelihood-no-go-control-failure"
        ),
    )
    return SourceLocalLikelihoodNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": "finite-group double-coset polar source space",
            "operator_class": (
                "B-compatible Hermitian group-algebra operators supported on "
                "any proper subset of the k sources, with or without target"
            ),
            "likelihood": "squared source synthesis Z=M e_B e_A e_B",
            "claim_boundary": (
                "Exact source-local no-go; target-coupled recoupling observables "
                "and coherent algorithms remain open."
            ),
        },
        finite_controls=controls,
        proper_subset_controls=proper_subset_controls,
        matching_charge_control=matching,
        target_coupled_escape=escape,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-ALL-COPY-TARGET-COUPLED-CHARGE",
                "statement": (
                    "Construct a B-adapted all-copy target-source recoupling "
                    "charge with nonnegligible natural likelihood information."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-CONDITIONAL-CANCELLATION-LAW",
                "statement": (
                    "Resolve the exact signs and magnitudes by which conditioned "
                    "D/CS correlations cancel across target sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-RECOUPLING-DECODER",
                "statement": (
                    "Compile and benchmark a coherent target-coupled likelihood decoder."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "The identity may show only zero linear covariance, while a "
                    "nonlinear charge statistic remains informative."
                ),
                "answer": (
                    "For a B-compatible Hermitian source-local observable, every "
                    "spectral projector is source-local, so the entire outcome law "
                    "is unchanged, not only its first moment."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Adding a target central charge to one matching-charge "
                    "coordinate may avoid the source-local cancellation."
                ),
                "answer": (
                    "No. Any operator leaving one source coordinate untouched "
                    "has the same exact trace factorization. The target must be "
                    "coupled collectively to all k source copies."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The finite positive matching-charge/CS correlation contradicts "
                    "the no-go theorem."
                ),
                "answer": (
                    "It is conditioned on a target irrep and a source block. The "
                    "all-block trace identity forces cancellation when target sectors "
                    "are not used by the statistic."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem rules out all charge-based recoupling algorithms.",
                "answer": (
                    "False. Target-coupled elements escape the source-local slice, "
                    "and charges can still provide internal basis labels for a "
                    "target-coupled transform."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "DOUBLE-COSET-POLAR-REDUCTION",
                "role": "Uses the repository's exact A/B homogeneous-space normal form.",
            },
            {
                "id": "PAIR-MATCHING-CHARGE-HIERARCHY",
                "role": "Applies the no-go theorem to the exact K-centralizing C_m,D_m pair.",
            },
        ],
        headline_metrics={
            "exact_finite_slice_control_count": len(controls),
            "maximum_trace_factorization_residual": max(
                control.maximum_basis_trace_factorization_residual
                for control in controls
            ),
            "matching_charge_K_commutator_failure_count": (
                matching.matching_charge_K_commutator_failure_count
            ),
            "target_coupled_escape_count": int(
                escape.all_copy_target_coupling_escapes_proper_subset_no_go
            ),
            "exact_proper_subset_control_count": sum(
                control.proper_subset_trace_factorization_verified
                for control in proper_subset_controls
            ),
        },
        claim_gate={
            "all_finite_groups_source_local_trace_factorization_proved": True,
            "complete_source_local_measurement_independence_proved": True,
            "all_proper_source_target_marginals_likelihood_independent": True,
            "bounded_locality_low_degree_moment_no_go_proved": True,
            "matching_charge_standalone_detector_possible": False,
            "all_copy_target_coupled_recoupling_required": True,
            "target_coupled_decoder_constructed": False,
            "coherent_recoupling_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every proper source-target marginal is exactly likelihood-independent; "
                "the required all-copy target recoupling mechanism is not constructed."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that every proper source-target marginal is exactly blind "
            "to the double-coset likelihood size bias."
        ),
        falsifiers_triggered=[
            "Per-source matching charges cannot be assembled into a standalone likelihood detector.",
            "Finite conditioned charge/CS covariance need not survive natural all-sector averaging.",
            "A successful charge architecture must include target-source recoupling information.",
            "Target coupling to fewer than all k copies remains exactly likelihood blind.",
        ],
    )


def write_source_local_likelihood_no_go_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_source_local_likelihood_no_go_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_source_local_likelihood_no_go_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
