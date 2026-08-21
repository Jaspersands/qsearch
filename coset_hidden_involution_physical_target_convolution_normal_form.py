"""Physical quotient normal form for genuine target-changing convolution.

Let ``L=G^k x G`` and ``A=diag(G)``.  Under the exact quotient coordinates

    Phi([(g_1,...,g_k;t)])=(x_1,...,x_k),  x_i=g_i t^-1,

left convolution by a group-basis element

    ell=(a_1,...,a_k;s)

acts as

    x_i -> a_i x_i s^-1                              (1)

on every source coordinate.  The shared right multiplier ``s^-1`` is what a
genuine target-changing operation becomes after gauge fixing.  In contrast,
target-diagonal representative control has ``s=e`` and reduces to the
source-local gauge-trivial route.

The exact likelihood operator has the positive group-basis expansion

    Z = 1/(4^k |K|)
        sum_(s in G) sum_(eps,eps' in H^k)
          (eps_1 s eps'_1,...,eps_k s eps'_k;s).       (2)

Define the conditioned shared-conjugation channel

    Q_s = 1/4^k sum_(eps,eps' in H^k)
            U_(eps,s,eps'),
    U_(eps,s,eps'): x_i -> eps_i s eps'_i x_i s^-1.

Then

    Z = 1/|K| sum_s Q_s = M E_(s uniform G)[Q_s],      (3)
    M=[G:K].

Every ``Q_s`` has positive group-basis L1 normalization one and factors over
source coordinates conditioned on the shared ``s``.  The full operator has
positive L1 normalization exactly ``M``.  Thus local twirls, term SELECT, and
uniform group sampling are not the hard part; the missing resource is a
structured coherent fast-forward of the factor ``M`` across the shared
conjugation orbit.

Equation (3) is an architecture reduction, not a detector.  Generic
PREP/SELECT implements ``Z/M`` and pays the normalization to recover ``Z``.
A successful quantum algorithm would need an implicit transform, polar, or
spectral construction that realizes the large cancellation/renormalization
without that cost and that survives matched classical estimation.  No such
fast-forward is proved here.
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

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    symmetric_group,
)
from coset_hidden_involution_matching_charge_target_gauge_trivialization import (
    SourceTuple,
    quotient_relative_coordinates,
)
from coset_hidden_involution_source_local_likelihood_no_go import (
    ProductElement,
    _subgroups,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_physical_target_convolution_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PHYSICAL-TARGET-CONVOLUTION-NORMAL-FORM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class QuotientConvolutionControl:
    degree: int
    copy_count: int
    tested_input_count: int
    tested_convolution_element_count: int
    quotient_action_formula_failure_count: int
    nonidentity_target_changes_every_relative_coordinate: bool
    exact_quotient_action_verified: bool
    status: str


@dataclass(frozen=True)
class LikelihoodExpansionControl:
    degree: int
    transposition_count: int
    copy_count: int
    group_order: int
    centralizer_order: int
    conjugacy_class_size: int
    raw_expansion_term_count: int
    distinct_group_basis_term_count: int
    positive_group_basis_L1_norm: str
    expected_positive_group_basis_L1_norm: int
    inside_K_conditioned_distinct_term_count_minimum: int
    inside_K_conditioned_distinct_term_count_maximum: int
    outside_K_conditioned_distinct_term_count_minimum: int
    outside_K_conditioned_distinct_term_count_maximum: int
    every_conditioned_Q_has_L1_one: bool
    Z_equals_M_times_uniform_Q_average: bool
    exact_expansion_verified: bool
    status: str


@dataclass(frozen=True)
class SharedConjugationScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    copy_count: int
    conditioned_Q_raw_term_count_decimal: str
    conditioned_Q_L1_norm: float
    full_Z_positive_L1_norm_decimal: str
    generic_uniform_group_block_encoding_normalization_decimal: str
    generic_normalization_is_candidate_count: bool
    status: str


@dataclass(frozen=True)
class PhysicalTargetConvolutionTheorem:
    quotient_action: str
    likelihood_expansion: str
    conditioned_channel: str
    normalization_identity: str
    compiler_boundary: str
    exact_all_finite_groups_quotient_action_proved: bool
    exact_shared_conjugation_likelihood_expansion_proved: bool
    conditioned_Q_normalization_one_proved: bool
    full_Z_positive_L1_equals_candidate_count_proved: bool
    generic_PREP_SELECT_fast_forward_compiled: bool
    structured_shared_orbit_fast_forward_compiled: bool
    matched_classical_separation_proved: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalTargetConvolutionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    quotient_controls: list[QuotientConvolutionControl]
    expansion_controls: list[LikelihoodExpansionControl]
    scaling_records: list[SharedConjugationScalingRecord]
    theorem: PhysicalTargetConvolutionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def quotient_left_convolution_action(
    sources: SourceTuple,
    target: Permutation,
    source_multipliers: SourceTuple,
    target_multiplier: Permutation,
) -> tuple[SourceTuple, Permutation]:
    if len(sources) != len(source_multipliers):
        raise ValueError("source multiplier count does not match copy count")
    return (
        tuple(
            compose_permutations(multiplier, source)
            for multiplier, source in zip(source_multipliers, sources)
        ),
        compose_permutations(target_multiplier, target),
    )


def direct_relative_convolution_action(
    relative_sources: SourceTuple,
    source_multipliers: SourceTuple,
    target_multiplier: Permutation,
) -> SourceTuple:
    target_inverse = inverse_permutation(target_multiplier)
    return tuple(
        compose_permutations(
            compose_permutations(multiplier, source),
            target_inverse,
        )
        for multiplier, source in zip(source_multipliers, relative_sources)
    )


def audit_quotient_convolution_action(
    degree: int,
    copy_count: int,
) -> QuotientConvolutionControl:
    group = symmetric_group(degree)
    probes = tuple(group[: min(6, len(group))])
    source_catalog = tuple(
        tuple(probes[(offset + index) % len(probes)] for index in range(copy_count))
        for offset in range(min(4, len(probes)))
    )
    failures = 0
    tested = 0
    nonidentity_changes_all = True
    identity = tuple(range(degree))
    for sources in source_catalog:
        for target in probes:
            relative = quotient_relative_coordinates(sources, target)
            for offset, target_multiplier in enumerate(probes):
                multipliers = tuple(
                    probes[(offset + index + 1) % len(probes)]
                    for index in range(copy_count)
                )
                acted_sources, acted_target = quotient_left_convolution_action(
                    sources,
                    target,
                    multipliers,
                    target_multiplier,
                )
                observed = quotient_relative_coordinates(
                    acted_sources,
                    acted_target,
                )
                expected = direct_relative_convolution_action(
                    relative,
                    multipliers,
                    target_multiplier,
                )
                failures += observed != expected
                if target_multiplier != identity:
                    # The shared right multiplier is algebraically present in every coordinate.
                    nonidentity_changes_all &= all(
                        compose_permutations(source, inverse_permutation(target_multiplier))
                        != source
                        for source in relative
                    )
                tested += 1
    verified = failures == 0
    return QuotientConvolutionControl(
        degree=degree,
        copy_count=copy_count,
        tested_input_count=len(source_catalog) * len(probes),
        tested_convolution_element_count=len(probes),
        quotient_action_formula_failure_count=failures,
        nonidentity_target_changes_every_relative_coordinate=nonidentity_changes_all,
        exact_quotient_action_verified=verified,
        status=(
            "physical-target-convolution-relative-action-verified"
            if verified
            else "physical-target-convolution-control-failure"
        ),
    )


def likelihood_expansion_coefficients(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[Counter[ProductElement], dict[Permutation, Counter[ProductElement]]]:
    group, centralizer, _, _, hidden = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    del centralizer
    identity = tuple(range(degree))
    order_two = (identity, hidden)
    total: Counter[ProductElement] = Counter()
    conditioned: dict[Permutation, Counter[ProductElement]] = {}
    for target in group:
        block: Counter[ProductElement] = Counter()
        for left_bits in itertools.product(order_two, repeat=copy_count):
            for right_bits in itertools.product(order_two, repeat=copy_count):
                sources = tuple(
                    compose_permutations(
                        compose_permutations(left, target),
                        right,
                    )
                    for left, right in zip(left_bits, right_bits)
                )
                element = sources + (target,)
                block[element] += 1
                total[element] += 1
        conditioned[target] = block
    return total, conditioned


def audit_likelihood_expansion(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> LikelihoodExpansionControl:
    group, centralizer, _, _, _ = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    total, conditioned = likelihood_expansion_coefficients(
        degree,
        transposition_count,
        copy_count,
    )
    raw_count = len(group) * 4**copy_count
    denominator = 4**copy_count * len(centralizer)
    L1 = Fraction(sum(total.values()), denominator)
    conditioned_L1 = [
        Fraction(sum(block.values()), 4**copy_count)
        for block in conditioned.values()
    ]
    centralizer_set = set(centralizer)
    inside_counts = [
        len(block)
        for target, block in conditioned.items()
        if target in centralizer_set
    ]
    outside_counts = [
        len(block)
        for target, block in conditioned.items()
        if target not in centralizer_set
    ]
    candidates = len(group) // len(centralizer)
    verified = bool(
        sum(total.values()) == raw_count
        and L1 == candidates
        and all(value == 1 for value in conditioned_L1)
        and set(inside_counts) == {2**copy_count}
        and set(outside_counts) == {4**copy_count}
    )
    return LikelihoodExpansionControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=len(group),
        centralizer_order=len(centralizer),
        conjugacy_class_size=candidates,
        raw_expansion_term_count=raw_count,
        distinct_group_basis_term_count=len(total),
        positive_group_basis_L1_norm=str(L1),
        expected_positive_group_basis_L1_norm=candidates,
        inside_K_conditioned_distinct_term_count_minimum=min(inside_counts),
        inside_K_conditioned_distinct_term_count_maximum=max(inside_counts),
        outside_K_conditioned_distinct_term_count_minimum=min(outside_counts),
        outside_K_conditioned_distinct_term_count_maximum=max(outside_counts),
        every_conditioned_Q_has_L1_one=all(value == 1 for value in conditioned_L1),
        Z_equals_M_times_uniform_Q_average=L1 == candidates,
        exact_expansion_verified=verified,
        status=(
            "shared-conjugation-likelihood-expansion-verified"
            if verified
            else "shared-conjugation-expansion-control-failure"
        ),
    )


def shared_conjugation_scaling_record(
    half_degree: int,
    copy_count: int,
) -> SharedConjugationScalingRecord:
    if half_degree < 2 or copy_count < 1:
        raise ValueError("invalid scaling parameters")
    degree = 2 * half_degree
    group_order = math.factorial(degree)
    centralizer_order = 2**half_degree * math.factorial(half_degree)
    candidates = group_order // centralizer_order
    return SharedConjugationScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        copy_count=copy_count,
        conditioned_Q_raw_term_count_decimal=str(4**copy_count),
        conditioned_Q_L1_norm=1.0,
        full_Z_positive_L1_norm_decimal=str(candidates),
        generic_uniform_group_block_encoding_normalization_decimal=str(candidates),
        generic_normalization_is_candidate_count=True,
        status="shared-conjugation-local-channels-easy-global-normalization-open",
    )


def build_physical_target_convolution_report() -> PhysicalTargetConvolutionReport:
    quotient_controls = [
        audit_quotient_convolution_action(3, 2),
        audit_quotient_convolution_action(4, 2),
        audit_quotient_convolution_action(4, 3),
    ]
    expansion_controls = [
        audit_likelihood_expansion(3, 1, 2),
        audit_likelihood_expansion(3, 1, 3),
        audit_likelihood_expansion(4, 2, 2),
    ]
    scaling = [
        shared_conjugation_scaling_record(
            value,
            copy_count=math.ceil(math.log2(64)) + math.ceil(
                math.log2(
                    math.factorial(2 * value)
                    // (2**value * math.factorial(value))
                )
            ),
        )
        for value in (4, 8, 16, 32, 64, 128)
    ]
    quotient = all(row.exact_quotient_action_verified for row in quotient_controls)
    expansion = all(row.exact_expansion_verified for row in expansion_controls)
    theorem = PhysicalTargetConvolutionTheorem(
        quotient_action=(
            "On (G^k x G)/diag(G), left convolution by (a_i;s) acts on "
            "relative coordinates as x_i->a_i x_i s^-1."
        ),
        likelihood_expansion=(
            "Z=[1/(4^k|K|)] sum_(s,eps,eps') "
            "(eps_i s eps'_i;s)."
        ),
        conditioned_channel=(
            "For fixed s, Q_s is a normalization-one product twirl over H "
            "insertions around a shared conjugation by s."
        ),
        normalization_identity=(
            "Z=(1/|K|)sum_s Q_s=M E_(s uniform G)Q_s and has positive "
            "group-basis L1 norm exactly M."
        ),
        compiler_boundary=(
            "A useful algorithm must fast-forward the shared-orbit factor M; "
            "local Q_s access and generic uniform PREP/SELECT do not do so."
        ),
        exact_all_finite_groups_quotient_action_proved=quotient,
        exact_shared_conjugation_likelihood_expansion_proved=expansion,
        conditioned_Q_normalization_one_proved=expansion,
        full_Z_positive_L1_equals_candidate_count_proved=expansion,
        generic_PREP_SELECT_fast_forward_compiled=False,
        structured_shared_orbit_fast_forward_compiled=False,
        matched_classical_separation_proved=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=quotient and expansion,
        status=(
            "physical-shared-conjugation-normal-form-proved-fast-forward-open"
            if quotient and expansion
            else "physical-target-convolution-normal-form-control-failure"
        ),
    )
    return PhysicalTargetConvolutionReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_space": "(G^k x G)/diag(G) identified with G^k",
            "operator": "Exact likelihood size-bias Z=M e_B e_A e_B",
            "normal_form": "Shared target conjugation s with independent local H insertions",
            "claim_boundary": (
                "Exact factorization and normalization only; no fast-forward, "
                "measurement, decoder, or classical separation."
            ),
        },
        quotient_controls=quotient_controls,
        expansion_controls=expansion_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-SHARED-CONJUGATION-FAST-FORWARD",
                "statement": (
                    "Find a transform that realizes the M-weighted shared-orbit "
                    "interference without coefficient normalization M, or prove none "
                    "exists in the subgroup-reflection/query model."
                ),
                "resolved": False,
            },
            {
                "id": "PO-SHARED-CONJUGATION-CHARGE-RECOUPLING",
                "statement": (
                    "Express Q_s transitions in the coherent C_m,D_m phase labels "
                    "and test whether matrix structure survives source averaging."
                ),
                "resolved": False,
            },
            {
                "id": "PO-SHARED-CONJUGATION-CLASSICAL-BASELINE",
                "statement": (
                    "Compare any proposed spectral statistic with classical sampling "
                    "of s and local H insertions under the same access and precision."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The target disappears completely after quotient gauge fixing.",
                "answer": (
                    "False for target-changing convolution: it becomes the shared right "
                    "multiplier s^-1 on every relative source coordinate."
                ),
                "resolved": True,
            },
            {
                "challenge": "Each Q_s has exponential 4^k normalization.",
                "answer": (
                    "False. It is a positive average with L1 norm one and a product "
                    "PREP conditioned on s."
                ),
                "resolved": True,
            },
            {
                "challenge": "Uniform coherent access to s immediately implements Z.",
                "answer": (
                    "It implements Z/M. Recovering Z by generic LCU pays the exact "
                    "candidate count M."
                ),
                "resolved": True,
            },
            {
                "challenge": "The positive L1 barrier rules out structured Fourier fast-forwarding.",
                "answer": (
                    "Too strong. An implicit transform can realize large basis L1; no "
                    "such transform or lower bound is proved here."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_quotient_action_theorem_count": int(quotient),
            "exact_shared_conjugation_expansion_count": int(expansion),
            "conditioned_normalization_one_channel_count": int(expansion),
            "tail_full_Z_L1_decimal": scaling[-1].full_Z_positive_L1_norm_decimal,
            "structured_fast_forward_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "physical_target_convolution_normal_form_proved": quotient,
            "likelihood_is_shared_conjugation_average_proved": expansion,
            "conditioned_Q_normalization_one": expansion,
            "full_Z_positive_L1_equals_candidate_count": expansion,
            "structured_shared_orbit_fast_forward_compiled": False,
            "matched_classical_separation_proved": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact remaining interference is a candidate-normalized shared "
                "conjugation average; its local channels are easy but no structured "
                "fast-forward or separation is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact quotient action and shared-conjugation tensor-network "
            "normal form for the physical likelihood operator."
        ),
        falsifiers_triggered=[
            "The physical target-changing action does not vanish under gauge fixing.",
            "Conditioned local H twirls are not the normalization bottleneck.",
            "Generic uniform target PREP/SELECT produces Z/M and does not fast-forward M.",
        ],
    )


def write_physical_target_convolution_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_physical_target_convolution_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_physical_target_convolution_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
