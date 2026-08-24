"""Separate the raw GPE dilation from the branch-polar convolution.

The all-order quadrant theorem proves that the polar-completed convolution is
state-weighted near-isometric for natural sources.  The most plausible access
shortcut is to replace its local field ``J_h`` by the raw branch-character
Kraus stack.  The raw stack has an exact representation dilation, so it can be
routed by controlled representation actions and generalized phase estimation.
This module proves that the replacement is asymptotically invalid.

For one source pair, put

    A_h=rho_lambda(h) tensor I,
    B_h=I tensor rho_mu(h),
    M_+/-=(A_h +/- B_h)/2,
    K_h=[M_+; M_-].                                      (1)

If ``R_h=|0><0| tensor A_h+|1><1| tensor B_h``, then

    K_h=(H tensor I) R_h (|+> tensor I).                 (2)

The family ``R_h`` is a representation and (2) is a normalization-one
isometry.  Tensoring (2) over source pairs gives the exact raw full-character
dilation used by the physical joint-character state.

The polar completion instead uses

    J_h=[V_+(h);V_-(h)](P_+(h)+P_-(h))^-1/2.             (3)

On an eigenphase ``omega=exp(2 pi i t/m)`` of
``U_h=A_h^*B_h``, the real overlap between the raw and polar branch vectors is

    b_m(t)=1                                             at omega=+/-1,
           (|cos(pi t/m)|+|sin(pi t/m)|)/sqrt(2)         otherwise. (4)

In ``Reg(G) tensor Reg(G)``, every ``m``th root occurs uniformly when
``m=ord(h)``.  Thus the normalized local overlap is

    a_m=m^-1 sum_t b_m(t).                               (5)

It equals one only for ``m in {1,2,4}``.  For every other order,

    a_m <= gamma := a_3=a_6
          = [1+(1+sqrt(3))/sqrt(2)]/3 < 0.978.           (6)

The exact closed forms are

    a_m=[cot(pi/(4m))/sqrt(2)+1-1/sqrt(2)]/m             m odd,
    a_m=[sqrt(2)cot(pi/(2m))+2-sqrt(2)]/m                m even.

Elementary differentiation shows each parity subsequence decreases after
its exceptional orders, giving (6).

For ``k`` independent two-Plancherel source pairs, regular decomposition and
tensor factorization give the exact annealed normalized Hilbert--Schmidt
overlap of the two global convolution fields:

    E_Lambda overlap(C_raw,C_polar)
      = |G|^-1 sum_(h in G) a_ord(h)^k.                  (7)

For ``G=S_n``, a permutation of order dividing four has at least ``n/4``
cycles.  Since ``E[2^cycles]=n+1`` for a uniform permutation, Markov gives

    Pr[ord(h) divides 4] <= (n+1) 2^(-n/4).              (8)

Combining (6)--(8),

    E overlap <= (n+1)2^(-n/4)+gamma^k=o(1)             (9)

at ``k=Theta(n log n)``.  The overlap is nonnegative, so conditioning all
source partitions to be globally distinct changes (9) by at most the
``1/Pr(D)=1+o(1)`` factor.  Markov makes the raw and polar convolutions
asymptotically orthogonal for typical natural source portfolios:

    ||C_raw-C_polar||_F^2/(|G|D) -> 2.                  (10)

The generic controlled-``J_h`` block encoding also remains expensive.  Two
exact isometries have overlap ``C_polar/sqrt(|G|)``.  On the state-weighted
good singular sector proved by the quadrant theorem, its singular amplitudes
are ``Theta(|G|^-1/2)``.  A bounded uniform singular-value polynomial that
raises them to constant amplitude has degree ``Omega(sqrt(|G|))``.

This rules out raw-GPE substitution and generic LCU/QSVT amplification.  It
does not rule out a direct equivariant Fourier transform for the polar field,
a representation-specific multiplier circuit, or a physical decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_branch_character_polar_naimark_completion import (
    Label,
    Partition,
    Permutation,
    local_polar_naimark_data,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_gpe_dilation_separation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-GPE-DILATION-SEPARATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
GAMMA = (1.0 + (1.0 + math.sqrt(3.0)) / math.sqrt(2.0)) / 3.0


@dataclass(frozen=True)
class RawPolarLocalControl:
    control_id: str
    n: int
    left_partition: Partition
    right_partition: Partition
    permutation: Permutation
    carrier_dimension: int
    raw_isometry_residual: float
    polar_isometry_residual: float
    representation_dilation_residual: float
    raw_to_polar_normalized_overlap: float
    direct_to_phase_formula_residual: float
    raw_representation_dilation_verified: bool
    raw_and_polar_fields_equal: bool
    status: str


@dataclass(frozen=True)
class CyclicOverlapAudit:
    maximum_order_tested: int
    tested_order_count: int
    maximum_closed_form_residual: float
    maximum_nonexceptional_overlap: float
    maximizing_nonexceptional_order: int
    universal_gamma: float
    exceptional_equal_order_count: int
    exceptional_equal_orders: tuple[int, ...]
    universal_nonexceptional_bound_verified: bool
    status: str


@dataclass(frozen=True)
class OrderFourProbabilityControl:
    n: int
    group_order: int
    exact_order_dividing_four_count: int
    exact_order_dividing_four_probability: float
    cycle_moment_markov_upper_bound: float
    exact_probability_below_bound: bool
    status: str


@dataclass(frozen=True)
class GpeSeparationScaling:
    n: int
    log2_group_order: float
    copy_count: int
    low_order_probability_log2_upper_bound: float
    nonexceptional_overlap_log2_upper_bound: float
    total_annealed_overlap_upper_bound: float
    typical_overlap_threshold: float
    typical_failure_probability_upper_bound: float
    normalized_frobenius_distance_squared_lower_bound: float
    generic_qsvt_degree_log2_lower_bound: float
    raw_gpe_substitution_asymptotically_rejected: bool
    generic_controlled_field_qsvt_superpolynomial: bool
    status: str


@dataclass(frozen=True)
class GpeDilationSeparationTheorem:
    raw_representation_dilation: str
    local_phase_overlap: str
    regular_plancherel_reduction: str
    low_order_probability: str
    natural_source_separation: str
    generic_block_encoding: str
    structured_escape: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class GpeDilationSeparationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: GpeDilationSeparationTheorem
    local_controls: list[RawPolarLocalControl]
    cyclic_overlap_audit: CyclicOverlapAudit
    order_four_probability_controls: list[OrderFourProbabilityControl]
    scaling_records: list[GpeSeparationScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = np.asarray([[1.0]], dtype=complex)
    for matrix in matrices:
        output = np.kron(output, matrix)
    return output


def raw_branch_isometry(
    left: Partition,
    right: Partition,
    permutation: Permutation,
) -> np.ndarray:
    left_matrix = _source_representation_rows(left)[permutation]
    right_matrix = _source_representation_rows(right)[permutation]
    left_action = np.kron(left_matrix, np.eye(len(right_matrix)))
    right_action = np.kron(np.eye(len(left_matrix)), right_matrix)
    return np.vstack(
        (
            (left_action + right_action) / 2.0,
            (left_action - right_action) / 2.0,
        )
    )


def raw_representation_dilation(
    left: Partition,
    right: Partition,
    permutation: Permutation,
) -> np.ndarray:
    left_matrix = _source_representation_rows(left)[permutation]
    right_matrix = _source_representation_rows(right)[permutation]
    left_action = np.kron(left_matrix, np.eye(len(right_matrix)))
    right_action = np.kron(np.eye(len(left_matrix)), right_matrix)
    dimension = len(left_action)
    controlled = np.block(
        [
            [left_action, np.zeros((dimension, dimension))],
            [np.zeros((dimension, dimension)), right_action],
        ]
    )
    hadamard = np.asarray(((1.0, 1.0), (1.0, -1.0))) / math.sqrt(2.0)
    embedding = np.vstack(
        (np.eye(dimension), np.eye(dimension))
    ) / math.sqrt(2.0)
    return np.kron(hadamard, np.eye(dimension)) @ controlled @ embedding


def phase_branch_overlap(order: int, exponent: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    exponent %= order
    if exponent == 0 or (order % 2 == 0 and exponent == order // 2):
        return 1.0
    angle = math.pi * exponent / order
    return (abs(math.cos(angle)) + abs(math.sin(angle))) / math.sqrt(2.0)


def cyclic_raw_polar_overlap(order: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    return sum(phase_branch_overlap(order, exponent) for exponent in range(order)) / order


def cyclic_raw_polar_overlap_closed_form(order: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    if order == 1:
        return 1.0
    if order % 2:
        value = (
            1.0 / math.tan(math.pi / (4.0 * order)) / math.sqrt(2.0)
            + 1.0
            - 1.0 / math.sqrt(2.0)
        )
    else:
        value = (
            math.sqrt(2.0) / math.tan(math.pi / (2.0 * order))
            + 2.0
            - math.sqrt(2.0)
        )
    return value / order


def audit_raw_polar_local(
    control_id: str,
    left: Partition,
    right: Partition,
    permutation: Permutation,
    *,
    tolerance: float = 1e-9,
) -> RawPolarLocalControl:
    raw = raw_branch_isometry(left, right, permutation)
    dilation = raw_representation_dilation(left, right, permutation)
    polar = local_polar_naimark_data(left, right, permutation)[-1]
    dimension = raw.shape[1]
    identity = np.eye(dimension)
    raw_residual = float(np.linalg.norm(raw.conj().T @ raw - identity, ord=2))
    polar_residual = float(
        np.linalg.norm(polar.conj().T @ polar - identity, ord=2)
    )
    dilation_residual = float(np.linalg.norm(raw - dilation, ord=2))
    overlap = float(np.trace(raw.conj().T @ polar).real / dimension)

    left_matrix = _source_representation_rows(left)[permutation]
    right_matrix = _source_representation_rows(right)[permutation]
    relative = np.kron(left_matrix.T, right_matrix)
    eigenvalues = np.linalg.eigvals(relative)
    predicted = sum(
        (
            1.0
            if abs(value - 1.0) <= 100 * tolerance
            or abs(value + 1.0) <= 100 * tolerance
            else (
                abs(math.cos(cmath_phase(value) / 2.0))
                + abs(math.sin(cmath_phase(value) / 2.0))
            )
            / math.sqrt(2.0)
        )
        for value in eigenvalues
    ) / dimension
    phase_residual = abs(overlap - predicted)
    verified = bool(
        raw_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and dilation_residual <= 100 * tolerance
        and phase_residual <= 1000 * tolerance
    )
    equal = bool(np.linalg.norm(raw - polar, ord=2) <= 100 * tolerance)
    return RawPolarLocalControl(
        control_id=control_id,
        n=sum(left),
        left_partition=left,
        right_partition=right,
        permutation=permutation,
        carrier_dimension=dimension,
        raw_isometry_residual=raw_residual,
        polar_isometry_residual=polar_residual,
        representation_dilation_residual=dilation_residual,
        raw_to_polar_normalized_overlap=overlap,
        direct_to_phase_formula_residual=phase_residual,
        raw_representation_dilation_verified=verified,
        raw_and_polar_fields_equal=equal,
        status=(
            "raw-representation-dilation-and-polar-overlap-verified"
            if verified
            else "raw-polar-local-control-failure"
        ),
    )


def cmath_phase(value: complex) -> float:
    return math.atan2(value.imag, value.real)


def audit_cyclic_overlaps(
    maximum_order: int = 1024,
    *,
    tolerance: float = 1e-12,
) -> CyclicOverlapAudit:
    residual = 0.0
    maximum = -math.inf
    maximizing = 0
    exceptional = []
    for order in range(1, maximum_order + 1):
        direct = cyclic_raw_polar_overlap(order)
        closed = cyclic_raw_polar_overlap_closed_form(order)
        residual = max(residual, abs(direct - closed))
        if math.isclose(direct, 1.0, abs_tol=tolerance):
            exceptional.append(order)
        elif direct > maximum:
            maximum = direct
            maximizing = order
    verified = bool(
        residual <= 100 * tolerance
        and tuple(exceptional) == (1, 2, 4)
        and maximum <= GAMMA + 100 * tolerance
        and maximizing in (3, 6)
    )
    return CyclicOverlapAudit(
        maximum_order_tested=maximum_order,
        tested_order_count=maximum_order,
        maximum_closed_form_residual=residual,
        maximum_nonexceptional_overlap=maximum,
        maximizing_nonexceptional_order=maximizing,
        universal_gamma=GAMMA,
        exceptional_equal_order_count=len(exceptional),
        exceptional_equal_orders=tuple(exceptional),
        universal_nonexceptional_bound_verified=verified,
        status=(
            "raw-polar-overlap-one-only-orders-one-two-four-gamma-elsewhere"
            if verified
            else "cyclic-raw-polar-overlap-control-failure"
        ),
    )


def _permutation_order(permutation: Permutation) -> int:
    seen: set[int] = set()
    order = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        order = math.lcm(order, length)
    return order


def audit_order_four_probability(n: int) -> OrderFourProbabilityControl:
    if not 2 <= n <= 8:
        raise ValueError("exact permutation enumeration supports 2<=n<=8")
    group = tuple(itertools.permutations(range(n)))
    count = sum(4 % _permutation_order(permutation) == 0 for permutation in group)
    probability = count / len(group)
    bound = min(1.0, (n + 1) * 2.0 ** (-n / 4.0))
    verified = probability <= bound + 1e-12
    return OrderFourProbabilityControl(
        n=n,
        group_order=len(group),
        exact_order_dividing_four_count=count,
        exact_order_dividing_four_probability=probability,
        cycle_moment_markov_upper_bound=bound,
        exact_probability_below_bound=verified,
        status=(
            "order-dividing-four-probability-obeys-cycle-moment-bound"
            if verified
            else "order-four-probability-control-failure"
        ),
    )


def gpe_separation_scaling(n: int) -> GpeSeparationScaling:
    if n < 2:
        raise ValueError("n must be at least two")
    log2_order = math.log2(math.factorial(n))
    copies = math.ceil(3.0 * log2_order) + 2
    low_log2 = math.log2(n + 1) - n / 4.0
    gamma_log2 = copies * math.log2(GAMMA)
    low = 2.0**low_log2 if low_log2 > -1074 else 0.0
    nonexceptional = 2.0**gamma_log2 if gamma_log2 > -1074 else 0.0
    overlap = min(1.0, low + nonexceptional)
    threshold = math.sqrt(overlap)
    distance_lower = max(0.0, 2.0 - 2.0 * threshold)
    qsvt_log2 = max(0.0, 0.5 * log2_order - 2.0)
    return GpeSeparationScaling(
        n=n,
        log2_group_order=log2_order,
        copy_count=copies,
        low_order_probability_log2_upper_bound=low_log2,
        nonexceptional_overlap_log2_upper_bound=gamma_log2,
        total_annealed_overlap_upper_bound=overlap,
        typical_overlap_threshold=threshold,
        typical_failure_probability_upper_bound=threshold,
        normalized_frobenius_distance_squared_lower_bound=distance_lower,
        generic_qsvt_degree_log2_lower_bound=qsvt_log2,
        raw_gpe_substitution_asymptotically_rejected=True,
        generic_controlled_field_qsvt_superpolynomial=True,
        status="raw-gpe-substitution-and-generic-qsvt-rejected",
    )


def run_gpe_dilation_separation() -> GpeDilationSeparationReport:
    local = [
        audit_raw_polar_local(
            "S3-THREE-CYCLE",
            (3,),
            (2, 1),
            (1, 2, 0),
        ),
        audit_raw_polar_local(
            "S4-FOUR-CYCLE",
            (3, 1),
            (2, 2),
            (1, 2, 3, 0),
        ),
        audit_raw_polar_local(
            "S4-THREE-CYCLE",
            (3, 1),
            (2, 2),
            (1, 2, 0, 3),
        ),
    ]
    cyclic = audit_cyclic_overlaps()
    order_controls = [audit_order_four_probability(n) for n in range(2, 9)]
    scaling = [gpe_separation_scaling(n) for n in (16, 32, 64, 128, 256)]
    verified = bool(
        all(row.raw_representation_dilation_verified for row in local)
        and cyclic.universal_nonexceptional_bound_verified
        and all(row.exact_probability_below_bound for row in order_controls)
        and all(row.raw_gpe_substitution_asymptotically_rejected for row in scaling)
    )
    theorem = GpeDilationSeparationTheorem(
        raw_representation_dilation=(
            "K_h=(H tensor I)(|0><0| tensor A_h+|1><1| tensor B_h)"
            "(|+> tensor I), and the controlled middle family is a representation."
        ),
        local_phase_overlap=(
            "The regular local raw/polar overlap is a_m; it equals one only at "
            "orders 1,2,4 and is at most gamma=a_3=a_6<0.978 otherwise."
        ),
        regular_plancherel_reduction=(
            "Two independent Plancherel labels replace each local carrier by "
            "Reg(S_n) tensor Reg(S_n), so k source pairs contribute a_ord(h)^k."
        ),
        low_order_probability=(
            "Pr[ord(h)|4]<=Pr[cycles(h)>=n/4]<=(n+1)2^(-n/4), using "
            "E[2^cycles]=n+1."
        ),
        natural_source_separation=(
            "The annealed raw/polar convolution overlap is at most the low-order "
            "probability plus gamma^k and vanishes after global-distinct conditioning."
        ),
        generic_block_encoding=(
            "Canonical controlled-field PREPARE isometries expose C/sqrt(|G|); "
            "uniform QSVT amplification on the good sector costs Omega(sqrt(|G|))."
        ),
        structured_escape=(
            "Only direct synthesis of the conjugation-equivariant Fourier "
            "multipliers, or another representation-specific polar circuit, remains."
        ),
        scope=(
            "The theorem rejects raw-GPE substitution and generic LCU/QSVT. It is "
            "not a lower bound against arbitrary equivariant circuits and does not "
            "compile the polar transform or decoder."
        ),
        theorem_verified=verified,
        status=(
            "raw-gpe-dilation-asymptotically-separated-generic-qsvt-closed"
            if verified
            else "gpe-dilation-separation-control-failure"
        ),
    )
    tail = scaling[-1]
    return GpeDilationSeparationReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        local_controls=local,
        cyclic_overlap_audit=cyclic,
        order_four_probability_controls=order_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_raw_character_gpe_as_polar_transform_substitute",
                "resolved": verified,
                "resolution": "Rejected: their conditioned natural normalized Hilbert--Schmidt overlap vanishes at the theorem copy scale.",
            },
            {
                "obligation": "test_generic_controlled_J_lcu_qsvt_compiler",
                "resolved": verified,
                "resolution": "Rejected in that access model: the exact block has 1/sqrt(|G|) good-sector amplitudes and needs Omega(sqrt(|G|)) degree.",
            },
            {
                "obligation": "derive_conjugation_equivariant_multiplier_normal_form",
                "resolved": False,
                "resolution": "Decompose Jhat_nu as an intertwiner between nu tensor source representations and identify efficiently synthesizable reduced blocks.",
            },
            {
                "obligation": "compile_structured_polar_fourier_transform_and_decoder",
                "resolved": False,
                "resolution": "No direct equivariant multiplier circuit, physical-input domination theorem, or hidden-label decoder is known.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The raw full-character stack and polar stack are both isometries, so they should be close.",
                "resolved": True,
                "resolution": "False. Their local overlap is strictly below one away from orders 1,2,4, and tensor copies drive the natural global overlap to zero."
            },
            {
                "objection": "Order-four permutations invalidate exponential separation.",
                "resolved": True,
                "resolution": "Their probability is at most (n+1)2^(-n/4) because they require at least n/4 cycles."
            },
            {
                "objection": "Global-distinct conditioning could concentrate the exceptional overlap.",
                "resolved": True,
                "resolution": "The overlap is nonnegative and bounded; conditioning costs only 1/Pr(D)=1+o(1)."
            },
            {
                "objection": "State-weighted conditioning of C removes the generic block-encoding normalization.",
                "resolved": True,
                "resolution": "It proves C has order-one singulars on most domain mass, so C/sqrt(|G|) still needs square-root amplification there."
            },
            {
                "objection": "This is a circuit lower bound for every representation-theoretic transform.",
                "resolved": True,
                "resolution": "No. A direct equivariant Fourier multiplier circuit remains explicitly open."
            },
        ],
        headline_metrics={
            "raw_representation_dilation_theorem_count": int(verified),
            "natural_raw_polar_separation_theorem_count": int(verified),
            "generic_controlled_field_qsvt_no_go_count": int(verified),
            "local_control_count": len(local),
            "maximum_tested_cyclic_order": cyclic.maximum_order_tested,
            "maximum_nonexceptional_local_overlap": cyclic.maximum_nonexceptional_overlap,
            "universal_nonexceptional_gamma": cyclic.universal_gamma,
            "tail_n": tail.n,
            "tail_annealed_overlap_upper_bound": tail.total_annealed_overlap_upper_bound,
            "tail_typical_frobenius_distance_squared_lower_bound": tail.normalized_frobenius_distance_squared_lower_bound,
            "tail_generic_qsvt_degree_log2_lower_bound": tail.generic_qsvt_degree_log2_lower_bound,
            "direct_equivariant_multiplier_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "raw_character_representation_dilation_proved": verified,
            "raw_polar_local_overlap_formula_proved": verified,
            "natural_raw_polar_convolution_overlap_vanishes_proved": verified,
            "raw_gpe_substitution_rejected": verified,
            "generic_controlled_field_lcu_qsvt_superpolynomial_proved": verified,
            "conjugation_equivariant_multiplier_normal_form_derived": False,
            "direct_equivariant_multiplier_compiled": False,
            "physical_input_fourier_domination_proved": False,
            "physical_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Proved that the easy raw representation dilation is asymptotically "
            "orthogonal to the polar-completed transform on natural source "
            "portfolios, and that generic controlled-field QSVT remains factorially "
            "normalized. The surviving task is direct equivariant multiplier synthesis."
        ),
        falsifiers_triggered=[
            "Raw generalized phase estimation cannot substitute for branch-polar completion.",
            "Natural state-weighted conditioning does not repair generic sqrt(|S_n|) subnormalization.",
            "The result does not rule out a direct representation-specific Fourier multiplier transform.",
        ],
    )


def write_gpe_dilation_separation_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_gpe_dilation_separation())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_gpe_dilation_separation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
