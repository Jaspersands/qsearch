"""Paid adaptive CNOT-tree parity extraction from unknown phase registers.

The exact Bellman solver is an explicitly bounded exponential benchmark,
not a scalable DCP algorithm. The executing controller sees public labels,
ancestry and actual measurement outcomes, never a hidden shift or density.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
from math import comb, factorial
import json
from pathlib import Path

from theorems.lattice_cube_coset_source import exact_int
from theorems.lattice_qft_precision import ceil_log2_rational
from theorems.lattice_sine_window_source import (
    SineWindowSource, SinePhysicalBackend, compile_source, simulate_batch,
    exact_reference, audit_batch, audit_template, _serialize_density,
)
from theorems.ternary_measured_lattice_decoder import exact_json

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "research/DCP_PAID_TREE_RECEIVER.md"
REPORT = ROOT / "research/phase_workbench/dcp_paid_tree_receiver.json"
CONTRACT = ROOT / "research/hypotheses/dcp_paid_tree_receiver_contract.json"


def normalize(state):
    return tuple(sorted(state, key=lambda x: x[1]))


def fixed_forest_baseline(labels, modulus, visibility):
    """Exact best precommitted forest, including terminal classical selection.

    Each block uses a fixed CNOT tree independent of outcomes. Its leaf
    signs are uniform modulo a global sign, irrelevant to target N/2.
    Disjoint blocks have independent branches; choose the best target after
    ALL fixed trees complete. This is stronger than a one-tree comparator.
    """
    m = len(labels)
    if not 1 <= m <= 8:
        raise ValueError("UNKNOWN_FIXED_FOREST_CAP")
    hits, assignments = {}, 0
    for mask in range(1, 1 << m):
        subset = [labels[i] for i in range(m) if mask & (1 << i)]
        count = 0
        for signs in product((-1, 1), repeat=len(subset) - 1):
            assignments += 1
            count += (subset[0] + sum(k * s for k, s in zip(subset[1:], signs))) % modulus == modulus // 2
        hits[mask] = Fraction(count, 1 << (len(subset) - 1))

    def partitions(mask):
        if not mask:
            yield ()
            return
        first = mask & -mask
        subset = mask
        while subset:
            if subset & first:
                for rest in partitions(mask ^ subset):
                    yield (subset,) + rest
            subset = (subset - 1) & mask

    best, best_blocks, tried = Fraction(0), tuple(1 << i for i in range(m)), 0
    for blocks in partitions((1 << m) - 1):
        tried += 1
        none, value = Fraction(1), Fraction(0)
        for mask in sorted(blocks, key=lambda x: (x.bit_count(), x)):
            value += none * hits[mask] * visibility ** mask.bit_count()
            none *= 1 - hits[mask]
        if value > best:
            best, best_blocks = value, blocks
    return {"optimal_target_weighted_visibility": str(best), "best_partition_masks": best_blocks,
            "complete_set_partitions_evaluated": tried, "signed_assignments_evaluated": assignments,
            "postmeasurement_selection_among_all_fixed_tree_targets_included": True}


class PaidTreePlan:
    """Optimal single-target bias within the stated merge/stop policy class."""
    def __init__(self, labels, modulus, visibility_lower, max_states=20000):
        exact_int(modulus, "dyadic modulus", 2)
        if modulus & (modulus - 1):
            raise ValueError("power-of-two modulus required")
        labels = tuple(labels)
        if not labels or len(labels) > 8:
            raise ValueError("UNKNOWN_BELLMAN_ROOT_CAP; not a receiver lower bound")
        for k in labels:
            exact_int(k, "canonical label", 0)
            if k >= modulus:
                raise ValueError("label outside modulus")
        if isinstance(visibility_lower, bool) or not isinstance(visibility_lower, (str, int, Fraction)):
            raise ValueError("exact visibility promise required")
        v = Fraction(visibility_lower)
        if not 0 <= v <= 1:
            raise ValueError("visibility promise in [0,1] required")
        exact_int(max_states, "positive state cap", 1)
        self.labels, self.modulus, self.visibility = labels, modulus, v
        self.max_states, self.values, self.actions = max_states, {}, {}
        self.states_visited = self.actions_evaluated = 0
        self.root = normalize((k, 1 << i) for i, k in enumerate(labels))
        self.value = self.solve(self.root)

    def target_stop(self, state):
        targets = [(self.visibility ** mask.bit_count(), mask)
                   for k, mask in state if k == self.modulus // 2]
        return max(targets, default=(Fraction(0), None), key=lambda x: (x[0], -(x[1] or 0)))

    def child(self, state, left, right, branch):
        a, b = state[left], state[right]
        return normalize([x for i, x in enumerate(state) if i not in (left, right)] +
                         [((a[0] + (1 if branch == 0 else -1) * b[0]) % self.modulus, a[1] | b[1])])

    def solve(self, state):
        if state in self.values:
            return self.values[state]
        self.states_visited += 1
        if self.states_visited > self.max_states:
            raise ValueError("UNKNOWN_BELLMAN_STATE_CAP; partial search is not optimality")
        best, mask = self.target_stop(state)
        action = ("stop", mask)
        # Both control orientations are included. Branches are not chosen.
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:
                    continue
                self.actions_evaluated += 1
                candidate = (self.solve(self.child(state, i, j, 0)) +
                             self.solve(self.child(state, i, j, 1))) / 2
                if candidate > best:
                    best, action = candidate, ("merge", state[i][1], state[j][1])
        self.values[state], self.actions[state] = best, action
        return best

    def record(self, certificate=True):
        fixed = fixed_forest_baseline(self.labels, self.modulus, self.visibility)
        out = {"labels": self.labels, "modulus": self.modulus,
               "externally_assumed_root_visibility_lower": str(self.visibility),
               "optimal_target_weighted_visibility": str(self.value),
               "parity_success_IF_model_and_fair_guess_on_failure": str((1 + self.value) / 2),
               "states_visited": self.states_visited, "ordered_actions_evaluated": self.actions_evaluated,
               "root_count": len(self.labels), "state_cap": self.max_states,
               "algorithm_is_polynomial_in_log_modulus_and_root_count": False,
               "source_model_is_certified_by_label_table": False,
               "policy_class": "PUBLIC_FEEDBACK_CNOT_Z_AND_STOP_WITH_ONE_PARITY_LABEL_X_READOUT"}
        out["fixed_forest_baseline"] = fixed
        out["public_feedback_gain_over_best_fixed_forest"] = str(self.value - Fraction(fixed["optimal_target_weighted_visibility"]))
        if certificate:
            out["Bellman_certificate"] = [{"state": state, "value": str(self.values[state]),
                "action": self.actions[state]} for state in sorted(self.values, key=lambda x: (len(x), x))]
        return out


def execute_plan(plan, backend, receipt_ids):
    """No density, truth, chosen branch, fresh labels or expectation oracle."""
    if not isinstance(plan, PaidTreePlan):
        raise ValueError("complete paid tree plan required")
    receipt_ids = tuple(receipt_ids)
    views = tuple(backend.public_view(rid) for rid in receipt_ids)
    if len(set(receipt_ids)) != len(receipt_ids) or len(views) != len(plan.labels):
        raise ValueError("distinct original roots matching plan required")
    for i, view in enumerate(views):
        if view["modulus"] != plan.modulus or view["label"] != plan.labels[i] or view["original_source_receipts"] != (receipt_ids[i],) or view["merge_depth"]:
            raise ValueError("bound unmerged public source roots required")
    state, live, transcript = plan.root, {1 << i: rid for i, rid in enumerate(receipt_ids)}, []
    while True:
        action = plan.actions[state]
        if action[0] == "stop":
            mask = action[1]
            if mask is None:
                return {"status": "NO_INFORMATIVE_TARGET_ABORT", "parity_bit": None,
                        "transcript": transcript, "roots_supplied_and_paid": len(receipt_ids),
                        "source_preparations_charged": backend.source_preparations_charged,
                        "unknown_phase_registers_reprepared_or_cloned": False}
            view = backend.public_view(live[mask])
            measurement = backend.measure(live[mask], "X")
            return {"status": "ONE_PHYSICAL_PARITY_LABEL_MEASURED", "parity_bit": measurement["outcome"],
                    "transcript": transcript, "terminal_public_receipt": view,
                    "terminal_measurement": measurement, "output_original_leaves": mask.bit_count(),
                    "roots_supplied_and_paid": len(receipt_ids),
                    "source_preparations_charged": backend.source_preparations_charged,
                    "unknown_phase_registers_reprepared_or_cloned": False,
                    "full_shift_recovered": False}
        _, a, b = action
        left, right = backend.public_view(live[a]), backend.public_view(live[b])
        result = backend.merge(live[a], live[b])
        if result["output"] is None:
            raise ValueError("UNKNOWN_PHYSICAL_BRANCH_NUMERICS; no free retry")
        output = result["output"]
        transcript.append({"left": left, "right": right, "actual_branch": result["branch"], "output": output})
        i = next(i for i, x in enumerate(state) if x[1] == a)
        j = next(i for i, x in enumerate(state) if x[1] == b)
        state = plan.child(state, i, j, result["branch"])
        if output["label"] != next(k for k, mask in state if mask == (a | b)):
            raise ValueError("physical output label disagrees with public branch")
        del live[a], live[b]
        live[a | b] = output["id"]


def direct_acquisition_budget(ell, stage, useful_records):
    """IID raw labels, no sieve/chosen-label generator silently supplied."""
    exact_int(ell, "positive phase width", 1)
    exact_int(stage, "prefix stage", 0)
    exact_int(useful_records, "positive useful quota", 1)
    if stage >= ell:
        raise ValueError("prefix stage below width required")
    probability = Fraction(1 << stage, 1 << ell)
    return {"ell": ell, "stage": stage, "stratum_probability": str(probability),
            "useful_record_quota": useful_records,
            "expected_original_preparations_without_sieve": str(useful_records / probability),
            "sieved_acquisition_cost_is_supplied_by_this_bound": False}


def sufficient_quadrature_quota(ell, visibility, failure="1/10"):
    """Hoeffding for scores in [-1,1] with conditional mean +/-v/2.

    m>=8*v^-2*ln(ell/delta) suffices. An exact dyadic logarithm upper
    bound avoids floating-point confidence claims. This is not optimality.
    """
    exact_int(ell, "positive phase width", 1)
    if any(isinstance(x, bool) or not isinstance(x, (int, str, Fraction)) for x in (visibility, failure)):
        raise ValueError("exact visibility and failure budget required")
    v, delta = Fraction(visibility), Fraction(failure)
    if not 0 < v <= 1 or not 0 < delta < 1:
        raise ValueError("positive visibility and subunit failure budget required")
    upper = Fraction(8 * ceil_log2_rational(Fraction(ell) / delta), 1) / (v * v)
    return (upper.numerator + upper.denominator - 1) // upper.denominator


def old_quota_counterexample():
    """Exact rational falsifier of the former factor-two confidence claim.

    ell=3,r=2,k=1,correct prefix=1,bit=0 gives alpha=pi/4.
    Both Pauli choices give D=z/sqrt(2), with p(z=+1)=(1+v/sqrt(2))/2.
    One strictly-negative binomial count already exceeds delta/ell.
    """
    m, ell, delta, v = 35, 3, Fraction(1, 10000), Fraction(4, 5)
    root_lower = Fraction(1414213, 1000000)
    assert root_lower**2 < 2
    p_upper = (1 + v / root_lower) / 2
    j = (m - 1) // 2
    # The binomial term decreases in p for p>j/m; p_upper bounds the true p.
    error_lower = comb(m, j) * p_upper**j * (1 - p_upper)**(m - j)
    x = m * v * v / 2
    exp_lower = sum((x**t / factorial(t) for t in range(17)), Fraction(0))
    assert exp_lower > 2 * ell / delta and error_lower > delta / ell
    return {"ell": ell, "stage": 2, "label": 1, "correct_prefix": 1,
            "true_stage_bit": 0, "root_visibility": str(v), "samples": m,
            "allowed_per_stage_error": str(delta / ell), "total_failure_budget": str(delta),
            "sqrt_two_rational_lower": str(root_lower), "positive_spin_probability_upper": str(p_upper),
            "strict_negative_score_positive_spin_count": j,
            "single_binomial_error_term_lower": str(error_lower),
            "exp_m_v_squared_over_two_Taylor_lower": str(exp_lower),
            "positive_exponential_Taylor_degree": 16,
            "old_factor_two_quota_is_met": True,
            "actual_error_exceeds_claimed_per_stage_budget": True,
            "corrected_sufficient_quota": sufficient_quadrature_quota(ell, v, delta),
            "within_inverse_log_bad_register_promise": 1 - v <= Fraction(1, ell),
            "source_acquisition_or_prefix_learning_is_free": False}


def physical_control(seed):
    source = SineWindowSource(((17, 0), (16, 1)), 7, 1, 0, 2, 4)
    compiled = compile_source(source)
    batch = simulate_batch(compiled, 6, seed, f"paid-tree-{seed}")
    reference = exact_reference(source)
    sampling = audit_batch(source, reference, batch)
    # Fixed external balanced-family promise, not extracted from hidden truth.
    plan = PaidTreePlan(tuple(r.label for r in batch.receipts), source.phase_modulus, "1/4")
    backend = SinePhysicalBackend(batch, seed + 100)
    result = execute_plan(plan, backend, tuple(r.id for r in batch.receipts))
    if result.get("terminal_public_receipt"):
        rid = result["terminal_public_receipt"]["id"]
        result["PRIVATE_AUDIT_ONLY_terminal_density"] = _serialize_density(backend._states[rid])
    return {"compiled_source_sampling_audit": sampling,
            "physical_source_certificate": {"compiled_resources": compiled.resource_record(),
                "exact_reference": reference, "actual_sampling_audit": sampling,
                "private_template_audit": audit_template(source, reference, (1, -1))},
            "public_plan": plan.record(),
            "actual_execution": result,
            "source_model_status": "FINITE_KNOWN_CONTROL_NOT_A_HARDNESS_OR_GROWING_PROMISE_CERTIFICATE",
            "only_one_parity_bit_targeted": True, "full_DCP_algorithm_claimed": False}


def build_report():
    cases = [((1, 3), 8, "3/4"), ((1, 1, 2), 8, "3/4"),
             ((1, 31), 64, "3/4"), ((1, 2, 3, 5), 16, "3/4"), ((1, 31, 2), 64, "3/4")]
    controls = [PaidTreePlan(k, N, v).record() for k, N, v in cases]
    deps = ("lattice_sine_window_source.py", "lattice_sine_packet.py", "lattice_cube_dcp_readout.py",
            "lattice_cube_coset_source.py", "lattice_qft_precision.py", "planted_qary_usvp_source.py",
            "ternary_measured_lattice_decoder.py")
    return {"status": "PAID_ADAPTIVE_SINGLE_TARGET_CNOT_TREE_BENCHMARK_NOT_A_DCP_SOLVER",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "dependency_sha256": {p: hashlib.sha256((ROOT / "theorems" / p).read_bytes()).hexdigest() for p in deps},
            "exact_finite_policy_controls": controls,
            "actual_physical_source_controls": [physical_control(seed) for seed in (86101, 86102, 86103, 86104)],
            "raw_label_acquisition_profiles": [direct_acquisition_budget(ell, r, 10)
                for ell in (16, 64, 256) for r in (0, ell - 1)],
            "feedback_template_raw_source_bounds": [{"ell": ell, "original_roots": ell * ell,
                "template": "ORDERED_ORIGINAL_LABELS_a_N/2-a_2a_WITH_NO_INITIAL_PARITY_TARGET",
                "probability_any_template_upper": str(min(Fraction(1),
                    Fraction((ell*ell)*(ell*ell-1)*(ell*ell-2)*((1<<ell)-4), (1<<ell)**3))),
                "generated_or_sieved_labels_covered": False} for ell in (16, 64, 256)],
            "old_quadrature_confidence_claim_counterexample": old_quota_counterexample(),
            "actual_source_preparations_charged": 24,
            "zero_labels_are_secret_independent_not_successful_parity_targets": True,
            "finite_policy_optimum_is_general_quantum_optimum": False,
            "efficient_noisy_receiver_supplied": False, "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False, "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print("Actual preparations:", report["actual_source_preparations_charged"])


if __name__ == "__main__":
    main()
