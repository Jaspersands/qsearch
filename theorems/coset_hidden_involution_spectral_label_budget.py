"""Exact spectral-packing budget under the hidden-involution source law.

This is a restriction on complete spectral labels, NOT a quantum circuit or
HSP lower bound. The derivation is in research/SPECTRAL_LABEL_BUDGET.md.
Integer/rational bounds are authoritative; floating-point logs are display
values. No finite numerical scan is promoted to a formal proof.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_hyperoctahedral_branching_mass import (
    even_hyperoctahedral_irrep_dimension_sum,
)
from coset_hidden_involution_natural_matrix_multiplicity import (
    symmetric_group_involution_count,
)
from research_registry import utc_now

REPORT_PATH = Path("research/representation/coset_hidden_involution_spectral_label_budget.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-SPECTRAL-LABEL-BUDGET"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


def spectral_label_capacity(gap: Fraction, *, observables: int = 1) -> int:
    """Packing upper bound for joint l-infinity separated labels in [-1,1]^r.

For a simultaneous eigenbasis the observables must commute. Adaptive
protocols instead need an explicit finite transcript alphabet; see below.
"""
    if not isinstance(gap, Fraction) or gap <= 0:
        raise ValueError("gap must be a positive exact Fraction")
    if type(observables) is not int or observables < 1:
        raise ValueError("observables must be a positive integer")
    return (2 // gap + 1) ** observables


def source_label_mass_bound(half_degree: int, label_capacity: int) -> Fraction:
    """Upper bound q{b<=L}, also average uniform-copy-label decoding success.

The decoding bound assumes at most L classical transcripts per known
branch, no label-correlated side information, and no residual quantum input
to the decoder. It says nothing about recovering the hidden involution.
"""
    if type(half_degree) is not int or half_degree < 2:
        raise ValueError("half_degree must be an integer >=2")
    if type(label_capacity) is not int or label_capacity < 0:
        raise ValueError("label_capacity must be a nonnegative integer")
    numerator = (2 * label_capacity * symmetric_group_involution_count(2 * half_degree)
                 * even_hyperoctahedral_irrep_dimension_sum(half_degree))
    return min(Fraction(1), Fraction(numerator, math.factorial(2 * half_degree)))


def necessary_label_rounds(half_degree: int, alphabet_size: int,
                           target_mass: Fraction = Fraction(1, 2)) -> int:
    """A necessary, not sufficient, depth for a finite-alphabet label protocol."""
    if type(alphabet_size) is not int or alphabet_size < 2:
        raise ValueError("alphabet_size must be an integer >=2")
    if not isinstance(target_mass, Fraction) or not 0 < target_mass <= 1:
        raise ValueError("target_mass must be an exact Fraction in (0,1]")
    rounds, capacity = 0, 1
    while source_label_mass_bound(half_degree, capacity) < target_mass:
        rounds += 1
        capacity *= alphabet_size
    return rounds


def tensor_source_label_mass_bound(degree: int, label_capacity: int, *, copies: int = 2,
                                  source: str = "involution-coset") -> Fraction:
    """Low tensor-multiplicity branch mass, not a conditional label-success bound.

