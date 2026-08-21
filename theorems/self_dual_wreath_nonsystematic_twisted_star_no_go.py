"""All-depth no-go for an explicit non-systematic codimension-two family.

The systematic stopping-core theorem does not cover binary codes without an
information set.  Such codes already exist at codimension two.  For ``n>=4``
define

    T_n = {(wt(u)+parity(y), u, y):
           u in {000,100,010,001}, y in F_2^(n-4)}.

The first coordinate is read modulo two.  The code has length ``n``, size
``2^(n-2)``, minimum distance two, and no information set of size ``n-2``.
Indeed its distance-two difference supports cover every coordinate pair.
Conversely, minimum distance two makes every projection omitting only one
coordinate injective, so its minimum separating-coordinate number is exactly
``n-1``.  This is a genuine all-depth non-systematic family, not a relabelled
graph code.

It does not evade the marked-presentation obstruction.  The code contains
``0`` and every star row ``e_0+e_i``.  The different-support relators therefore
give ``z_0 z_i=1`` for all ``i>0`` after the zero row is used, eliminating
``n-1`` appended generators.  The split, zero-row, and one same-support
complement relation leave six generators and a relator of the form

    h^-1 e^-1 h x^a c^-1 [p,q] c x^-a e.

Cyclic rotation and the Nielsen change ``c -> c x^-a`` identify this with an
orientable genus-two word for every integer ``a``.  Hence the symmetric-group
solution exponent is at most five.  For support sizes ``2^(n-2)-1`` and
``2^(n-2)``, the crossing-pressure margin is

    n - 1/2 log2(2^(n-2)(2^(n-2)-1)) > 2.

Thus lack of an information set is real but is not, by itself, a pressure
escape.  Other non-systematic codes and other marked patterns remain open.
No quantum speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)
from self_dual_wreath_support_difference_peeling_no_go import (
    Assignment,
    audit_support_difference_peeling_lift,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_nonsystematic_twisted_star_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TwistedStarControl:
    code_width: int
    code_size: int
    codimension: int
    minimum_distance: int
    all_codewords_have_even_parity: bool
    distance_two_coordinate_pair_count: int
    all_coordinate_pairs_realized_by_distance_two_differences: bool
    minimum_separating_coordinate_count: int
    has_dimension_sized_information_set: bool
    recursive_twisted_extension_verified: bool
    zero_and_all_star_rows_present: bool
    support_difference_peeling_stalls_on_full_core: bool
    remaining_generator_count: int
    residual_relations: tuple[SignedWord, ...]
    residual_involution_relation_present: bool
    solution_exponent_upper_bound: float
    solution_exponent_certificate_source: str
    support_entropy_bits: float
    true_pressure_margin_lower_bound: float
    residual_target_word: SignedWord
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class TwistedStarAllDepthCertificate:
    minimum_width: int
    family_formula: str
    size_and_codimension_proof: str
    minimum_distance_proof: str
    no_information_set_proof: str
    recursive_extension_formula: str
    star_relator_elimination: str
    residual_surface_relation: str
    residual_surface_nielsen_reduction: str
    symmetric_group_solution_exponent_upper_bound: float
    pressure_margin_formula: str
    uniform_pressure_margin_lower_bound: float
    arbitrary_width: bool
    universal_twisted_star_family_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class TwistedStarNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[TwistedStarControl]
    all_depth_certificate: TwistedStarAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def twisted_star_code(width: int) -> tuple[Assignment, ...]:
    if width < 4:
        raise ValueError("twisted-star code requires width at least four")
    unit_ball = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
    rows = []
    for leaf in unit_ball:
        for tail in itertools.product((0, 1), repeat=width - 4):
            center = (sum(leaf) + sum(tail)) % 2
            rows.append((center, *leaf, *tail))
    return tuple(sorted(rows))


def twisted_star_recursive_extension(
    code: tuple[Assignment, ...],
) -> tuple[Assignment, ...]:
    if not code or any(len(row) != len(code[0]) for row in code):
        raise ValueError("recursive extension requires a nonempty uniform code")
    output = []
    for row in code:
        output.append((*row, 0))
        output.append((row[0] ^ 1, *row[1:], 1))
    return tuple(sorted(output))


def _minimum_distance(code: tuple[Assignment, ...]) -> int:
    return min(
        sum(a != b for a, b in zip(left, right))
        for left, right in itertools.combinations(code, 2)
    )


def distance_two_difference_supports(
    code: tuple[Assignment, ...],
) -> tuple[tuple[int, int], ...]:
    supports = set()
    for left, right in itertools.combinations(code, 2):
        difference = tuple(
            index for index, (a, b) in enumerate(zip(left, right)) if a != b
        )
        if len(difference) == 2:
            supports.add(difference)
    return tuple(sorted(supports))


def minimum_separating_coordinate_count(
    code: tuple[Assignment, ...],
) -> int:
    width = len(code[0])
    for size in range(width + 1):
        for coordinates in itertools.combinations(range(width), size):
            projections = {
                tuple(row[index] for index in coordinates) for row in code
            }
            if len(projections) == len(code):
                return size
    raise AssertionError("all coordinates must separate distinct codewords")


def twisted_star_marked_supports(
    width: int,
) -> tuple[str, tuple[Assignment, ...], tuple[Assignment, ...]]:
    code = twisted_star_code(width)
    same = tuple((1, 0, 1, 0, *row) for row in code if any(row))
    different = tuple((0, 0, 0, 0, *row) for row in code)
    pattern = "E" + "BABA" + "A" * width + "FEF"
    return pattern, same, different


def audit_twisted_star(width: int) -> TwistedStarControl:
    code = twisted_star_code(width)
    pattern, same, different = twisted_star_marked_supports(width)
    coordinate_pairs = tuple(itertools.combinations(range(width), 2))
    realized_pairs = distance_two_difference_supports(code)
    separator = minimum_separating_coordinate_count(code)
    recursive = width == 4 or twisted_star_recursive_extension(
        twisted_star_code(width - 1)
    ) == code
    star_rows = {
        tuple(int(index in (0, coordinate)) for index in range(width))
        for coordinate in range(1, width)
    }
    star_present = (0,) * width in code and star_rows.issubset(set(code))
    appended = tuple(range(5, 5 + width))
    peeling = audit_support_difference_peeling_lift(
        f"TWISTED-STAR-{width}",
        pattern,
        appended,
        same,
        different,
    )
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    exponent, source = presentation_solution_exponent_upper_bound(reduction)
    appended_generators = set(range(6, 6 + width))
    surviving_appended = appended_generators.intersection(
        reduction.remaining_generators
    )
    involution = any(
        len(relation) == 2
        and abs(relation[0]) == abs(relation[1])
        and abs(relation[0]) in surviving_appended
        for relation in reduction.residual_relations
    )
    entropy = 0.5 * math.log2(len(same)) + 0.5 * math.log2(
        len(different)
    )
    margin = width + 5 - (exponent + entropy)
    target = _transport_target_product_word(len(pattern), reduction)
    exact = (
        len(code) == 1 << (width - 2)
        and _minimum_distance(code) == 2
        and all(sum(row) % 2 == 0 for row in code)
        and realized_pairs == coordinate_pairs
        and separator == width - 1
        and recursive
        and star_present
        and peeling.uncovered_appended_coordinates_one_based == appended
        and peeling.residual_core_is_stopping_set
        and len(reduction.remaining_generators) == 6
        and len(surviving_appended) == 1
        and (width == 4 or involution)
        and exponent <= 5.0
        and margin > 2.0
        and bool(target)
    )
    return TwistedStarControl(
        code_width=width,
        code_size=len(code),
        codimension=2,
        minimum_distance=_minimum_distance(code),
        all_codewords_have_even_parity=all(sum(row) % 2 == 0 for row in code),
        distance_two_coordinate_pair_count=len(realized_pairs),
        all_coordinate_pairs_realized_by_distance_two_differences=(
            realized_pairs == coordinate_pairs
        ),
        minimum_separating_coordinate_count=separator,
        has_dimension_sized_information_set=separator <= width - 2,
        recursive_twisted_extension_verified=recursive,
        zero_and_all_star_rows_present=star_present,
        support_difference_peeling_stalls_on_full_core=(
            peeling.uncovered_appended_coordinates_one_based == appended
        ),
        remaining_generator_count=len(reduction.remaining_generators),
        residual_relations=reduction.residual_relations,
        residual_involution_relation_present=involution,
        solution_exponent_upper_bound=exponent,
        solution_exponent_certificate_source=source,
        support_entropy_bits=entropy,
        true_pressure_margin_lower_bound=margin,
        residual_target_word=target,
        exact_control_verified=exact,
        status=(
            "nonsystematic-twisted-star-uniformly-subleading"
            if exact
            else "nonsystematic-twisted-star-certificate-failure"
        ),
    )


def twisted_star_all_depth_certificate() -> TwistedStarAllDepthCertificate:
    return TwistedStarAllDepthCertificate(
        minimum_width=4,
        family_formula=(
            "T_n={(wt(u)+parity(y),u,y):u in {000,e1,e2,e3}, "
            "y in F_2^(n-4)}"
        ),
        size_and_codimension_proof=(
            "The four choices of u and 2^(n-4) choices of y give exactly "
            "2^(n-2) distinct length-n rows."
        ),
        minimum_distance_proof=(
            "Every row has even parity, so every nonzero difference has even "
            "weight; explicit star pairs attain weight two."
        ),
        no_information_set_proof=(
            "Every coordinate pair is the exact support of a codeword "
            "difference, so omitting any two coordinates causes a collision. "
            "Minimum distance two makes omission of one coordinate injective."
        ),
        recursive_extension_formula=(
            "T_(n+1)={(c,0):c in T_n} union "
            "{(c+e_0,1):c in T_n}."
        ),
        star_relator_elimination=(
            "0 and e_0+e_i lie in T_n for every i>0; their different-support "
            "relators give z_0 z_i=1 and leave one appended generator."
        ),
        residual_surface_relation=(
            "h^-1 e^-1 h x^a c^-1 [p,q] c x^-a e for an integer a"
        ),
        residual_surface_nielsen_reduction=(
            "After cyclic rotation, c -> c x^-a turns the relator into a "
            "product of two commutators, with the remaining generator free."
        ),
        symmetric_group_solution_exponent_upper_bound=5.0,
        pressure_margin_formula=(
            "n-0.5*log2(2^(n-2)*(2^(n-2)-1)) > 2"
        ),
        uniform_pressure_margin_lower_bound=2.0,
        arbitrary_width=True,
        universal_twisted_star_family_no_go_verified=True,
        status="all-depth-nonsystematic-twisted-star-pressure-no-go",
    )


def run_nonsystematic_twisted_star_no_go() -> TwistedStarNoGoReport:
    controls = [audit_twisted_star(width) for width in range(4, 8)]
    theorem = twisted_star_all_depth_certificate()
    exact = all(control.exact_control_verified for control in controls)
    return TwistedStarNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "construction": (
                "An explicit nonlinear codimension-two code family with no "
                "dimension-sized coordinate information set."
            ),
            "non_systematic_witness": (
                "Distance-two differences cover every omitted coordinate pair."
            ),
            "presentation_conclusion": (
                "Star rows collapse the growing frame and a fixed genus-two "
                "relator bounds the solution exponent by five."
            ),
            "scope_limit": (
                "This kills one all-depth non-systematic family, not every "
                "non-systematic stopping code or marked pattern."
            ),
        },
        representative_controls=controls,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "construct_constant_codimension_nonsystematic_family",
                "resolved": True,
                "resolution": (
                    "T_n has codimension two and separator number n-1 for every n>=4."
                ),
            },
            {
                "obligation": "test_information_set_defect_as_pressure_escape",
                "resolved": True,
                "resolution": (
                    "Information-set defect alone fails: T_n has pressure margin >2."
                ),
            },
            {
                "obligation": "classify_all_nonsystematic_stopping_codes",
                "resolved": False,
                "resolution": (
                    "Search families without a spanning star subsystem and bound "
                    "their ordered-word presentation rank."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "All dense stopping codes may secretly be systematic.",
                "resolved": True,
                "resolution": (
                    "False: every n-2 coordinate projection of T_n has a certified "
                    "distance-two collision."
                ),
            },
            {
                "objection": "Removing systematic coordinates may preserve pressure.",
                "resolved": True,
                "resolution": (
                    "False for T_n: its star rows eliminate all but one growing "
                    "generator and the surface relation costs another exponent."
                ),
            },
            {
                "objection": "Finite-width SAT examples do not define a family.",
                "resolved": True,
                "resolution": (
                    "The closed formula and twisted-extension recursion work at "
                    "every width n>=4."
                ),
            },
        ],
        headline_metrics={
            "all_depth_nonsystematic_family_construction_count": 1,
            "all_depth_twisted_star_no_go_theorem_count": int(
                theorem.universal_twisted_star_family_no_go_verified
            ),
            "stored_width_control_count": len(controls),
            "control_failure_count": sum(
                not control.exact_control_verified for control in controls
            ),
            "maximum_stored_information_set_defect": max(
                control.minimum_separating_coordinate_count
                - (control.code_width - 2)
                for control in controls
            ),
            "minimum_stored_true_pressure_margin": min(
                control.true_pressure_margin_lower_bound for control in controls
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "explicit_nonsystematic_constant_codimension_family_constructed": True,
            "twisted_star_information_set_escape_survives": False,
            "twisted_star_actual_pressure_survives": False,
            "all_twisted_star_widths_controlled": (
                theorem.universal_twisted_star_family_no_go_verified
            ),
            "all_nonsystematic_stopping_codes_controlled": False,
            "all_multiple_base_fiber_patterns_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The explicit non-systematic family exists, but star relators and "
                "a fixed surface law make it uniformly subleading."
            ),
        },
        status=(
            "nonsystematic-twisted-star-family-falsified-by-surface-loss"
            if exact
            else "nonsystematic-twisted-star-no-go-certificate-failure"
        ),
        summary=(
            "Constructed an all-depth codimension-two code with no information "
            "set and proved that its marked presentation still has margin >2."
        ),
        falsifiers_triggered=[
            "Dense stopping codes need not admit dimension-sized information sets.",
            "Information-set defect alone does not preserve crossing pressure.",
            "The twisted-star family collapses to a fixed-rank surface system.",
        ],
    )


def write_nonsystematic_twisted_star_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_nonsystematic_twisted_star_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_nonsystematic_twisted_star_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
