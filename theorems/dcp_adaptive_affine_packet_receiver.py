"""Paid affine-Z feedback on native carry packets: exact, exponential benchmark.

All policy decisions depend only on public labels, chart geometry and observed
measurement bits. No private phase/secret evaluator is available to the policy.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from random import Random

from theorems.dcp_adaptive_direction_rank_gate import (
    binary_basis, binary_kernel, binary_map, dyadic, integer,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_adaptive_affine_packet_receiver.json"
CONTRACT = ROOT / "research/hypotheses/dcp_adaptive_affine_packet_receiver_contract.json"


class ResearchCap(ValueError):
    """An unexecuted search, not evidence against a quantum mechanism."""


@dataclass(frozen=True)
class Policy:
    max_input_qubits: int = 10
    max_logical_qubits: int = 5
    max_states: int = 20000
    max_actions: int = 100000

    def __post_init__(self):
        for key, value in vars(self).items():
            integer(value, key, 1)


def gaussian_binomial(k, d):
    integer(k, "ambient binary dimension", 0, 256)
    integer(d, "subspace dimension", 0, k)
    numerator = denominator = 1
    for j in range(d):
        numerator *= (1 << (k - j)) - 1
        denominator *= (1 << (d - j)) - 1
    return numerator // denominator


def search_cost(k, initial_rank):
    integer(initial_rank, "initial parity rank", 0, 4096)
    integer(k, "remaining logical dimension", 1, 256)
    strata = []
    for d in range(1, k + 1):
        states = (1 << (initial_rank + k - d)) * gaussian_binomial(k, d)
        actions = states * ((1 << d) - 1) if d > 1 else 0
        strata.append((d, states, actions))
    return {"logical_dimension": k, "initial_parity_rank": initial_rank,
            "all_syndromes_chart_states": sum(s for _, s, _ in strata),
            "all_syndromes_chart_actions": sum(a for _, _, a in strata),
            "dimension_strata": strata}


def canonical_chart(basis, origin, width):
    basis = binary_basis(basis, width)
    for row in basis:
        if origin >> (row.bit_length() - 1) & 1:
            origin ^= row
    return basis, origin


def points(basis, origin):
    out = [origin]
    for row in basis:
        out += [x ^ row for x in out]
    return tuple(sorted(out))


def split_chart(basis, origin, form, width):
    """Measure a nonzero binary linear functional in the CURRENT chart."""
    integer(form, "nonzero chart functional", 1, (1 << len(basis)) - 1)
    pivot = (form & -form).bit_length() - 1
    subspace = tuple(v ^ (basis[pivot] if form >> j & 1 else 0)
                     for j, v in enumerate(basis) if j != pivot)
    return (canonical_chart(subspace, origin, width),
            canonical_chart(subspace, origin ^ basis[pivot], width))


def output_label(labels, phase_bits, x, y):
    Q = 1 << (phase_bits - 1)
    delta = tuple(sum(a * (((y >> i) & 1) - ((x >> i) & 1))
                      for i, a in enumerate(row)) for row in labels)
    if any(d & 1 for d in delta):
        raise ValueError("pair not in a common parity-chart fibre")
    return tuple(d // 2 % Q for d in delta)


def is_useful_descent(label):
    return not any(a & 1 for a in label) and any(a != 0 for a in label)


def quadratic_low_phase_map(labels, phase_bits, basis, origin):
    """The next low phase is a vector quadratic map on the binary chart.

    Only linear coefficients depend on higher labels/background. Polar
    coefficients are B(u_i AND u_j), fixed by native low labels and chart.
    This public polynomial does not prepare/evaluate an unknown quantum state.
    """
    B = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in labels)
    linear = [sum((a & 1) << j for j, a in enumerate(
        output_label(labels, phase_bits, origin, origin ^ u))) for u in basis]
    cross = [{"i": i, "j": j, "coefficient_hex": hex(binary_map(B, basis[i] & basis[j]))}
             for i in range(len(basis)) for j in range(i + 1, len(basis))]
    return {"linear_coefficients_hex": [hex(v) for v in linear], "cross_terms": cross,
            "constant_coefficient": 0, "degree_at_most_two": True,
            "public_polynomial_is_unknown_state_preparation_oracle": False}


def evaluate_quadratic(record, z):
    integer(z, "quadratic chart coordinate", 0, (1 << len(record["linear_coefficients_hex"])) - 1)
    out = 0
    for j, coefficient in enumerate(record["linear_coefficients_hex"]):
        if z >> j & 1:
            out ^= int(coefficient, 16)
    for term in record["cross_terms"]:
        if ((z >> term["i"]) & (z >> term["j"]) & 1):
            out ^= int(term["coefficient_hex"], 16)
    return out


def solve(labels, phase_bits=4, *, policy=Policy()):
    integer(phase_bits, "phase bits", 3, 256)
    labels = tuple(tuple(row) for row in labels)
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular public label matrix required")
    n, m, q = len(labels), len(labels[0]), 1 << phase_bits
    if m > policy.max_input_qubits:
        raise ResearchCap("UNKNOWN: native input register cap")
    for row in labels:
        for a in row:
            integer(a, "canonical label", 0, q - 1)
    B = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in labels)
    K = binary_basis(binary_kernel(B, m), m)
    k, rank = len(K), m - len(K)
    if not k or k > policy.max_logical_qubits:
        raise ResearchCap("UNKNOWN: retained logical dimension cap")
    cost = search_cost(k, rank)
    if cost["all_syndromes_chart_states"] > policy.max_states or cost["all_syndromes_chart_actions"] > policy.max_actions:
        raise ResearchCap("UNKNOWN: exact Bellman policy-search work cap")
    roots = sorted({canonical_chart(K, x, m)[1] for x in range(1 << m)})
    memo, states = {}, []

    def visit(basis, origin):
        key = basis, origin
        if key in memo:
            return memo[key]
        record = {"basis_hex": [hex(v) for v in basis], "origin_hex": hex(origin),
                  "dimension": len(basis)}
        if len(basis) == 1:
            label = output_label(labels, phase_bits, origin, origin ^ basis[0])
            good = 2 * int(is_useful_descent(label))
            record.update(output_label_hex=[hex(a) for a in label], useful_descent=bool(good),
                          good_assignments=good, actions=[], chosen_form=None)
        else:
            actions = []
            for form in range(1, 1 << len(basis)):
                children = [visit(*chart) for chart in split_chart(basis, origin, form, m)]
                good = sum(states[c]["good_assignments"] for c in children)
                actions.append({"form": form, "children": children, "good_assignments": good})
            best = max(actions, key=lambda a: (a["good_assignments"], -a["form"]))
            record.update(good_assignments=best["good_assignments"], actions=actions,
                          chosen_form=best["form"])
        identifier = len(states)
        memo[key] = identifier
        record["id"] = identifier
        states.append(record)
        return identifier

    root_ids = [visit(K, x) for x in roots]
    all_u = points(K, 0)[1:]
    static, pairing_bounds = [], []
    for x0 in roots:
        assignments = points(K, x0)
        choices = []
        for u in all_u:
            good = sum(2 * int(is_useful_descent(output_label(labels, phase_bits, x, x ^ u)))
                       for x in assignments if x < (x ^ u))
            choices.append({"physical_direction_hex": hex(u), "good_assignments": good})
        best = max(choices, key=lambda c: (c["good_assignments"], -int(c["physical_direction_hex"], 16)))
        static.append({"origin_hex": hex(x0), "all_direction_scores": choices,
                       "best_good_assignments": best["good_assignments"],
                       "best_direction_hex": best["physical_direction_hex"]})
        classes = {}
        for x in assignments:
            phase_value = output_label(labels, phase_bits, x0, x)
            low = tuple(a & 1 for a in phase_value)
            classes.setdefault(low, Counter())[phase_value] += 1
        blocks = []
        for low, counts in sorted(classes.items()):
            size, largest = sum(counts.values()), max(counts.values())
            # Complete multipartite graph: equal low phase, unequal full phase.
            pairs = min(size // 2, size - largest)
            blocks.append({"low_phase_bits": list(low), "population": size,
                           "largest_equal_full_phase_class": largest,
                           "maximum_useful_pairs": pairs})
        pairing_bounds.append({"origin_hex": hex(x0), "color_blocks": blocks,
                               "maximum_good_assignments": 2 * sum(b["maximum_useful_pairs"] for b in blocks)})
    adaptive_good = sum(states[r]["good_assignments"] for r in root_ids)
    static_good = sum(row["best_good_assignments"] for row in static)
    pairing_good = sum(row["maximum_good_assignments"] for row in pairing_bounds)
    if adaptive_good > pairing_good:
        raise ArithmeticError("affine policy exceeds unrestricted basis-pairing bound")
    leaves = []
    def collect(identifier):
        state = states[identifier]
        if state["dimension"] == 1:
            leaves.append(identifier)
            return
        chosen = next(a for a in state["actions"] if a["form"] == state["chosen_form"])
        for child in chosen["children"]:
            collect(child)
    for root in root_ids:
        collect(root)
    hist = Counter(tuple(states[i]["output_label_hex"]) for i in leaves)
    if len(states) != cost["all_syndromes_chart_states"] or sum(len(s["actions"]) for s in states) != cost["all_syndromes_chart_actions"]:
        raise ArithmeticError("Bellman geometry census disagrees with Gaussian-binomial cost")
    return {
        "phase_bits": phase_bits, "component_count": n, "input_qubits": m,
        "public_labels_hex": [[hex(a) for a in row] for row in labels],
        "root_kernel_dimension": k, "initial_parity_rank": rank,
        "root_ids_all_syndromes": root_ids, "states": states,
        "root_quadratic_maps": [dict(root_id=i, **quadratic_low_phase_map(
            labels, phase_bits, K, int(states[i]["origin_hex"], 16))) for i in root_ids],
        "static_comparator_all_syndromes": static, "search_cost": cost,
        "arbitrary_basis_pairing_bounds_all_syndromes": pairing_bounds,
        "arbitrary_basis_pairing_useful_descent_upper_bound": dyadic(Fraction(pairing_good, 1 << m)),
        "affine_policy_saturates_arbitrary_pairing_bound": adaptive_good == pairing_good,
        "arbitrary_basis_pairing_bound_is_general_quantum_optimum": False,
        "optimal_feedback_useful_descent_probability": dyadic(Fraction(adaptive_good, 1 << m)),
        "best_static_useful_descent_probability": dyadic(Fraction(static_good, 1 << m)),
        "feedback_gain": dyadic(Fraction(adaptive_good - static_good, 1 << m)),
        "chosen_policy_leaf_ids": leaves,
        "retained_label_distribution_all_outcomes": [
            {"label_hex": list(label), "physical_outcome_pairs": count,
             "probability": dyadic(Fraction(2 * count, 1 << m)),
             "useful_descent": is_useful_descent(tuple(int(a, 16) for a in label))}
            for label, count in sorted(hist.items())],
        "resource_ledger_per_supplied_packet": {
            "original_unknown_phase_qubits": m,
            "initial_syndrome_Z_measurements": rank,
            "adaptive_complement_Z_measurements": k - 1,
            "retained_qubits": 1,
            "every_branch_probability_charged": True,
            "initial_syndromes_postselected": False,
            "secret_or_unknown_state_evaluator_available_to_policy": False,
            "source_preparation_inverse_available": False,
        },
        "objective_excludes_zero_labels": True,
        "guarantee_conditional_on_supplied_public_A": True,
        "noise_model": "pure-flat-native-phase-packet",
        "classical_policy_search_polynomial_time": False,
        "general_quantum_optimum": False,
    }


def execute_public_policy(certificate, port):
    """Port owns unknown states; controller sees only public measurement bits.

    A production port must implement the declared chart changes and Z
    measurements, not evaluate the hidden phase. Tests use physical projectors.
    No quantum source/preparation implementation is implied by this interface.
    """
    states = certificate["states"]
    labels = tuple(tuple(int(a, 16) for a in row) for row in certificate["public_labels_hex"])
    B = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in labels)
    syndrome = port.measure_initial_parity(B)
    integer(syndrome, "observed initial syndrome", 0, (1 << len(B)) - 1)
    roots = [i for i in certificate["root_ids_all_syndromes"]
             if binary_map(B, int(states[i]["origin_hex"], 16)) == syndrome]
    if len(roots) != 1:
        raise ValueError("inconsistent measured initial syndrome")
    identifier, transcript = roots[0], []
    while states[identifier]["dimension"] > 1:
        state = states[identifier]
        basis = tuple(int(v, 16) for v in state["basis_hex"])
        origin, form = int(state["origin_hex"], 16), state["chosen_form"]
        bit = port.measure_chart_linear(basis, origin, form)
        integer(bit, "observed complement bit", 0, 1)
        transcript.append({"state_id": identifier, "form": form, "outcome": bit})
        action = next(a for a in state["actions"] if a["form"] == form)
        identifier = action["children"][bit]
    leaf = states[identifier]
    receipt = port.retain_pair(int(leaf["origin_hex"], 16), int(leaf["basis_hex"][0], 16))
    return {"leaf_id": identifier, "measurement_transcript": transcript,
            "output_label_hex": leaf["output_label_hex"],
            "useful_descent": leaf["useful_descent"], "unknown_output_receipt": receipt}


def exact_json(value):
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int):
        return hex(value) if abs(value) > (1 << 53) - 1 else value
    if isinstance(value, (list, tuple)):
        return [exact_json(v) for v in value]
    if isinstance(value, dict):
        return {k: exact_json(v) for k, v in value.items()}
    return value


def build_report():
    cases = []
    for n, m, seed in ((1, 5, 0), (1, 5, 1), (1, 5, 2), (2, 6, 3), (2, 6, 4), (2, 6, 5)):
        rng = Random(seed)
        labels = tuple(tuple(rng.randrange(16) for _ in range(m)) for _ in range(n))
        case = solve(labels)
        case["public_source_selection"] = {"kind": "unfiltered-fixed-seed-native-IID-label-control",
                                           "seed": seed, "asymptotic_success_estimate": False,
                                           "source_quantum_preparations_executed": 0}
        cases.append(case)
    contract = json.loads(CONTRACT.read_text())
    rng = Random(94)
    gap = solve(tuple(tuple(rng.randrange(16) for _ in range(6)) for _ in range(2)))
    gap["public_source_selection"] = {
        "kind": "SELECTED-affine-grammar-gap-counterexample-not-unfiltered-cohort",
        "seed": 94, "fixed_seed_search_controls_examined": 95,
        "asymptotic_success_estimate": False,
        "source_quantum_preparations_executed": 0,
    }
    return exact_json({
        "status": "BOUNDED_AFFINE_FEEDBACK_OPTIMUM_NOT_EFFICIENT_RECEIVER",
        "contract_id": contract["contract_id"], "source_controls": cases,
        "affine_grammar_gap_counterexample": gap,
        "known_algorithm_boundary": {
            "base_group": "(Z_(2^t))^n with inversion semidirect action by Z_2",
            "nilpotency_class": "t; a fixed t is constant-class, not growing-class evidence",
            "fixed_t_full_HSP_oracle_novelty_claim_allowed": False,
            "constant_class_bounded_prime_theorem": "https://arxiv.org/html/2304.08376v1",
            "exact_theorem_requires_subgroup_state_creating_unitary_and_inverse": True,
            "copy_only_phase_source_transfer_proved": False,
            "nonexact_forward_only_HSMC_variant_in_Proposition3_exists": True,
            "missing_inverse_alone_blocks_all_published_methods": False,
            "existing_copy_to_coset_compiler": "research/NATIVE_ORBIT_SOURCE_ACCESS.md",
            "uniform_polynomial_bound_when_t_grows_supplied": False,
            "nil2_quadratic_cancellation_reference": "https://arxiv.org/html/0707.1260",
            "already_in_repo_context": "research/reductions/hsp_campaign_claim_audit.json",
        },
        "scaling_cost_ledgers_not_executed": [search_cost(k, 0) for k in (4, 8, 16, 32, 64)],
        "scope": contract["scope"], "remaining_proof_obligations": contract["remaining_proof_obligations"],
        "accepted_speedup_candidate": False, "novelty_claim": False,
        "efficient_receiver_supplied": False,
        "zero_output_labels_counted_as_success": False,
        "source_quantum_preparations_executed": 0,
    })


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "source_controls": len(report["source_controls"]),
                      "strict_feedback_gains": sum(c["feedback_gain"]["numerator_hex"] != "0x0"
                                                   for c in report["source_controls"]),
                      "accepted_speedup_candidate": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
