"""Exact higher-rank falsifier and observable-basis repair for native moments.

LOCAL DERIVATION / REVIEW PENDING. Full sparse Bochner consistency need not
give a distribution over secrets. The repair proves a saturation/error bound,
not native noisy likelihood tightness or an efficient decoder.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from flint import nmod_mat
from sympy import Matrix

from ternary_character_synchronization import _records, lifted_inverse, rank_one_character_lift
from ternary_covariant_noise import CovariantRecord

ROOT = Path(__file__).resolve().parents[1]
BASE_REPORT = ROOT / "research/classical_baselines/ternary_character_synchronization.json"
DERIVATION = ROOT / "research/TERNARY_OBSERVABLE_MOMENT_LIFT.md"
REPORT = ROOT / "research/classical_baselines/ternary_observable_moment_lift.json"


def difference_basis(records):
    records, n, q = _records(records)
    rows = [tuple((a-b) % q for a, b in zip(r.first, r.second)) for r in records]
    reduced, rank = nmod_mat([[row[j] % 3 for row in rows] for j in range(n)], 3).rref()
    if rank < n:
        return {"status": "UNKNOWN_NO_FULL_UNIT_DIFFERENCE_BASIS", "rank_mod3": int(rank)}
    basis = tuple(next(j for j in range(len(rows)) if reduced[i, j]) for i in range(n))
    inverse = lifted_inverse([rows[j] for j in basis], q)
    return {"status": "FULL_UNIT_DIFFERENCE_BASIS", "rank_mod3": n,
            "basis_record_indices": basis,
            "modular_unit_difference_inverse": [list(map(int, inverse.row(i))) for i in range(n)]}


def full_moment_stencils(lift, q, max_entries=1_000_000):
    """Complete equality audit, with one representative for each difference."""
    nodes = lift["nodes"]
    if type(max_entries) is not int or max_entries < 1:
        raise ValueError("positive whole-table moment cap required")
    if len(nodes)**2 > max_entries:
        raise ValueError("complete moment closure exceeds whole-table cap")
    stencils = list(lift["linear_moment_stencils"])
    seen = {}
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            difference = tuple((a-b) % q for a, b in zip(u["frequency"], v["frequency"]))
            old = seen.setdefault(difference, (i, j))
            if old != (i, j):
                stencils.append({"kind": "full_translation", "left_entry": old, "right_entry": (i, j)})
    return stencils, {"all_moment_entries_checked": len(nodes)**2,
                      "distinct_frequency_differences": len(seen),
                      "full_translation_equalities": len(nodes)**2-len(seen)}


def partition_witness(lift, q, imposed_equalities=(), max_entries=1_000_000):
    """Exact PSD: give every final equivalence class an orthogonal unit vector.

    A stencil with one diagonal-class entry forces the other entry to be one.
    At the fixed point all stencils compare either two ones or two zeros.
    """
    stencils, closure = full_moment_stencils(lift, q, max_entries)
    parent = list(range(len(lift["nodes"])))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def merge(i, j):
        a, b = find(i), find(j)
        if a == b:
            return False
        parent[max(a, b)] = min(a, b)
        return True

    for i, j in imposed_equalities:
        if not (0 <= i < len(parent) and 0 <= j < len(parent)):
            raise ValueError("imposed Gram equality outside complete node vocabulary")
        merge(i, j)
    passes = 0
    changed = True
    while changed:
        changed = False
        passes += 1
        for stencil in stencils:
            a, b = stencil["left_entry"]
            c, d = stencil["right_entry"]
            if find(a) == find(b):
                changed = merge(c, d) or changed
            if find(c) == find(d):
                changed = merge(a, b) or changed
    classes = tuple(find(i) for i in range(len(parent)))
    for stencil in stencils:
        a, b = stencil["left_entry"]
        c, d = stencil["right_entry"]
        if (classes[a] == classes[b]) != (classes[c] == classes[d]):
            raise ArithmeticError("partition Gram failed an exact moment constraint")
    return {"class_labels": classes, "matrix_rank_exact": len(set(classes)),
            "PSD_certificate": "M_ij=1[class(i)=class(j)], Gram of orthogonal class unit vectors",
            "all_diagonal_entries_one": True, "all_selected_and_full_translation_constraints_satisfied": True,
            "closure_passes": passes, **closure}


class _Circuit:
    def __init__(self, records, lift, max_nodes):
        self.records, self.n, self.q = _records(records)
        if type(max_nodes) is not int or max_nodes < len(lift["nodes"]):
            raise ValueError("whole observable-circuit node cap exceeded")
        self.rows = [row for r in records for row in (r.first, r.second)]
        self.ys = [x for r in records for x in r.outcome]
        self.nodes = deepcopy(lift["nodes"])
        self.stencils = deepcopy(lift["linear_moment_stencils"])
        self.indices = {tuple(x["formal_coefficients"]): i for i, x in enumerate(self.nodes)}
        self.max_nodes = max_nodes
        self.powers = {}
        self.conjugated = {s["left_entry"][0] for s in self.stencils if s["kind"] == "conjugation"}

    def node(self, formal):
        formal = tuple(x % self.q for x in formal)
        if formal not in self.indices:
            if len(self.nodes) >= self.max_nodes:
                raise ValueError("whole observable-circuit node cap exceeded")
            self.indices[formal] = len(self.nodes)
            self.nodes.append({"formal_coefficients": formal,
                               "frequency": tuple(sum(a*row[j] for a, row in zip(formal, self.rows)) % self.q for j in range(self.n)),
                               "fake_observed_phase_exponent": sum(a*y for a, y in zip(formal, self.ys)) % self.q})
        return self.indices[formal]

    def negative(self, i):
        j = self.node(tuple(-x for x in self.nodes[i]["formal_coefficients"]))
        if i not in self.conjugated:
            self.stencils.append({"kind": "conjugation", "left_entry": (i, 0), "right_entry": (0, j)})
            self.conjugated.add(i)
        return j

    def add(self, i, j):
        k = self.node(tuple(a+b for a, b in zip(self.nodes[i]["formal_coefficients"], self.nodes[j]["formal_coefficients"])))
        neg = self.negative(j)
        self.stencils.append({"kind": "addition", "left_entry": (k, 0), "right_entry": (i, neg)})
        return k

    def multiply(self, i, coefficient):
        if coefficient < 0:
            i, coefficient = self.negative(i), -coefficient
        total, power, bit = 0, i, 0
        while coefficient:
            if coefficient & 1:
                total = self.add(total, power)
            coefficient >>= 1
            bit += 1
            if coefficient:
                if (i, bit) not in self.powers:
                    self.powers[i, bit] = self.add(power, power)
                power = self.powers[i, bit]
        return total


def observable_refinement(records, max_nodes=10000, max_entries=1_000_000):
    """Anchor pair differences and reconstruct native rows in that unit basis."""
    records, n, q = _records(records)
    basis = difference_basis(records)
    if basis["rank_mod3"] < n:
        return {**basis, "observable_saturation_bound_certified": False}
    original = rank_one_character_lift(records, max_nodes=max_nodes)
    circuit = _Circuit(records, original, max_nodes)
    native = [x["native_node"] for x in original["native_target_maps"]]
    difference_nodes = []
    for i in range(len(records)):
        formal = [0]*len(circuit.rows)
        formal[2*i], formal[2*i+1] = 1, -1
        node = circuit.node(formal)
        difference_nodes.append(node)
        circuit.stencils.append({"kind": "pair_difference_anchor", "left_entry": (node, 0),
                                 "right_entry": (native[2*i], native[2*i+1])})
    indices = basis["basis_record_indices"]
    inverse = Matrix(basis["modular_unit_difference_inverse"])
    loops = []
    for i in indices:
        endpoint = circuit.multiply(difference_nodes[i], q)
        if endpoint != 0:
            raise ArithmeticError("observable basis q-loop did not close")
        loops.append({"basis_record_index": i, "integer_multiplier": q, "endpoint": endpoint})
    targets = []
    for j, row in enumerate(circuit.rows):
        canonical = tuple(int(x) % q for x in Matrix([row])*inverse)
        balanced = tuple(c if 2*c < q else c-q for c in canonical)
        total = 0
        for i, coefficient in zip(indices, balanced):
            if coefficient:
                total = circuit.add(total, circuit.multiply(difference_nodes[i], coefficient))
        circuit.stencils.append({"kind": "observable_native_target", "left_entry": (total, 0),
                                 "right_entry": (native[j], 0)})
        targets.append({"frequency_row": j, "computed_node": total, "native_node": native[j],
                        "canonical_basis_coefficients": canonical, "balanced_basis_coefficients": balanced})
    lift = {"nodes": circuit.nodes, "linear_moment_stencils": circuit.stencils,
            "native_target_maps": original["native_target_maps"]}
    for stencil in circuit.stencils:
        def difference(pair):
            return tuple((a-b) % q for a, b in zip(circuit.nodes[pair[0]]["frequency"], circuit.nodes[pair[1]]["frequency"]))
        if difference(stencil["left_entry"]) != difference(stencil["right_entry"]):
            raise ArithmeticError("observable repair introduced an invalid native moment constraint")
    _, closure = full_moment_stencils(lift, q, max_entries)
    constant = sum(sum(c*c for c in t["balanced_basis_coefficients"]) for t in targets)
    weight = min(Fraction(1, len(records)*q*q), Fraction(1, 1+constant))
    residual_constants = [6*sum(abs(c) for c in t["balanced_basis_coefficients"])+1 for t in targets]
    residual_energy = sum(x*x for x in residual_constants)
    amplification = weight*residual_energy/(1-weight*constant)
    gap = 2*len(records)*weight
    return {"status": "OBSERVABLE_BASIS_SATURATION_AND_ERROR_BOUND_REVIEW_PENDING",
            **lift, "difference_basis": basis, "pair_difference_nodes": difference_nodes,
            "observable_basis_q_loops": loops, "observable_native_target_maps": targets,
            "sum_native_balanced_coefficient_squared_norms": constant,
            "native_anchor_total_deficit_upper_per_basis_pair_deficit": constant,
            "weighted_separating_score_anchor_weight": str(weight),
            "weighted_diagnostic_repaired_all_rank_optimum": str(Fraction(len(records))-2*len(records)*weight),
            "weighted_diagnostic_integrality_gap_before_repair": str(2*len(records)*weight),
            "per_native_target_stencil_residual_error_constants": residual_constants,
            "sum_stencil_residual_error_constant_squares": residual_energy,
            "weighted_objective_excess_upper_per_max_complex_stencil_residual": str(amplification),
            "max_stencil_residual_for_half_diagnostic_gap": str(gap/(2*amplification)),
            "residual_bound_requires_exact_PSD_and_unit_diagonal": True,
            "observable_saturation_bound_certified": True,
            "all_rank_repair_applies_to_weighted_diagnostic_not_native_noisy_likelihood": True,
            "every_exact_saturated_basis_pair_forces_shared_character_native_anchors": True,
            "matrix_dimension": len(circuit.nodes), "dense_PSD_complex_entries": len(circuit.nodes)**2,
            "complete_moment_closure": closure, "noisy_recovery_or_general_convex_tightness_proved": False}


def residual_budget(refinement, max_complex_stencil_residual):
    """Conditional exact-rational gate; numerical PSD/diagonal is NOT certified."""
    if type(max_complex_stencil_residual) not in (int, Fraction) or max_complex_stencil_residual < 0:
        raise ValueError("nonnegative exact rational stencil residual required")
    if not refinement.get("observable_saturation_bound_certified"):
        raise ValueError("complete observable refinement certificate required")
    tau = Fraction(max_complex_stencil_residual)
    amplification = Fraction(refinement["weighted_objective_excess_upper_per_max_complex_stencil_residual"])
    excess = amplification*tau
    gap = Fraction(refinement["weighted_diagnostic_integrality_gap_before_repair"])
    optimum = Fraction(refinement["weighted_diagnostic_repaired_all_rank_optimum"])
    return {"maximum_complex_stencil_residual": str(tau),
            "conditional_weighted_diagnostic_score_upper": str(optimum+excess),
            "conditional_weighted_diagnostic_excess_upper": str(excess),
            "at_most_half_original_diagnostic_gap": excess <= gap/2,
            "condition_requires_exact_PSD_and_unit_diagonal": True,
            "floating_solver_eigenvalues_or_diagonal_certified": False,
            "native_noisy_likelihood_recovery_certified": False}


def native_falsifier(records, max_nodes=10000, max_entries=1_000_000):
    records, n, q = _records(records)
    basis = difference_basis(records)
    if basis["rank_mod3"] < n:
        return {**basis, "noncharacter_mixture_falsifier_certified": False}
    original = rank_one_character_lift(records, max_nodes=max_nodes)
    native = [x["native_node"] for x in original["native_target_maps"]]
    pairs = tuple((native[2*i], native[2*i+1]) for i in range(len(records)))
    witness = partition_witness(original, q, pairs, max_entries)
    classes = witness["class_labels"]
    anchor = tuple(int(classes[i] == classes[0]) for i in native)
    if any(anchor):
        return {"status": "UNKNOWN_PARTITION_COLLAPSED_NATIVE_ANCHORS", "difference_basis": basis,
                "partition_witness": witness, "noncharacter_mixture_falsifier_certified": False}
    repair = observable_refinement(records, max_nodes, max_entries)
    repaired_pairs = tuple((native[2*i], native[2*i+1]) for i in range(len(records)))
    repaired = partition_witness(repair, q, repaired_pairs, max_entries)
    if any(repaired["class_labels"][i] != repaired["class_labels"][0] for i in native):
        raise ArithmeticError("saturated observable-basis repair failed to force native anchors")
    m = len(records)
    weight = Fraction(repair["weighted_separating_score_anchor_weight"])
    return {"status": "FULL_TRANSLATION_PSD_NOT_A_CHARACTER_MIXTURE_REVIEW_PENDING",
            "records": [r.public() for r in records], "difference_basis": basis,
            "original_native_nodes": native, "saturated_native_pairs": pairs,
            "partition_witness": witness, "original_native_anchor_moments": anchor,
            "noncharacter_mixture_falsifier_certified": True,
            "character_mixture_contradiction": "unit difference basis has expectation1, forcing support only at secret0; native anchors are0, not1",
            "weighted_diagnostic": {"pair_weight": "1", "native_anchor_penalty": str(weight),
                                    "partition_PSD_score": str(m),
                                    "true_character_maximum": str(Fraction(m)-2*m*weight),
                                    "true_maximum_attained_at_secret": [0]*n,
                                    "exact_integrality_gap": str(2*m*weight),
                                    "maximum_requires_no_secret_enumeration": True,
                                    "is_native_noisy_likelihood_objective": False},
            "observable_refinement": repair, "saturated_repaired_partition": repaired,
            "hidden_secret_or_outcomes_used_to_select_falsifier_or_circuit": False,
            "external_original_source_supply_physically_certified": False,
            "pointwise_representation_failure_is_random_source_decoder_failure": False}


def run_controls():
    base = json.loads(BASE_REPORT.read_text())
    controls = []
    for source in base["native_controls"]:
        records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                        for r in source["native_records"])
        result = native_falsifier(records)
        if not result["noncharacter_mixture_falsifier_certified"]:
            raise ArithmeticError("prespecified native full-moment falsifier not reproduced")
        controls.append({"source_seed": source["seed"], **result})
    return {"status": "NATIVE_FULL_MOMENT_FALSIFIER_AND_OBSERVABLE_REPAIR_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "source_report": str(BASE_REPORT.relative_to(ROOT)),
            "source_report_sha256": hashlib.sha256(BASE_REPORT.read_bytes()).hexdigest(),
            "native_controls": controls, "full_group_or_secret_enumeration_used": False,
            "general_sparse_Bochner_convex_hull_equality_falsified_on_retained_sources": True,
            "weighted_diagnostic_repaired_at_every_PSD_rank": True,
            "native_noisy_likelihood_tightness_or_decoder_proved": False,
            "quantum_speedup_proved": False, "candidate_record_accepted": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "native_controls": [{"seed": c["source_seed"],
                                           "original_PSD_rank": c["partition_witness"]["matrix_rank_exact"],
                                           "exact_gap": c["weighted_diagnostic"]["exact_integrality_gap"],
                                           "repaired_dimension": c["observable_refinement"]["matrix_dimension"]}
                                          for c in report["native_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
