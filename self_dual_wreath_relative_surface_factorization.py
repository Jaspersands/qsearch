"""A proof-carrying support-conditioned surface factorization.

The strongest degree-three positive-genus profile in the marked-pressure
search has one residual relation and a nontrivial target boundary.  A free
basis change separates them onto disjoint generator pairs:

    relation -> A [K,C] A^-1,
    target   -> H^-1 A H A^-1.

Thus the relation only requires ``K`` and ``C`` to commute, while the target
is a commutator of independent uniform ``H`` and ``A``.  Over any finite group
``G`` with ``k(G)`` conjugacy classes, the residual solution count is exactly
``|G|^3 k(G)`` and every irreducible target of dimension ``d`` has normalized
character average exactly ``d^-2``.  For ``S_n``, ``k(G)=p(n)=|G|^o(1)``, so
the apparent threshold profile loses one full group exponent.

This is one exact relative-surface certificate, not a classification of every
support-conditioned target word.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    _evaluate_signed_word,
    _substitute_word_images,
    canonical_relator,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_relative_surface_factorization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

SOURCE_PATTERN = "EFBEBFB"
SOURCE_RELATION: SignedWord = (-7, -6, 7, 4, 6, -4)
SOURCE_TARGET: SignedWord = (-4, -7, -6, -5, 4, 5, 6, 7)
GENERATORS = (4, 5, 6, 7)

# New basis names reuse 4=A, 5=H, 6=C, 7=K.
OLD_TO_NEW = {
    4: (4,),
    5: (5, -7, -6),
    6: (6,),
    7: (7, -4),
}
NEW_TO_OLD = {
    4: (4,),
    5: (5, 6, 7, 4),
    6: (6,),
    7: (7, 4),
}
EXPECTED_TRANSFORMED_RELATION: SignedWord = (4, -7, -6, 7, 6, -4)
EXPECTED_CANONICAL_RELATION: SignedWord = (-7, -6, 7, 6)
EXPECTED_TRANSFORMED_TARGET: SignedWord = (-5, 4, 5, -4)


@dataclass(frozen=True)
class RelativeSurfaceFactorizationControl:
    control_id: str
    source_pattern: str
    source_relation: SignedWord
    source_target: SignedWord
    generators: tuple[int, ...]
    old_to_new_basis_images: dict[int, SignedWord]
    new_to_old_basis_images: dict[int, SignedWord]
    transformed_relation: SignedWord
    canonical_transformed_relation: SignedWord
    transformed_target: SignedWord
    relation_generator_pair: tuple[int, int]
    target_generator_pair: tuple[int, int]
    disjoint_generator_pairs: bool
    exact_two_sided_basis_inverse_verified: bool
    exact_relative_surface_factorization_verified: bool
    symmetric_group_control_degree: int
    exact_solution_count: int
    predicted_solution_count: int
    standard_normalized_character_average: str
    predicted_standard_normalized_character_average: str
    exact_finite_control_verified: bool
    symmetric_group_solution_exponent: int
    normalized_character_dimension_exponent: int
    status: str


@dataclass(frozen=True)
class RelativeSurfaceFactorizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[RelativeSurfaceFactorizationControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _two_sided_basis_inverse_verified() -> bool:
    return all(
        _substitute_word_images(
            _substitute_word_images((generator,), OLD_TO_NEW),
            NEW_TO_OLD,
        )
        == (generator,)
        and _substitute_word_images(
            _substitute_word_images((generator,), NEW_TO_OLD),
            OLD_TO_NEW,
        )
        == (generator,)
        for generator in GENERATORS
    )


def _s3_finite_control() -> tuple[int, Fraction]:
    degree = 3
    group = tuple(itertools.permutations(range(degree)))
    identity = tuple(range(degree))
    solutions = 0
    standard_character_sum = 0
    for values in itertools.product(group, repeat=len(GENERATORS)):
        assignment = dict(zip(GENERATORS, values))
        if _evaluate_signed_word(SOURCE_RELATION, assignment) != identity:
            continue
        target = _evaluate_signed_word(SOURCE_TARGET, assignment)
        solutions += 1
        standard_character_sum += sum(
            target[index] == index for index in range(degree)
        ) - 1
    return solutions, Fraction(standard_character_sum, 2 * solutions)


def relative_surface_factorization_control() -> RelativeSurfaceFactorizationControl:
    degree = 3
    transformed_relation = _substitute_word_images(SOURCE_RELATION, OLD_TO_NEW)
    transformed_target = _substitute_word_images(SOURCE_TARGET, OLD_TO_NEW)
    canonical_relation = canonical_relator(transformed_relation)
    basis_exact = _two_sided_basis_inverse_verified()
    relation_pair = (6, 7)
    target_pair = (4, 5)
    disjoint = set(relation_pair).isdisjoint(target_pair)
    factorization_exact = (
        basis_exact
        and transformed_relation == EXPECTED_TRANSFORMED_RELATION
        and canonical_relation == EXPECTED_CANONICAL_RELATION
        and transformed_target == EXPECTED_TRANSFORMED_TARGET
        and disjoint
    )
    solution_count, character_average = _s3_finite_control()
    group_order = 6
    conjugacy_class_count = 3
    predicted_solution_count = group_order**3 * conjugacy_class_count
    predicted_character_average = Fraction(1, 2**2)
    finite_exact = (
        solution_count == predicted_solution_count
        and character_average == predicted_character_average
    )
    return RelativeSurfaceFactorizationControl(
        control_id="EFBEBFB-DISJOINT-COMMUTATOR-FACTORIZATION",
        source_pattern=SOURCE_PATTERN,
        source_relation=SOURCE_RELATION,
        source_target=SOURCE_TARGET,
        generators=GENERATORS,
        old_to_new_basis_images=OLD_TO_NEW,
        new_to_old_basis_images=NEW_TO_OLD,
        transformed_relation=transformed_relation,
        canonical_transformed_relation=canonical_relation,
        transformed_target=transformed_target,
        relation_generator_pair=relation_pair,
        target_generator_pair=target_pair,
        disjoint_generator_pairs=disjoint,
        exact_two_sided_basis_inverse_verified=basis_exact,
        exact_relative_surface_factorization_verified=factorization_exact,
        symmetric_group_control_degree=degree,
        exact_solution_count=solution_count,
        predicted_solution_count=predicted_solution_count,
        standard_normalized_character_average=str(character_average),
        predicted_standard_normalized_character_average=(
            str(predicted_character_average)
        ),
        exact_finite_control_verified=finite_exact,
        symmetric_group_solution_exponent=3,
        normalized_character_dimension_exponent=2,
        status=(
            "exact-relative-surface-factorization-proved"
            if factorization_exact and finite_exact
            else "relative-surface-factorization-control-failure"
        ),
    )


def run_relative_surface_factorization() -> RelativeSurfaceFactorizationReport:
    control = relative_surface_factorization_control()
    exact = (
        control.exact_relative_surface_factorization_verified
        and control.exact_finite_control_verified
    )
    return RelativeSurfaceFactorizationReport(
        created_at=utc_now(),
        theorem_contract={
            "basis_change": (
                "With A=a, H=bcd a, C=c, K=da, the explicit old/new word "
                "maps are two-sided free-basis inverses."
            ),
            "relation_factor": (
                "The sole support relation becomes A[K,C]A^-1, so its "
                "solutions are two free variables times a commuting pair."
            ),
            "target_factor": (
                "The target becomes H^-1 A H A^-1 on the disjoint free pair "
                "(A,H), giving normalized character average d_nu^-2."
            ),
            "symmetric_group_asymptotic": (
                "The exact count is |S_n|^3 p(n)=|S_n|^(3+o(1)), one exponent "
                "below the previous trivial four-generator bound."
            ),
        },
        controls=[control],
        proof_obligations=[
            {
                "obligation": "factor_the_leading_degree_three_relative_surface",
                "resolved": exact,
                "resolution": (
                    "Relation and boundary are disjoint commutators under an "
                    "explicit verified free-basis automorphism."
                ),
            },
            {
                "obligation": "classify_all_positive_genus_support_profiles",
                "resolved": False,
                "resolution": (
                    "Search for simultaneous relation/boundary Nielsen forms and "
                    "prove a uniform handle-loss alternative at growing degree."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A threshold scalar bound makes this row dangerous.",
                "resolved": True,
                "resolution": (
                    "The threshold came from stopping proof search early. The "
                    "surface relation lowers the exact S_n exponent by one."
                ),
            },
            {
                "objection": "The finite S3 character average proves the factorization.",
                "resolved": True,
                "resolution": (
                    "False: the two-sided basis certificate proves it for every "
                    "finite group; S3 is only an independent regression control."
                ),
            },
        ],
        headline_metrics={
            "relative_surface_factorization_control_count": 1,
            "relative_surface_factorization_failure_count": int(not exact),
            "symmetric_group_solution_exponent_improvement": 1,
            "normalized_character_dimension_exponent": 2,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "leading_relative_surface_factorization_proved": exact,
            "all_positive_genus_support_profiles_classified": False,
            "growing_degree_relative_surface_theorem_proved": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One leading obstruction factorizes exactly, but no uniform "
                "growing-degree relative-surface theorem is proved."
            ),
        },
        status=(
            "leading-relative-surface-obstruction-resolved"
            if exact
            else "relative-surface-factorization-failure"
        ),
        summary=(
            "Removed the leading degree-three mixed target obstruction by a "
            "disjoint commutator factorization."
        ),
        falsifiers_triggered=[
            "Early stopping at the required pressure threshold hid a stronger surface certificate.",
            "A nontrivial residual target need not remain coupled to the support relation after a free-basis change.",
        ],
    )


def write_relative_surface_factorization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_relative_surface_factorization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_relative_surface_factorization": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_relative_surface_factorization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
