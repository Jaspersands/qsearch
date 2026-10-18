"""Paid ENU channel splitting and cyclic computation-tree BPQM controls.

Known state-splitting mechanism. No arbitrary-state cloning or new algorithm.
Every root owns fresh ancillas; all disturbed split workspace is retained.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
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
from theorems.coherent_bpqm_tree import TreeCompilationLimit, root_program

REPORT = ROOT/"research/phase_workbench/coherent_bpqm_split.json"


def weakened_overlaps(overlap, copies, *, fractional_bits=16):
    """Near-equal rational overlaps with EXACT product equal to the input.

    An upper dyadic root is used for the first m-1 outputs; the final output
    receives the exact residual. No irrational root is silently rounded.
    """
    c = rational(overlap)
    if not 0 <= c < 1:
        raise ValueError("native overlap in [0,1) required")
    integer(copies, "number of weaker outputs", 1, 10)
    integer(fractional_bits, "dyadic root bits", 4, 64)
    if copies == 1 or c == 0:
        return (c,)*copies
    denominator = 1 << fractional_bits
    target = c.numerator*denominator**copies
    lo, hi = 0, denominator
    while lo < hi:
        middle = (lo+hi)//2
        if middle**copies*c.denominator >= target:
            hi = middle
        else:
            lo = middle+1
    a = Fraction(lo, denominator)
    result = (a,)*(copies-1)+(c/a**(copies-1),)
    if math.prod(result) != c or any(not c <= x <= 1 for x in result):
        raise ArithmeticError("state-splitting overlap conservation failed")
    return result


@lru_cache(maxsize=128)
def _splitter(a, b):
    compression = QuantumCircuit(2)
    compression.cx(1, 0)
    for bit in (0, 1):
        p0, p1 = ((1+a)*(1+b), (1-a)*(1-b)) if bit == 0 else ((1-a)*(1+b), (1+a)*(1-b))
        angle = 0 if p0+p1 == 0 else -2*math.atan2(math.sqrt(float(p1/(p0+p1))), math.sqrt(float(p0/(p0+p1))))
        compression.append(RYGate(angle).control(1, ctrl_state=bit), [0, 1])
    return transpile(compression.inverse(), basis_gates=["u", "cx"], optimization_level=0)


def splitter(a, b):
    a, b = rational(a), rational(b)
    if not 0 <= a <= 1 or not 0 <= b <= 1:
        raise ValueError("nonnegative child overlaps in [0,1] required")
    return _splitter(a, b).copy()


def unroll(problem, root, depth):
    integer(root, "native root", 0, problem.length-1)
    integer(depth, "finite unrolling check depth", 0, 3)
    rows = tuple(h for h in problem.checks if h)
    origins, checks = [], []

    def variable(v, parent, remaining):
        if len(origins) >= 10:
            raise TreeCompilationLimit("UNKNOWN: finite unrolled-channel compilation cap")
        occurrence = len(origins)
        origins.append(v)
        if remaining:
            for index, row in enumerate(rows):
                if index == parent or not (row >> v) & 1:
                    continue
                children = [j for j in range(problem.length) if j != v and (row >> j) & 1]
                if not children:
                    raise TreeCompilationLimit("UNKNOWN: unit-check primitive is not implemented")
                support = [occurrence, *[variable(j, index, remaining-1) for j in children]]
                checks.append(sum(1 << j for j in support))
        return occurrence

    variable(root, None, depth)
    return tuple(origins), tuple(checks)


@lru_cache(maxsize=128)
def _split_root(problem, c, root, depth):
    from theorems.coherent_local_gibbs import CodeProblem
    origins, checks = unroll(problem, root, depth)
    if not checks:
        # The all-variable code is allowed for a depth-zero root measurement.
        checks = (0,)
    tree = CodeProblem(len(origins), checks)
    multiplicities = Counter(origins)
    extra = len(origins)-len(multiplicities)
    circuit = QuantumCircuit(problem.length+extra)
    circuit.h(range(problem.length))
    physical, overlaps, allocations = {}, {}, []
    next_ancilla = problem.length
    for native in sorted(multiplicities):
        occurrences = [i for i, origin in enumerate(origins) if origin == native]
        values = weakened_overlaps(c, len(occurrences))
        remaining, remaining_overlap = native, c
        for i, occurrence in enumerate(occurrences):
            physical[occurrence], overlaps[occurrence] = remaining, values[i]
            if i+1 < len(occurrences):
                next_qubit = next_ancilla
                next_ancilla += 1
                tail = math.prod(values[i+1:])
                if values[i]*tail != remaining_overlap:
                    raise ArithmeticError("split chain does not preserve its incoming overlap")
                circuit.compose(splitter(values[i], tail), qubits=[remaining, next_qubit], inplace=True)
                remaining, remaining_overlap = next_qubit, tail
        allocations.append({"native_coordinate": native, "occurrences": occurrences,
                            "physical_qubits": [physical[i] for i in occurrences],
                            "weaker_overlaps": list(map(str, values)), "exact_product": str(math.prod(values))})
    message, tree_ledger = root_program(tree, c, 0, overlaps=tuple(overlaps[i] for i in range(len(origins))), fourier_input=True)
    circuit.compose(message, qubits=[physical[i] for i in range(len(origins))], inplace=True)
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    return compiled, {"root": root, "check_depth": depth, "native_code_length": problem.length,
                      "unrolled_variable_origins": list(origins), "unrolled_check_masks": list(checks),
                      "split_allocations": allocations, "additional_split_qubits": extra,
                      "unrolled_tree_program": tree_ledger,
                      "source_overlap_conserved_exactly": True,
                      "arbitrary_unknown_state_cloning_used": False,
                      "split_workspace_clean_after_root_measurement_assumed": False,
                      "weaker_split_outputs_are_fresh_native_samples": False,
                      "new_native_source_calls": 0,
                      "explicit_herald_angle_tables_can_be_exponential": True,
                      "unrolled_independence_is_not_the_native_joint_law": True}


def split_root(problem, c, root, *, depth=1):
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("finite native overlap required")
    integer(root, "native root", 0, problem.length-1)
    integer(depth, "finite unrolling depth", 0, 3)
    circuit, ledger = _split_root(problem, c, root, depth)
    return circuit.copy(), json.loads(json.dumps(ledger))


def split_decoder(problem, c, *, depth=1, reverse=False):
    """Each root receives its OWN initial-zero split workspace, never reset."""
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("finite native overlap required")
    integer(depth, "finite unrolling depth", 0, 3)
    if type(reverse) is not bool:
        raise ValueError("Boolean measurement order required")
    sequence = list(enumerate(problem.structure[1]))
    if reverse:
        sequence.reverse()
    roots = [(i, *split_root(problem, c, root, depth=depth)) for i, root in sequence]
    extra = sum(item[2]["additional_split_qubits"] for item in roots)
    m, k = problem.length, len(problem.structure[0])
    if m+2*k+extra > 20:
        raise TreeCompilationLimit("UNKNOWN: total retained-workspace statevector cap")
    decoder = QuantumCircuit(m+k+extra)
    offset, ledgers = 0, []
    for i, unitary, ledger in roots:
        size = ledger["additional_split_qubits"]
        mapping = [*range(m), *range(m+k+offset, m+k+offset+size)]
        decoder.compose(unitary, qubits=mapping, inplace=True)
        decoder.cx(ledger["root"], m+i)
        decoder.compose(unitary.inverse(), qubits=mapping, inplace=True)
        ledger["private_split_workspace_in_decoder"] = list(range(m+k+offset, m+k+offset+size))
        ledger["information_record_index"] = i
        offset += size
        ledgers.append(ledger)
    return decoder, {"additional_split_qubits": extra, "tree_root_programs": ledgers,
                     "each_root_has_private_unreset_split_workspace": True,
                     "split_check_depth": depth}


def run_controls():
    import numpy as np
    import qiskit
    from theorems.coherent_local_gibbs import CodeProblem, decoder_word_errors, finite_readout
    from theorems.xor_factor_reference import ExactXorReference
    problem = CodeProblem(4, (7, 13))
    rows = []
    classical = []
    for c in ("1/5", "13/20"):
        for signs in range(16):
            reference = ExactXorReference(problem.ising(signs), c)
            classical.append({"overlap_c_exact": c, "sign_mask_hex": hex(signs),
                              "exact_native_spin_probabilities": [str(reference.probability(x)) for x in range(4)],
                              "resource_ledger": reference.ledger()})
        for depth in (0, 1, 2):
            cases = [finite_readout(problem, c, signs, mode="split_tree_bpqm", tree_depth=depth)
                     for signs in range(16)]
            rows.append({"length": 4, "checks": [7, 13], "native_Tanner_graph_is_cyclic": True,
                         "overlap_c_exact": c, "check_depth": depth,
                         "word_recovery": decoder_word_errors(problem, c, mode="split_tree_bpqm", tree_depth=depth),
                         "all_sign_cases": cases, "all_signs_enumerated_no_favorable_selection": True,
                         "mean_unconditional_TV": float(np.mean([r["unconditional_TV_including_abort"] for r in cases])),
                         "maximum_unconditional_TV": max(r["unconditional_TV_including_abort"] for r in cases)})
    helpers = ("coherent_local_gibbs.py", "coherent_bpqm_tree.py", "bpqm_gibbs_frontier.py", "parity_block_usd_prange.py", "linear_erasure_prange_duality.py", "xor_factor_reference.py")
    return {"schema_version": "1.0", "subsystem": "coherent_bpqm_split", "results": rows,
            "classical_native_targets": classical,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in helpers},
            "qiskit_version": qiskit.__version__, "numpy_version": np.__version__,
            "prior_art_ENU_and_computation_trees": "https://arxiv.org/pdf/2109.08170",
            "native_sampling_family_classically_difficult": False,
            "classical_baseline": "exact integer-factor Gibbs sampler on the original native matrix",
            "accepted_speedup_candidate": False, "new_quantum_algorithm_claimed": False,
            "binary64_angles_are_not_certified_universal_gate_synthesis": True,
            "efficient_reliability_arithmetic_implemented": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{k: row[k] for k in ("overlap_c_exact", "check_depth", "mean_unconditional_TV", "maximum_unconditional_TV")}
                      for row in report["results"]], indent=2))


if __name__ == "__main__":
    main()
