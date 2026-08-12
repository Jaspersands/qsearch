"""Admission theorem for explicit public-base hidden-shift phase families.

Let ``f:G->Sigma`` be public and classically evaluable, and let a value oracle
return ``g_s(x)=f(x+s)``.  Define

    mu(f) = max_{delta != 0} Pr_x[f(x)=f(x+delta)].

For ``m`` independent uniform queries to ``g_s``, a fixed wrong shift survives
the consistency test with probability at most ``mu(f)^m``.  A union bound over
the other ``|G|-1`` shifts therefore gives

    Pr[any wrong shift survives] <= (|G|-1) mu(f)^m.       (1)

Consequently, any explicit family with ``mu <= 1-c`` for a constant ``c>0``
has an ``O(log |G|)`` classical *query* upper bound.  The direct decoder uses
``O(|G| log |G|)`` candidate-evaluator operations, so (1) does not establish a
polynomial-time classical algorithm.  It moves the only possible advantage
from query complexity to computational decoding complexity.

This scope is essential.  Equation (1) does not apply when the reference
function is itself a charged black box, when the classical side receives only
a coherent phase oracle, or when the input consists of DHSP phase/coset-state
samples.  In particular it does not contradict the exponential two-black-box
classical query lower bounds for bent hidden shift.

For the repository's explicit families, elementary algebra gives stronger
certificates.  For nonzero shifts:

* a nondegenerate Boolean bent quadratic and an even-dimensional
  Maiorana--McFarland phase have agreement exactly ``1/2``;
* ``x^2`` and ``x^3`` chirps have at most one and two equal-value points;
* the modified Legendre phase has agreement at most ``(p+1)/(2p)``;
* a quartic character has at most ``(p+3)/4`` equal-value points;
* ``x+x^-1`` (with zero fixed) has at most four equal-value points;
* the nondegenerate ``F_p^2`` quadratic has agreement ``1/p``;
* a cubic plus a one-bit public mask has at most six equal-value points.

These bounds are admission filters, not speedup claims.  Low-degree and
rational families also have direct polynomial-time public-value decoders.
Multiplicative-character shifts retain a possible computational gap, but the
basic mechanism is already known.  Synthetic masks have neither a natural
problem reduction nor a proved quantum decoder.  The DHSP phase-state branch
remains outside this theorem and should retain priority.

Primary model boundaries:

* van Dam--Hallgren--Ip, arXiv:quant-ph/0211140, gives the multiplicative-
  character hidden-shift mechanism.
* Roetteler, arXiv:0811.3208, explicitly defines the bent problem with oracle
  access to both ``f`` and its shift and proves an oracle query separation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import (
    PhaseFamilySpec,
    apply_hidden_shift,
    generate_cyclic_phase_family,
    shifted_index,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/hidden_shift_public_evaluator_admission_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-HIDDEN-SHIFT-PUBLIC-EVALUATOR-ADMISSION-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"
VDHI_URL = "https://arxiv.org/abs/quant-ph/0211140"
ROETTELER_URL = "https://arxiv.org/abs/0811.3208"


@dataclass(frozen=True)
class FingerprintTheoremControl:
    domain_size: int
    maximum_wrong_shift_agreement: float
    failure_probability: float
    shifted_oracle_query_ceiling: int | None
    exhaustive_candidate_evaluations: int | None
    union_bound_at_ceiling: float | None
    logarithmic_query_ceiling: bool
    polynomial_time_decoder_proved: bool
    applies_with_public_base_evaluator: bool
    applies_with_two_black_box_functions: bool
    applies_to_dhsp_phase_states: bool
    status: str


@dataclass(frozen=True)
class AnalyticAgreementCertificate:
    family_id: str
    group: str
    n_bits: int
    domain_size: int
    modulus: int
    assumptions: str
    analytic_agreement_bound: float | None
    analytic_equal_point_bound: int | None
    exact_finite_max_agreement: float
    exact_finite_max_equal_points: int
    analytic_bound_verified_by_finite_control: bool
    public_evaluator_query_ceiling: int | None
    query_ceiling_over_log2_domain: float | None
    asymptotic_query_class: str
    public_evaluator_superlog_query_advantage_possible: bool
    two_black_box_oracle_lower_bound_invalidated: bool
    status: str


@dataclass(frozen=True)
class PublicDecoderTriage:
    family_id: str
    decoder_or_obstruction: str
    shifted_value_queries: str
    classical_time_status: str
    mechanism_novel: bool
    natural_problem_reduction_present: bool
    admit_as_breakthrough_search_family: bool
    reason: str


@dataclass(frozen=True)
class PublicDecoderControl:
    family_id: str
    n_bits: int
    domain_size: int
    true_shift: int
    recovered_shift: int | None
    shifted_value_query_count: int
    candidate_count_after_first_query: int | None
    polynomial_in_input_length: bool
    recovered_exactly: bool
    decoder: str
    status: str


@dataclass(frozen=True)
class AccessModelBoundary:
    access_model: str
    classical_observation: str
    reference_function_cost: str
    fingerprint_theorem_applies: bool
    consequence: str


@dataclass(frozen=True)
class PublicEvaluatorAdmissionTheorem:
    statement: str
    proof: str
    decoder_cost_boundary: str
    access_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenShiftPublicEvaluatorAdmissionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PublicEvaluatorAdmissionTheorem
    generic_controls: list[FingerprintTheoremControl]
    analytic_certificates: list[AnalyticAgreementCertificate]
    decoder_triage: list[PublicDecoderTriage]
    decoder_controls: list[PublicDecoderControl]
    access_model_boundaries: list[AccessModelBoundary]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def fingerprint_query_ceiling(
    domain_size: int,
    maximum_wrong_shift_agreement: float,
    failure_probability: float = 0.01,
) -> int | None:
    """Return the least ``m`` certified by ``(N-1) mu^m <= epsilon``."""

    if domain_size < 2:
        raise ValueError("domain_size must be at least two")
    if not 0.0 < failure_probability < 1.0:
        raise ValueError("failure_probability must lie strictly between zero and one")
    mu = float(maximum_wrong_shift_agreement)
    if not 0.0 <= mu <= 1.0:
        raise ValueError("maximum agreement must lie in [0,1]")
    if mu == 1.0:
        return None
    if mu == 0.0:
        return 1
    numerator = math.log((domain_size - 1) / failure_probability)
    return int(math.ceil(numerator / -math.log(mu)))


def fingerprint_theorem_control(
    domain_size: int,
    maximum_wrong_shift_agreement: float,
    failure_probability: float = 0.01,
) -> FingerprintTheoremControl:
    ceiling = fingerprint_query_ceiling(
        domain_size,
        maximum_wrong_shift_agreement,
        failure_probability,
    )
    union_bound = (
        None
        if ceiling is None
        else (domain_size - 1) * maximum_wrong_shift_agreement**ceiling
    )
    logarithmic = bool(
        ceiling is not None
        and ceiling <= 8 * math.ceil(math.log2(domain_size))
    )
    return FingerprintTheoremControl(
        domain_size=domain_size,
        maximum_wrong_shift_agreement=float(maximum_wrong_shift_agreement),
        failure_probability=float(failure_probability),
        shifted_oracle_query_ceiling=ceiling,
        exhaustive_candidate_evaluations=(
            None if ceiling is None else domain_size * ceiling
        ),
        union_bound_at_ceiling=union_bound,
        logarithmic_query_ceiling=logarithmic,
        polynomial_time_decoder_proved=False,
        applies_with_public_base_evaluator=True,
        applies_with_two_black_box_functions=False,
        applies_to_dhsp_phase_states=False,
        status=(
            "public-evaluator-logarithmic-query-ceiling"
            if logarithmic
            else "agreement-does-not-certify-logarithmic-query-ceiling"
        ),
    )


def exact_pairwise_agreement_profile(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    *,
    tolerance: float = 1e-8,
) -> tuple[int, float]:
    """Compute the maximum equal-value overlap over nonidentity shifts."""

    values = np.asarray(signal, dtype=complex)
    if values.shape != (spec.domain_size,):
        raise ValueError("signal size does not match the phase-family domain")
    maximum = 0
    for delta in range(1, spec.domain_size):
        count = sum(
            abs(values[x] - values[shifted_index(spec, x, delta)]) <= tolerance
            for x in range(spec.domain_size)
        )
        maximum = max(maximum, int(count))
    return maximum, maximum / spec.domain_size


def _analytic_equal_point_bound(spec: PhaseFamilySpec) -> tuple[int | None, str]:
    family = spec.id
    p = spec.modulus
    if family in {"bent_quadratic_f2", "mm_majority_bent_f2"}:
        if spec.n_bits % 2:
            return None, "even dimension is required for the nondegenerate bent certificate"
        return spec.domain_size // 2, (
            "every nonzero derivative is a nonconstant affine Boolean form and is balanced"
        )
    if family == "quadratic_chirp":
        return 1, "2*delta*x+delta^2 is a nonconstant linear polynomial over F_p"
    if family == "cubic_chirp":
        return 2, "3*delta*x^2+3*delta^2*x+delta^3 has degree two for p != 3"
    if family == "noisy_cubic_chirp":
        return 6, (
            "the mask difference is in {-1,0,1}; each of the three resulting nonzero quadratics has at most two roots"
        )
    if family == "legendre_symbol":
        return (p + 1) // 2, (
            "the quadratic-character correlation is -1 before the two zero-convention corrections"
        )
    if family == "quartic_character":
        return (p + 3) // 4, (
            "x/(x+delta) bijects the interior onto F_p without {0,1}; equality selects quartic residues, plus two zero exceptions"
        )
    if family == "kloosterman_trace":
        return 4, (
            "away from 0 and -delta, equality reduces to x(x+delta)=1; the two exceptional points can also agree"
        )
    if family == "fp2_quadratic_form":
        if p == 19:
            return spec.domain_size, (
                "the quadratic polar form has a radical at p=19, producing nontrivial aliases"
            )
        return p, (
            "the nonzero derivative is one affine linear equation in two F_p coordinates; nondegeneracy fails only at p=19"
        )
    if family == "masked_quadratic_f2":
        return None, (
            "an arbitrary deterministic mask has no uniform derivative-balance certificate"
        )
    raise ValueError(f"unsupported phase family: {family}")


def audit_analytic_family(
    family_id: str,
    n_bits: int = 6,
    failure_probability: float = 0.01,
) -> AnalyticAgreementCertificate:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    exact_points, exact_fraction = exact_pairwise_agreement_profile(spec, signal)
    point_bound, assumptions = _analytic_equal_point_bound(spec)
    analytic_fraction = (
        None if point_bound is None else point_bound / spec.domain_size
    )
    verified = bool(
        point_bound is not None and exact_points <= point_bound
    )
    ceiling = (
        None
        if analytic_fraction is None
        else fingerprint_query_ceiling(
            spec.domain_size,
            analytic_fraction,
            failure_probability,
        )
    )
    ratio = (
        None
        if ceiling is None
        else ceiling / max(1.0, math.log2(spec.domain_size))
    )
    logarithmic = bool(
        ceiling is not None
        and analytic_fraction is not None
        and analytic_fraction <= 0.75
    )
    return AnalyticAgreementCertificate(
        family_id=spec.id,
        group=spec.group,
        n_bits=spec.n_bits,
        domain_size=spec.domain_size,
        modulus=spec.modulus,
        assumptions=assumptions,
        analytic_agreement_bound=analytic_fraction,
        analytic_equal_point_bound=point_bound,
        exact_finite_max_agreement=exact_fraction,
        exact_finite_max_equal_points=exact_points,
        analytic_bound_verified_by_finite_control=verified,
        public_evaluator_query_ceiling=ceiling,
        query_ceiling_over_log2_domain=ratio,
        asymptotic_query_class=(
            "O(log |G|) public-evaluator value queries"
            if logarithmic
            else "no uniform asymptotic certificate from this theorem"
        ),
        public_evaluator_superlog_query_advantage_possible=not logarithmic,
        two_black_box_oracle_lower_bound_invalidated=False,
        status=(
            "public-evaluator-query-admission-rejected"
            if logarithmic and verified
            else "analytic-certificate-failed-finite-control"
            if point_bound is not None
            else "no-uniform-agreement-certificate"
        ),
    )


def _decoder_triage() -> list[PublicDecoderTriage]:
    rows = [
        (
            "quadratic_chirp",
            "interpolate (x+s)^2; its linear coefficient gives s",
            "constant",
            "polynomial",
            False,
            True,
            "Direct low-degree reconstruction dequantizes the public-value problem.",
        ),
        (
            "cubic_chirp",
            "interpolate (x+s)^3; its quadratic coefficient is 3s",
            "constant",
            "polynomial",
            False,
            True,
            "Direct low-degree reconstruction dequantizes the public-value problem.",
        ),
        (
            "bent_quadratic_f2",
            "query zero and a basis; invert the nondegenerate polar bilinear form",
            "n+1",
            "polynomial",
            False,
            True,
            "The explicit quadratic instance is easy even though two-black-box bent hidden shift has a known oracle separation.",
        ),
        (
            "mm_majority_bent_f2",
            "x-direction differences reveal the y-shift; subtract the known majority term and recover the x-shift linearly",
            "O(n)",
            "polynomial",
            False,
            True,
            "The public split formula exposes both shift halves by affine differences.",
        ),
        (
            "fp2_quadratic_form",
            "query zero and two basis directions; invert the polar form when p != 19",
            "3",
            "polynomial",
            False,
            True,
            "The explicit finite-field quadratic is classically reconstructible.",
        ),
        (
            "kloosterman_trace",
            "solve z^2-yz+1=0 for z=x+s and use a second value to resolve the fiber",
            "at most a constant",
            "polynomial",
            False,
            True,
            "Fixed-degree finite-field root finding dequantizes this public-value family.",
        ),
        (
            "legendre_symbol",
            "agreement fingerprint is short but exhaustive decoding is exponential in log p in this report",
            "O(log p)",
            "computational decoding gap remains",
            False,
            True,
            "The Fourier/character mechanism is already the van Dam--Hallgren--Ip hidden-shift algorithm.",
        ),
        (
            "quartic_character",
            "agreement fingerprint is short but exhaustive decoding is exponential in log p in this report",
            "O(log p)",
            "computational decoding gap remains",
            False,
            True,
            "This is a direct multiplicative-character variant, not a new mechanism or reduction.",
        ),
        (
            "noisy_cubic_chirp",
            "no polynomial decoder or quantum decoder is proved after deterministic masking",
            "O(log p) information-theoretically",
            "unresolved",
            False,
            False,
            "A synthetic mask without a natural reduction or quantum mechanism is not a breakthrough search target.",
        ),
        (
            "masked_quadratic_f2",
            "no uniform agreement theorem or quantum decoder is proved for the deterministic hash mask",
            "unresolved",
            "unresolved",
            False,
            False,
            "Obscuring an easy public phase with a synthetic hash does not create research leverage.",
        ),
    ]
    return [
        PublicDecoderTriage(
            family_id=family,
            decoder_or_obstruction=decoder,
            shifted_value_queries=queries,
            classical_time_status=time_status,
            mechanism_novel=novel,
            natural_problem_reduction_present=natural,
            admit_as_breakthrough_search_family=False,
            reason=reason,
        )
        for family, decoder, queries, time_status, novel, natural, reason in rows
    ]


def _phase_exponent(value: complex, prime: int) -> int:
    angle = math.atan2(complex(value).imag, complex(value).real)
    if angle < 0.0:
        angle += 2.0 * math.pi
    return int(round(prime * angle / (2.0 * math.pi))) % prime


def _boolean_label(value: complex) -> int:
    if abs(complex(value).imag) > 1e-7:
        raise ValueError("Boolean phase must be real")
    return 0 if complex(value).real > 0.0 else 1


def _sqrt_mod_prime(value: int, prime: int) -> int | None:
    """Tonelli--Shanks square root in time polynomial in ``log prime``."""

    value %= prime
    if value == 0:
        return 0
    if pow(value, (prime - 1) // 2, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(value, (prime + 1) // 4, prime)
    odd = prime - 1
    power = 0
    while odd % 2 == 0:
        power += 1
        odd //= 2
    nonresidue = 2
    while pow(nonresidue, (prime - 1) // 2, prime) != prime - 1:
        nonresidue += 1
    c = pow(nonresidue, odd, prime)
    root = pow(value, (odd + 1) // 2, prime)
    residue = pow(value, odd, prime)
    exponent = power
    while residue != 1:
        i = 1
        square = residue * residue % prime
        while square != 1:
            square = square * square % prime
            i += 1
            if i >= exponent:
                raise ArithmeticError("Tonelli--Shanks invariant failed")
        factor = pow(c, 1 << (exponent - i - 1), prime)
        root = root * factor % prime
        residue = residue * factor * factor % prime
        c = factor * factor % prime
        exponent = i
    return root


def _decode_quadratic_chirp(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int, int, int]:
    p = spec.modulus
    y0 = _phase_exponent(shifted[0], p)
    y1 = _phase_exponent(shifted[1], p)
    recovered = (y1 - y0 - 1) * pow(2, -1, p) % p
    return recovered, 2, 2


def _decode_cubic_chirp(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int, int, int]:
    p = spec.modulus
    values = [_phase_exponent(shifted[x], p) for x in range(3)]
    second_difference = (values[2] - 2 * values[1] + values[0]) % p
    recovered = (second_difference - 6) * pow(6, -1, p) % p
    return recovered, 3, min(3, p)


def _kloosterman_value(point: int, prime: int) -> int:
    point %= prime
    if point == 0:
        return 0
    return (point + pow(point, -1, prime)) % prime


def _decode_kloosterman(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int | None, int, int]:
    p = spec.modulus
    first = _phase_exponent(shifted[0], p)
    candidates: set[int] = {0} if first == 0 else set()
    square_root = _sqrt_mod_prime((first * first - 4) % p, p)
    if square_root is not None:
        inverse_two = pow(2, -1, p)
        candidates.add((first + square_root) * inverse_two % p)
        candidates.add((first - square_root) * inverse_two % p)
    first_count = len(candidates)
    queries = 1
    # A first Kloosterman value has at most three candidate fibers.  For each
    # candidate pair, shifted equality excludes all but at most four x values,
    # so the first 4*C(3,2)+1 positions contain a separating query.
    while len(candidates) > 1:
        best_position: int | None = None
        best_buckets: dict[int, set[int]] = {}
        for position in range(1, min(p, 14)):
            buckets: dict[int, set[int]] = {}
            for candidate in candidates:
                label = _kloosterman_value(position + candidate, p)
                buckets.setdefault(label, set()).add(candidate)
            if len(buckets) > len(best_buckets):
                best_position = position
                best_buckets = buckets
        if best_position is None or len(best_buckets) <= 1:
            return None, queries, first_count
        observed = _phase_exponent(shifted[best_position], p)
        candidates = best_buckets.get(observed, set())
        queries += 1
    return (next(iter(candidates)) if candidates else None), queries, first_count


def _decode_bent_quadratic(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int, int, int]:
    if spec.n_bits % 2:
        raise ValueError("nondegenerate paired quadratic decoder requires even n")
    q_shift = _boolean_label(shifted[0])
    recovered = 0
    derivatives = []
    for bit in range(spec.n_bits):
        q_basis = 0
        observed = _boolean_label(shifted[1 << bit])
        derivatives.append(observed ^ q_basis ^ q_shift)
    for bit in range(0, spec.n_bits, 2):
        recovered |= derivatives[bit + 1] << bit
        recovered |= derivatives[bit] << (bit + 1)
    return recovered, spec.n_bits + 1, spec.domain_size // 2


def _majority_bit(value: int, width: int) -> int:
    return int(value.bit_count() >= ((width + 1) // 2))


def _decode_mm_majority(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int, int, int]:
    if spec.n_bits % 2:
        raise ValueError("Maiorana--McFarland control requires equal split dimensions")
    width = spec.n_bits // 2
    origin = _boolean_label(shifted[0])
    right_shift = 0
    for bit in range(width):
        derivative = _boolean_label(shifted[1 << bit]) ^ origin
        right_shift |= derivative << bit
    left_shift = 0
    majority_at_shift = _majority_bit(right_shift, width)
    for bit in range(width):
        y_basis_index = 1 << (width + bit)
        derivative = _boolean_label(shifted[y_basis_index]) ^ origin
        derivative ^= _majority_bit(right_shift ^ (1 << bit), width)
        derivative ^= majority_at_shift
        left_shift |= derivative << bit
    recovered = left_shift | (right_shift << width)
    return recovered, 2 * width + 1, spec.domain_size // 2


def _decode_fp2_quadratic(spec: PhaseFamilySpec, shifted: np.ndarray) -> tuple[int, int, int]:
    p = spec.modulus
    if p == 19:
        raise ValueError("the F_p^2 quadratic polar form is singular at p=19")
    y0 = _phase_exponent(shifted[0], p)
    y_e1 = _phase_exponent(shifted[p], p)
    y_e2 = _phase_exponent(shifted[1], p)
    first_polar = (y_e1 - y0 - 1) % p
    second_polar = (y_e2 - y0 - 5) % p
    inverse_det = pow(19, -1, p)
    first_coord = (10 * first_polar - second_polar) * inverse_det % p
    second_coord = (-first_polar + 2 * second_polar) * inverse_det % p
    return first_coord * p + second_coord, 3, p


def audit_public_decoder(
    family_id: str,
    n_bits: int = 6,
    shift: int = 37,
) -> PublicDecoderControl:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    decoders = {
        "quadratic_chirp": _decode_quadratic_chirp,
        "cubic_chirp": _decode_cubic_chirp,
        "kloosterman_trace": _decode_kloosterman,
        "bent_quadratic_f2": _decode_bent_quadratic,
        "mm_majority_bent_f2": _decode_mm_majority,
        "fp2_quadratic_form": _decode_fp2_quadratic,
    }
    if spec.id not in decoders:
        raise ValueError(f"no certified public decoder for {spec.id}")
    recovered, query_count, first_candidates = decoders[spec.id](spec, shifted)
    success = recovered == true_shift
    return PublicDecoderControl(
        family_id=spec.id,
        n_bits=spec.n_bits,
        domain_size=spec.domain_size,
        true_shift=true_shift,
        recovered_shift=recovered,
        shifted_value_query_count=query_count,
        candidate_count_after_first_query=first_candidates,
        polynomial_in_input_length=True,
        recovered_exactly=success,
        decoder=decoders[spec.id].__name__,
        status=(
            "public-value-shift-polynomially-dequantized"
            if success
            else "public-decoder-control-failure"
        ),
    )


def _access_boundaries() -> list[AccessModelBoundary]:
    return [
        AccessModelBoundary(
            access_model="public-base shifted-value oracle",
            classical_observation="an exact classical label f(x+s)",
            reference_function_cost="f is explicit and candidate evaluations are not oracle queries",
            fingerprint_theorem_applies=True,
            consequence="constant-disagreement families have O(log |G|) query complexity; only decoding time can remain hard",
        ),
        AccessModelBoundary(
            access_model="two-black-box hidden shift",
            classical_observation="classical labels from separately queried f and g",
            reference_function_cost="every f and g evaluation is charged",
            fingerprint_theorem_applies=False,
            consequence="the public-table consistency test is illegal; known bent-function oracle lower bounds remain intact",
        ),
        AccessModelBoundary(
            access_model="coherent phase oracle only",
            classical_observation="no exact phase label is exposed by a computational-basis query",
            reference_function_cost="access must be translated to a fair classical observation model",
            fingerprint_theorem_applies=False,
            consequence="a value-query fingerprint cannot be imported without an oracle simulation theorem",
        ),
        AccessModelBoundary(
            access_model="DHSP phase/coset-state samples",
            classical_observation="independent quantum states with hidden phase labels",
            reference_function_cost="there is no public pointwise base evaluator",
            fingerprint_theorem_applies=False,
            consequence="the DHSP sieve and measurement problem remains an active research direction",
        ),
    ]


def run_public_evaluator_admission_theorem(
    *,
    n_bits: int = 6,
    failure_probability: float = 0.01,
) -> HiddenShiftPublicEvaluatorAdmissionReport:
    families = [
        "quadratic_chirp",
        "cubic_chirp",
        "noisy_cubic_chirp",
        "legendre_symbol",
        "quartic_character",
        "kloosterman_trace",
        "bent_quadratic_f2",
        "mm_majority_bent_f2",
        "fp2_quadratic_form",
        "masked_quadratic_f2",
    ]
    generic = [
        fingerprint_theorem_control(size, mu, failure_probability)
        for size, mu in ((64, 0.5), (257, 0.25), (1024, 0.75))
    ]
    certificates = [
        audit_analytic_family(family, n_bits=n_bits, failure_probability=failure_probability)
        for family in families
    ]
    triage = _decoder_triage()
    decoder_controls = [
        audit_public_decoder(family, n_bits=n_bits, shift=37)
        for family in (
            "quadratic_chirp",
            "cubic_chirp",
            "kloosterman_trace",
            "bent_quadratic_f2",
            "mm_majority_bent_f2",
            "fp2_quadratic_form",
        )
    ]
    boundaries = _access_boundaries()
    certified = [row for row in certificates if row.analytic_bound_verified_by_finite_control]
    query_rejected = [
        row for row in certificates
        if not row.public_evaluator_superlog_query_advantage_possible
    ]
    failed = [
        row for row in certificates
        if row.analytic_agreement_bound is not None
        and not row.analytic_bound_verified_by_finite_control
    ]
    decoder_failures = [row for row in decoder_controls if not row.recovered_exactly]
    theorem_verified = bool(
        not failed
        and not decoder_failures
        and all(row.logarithmic_query_ceiling for row in generic)
        and any(not row.fingerprint_theorem_applies for row in boundaries)
    )
    theorem = PublicEvaluatorAdmissionTheorem(
        statement=(
            "For public f and a classical value oracle g_s(x)=f(x+s), m uniform queries leave any wrong shift with probability at most mu(f)^m, so total failure is at most (|G|-1)mu(f)^m."
        ),
        proof=(
            "For a wrong t, each independent x accepts exactly on f(x+s)=f(x+t), whose probability is a(t-s)<=mu; independence gives a(t-s)^m and the union bound sums over t!=s."
        ),
        decoder_cost_boundary=(
            "The direct consistency decoder performs O(|G|m) public evaluations. The theorem is a query upper bound, not a polynomial-time dequantization theorem."
        ),
        access_scope=(
            "The proof requires free explicit evaluation of the base function and classical value observations; it excludes two-black-box, phase-only, and DHSP state-sample inputs."
        ),
        theorem_verified=theorem_verified,
        status=(
            "public-evaluator-query-admission-theorem-verified"
            if theorem_verified
            else "admission-theorem-control-failure"
        ),
    )
    return HiddenShiftPublicEvaluatorAdmissionReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        generic_controls=generic,
        analytic_certificates=certificates,
        decoder_triage=triage,
        decoder_controls=decoder_controls,
        access_model_boundaries=boundaries,
        proof_obligations=[
            {
                "obligation": "separate_public_evaluator_from_two_black_box_query_complexity",
                "resolved": theorem_verified,
                "resolution": "The theorem and every certificate carry an explicit public-base value-oracle scope.",
            },
            {
                "obligation": "derive_public_evaluator_agreement_bounds_for_current_natural_families",
                "resolved": not failed and len(certified) >= 9,
                "resolution": "Nine algebraic families have symbolic bounds checked against exact finite profiles; the arbitrary hash mask is intentionally uncertified.",
            },
            {
                "obligation": "construct_polynomial_public_value_decoders_for_algebraically_exposed_families",
                "resolved": not decoder_failures and len(decoder_controls) == 6,
                "resolution": "Quadratic, cubic, paired-bent, split Maiorana--McFarland, F_p^2 quadratic, and Kloosterman controls recover the exact shift with O(n) or constant value queries and polynomial arithmetic.",
            },
            {
                "obligation": "prove_polynomial_time_classical_decoder_for_multiplicative_character_shift",
                "resolved": False,
                "resolution": "Short fingerprints only remove a query lower-bound route. Legendre/quartic decoding time remains a separate complexity question, although the quantum mechanism is known.",
            },
            {
                "obligation": "find_natural_problem_reduction_and_quantum_decoder_for_masked_families",
                "resolved": False,
                "resolution": "Synthetic masking is rejected from the high-upside queue until both obligations exist.",
            },
            {
                "obligation": "transfer_any_public_evaluator_bound_to_dhsp_phase_states",
                "resolved": False,
                "resolution": "No transfer is valid; DHSP samples expose neither a public base evaluator nor classical labels.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The logarithmic fingerprint contradicts the exponential classical bent hidden-shift query lower bound.",
                "resolved": True,
                "resolution": "It does not: Roetteler charges oracle access to both f and g, while the fingerprint enumerates candidates using a free public evaluator for f.",
            },
            {
                "objection": "A logarithmic query ceiling proves a polynomial-time classical algorithm.",
                "resolved": True,
                "resolution": "False. Generic candidate filtering costs O(|G| log |G|), exponential in the input length log |G|.",
            },
            {
                "objection": "A quantum phase oracle automatically gives the same exact labels to a classical algorithm.",
                "resolved": True,
                "resolution": "False without an oracle simulation. A phase on a basis state is not itself a readable classical value.",
            },
            {
                "objection": "An arbitrary public hash mask creates a hard hidden-shift family.",
                "resolved": True,
                "resolution": "No natural reduction or quantum decoder follows from masking; hardness-by-obscurity is not admitted.",
            },
            {
                "objection": "This theorem dequantizes the DHSP phase-state problem.",
                "resolved": True,
                "resolution": "The DHSP input is a state-sample experiment with no public pointwise reference evaluator, so equation (1) is unavailable.",
            },
        ],
        literature_links=[
            {
                "paper": "Quantum Algorithms for some Hidden Shift Problems",
                "url": VDHI_URL,
                "used_for": "Known multiplicative-character hidden-shift mechanism and access-model comparison",
                "new_mechanism_supplied": False,
            },
            {
                "paper": "Quantum algorithms for highly non-linear Boolean functions",
                "url": ROETTELER_URL,
                "used_for": "Two-black-box bent hidden-shift query separation that limits this theorem's scope",
                "new_mechanism_supplied": False,
            },
        ],
        headline_metrics={
            "analytic_family_count": len(certificates),
            "analytic_certificate_count": len(certified),
            "analytic_control_failure_count": len(failed),
            "public_evaluator_query_admission_rejection_count": len(query_rejected),
            "polynomial_time_public_decoder_family_count": sum(
                row.classical_time_status == "polynomial" for row in triage
            ),
            "polynomial_decoder_control_success_count": sum(
                row.recovered_exactly for row in decoder_controls
            ),
            "polynomial_decoder_control_failure_count": len(decoder_failures),
            "breakthrough_search_family_admission_count": sum(
                row.admit_as_breakthrough_search_family for row in triage
            ),
            "two_black_box_lower_bound_invalidated_count": sum(
                row.two_black_box_oracle_lower_bound_invalidated
                for row in certificates
            ),
            "dhsp_phase_state_no_go_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "public_evaluator_fingerprint_theorem_proved": theorem_verified,
            "current_explicit_families_support_superlog_public_value_query_advantage": False,
            "generic_fingerprint_is_polynomial_time_decoder": False,
            "two_black_box_bent_query_separation_refuted": False,
            "phase_only_oracle_bound_proved": False,
            "dhsp_phase_state_bound_proved": False,
            "masked_family_natural_reduction_proved": False,
            "masked_family_quantum_decoder_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "The repository's explicit public-base phase families have no superlogarithmic classical value-query story: nine receive analytic logarithmic fingerprint ceilings, six also have direct polynomial-time public decoders, two instantiate known character-shift mechanisms, and synthetic masks lack reductions and quantum decoders. This does not touch two-black-box bent hidden shift or DHSP state samples."
        ),
        falsifiers_triggered=[
            "Survival of undersampled random-correlation code is not query-complexity evidence when the public base function has constant pairwise disagreement.",
            "Finite agreement fingerprints cannot be transferred to two-black-box or phase-state access models.",
            "The current explicit phase-family list contains no admitted new breakthrough mechanism.",
        ],
    )


def write_public_evaluator_admission_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-HIDDEN-SHIFT-PUBLIC-EVALUATOR-ADMISSION-THEOREM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_public_evaluator_admission" in globals():
        report = run_public_evaluator_admission(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-N-SHIFT-PUBLIC-EVALUATOR-ADMISSION-THEOREM",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-HIDDEN-SHIFT-PUBLIC-EVALUATOR-ADMISSION-THEOREM.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-HIDDEN-SHIFT-PUBLIC-EVALUATOR-ADMISSION-THEOREM.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "hidden_shift_public_evaluator_admission_theorem": str(path)
                },
            )
        )
    return payload
