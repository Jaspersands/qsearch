"""Regular-source Walsh output is flat, killing fixed sparse-mode truncation.

Let ``G`` be a finite group of order ``d``, let ``rho`` be any unitary target
representation of dimension ``t``, and put one left-regular register in each
of ``K`` source pairs.  For orientation ``e in F_2^K``, define

    E_e = d^-1 sum_g rho(g) tensor_i L(g)_(e_i) tensor I_(1-e_i).  (1)

Each ``E_e`` is an orthogonal invariant-subspace projector of rank
``r=t d^(2K-1)``.  For normalized Walsh modes

    Ehat_S = 2^-K sum_e (-1)^(S.e) E_e,                  (2)

regular-character orthogonality gives the exact all-group formulas

    ||Ehat_0||_F^2 = t d^(2K-2) [1+(d-1)/2^K],
    ||Ehat_S||_F^2 = t d^(2K-2) (d-1)/2^K,  S != 0.      (3)

The proof is local to each source pair.  For
``A_+/-=(L(g) tensor I +/- I tensor L(g))/2``, the Hilbert--Schmidt inner
product vanishes unless the two group elements agree.  At a nonidentity
element both signs have squared norm ``d^2/2``; at the identity the minus
factor vanishes and the plus factor has squared norm ``d^2``.

Equation (3) has a direct polar meaning.  Let ``R`` stack the ``E_e``, put
``F=R*R``, and let ``Q=R F^(+/2)`` be the exact orientation polar.  On the
canonical native input ``sigma=F/Tr(F)``, Walsh transforming the output mask
gives

    Pr[S] = ||Ehat_S||_F^2/r.                            (4)

Therefore

    Pr[0]   = 1/d + (d-1)/(d 2^K),
    Pr[S!=0]= (d-1)/(d 2^K).                             (5)

At ``d=n!`` and ``K=ceil(log2 d)+2``, this distribution is asymptotically
flat across the factorial number of Walsh characters.  A fixed set of ``m``
nonzero modes retains at most

    1/d + (d-1)(m+1)/(d 2^K)                            (6)

of the ideal native polar output.  Polynomial ``m`` has vanishing mass, and
fixed low-degree Walsh truncations are rejected exactly.

This does not make the dense Walsh transform hard: a Hadamard uses all modes
efficiently.  It also does not rule out source-label-adaptive sparse sets,
non-Walsh recoupling transforms, or direct rectangular-CS compilation.  The
result is an annealed regular-source no-go for fixed sparse/low-degree output
truncation, not a complete-polar lower bound or a speedup claim.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_regular_master_walsh_flatness_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-WALSH-FLATNESS-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RegularWalshFlatnessControl:
    control_id: str
    group_order: int
    target_dimension: int
    copy_count: int
    orientation_count: int
    carrier_dimension: int
    orientation_projector_rank: int
    maximum_projector_residual: float
    constant_mode_energy: float
    predicted_constant_mode_energy: float
    minimum_nonzero_mode_energy: float
    maximum_nonzero_mode_energy: float
    predicted_nonzero_mode_energy: float
    maximum_mode_energy_formula_residual: float
    parseval_residual: float
    maximum_native_polar_probability_residual: float
    native_polar_probability_sum_residual: float
    exact_regular_walsh_flatness_verified: bool
    exact_native_polar_output_law_verified: bool
    status: str


@dataclass(frozen=True)
class WalshTruncationScalingRecord:
    n: int
    group_order_decimal: str
    copy_count: int
    orientation_count_decimal: str
    zero_mode_probability: float
    each_nonzero_mode_probability: float
    total_nonzero_mode_probability: float
    polynomial_mode_budget: int
    best_fixed_polynomial_mode_retained_probability: float
    quarter_degree_cutoff: int
    quarter_degree_nonzero_mode_count_decimal: str
    quarter_degree_retained_probability: float
    minimum_nonzero_modes_for_ninety_percent_decimal: str
    minimum_mode_fraction_for_ninety_percent: float
    fixed_polynomial_mode_truncation_retains_constant_mass: bool
    fixed_quarter_degree_truncation_retains_constant_mass: bool
    source_adaptive_sparse_mode_no_go_proved: bool
    complete_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class RegularWalshFlatnessTheorem:
    projector_rank: str
    mode_energy: str
    native_polar_law: str
    sparse_truncation: str
    low_degree: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RegularWalshFlatnessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RegularWalshFlatnessTheorem
    finite_controls: list[RegularWalshFlatnessControl]
    scaling_records: list[WalshTruncationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _cyclic_left_regular(order: int, element: int) -> np.ndarray:
    matrix = np.zeros((order, order), dtype=complex)
    for source in range(order):
        matrix[(source + element) % order, source] = 1.0
    return matrix


def _cyclic_target_rows(
    order: int,
    characters: tuple[int, ...],
) -> tuple[np.ndarray, ...]:
    if order < 2 or not characters:
        raise ValueError("a nontrivial cyclic group and target are required")
    return tuple(
        np.diag(
            [
                np.exp(2j * math.pi * character * element / order)
                for character in characters
            ]
        )
        for element in range(order)
    )


def _kron_all(factors: list[np.ndarray]) -> np.ndarray:
    output = np.asarray([[1.0]], dtype=complex)
    for factor in factors:
        output = np.kron(output, factor)
    return output


def cyclic_regular_orientation_projectors(
    group_order: int,
    target_characters: tuple[int, ...],
    copy_count: int,
) -> tuple[np.ndarray, ...]:
    if copy_count < 1:
        raise ValueError("copy count must be positive")
    regular = tuple(
        _cyclic_left_regular(group_order, element)
        for element in range(group_order)
    )
    target = _cyclic_target_rows(group_order, target_characters)
    identity = np.eye(group_order, dtype=complex)
    projectors = []
    for orientation in range(1 << copy_count):
        accumulator = None
        for element in range(group_order):
            factors = [target[element]]
            for pair_index in range(copy_count):
                if orientation & (1 << pair_index):
                    factors.extend((identity, regular[element]))
                else:
                    factors.extend((regular[element], identity))
            term = _kron_all(factors)
            accumulator = term if accumulator is None else accumulator + term
        if accumulator is None:
            raise ArithmeticError("empty group average")
        projector = accumulator / group_order
        projectors.append((projector + projector.conj().T) / 2.0)
    return tuple(projectors)


def walsh_modes(projectors: tuple[np.ndarray, ...]) -> tuple[np.ndarray, ...]:
    if not projectors or len(projectors) & (len(projectors) - 1):
        raise ValueError("a nonempty power-of-two projector family is required")
    if any(projector.shape != projectors[0].shape for projector in projectors):
        raise ValueError("projectors must share one carrier space")
    count = len(projectors)
    modes = []
    for character in range(count):
        mode = np.zeros_like(projectors[0])
        for orientation, projector in enumerate(projectors):
            sign = -1 if (character & orientation).bit_count() & 1 else 1
            mode += sign * projector
        modes.append(mode / count)
    return tuple(modes)


def regular_walsh_mode_energy_formula(
    group_order: int,
    target_dimension: int,
    copy_count: int,
) -> tuple[float, float, int]:
    if group_order < 2 or target_dimension < 1 or copy_count < 1:
        raise ValueError("positive dimensions and a nontrivial group are required")
    count = 1 << copy_count
    scale = target_dimension * group_order ** (2 * copy_count - 2)
    constant = scale * (1.0 + (group_order - 1) / count)
    nonzero = scale * (group_order - 1) / count
    rank = target_dimension * group_order ** (2 * copy_count - 1)
    return float(constant), float(nonzero), rank


def native_polar_walsh_probabilities(
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[float, ...]:
    """Compute equation (4) directly from the exact polar and native state."""

    modes = walsh_modes(projectors)
    count = len(projectors)
    frame = sum(projectors, np.zeros_like(projectors[0]))
    values, vectors = np.linalg.eigh((frame + frame.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > 100 * tolerance] = 1.0 / np.sqrt(values[values > 100 * tolerance])
    inverse_root = (vectors * inverse) @ vectors.conj().T
    native = frame / float(np.trace(frame).real)
    probabilities = []
    for mode in modes:
        polar_row = math.sqrt(count) * mode @ inverse_root
        probability = np.trace(polar_row @ native @ polar_row.conj().T).real
        probabilities.append(float(probability))
    return tuple(probabilities)


def audit_regular_walsh_flatness(
    control_id: str,
    group_order: int,
    target_characters: tuple[int, ...],
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> RegularWalshFlatnessControl:
    projectors = cyclic_regular_orientation_projectors(
        group_order,
        target_characters,
        copy_count,
    )
    modes = walsh_modes(projectors)
    energies = [float(np.linalg.norm(mode, ord="fro") ** 2) for mode in modes]
    predicted_constant, predicted_nonzero, rank = regular_walsh_mode_energy_formula(
        group_order,
        len(target_characters),
        copy_count,
    )
    probabilities = native_polar_walsh_probabilities(
        projectors,
        tolerance=tolerance,
    )
    predicted_probabilities = (
        predicted_constant / rank,
        *((predicted_nonzero / rank,) * (len(projectors) - 1)),
    )
    projector_residual = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    formula_residual = max(
        abs(energies[0] - predicted_constant),
        *(abs(energy - predicted_nonzero) for energy in energies[1:]),
    )
    parseval = abs(sum(energies) - rank)
    probability_residual = max(
        abs(actual - predicted)
        for actual, predicted in zip(probabilities, predicted_probabilities)
    )
    probability_sum = abs(sum(probabilities) - 1.0)
    energy_scale = max(predicted_constant, predicted_nonzero, 1.0)
    flat = bool(
        projector_residual <= 100 * tolerance
        and formula_residual <= 1000 * tolerance * energy_scale
        and parseval <= 1000 * tolerance * rank
    )
    polar = bool(
        probability_residual <= 1000 * tolerance
        and probability_sum <= 1000 * tolerance
    )
    return RegularWalshFlatnessControl(
        control_id=control_id,
        group_order=group_order,
        target_dimension=len(target_characters),
        copy_count=copy_count,
        orientation_count=len(projectors),
        carrier_dimension=projectors[0].shape[0],
        orientation_projector_rank=rank,
        maximum_projector_residual=projector_residual,
        constant_mode_energy=energies[0],
        predicted_constant_mode_energy=predicted_constant,
        minimum_nonzero_mode_energy=min(energies[1:]),
        maximum_nonzero_mode_energy=max(energies[1:]),
        predicted_nonzero_mode_energy=predicted_nonzero,
        maximum_mode_energy_formula_residual=formula_residual,
        parseval_residual=parseval,
        maximum_native_polar_probability_residual=probability_residual,
        native_polar_probability_sum_residual=probability_sum,
        exact_regular_walsh_flatness_verified=flat,
        exact_native_polar_output_law_verified=polar,
        status=(
            "regular-walsh-flatness-and-native-polar-law-verified"
            if flat and polar
            else "regular-walsh-flatness-control-failure"
        ),
    )


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def walsh_truncation_scaling_record(n: int) -> WalshTruncationScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    group_order = math.factorial(n)
    copies = (group_order - 1).bit_length() + 2
    count = 1 << copies
    zero = Fraction(count + group_order - 1, group_order * count)
    nonzero = Fraction(group_order - 1, group_order * count)
    polynomial_budget = min(count - 1, copies**6)
    polynomial_retained = zero + polynomial_budget * nonzero
    cutoff = copies // 4
    low_degree_modes = sum(math.comb(copies, degree) for degree in range(1, cutoff + 1))
    low_degree_retained = zero + low_degree_modes * nonzero
    needed = _ceil_fraction((Fraction(9, 10) - zero) / nonzero)
    return WalshTruncationScalingRecord(
        n=n,
        group_order_decimal=str(group_order),
        copy_count=copies,
        orientation_count_decimal=str(count),
        zero_mode_probability=float(zero),
        each_nonzero_mode_probability=float(nonzero),
        total_nonzero_mode_probability=float((count - 1) * nonzero),
        polynomial_mode_budget=polynomial_budget,
        best_fixed_polynomial_mode_retained_probability=float(polynomial_retained),
        quarter_degree_cutoff=cutoff,
        quarter_degree_nonzero_mode_count_decimal=str(low_degree_modes),
        quarter_degree_retained_probability=float(low_degree_retained),
        minimum_nonzero_modes_for_ninety_percent_decimal=str(needed),
        minimum_mode_fraction_for_ninety_percent=float(Fraction(needed, count)),
        fixed_polynomial_mode_truncation_retains_constant_mass=False,
        fixed_quarter_degree_truncation_retains_constant_mass=False,
        source_adaptive_sparse_mode_no_go_proved=False,
        complete_orientation_polar_compiled=False,
        status="fixed-sparse-walsh-truncation-rejected-dense-structured-route-open",
    )


def regular_walsh_flatness_theorem() -> RegularWalshFlatnessTheorem:
    return RegularWalshFlatnessTheorem(
        projector_rank="rank(E_e)=t d^(2K-1)",
        mode_energy=(
            "||Ehat_0||F^2=t d^(2K-2)(1+(d-1)/2^K); every "
            "nonzero mode has t d^(2K-2)(d-1)/2^K"
        ),
        native_polar_law=(
            "for sigma=F/Tr(F), the Walsh-output probability of Q=R F^(+/2) "
            "is ||Ehat_S||F^2/rank(E_e)"
        ),
        sparse_truncation=(
            "a fixed set of m nonzero modes retains at most "
            "1/d+(d-1)(m+1)/(d 2^K) native polar mass"
        ),
        low_degree=(
            "degree at most K/4 contains sum_(j<=K/4) binom(K,j) modes and "
            "therefore vanishing native mass at the factorial schedule"
        ),
        scope=(
            "annealed regular-source and fixed mode sets only; dense structured "
            "Walsh transforms, source-adaptive mode sets, recoupling, direct CS, "
            "and complete-polar compilation remain open"
        ),
        theorem_verified=True,
        status="regular-master-native-polar-walsh-flatness-proved",
    )


def run_regular_master_walsh_flatness_no_go() -> RegularWalshFlatnessReport:
    controls = [
        audit_regular_walsh_flatness("C2-K2-TWO-CHARACTER", 2, (0, 1), 2),
        audit_regular_walsh_flatness("C3-K1-NONTRIVIAL-CHARACTER", 3, (1,), 1),
        audit_regular_walsh_flatness("C3-K2-TWO-CHARACTER", 3, (0, 1), 2),
    ]
    scaling = [
        walsh_truncation_scaling_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 48, 64, 96, 128)
    ]
    theorem = regular_walsh_flatness_theorem()
    failures = sum(
        not (
            row.exact_regular_walsh_flatness_verified
            and row.exact_native_polar_output_law_verified
        )
        for row in controls
    )
    verified = theorem.theorem_verified and failures == 0
    return RegularWalshFlatnessReport(
        created_at=utc_now(),
        theorem_contract={
            "rank": theorem.projector_rank,
            "mode_energy": theorem.mode_energy,
            "native_polar": theorem.native_polar_law,
            "sparse_bound": theorem.sparse_truncation,
            "low_degree": theorem.low_degree,
            "scope": theorem.scope,
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compute_regular_source_orientation_walsh_energy_exactly",
                "resolved": verified,
                "resolution": (
                    "The regular character makes every source-pair Hilbert--"
                    "Schmidt kernel diagonal in the averaged group element."
                ),
            },
            {
                "obligation": "transfer_mode_energy_to_native_exact_polar_output",
                "resolved": verified,
                "resolution": (
                    "F/Tr(F) cancels F^(+/2) in the polar row probability, "
                    "leaving ||Ehat_S||F^2/rank(E_e)."
                ),
            },
            {
                "obligation": "test_fixed_low_degree_or_polynomial_walsh_mode_router",
                "resolved": verified,
                "resolution": (
                    "Every nonzero mode has equal mass, so polynomially many "
                    "fixed modes and the quarter-degree ball retain vanishing mass."
                ),
            },
            {
                "obligation": "rule_out_source_label_adaptive_sparse_mode_sets",
                "resolved": False,
                "resolution": (
                    "The regular-master average does not prevent a reversible "
                    "mode set that changes with the measured source labels."
                ),
            },
            {
                "obligation": "compile_dense_structured_orientation_polar",
                "resolved": False,
                "resolution": (
                    "Walsh density is not circuit hardness; Hadamards expose all "
                    "modes, while the rectangular-CS normalization remains open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The frame F itself has exponentially many Walsh modes.",
                "resolved": True,
                "resolution": (
                    "False: F=sum_e E_e is the zero mode. The theorem concerns "
                    "the branch-resolved analysis/polar output, not sparse storage of F."
                ),
            },
            {
                "objection": "Flat Walsh output proves the dense transform is hard.",
                "resolved": True,
                "resolution": (
                    "False. A tensor Hadamard produces a flat spectrum in "
                    "polynomial depth; only truncation to fixed few modes is rejected."
                ),
            },
            {
                "objection": "A source-dependent polynomial character set is also ruled out.",
                "resolved": True,
                "resolution": (
                    "Not by this annealed identity. Its selected modes may vary "
                    "across Fourier source blocks and must be analyzed separately."
                ),
            },
            {
                "objection": "Raw projector Frobenius mass may be irrelevant to the PGM polar.",
                "resolved": True,
                "resolution": (
                    "The exact native-state cancellation in equation (4) makes "
                    "the same energy the ideal polar's output probability."
                ),
            },
        ],
        headline_metrics={
            "exact_regular_walsh_energy_theorem_count": int(verified),
            "exact_native_polar_walsh_output_law_count": int(verified),
            "fixed_sparse_mode_truncation_no_go_count": int(verified),
            "fixed_low_degree_truncation_no_go_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_mode_energy_formula_residual": max(
                row.maximum_mode_energy_formula_residual for row in controls
            ),
            "maximum_native_probability_residual": max(
                row.maximum_native_polar_probability_residual for row in controls
            ),
            "scaling_record_count": len(scaling),
            "tail_fixed_polynomial_mode_retained_probability": (
                scaling[-1].best_fixed_polynomial_mode_retained_probability
            ),
            "tail_quarter_degree_retained_probability": (
                scaling[-1].quarter_degree_retained_probability
            ),
            "tail_minimum_mode_fraction_for_ninety_percent": (
                scaling[-1].minimum_mode_fraction_for_ninety_percent
            ),
            "source_adaptive_sparse_mode_no_go_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "regular_source_walsh_mode_energy_flatness_proved": verified,
            "native_exact_polar_walsh_output_law_proved": verified,
            "fixed_polynomial_walsh_mode_truncation_rejected": verified,
            "fixed_low_degree_walsh_truncation_rejected": verified,
            "frame_F_requires_dense_walsh_storage": False,
            "dense_walsh_transform_hardness_proved": False,
            "source_label_adaptive_sparse_mode_router_rejected": False,
            "direct_recoupling_or_rectangular_cs_rejected": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The ideal native polar has asymptotically flat regular-source "
                "Walsh output, killing fixed sparse/low-degree truncations but "
                "not dense structured or source-adaptive compilers."
            ),
        },
        status=(
            "regular-native-polar-walsh-flat-fixed-sparse-truncation-rejected"
            if verified
            else "regular-walsh-flatness-control-failure"
        ),
        summary=(
            "Proved exact regular-source Walsh flatness and transferred it to "
            "the native ideal polar output, rejecting every fixed polynomial "
            "mode and low-degree truncation strategy."
        ),
        falsifiers_triggered=[
            "Fixed low-degree orientation characters cannot retain constant native ideal-PGM mass.",
            "No fixed polynomial set of Walsh modes approximates the regular-source polar output.",
            "The frame sum F is still only the zero mode; this is not a storage lower bound for F.",
            "Walsh density is not dense-transform circuit hardness and does not reject source-adaptive recoupling.",
        ],
    )


def write_regular_master_walsh_flatness_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(run_regular_master_walsh_flatness_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_regular_master_walsh_flatness_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
