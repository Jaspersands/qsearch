"""Actual binary tree BPQM gates with retained coherent parity heralds.

Known mechanism, bounded explicit-herald reference. Conditional tables may grow
exponentially; this is NOT the efficient approximate reliability-register scheme.
No copied channel outputs, measured internal heralds, or ideal decoder gates.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import RYGate

from theorems.bpqm_gibbs_frontier import integer, rational

REPORT = ROOT/"research/phase_workbench/coherent_bpqm_tree.json"


class TreeCompilationLimit(RuntimeError):
    pass


@dataclass(frozen=True)
class Message:
    qubit: int
    flags: tuple[int, ...]
    overlaps: tuple


@lru_cache(maxsize=128)
def _root_program(problem, c, root, depth, overlaps, fourier_input):
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("overlap in [0,1) required")
    integer(root, "root coordinate", 0, problem.length-1)
    if depth is not None:
        integer(depth, "actual check-neighborhood depth", 0, problem.length)
    if problem.length > 10:
        raise TreeCompilationLimit("UNKNOWN: explicit coherent-herald compilation cap")
    if float(c) == 1 or (c and float(c) == 0):
        raise TreeCompilationLimit("UNKNOWN: gate-angle precision cap")
    circuit = QuantumCircuit(problem.length)
    if not fourier_input:
        circuit.h(range(problem.length))
    rows = tuple(h for h in problem.checks if h)
    neighbors = {v: [i for i, h in enumerate(rows) if (h >> v) & 1] for v in range(problem.length)}
    visited_variables, visited_checks = set(), set()
    conditional_angles = 0
    max_controls = 0

    def parity(left, right):
        # (a,b)->(a xor b,b); the first message becomes a retained herald.
        circuit.cx(right.qubit, left.qubit)
        flags = (*left.flags, *right.flags, left.qubit)
        values = []
        for word in range(1 << len(flags)):
            a = left.overlaps[word & ((1 << len(left.flags))-1)]
            b = right.overlaps[(word >> len(left.flags)) & ((1 << len(right.flags))-1)]
            if (word >> (len(flags)-1)) & 1:
                denominator, numerator = 1-a*b, b-a
            else:
                denominator, numerator = 1+a*b, a+b
            values.append(numerator/denominator if denominator else rational(0))
        return Message(right.qubit, flags, tuple(values))

    def equality(left, right):
        nonlocal conditional_angles, max_controls
        flags = (*left.flags, *right.flags)
        circuit.cx(right.qubit, left.qubit)
        values = []
        for word in range(1 << len(flags)):
            a = left.overlaps[word & ((1 << len(left.flags))-1)]
            b = right.overlaps[word >> len(left.flags)]
            values.append(a*b)
            for bit in (0, 1):
                if bit == 0:
                    p0, p1 = (1+a)*(1+b), (1-a)*(1-b)
                else:
                    p0, p1 = (1-a)*(1+b), (1+a)*(1-b)
                angle = 0 if p0+p1 == 0 else -2*math.atan2(math.sqrt(float(p1/(p0+p1))), math.sqrt(float(p0/(p0+p1))))
                controls = [*flags, left.qubit]
                circuit.append(RYGate(angle).control(len(controls), ctrl_state=word | (bit << len(flags))),
                               [*controls, right.qubit])
                conditional_angles += 1
                max_controls = max(max_controls, len(controls))
        return Message(left.qubit, flags, tuple(values))

    def variable(v, parent, remaining):
        if v in visited_variables:
            raise TreeCompilationLimit("UNKNOWN: repeated physical channel in computation tree; no cloning")
        visited_variables.add(v)
        result = Message(v, (), (overlaps[v],))
        if remaining == 0:
            return result
        for check in neighbors[v]:
            if check == parent:
                continue
            if check in visited_checks:
                raise TreeCompilationLimit("UNKNOWN: cyclic check reuse is not a fresh tree")
            visited_checks.add(check)
            children = [j for j in range(problem.length) if j != v and (rows[check] >> j) & 1]
            if not children:
                raise TreeCompilationLimit("UNKNOWN: fixed-bit unit check needs a separate public primitive")
            messages = [variable(j, check, None if remaining is None else remaining-1) for j in children]
            combined = messages[0]
            for message in messages[1:]:
                combined = parity(combined, message)
            result = equality(result, combined)
        return result

    result = variable(root, None, depth)
    assert result.qubit == root
    circuit.h(root)
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    return compiled, {"root": root, "check_depth": depth,
                      "input_already_in_channel_Fourier_basis": fourier_input,
                      "physical_input_overlaps": list(map(str, overlaps)),
                      "distinct_original_channels_used": sorted(visited_variables),
                      "checks_used": [rows[i] for i in sorted(visited_checks)],
                      "retained_parity_herald_qubits": list(result.flags),
                      "signed_root_overlap_by_herald": [str(a) for a in result.overlaps],
                      "explicit_herald_table_entries": len(result.overlaps),
                      "conditional_Ry_angles_constructed": conditional_angles,
                      "maximum_rotation_controls": max_controls,
                      "internal_heralds_measured_or_reset": False,
                      "unknown_channel_output_cloning_used": False,
                      "explicit_herald_tables_can_be_exponential": True,
                      "efficient_approximate_reliability_register_implemented": False,
                      "full_BPQM_asymptotic_gate_bound_certified": False}


def root_program(problem, c, root, *, depth=None, overlaps=None, fourier_input=False):
    integer(root, "root coordinate", 0, problem.length-1)
    if depth is not None:
        integer(depth, "actual check-neighborhood depth", 0, problem.length)
    c = rational(c)
    if type(fourier_input) is not bool:
        raise ValueError("explicit Boolean channel-basis flag required")
    if overlaps is None:
        overlaps = (c,)*problem.length
    if type(overlaps) is not tuple or len(overlaps) != problem.length:
        raise ValueError("one immutable signed overlap per physical input required")
    overlaps = tuple(rational(a) for a in overlaps)
    if any(not -1 <= a <= 1 for a in overlaps):
        raise ValueError("signed channel overlaps must be in [-1,1]")
    circuit, ledger = _root_program(problem, c, root, depth, overlaps, fourier_input)
    # Cached circuits/ledgers are never exposed for caller mutation.
    return circuit.copy(), json.loads(json.dumps(ledger))


def run_controls():
    import numpy as np
    from theorems.coherent_local_gibbs import CodeProblem, decoder_word_errors, finite_readout
    problems = (CodeProblem(3, (7,)), CodeProblem(5, (7, 28)))
    results = []
    for problem in problems:
        for c in ("1/5", "13/20"):
            for depth in (0, 1, None):
                cases = [finite_readout(problem, c, signs, mode="tree_bpqm", tree_depth=depth)
                         for signs in range(1 << problem.length)]
                results.append({"length": problem.length, "checks": list(problem.checks),
                    "overlap_c_exact": c, "check_depth": depth,
                    "word_recovery": decoder_word_errors(problem, c, mode="tree_bpqm", tree_depth=depth),
                    "all_sign_cases": cases, "all_signs_enumerated_no_favorable_selection": True,
                    "mean_unconditional_TV": float(np.mean([r["unconditional_TV_including_abort"] for r in cases])),
                    "maximum_unconditional_TV": max(r["unconditional_TV_including_abort"] for r in cases)})
    helpers = ("coherent_local_gibbs.py", "bpqm_gibbs_frontier.py", "linear_erasure_prange_duality.py", "parity_block_usd_prange.py")
    return {"schema_version": "1.0", "subsystem": "coherent_bpqm_tree", "results": results,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in helpers},
            "prior_art": "https://arxiv.org/html/2609.05857v1",
            "new_quantum_algorithm_claimed": False, "accepted_speedup_candidate": False,
            "classical_hardness_proved": False, "random_regular_cyclic_ensemble_executed": False,
            "classical_tree_Gibbs_sampling_is_already_efficient": True,
            "explicit_herald_tables_can_be_exponential": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{k: row[k] for k in ("length", "overlap_c_exact", "check_depth", "mean_unconditional_TV", "maximum_unconditional_TV")}
                      for row in report["results"]], indent=2))


if __name__ == "__main__":
    main()
