"""The even collision core is pure block dependence, not marginal failure.

For any group, define

    F(g,h,k)=(a,b,c)=(gk,hk,ghk).

This map is bijective.  With multiplication written by juxtaposition, its
inverse is

    k=b c^-1 a,
    g=c b^-1,
    h=b a^-1 c b^-1.                                    (1)

It preserves ``A_n^3``.  Thus if ``g,h,k`` are independent uniform even
permutations, then ``a,b,c`` are also independent uniform even permutations.
Every individual input permutation is independent of every individual output
permutation as well.  Passing to cycle types preserves these facts.

Let ``X=(type(g),type(h),type(k))`` and
``Y=(type(gk),type(hk),type(ghk))``.  Both ``X`` and ``Y`` have the same
three-fold product law ``q^3``, and all six scalar coordinates are pairwise
independent.  Nevertheless the blocks can have higher-order dependence.  The
even collision moment is exactly

    C_even = 1 + chi2(P_(X,Y) || q^3 tensor q^3).         (2)

Therefore every one-product or pairwise cycle-mixing theorem is structurally
insufficient.  The missing estimate is a joint three-output conditional
collision theorem.

There is also a crucial Fourier boundary.  Equation (2) equals the likelihood
second moment of the coarse ``A_n`` irrep-label law by character
orthogonality.  Shannon relative entropy is not preserved by that orthogonal
transform: classical cycle-type mutual information ``I(X;Y)`` need not equal
the coarse label KL.  Direct classical Shannon estimates cannot be silently
substituted for the label-entropy gate; the exact classical dual currently
exists only at Renyi order two.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
)
from self_dual_wreath_character_moments import (
    compose_permutations,
)
from self_dual_wreath_projected_parity_coset_kernel import (
    full_parity_class_collision_energy,
    parity_coset_signature_counts,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_cycle_type_block_dependence.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-CYCLE-TYPE-BLOCK-DEPENDENCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
Partition = tuple[int, ...]


@dataclass(frozen=True)
class CycleTypeBlockDependenceControl:
    n: int
    alternating_group_order: int
    occupied_joint_signature_count: int
    maximum_one_coordinate_marginal_residual: str
    maximum_pairwise_independence_residual: str
    exact_cycle_type_collision_moment: str
    exact_even_collision_moment: str
    collision_duality_residual: str
    classical_cycle_type_mutual_information_bits: float
    coarse_irrep_label_kl_bits: float
    shannon_duality_residual_bits: float
    shannon_information_preserved_by_fourier_transform: bool
    exact_block_dependence_structure_verified: bool
    status: str


@dataclass(frozen=True)
class BlockDependenceTheorem:
    output_map: str
    inverse_map: str
    input_output_block_marginals: str
    scalar_coordinate_dependence: str
    collision_identity: str
    shannon_fourier_duality: bool
    joint_block_mixing_proved: bool
    status: str


@dataclass(frozen=True)
class AlternatingCycleTypeBlockDependenceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: BlockDependenceTheorem
    exact_controls: list[CycleTypeBlockDependenceControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def output_word_map(
    g: Permutation,
    h: Permutation,
    k: Permutation,
) -> tuple[Permutation, Permutation, Permutation]:
    gh = compose_permutations(g, h)
    return (
        compose_permutations(g, k),
        compose_permutations(h, k),
        compose_permutations(gh, k),
    )


def inverse_output_word_map(
    a: Permutation,
    b: Permutation,
    c: Permutation,
) -> tuple[Permutation, Permutation, Permutation]:
    if not (len(a) == len(b) == len(c)):
        raise ValueError("permutations must have equal degree")
    inverse_a = inverse_permutation(a)
    inverse_b = inverse_permutation(b)
    inverse_c = inverse_permutation(c)
    k = compose_permutations(compose_permutations(b, inverse_c), a)
    g = compose_permutations(c, inverse_b)
    h = compose_permutations(
        compose_permutations(compose_permutations(b, inverse_a), c),
        inverse_b,
    )
    return g, h, k


def _coarse_even_class_probability(n: int, cycle_type: Partition) -> Fraction:
    order_a = math.factorial(n) // 2
    return Fraction(conjugacy_class_size(cycle_type), order_a)


def audit_cycle_type_block_dependence(n: int) -> CycleTypeBlockDependenceControl:
    if not 2 <= n <= 5:
        raise ValueError("exact block-dependence controls require 2<=n<=5")
    counts = parity_coset_signature_counts(n, (0, 0, 0))
    order_a = math.factorial(n) // 2
    total = order_a**3
    coordinate_counts = [defaultdict(int) for _ in range(6)]
    pair_counts = {
        (left, right): defaultdict(int)
        for left in range(6)
        for right in range(left + 1, 6)
    }
    for signature, count in counts.items():
        for axis, cycle_type in enumerate(signature):
            coordinate_counts[axis][cycle_type] += count
        for pair, rows in pair_counts.items():
            rows[(signature[pair[0]], signature[pair[1]])] += count

    marginal_residual = Fraction()
    all_types = sorted({cycle_type for signature in counts for cycle_type in signature})
    for axis in range(6):
        for cycle_type in all_types:
            observed = Fraction(coordinate_counts[axis][cycle_type], total)
            expected = _coarse_even_class_probability(n, cycle_type)
            marginal_residual = max(marginal_residual, abs(observed - expected))

    pair_residual = Fraction()
    for rows in pair_counts.values():
        for left_type in all_types:
            for right_type in all_types:
                observed = Fraction(rows[(left_type, right_type)], total)
                expected = _coarse_even_class_probability(
                    n, left_type
                ) * _coarse_even_class_probability(n, right_type)
                pair_residual = max(pair_residual, abs(observed - expected))

    collision = Fraction()
    shannon = 0.0
    for signature, count in counts.items():
        probability = Fraction(count, total)
        reference = math.prod(
            _coarse_even_class_probability(n, cycle_type)
            for cycle_type in signature
        )
        collision += probability * probability / reference
        shannon += float(probability) * math.log2(float(probability / reference))
    even_collision = full_parity_class_collision_energy(n, (0, 0, 0))

    _orbits, likelihood, _reference, physical = aggregate_sign_orbit_law(n)
    positive = physical > 0
    label_kl = float(np.sum(physical[positive] * np.log2(likelihood[positive])))
    shannon_residual = abs(shannon - label_kl)
    collision_residual = abs(collision - even_collision)
    shannon_preserved = shannon_residual <= 1e-10
    exact = bool(
        sum(counts.values()) == total
        and marginal_residual == 0
        and pair_residual == 0
        and collision_residual == 0
    )
    return CycleTypeBlockDependenceControl(
        n=n,
        alternating_group_order=order_a,
        occupied_joint_signature_count=len(counts),
        maximum_one_coordinate_marginal_residual=str(marginal_residual),
        maximum_pairwise_independence_residual=str(pair_residual),
        exact_cycle_type_collision_moment=str(collision),
        exact_even_collision_moment=str(even_collision),
        collision_duality_residual=str(collision_residual),
        classical_cycle_type_mutual_information_bits=max(0.0, shannon),
        coarse_irrep_label_kl_bits=max(0.0, label_kl),
        shannon_duality_residual_bits=shannon_residual,
        shannon_information_preserved_by_fourier_transform=shannon_preserved,
        exact_block_dependence_structure_verified=exact,
        status=(
            "cycle-type-blocks-product-marginal-pairwise-independent-with-renyi-dependence"
            if exact
            else "cycle-type-block-dependence-control-failure"
        ),
    )


def run_alternating_cycle_type_block_dependence(
) -> AlternatingCycleTypeBlockDependenceReport:
    controls = [audit_cycle_type_block_dependence(n) for n in range(2, 6)]
    failures = sum(not row.exact_block_dependence_structure_verified for row in controls)
    nonpreserved = sum(
        not row.shannon_information_preserved_by_fourier_transform
        for row in controls
        if n_or_nontrivial(row.n)
    )
    exact = failures == 0 and nonpreserved > 0
    theorem = BlockDependenceTheorem(
        output_map="F(g,h,k)=(gk,hk,ghk)",
        inverse_map="k=bc^-1a, g=cb^-1, h=ba^-1cb^-1",
        input_output_block_marginals=(
            "Both three-coordinate cycle-type blocks have product coarse-even class law"
        ),
        scalar_coordinate_dependence="All fifteen scalar coordinate pairs are independent",
        collision_identity=(
            "C_even=1+chi2(P_(X,Y)||q_even^3 tensor q_even^3)"
        ),
        shannon_fourier_duality=False,
        joint_block_mixing_proved=False,
        status=(
            "even-collision-is-pure-higher-order-input-output-block-dependence"
            if exact
            else "cycle-type-block-dependence-theorem-control-failure"
        ),
    )
    return AlternatingCycleTypeBlockDependenceReport(
        created_at=utc_now(),
        theorem_contract={
            "bijective_word_map": theorem.output_map,
            "inverse": theorem.inverse_map,
            "block_marginals": theorem.input_output_block_marginals,
            "pairwise_independence": theorem.scalar_coordinate_dependence,
            "renyi_two_dependence": theorem.collision_identity,
            "fourier_boundary": (
                "Collision/Renyi-two is dual to the coarse irrep law; Shannon KL is not."
            ),
            "scope": (
                "No joint block collision estimate is proved for growing support."
            ),
        },
        theorem=theorem,
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "identify_output_triple_as_bijective_reparameterization",
                "resolved": exact,
                "resolution": "The explicit inverse in (1) works in every group.",
            },
            {
                "obligation": "remove_all_marginal_and_pairwise_cycle_mixing_questions",
                "resolved": exact,
                "resolution": (
                    "Uniform inputs and the relevant two-coordinate word maps are "
                    "bijective, giving exact pairwise independence."
                ),
            },
            {
                "obligation": "prove_joint_three_output_conditional_collision_mixing",
                "resolved": False,
                "resolution": (
                    "Control P(Y|X) in class-level chi-square jointly; separate "
                    "one-product normal-set mixing theorems are insufficient."
                ),
            },
            {
                "obligation": "bridge_classical_shannon_information_to_label_kl",
                "resolved": False,
                "resolution": (
                    "No Shannon Fourier isometry exists; use Renyi-two, direct label "
                    "entropy, or prove a new comparison under additional regularity."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "One output product may have a biased cycle type.",
                "resolved": True,
                "resolution": "Every output permutation is exactly uniform in A_n.",
            },
            {
                "objection": "Pairwise cycle-type tests can detect the obstruction.",
                "resolved": True,
                "resolution": (
                    "All fifteen coordinate pairs are exactly independent; dependence "
                    "is genuinely block-level synergy."
                ),
            },
            {
                "objection": "Marginal normal-set mixing composes into joint mixing.",
                "resolved": True,
                "resolution": (
                    "The XOR-style possibility of pairwise-independent block synergy "
                    "remains; a joint theorem is required."
                ),
            },
            {
                "objection": "Classical cycle-type mutual information equals label KL.",
                "resolved": True,
                "resolution": (
                    "Finite exact controls falsify Shannon preservation; only the "
                    "quadratic collision norm is preserved by character orthogonality."
                ),
            },
        ],
        headline_metrics={
            "word_map_bijection_theorem_count": int(exact),
            "pairwise_independence_theorem_count": int(exact),
            "renyi_block_dependence_identity_count": int(exact),
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "shannon_fourier_counterexample_count": nonpreserved,
            "joint_block_mixing_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "input_output_word_map_bijection_proved": exact,
            "all_scalar_cycle_type_pairs_independent_proved": exact,
            "even_collision_is_joint_block_renyi_dependence_proved": exact,
            "single_product_mixing_sufficient": False,
            "pairwise_mixing_sufficient": False,
            "shannon_cycle_type_information_equals_label_kl": False,
            "joint_block_collision_subpolynomial_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All marginal questions are exact, but the higher-order joint block "
                "collision on growing support remains open."
            ),
        },
        status=(
            "growing-support-target-is-pure-joint-cycle-type-block-synergy"
            if exact
            else "alternating-cycle-type-block-dependence-failure"
        ),
        summary=(
            "Proved exact product block marginals and pairwise independence, isolating "
            "the even collision core as higher-order input/output cycle-type synergy."
        ),
        falsifiers_triggered=[
            "No single output cycle type or coordinate pair can witness the obstruction.",
            "Separate normal-set product-mixing estimates do not imply joint three-output mixing.",
            "Shannon cycle-type mutual information is not Fourier-dual to coarse irrep-label KL.",
        ],
    )


def n_or_nontrivial(n: int) -> bool:
    return n >= 3


def write_alternating_cycle_type_block_dependence_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_cycle_type_block_dependence())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_cycle_type_block_dependence_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
