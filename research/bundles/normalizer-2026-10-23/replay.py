"""Reproduce public algebra and bounded simulations; no scalable HSP claim."""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from abelian_action_normalizer import AbelianAction
from quotient_bridge_controls import (
    clean_compiler_error, in_place_householder_falsifier, reduction_control,
    span_rows,
)


def build_bridge_report():
    cases = []
    for conjugation in (0, 1, 3, 6):
        control = reduction_control(conjugation)
        probability_checks = []
        for stage in ("first", "second"):
            distribution = control[stage + "_probability"]
            probability_checks.append({
                "addresses_enumerated": int(distribution.size),
                "normalization": float(distribution.sum()),
                "positive_fourier_outcomes": int((distribution > 1e-12).sum()),
                "samples_drawn": len(control[stage + "_samples"]),
            })
        cases.append({
            "conjugation": conjugation,
            "learned_intersection": control["intersection"],
            "action_order": control["action_result"].action_order,
            "action_stabilizer_order": control["action_result"].stabilizer_order,
            "learned_terminal_subgroup": control["terminal"],
            "recovered_generators": control["answer"],
            "recovered_lie_rank": len(span_rows(control["answer"], 5, 7)),
            "fourier_stages": probability_checks,
        })
    delta = .01
    unitary = np.array([[np.sqrt(1-delta), -np.sqrt(delta)],
                        [np.sqrt(delta), np.sqrt(1-delta)]])
    fresh_error, failure = clean_compiler_error([unitary], [0])
    arbitrary_error, _ = clean_compiler_error([unitary], [0], arbitrary_target=True)
    false_compiler = in_place_householder_falsifier(2**40)
    return {
        "status": "BOUNDED_MECHANISM_CONTROLS_NOT_HARDNESS_EVIDENCE",
        "prime": 7,
        "ambient_class": 3,
        "ambient_order": 7**5,
        "numeric_labels_classically_easy": True,
        "enumeration_is_not_an_efficient_quantum_implementation": True,
        "cases": cases,
        "retained_input_compiler": {
            "workspace_failure_probability": failure,
            "fresh_target_squared_error": fresh_error**2,
            "arbitrary_target_squared_operator_error": arbitrary_error**2,
        },
        "in_place_counterexample": {
            "dimension": 2**40,
            "method": "symbolic_formula_not_dense_simulation",
            "basis_failure_probability_exact": str(false_compiler["basis_failure_probability"]),
            "uniform_input_trace_distance": false_compiler["uniform_input_trace_distance"],
            "balanced_witness_overlap_exact": str(false_compiler["balanced_witness_overlap"]),
            "balanced_witness_trace_distance": false_compiler["balanced_witness_trace_distance"],
        },
    }


def build_report():
    cases = []
    for p in (5, 2**127 - 1):
        action = AbelianAction(p, (2, 1))
        generators = (((1, p), (0, 1)), ((1, 0), (1, 1)))
        subgroup = ((0, 1),)
        result = action.stabilizer(generators, subgroup)
        assert result.action_order == p**3
        assert result.stabilizer_order == p**2
        assert all(action.preserves(g, subgroup) for g in result.stabilizer_group_generators)
        cases.append({"prime": p, "module_exponents": [2, 1],
                      "action_generators": generators, "supplied_subgroup": subgroup,
                      "result": asdict(result)})
    dimension, p = 8, 11
    action = AbelianAction(p, (1,) * dimension)
    g = tuple(tuple(int(i == j) + int(j == i+1) for j in range(dimension))
              for i in range(dimension))
    k = tuple(tuple(int(i == j) for i in range(dimension))
              for j in range(dimension-2))
    result = action.stabilizer((g,), k)
    assert result.action_order == result.stabilizer_order == p
    base = Path(__file__).resolve().parent
    names = ("abelian_action_normalizer.py", "test_abelian_action_normalizer.py",
             "ABELIAN_ACTION_NORMALIZER.md", "replay.py", "INTEGRATION.md",
             "quotient_bridge_controls.py", "test_quotient_bridge_controls.py",
             "QUOTIENT_BRIDGE_AUDIT.md")
    return {
        "status": "PUBLIC_ALGEBRA_AND_BOUNDED_FOURIER_CONTROLS",
        "independent_review": "pending",
        "quantum_device_execution": False,
        "scalable_quantum_receiver_executed": False,
        "black_box_preprocessing_executed": False,
        "hidden_intersections_learned_in_bounded_simulation_only": True,
        "general_all_prime_normalizer_implemented": False,
        "repository_integrated": False,
        "reason_not_integrated": "Desktop repository was actively being migrated",
        "cases": cases,
        "quotient_bridge": build_bridge_report(),
        "growing_class_control": {
            "ambient_semidirect_class": dimension,
            "prime": p,
            "abelian_module_dimension": dimension,
            "supplied_intersection_dimension": len(k),
            "action_stabilizer_order": result.stabilizer_order,
            "quotient_abelian_module_dimension": 2,
            "quotient_semidirect_order": p**3,
            "quotient_semidirect_class": 2,
        },
        "source_sha256": {name: sha256((base / name).read_bytes()).hexdigest()
                          for name in names},
        "unestablished": ["whole black-box reduction independently checked",
                          "all-prime normalizer interface independently audited",
                          "uniform FPT bound for all-prime terminal algorithm",
                          "novelty", "natural hard input family", "quantum speedup"],
    }


if __name__ == "__main__":
    report = build_report()
    target = Path(__file__).resolve().with_name("normalizer_receipt.json")
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="ascii")
    print(json.dumps({"status": report["status"], "receipt": str(target),
                      "cases": len(report["cases"]),
                      "growing_class_control": report["growing_class_control"]}, indent=2))
