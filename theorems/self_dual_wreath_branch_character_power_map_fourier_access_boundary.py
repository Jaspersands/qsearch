"""Fourier-block normalization of the branch power-map expansion.

The equivariant normal form leaves the specific reduced maps as the only
possible structured access route.  The local cyclic compiler supplies an
explicit expansion

    J_h = sum_(z,r) c_(z,r;h) |z> tensor
          tensor_i rho_(lambda_i)(h^(1-r_i))
                   tensor rho_(mu_i)(h^r_i).              (1)

For fixed exponent tuple ``r``, the corresponding multiplier monomial is

    M_(nu,r)=|G|^-1/2 sum_h rho_nu(h^-1) tensor
              tensor_i rho_(lambda_i)(h^(1-r_i))
                       tensor rho_(mu_i)(h^r_i).           (2)

Equation (2) is a block of an efficient nonlinear Fourier isometry.  Define

    Phi_r(h)=(h^(1-r_1),h^r_1,...,h^(1-r_k),h^r_k).

The map is injective because multiplying either adjacent pair recovers ``h``.
Group powering and multiplication make

    V_r: |h> -> |Phi_r(h)>

an efficiently reversible isometry.  Conjugating its input and all ``2k``
outputs by group QFTs gives a fast power-map Fourier tensor.

The useful block is nevertheless highly subnormalized.  If the input block is
``nu`` and the output blocks have dimensions ``d_1,...,d_(2k)``, QFT matrix
normalization gives

    block(V_r) = sqrt(d_nu product_j d_j)
                 / |G|^((2k+1)/2)
                 sum_h rho_nu(h^-1) tensor product_j rho_j(h^a_j).

Comparing with (2),

    M_(nu,r) = alpha_(nu,Lambda) block(V_r),
    alpha_(nu,Lambda)=|G|^k/sqrt(d_nu D_Lambda),          (3)

where ``D_Lambda=product_i d_lambda_i d_mu_i``.

Every finite-group irrep has dimension at most ``sqrt(|G|)``.  Hence

    alpha_(nu,Lambda) >= |G|^(k/2-1/4).                  (4)

At ``k=Theta(log|G|)``, termwise extraction or amplitude amplification of a
power-map Fourier block is superpolynomial by an exponent quadratic in
``log|G|``.  The direct cyclic controls below verify the exact normalization,
including both nonzero and selection-rule-zero blocks.

This does not reject a coherent transform of the full sum in (1).  As with a
fast Fourier transform, exponentially many individually tiny blocks can
combine into a normalization-one unitary.  A positive result must therefore
factor the whole quadrant coefficient tensor before block selection, or find
an exact recursion that cancels the QFT dimension factors.  Termwise
power-map compilation is not that result.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_power_map_fourier_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-POWER-MAP-"
    "FOURIER-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CyclicPowerMapFourierControl:
    control_id: str
    group_order: int
    copy_count: int
    exponent_parameters: tuple[int, ...]
    power_tuple: tuple[int, ...]
    input_character: int
    output_characters: tuple[int, ...]
    power_map_image_size: int
    power_map_is_injective: bool
    transformed_isometry_residual: float
    direct_multiplier_monomial: tuple[float, float]
    transformed_fourier_block: tuple[float, float]
    predicted_block_normalization: float
    direct_to_scaled_block_residual: float
    selection_rule_satisfied: bool
    exact_power_map_fourier_normalization_verified: bool
    status: str


@dataclass(frozen=True)
class PowerMapAccessScaling:
    n: int
    log2_group_order: float
    copy_count: int
    source_factor_count: int
    maximum_possible_fourier_dimension_log2: float
    maximum_possible_source_carrier_dimension_log2: float
    termwise_block_normalization_log2_lower_bound: float
    generic_amplification_query_log2_lower_bound: float
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    termwise_power_map_block_extraction_superpolynomial: bool
    coherent_full_quadrant_sum_compiled: bool
    status: str


@dataclass(frozen=True)
class PowerMapFourierAccessTheorem:
    branch_power_expansion: str
    injective_power_map: str
    nonlinear_fourier_isometry: str
    exact_block_normalization: str
    dimension_lower_bound: str
    natural_copy_consequence: str
    surviving_escape: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PowerMapFourierAccessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PowerMapFourierAccessTheorem
    nonzero_controls: list[CyclicPowerMapFourierControl]
    zero_controls: list[CyclicPowerMapFourierControl]
    scaling_records: list[PowerMapAccessScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def cyclic_qft(order: int) -> np.ndarray:
    if order < 2:
        raise ValueError("order must be at least two")
    values = np.arange(order)
    return np.exp(2j * math.pi * np.outer(values, values) / order) / math.sqrt(order)


def power_tuple(exponent_parameters: tuple[int, ...]) -> tuple[int, ...]:
    output = []
    for exponent in exponent_parameters:
        output.extend((1 - exponent, exponent))
    return tuple(output)


def cyclic_power_map_isometry(
    order: int,
    exponent_parameters: tuple[int, ...],
) -> np.ndarray:
    if order < 2 or not exponent_parameters:
        raise ValueError("need a nontrivial group and at least one source pair")
    exponents = power_tuple(exponent_parameters)
    output_dimension = order ** len(exponents)
    isometry = np.zeros((output_dimension, order), dtype=complex)
    for element in range(order):
        coordinates = tuple((exponent * element) % order for exponent in exponents)
        index = 0
        for coordinate in coordinates:
            index = index * order + coordinate
        isometry[index, element] = 1.0
    return isometry


def transformed_cyclic_power_map(
    order: int,
    exponent_parameters: tuple[int, ...],
) -> np.ndarray:
    qft = cyclic_qft(order)
    output_qft = np.asarray([[1.0]], dtype=complex)
    for _ in power_tuple(exponent_parameters):
        output_qft = np.kron(output_qft, qft)
    return (
        output_qft
        @ cyclic_power_map_isometry(order, exponent_parameters)
        @ qft.conj().T
    )


def _tuple_index(order: int, coordinates: tuple[int, ...]) -> int:
    output = 0
    for coordinate in coordinates:
        if not 0 <= coordinate < order:
            raise ValueError("coordinate outside cyclic character range")
        output = output * order + coordinate
    return output


def cyclic_multiplier_monomial(
    order: int,
    exponent_parameters: tuple[int, ...],
    input_character: int,
    output_characters: tuple[int, ...],
) -> complex:
    exponents = power_tuple(exponent_parameters)
    if len(output_characters) != len(exponents):
        raise ValueError("one output character is required per power coordinate")
    return sum(
        (
            np.exp(-2j * math.pi * input_character * element / order)
            * math.prod(
                np.exp(
                    2j
                    * math.pi
                    * character
                    * exponent
                    * element
                    / order
                )
                for character, exponent in zip(output_characters, exponents)
            )
            for element in range(order)
        ),
        0.0j,
    ) / math.sqrt(order)


def audit_cyclic_power_map_fourier(
    control_id: str,
    order: int,
    exponent_parameters: tuple[int, ...],
    input_character: int,
    output_characters: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> CyclicPowerMapFourierControl:
    exponents = power_tuple(exponent_parameters)
    if len(output_characters) != len(exponents):
        raise ValueError("output character count mismatch")
    isometry = cyclic_power_map_isometry(order, exponent_parameters)
    transformed = transformed_cyclic_power_map(order, exponent_parameters)
    image_size = int(np.count_nonzero(np.linalg.norm(isometry, axis=1)))
    injective = image_size == order
    isometry_residual = float(
        np.linalg.norm(
            transformed.conj().T @ transformed - np.eye(order),
            ord=2,
        )
    )
    row = _tuple_index(order, tuple(value % order for value in output_characters))
    block = complex(transformed[row, input_character % order])
    direct = cyclic_multiplier_monomial(
        order,
        exponent_parameters,
        input_character % order,
        tuple(value % order for value in output_characters),
    )
    normalization = float(order ** len(exponent_parameters))
    residual = abs(direct - normalization * block)
    frequency = sum(
        character * exponent
        for character, exponent in zip(output_characters, exponents)
    ) % order
    selection = frequency == input_character % order
    verified = bool(
        injective
        and isometry_residual <= 100 * tolerance
        and residual <= 1000 * tolerance
        and (abs(direct) > tolerance) == selection
    )
    return CyclicPowerMapFourierControl(
        control_id=control_id,
        group_order=order,
        copy_count=len(exponent_parameters),
        exponent_parameters=exponent_parameters,
        power_tuple=exponents,
        input_character=input_character % order,
        output_characters=tuple(value % order for value in output_characters),
        power_map_image_size=image_size,
        power_map_is_injective=injective,
        transformed_isometry_residual=isometry_residual,
        direct_multiplier_monomial=(float(direct.real), float(direct.imag)),
        transformed_fourier_block=(float(block.real), float(block.imag)),
        predicted_block_normalization=normalization,
        direct_to_scaled_block_residual=residual,
        selection_rule_satisfied=selection,
        exact_power_map_fourier_normalization_verified=verified,
        status=(
            "injective-power-map-fourier-block-normalization-verified"
            if verified
            else "power-map-fourier-control-failure"
        ),
    )


def power_map_access_scaling(
    n: int,
    *,
    polynomial_benchmark_degree: int = 20,
) -> PowerMapAccessScaling:
    if n < 2 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid scaling parameters")
    log2_order = math.log2(math.factorial(n))
    copies = math.ceil(3.0 * log2_order) + 2
    factor_count = 2 * copies
    max_irrep_log2 = log2_order / 2.0
    max_source_log2 = copies * log2_order
    normalization_lower = (copies / 2.0 - 0.25) * log2_order
    benchmark = polynomial_benchmark_degree * math.log2(n)
    return PowerMapAccessScaling(
        n=n,
        log2_group_order=log2_order,
        copy_count=copies,
        source_factor_count=factor_count,
        maximum_possible_fourier_dimension_log2=max_irrep_log2,
        maximum_possible_source_carrier_dimension_log2=max_source_log2,
        termwise_block_normalization_log2_lower_bound=normalization_lower,
        generic_amplification_query_log2_lower_bound=normalization_lower,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        termwise_power_map_block_extraction_superpolynomial=(
            normalization_lower > benchmark
        ),
        coherent_full_quadrant_sum_compiled=False,
        status=(
            "termwise-power-map-fourier-block-extraction-superpolynomial"
            if normalization_lower > benchmark
            else "finite-termwise-separation-not-yet-visible"
        ),
    )


def run_power_map_fourier_access_boundary() -> PowerMapFourierAccessReport:
    nonzero = [
        audit_cyclic_power_map_fourier(
            "C5-ONE-PAIR-NONZERO",
            5,
            (2,),
            1,
            (1, 1),
        ),
        audit_cyclic_power_map_fourier(
            "C3-TWO-PAIR-NONZERO",
            3,
            (2, 1),
            0,
            (1, 0, 1, 1),
        ),
    ]
    zero = [
        audit_cyclic_power_map_fourier(
            "C5-ONE-PAIR-ZERO",
            5,
            (2,),
            3,
            (1, 1),
        ),
        audit_cyclic_power_map_fourier(
            "C3-TWO-PAIR-ZERO",
            3,
            (2, 1),
            1,
            (1, 0, 1, 1),
        ),
    ]
    scaling = [power_map_access_scaling(n) for n in (8, 16, 32, 64, 128)]
    verified = bool(
        all(row.exact_power_map_fourier_normalization_verified for row in nonzero)
        and all(row.exact_power_map_fourier_normalization_verified for row in zero)
        and all(row.selection_rule_satisfied for row in nonzero)
        and all(not row.selection_rule_satisfied for row in zero)
        and all(row.termwise_power_map_block_extraction_superpolynomial for row in scaling)
    )
    theorem = PowerMapFourierAccessTheorem(
        branch_power_expansion=(
            "Each branch-polar field is a coherent cyclic Fourier sum of paired "
            "source actions h^(1-r_i) and h^r_i."
        ),
        injective_power_map=(
            "Phi_r(h) is injective because either adjacent output pair multiplies "
            "to h, so its group-basis isometry is efficiently reversible."
        ),
        nonlinear_fourier_isometry=(
            "Applying one input and 2k output group QFTs gives an efficient "
            "power-map Fourier tensor containing every multiplier monomial block."
        ),
        exact_block_normalization=(
            "M_(nu,r)=|G|^k/sqrt(d_nu D_Lambda) times the selected Fourier block."
        ),
        dimension_lower_bound=(
            "Since every irrep dimension is at most sqrt(|G|), the block "
            "normalization is at least |G|^(k/2-1/4)."
        ),
        natural_copy_consequence=(
            "At k=Theta(log|G|), termwise block extraction or amplification has "
            "log cost Omega((log|G|)^2)."
        ),
        surviving_escape=(
            "Only a coherent factorization of the full quadrant coefficient sum, "
            "before tiny block selection, can use the efficient power-map isometry."
        ),
        scope=(
            "This rejects termwise power-map block compilation, not an FFT-like "
            "whole-sum recursion or arbitrary structured multiplier circuit."
        ),
        theorem_verified=verified,
        status=(
            "power-map-fourier-primitive-proved-termwise-normalization-fatal"
            if verified
            else "power-map-fourier-access-control-failure"
        ),
    )
    tail = scaling[-1]
    return PowerMapFourierAccessReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        nonzero_controls=nonzero,
        zero_controls=zero,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "realize_each_quadrant_power_monomial_as_fast_fourier_primitive",
                "resolved": verified,
                "resolution": "The paired power map is injective and reversible; QFT conjugation contains the monomial as an exact block."
            },
            {
                "obligation": "test_termwise_power_map_block_extraction_as_compiler",
                "resolved": verified,
                "resolution": "Rejected: the exact block normalization is |G|^k/sqrt(d_nu D), at least |G|^(k/2-1/4)."
            },
            {
                "obligation": "factor_full_quadrant_coefficient_tensor_before_block_selection",
                "resolved": False,
                "resolution": "Search for an FFT-like recursion or shared cyclic-phase register that sums exponent tuples without termwise postselection."
            },
            {
                "obligation": "compile_direct_multiplier_and_hidden_label_decoder",
                "resolved": False,
                "resolution": "No normalization-one whole-sum transform, physical decoder, or speedup is established."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Efficient reversible power maps immediately compile the Fourier multipliers.",
                "resolved": True,
                "resolution": "False. The desired representation block is smaller than the isometry block by the exact factor in equation (3)."
            },
            {
                "objection": "Typical maximal irrep dimensions cancel the block normalization.",
                "resolved": True,
                "resolution": "Even assigning sqrt(|G|) to every input and source irrep leaves |G|^(k/2-1/4)."
            },
            {
                "objection": "A huge termwise factor proves the coherent full sum is hard.",
                "resolved": True,
                "resolution": "No. Fourier transforms themselves combine tiny entries efficiently; a whole-sum recursion remains open."
            },
        ],
        headline_metrics={
            "injective_power_map_fourier_primitive_theorem_count": int(verified),
            "termwise_power_map_normalization_no_go_count": int(verified),
            "nonzero_fourier_block_control_count": len(nonzero),
            "selection_rule_zero_control_count": len(zero),
            "maximum_control_normalization": max(
                row.predicted_block_normalization for row in (*nonzero, *zero)
            ),
            "tail_n": tail.n,
            "tail_copy_count": tail.copy_count,
            "tail_termwise_normalization_log2_lower_bound": tail.termwise_block_normalization_log2_lower_bound,
            "coherent_full_quadrant_sum_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "paired_power_map_injective_isometry_proved": verified,
            "power_map_fourier_block_identity_proved": verified,
            "termwise_block_normalization_formula_proved": verified,
            "termwise_power_map_compiler_superpolynomial_proved": verified,
            "coherent_full_quadrant_sum_factorized": False,
            "direct_equivariant_multiplier_compiled": False,
            "physical_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Identified every quadrant monomial as a block of an efficient "
            "injective power-map Fourier isometry, then proved that extracting "
            "those blocks term by term is catastrophically subnormalized. The "
            "remaining positive target is an FFT-like coherent whole-sum factorization."
        ),
        falsifiers_triggered=[
            "An efficient power-map basis circuit is not by itself an efficient selected Fourier block.",
            "Maximal irrep dimensions do not cancel termwise normalization at natural copy count.",
            "The no-go does not cover coherent whole-sum recursions.",
        ],
    )


def write_power_map_fourier_access_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_power_map_fourier_access_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_power_map_fourier_access_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
