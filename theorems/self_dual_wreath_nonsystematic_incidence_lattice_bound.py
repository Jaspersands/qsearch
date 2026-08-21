"""Incidence-lattice bound for normalized non-systematic quarter-cube codes.

Let ``C`` be a length-``n`` binary code containing zero, of size ``2^(n-2)``
and minimum distance at least two.  If no ``n-2`` coordinates separate ``C``,
then for every coordinate pair ``{i,j}`` two codewords differ exactly there.
For the integer incidence lattice ``L=span_Z(C)``, this gives

    e_i = +/- e_j  in Z^n/L

for every pair.  Hence the quotient is cyclic: either infinite, or finite with
Smith invariants ``(1,...,1,D)``.

In the finite case of order ``D>=5``, choose signs ``sigma_i`` with
``e_i=sigma_i g``.  Every codeword satisfies

    sum sigma_i c_i = 0 (mod D).

Complementing the negative-sign bits turns this into one residue class of a
``Binomial(n,1/2)`` random variable.  Because zero belongs to ``C``, a
single-level residue fiber would put ``C`` in a real hyperplane, contradicting
full rank.  A residue containing at least two levels has mass below ``1/4``:
condition on all but nine bits.  Among the remaining nine, admissible weights
are separated by at least five, and their largest binomial mass is

    (binom(9,0)+binom(9,5))/2^9 = 127/512 < 1/4.

Widths below nine are checked directly.  Thus every full-rank incidence
lattice has ``D<=4``.  If the quotient is infinite, the code lies in an exact
signed-weight layer of size at most ``binom(n,floor(n/2))``, already below a
quarter cube for ``n>=9``.  Therefore every all-depth normalized family has
full incidence rank and cyclic torsion of order at most four.

This rules out a growing abelian root-degree escape.  It does not prove that
the full ordered noncommutative presentation has bounded rank: perfect or
commutator-subgroup residual laws remain the decisive open case.  No quantum
speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

from research_registry import utc_now
from self_dual_wreath_nonsystematic_mod_four_no_go import mod_four_code
from self_dual_wreath_nonsystematic_twisted_star_no_go import twisted_star_code
from self_dual_wreath_support_difference_peeling_no_go import Assignment


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_nonsystematic_incidence_lattice_bound.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


INDEX_THREE_CODE: tuple[Assignment, ...] = tuple(
    tuple((value >> index) & 1 for index in range(5))
    for value in (0, 7, 11, 13, 14, 19, 21, 22)
)
RANK_DEFICIENT_CODE: tuple[Assignment, ...] = tuple(
    tuple((value >> index) & 1 for index in range(5))
    for value in (0, 10, 12, 15, 18, 20, 23, 30)
)


@dataclass(frozen=True)
class IncidenceLatticeControl:
    control_id: str
    code_width: int
    code_size: int
    minimum_distance: int
    distance_two_coordinate_pair_count: int
    all_coordinate_pairs_covered: bool
    has_dimension_sized_information_set: bool
    integer_incidence_rank: int
    quotient_kind: str
    finite_lattice_index: int | None
    nonzero_smith_invariants: tuple[int, ...]
    signed_congruence_vector: tuple[int, ...] | None
    signed_congruence_modulus: int | None
    signed_relation_verified: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class BinomialResidueAnticoncentrationControl:
    bit_width: int
    modulus: int
    maximum_multilevel_residue_sum: int
    quarter_cube_size: int
    maximizing_residue: int | None
    every_multilevel_residue_strictly_below_quarter: bool
    status: str


@dataclass(frozen=True)
class IncidenceLatticeAllDepthCertificate:
    normalized_code_scope: str
    no_information_set_pair_coverage: str
    cyclic_quotient_derivation: str
    finite_quotient_signed_congruence: str
    nine_bit_anticoncentration_bound: str
    nine_bit_maximum_mass: float
    small_width_direct_bound: str
    infinite_quotient_layer_bound: str
    rank_deficient_maximum_width: int
    full_rank_maximum_lattice_index: int
    arbitrary_width_at_least_nine: bool
    growing_abelian_torsion_escape_excluded: bool
    nonabelian_residual_presentation_still_open: bool
    status: str


@dataclass(frozen=True)
class IncidenceLatticeBoundReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[IncidenceLatticeControl]
    anticoncentration_controls: list[BinomialResidueAnticoncentrationControl]
    all_depth_certificate: IncidenceLatticeAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _minimum_distance(code: tuple[Assignment, ...]) -> int:
    return min(
        sum(a != b for a, b in zip(left, right))
        for left, right in itertools.combinations(code, 2)
    )


def distance_two_coordinate_pairs(
    code: tuple[Assignment, ...],
) -> tuple[tuple[int, int], ...]:
    pairs = set()
    for left, right in itertools.combinations(code, 2):
        difference = tuple(
            index for index, (a, b) in enumerate(zip(left, right)) if a != b
        )
        if len(difference) == 2:
            pairs.add(difference)
    return tuple(sorted(pairs))


def incidence_smith_invariants(
    code: tuple[Assignment, ...],
) -> tuple[int, tuple[int, ...]]:
    matrix = Matrix(code)
    rank = int(matrix.rank())
    smith = smith_normal_form(matrix, domain=ZZ)
    diagonal = tuple(
        abs(int(smith[index, index]))
        for index in range(min(smith.shape))
        if smith[index, index] != 0
    )
    return rank, diagonal


def _signed_relation(
    code: tuple[Assignment, ...],
    modulus: int | None,
) -> tuple[int, ...] | None:
    width = len(code[0])
    for tail in itertools.product((-1, 1), repeat=width - 1):
        signs = (1, *tail)
        if all(
            (
                sum(sign * bit for sign, bit in zip(signs, row)) == 0
                if modulus is None
                else sum(sign * bit for sign, bit in zip(signs, row)) % modulus
                == 0
            )
            for row in code
        ):
            return signs
    return None


def audit_incidence_lattice(
    control_id: str,
    code: tuple[Assignment, ...],
) -> IncidenceLatticeControl:
    if not code or code[0] != (0,) * len(code[0]):
        raise ValueError("incidence theorem controls must be normalized at zero")
    width = len(code[0])
    if len(code) != 1 << (width - 2):
        raise ValueError("control must have quarter-cube cardinality")
    pairs = distance_two_coordinate_pairs(code)
    all_pairs = tuple(itertools.combinations(range(width), 2))
    rank, smith = incidence_smith_invariants(code)
    if rank == width:
        index = math.prod(smith)
        quotient_kind = "finite-cyclic"
        signs = _signed_relation(code, index)
        modulus = index
    else:
        index = None
        quotient_kind = "infinite-cyclic"
        signs = _signed_relation(code, None)
        modulus = None
    signed_exact = signs is not None
    exact = (
        _minimum_distance(code) >= 2
        and pairs == all_pairs
        and rank in (width - 1, width)
        and len(smith) == rank
        and all(value == 1 for value in smith[:-1])
        and signed_exact
    )
    return IncidenceLatticeControl(
        control_id=control_id,
        code_width=width,
        code_size=len(code),
        minimum_distance=_minimum_distance(code),
        distance_two_coordinate_pair_count=len(pairs),
        all_coordinate_pairs_covered=pairs == all_pairs,
        has_dimension_sized_information_set=pairs != all_pairs,
        integer_incidence_rank=rank,
        quotient_kind=quotient_kind,
        finite_lattice_index=index,
        nonzero_smith_invariants=smith,
        signed_congruence_vector=signs,
        signed_congruence_modulus=modulus,
        signed_relation_verified=signed_exact,
        exact_control_verified=exact,
        status=(
            "cyclic-incidence-quotient-verified"
            if exact
            else "incidence-lattice-certificate-failure"
        ),
    )


def maximum_multilevel_binomial_residue_sum(
    bit_width: int,
    modulus: int,
) -> tuple[int, int | None]:
    if bit_width < 1 or modulus < 2:
        raise ValueError("positive width and modulus at least two required")
    best = 0
    maximizing = None
    for residue in range(modulus):
        levels = tuple(range(residue, bit_width + 1, modulus))
        if len(levels) < 2:
            continue
        total = sum(math.comb(bit_width, level) for level in levels)
        if total > best:
            best = total
            maximizing = residue
    return best, maximizing


def audit_binomial_residue_anticoncentration(
    bit_width: int,
    modulus: int,
) -> BinomialResidueAnticoncentrationControl:
    maximum, residue = maximum_multilevel_binomial_residue_sum(
        bit_width,
        modulus,
    )
    quarter = 1 << (bit_width - 2) if bit_width >= 2 else 0
    exact = maximum < quarter
    return BinomialResidueAnticoncentrationControl(
        bit_width=bit_width,
        modulus=modulus,
        maximum_multilevel_residue_sum=maximum,
        quarter_cube_size=quarter,
        maximizing_residue=residue,
        every_multilevel_residue_strictly_below_quarter=exact,
        status=(
            "multilevel-binomial-residue-below-quarter"
            if exact
            else "binomial-residue-anticoncentration-failure"
        ),
    )


def incidence_lattice_all_depth_certificate(
) -> IncidenceLatticeAllDepthCertificate:
    nine_bit_maximum = (
        math.comb(9, 0) + math.comb(9, 5)
    ) / (1 << 9)
    small_width_exact = all(
        audit_binomial_residue_anticoncentration(width, modulus)
        .every_multilevel_residue_strictly_below_quarter
        for width in range(5, 9)
        for modulus in range(5, width + 1)
    )
    central_nine = math.comb(9, 4) < 1 << 7
    exact = nine_bit_maximum < 0.25 and small_width_exact and central_nine
    return IncidenceLatticeAllDepthCertificate(
        normalized_code_scope=(
            "0 in C subset F_2^n, |C|=2^(n-2), minimum distance at least two, "
            "and no injective projection onto n-2 coordinates"
        ),
        no_information_set_pair_coverage=(
            "Failure after omitting {i,j} gives a collision supported exactly "
            "on {i,j}; hence e_i=+/-e_j in the incidence quotient."
        ),
        cyclic_quotient_derivation=(
            "All coordinate classes equal one generator up to sign, so Z^n/L "
            "is finite cyclic or infinite cyclic."
        ),
        finite_quotient_signed_congruence=(
            "For order D>2, unique signs sigma_i give every codeword signed "
            "weight zero modulo D."
        ),
        nine_bit_anticoncentration_bound=(
            "Conditioning outside nine bits leaves binomial levels separated by "
            "at least five; their maximum mass is (C(9,0)+C(9,5))/2^9."
        ),
        nine_bit_maximum_mass=nine_bit_maximum,
        small_width_direct_bound=(
            "For widths 5,6,7,8 the maxima are respectively 2,7,22,57, all "
            "below 2^(n-2)."
        ),
        infinite_quotient_layer_bound=(
            "An infinite quotient places C in one exact signed-weight layer of "
            "size at most C(n,floor(n/2)), below 2^(n-2) for n>=9."
        ),
        rank_deficient_maximum_width=8,
        full_rank_maximum_lattice_index=4,
        arbitrary_width_at_least_nine=True,
        growing_abelian_torsion_escape_excluded=exact,
        nonabelian_residual_presentation_still_open=True,
        status=(
            "all-depth-incidence-lattice-torsion-bound"
            if exact
            else "incidence-lattice-anticoncentration-proof-failure"
        ),
    )


def run_nonsystematic_incidence_lattice_bound(
) -> IncidenceLatticeBoundReport:
    controls = [
        audit_incidence_lattice(
            "INDEX-TWO-TWISTED-STAR",
            twisted_star_code(5),
        ),
        audit_incidence_lattice("INDEX-THREE", INDEX_THREE_CODE),
        audit_incidence_lattice("INDEX-FOUR-MOD-FOUR", mod_four_code(6)),
        audit_incidence_lattice("RANK-DEFICIENT-SIGNED-LAYER", RANK_DEFICIENT_CODE),
    ]
    anticoncentration = [
        audit_binomial_residue_anticoncentration(width, modulus)
        for width in range(5, 33)
        for modulus in range(5, width + 1)
    ]
    theorem = incidence_lattice_all_depth_certificate()
    exact = (
        all(control.exact_control_verified for control in controls)
        and all(
            control.every_multilevel_residue_strictly_below_quarter
            for control in anticoncentration
        )
        and theorem.growing_abelian_torsion_escape_excluded
    )
    return IncidenceLatticeBoundReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.normalized_code_scope,
            "quotient_classification": (
                "Pair coverage forces the incidence quotient to be cyclic."
            ),
            "asymptotic_bound": (
                "For n>=9 the lattice has full rank and finite index at most four."
            ),
            "research_consequence": (
                "No all-depth candidate can obtain vanishing loss merely from a "
                "growing Smith invariant of the codeword incidence lattice."
            ),
            "scope_limit": (
                "Unnormalized supports and nonabelian residual presentation rank "
                "are not controlled by this abelian theorem."
            ),
        },
        representative_controls=controls,
        anticoncentration_controls=anticoncentration,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "bound_normalized_nonsystematic_incidence_torsion",
                "resolved": True,
                "resolution": "The cyclic quotient has order at most four for n>=9.",
            },
            {
                "obligation": "exclude_rank_deficient_all_depth_family",
                "resolved": True,
                "resolution": (
                    "Central-binomial anticoncentration confines infinite quotient "
                    "controls to n<=8."
                ),
            },
            {
                "obligation": "bound_nonabelian_ordered_presentation_rank",
                "resolved": False,
                "resolution": (
                    "Bound the commutator-subgroup kernel after the cyclic "
                    "abelian quotient reduction, or construct a growing-rank family."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A dense no-information-set code may have many Smith factors.",
                "resolved": True,
                "resolution": "Pair coverage makes the entire quotient cyclic.",
            },
            {
                "objection": "The one Smith factor may grow with width.",
                "resolved": True,
                "resolution": (
                    "A modulus at least five has multilevel binomial mass below one quarter."
                ),
            },
            {
                "objection": "A rank-deficient lattice evades the modular bound.",
                "resolved": True,
                "resolution": (
                    "Its exact signed layer is too small once n>=9."
                ),
            },
            {
                "objection": "Bounded abelianization proves bounded full presentation.",
                "resolved": False,
                "resolution": (
                    "False as a general group-theoretic inference; nonabelian kernels "
                    "can be large and remain the next proof obligation."
                ),
            },
        ],
        headline_metrics={
            "all_depth_incidence_lattice_bound_theorem_count": int(
                theorem.growing_abelian_torsion_escape_excluded
            ),
            "representative_index_control_count": len(controls),
            "maximum_realized_finite_index": max(
                control.finite_lattice_index or 0 for control in controls
            ),
            "anticoncentration_case_count": len(anticoncentration),
            "anticoncentration_failure_count": sum(
                not control.every_multilevel_residue_strictly_below_quarter
                for control in anticoncentration
            ),
            "rank_deficient_maximum_width": theorem.rank_deficient_maximum_width,
            "full_rank_maximum_lattice_index": (
                theorem.full_rank_maximum_lattice_index
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "no_information_set_forces_cyclic_incidence_quotient": True,
            "growing_abelian_smith_torsion_escape_survives": False,
            "rank_deficient_all_depth_escape_survives": False,
            "bounded_index_nonabelian_residual_escape_open": True,
            "all_nonsystematic_stopping_codes_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The abelian incidence quotient is bounded, but its nonabelian "
                "ordered-presentation kernel is not yet classified."
            ),
        },
        status=(
            "growing-incidence-torsion-escape-falsified"
            if exact
            else "incidence-lattice-bound-certificate-failure"
        ),
        summary=(
            "Proved that every all-depth normalized codimension-two no-information-"
            "set family has cyclic incidence torsion of order at most four."
        ),
        falsifiers_triggered=[
            "The incidence quotient cannot have multiple independent Smith factors.",
            "Its finite order cannot grow beyond four asymptotically.",
            "Rank-deficient normalized families cannot persist beyond width eight.",
        ],
    )


def write_nonsystematic_incidence_lattice_bound_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_nonsystematic_incidence_lattice_bound())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_nonsystematic_incidence_lattice_bound_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
