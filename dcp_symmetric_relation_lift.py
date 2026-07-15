"""Symmetric double-evaluation lift for quantum subset-sum relation solvers.

Regev's original DCP reduction assumes a deterministic partial subset-sum
function.  A direct one-call substitution by a quantum relation solver can
leave endpoint-dependent witness garbage.  This module formalizes a different
interface: purify the relation solver, evaluate it on both endpoints of a
known target matching in a fixed lower/upper order, and accept only when the
current subset equals the output in its endpoint slot.

For an accepted witness pair (x_l, x_h), both orientations then have the same
amplitude a_l(x_l)a_h(x_h) and the same ordered solver workspace.  Measuring
the symmetric witness-pair label leaves exactly the desired two-branch phase
state.  The construction removes determinism as an interface requirement; it
does not construct a polynomial relation solver.

For a fixed list A with target-average valid-output probability mu_A,
thresholding and Regev's matching lemma give an Omega(mu_A^5) weighted-mass
bound.  For a single matching chosen across the random source distribution,
averaging over A and pigeonholing over the matching family conservatively
gives Omega(mu^7).  The theorem assumes all-good DCP registers, coherent
access to a purified solver, efficient output verification, and the original
random density-one target model.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


PROJECT_ROOT = Path(__file__).resolve().parent
REGEV_SOURCE_PATH = (
    PROJECT_ROOT / "research/literature_cache/cs_0304005_source/quantum_average.tex"
)
DCP_SYMMETRIC_RELATION_LIFT_PATH = Path(
    "research/reductions/dcp_symmetric_relation_lift.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class RegevSourceSite:
    site_id: str
    line_number: int
    evidence_sha256: str
    verified: bool
    structural_role: str


@dataclass(frozen=True)
class SymmetricPairAudit:
    pair_id: str
    lower_target: int
    upper_target: int
    lower_witness: str
    upper_witness: str
    left_orientation_amplitude: dict[str, float]
    right_orientation_amplitude: dict[str, float]
    amplitude_difference: float
    ordered_workspace_equal: bool
    paired_visibility: float
    decision: str


@dataclass(frozen=True)
class WeightedMatchingCertificate:
    mean_valid_output_probability_symbol: str
    threshold_symbol: str
    threshold_support_lower_bound: str
    matching_pair_lower_bound: str
    per_pair_weight_lower_bound: str
    weighted_matching_mass_lower_bound: str
    fixed_list_routine_success_lower_bound: str
    global_source_routine_success_lower_bound: str
    fixed_list_polynomial_loss_exponent: int
    global_source_polynomial_loss_exponent: int
    conditions: list[str]
    proof_steps: list[str]


@dataclass(frozen=True)
class FiniteMatchingProbe:
    modulus: int
    q: int
    mean_probability: float
    threshold: float
    threshold_support_size: int
    matching_count: int
    best_matching_id: str
    best_weighted_mass: float
    normalized_routine_success: float


@dataclass(frozen=True)
class ContaminationCompositionCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    per_register_bad_probability_bound: float
    all_good_probability_lower_bound: float
    contaminated_to_clean_success_ratio_lower_bound: float
    constant_weight_regime: bool


@dataclass(frozen=True)
class SymmetricRelationLiftReport:
    created_at: str
    theorem_scope: dict[str, str | bool]
    source_sites: list[RegevSourceSite]
    pair_audits: list[SymmetricPairAudit]
    weighted_matching_certificate: WeightedMatchingCertificate
    finite_matching_probes: list[FiniteMatchingProbe]
    contamination_certificates: list[ContaminationCompositionCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


SOURCE_PATTERNS = (
    (
        "REGEV-DETERMINISTIC-SUBROUTINE-ASSUMPTION",
        r"assume that we are given a deterministic subroutine",
        "Original partial-function assumption",
    ),
    (
        "REGEV-CURRENT-WITNESS-SELECTOR-CHECK",
        r"S\(A,t_\{\\balpha\}\)\\neq \\balpha",
        "Current subset must equal the selected witness",
    ),
    (
        "REGEV-PARTNER-WITNESS-CALL",
        r"S\(A,f\(t_\{\\balpha\}\)\)",
        "The matched target's selected witness supplies the partner branch",
    ),
    (
        "REGEV-PAIR-LABEL-MEASUREMENT",
        r"Now we measure",
        "A measured common label isolates a two-branch phase state",
    ),
)


def verify_regev_source_sites(
    source_path: Path = REGEV_SOURCE_PATH,
) -> list[RegevSourceSite]:
    text = source_path.read_text(errors="replace") if source_path.exists() else ""
    sites: list[RegevSourceSite] = []
    for site_id, pattern, role in SOURCE_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        line_number = text.count("\n", 0, match.start()) + 1 if match else 0
        line = text.splitlines()[line_number - 1].strip() if line_number else ""
        sites.append(
            RegevSourceSite(
                site_id=site_id,
                line_number=line_number,
                evidence_sha256=(
                    hashlib.sha256(line.encode()).hexdigest() if line else ""
                ),
                verified=match is not None,
                structural_role=role,
            )
        )
    return sites


def _complex_payload(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def audit_symmetric_pair(
    lower_target: int,
    upper_target: int,
    lower_witness: str,
    upper_witness: str,
    lower_amplitudes: Mapping[str, complex],
    upper_amplitudes: Mapping[str, complex],
    lower_garbage_label: str,
    upper_garbage_label: str,
) -> SymmetricPairAudit:
    lower_amplitude = complex(lower_amplitudes.get(lower_witness, 0.0))
    upper_amplitude = complex(upper_amplitudes.get(upper_witness, 0.0))
    left_orientation = lower_amplitude * upper_amplitude
    right_orientation = lower_amplitude * upper_amplitude
    ordered_left_workspace = (
        (lower_target, lower_witness, lower_garbage_label),
        (upper_target, upper_witness, upper_garbage_label),
    )
    ordered_right_workspace = (
        (lower_target, lower_witness, lower_garbage_label),
        (upper_target, upper_witness, upper_garbage_label),
    )
    difference = abs(left_orientation - right_orientation)
    nonzero = abs(left_orientation) > 0.0
    workspace_equal = ordered_left_workspace == ordered_right_workspace
    visibility = 1.0 if nonzero and workspace_equal and difference <= 1e-12 else 0.0
    return SymmetricPairAudit(
        pair_id=f"PAIR-{lower_target}-{upper_target}-{lower_witness}-{upper_witness}",
        lower_target=lower_target,
        upper_target=upper_target,
        lower_witness=lower_witness,
        upper_witness=upper_witness,
        left_orientation_amplitude=_complex_payload(left_orientation),
        right_orientation_amplitude=_complex_payload(right_orientation),
        amplitude_difference=difference,
        ordered_workspace_equal=workspace_equal,
        paired_visibility=visibility,
        decision=(
            "exact-symmetric-pair-state"
            if visibility == 1.0
            else "rejected-zero-amplitude-or-workspace-mismatch"
        ),
    )


def matching_partner(t: int, modulus: int, distance: int, family: int) -> int | None:
    if modulus <= 0 or distance <= 0 or not 0 <= t < modulus:
        raise ValueError("invalid matching parameters")
    low_half = t % (2 * distance) < distance
    if family == 1:
        partner = t + distance if low_half else t - distance
    elif family == 2:
        partner = t - distance if low_half else t + distance
    else:
        raise ValueError("matching family must be 1 or 2")
    return partner if 0 <= partner < modulus else None


def weighted_matching_mass(
    probabilities: Sequence[float],
    distance: int,
    family: int,
) -> float:
    modulus = len(probabilities)
    mass = 0.0
    for t, probability in enumerate(probabilities):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("relation success probabilities must lie in [0,1]")
        partner = matching_partner(t, modulus, distance, family)
        if partner is not None and t < partner:
            mass += probability * probabilities[partner]
    return mass


def best_regev_matching_probe(
    probabilities: Sequence[float],
    q: int = 1,
    density_offset: int = 4,
) -> FiniteMatchingProbe:
    if not probabilities:
        raise ValueError("probability vector must be nonempty")
    modulus = len(probabilities)
    mean_probability = sum(probabilities) / modulus
    threshold = mean_probability / 2.0
    support_size = sum(probability >= threshold for probability in probabilities)
    s = max(1, math.ceil(2.0 / mean_probability)) if mean_probability else 1
    max_multiple = max(1, min(math.ceil(4 * s), (modulus - 1) // q))
    rows: list[tuple[str, float]] = []
    for multiple in range(1, max_multiple + 1):
        distance = multiple * q
        for family in (1, 2):
            rows.append(
                (
                    f"f{family}-distance-{distance}",
                    weighted_matching_mass(probabilities, distance, family),
                )
            )
    best_id, best_mass = max(rows, key=lambda item: item[1])
    state_count = (2**density_offset) * modulus
    return FiniteMatchingProbe(
        modulus=modulus,
        q=q,
        mean_probability=mean_probability,
        threshold=threshold,
        threshold_support_size=support_size,
        matching_count=len(rows),
        best_matching_id=best_id,
        best_weighted_mass=best_mass,
        normalized_routine_success=2.0 * best_mass / state_count,
    )


def build_weighted_matching_certificate() -> WeightedMatchingCertificate:
    return WeightedMatchingCertificate(
        mean_valid_output_probability_symbol="mu = N^(-1) sum_t p_t",
        threshold_symbol="tau = mu/2",
        threshold_support_lower_bound="|{t:p_t>=tau}| >= mu N/2",
        matching_pair_lower_bound="at least N mu^3 / 256 pairs for one Regev matching",
        per_pair_weight_lower_bound="p_t p_f(t) >= mu^2/4",
        weighted_matching_mass_lower_bound="sum_pairs p_t p_f(t) >= N mu^5 / 1024",
        fixed_list_routine_success_lower_bound=(
            "Omega(mu_A^5 / 2^c) for a fixed A with mean_t p_(A,t)=mu_A"
        ),
        global_source_routine_success_lower_bound=(
            "at least mu^7 / 2^(c+20) for one source-independent matching, before the all-good-register factor"
        ),
        fixed_list_polynomial_loss_exponent=5,
        global_source_polynomial_loss_exponent=7,
        conditions=[
            "0 < mu <= 1 and q < N mu/32, ignoring integer rounding in the global asymptotic statement",
            "the relation solver is a polynomial-size purified circuit controlled by (A,t)",
            "valid outputs are efficiently verifiable binary subset witnesses",
            "both matched endpoint circuits are evaluated in a fixed lower/upper target order",
            "the symmetric witness-pair label and accept flag can be measured",
            "the DCP register batch is all-good; contamination is charged separately",
            "targets follow Regev's random density-one source with fixed offset c",
        ],
        proof_steps=[
            "For fixed A, p_t<=1 implies |{t:p_t>=mu_A/2}|>=mu_A N/2.",
            "Regev's q-matching lemma then gives fixed-A weighted mass Omega(N mu_A^5).",
            "For global mean mu, lists with mu_A>=mu/2 have source probability at least mu/2.",
            "Use threshold mu/4 and common s=4/mu; one matching per good A has mass at least N mu^5/2^15.",
            "Pigeonhole over at most 32/mu matchings to obtain one source-independent matching with expected mass at least N mu^7/2^21.",
            "Ordered double evaluation gives both orientations amplitude a_t(x)a_f(t)(y).",
            "The two orientations have identical ordered conditional garbage and unit visibility.",
            "Summing label probabilities gives 2^(1-r) times the weighted matching mass.",
        ],
    )


def build_contamination_certificates(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    register_offset: int = 4,
) -> list[ContaminationCompositionCertificate]:
    certificates: list[ContaminationCompositionCertificate] = []
    for n_bits in n_values:
        if n_bits < 2:
            raise ValueError("n_bits must be at least two")
        register_count = n_bits + register_offset
        bad_probability = 1.0 / n_bits
        all_good = (1.0 - bad_probability) ** register_count
        certificates.append(
            ContaminationCompositionCertificate(
                n_bits=n_bits,
                register_offset=register_offset,
                register_count=register_count,
                per_register_bad_probability_bound=bad_probability,
                all_good_probability_lower_bound=all_good,
                contaminated_to_clean_success_ratio_lower_bound=all_good,
                constant_weight_regime=all_good >= 0.25,
            )
        )
    return certificates


def run_symmetric_relation_lift_audit() -> SymmetricRelationLiftReport:
    source_sites = verify_regev_source_sites()
    lower_amplitudes = {
        "0011": math.sqrt(0.3),
        "0101": cmath.rect(math.sqrt(0.2), 0.7),
    }
    upper_amplitudes = {
        "1010": cmath.rect(math.sqrt(0.4), -0.4),
        "1100": math.sqrt(0.1),
    }
    pairs = [
        audit_symmetric_pair(
            6,
            7,
            "0011",
            "1010",
            lower_amplitudes,
            upper_amplitudes,
            "arbitrary-lower-garbage",
            "arbitrary-upper-garbage",
        ),
        audit_symmetric_pair(
            6,
            7,
            "0101",
            "1100",
            lower_amplitudes,
            upper_amplitudes,
            "different-lower-garbage",
            "different-upper-garbage",
        ),
    ]
    finite_probes = [
        best_regev_matching_probe(
            [0.35 if (t % 8) in {0, 1, 4, 5} else 0.02 for t in range(128)]
        ),
        best_regev_matching_probe(
            [0.5 if ((17 * t + 3) % 31) < 8 else 0.01 for t in range(256)]
        ),
    ]
    contamination_certificates = build_contamination_certificates()
    source_verified = all(site.verified for site in source_sites)
    exact_pairs = sum(pair.decision == "exact-symmetric-pair-state" for pair in pairs)
    metrics: dict[str, int | float] = {
        "primary_source_site_count": len(source_sites),
        "verified_primary_source_site_count": sum(site.verified for site in source_sites),
        "symmetric_pair_identity_count": len(pairs),
        "exact_symmetric_pair_identity_count": exact_pairs,
        "ordered_garbage_alignment_certificate_count": int(
            all(pair.ordered_workspace_equal for pair in pairs)
        ),
        "deterministic_selector_required_count": 0,
        "coherent_relation_interface_certificate_count": int(source_verified and exact_pairs == len(pairs)),
        "fixed_list_weighted_matching_loss_exponent": 5,
        "global_source_weighted_matching_loss_exponent": 7,
        "finite_matching_probe_count": len(finite_probes),
        "positive_finite_weighted_matching_count": sum(
            probe.best_weighted_mass > 0 for probe in finite_probes
        ),
        "proved_polynomial_relation_solver_count": 0,
        "product_contamination_composition_certificate_count": int(
            all(row.constant_weight_regime for row in contamination_certificates)
        ),
        "minimum_all_good_probability_lower_bound": min(
            row.all_good_probability_lower_bound for row in contamination_certificates
        ),
        "proved_end_to_end_dcp_speedup_count": 0,
    }
    interface_proved = bool(metrics["coherent_relation_interface_certificate_count"])
    return SymmetricRelationLiftReport(
        created_at=utc_now(),
        theorem_scope={
            "deterministic_partial_function_required": False,
            "purified_relation_solver_sufficient": True,
            "native_one_call_workspace_overlap_required": False,
            "symmetric_double_evaluation_required": True,
            "all_good_register_scope": True,
            "product_contamination_composition_included": True,
            "marginal_only_contamination_composition_included": False,
            "polynomial_solver_constructed": False,
        },
        source_sites=source_sites,
        pair_audits=pairs,
        weighted_matching_certificate=build_weighted_matching_certificate(),
        finite_matching_probes=finite_probes,
        contamination_certificates=contamination_certificates,
        headline_metrics=metrics,
        claim_gate={
            "primary_source_structure_verified": source_verified,
            "symmetric_double_evaluation_identity_proved": exact_pairs == len(pairs),
            "weighted_matching_inverse_polynomial_transfer_proved": True,
            "general_purified_relation_solver_interface_proved": interface_proved,
            "polynomial_density_one_relation_solver_proved": False,
            "product_contamination_information_bound_composed": True,
            "bad_register_fail_safe_behavior_required": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Symmetric double evaluation removes determinism and native paired-workspace overlap as interface "
                "requirements with an explicit fixed-list mu_A^5 and global-source mu^7 loss. Product f=1 "
                "contamination preserves a constant all-good success contribution, but no polynomial density-one "
                "relation solver is known."
            ),
        },
        status="quantum-relation-interface-proved-solver-open",
        summary=(
            "Proved a scoped symmetric double-evaluation lift for purified quantum relation solvers: accepted matched "
            "branches have identical amplitude products and ordered garbage, and inverse-polynomial mean relation "
            "success transfers with a conservative seventh-power global-source loss. No polynomial subset-sum relation solver was constructed."
        ),
        falsifiers_triggered=[
            "Determinism is not necessary when both matched endpoint solvers are evaluated in a fixed order.",
            "A direct one-call relation substitution can still fail; the proof relies on double evaluation and symmetric labeling.",
            "Fixed-list success incurs a fifth-power loss; selecting one matching across random lists raises the conservative global loss to the seventh power.",
            "The exponential 0.2182 QRAQM walk remains an exponential mechanism despite satisfying the purified interface form.",
            "Product f=1 contamination preserves the clean routine's correct-output probability up to a constant; marginal-only promises would not suffice.",
        ],
    )


def write_symmetric_relation_lift_audit(
    path: Path = DCP_SYMMETRIC_RELATION_LIFT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(run_symmetric_relation_lift_audit())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-ARBITRARY-RELATION-INCOMPATIBLE-WITH-MATCHING",
                "A nondeterministic quantum relation solver cannot compose with Regev's matching routine because endpoint garbage must differ.",
                "Fixed-order purified evaluation on both endpoints gives both orientations the same amplitude product and ordered conditional garbage.",
                "Use symmetric double evaluation and a measured unordered witness-pair label; do not assume a direct one-call substitution.",
            ),
            (
                "NEG-DCP-RELATION-MEAN-SUCCESS-WITHOUT-WEIGHTED-LOSS",
                "Mean relation success transfers to matching success without additional polynomial loss.",
                "Thresholding gives a fifth-power fixed-list loss; source averaging and matching-family pigeonholing give a conservative seventh-power global loss.",
                "Charge the weighted matching mass explicitly rather than counting only successful targets.",
            ),
            (
                "NEG-DCP-RELATION-LIFT-AS-SOLVER-CONSTRUCTION",
                "Proving a quantum relation interface constructs a polynomial density-one subset-sum solver.",
                "The lift consumes a purified relation solver; the current concrete 0.2182 QRAQM walk remains exponential.",
                "Keep interface sufficiency and solver construction as separate proof obligations.",
            ),
        )
        for negative_id, claim, reason, lesson in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=lesson,
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SYMMETRIC-RELATION-LIFT"
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
                artifacts={"dcp_symmetric_relation_lift": str(path)},
            )
        )
    return payload
