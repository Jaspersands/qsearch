"""Coherent overlapping nonmissing-sector echoes with an actual X readout.

The growing-copy program is a proposal, not a speedup. Two independent finite
evaluators check its physical output: source-block matrices and an exact
three-copy group-word contraction. See research/COHERENT_OVERLAP_ECHO.md.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np

from coherent_overlap_programs import OverlapEchoProgram
from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations, inverse_permutation, involution_conjugacy_class,
    right_regular_matrix, symmetric_group,
)
from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result,
    upsert_negative_result, utc_now,
)
from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
from symmetric_character import symmetric_character
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path("research/representation/coset_overlap_echo.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COHERENT-OVERLAP-ECHO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@lru_cache(maxsize=5)
def _group_data(n: int) -> tuple:
    if type(n) is not int or not 2 <= n <= 6:
        raise ValueError("exact group contraction budget is restricted to 2<=n<=6")
    group = symmetric_group(n)
    index = {g: i for i, g in enumerate(group)}
    multiply = np.array([[index[compose_permutations(g, h)] for h in group]
                         for g in group], dtype=np.int32)
    inverse = np.array([index[inverse_permutation(g)] for g in group])
    classes = tuple(permutation_cycle_type(g) for g in group)
    multiply.setflags(write=False)
    inverse.setflags(write=False)
    return group, index, multiply, inverse, classes


@lru_cache(maxsize=8)
def reflection_coefficients(n: int, transpositions: int) -> tuple:
    OverlapEchoProgram(n, transpositions, 3)
    group, _, _, _, classes = _group_data(n)
    partitions = integer_partitions(n)
    targets = [(lam, hook_length_dimension(lam), character_on_involution(lam, transpositions))
               for lam in partitions]
    by_class = {cycle: sum(d * (-1 if ch < 0 else 1) * symmetric_character(lam, cycle)
                          for lam, d, ch in targets) for cycle in set(classes)}
    numerator = np.array([by_class[c] for c in classes], dtype=np.int64)
    order = len(group)
    if sum(int(a)**2 for a in numerator) != order**2:
        raise ValueError("character reflection lost exact Parseval normalization")
    numerator.setflags(write=False)
    return numerator, targets


def _probabilities(null_moment: Fraction, hidden_moments: tuple[Fraction, ...]) -> dict:
    if not hidden_moments or any(abs(v) > 1 for v in (null_moment, *hidden_moments)):
        raise ValueError("physical unitary moment outside [-1,1]")
    p0 = (1 - null_moment) / 2
    p1 = sum((1 - m) / 2 for m in hidden_moments) / len(hidden_moments)
    return {
        "null_minus_probability": str(p0), "alternative_minus_probability": str(p1),
        "exact_output_total_variation": str(abs(p0 - p1)),
        "output_total_variation": float(abs(p0 - p1)),
        "fixed_minus_means_null_success": str((1 + p0 - p1) / 2),
        "fixed_orientation_is_useful": p0 > p1,
        "per_hidden_moments": [str(m) for m in hidden_moments],
        "class_covariance_checked": len(set(hidden_moments)) == 1,
    }


@lru_cache(maxsize=8)
def exact_three_copy_echo(n: int, transpositions: int) -> dict:
    """Sum D^2 assignments after eliminating the two endpoint variables.

    W=B A B A. For variables a,b,c,d in chronological order, the three
    group words are ca, dcba, db. Their traces on rho_h are indicators of
    membership in {e,h}. Set c=x a^-1 and d=z b^-1, x,z in {e,h}; only the
    middle constraint remains. The SAME h appears on every register.
    """
    coefficients, targets = reflection_coefficients(n, transpositions)
    group, index, multiply, inverse, _ = _group_data(n)
    order = len(group)
    if 4 * order**2 * max(abs(int(a)) for a in coefficients)**4 > np.iinfo(np.int64).max:
        raise ValueError("exact contraction accumulator budget exceeded")
    identity = index[tuple(range(n))]
    convolution = [sum(int(coefficients[a]) * int(coefficients[multiply[inverse[a], x]])
                       for a in range(order)) for x in range(order)]
    if any(value != (order**2 if x == identity else 0) for x, value in enumerate(convolution)):
        raise ValueError("phase coefficients fail the exact reflection convolution identity")
    hidden = involution_conjugacy_class(n, transpositions)
    support = np.flatnonzero(coefficients)
    support_commutes = bool(np.array_equal(multiply[np.ix_(support, support)],
                                          multiply[np.ix_(support, support)].T))

    def moment(h_index: int | None) -> Fraction:
        choices = (identity,) if h_index is None else (identity, h_index)
        total = 0
        for a in support:
            for x in choices:
                c = multiply[x, inverse[a]]
                if not coefficients[c]:
                    continue
                for z in choices:
                    d = multiply[z, inverse]
                    middle = multiply[multiply[multiply[d, c], np.arange(order)], a]
                    legal = middle == identity
                    if h_index is not None:
                        legal |= middle == h_index
                    total += int(coefficients[a]) * int(coefficients[c]) * int(
                        np.sum(coefficients * coefficients[d] * legal, dtype=np.int64))
        return Fraction(total, order**4)

    m0 = moment(None)
    mh = tuple(moment(index[h]) for h in hidden)
    output = _probabilities(m0, mh)
    raw_cap_squared = min(Fraction(1), Fraction(7, 4 * len(hidden)))
    if Fraction(output["exact_output_total_variation"])**2 > raw_cap_squared:
        raise ValueError("readout violates the three-copy raw information bound")
    return {
        "degree": n, "transpositions": transpositions, "copies": 3, "rounds": 1,
        "group_order": order, "hidden_members_checked": len(hidden),
        "coefficient_denominator": order, "coefficient_support_size": len(support),
        "exact_reflection_convolution_verified": True,
        "coefficient_support_is_commuting": support_commutes,
        "negative_targets": [list(lam) for lam, _, ch in targets if ch < 0],
        "nonmissing_negative_targets": [list(lam) for lam, d, ch in targets if ch < 0 and d + ch > 0],
        "null_word_moment": str(m0),
        "normalized_squared_commutator_norm": str(2 - 2 * m0),
        "raw_three_copy_trace_distance_squared_cap": str(raw_cap_squared),
        "factorial_contraction_is_polynomial_in_degree": False,
        "classical_solver_for_unknown_input_constructed": False,
        "verified": output["class_covariance_checked"],
        **output,
    }


def _tensor(matrices) -> np.ndarray:
    result = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def source_block_control(program: OverlapEchoProgram) -> dict:
    """Keep all source branches with unnormalized blocks, including zero ones."""
    n, k = program.degree, program.copies
    if n not in (3, 4) or k > (5 if n == 3 else 4) or program.rounds > 4:
        raise ValueError("source-block matrix control budget exceeded")
    group, _, _, _, _ = _group_data(n)
    numerators, _ = reflection_coefficients(n, program.transpositions)
    partitions = integer_partitions(n)
    reps = {lam: dict(permutation_representation_matrices(lam)) for lam in partitions}
    hidden = involution_conjugacy_class(n, program.transpositions)
    hypotheses = (None, *hidden)
    moments = np.zeros(len(hypotheses), dtype=complex)
    masses = np.zeros(len(hypotheses))
    minus_probabilities = np.zeros(len(hypotheses))
    residuals = {"query_unitarity": 0.0, "word_unitarity": 0.0,
                 "explicit_hadamard_probability": 0.0, "source_mass": 0.0,
                 "class_covariance": 0.0, "moment_imaginary_part": 0.0}
    blocks = 0
    for sources in product(partitions, repeat=k):
        dimensions = [hook_length_dimension(lam) for lam in sources]
        dimension = math.prod(dimensions)
        identity = np.eye(dimension)
        queries = []
        for bond in range(k - 1):
            unitary = sum((int(coefficient) / len(group) * _tensor(
                reps[lam][g] if i in (bond, bond + 1) else np.eye(dimensions[i])
                for i, lam in enumerate(sources)) for coefficient, g in zip(numerators, group)
                if coefficient), np.zeros((dimension, dimension), dtype=complex))
            residuals["query_unitarity"] = max(residuals["query_unitarity"],
                float(np.linalg.norm(unitary.conj().T @ unitary - identity)))
            queries.append(unitary)
        word = identity.astype(complex)
        for left, _right in program.chronological_bonds():
            word = queries[left] @ word
        residuals["word_unitarity"] = max(residuals["word_unitarity"],
            float(np.linalg.norm(word.conj().T @ word - identity)))
        row_weight = dimension / len(group)**k
        for j, h in enumerate(hypotheses):
            block = _tensor(np.eye(d) if h is None else np.eye(d) + reps[lam][h]
                            for lam, d in zip(sources, dimensions)) * row_weight
            mass = float(np.trace(block).real)
            moment = np.trace(word @ block)
            masses[j] += mass
            moments[j] += moment
            # This is the actual controlled-word/X measurement, not Helstrom.
            minus_kraus = (identity - word) / 2
            direct_minus = np.trace(minus_kraus @ block @ minus_kraus.conj().T)
            minus_probabilities[j] += float(direct_minus.real)
            residuals["explicit_hadamard_probability"] = max(
                residuals["explicit_hadamard_probability"],
                abs(complex(direct_minus) - (mass - moment.real) / 2))
        blocks += 1
    residuals["source_mass"] = float(np.max(np.abs(masses - 1)))
    residuals["class_covariance"] = float(np.max(np.abs(moments[1:] - moments[1])))
    residuals["moment_imaginary_part"] = float(np.max(np.abs(moments.imag)))
    p0, p1 = minus_probabilities[0], np.mean(minus_probabilities[1:])
    residuals["probability_range"] = max(0.0, float(-np.min(minus_probabilities)), float(np.max(minus_probabilities) - 1))
    return {"degree": n, "transpositions": program.transpositions, "copies": k,
        "rounds": program.rounds, "source_blocks_checked": blocks,
        "hidden_members_checked": len(hidden), "null_minus_probability": float(p0),
        "alternative_minus_probability": float(p1), "output_total_variation": float(abs(p0 - p1)),
        "fixed_minus_means_null_success": float((1 + p0 - p1) / 2),
        "residuals": residuals, "verified": max(residuals.values()) < 1e-8}


def regular_control() -> dict:
    """Independent raw regular matrices, bypassing all source-prior formulas."""
    n, k = 3, 3
    group, _, _, _, _ = _group_data(n)
    numerators, _ = reflection_coefficients(n, 1)
    regular = [right_regular_matrix(n, g) for g in group]
    identity = np.eye(len(group))
    a = sum(int(c) / len(group) * _tensor((r, r, identity)) for c, r in zip(numerators, regular))
    b = sum(int(c) / len(group) * _tensor((identity, r, r)) for c, r in zip(numerators, regular))
    word = b @ a @ b @ a
    exact = exact_three_copy_echo(n, 1)
    residual = abs(np.trace(word) / len(group)**k - float(Fraction(exact["null_word_moment"])))
    hidden = involution_conjugacy_class(n, 1)
    for h, predicted in zip(hidden, exact["per_hidden_moments"]):
        state = _tensor([(identity + right_regular_matrix(n, h)) / len(group)] * k)
        residual = max(residual, abs(np.trace(word @ state) - float(Fraction(predicted))))
    averaged_single = sum((identity + right_regular_matrix(n, h)) / len(group) for h in hidden) / len(hidden)
    wrong_moment = float(np.trace(word @ _tensor([averaged_single] * k)).real)
    reverse_undo_residual = float(np.linalg.norm(a @ b @ b @ a - np.eye(len(group)**k)))
    commutator = a @ b - b @ a
    minus_kraus = (np.eye(len(group)**k) - word) / 2
    otoc_residual = float(np.linalg.norm(minus_kraus.conj().T @ minus_kraus - commutator.conj().T @ commutator / 4))
    return {"degree": n, "copies": k, "residual": float(residual),
        "independently_averaged_hidden_minus_probability": (1 - wrong_moment) / 2,
        "shared_hidden_minus_probability": float(Fraction(exact["alternative_minus_probability"])),
        "reverse_order_undo_identity_residual": reverse_undo_residual,
        "state_weighted_commutator_effect_residual": otoc_residual,
        "verified": bool(max(residual, reverse_undo_residual, otoc_residual) < 1e-9)}


def build_overlap_echo_report() -> dict:
    from coset_binary_carrier_instruments import independent_pair_copy_baseline
    exact = [exact_three_copy_echo(*spec) for spec in ((3, 1), (4, 1), (4, 2), (5, 2), (6, 3))]
    physical = [source_block_control(OverlapEchoProgram(*spec)) for spec in
                ((3, 1, 3, 1), (3, 1, 4, 1), (3, 1, 4, 2), (4, 1, 3, 1), (4, 2, 3, 1))]
    regular = regular_control()
    comparisons = []
    for row in physical:
        if row["copies"] == 3 and row["rounds"] == 1:
            partner = next(r for r in exact if (r["degree"], r["transpositions"]) ==
                           (row["degree"], row["transpositions"]))
            comparisons.append(max(abs(row[key] - float(Fraction(partner[key]))) for key in
                ("null_minus_probability", "alternative_minus_probability")))
    baselines = []
    for row in exact:
        if (row["degree"], row["transpositions"]) in ((3, 1), (4, 2), (6, 3)):
            baseline = independent_pair_copy_baseline(row["degree"], row["transpositions"], 3)
            baselines.append({"degree": row["degree"], "transpositions": row["transpositions"],
                "echo_total_variation": row["exact_output_total_variation"],
                "pair_plus_single_total_variation": baseline["exact_total_variation"],
                "echo_group_qft_calls": 8,
                "pair_plus_single_group_qft_calls": 2 * 3 + 2 * baseline["additional_clean_pair_label_queries"],
                "both_copy_budgets": 3,
                "echo_beats_baseline": Fraction(row["exact_output_total_variation"]) > Fraction(baseline["exact_total_variation"]),
                "baseline_has_quantum_frontend": True, "classical_dequantization_proved": False})
    verified = bool(exact and physical and comparisons and all(r["verified"] for r in exact + physical)
                    and regular["verified"] and max(comparisons) < 1e-8)
    s6 = next(row for row in exact if row["degree"] == 6)
    s4 = next(row for row in exact if (row["degree"], row["transpositions"]) == (4, 2))
    return {
        "created_at": utc_now(), "derivation_document": "research/COHERENT_OVERLAP_ECHO.md",
        "primary_literature": [
            {"title": "On the Power of One Bit of Quantum Information", "url": "https://arxiv.org/abs/quant-ph/9802037", "role": "Prior art for mixed-state one-clean-qubit computation; this readout is not a new primitive."},
            {"title": "Measuring the scrambling of quantum information", "url": "https://arxiv.org/abs/1602.06271", "role": "Prior art for echo-based out-of-time-order correlation measurements, not a hidden-subgroup speedup."},
            {"title": "On the Impossibility of a Quantum Sieve Algorithm for Graph Isomorphism", "url": "https://arxiv.org/abs/quant-ph/0612089", "role": "Measured-sieve barrier; model transfer to this unmeasured word is not proved."},
        ],
        "exact_controls": exact, "physical_controls": physical, "regular_control": regular,
        "exact_vs_physical_residuals": comparisons, "baselines": baselines,
        "scaling_contracts": [OverlapEchoProgram(n, n // 2, n*n, n).resource_contract()
                              for n in (6, 10, 18, 34, 66, 130, 258, 514, 1026)],
        "fixed_three_copy_falsifier_contracts": [OverlapEchoProgram(n, n // 2, 3, n).resource_contract()
                              for n in (6, 10, 18, 34, 66, 130, 258, 514, 1026)],
        "claim_gate": {"finite_controls_verified": verified,
            "nonmissing_noncommuting_control_verified": verified and bool(s6["nonmissing_negative_targets"]) and not s6["coefficient_support_is_commuting"],
            "fixed_readout_and_resource_schema_supplied": True,
            "growing_degree_signal_proved": False, "natural_reduction_proved": False,
            "classical_dequantization_proved": False, "independently_reviewed": False,
            "novelty_established": False, "speedup_claim_allowed": False},
        "headline_metrics": {"exact_control_count": len(exact), "physical_control_count": len(physical),
            "hidden_member_exact_control_count": sum(row["hidden_members_checked"] for row in exact),
            "finite_control_failure_count": sum(not row["verified"] for row in exact + physical) + int(not regular["verified"]) + sum(error >= 1e-8 for error in comparisons),
            "scaling_contract_count": 9, "finite_baseline_wins": sum(row["echo_beats_baseline"] for row in baselines),
            "growing_degree_signal_theorem_count": 0, "speedup_count": 0},
        "status": "costed-coherent-program-scaling-unresolved" if verified else "control-failure",
        "summary": "A retained-data overlapping nonmissing-sector echo now has a fixed X readout and charged primitive costs. Exact three-copy controls and growing-copy resource contracts do not establish a scalable advantage.",
        "falsifiers_triggered": (["S4 fixed-point-free negative-character queries have commuting support, so the echo is exactly identity."]
            if s4["coefficient_support_is_commuting"] and Fraction(s4["null_word_moment"]) == 1 else []) +
            (["The three-copy S6 echo fails to beat the pair-plus-single quantum measurement baseline."]
             if any(r["degree"] == 6 and not r["echo_beats_baseline"] for r in baselines) else []),
        "proof_obligations": [
            "Bound the actual fixed X-readout bias for K=n^2 and r=n; no optimal uncompiled measurement may replace it.",
            "Find a contraction or analytic estimate for the growing path word without granting a factorial-table oracle.",
            "Charge errors and repetitions against the proved bias, not just a polynomial number of ideal queries.",
            "Compare legal classical natural-input solvers and preserve the binary promise in a costed reduction.",
            "Check known measured-sieve restrictions without transferring them to an unmeasured overlapping circuit by analogy.",
        ],
    }


def write_overlap_echo_report(output_path: Path = REPORT_PATH, *, write_registry: bool = True,
                              registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                              registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                              registry_result_id: str | None = None) -> dict:
    payload = build_overlap_echo_report()
    payload["artifacts"] = {"report": str(output_path)}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-COSET",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id,
            created_at=payload["created_at"], status=payload["status"], summary=payload["summary"],
            metrics=payload["headline_metrics"], falsifiers_triggered=payload["falsifiers_triggered"],
            artifacts=payload["artifacts"]))
        if payload["claim_gate"]["finite_controls_verified"] and payload["falsifiers_triggered"]:
            upsert_negative_result(NegativeResultRecord(
                id="COHERENT-OVERLAP-ECHO-FINITE-CALIBRATION-LIMITS", source=str(output_path),
                claim="Overlapping negative-character echoes already demonstrate an algorithmic advantage in the finite controls.",
                reason_invalid=" ".join(payload["falsifiers_triggered"]),
                lesson="These are finite readout falsifiers, not a growing-copy no-go, classical solver or general coherent-query bound. A nonzero commutator and leaving a prior bound's scope do not prove useful output bias.",
                applies_to=[registry_candidate_id], evidence={"baselines": payload["baselines"], "artifact": str(output_path)}))
    return payload
