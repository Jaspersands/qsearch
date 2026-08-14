"""Kronecker reduction inside hyperoctahedral Clebsch--Gordan fusion.

Let ``K_m=C_2 wr S_m=(C_2)^m semidirect S_m`` and let
``pi:K_m->S_m`` be the quotient map.  The wreath irrep indexed by
``(lambda,empty)`` is exactly the inflation of the Specht module ``S^lambda``:

    W_(lambda,empty) = Infl_pi(S^lambda).                (1)

Therefore

    W_(lambda,empty) tensor W_(mu,empty)
      = direct_sum_nu g(lambda,mu,nu) W_(nu,empty),      (2)

where ``g`` is the ordinary symmetric-group Kronecker coefficient.  Any
uniform coherent Clebsch--Gordan transform for the hyperoctahedral family,
restricted to this trivial-color sector, implements an internal ``S_m``
Kronecker transform.  A fast wreath-product QFT or isotypic measurement does
not supply this multiplicity basis.

The reduction is not a hardness proof for the natural hidden-involution
source.  In the regular ``K_m`` representation, the total trivial-color
Plancherel mass is ``2^-m`` and its mass conditioned on even central parity is
``2^(1-m)``.  The actual source fiber ``ran(P_0)^tensor k`` is not regular
``K_m`` Plancherel, so its weight on these embedded sectors must be proved
before this reduction can obstruct a source-weighted compiler.  Conversely,
an algorithm may bypass generic wreath fusion by exploiting the specific
matrix-Hecke transfer rather than implementing every Clebsch--Gordan block.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hyperoctahedral_cg_kronecker_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HYPEROCTAHEDRAL-CG-KRONECKER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class InflatedKroneckerFiniteControl:
    half_degree: int
    partition_count: int
    partition_triple_count: int
    maximum_ordinary_kronecker_coefficient: int
    maximum_inflated_wreath_coefficient: int
    coefficient_mismatch_count: int
    sum_inflated_irrep_dimension_squares: int
    expected_symmetric_group_order: int
    hyperoctahedral_group_order: int
    trivial_color_regular_plancherel_mass: float
    even_parity_conditioned_trivial_color_mass: float
    exact_inflation_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralCgScalingRecord:
    half_degree: int
    hyperoctahedral_order_decimal: str
    symmetric_group_order_decimal: str
    trivial_color_dimension_square_sum_decimal: str
    trivial_color_regular_plancherel_mass: float
    even_parity_conditioned_trivial_color_mass: float
    generic_wreath_cg_contains_symmetric_kronecker: bool
    efficient_wreath_qft_implies_efficient_wreath_cg: bool
    natural_source_trivial_color_mass_lower_bound_proved: bool
    source_specific_matrix_hecke_bypass_ruled_out: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralCgKroneckerTheorem:
    quotient: str
    inflated_irreps: str
    tensor_product_identity: str
    transform_reduction: str
    regular_mass: str
    natural_source_caveat: str
    scope_limit: str
    inflated_tensor_identity_proved: bool
    generic_wreath_cg_contains_internal_symmetric_kronecker: bool
    efficient_qft_sufficient_for_cg: bool
    natural_source_hard_sector_mass_proved: bool
    source_specific_fusion_compiler_ruled_out: bool
    quantum_complexity_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HyperoctahedralCgKroneckerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[InflatedKroneckerFiniteControl]
    scaling_records: list[HyperoctahedralCgScalingRecord]
    theorem: HyperoctahedralCgKroneckerTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def kronecker_coefficient(
    left: Partition,
    right: Partition,
    target: Partition,
) -> int:
    size = sum(left)
    if sum(right) != size or sum(target) != size:
        raise ValueError("partitions must have one common size")
    total = 0
    for cycle_type in integer_partitions(size):
        total += (
            conjugacy_class_size(cycle_type)
            * symmetric_character(left, cycle_type)
            * symmetric_character(right, cycle_type)
            * symmetric_character(target, cycle_type)
        )
    coefficient = Fraction(total, math.factorial(size))
    if coefficient.denominator != 1 or coefficient < 0:
        raise ArithmeticError("Kronecker character sum was not nonnegative integral")
    return coefficient.numerator


def inflated_wreath_tensor_coefficient(
    left: Partition,
    right: Partition,
    target: Partition,
) -> int:
    """Evaluate the inflated ``K_m`` character inner product.

    Every permutation in ``S_m`` has ``2^m`` preimages under ``K_m->S_m``;
    inflated characters are constant on each fiber, so the wreath inner
    product cancels that factor exactly.
    """

    size = sum(left)
    if sum(right) != size or sum(target) != size:
        raise ValueError("partitions must have one common size")
    wreath_order = (2**size) * math.factorial(size)
    total = 0
    for cycle_type in integer_partitions(size):
        total += (
            (2**size)
            * conjugacy_class_size(cycle_type)
            * symmetric_character(left, cycle_type)
            * symmetric_character(right, cycle_type)
            * symmetric_character(target, cycle_type)
        )
    coefficient = Fraction(total, wreath_order)
    if coefficient.denominator != 1 or coefficient < 0:
        raise ArithmeticError("inflated wreath character sum was invalid")
    return coefficient.numerator


def audit_inflated_kronecker_reduction(
    half_degree: int,
) -> InflatedKroneckerFiniteControl:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    partitions = integer_partitions(half_degree)
    mismatches = 0
    maximum_ordinary = 0
    maximum_wreath = 0
    for left in partitions:
        for right in partitions:
            for target in partitions:
                ordinary = kronecker_coefficient(left, right, target)
                wreath = inflated_wreath_tensor_coefficient(
                    left, right, target
                )
                maximum_ordinary = max(maximum_ordinary, ordinary)
                maximum_wreath = max(maximum_wreath, wreath)
                mismatches += ordinary != wreath
    dimension_square_sum = sum(
        hook_length_dimension(partition) ** 2 for partition in partitions
    )
    symmetric_order = math.factorial(half_degree)
    wreath_order = (2**half_degree) * symmetric_order
    regular_mass = dimension_square_sum / wreath_order
    conditioned_mass = 2.0 * regular_mass
    verified = bool(
        mismatches == 0
        and dimension_square_sum == symmetric_order
        and regular_mass == 2.0 ** (-half_degree)
        and conditioned_mass == 2.0 ** (1 - half_degree)
    )
    return InflatedKroneckerFiniteControl(
        half_degree=half_degree,
        partition_count=len(partitions),
        partition_triple_count=len(partitions) ** 3,
        maximum_ordinary_kronecker_coefficient=maximum_ordinary,
        maximum_inflated_wreath_coefficient=maximum_wreath,
        coefficient_mismatch_count=mismatches,
        sum_inflated_irrep_dimension_squares=dimension_square_sum,
        expected_symmetric_group_order=symmetric_order,
        hyperoctahedral_group_order=wreath_order,
        trivial_color_regular_plancherel_mass=regular_mass,
        even_parity_conditioned_trivial_color_mass=conditioned_mass,
        exact_inflation_reduction_verified=verified,
        status=(
            "inflated-wreath-cg-equals-symmetric-kronecker"
            if verified
            else "inflated-kronecker-control-failure"
        ),
    )


def hyperoctahedral_cg_scaling_record(
    half_degree: int,
) -> HyperoctahedralCgScalingRecord:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    symmetric_order = math.factorial(half_degree)
    wreath_order = (2**half_degree) * symmetric_order
    return HyperoctahedralCgScalingRecord(
        half_degree=half_degree,
        hyperoctahedral_order_decimal=str(wreath_order),
        symmetric_group_order_decimal=str(symmetric_order),
        trivial_color_dimension_square_sum_decimal=str(symmetric_order),
        trivial_color_regular_plancherel_mass=2.0 ** (-half_degree),
        even_parity_conditioned_trivial_color_mass=2.0 ** (1 - half_degree),
        generic_wreath_cg_contains_symmetric_kronecker=True,
        efficient_wreath_qft_implies_efficient_wreath_cg=False,
        natural_source_trivial_color_mass_lower_bound_proved=False,
        source_specific_matrix_hecke_bypass_ruled_out=False,
        status="generic-wreath-cg-reduced-natural-sector-mass-open",
    )


def build_hyperoctahedral_cg_kronecker_report(
    *,
    finite_half_degrees: tuple[int, ...] = (2, 3, 4, 5, 6),
    scaling_half_degrees: tuple[int, ...] = (4, 8, 16, 32, 64, 128),
) -> HyperoctahedralCgKroneckerReport:
    controls = [
        audit_inflated_kronecker_reduction(m) for m in finite_half_degrees
    ]
    scaling = [
        hyperoctahedral_cg_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = all(row.exact_inflation_reduction_verified for row in controls)
    theorem = HyperoctahedralCgKroneckerTheorem(
        quotient="K_m=(C_2)^m semidirect S_m has quotient pi:K_m->S_m.",
        inflated_irreps=(
            "The wreath irrep (lambda,empty) is Infl_pi(S^lambda); the base "
            "group acts trivially."
        ),
        tensor_product_identity=(
            "(lambda,empty) tensor (mu,empty) decomposes with the ordinary "
            "S_m Kronecker coefficients g(lambda,mu,nu)."
        ),
        transform_reduction=(
            "Restricting a uniform K_m Clebsch-Gordan transform to trivial "
            "color implements the internal S_m Kronecker transform."
        ),
        regular_mass=(
            "Trivial-color mass is 2^-m under K_m Plancherel and 2^(1-m) "
            "after conditioning on even central parity."
        ),
        natural_source_caveat=(
            "The hidden-involution fiber is not regular K_m Plancherel; its "
            "weight on the embedded sectors is not bounded here."
        ),
        scope_limit=(
            "No complexity lower bound is proved, and a source-specific "
            "matrix-Hecke transform may bypass generic wreath fusion."
        ),
        inflated_tensor_identity_proved=True,
        generic_wreath_cg_contains_internal_symmetric_kronecker=True,
        efficient_qft_sufficient_for_cg=False,
        natural_source_hard_sector_mass_proved=False,
        source_specific_fusion_compiler_ruled_out=False,
        quantum_complexity_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "generic-wreath-cg-contains-kronecker-natural-mass-open"
            if verified
            else "hyperoctahedral-cg-reduction-control-failure"
        ),
    )
    return HyperoctahedralCgKroneckerReport(
        created_at=utc_now(),
        theorem_contract={
            "group_family": "K_m=C_2 wr S_m with quotient onto S_m.",
            "transform": (
                "A uniform coherent Clebsch-Gordan transform on arbitrary "
                "K_m irrep pairs, including multiplicity registers."
            ),
            "embedded_sector": (
                "Bipartitions (lambda,empty) with trivial base-group color."
            ),
            "outside_scope": (
                "Natural source weighting, approximate/source-specific fusion, "
                "and any lower bound for quantum circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-NATURAL-COLOR-MASS",
                "statement": (
                    "Compute the alternative/source-weighted mass of trivial-"
                    "color and other Kronecker-hard K_m fusion sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-SOURCE-SPECIFIC-FUSION",
                "statement": (
                    "Determine whether the matrix-Hecke transfer needs a general "
                    "K_m CG transform or only a smaller structured subtransform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-CG-DEQUANTIZATION",
                "statement": (
                    "Test whether the source-relevant wreath fusion amplitudes "
                    "are classically computable or sampleable."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "An efficient hyperoctahedral QFT supplies its CG transform.",
                "answer": (
                    "False: QFT/isotypic access does not resolve tensor-product "
                    "multiplicity, and the trivial-color restriction contains "
                    "the full S_m Kronecker transform."
                ),
                "resolved": True,
            },
            {
                "challenge": "The embedded Kronecker sectors block the natural algorithm.",
                "answer": (
                    "Unproved. Their regular parity-conditioned mass is "
                    "exponentially small, and natural source mass is unknown."
                ),
                "resolved": True,
            },
            {
                "challenge": "Kronecker multiplicities imply a quantum lower bound.",
                "answer": (
                    "False. Neither difficult classical counting nor unresolved "
                    "basis construction proves quantum circuit hardness."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": "arxiv:quant-ph/0304064",
                "title": "Generic Quantum Fourier Transforms",
                "url": "https://arxiv.org/abs/quant-ph/0304064",
                "use": (
                    "Efficient QFT framework; does not by itself provide the "
                    "tensor-product multiplicity transform used here."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "arxiv:2302.11454",
                "title": "Quantum complexity of the Kronecker coefficients",
                "url": "https://arxiv.org/abs/2302.11454",
                "use": (
                    "Complexity context for Kronecker multiplicity estimation; "
                    "not used as a circuit lower bound."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics={
            "exact_inflation_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_inflation_reduction_verified for row in controls
            ),
            "generic_wreath_cg_to_kronecker_reduction_count": 1,
            "efficient_wreath_qft_to_cg_implication_count": 0,
            "natural_source_hard_sector_mass_theorem_count": 0,
            "quantum_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "generic_hyperoctahedral_cg_contains_symmetric_kronecker": verified,
            "efficient_hyperoctahedral_qft_implies_efficient_cg": False,
            "natural_source_kronecker_hard_mass_proved": False,
            "source_specific_matrix_hecke_bypass_ruled_out": False,
            "uniform_hyperoctahedral_cg_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Generic wreath fusion contains the unresolved symmetric-group "
                "Kronecker transform, but those sectors may be negligible or "
                "avoidable for the natural source."
            ),
        },
        status=theorem.status,
        summary=(
            "Reduced generic hyperoctahedral Clebsch-Gordan fusion to the "
            "ordinary symmetric-group Kronecker transform on trivial-color "
            "sectors, while isolating natural source-sector mass as the required "
            "next test before treating this as an algorithmic obstruction."
        ),
        falsifiers_triggered=[
            "Efficient wreath QFT access does not imply efficient wreath fusion.",
            "Generic hyperoctahedral fusion is not easier than internal symmetric-group Kronecker fusion.",
            "The embedded hard-looking sector has exponentially small regular even-parity mass.",
            "No natural-source obstruction or quantum lower bound follows without a source-mass theorem.",
        ],
    )


def write_hyperoctahedral_cg_kronecker_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_hyperoctahedral_cg_kronecker_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_hyperoctahedral_cg_kronecker_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
