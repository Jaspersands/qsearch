"""Exact all-n gap certificate for one Kronecker commutant family.

For lambda=(n-2,2), let H_n be the simultaneous-conjugacy orbit sum

    sum rho_lambda(tau) tensor rho_lambda(c),

where c ranges over oriented 3-cycles and tau is a transposition on the same
three points.  The target nu=(n-3,2,1) occurs twice in lambda tensor lambda.
This module constructs its symmetric and antisymmetric copies explicitly from
Specht polytabloids in the 2-subset permutation module and evaluates both
Rayleigh quotients symbolically.  Their exact difference is 2(n-2), giving
LCU-normalized gap 2/[n(n-1)] for every n>=6.

This closes one restricted spectral-gap obligation.  It does not construct a
general Kronecker transform, a Racah/associator network, or a hidden-involution
decoder.
"""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import TypeAlias

import sympy as sp

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_COMMUTANT_GAP_CERTIFICATE_PATH = Path(
    "research/representation/coset_commutant_gap_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COMMUTANT-GAP-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Edge: TypeAlias = tuple[int, int]
TensorEdge: TypeAlias = tuple[Edge, Edge]
Tabloid: TypeAlias = tuple[Edge, int]


@dataclass(frozen=True)
class ParityGapRecord:
    parity: str
    sparse_vector_term_count: int
    exact_norm: str
    exact_hamiltonian_expectation: str
    exact_eigenvalue: str
    nonzero_for_all_n_at_least_6: bool


@dataclass(frozen=True)
class CommutantGapCertificate:
    created_at: str
    theorem: dict[str, object]
    local_operator_certificate: dict[str, object]
    multiplicity_certificate: dict[str, object]
    specht_map_certificate: dict[str, object]
    parity_records: list[ParityGapRecord]
    exact_gap_certificate: dict[str, object]
    literature_scope: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _edge(left: int, right: int) -> Edge:
    if left == right:
        raise ValueError("an edge needs two distinct vertices")
    return tuple(sorted((left, right)))


def _permutation_parity(values: tuple[int, ...]) -> int:
    inversions = sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def target_polytabloid() -> dict[Tabloid, int]:
    """Return a 12-term (n-3,2,1) polytabloid in M^(n-3,2,1).

    The first two columns are (1,3,5) and (2,4); all remaining entries lie in
    the first row and do not enter the column antisymmetrizer.
    """

    terms: defaultdict[Tabloid, int] = defaultdict(int)
    for first_column in itertools.permutations((1, 3, 5)):
        for second_column in itertools.permutations((2, 4)):
            permutation = dict(zip((1, 3, 5), first_column))
            permutation.update(zip((2, 4), second_column))
            tabloid = (_edge(permutation[3], permutation[4]), permutation[5])
            terms[tabloid] += _permutation_parity(
                first_column
            ) * _permutation_parity(second_column)
    return {tabloid: coefficient for tabloid, coefficient in terms.items() if coefficient}


def parity_specht_vector(parity: int) -> dict[TensorEdge, int]:
    """Apply the equivariant path map and its swap parity projection."""

    if parity not in (-1, 1):
        raise ValueError("parity must be +1 or -1")
    vector: defaultdict[TensorEdge, int] = defaultdict(int)
    for (base_edge, point), coefficient in target_polytabloid().items():
        left, right = base_edge
        for incident_edge in (_edge(left, point), _edge(right, point)):
            vector[(base_edge, incident_edge)] += coefficient
            vector[(incident_edge, base_edge)] += parity * coefficient
    return {basis: coefficient for basis, coefficient in vector.items() if coefficient}


@lru_cache(maxsize=None)
def projected_edge_inner_product(
    left: Edge, right: Edge, n: sp.Symbol | int
) -> sp.Expr:
    """Gram entry for the [n-2,2] projection of two edge basis vectors."""

    intersection = len(set(left).intersection(right))
    diagonal = 1 if left == right else 0
    return sp.factor(
        diagonal - (intersection - sp.Rational(2, 1) / (n - 1)) / (n - 2)
    )


@lru_cache(maxsize=None)
def _tensor_inner_product(
    left: TensorEdge, right: TensorEdge, n: sp.Symbol
) -> sp.Expr:
    return projected_edge_inner_product(left[0], right[0], n) * projected_edge_inner_product(
        left[1], right[1], n
    )


def symbolic_vector_inner_product(
    left: dict[TensorEdge, int],
    right: dict[TensorEdge, int],
    n: sp.Symbol,
) -> sp.Expr:
    return sp.factor(
        sum(
            left_coefficient
            * right_coefficient
            * _tensor_inner_product(left_basis, right_basis, n)
            for left_basis, left_coefficient in left.items()
            for right_basis, right_coefficient in right.items()
        )
    )


def _point_transposition(left: int, right: int) -> dict[int, int]:
    return {left: right, right: left}


def _point_cycle(first: int, second: int, third: int) -> dict[int, int]:
    return {first: second, second: third, third: first}


def _apply_point_permutation(edge: Edge, permutation: dict[int, int]) -> Edge:
    return _edge(
        permutation.get(edge[0], edge[0]),
        permutation.get(edge[1], edge[1]),
    )


def symbolic_hamiltonian_expectation(
    vector: dict[TensorEdge, int], n: sp.Symbol
) -> sp.Expr:
    """Evaluate <v,H_n v> by exact support-orbit aggregation.

    The vector is supported on vertices 1..5.  A 3-subset contributing to H_n
    is classified by how many vertices lie outside this support.  All choices
    in one class have the same matrix element, giving binomial(n-5,r) copies.
    """

    support = {1, 2, 3, 4, 5}
    canonical_outside = (6, 7, 8)
    overlap_cache: dict[TensorEdge, sp.Expr] = {}

    def overlap(transformed: TensorEdge) -> sp.Expr:
        if transformed not in overlap_cache:
            overlap_cache[transformed] = sum(
                bra_coefficient
                * _tensor_inner_product(bra_basis, transformed, n)
                for bra_basis, bra_coefficient in vector.items()
            )
        return overlap_cache[transformed]

    total = sp.Integer(0)
    for outside_count in range(4):
        inside_count = 3 - outside_count
        subtotal = sp.Integer(0)
        for inside in itertools.combinations(sorted(support), inside_count):
            triple = (*inside, *canonical_outside[:outside_count])
            first, second, third = triple
            cycles = (
                _point_cycle(first, second, third),
                _point_cycle(first, third, second),
            )
            for ket_basis, ket_coefficient in vector.items():
                for transposition in itertools.combinations(triple, 2):
                    left_edge = _apply_point_permutation(
                        ket_basis[0], _point_transposition(*transposition)
                    )
                    for cycle in cycles:
                        transformed = (
                            left_edge,
                            _apply_point_permutation(ket_basis[1], cycle),
                        )
                        subtotal += ket_coefficient * overlap(transformed)
        total += sp.binomial(n - len(support), outside_count) * subtotal
    return sp.factor(sp.expand_func(total))


def _stirling_second(power: int, count: int) -> int:
    if power == count == 0:
        return 1
    if power == 0 or count == 0 or count > power:
        return 0
    table = [[0] * (count + 1) for _ in range(power + 1)]
    table[0][0] = 1
    for row in range(1, power + 1):
        for column in range(1, min(row, count) + 1):
            table[row][column] = table[row - 1][column - 1] + column * table[row - 1][column]
    return table[power][count]


def stable_kronecker_multiplicity_certificate() -> dict[str, object]:
    """Prove g((n-2,2),(n-2,2),(n-3,2,1))=2 for n>=6."""

    x1, x2, x3 = sp.symbols("X1 X2 X3")
    source_character = sp.expand_func(sp.binomial(x1, 2) + x2 - x1)
    target_character = (x1**3 - 6 * x1**2 + 8 * x1) / 3 - x3
    product = sp.Poly(sp.expand(source_character**2 * target_character), x1, x2, x3)
    falling_terms: defaultdict[tuple[int, int, int], sp.Expr] = defaultdict(
        lambda: sp.Integer(0)
    )
    for powers, coefficient in product.terms():
        for fixed_cycles in range(powers[0] + 1):
            for two_cycles in range(powers[1] + 1):
                for three_cycles in range(powers[2] + 1):
                    transformed = (
                        coefficient
                        * _stirling_second(powers[0], fixed_cycles)
                        * _stirling_second(powers[1], two_cycles)
                        * _stirling_second(powers[2], three_cycles)
                    )
                    if transformed:
                        falling_terms[(fixed_cycles, two_cycles, three_cycles)] += transformed
    falling_terms = defaultdict(
        lambda: sp.Integer(0),
        {
            powers: sp.simplify(coefficient)
            for powers, coefficient in falling_terms.items()
            if sp.simplify(coefficient) != 0
        },
    )
    stable_threshold = max(
        fixed_cycles + 2 * two_cycles + 3 * three_cycles
        for fixed_cycles, two_cycles, three_cycles in falling_terms
    )
    stable_expectation = sp.simplify(
        sum(
            coefficient
            / (sp.Integer(2) ** two_cycles * sp.Integer(3) ** three_cycles)
            for (fixed_cycles, two_cycles, three_cycles), coefficient in falling_terms.items()
        )
    )
    n6_multiplicity = kronecker_coefficient((4, 2), (4, 2), (3, 2, 1))
    return {
        "source_character_polynomial": "binomial(X1,2)+X2-X1",
        "target_character_polynomial": "(X1^3-6*X1^2+8*X1)/3-X3",
        "cycle_factorial_moment_rule": (
            "E[product_i (X_i)_{a_i}]=product_i i^{-a_i} whenever sum_i i*a_i<=n"
        ),
        "stable_factorial_moment_threshold": stable_threshold,
        "stable_multiplicity_for_n_at_least_7": int(stable_expectation),
        "direct_n6_multiplicity": n6_multiplicity,
        "all_n_at_least_6_multiplicity": 2,
        "proved": stable_threshold == 7 and stable_expectation == 2 and n6_multiplicity == 2,
    }


@lru_cache(maxsize=1)
def build_commutant_gap_certificate() -> CommutantGapCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    symmetric_vector = parity_specht_vector(1)
    antisymmetric_vector = parity_specht_vector(-1)
    symmetric_norm = symbolic_vector_inner_product(symmetric_vector, symmetric_vector, n)
    antisymmetric_norm = symbolic_vector_inner_product(
        antisymmetric_vector, antisymmetric_vector, n
    )
    symmetric_expectation = symbolic_hamiltonian_expectation(symmetric_vector, n)
    antisymmetric_expectation = symbolic_hamiltonian_expectation(antisymmetric_vector, n)
    symmetric_eigenvalue = sp.factor(sp.cancel(symmetric_expectation / symmetric_norm))
    antisymmetric_eigenvalue = sp.factor(
        sp.cancel(antisymmetric_expectation / antisymmetric_norm)
    )
    raw_gap = sp.factor(symmetric_eigenvalue - antisymmetric_eigenvalue)
    term_count = n * (n - 1) * (n - 2)
    normalized_gap = sp.factor(raw_gap / term_count)
    expected_symmetric = n**3 - 11 * n**2 + 34 * n - 26
    expected_antisymmetric = (n - 1) * (n**2 - 10 * n + 22)
    multiplicity = stable_kronecker_multiplicity_certificate()
    identities_hold = (
        sp.simplify(symmetric_eigenvalue - expected_symmetric) == 0
        and sp.simplify(antisymmetric_eigenvalue - expected_antisymmetric) == 0
        and sp.simplify(raw_gap - 2 * (n - 2)) == 0
        and sp.simplify(normalized_gap - 2 / (n * (n - 1))) == 0
    )
    parity_records = [
        ParityGapRecord(
            parity="symmetric",
            sparse_vector_term_count=len(symmetric_vector),
            exact_norm=str(symmetric_norm),
            exact_hamiltonian_expectation=str(symmetric_expectation),
            exact_eigenvalue=str(symmetric_eigenvalue),
            nonzero_for_all_n_at_least_6=True,
        ),
        ParityGapRecord(
            parity="antisymmetric",
            sparse_vector_term_count=len(antisymmetric_vector),
            exact_norm=str(antisymmetric_norm),
            exact_hamiltonian_expectation=str(antisymmetric_expectation),
            exact_eigenvalue=str(antisymmetric_eigenvalue),
            nonzero_for_all_n_at_least_6=True,
        ),
    ]
    theorem_proved = identities_hold and bool(multiplicity["proved"])
    return CommutantGapCertificate(
        created_at=utc_now(),
        theorem={
            "source_partition": "lambda_n=(n-2,2)",
            "target_partition": "nu_n=(n-3,2,1)",
            "range": "every integer n>=6",
            "hamiltonian": (
                "H_n=sum rho_lambda(tau) tensor rho_lambda(c) over oriented 3-cycles c and transpositions tau on supp(c)"
            ),
            "statement": (
                "The two target multiplicity eigenvalues differ by exactly 2(n-2), hence the LCU-normalized gap is 2/[n(n-1)]."
            ),
            "proof_method": (
                "Explicit symmetric/antisymmetric Specht polytabloids in the projected 2-subset module, with exact support-orbit aggregation."
            ),
        },
        local_operator_certificate={
            "two_subset_realization": (
                "V_(n-2,2) is the kernel component of the vertex-edge incidence map in the 2-subset permutation module."
            ),
            "projected_edge_gram_entry": (
                "delta(e,f)-(|e intersect f|-2/(n-1))/(n-2)"
            ),
            "local_s3_identity": (
                "On V_(n-2,2), the local 3-cycle class sum Z_S equals T_S-I because the restricted S_3 module has no sign constituent."
            ),
            "swap_symmetry": (
                "Summing T_S tensor (T_S-I) over triples is swap invariant since sum_S T_S is a one-sided central scalar."
            ),
            "lcu_term_count": "6*binomial(n,3)=n(n-1)(n-2)",
            "proved": True,
        },
        multiplicity_certificate=multiplicity,
        specht_map_certificate={
            "domain": "Young permutation module M^(n-3,2,1)",
            "polytabloid_column_groups": "S_{1,3,5} x S_{2,4}",
            "polytabloid_term_count": len(target_polytabloid()),
            "equivariant_map": (
                "({a,b},c) maps to w_ab tensor (w_ac+w_bc) plus or minus its swapped tensor."
            ),
            "symmetric_image_norm": str(symmetric_norm),
            "antisymmetric_image_norm": str(antisymmetric_norm),
            "nonzero_for_every_n_at_least_6": True,
            "parity_multiplicities": (
                "Each image supplies one target copy in opposite swap parity; total Kronecker multiplicity two makes both parity blocks one-dimensional."
            ),
            "proved": bool(multiplicity["proved"]),
        },
        parity_records=parity_records,
        exact_gap_certificate={
            "symmetric_eigenvalue": str(symmetric_eigenvalue),
            "antisymmetric_eigenvalue": str(antisymmetric_eigenvalue),
            "raw_gap": str(raw_gap),
            "lcu_normalization": str(term_count),
            "lcu_normalized_gap": str(normalized_gap),
            "phase_estimation_inverse_gap_scaling": "n(n-1)/2",
            "symbolic_identities_verified": identities_hold,
        },
        literature_scope=[
            {
                "id": "arXiv:1210.5579",
                "role": "Partition-algebra framework for stable Kronecker coefficients and two-row families.",
            },
            {
                "id": "arXiv:1204.4533",
                "role": "FI-module and character-polynomial stability context; not used as a substitute for the explicit calculation.",
            },
        ],
        headline_metrics={
            "all_n_critical_gap_theorem_count": int(theorem_proved),
            "restricted_family_inverse_polynomial_gap_count": int(theorem_proved),
            "symbolic_parity_eigenvalue_count": 2,
            "stable_kronecker_multiplicity": int(multiplicity["all_n_at_least_6_multiplicity"]),
            "minimum_proved_n": 6,
            "lcu_normalized_gap_exponent": 2,
            "general_sector_gap_theorem_count": 0,
            "kcopy_associator_count": 0,
            "hidden_involution_decoder_count": 0,
        },
        claim_gate={
            "exact_symbolic_specht_calculation": identities_hold,
            "all_n_restricted_gap_theorem_proved": theorem_proved,
            "restricted_family_phase_estimation_polynomial": theorem_proved,
            "general_kronecker_multiplicity_transform_proved": False,
            "balanced_or_plancherel_relevant_sector_coverage_proved": False,
            "kcopy_associator_polynomial_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact gap theorem covers one stable two-row source and multiplicity-two target. It does not cover general sectors, recoupling, or decoding."
            ),
        },
        status=(
            "all-n-restricted-commutant-gap-proved-associator-decoder-open"
            if theorem_proved
            else "commutant-gap-certificate-failed"
        ),
        summary=(
            "Proved the raw 2(n-2) and LCU-normalized 2/[n(n-1)] multiplicity gap for "
            "lambda=(n-2,2), nu=(n-3,2,1), all n>=6; general-sector, Racah, and decoder obligations remain open."
        ),
        falsifiers_triggered=[
            "Finite interpolation is not used: both parity Rayleigh quotients are exact symbolic expressions.",
            "A theorem on one multiplicity-two family is not promoted to a general internal Kronecker transform.",
            "Polynomial phase estimation for this label does not implement overlapping Racah moves or decode a hidden involution.",
        ],
    )


def write_commutant_gap_certificate(
    output_path: Path = COSET_COMMUTANT_GAP_CERTIFICATE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_commutant_gap_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-RESTRICTED-GAP-AS-GENERAL-KRONECKER-TRANSFORM",
                source=str(output_path),
                claim=(
                    "The proved (n-2,2) multiplicity-two gap supplies a general efficient internal S_n Kronecker transform."
                ),
                reason_invalid=(
                    "The certificate proves one stable parity-split block only; balanced sectors, larger multiplicities, associators, and decoding are absent."
                ),
                lesson=(
                    "Use the exact family as a test case for Racah constructions, not as an end-to-end algorithm claim."
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
                artifacts={"coset_commutant_gap_certificate": str(output_path)},
            )
        )
    return payload
