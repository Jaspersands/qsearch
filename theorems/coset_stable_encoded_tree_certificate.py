"""Complete encoded coupling-tree labels for the stable final-xi branch.

The stable shape router, first-stage gap certificate, and seven second-stage
gap certificates can be composed without a dense Clebsch transform.  All
observables act directly on W_n^tensor3:

* pair central class sums label the intermediate shape eta;
* a pair commutant Hamiltonian labels g(W_n,W_n,eta);
* an equivariant pair/third-factor Hamiltonian labels g(eta,W_n,xi_n).

The first-stage Hamiltonian commutes with every diagonal pair action.  The
second-stage Hamiltonian is a sum of those diagonal pair actions tensored with
third-factor actions.  Hence all three layers commute, and their joint labels
have exactly sum_eta g(W,W,eta)g(eta,W,xi)=25 values.

Mirroring factors gives right-tree labels.  U_R U_L^dagger is therefore a
polynomial coherent transition between the two *encoded label interfaces*.
The physical multiplicity state remains in W_n^tensor3, so this is not a
compressed 25-dimensional Racah matrix, transition filter, or decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import transposition_matrix
from coset_multiplicity_commutant_search import (
    _oriented_three_cycles,
    transposition_three_cycle_intersection_operator,
)
from coset_stable_first_stage_label_certificate import (
    build_stable_first_stage_label_certificate,
)
from coset_stable_shape_coherent_label_certificate import (
    build_stable_shape_coherent_label_certificate,
)
from coset_stable_shape_family_certificate import (
    build_stable_shape_family_certificate,
)
from coset_stable_shape_router_certificate import (
    build_stable_shape_router_certificate,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_ENCODED_TREE_PATH = Path(
    "research/representation/coset_stable_encoded_tree_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EncodedBranchLabelRecord:
    intermediate_tail: tuple[int, ...]
    padded_partition: str
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    joint_multiplicity_label_count: int
    shape_label_proved: bool
    first_stage_label_proved: bool
    second_stage_label_proved: bool
    complete_joint_branch_label_proved: bool
    status: str


@dataclass(frozen=True)
class EncodedOperatorCommutationAudit:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    triple_dimension: int
    operator_names: tuple[str, ...]
    pairwise_commutator_count: int
    maximum_normalized_commutator_residual: float
    first_stage_orbit_term_count: int
    second_stage_orbit_term_count: int
    numerical_identity_check_passed: bool
    finite_control_only: bool


@dataclass(frozen=True)
class StableEncodedTreeCertificate:
    created_at: str
    theorem: dict[str, object]
    branch_records: list[EncodedBranchLabelRecord]
    algebraic_commutation_certificate: dict[str, object]
    finite_commutation_audit: EncodedOperatorCommutationAudit
    left_tree_circuit_contract: dict[str, object]
    encoded_transition_contract: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=1)
def finite_encoded_operator_commutation_audit(
    n: int = 5,
) -> EncodedOperatorCommutationAudit:
    if n != 5:
        raise ValueError("the lightweight finite commutation control is pinned to n=5")
    source = (n - 2, 2)
    dimension = len(transposition_matrix(source, 1, 2))
    transpositions = [
        transposition_matrix(source, left, right)
        for left, right in itertools.combinations(range(1, n + 1), 2)
    ]
    pair_transposition_class = sum(
        (np.kron(matrix, matrix) for matrix in transpositions),
        np.zeros((dimension * dimension, dimension * dimension)),
    )
    cycles = [matrix for _, matrix in _oriented_three_cycles(source)]
    pair_three_cycle_class = sum(
        (np.kron(matrix, matrix) for matrix in cycles),
        np.zeros((dimension * dimension, dimension * dimension)),
    )
    first_stage, first_term_count = (
        transposition_three_cycle_intersection_operator(source, source, 2)
    )
    second_stage = np.zeros((dimension**3, dimension**3))
    second_term_count = 0
    for triple in itertools.combinations(range(1, n + 1), 3):
        first, second, third = triple
        forward_cycle = (
            transposition_matrix(source, first, second)
            @ transposition_matrix(source, second, third)
        )
        for transposition_support in itertools.combinations(triple, 2):
            transposition = transposition_matrix(
                source, *transposition_support
            )
            diagonal_pair = np.kron(transposition, transposition)
            for cycle in (forward_cycle, forward_cycle.T):
                second_stage += np.kron(diagonal_pair, cycle)
                second_term_count += 1
    identity = np.eye(dimension)
    names = (
        "pair-transposition-class",
        "pair-three-cycle-class",
        "first-stage-commutant",
        "second-stage-equivariant-orbit",
    )
    operators = (
        np.kron(pair_transposition_class, identity),
        np.kron(pair_three_cycle_class, identity),
        np.kron(first_stage, identity),
        second_stage,
    )
    residuals = []
    for left in range(len(operators)):
        for right in range(left + 1, len(operators)):
            denominator = max(
                1.0,
                float(np.linalg.norm(operators[left]))
                * float(np.linalg.norm(operators[right])),
            )
            residuals.append(
                float(
                    np.linalg.norm(
                        operators[left] @ operators[right]
                        - operators[right] @ operators[left]
                    )
                    / denominator
                )
            )
    maximum_residual = max(residuals, default=math.inf)
    return EncodedOperatorCommutationAudit(
        n=n,
        source_partition=source,
        source_dimension=dimension,
        triple_dimension=dimension**3,
        operator_names=names,
        pairwise_commutator_count=len(residuals),
        maximum_normalized_commutator_residual=maximum_residual,
        first_stage_orbit_term_count=first_term_count,
        second_stage_orbit_term_count=second_term_count,
        numerical_identity_check_passed=maximum_residual < 1e-12,
        finite_control_only=True,
    )


@lru_cache(maxsize=1)
def build_stable_encoded_tree_certificate() -> StableEncodedTreeCertificate:
    family = build_stable_shape_family_certificate()
    router = build_stable_shape_router_certificate()
    first_stage = build_stable_first_stage_label_certificate()
    second_stage = build_stable_shape_coherent_label_certificate()
    audit = finite_encoded_operator_commutation_audit()

    router_proved = bool(
        router.claim_gate["coherent_encoded_intermediate_shape_router_proved"]
    )
    first_stage_proved = bool(
        first_stage.claim_gate["all_stable_first_stage_multiplicity_labels_proved"]
    )
    second_stage_by_tail = {
        tuple(record.intermediate_tail): (
            record.coherent_phase_estimation_label_proved
        )
        for record in second_stage.shape_records
    }
    branch_records: list[EncodedBranchLabelRecord] = []
    for record in family.shape_records:
        tail = tuple(record.tail)
        first_label = record.first_stage_multiplicity == 1 or first_stage_proved
        second_label = (
            record.second_stage_multiplicity == 1
            or second_stage_by_tail.get(tail, False)
        )
        complete = router_proved and first_label and second_label
        branch_records.append(
            EncodedBranchLabelRecord(
                intermediate_tail=tail,
                padded_partition=record.padded_partition,
                first_stage_multiplicity=record.first_stage_multiplicity,
                second_stage_multiplicity=record.second_stage_multiplicity,
                joint_multiplicity_label_count=record.branch_dimension,
                shape_label_proved=router_proved,
                first_stage_label_proved=first_label,
                second_stage_label_proved=second_label,
                complete_joint_branch_label_proved=complete,
                status=(
                    "complete-encoded-branch-label-proved"
                    if complete
                    else "encoded-branch-label-incomplete"
                ),
            )
        )

    joint_label_count = sum(
        record.joint_multiplicity_label_count for record in branch_records
    )
    complete_branch_count = sum(
        record.complete_joint_branch_label_proved for record in branch_records
    )
    source_total = int(family.theorem["final_total_multiplicity"])
    all_labels_complete = (
        bool(family.theorem["proved"])
        and complete_branch_count == 9
        and joint_label_count == source_total == 25
        and audit.numerical_identity_check_passed
    )
    left_transform_proved = all_labels_complete
    right_transform_proved = left_transform_proved
    encoded_transition_proved = left_transform_proved and right_transform_proved
    maximum_query_exponent = max(
        int(
            second_stage.headline_metrics[
                "maximum_phase_estimation_query_exponent"
            ]
        ),
        int(
            first_stage.headline_metrics[
                "maximum_normalized_gap_inverse_polynomial_exponent"
            ]
        ),
        int(router.headline_metrics["maximum_lcu_term_exponent"]),
    )
    metrics: dict[str, int | float] = {
        "stable_branch_count": len(branch_records),
        "complete_joint_branch_label_count": complete_branch_count,
        "joint_multiplicity_label_count": joint_label_count,
        "final_multiplicity_dimension": source_total,
        "coherent_shape_router_count": int(router_proved),
        "coherent_first_stage_label_transform_count": int(first_stage_proved),
        "coherent_second_stage_nontrivial_shape_label_count": sum(
            bool(value) for value in second_stage_by_tail.values()
        ),
        "complete_encoded_left_tree_label_transform_count": int(
            left_transform_proved
        ),
        "complete_encoded_right_tree_label_transform_count": int(
            right_transform_proved
        ),
        "encoded_coupling_tree_transition_isometry_count": int(
            encoded_transition_proved
        ),
        "compressed_clebsch_transform_count": 0,
        "compressed_racah_associator_count": 0,
        "transition_filter_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_phase_estimation_query_exponent": maximum_query_exponent,
        "finite_commutation_audit_pair_count": audit.pairwise_commutator_count,
        "maximum_finite_normalized_commutator_residual": (
            audit.maximum_normalized_commutator_residual
        ),
    }
    return StableEncodedTreeCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "statement": (
                "On the final xi_n isotypic branch of W_n^tensor3, commuting shape, first-stage multiplicity, and "
                "second-stage multiplicity observables provide exactly 25 coherent joint labels, one for every "
                "left-coupled multiplicity line. The mirrored construction gives the right-coupled labels."
            ),
            "proved": all_labels_complete,
        },
        branch_records=branch_records,
        algebraic_commutation_certificate={
            "pair_shape_centrality": (
                "C_2^(12) and C_3^(12) are central in the diagonal pair representation and commute with pair commutants."
            ),
            "first_second_stage_commutation": (
                "K_12 lies in End_Sn(W tensor W), while K_(12),3 is a sum of D_12(tau) tensor rho_W(c); "
                "therefore [K_12,K_(12),3]=0 term by term."
            ),
            "final_irrep_preservation": (
                "Every orbit sum is invariant under total simultaneous conjugation and commutes with the final-xi projector."
            ),
            "encoded_second_stage_realization": (
                "On the eta isotypic block, D_12(tau) acts as rho_eta(tau) tensor I_first, so one global triple-register "
                "operator restricts to every certified H_eta tensor I_first without constructing an eta register."
            ),
            "joint_label_count_identity": (
                "sum_eta g(W,W,eta)g(eta,W,xi)=25=dim Hom_Sn(xi,W^tensor3)"
            ),
            "proved": all_labels_complete,
        },
        finite_commutation_audit=audit,
        left_tree_circuit_contract={
            "input": "W_n^tensor3 conditioned on the final xi_n irrep label",
            "steps": [
                "append pair central signature (C_2^(12),C_3^(12)) and decode eta",
                "append the K_12 first-stage multiplicity eigenlabel",
                "append the K_(12),3 second-stage multiplicity eigenlabel",
            ],
            "output_label": "(eta, first multiplicity index, second multiplicity index)",
            "joint_label_count": 25,
            "physical_state_encoding": "unchanged W_n^tensor3 registers",
            "maximum_inverse_gap_exponent": maximum_query_exponent,
            "complexity": "polynomial in n and log(1/error)",
            "dense_clebsch_or_racah_table_used": False,
        },
        encoded_transition_contract={
            "left_label_unitary": "U_L appends the complete (12)3 joint label",
            "right_label_unitary": (
                "U_R is the factor-permuted construction appending the 1(23) joint label"
            ),
            "transition": "T_encoded=U_R U_L^dagger on valid left-labelled encoded states",
            "transition_preserves_physical_state": True,
            "transition_error": (
                "inverse polynomial after choosing each phase-estimation precision below one third of its proved gap"
            ),
            "polynomial_encoded_transition_label_isometry_proved": (
                encoded_transition_proved
            ),
            "compressed_25_by_25_racah_unitary_produced": False,
            "transition_amplitude_table_materialized": False,
            "state_dependent_transition_filter_implemented": False,
        },
        headline_metrics=metrics,
        claim_gate={
            "complete_encoded_left_tree_joint_labels_proved": left_transform_proved,
            "complete_encoded_right_tree_joint_labels_proved": right_transform_proved,
            "encoded_coupling_tree_transition_label_isometry_proved": (
                encoded_transition_proved
            ),
            "compressed_internal_kronecker_transform_proved": False,
            "compressed_racah_associator_proved": False,
            "state_dependent_transition_filter_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_superpolynomial_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The stable final branch now has complete coherent left/right labels and an encoded relabelling "
                "isometry, but no compressed Racah matrix, state-dependent frame filter, hidden-involution decoder, "
                "source-family coverage theorem, or classical separation."
            ),
        },
        status=(
            "complete-stable-encoded-tree-labels-and-transition-proved-filter-decoder-open"
            if encoded_transition_proved
            else "stable-encoded-tree-certificate-failed"
        ),
        summary=(
            "Composed exact shape, first-stage, and second-stage observables into 25 complete coherent labels on both "
            "stable coupling trees and a polynomial encoded transition-label isometry; filtering and decoding remain open."
        ),
        falsifiers_triggered=[
            "The three observable layers must commute; the finite operator audit would reject an incorrect composition.",
            "The sum of branch label products must equal the exact final multiplicity 25.",
            "An encoded label transition is not a standalone compressed 25x25 Racah matrix.",
            "No state-dependent transition filter or hidden-involution information follows from basis labels alone.",
            "A result conditioned on one stable source/final branch is not full symmetric-HSP sector coverage.",
        ],
    )


def write_stable_encoded_tree_certificate(
    output_path: Path = COSET_STABLE_ENCODED_TREE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_encoded_tree_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-ENCODED-TREE-LABELS-AS-COMPLETE-HSP-DECODER",
                source=str(output_path),
                claim=(
                    "Complete coherent coupling-tree labels on one stable branch already implement the hidden-involution decoder."
                ),
                reason_invalid=(
                    "The construction exposes a basis interface but no state-dependent transition filter, outcome "
                    "information theorem, full-sector coverage, or classical separation."
                ),
                lesson=(
                    "Use the encoded transition to formulate and test scalable frame/measurement operators, then kill "
                    "any signal with legal classical representation baselines before promoting it."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "coset_stable_encoded_tree_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_encoded_tree_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
