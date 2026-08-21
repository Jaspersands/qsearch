"""Faithful matching-charge orbit and target-recoupling reduction.

Let ``h`` be the reference fixed-point-free involution in ``S_(2m)`` and
``K=C_G(h)``.  The normalized disjoint matching charge ``D_h`` is invariant
under conjugation by ``K``.  This module proves that its full conjugation
stabilizer is *exactly* ``K`` for every ``m>=4``.

The proof is elementary.  The unnormalized charge contains 192 terms on each
four-set of matched pair labels, and every term touches all four pairs.  A
fixed eight-point term has the property that conjugation by the cross-pair
transposition ``(1 2)`` touches only three reference pairs, so the conjugated
term is absent from ``D_h``.  Thus ``D_h`` is not central in ``C[S_(2m)]``.

The perfect-matching stabilizer ``K`` is maximal.  If a subgroup containing
``K`` contains ``y notin K``, then some matched pair is sent across two
different matched pairs.  Conjugating that pair's internal transposition by
``y`` supplies a cross-pair transposition.  Its ``K`` conjugates are all
``4*binomial(m,2)`` cross-pair transpositions, while ``K`` already contains
all ``m`` within-pair transpositions.  These are every transposition in
``S_(2m)``, so ``<K,y>=S_(2m)``.  A stabilizer strictly larger than ``K``
would therefore make ``D_h`` central, contradicting the explicit witness.

Consequently

    tK  ->  D_(t h t^-1) = t D_h t^-1

is an injective, equivariant encoding of all ``M=(2m)!/(2^m m!)`` hidden
matchings.  The coherent sparse-LCU compiler extends uniformly to this orbit:
given a target permutation ``t``, conjugate every indexed constant-support
term before SELECT.  The block-encoding normalization remains one.

This identifies a candidate-indexed recoupling object, but the conjugator
``t`` here is an explicitly supplied external register.  The physical
``L/A`` target coordinate is only a gauge representative; the target-gauge
trivialization theorem proves that using it as a diagonal conjugation control
reduces to a source-local likelihood-blind action.  A physical target-coupled
detector must genuinely change the target coordinate.  This theorem proves
faithful covariance and external coherent access, not physical target access,
a useful transition gap, source-aware normalization, decoder, or speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
    involution_class_size,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    _K_generators,
)
from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    matching_charge_term_count,
    matching_charge_term_from_index,
)
from coset_hidden_involution_matching_charge_natural_independence import (
    _moved_pair_support,
)
from coset_hidden_involution_pair_gaudin_hierarchy import _commutator
from coset_hidden_involution_pair_matching_charge_hierarchy import (
    GroupAlgebraElement,
    Permutation,
    disjoint_matching_charge,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_orbit_recoupling_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-ORBIT-RECOUPLING-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

_LOCAL_WITNESS: Permutation = (0, 4, 2, 6, 5, 1, 7, 3)
_LOCAL_CROSS_CONJUGATE: Permutation = (0, 1, 4, 6, 5, 2, 7, 3)


@dataclass(frozen=True)
class ChargeStabilizerControl:
    half_degree: int
    matching_charge_term_count: int
    K_generator_count: int
    K_conjugation_failure_count: int
    cross_transposition: Permutation
    witness_term: Permutation
    witness_coefficient_before_conjugation: int
    witness_conjugate: Permutation
    witness_conjugate_coefficient: int
    witness_pair_support_before: int
    witness_pair_support_after: int
    charge_is_K_invariant: bool
    charge_is_G_central: bool
    maximality_cross_transposition_count: int
    maximality_total_transposition_count: int
    exact_stabilizer_is_K_proved: bool
    status: str


@dataclass(frozen=True)
class ChargeOrbitScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count: int
    hidden_matching_label_bits: float
    matching_charge_term_count: int
    term_index_bits: int
    orbit_stabilizer_order: int
    orbit_size_equals_hidden_matching_count: bool
    controlled_conjugated_block_encoding_normalization: float
    status: str


@dataclass(frozen=True)
class ChargeOrbitRecouplingTheorem:
    stabilizer: str
    maximality_proof: str
    covariant_orbit: str
    controlled_access: str
    physical_reduction: str
    exact_all_rank_charge_stabilizer_proved: bool
    hidden_matching_to_charge_orbit_injective: bool
    normalization_one_controlled_orbit_access_compiled: bool
    charge_orbit_is_a_faithful_candidate_coordinate: bool
    useful_cross_charge_transition_gap_proved: bool
    source_aware_transition_mass_proved: bool
    all_copy_target_recoupling_compiled: bool
    standalone_charge_detector_constructed: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ChargeOrbitRecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    stabilizer_controls: list[ChargeStabilizerControl]
    scaling_records: list[ChargeOrbitScalingRecord]
    theorem: ChargeOrbitRecouplingTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def reference_hidden_involution(half_degree: int) -> Permutation:
    output = list(range(2 * half_degree))
    for pair in range(half_degree):
        output[2 * pair], output[2 * pair + 1] = 2 * pair + 1, 2 * pair
    return tuple(output)


def cross_pair_transposition(half_degree: int) -> Permutation:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    output = list(range(2 * half_degree))
    output[1], output[2] = output[2], output[1]
    return tuple(output)


def embed_local_permutation(
    local: Permutation,
    half_degree: int,
) -> Permutation:
    if len(local) != 8 or half_degree < 4:
        raise ValueError("require an eight-point local permutation and m>=4")
    output = list(range(2 * half_degree))
    output[:8] = local
    return tuple(output)


def conjugate_permutation(
    conjugator: Permutation,
    permutation: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(conjugator, permutation),
        inverse_permutation(conjugator),
    )


def conjugate_group_algebra_element(
    conjugator: Permutation,
    element: GroupAlgebraElement,
) -> GroupAlgebraElement:
    return {
        conjugate_permutation(conjugator, permutation): coefficient
        for permutation, coefficient in element.items()
    }


def conjugated_matching_charge_term_from_index(
    half_degree: int,
    conjugator: Permutation,
    term_index: int,
) -> Permutation:
    if len(conjugator) != 2 * half_degree:
        raise ValueError("conjugator degree does not match half_degree")
    return conjugate_permutation(
        conjugator,
        matching_charge_term_from_index(half_degree, term_index),
    )


def audit_charge_stabilizer(half_degree: int) -> ChargeStabilizerControl:
    if not 4 <= half_degree <= 7:
        raise ValueError("dense stabilizer audit is limited to 4<=m<=7")
    charge = disjoint_matching_charge(half_degree)
    generators = _K_generators(half_degree)
    K_failures = sum(
        bool(_commutator(charge, {generator: 1})) for generator in generators
    )
    cross = cross_pair_transposition(half_degree)
    witness = embed_local_permutation(_LOCAL_WITNESS, half_degree)
    witness_conjugate = conjugate_permutation(cross, witness)
    expected_conjugate = embed_local_permutation(
        _LOCAL_CROSS_CONJUGATE,
        half_degree,
    )
    cross_count = 4 * math.comb(half_degree, 2)
    total_transpositions = math.comb(2 * half_degree, 2)
    exact = bool(
        K_failures == 0
        and charge.get(witness, 0) == 1
        and witness_conjugate == expected_conjugate
        and charge.get(witness_conjugate, 0) == 0
        and _moved_pair_support(witness) == 4
        and _moved_pair_support(witness_conjugate) == 3
        and half_degree + cross_count == total_transpositions
    )
    return ChargeStabilizerControl(
        half_degree=half_degree,
        matching_charge_term_count=len(charge),
        K_generator_count=len(generators),
        K_conjugation_failure_count=K_failures,
        cross_transposition=cross,
        witness_term=witness,
        witness_coefficient_before_conjugation=charge.get(witness, 0),
        witness_conjugate=witness_conjugate,
        witness_conjugate_coefficient=charge.get(witness_conjugate, 0),
        witness_pair_support_before=_moved_pair_support(witness),
        witness_pair_support_after=_moved_pair_support(witness_conjugate),
        charge_is_K_invariant=K_failures == 0,
        charge_is_G_central=False,
        maximality_cross_transposition_count=cross_count,
        maximality_total_transposition_count=total_transpositions,
        exact_stabilizer_is_K_proved=exact,
        status=(
            "matching-charge-conjugation-stabilizer-exactly-K"
            if exact
            else "matching-charge-stabilizer-control-failure"
        ),
    )


def charge_orbit_scaling_record(half_degree: int) -> ChargeOrbitScalingRecord:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    degree = 2 * half_degree
    matching_count = involution_class_size(degree, half_degree)
    stabilizer_order = 2**half_degree * math.factorial(half_degree)
    orbit_size = math.factorial(degree) // stabilizer_order
    terms = matching_charge_term_count(half_degree)
    return ChargeOrbitScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count=matching_count,
        hidden_matching_label_bits=math.log2(matching_count),
        matching_charge_term_count=terms,
        term_index_bits=math.ceil(math.log2(terms)),
        orbit_stabilizer_order=stabilizer_order,
        orbit_size_equals_hidden_matching_count=orbit_size == matching_count,
        controlled_conjugated_block_encoding_normalization=1.0,
        status="faithful-hidden-matching-charge-orbit-scaling",
    )


def build_charge_orbit_recoupling_report() -> ChargeOrbitRecouplingReport:
    controls = [audit_charge_stabilizer(value) for value in (4, 5, 6)]
    scaling = [
        charge_orbit_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    stabilizer = all(row.exact_stabilizer_is_K_proved for row in controls)
    orbit = all(row.orbit_size_equals_hidden_matching_count for row in scaling)
    theorem = ChargeOrbitRecouplingTheorem(
        stabilizer=(
            "Stab_G(D_h)=K=C_G(h) for every m>=4: K invariance, one "
            "all-rank noncentral witness, and maximality of the matching stabilizer."
        ),
        maximality_proof=(
            "Any y outside K conjugates a within-pair transposition to a cross-pair "
            "one; K conjugates then supply every transposition and generate S_(2m)."
        ),
        covariant_orbit=(
            "The map tK -> D_(t h t^-1)=tD_ht^-1 is injective and its orbit "
            "has exactly (2m)!/(2^m m!) elements."
        ),
        controlled_access=(
            "Given an external coherent candidate permutation, conjugating each "
            "indexed D_h term gives normalization-one access to the full charge orbit."
        ),
        physical_reduction=(
            "An external-candidate transition can compare D_h and D_(t h t^-1); "
            "the physical quotient target cannot supply t as a diagonal control."
        ),
        exact_all_rank_charge_stabilizer_proved=stabilizer,
        hidden_matching_to_charge_orbit_injective=stabilizer and orbit,
        normalization_one_controlled_orbit_access_compiled=stabilizer and orbit,
        charge_orbit_is_a_faithful_candidate_coordinate=stabilizer and orbit,
        useful_cross_charge_transition_gap_proved=False,
        source_aware_transition_mass_proved=False,
        all_copy_target_recoupling_compiled=False,
        standalone_charge_detector_constructed=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=stabilizer and orbit,
        status=(
            "faithful-matching-charge-orbit-proved-transition-kernel-open"
            if stabilizer and orbit
            else "matching-charge-orbit-reduction-control-failure"
        ),
    )
    return ChargeOrbitRecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "group_pair": "S_(2m) >= C_2 wr S_m",
            "charge": "Normalized K-conjugation-invariant disjoint matching charge D_h",
            "candidate_parameter": "Right coset tK, equivalently hidden involution t h t^-1",
            "claim_boundary": (
                "Faithful covariant encoding and external candidate access only; "
                "no physical quotient-target control, useful transition, or detector."
            ),
        },
        stabilizer_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-MATCHING-CHARGE-CROSS-TRANSITION-KERNEL",
                "statement": (
                    "Derive the source-weighted transition kernel between spectral "
                    "projectors of D_h and D_(t h t^-1), stratified by K double coset."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-CROSS-TRANSITION-GAP",
                "statement": (
                    "Prove an inverse-polynomial useful transition singular-value "
                    "gap on natural all-copy target-coupled source mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-CROSS-TRANSITION-DEQUANTIZATION",
                "statement": (
                    "Compare any transition statistic with the best classical "
                    "matching-overlap and character-polynomial baselines."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Different hidden matchings may define the same D charge.",
                "answer": (
                    "False. The charge stabilizer is exactly K, so equality of "
                    "conjugated charges is equivalent to equality of tK."
                ),
                "resolved": True,
            },
            {
                "challenge": "K maximality is being assumed without a generator proof.",
                "answer": (
                    "The proof is explicit: one outside element yields a cross-pair "
                    "transposition, whose K orbit plus within-pair swaps is the full "
                    "set of transpositions."
                ),
                "resolved": True,
            },
            {
                "challenge": "Faithful charge covariance gives a detector.",
                "answer": (
                    "False. Candidate injectivity says nothing about source overlap, "
                    "normalization, or outcome distinguishability."
                ),
                "resolved": True,
            },
            {
                "challenge": "The scalar cross-Hecke no-go already rules out this route.",
                "answer": (
                    "Too strong. That theorem covers normalized scalar/mixed word LCUs; "
                    "the matrix-valued cross-charge spectral transition remains open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_all_rank_charge_stabilizer_theorem_count": int(stabilizer),
            "faithful_hidden_matching_charge_orbit_count": int(stabilizer and orbit),
            "tail_hidden_matching_count_decimal": str(scaling[-1].hidden_matching_count),
            "tail_hidden_matching_label_bits": scaling[-1].hidden_matching_label_bits,
            "normalization_one_controlled_orbit_access_count": int(stabilizer and orbit),
            "useful_transition_kernel_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "charge_stabilizer_exactly_K_proved": stabilizer,
            "hidden_matching_charge_orbit_injective": stabilizer and orbit,
            "normalization_one_controlled_charge_access_compiled": stabilizer and orbit,
            "physical_A_quotient_target_control_compiled": False,
            "useful_cross_charge_transition_gap_proved": False,
            "source_aware_transition_mass_proved": False,
            "all_copy_target_recoupling_compiled": False,
            "standalone_charge_measurement_likelihood_blind": True,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "D_h is a faithful coherently accessible coordinate for the hidden "
                "matching orbit, but only an unproved cross-charge transition can "
                "couple it to the likelihood."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the matching-charge conjugation orbit is exactly the hidden-"
            "involution candidate space and reduced the positive route to cross-charge recoupling."
        ),
        falsifiers_triggered=[
            "The natural matching charge is not invariant under a larger subgroup than K.",
            "Distinct hidden perfect matchings cannot collapse to the same conjugated D charge.",
            "Faithful covariance alone does not evade source-local likelihood blindness.",
        ],
    )


def write_charge_orbit_recoupling_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_charge_orbit_recoupling_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_charge_orbit_recoupling_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