Independent Plancherel registers give q=(prod d_lambda)*d_nu*g/|G|^k.
Order-two coset states, independent conditional on the same hidden h, are
operator-dominated by 2^k times the maximally mixed source. This remains true
after averaging h, but not after arbitrary postselection or conditioning on
one chosen lambda tuple.
"""
    if type(degree) is not int or degree < 2 or type(copies) is not int or copies < 2:
        raise ValueError("degree and copies must be integers >=2")
    if type(label_capacity) is not int or label_capacity < 0:
        raise ValueError("label_capacity must be a nonnegative integer")
    if source not in {"plancherel", "involution-coset"}:
        raise ValueError("unsupported source law; rederive its density domination")
    factor = 2**copies if source == "involution-coset" else 1
    return min(Fraction(1), Fraction(
        factor * label_capacity * symmetric_group_involution_count(degree)**(copies + 1),
        math.factorial(degree)**copies,
    ))


def _exact_bound_payload(bound: Fraction) -> dict[str, str | float]:
    return {
        "numerator": str(bound.numerator),
        "denominator": str(bound.denominator),
        "log2_display": math.log2(bound.numerator) - math.log2(bound.denominator),
    }


def build_spectral_label_budget(*, half_degrees: tuple[int, ...] = (7, 16, 32, 64, 128, 256),
                               gap_powers: tuple[int, ...] = (1, 2, 4),
                               observable_counts: tuple[int, ...] = (1, 2, 4)) -> dict[str, Any]:
    if not half_degrees or not gap_powers or not observable_counts:
        raise ValueError("scaling grids must be nonempty")
    if any(type(power) is not int or power < 0 for power in gap_powers):
        raise ValueError("gap powers must be nonnegative integers")
    rows = []
    for m in half_degrees:
        source_label_mass_bound(m, 1)  # Validate before exponentiation.
        for power in gap_powers:
            gap = Fraction(1, m**power)
            alphabet = spectral_label_capacity(gap)
            for count in observable_counts:
                capacity = spectral_label_capacity(gap, observables=count)
                bound = source_label_mass_bound(m, capacity)
                rows.append({
                    "half_degree": m,
                    "inverse_polynomial_gap_power": power,
                    "observable_count": count,
                    "label_capacity": str(capacity),
                    "resolvable_branch_mass_upper_bound": _exact_bound_payload(bound),
                    "necessary_rounds_for_half_mass": necessary_label_rounds(m, alphabet),
                    "upper_bound_below_one_percent": bound < Fraction(1, 100),
                })
    tensor_rows = []
    for m in half_degrees:
        n = 2 * m
        for power in gap_powers:
            for count in observable_counts:
                capacity = spectral_label_capacity(Fraction(1, n**power), observables=count)
                bound = tensor_source_label_mass_bound(n, capacity)
                tensor_rows.append({
                    "degree": n, "copies": 2, "source": "involution-coset",
                    "inverse_polynomial_gap_power": power, "observable_count": count,
                    "resolvable_branch_mass_upper_bound": _exact_bound_payload(bound),
                    "conditional_eigenlabel_distribution_assumed_uniform": False,
                })
    return {
        "created_at": utc_now(),
        "status": "single-and-fixed-count-gapped-label-route-obstructed",
        "summary": ("Spectral packing and the exact branching source law exclude a fixed number of "
                    "bounded-norm inverse-polynomial-gap observables as complete typical copy labels. "
                    "Adaptive label hierarchies and direct transforms remain open."),
        "derivation": {
            "source_law": "q(lambda,mu)=2*d_lambda*d_mu*b(lambda,mu)/(2m)! for h-even mu",
            "packing": "b <= (floor(2/delta)+1)^r for delta-separated complete joint labels",
            "mass_bound": "q{b<=L} <= min(1,2*L*I_(2m)*J_m^+/(2m)!)",
            "decoding_bound": "E_q min(1,L/b) <= min(1,2*L*I_(2m)*J_m^+/(2m)!)",
            "tensor_mass_bound": "q_coset{g<=L} <= min(1,2^k*L*I_n^(k+1)/(n!)^k)",
            "asymptotics": "For fixed r,c and delta=m^-c the bound is exp(-0.5*m*log(m)+O(m))",
            "proof_document": "research/SPECTRAL_LABEL_BUDGET.md",
            "evidence_kind": "human-readable-derivation-with-exact-arithmetic-regression-checks",
            "machine_checked_formal_proof": False,
        },
        "scaling_records": rows,
        "tensor_scaling_records": tensor_rows,
        "assumptions": [
            "The exact one-coordinate h-even branching source law, not an arbitrary input distribution.",
            "Every multiplicity eigenlabel must be resolved, not just a task-relevant coarse observable.",
            "Each observable has norm at most one AFTER its declared physical/LCU normalization.",
            "Joint spectra use commuting observables; r and the inverse-gap power are fixed as m grows.",
            "The decoding variant has a uniform copy label and only L possible classical transcripts per branch.",
        ],
        "escape_routes": [
            "Polynomial-depth adaptive coarse labels with a reversible source-aware implementation.",
            "A direct subduction transform which never estimates one globally simple spectrum.",
            "A task-specific measurement that does not require identifying every multiplicity basis vector.",
            "Fast-forwarded powers, noncommuting procedures, or retained quantum information outside the transcript model.",
        ],
        "proof_obligations": [
            {"obligation": "independently_review_source_law_and_packing_derivation", "resolved": False},
            {"obligation": "compile_coarse_labels_without_dense_block_diagonalization", "resolved": False},
            {"obligation": "retain_hidden_involution_information_through_measurement", "resolved": False},
            {"obligation": "compare_total_cost_to_classical_baselines", "resolved": False},
        ],
        "headline_metrics": {
            "exact_rational_scaling_record_count": len(rows),
            "tensor_source_scaling_record_count": len(tensor_rows),
            "scaling_records_below_one_percent": sum(row["upper_bound_below_one_percent"] for row in rows),
            "maximum_half_degree": max(half_degrees),
            "formal_proof_count": 0,
            "coherent_transform_count": 0,
        },
        "claim_gate": {
            "fixed_count_inverse_polynomial_complete_label_route_obstructed": True,
            "unpostselected_tensor_source_complete_label_route_obstructed": True,
            "all_quantum_measurements_ruled_out": False,
            "adaptive_hierarchy_compiled": False,
            "generic_circuit_lower_bound_proved": False,
            "speedup_claim_allowed": False,
        },
        "falsifiers_triggered": [
            "A typical-block complete simple spectrum cannot retain an inverse-polynomial normalized minimum gap.",
            "Per-branch optimized finite separators do not solve the spectral label capacity deficit.",
        ],
    }


def write_spectral_label_budget_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
                                      registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                                      registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                                      registry_result_id: str = "", **kwargs: Any) -> dict[str, Any]:
    payload = build_spectral_label_budget(**kwargs)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                       upsert_experiment, upsert_experiment_result, upsert_negative_result)

        upsert_experiment(ExperimentRecord(
            id=registry_experiment_id, candidate_id=registry_candidate_id,
            title="Spectral label capacity under the natural branching source law",
            status=payload["status"], hypothesis="A fixed number of normalized gapped observables can label typical multiplicity blocks.",
            protocol="Combine exact branching dimension sums with spectral packing; audit scope against adaptive and direct transforms.",
            positive_signal="An escape using task-relevant coarse labels or a polynomial-depth coherent hierarchy.",
            falsifiers=["label capacity has vanishing exact source mass", "the argument silently assumes complete eigenlabel recovery"],
            metrics=list(payload["headline_metrics"]),
            dependencies=["coset_hidden_involution_hyperoctahedral_branching_mass.py"],
            next_actions=["independently review the written derivation", "construct a task-relevant adaptive labeling contract"]
        ))
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}", experiment_id=registry_experiment_id,
            candidate_id=registry_candidate_id, created_at=payload["created_at"], status=payload["status"],
            summary=payload["summary"], metrics=payload["headline_metrics"],
            falsifiers_triggered=payload["falsifiers_triggered"], artifacts={"spectral_label_budget": str(path)}
        ))
        upsert_negative_result(NegativeResultRecord(
            id="TYPICAL-MULTIPLICITY-SINGLE-GAPPED-SEPARATOR-PACKING-OBSTRUCTION",
            source=registry_experiment_id,
            claim="One bounded-norm inverse-polynomial-gap simple-spectrum separator resolves typical multiplicity labels.",
            reason_invalid="The packed label capacity is polynomial, while the exact source mass of such small multiplicities vanishes superpolynomially.",
            lesson="Pursue adaptive coarse labels, a direct transform, or a task-specific observable; this is not an HSP lower bound.",
            applies_to=[registry_candidate_id, "complete spectral copy-label decoding"],
            evidence={"artifact": str(path), "derivation": "research/SPECTRAL_LABEL_BUDGET.md"}
        ))
        upsert_negative_result(NegativeResultRecord(
            id="TYPICAL-KRONECKER-COMPLETE-SEPARATOR-PACKING-OBSTRUCTION",
            source=registry_experiment_id,
            claim="A fixed number of polynomial-gap normalized spectra labels every typical Kronecker multiplicity direction.",
            reason_invalid="Under the unpostselected k-register order-two coset source, low-multiplicity branch mass is at most 2^k*L*I_n^(k+1)/(n!)^k, which vanishes for polynomial L and fixed k>=2.",
            lesson="Finite selected-partition spectra are not typical-source evidence. Growing-depth and task-specific measurements remain open; conditional copy states need not be uniform.",
            applies_to=[registry_candidate_id, "complete tensor-multiplicity spectral labels"],
            evidence={"artifact": str(path), "derivation": "research/SPECTRAL_LABEL_BUDGET.md"}
        ))
    return payload
