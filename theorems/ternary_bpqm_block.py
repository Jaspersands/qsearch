"""Extrinsic ternary tree schedules, exact erasure maps, and coherent DAG lowering.

Instantiates a KNOWN two-stage decoder. Topology, F3 elimination, and the
uniform header-DAG quantum circuit compiler are implemented; full-statevector
gate replay is explicitly bounded. No quantum speedup is claimed.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from math import lcm, sqrt
from pathlib import Path
import sys

import numpy as np
from flint import nmod_mat
from qiskit import QuantumCircuit, QuantumRegister

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.ternary_coloring_bpqm import OMEGA, PHYSICAL, spectrum
from theorems.ternary_coherent_reliability import (
    Header, append_adder, combine, compression_reference, message_program, natural, precision_budget,
)
from theorems.ternary_cordic_step import sparse_gate_program, variable_rotation
from theorems.ternary_decoded_sampler import (
    index, local_gate, matrix_data, native_distribution, prepare_source, sources, subtract_label,
)

REPORT = ROOT / "research/phase_workbench/ternary_bpqm_block.json"
SOURCE = ROOT / "research/phase_workbench/ternary_bpqm_certificate.json"


def canonical_matrix(rows):
    rows = tuple(tuple(row) for row in rows)
    if (not rows or not rows[0] or any(len(row) != len(rows[0]) or
            any(type(x) is not int or x not in (0, 1, 2) for x in row) for row in rows)):
        raise ValueError("canonical nonempty rectangular F3 matrix required")
    return rows


@dataclass(frozen=True)
class SocketGraph:
    H: tuple
    sockets: tuple  # (variable, check, nonzero coefficient), in original order

    def __post_init__(self):
        H = canonical_matrix(self.H)
        sockets = tuple(tuple(edge) for edge in self.sockets)
        recovered = [[0]*len(H[0]) for _ in H]
        for edge in sockets:
            if (len(edge) != 3 or any(type(x) is not int for x in edge) or
                    not 0 <= edge[0] < len(H[0]) or not 0 <= edge[1] < len(H) or edge[2] not in (1, 2)):
                raise ValueError("raw canonical (variable, check, nonzero coefficient) sockets required")
            v, c, a = edge
            recovered[c][v] = (recovered[c][v]+a) % 3
        if tuple(map(tuple, recovered)) != H:
            raise ValueError("raw socket sum does not equal unchanged public H")
        object.__setattr__(self, "H", H)
        object.__setattr__(self, "sockets", sockets)

    @classmethod
    def simple(cls, rows):
        H = canonical_matrix(rows)
        return cls(H, tuple((v, c, a) for c, row in enumerate(H) for v, a in enumerate(row) if a))

    @property
    def length(self):
        return len(self.H[0])

    def adjacency(self):
        variables, checks = [[] for _ in range(self.length)], [[] for _ in self.H]
        for e, (v, c, _) in enumerate(self.sockets):
            variables[v].append(e)
            checks[c].append(e)
        return variables, checks


def tree_partition(graph, depth, *, outgoing=None):
    """One fixed outgoing socket per root, excluded only at that root.

    Selection is topology-only, before reading coefficients or channel data.
    A collision is an actual repeated physical variable/check, not a cost cap.
    """
    natural(depth, "check depth")
    variables, checks = graph.adjacency()
    if outgoing is None:
        outgoing = tuple(edges[0] if edges else None for edges in variables)
    outgoing = tuple(outgoing)
    if len(outgoing) != graph.length or any(
            (e is not None and (type(e) is not int or e not in variables[v])) or
            (e is None and variables[v]) for v, e in enumerate(outgoing)):
        raise ValueError("one fixed incident outgoing socket per nonisolated root required")
    good, bad, trees = [], [], []
    for root in range(graph.length):
        seen_v, seen_c = set(), set()

        def visit(v, excluded_edge, remaining):
            if v in seen_v:
                raise ArithmeticError("repeated_physical_variable_or_parallel_socket")
            seen_v.add(v)
            node = {"variable": v, "checks": []}
            if remaining == 0:
                return node
            for e in variables[v]:
                if e == excluded_edge:
                    continue
                _, c, a = graph.sockets[e]
                if c in seen_c:
                    raise ArithmeticError("repeated_check_or_parallel_socket")
                seen_c.add(c)
                children = []
                for f in checks[c]:
                    if f == e:
                        continue
                    u, _, b = graph.sockets[f]
                    children.append({"edge": f, "symbol_factor": (-a*b) % 3,
                                     "tree": visit(u, f, remaining-1)})
                node["checks"].append({"check": c, "parent_edge": e, "children": children})
            return node

        try:
            tree = visit(root, outgoing[root], depth)
        except ArithmeticError as error:
            bad.append({"root": root, "reason": str(error)})
        else:
            good.append(root)
            trees.append({"root": root, "depth": depth, "outgoing_edge": outgoing[root],
                          "variables": sorted(seen_v), "checks": sorted(seen_c), "tree": tree})
    return {"depth": depth, "outgoing_edges": outgoing, "good": good, "bad": bad,
            "trees": trees, "root_policy": "fixed_outgoing_socket_extrinsic",
            "raw_parallel_sockets_preserved": True,
            "compilation_failure_reclassified_as_bad_topology": False}


def erasure_recovery(rows, good):
    """Exact F3 left inverse or explicit kernel witness, without d_min advice.

    On arbitrary (possibly inconsistent) outcomes, the returned linear map is
    TOTAL. Correctness is asserted only on restrictions of actual codewords.
    """
    H = canonical_matrix(rows)
    good = tuple(good)
    m = len(H[0])
    if len(set(good)) != len(good) or any(type(v) is not int or not 0 <= v < m for v in good):
        raise ValueError("distinct canonical good coordinates required")
    bad = tuple(v for v in range(m) if v not in good)
    HB = [[row[v] for v in bad] for row in H]
    rank = nmod_mat(HB, 3).rank() if bad else 0
    result = {"good": good, "erased": bad, "erased_column_rank": rank,
              "minimum_distance_oracle_used": False, "postselection_on_consistency": False}
    if rank < len(bad):
        R, _ = nmod_mat(HB, 3).rref()
        pivots = [next(j for j in range(len(bad)) if R[i, j]) for i in range(rank)]
        f = next(j for j in range(len(bad)) if j not in pivots)
        witness = [0]*m
        witness[bad[f]] = 1
        for i, pivot in enumerate(pivots):
            witness[bad[pivot]] = -int(R[i, f]) % 3
        if not any(witness) or any(sum(a*b for a, b in zip(row, witness)) % 3 for row in H):
            raise ArithmeticError("erasure nonuniqueness witness is invalid")
        return dict(result, status="ERASURE_NOT_UNIQUELY_RECOVERABLE", kernel_codeword=witness)
    # RREF on [H_B|I] has its first |B| pivots in H_B. Retain those row operations.
    augmented = [row+[int(i == j) for j in range(len(H))] for i, row in enumerate(HB)]
    R, _ = nmod_mat(augmented, 3).rref()
    L = [[int(R[i, len(bad)+j]) for j in range(len(H))] for i in range(len(bad))]
    M = [[0]*len(good) for _ in range(m)]
    for j, v in enumerate(good):
        M[v][j] = 1
    for i, v in enumerate(bad):
        M[v] = [-sum(L[i][c]*H[c][g] for c in range(len(H))) % 3 for g in good]
    if any(sum(L[i][c]*HB[c][j] for c in range(len(H))) % 3 != int(i == j)
           for i in range(len(bad)) for j in range(len(bad))):
        raise ArithmeticError("claimed left inverse does not multiply to identity")
    return dict(result, status="EXACT_PUBLIC_LEFT_INVERSE", left_inverse=L, codeword_from_good=M,
                arbitrary_wrong_good_records_need_not_produce_a_codeword=True)


def root_schedule(graph, tree):
    """Uniform header DAG and physical-wire schedule, without branch tables.

    Every check herald becomes immutable. Persistent headers depend ONLY on
    these heralds, so their classical arithmetic can be reversed at the end
    without reversing the physical gates. Fiber headers are temporary and
    must be uncomputed before the surviving frequency is changed.
    """
    variables, checks = graph.adjacency()
    nodes, active, heralds, garbage, seen, seen_checks = [], set(), set(), set(), set(), set()

    def add(kind, wire, inputs=(), **fields):
        controls = set().union(*(set(nodes[j]["controls"]) for j in inputs))
        leaves = sum(nodes[j]["leaf_count"] for j in inputs) if inputs else 1
        if kind == "check":
            controls.add(nodes[inputs[0]]["wire"])
        record = {"kind": kind, "wire": wire, "inputs": inputs, "controls": sorted(controls),
                  "leaf_count": leaves, **fields}
        nodes.append(record)
        return len(nodes)-1

    def merge(kind, left, right):
        a, b = nodes[left]["wire"], nodes[right]["wire"]
        if a == b or a not in active or b not in active:
            raise ValueError("physical message reuse would clone or overwrite a retired wire")
        active.remove(a if kind == "check" else b)
        (heralds if kind == "check" else garbage).add(a if kind == "check" else b)
        return add(kind, b if kind == "check" else a, (left, right))

    def visit(node, excluded, remaining):
        v = node["variable"]
        if type(v) is not int or not 0 <= v < graph.length or v in seen:
            raise ValueError("tree schedule repeats or invents a physical variable")
        seen.add(v)
        active.add(v)
        result = add("leaf", v)
        expected = [e for e in variables[v] if e != excluded] if remaining else []
        if [c["parent_edge"] for c in node["checks"]] != expected:
            raise ValueError("tree does not implement the fixed extrinsic depth policy")
        for c in node["checks"]:
            edge = c["parent_edge"]
            _, check_index, a = graph.sockets[edge]
            if check_index != c["check"] or check_index in seen_checks:
                raise ValueError("tree repeats or changes an original check")
            seen_checks.add(check_index)
            children = [f for f in checks[check_index] if f != edge]
            if [child["edge"] for child in c["children"]] != children:
                raise ValueError("tree drops or changes an original raw check socket")
            if not children:
                raise ValueError("UNKNOWN: unit parity check is not a topology failure; separate primitive required")
            incoming = []
            for child in c["children"]:
                u, _, b = graph.sockets[child["edge"]]
                factor = (-a*b) % 3
                if child["tree"]["variable"] != u or child["symbol_factor"] != factor:
                    raise ValueError("tree changed a public coefficient or endpoint")
                msg = visit(child["tree"], child["edge"], remaining-1)
                if factor == 2:
                    msg = add("permute", nodes[msg]["wire"], (msg,), factor=factor)
                incoming.append(msg)
            message = incoming[0]
            for other in incoming[1:]:
                message = merge("check", message, other)
            result = merge("bit", result, message)
        return result

    root, outgoing, depth = tree["root"], tree["outgoing_edge"], tree["depth"]
    natural(depth, "tree depth")
    if (type(root) is not int or not 0 <= root < graph.length or
            (outgoing not in variables[root] if variables[root] else outgoing is not None)):
        raise ValueError("tree root or outgoing edge is invalid")
    output = visit(tree["tree"], outgoing, depth)
    if (tree["tree"]["variable"] != root or seen != set(tree["variables"]) or
            seen_checks != set(tree["checks"]) or active != {root}):
        raise ValueError("tree summary or final active wire is inconsistent")
    if any(set(node["controls"])-heralds or node["wire"] in node["controls"] for node in nodes):
        raise ArithmeticError("header depends on a mutable physical wire")
    return {"root": root, "nodes": nodes, "output_header": output,
            "immutable_herald_wires": sorted(heralds), "retained_compression_garbage": sorted(garbage),
            "distinct_physical_leaves": len(seen),
            "signed_trine_persistent_header_bits_sufficient": 3*sum(node["leaf_count"]+1 for node in nodes),
            "cleanup_order_header_ids": list(reversed(range(len(nodes)))),
            "persistent_header_cleanup_needs_no_physical_gate_reversal": True,
            "temporary_fiber_header_uncomputed_before_frequency_changes_required": True,
            "uniform_arithmetic_header_dag_lowered": True,
            "uniform_arithmetic_schedule_not_yet_lowered_to_whole_receiver": False}


def regular_tree_size(depth, dv=3, dc=6):
    natural(depth, "tree depth")
    natural(dv, "variable degree", 2)
    natural(dc, "check degree", dv+1)
    alpha = (dv-1)*(dc-1)
    internal = (alpha**depth-1)//(alpha-1)
    checks = (dv-1)*internal
    return {"depth": depth, "physical_leaves": 1+alpha*internal,
            "check_vertices": checks, "binary_check_gates": (dc-2)*checks,
            "bit_compressions": checks,
            "sampler_compressions_per_decoded_root_including_ALL_adjoints": 4*checks}


def sufficient_depth_contract(length):
    """An integer-only asymptotic schedule, NOT a finite block accuracy claim.

    Conditional on the source certificate, F_l <= 3*f/N^6. The unknown
    erasure-rank failure probability remains in the ensemble TV bound.
    """
    natural(length, "original block length", 2)
    if length % 2:
        raise ValueError("(3,6) ensemble requires an even block length")
    result = json.loads(SOURCE.read_text())["result"]
    certificate = result["certificate"]
    f = Fraction(certificate["f_upper_exact"])
    rate = Fraction(certificate["lambda_upper_exact"])
    if (result["variable_degree"] != 3 or result["check_degree"] != 6 or
            tuple(map(Fraction, result["source_normalized_spectrum"])) != PHYSICAL or
            certificate["level"] != 13 or not certificate["certified"] or
            not 0 < f < 1 or not 0 < rate < Fraction(1, 3)):
        raise ValueError("signed-trine level13 certificate with lambda<1/3 required")
    t = 0
    while pow(3, 1 << t) < length**6:
        t += 1
    resources = regular_tree_size(13+t)
    E = length*resources["sampler_compressions_per_decoded_root_including_ALL_adjoints"]
    budget = precision_budget(E, Fraction(1, length), source_error=Fraction(1, 3*length),
                              gate_synthesis_error=Fraction(1, 3*length))
    return {"original_block_length": str(length), "extra_levels": t, "resources": resources,
            "fidelity_upper_conditional_on_review_pending_certificate": str(3*f/length**6),
            "squared_sampling_TV_term_excluding_rank_failure_and_gate_errors": str(192*f/length**5),
            "ensemble_mean_TV_bound": "P[rank(H_B)<|B|] + sqrt(192*f/N^5) + 1/N",
            "finite_N_rank_failure_probability_certified": False,
            "topology_size_status": "NO_GOOD_ROOT_POSSIBLE_AT_THIS_SUFFICIENT_DEPTH"
                if resources["physical_leaves"] > length else "SIZE_NOT_EXCLUDED_NOT_ACCURACY_CERTIFIED",
            "whole_sampler_precision_contract": budget,
            "resource_counts_are_not_circuits_allocated_or_executed": True}


@dataclass(frozen=True)
class Message:
    wire: int
    controls: tuple
    expression: tuple

    def header(self, values):
        kind, *args = self.expression
        if kind == "leaf":
            return args[0]
        if kind == "permute":
            source, factor = args
            h = source.header(values)
            return Header(tuple(h.weights[factor*j % 3] for j in range(3)), h.capacity)
        left, right = args[:2]
        selector = values[args[2]] if kind == "check" else 0
        return combine(left.header(values), right.header(values), kind, selector)


def givens_compression(weights, steps=None):
    """Two rotations with a TOTAL identity completion for the zero vector."""
    if steps is not None:
        return compression_reference(weights, steps)[0]
    w0, w1, w2 = weights
    result = np.eye(3)
    for a, b, pair in ((w0, w1, (0, 1)), (w0+w1, w2, (0, 2))):
        if a+b:
            c, s = sqrt(Fraction(a, a+b)), sqrt(Fraction(b, a+b))
            gate = np.eye(3)
            i, j = pair
            gate[i, i] = gate[j, j] = c
            gate[i, j], gate[j, i] = s, -s
            result = gate @ result
    return result


def root_transform(graph, tree, mu=PHYSICAL, *, steps=None):
    """Bounded local-gate reference, NOT a hidden global PGM matrix.

    Conditional header histories are enumerated here and explicitly charged.
    The arithmetic compiler is assembled separately by compile_root_program.
    """
    mu = spectrum(mu)
    if graph.length > 6 or tree["root"] not in tree["variables"]:
        raise ValueError("UNKNOWN: bounded dense root replay requires <=6 physical qutrits")
    if steps is not None:
        natural(steps, "CORDIC steps", 1)
    schedule = root_schedule(graph, tree)
    denominator = lcm(*(p.denominator for p in mu))
    leaf = Header(tuple(int(p*denominator) for p in mu), denominator)
    m, D = graph.length, 3**graph.length
    tensor = np.eye(D, dtype=complex).reshape((3,)*m+(D,))
    ledger = {"check_nodes": 0, "bit_compressions": 0, "conditional_bit_blocks_enumerated": 0,
              "dark_fiber_blocks_completed_by_identity": 0}
    negation = np.eye(3)[[0, 2, 1]]
    check = np.zeros((9, 9))
    add = np.zeros((9, 9))
    for i, j in product(range(3), repeat=2):
        check[3*((i-j) % 3)+j, 3*i+j] = 1
        add[3*((i+j) % 3)+j, 3*i+j] = 1

    def bit(left, right):
        nonlocal tensor
        controls = tuple(sorted(set(left.controls+right.controls)))
        if set(controls) & {left.wire, right.wire}:
            raise ArithmeticError("active message reused as its own classical control")
        size = 3**len(controls)*9
        gate = np.zeros((size, size), complex)
        for values in product(range(3), repeat=len(controls)):
            assignment = dict(zip(controls, values))
            a, b = left.header(assignment), right.header(assignment)
            block = np.zeros((9, 9))
            for t in range(3):
                weights = combine(a, b, "fiber", t).weights
                block[3*t:3*t+3, 3*t:3*t+3] = givens_compression(weights, steps)
                ledger["dark_fiber_blocks_completed_by_identity"] += not any(weights)
            start = 9*index(values)
            gate[start:start+9, start:start+9] = block @ add
            ledger["conditional_bit_blocks_enumerated"] += 1
        tensor = local_gate(tensor, gate, (*controls, left.wire, right.wire))
        ledger["bit_compressions"] += 1
        return Message(left.wire, controls, ("bit", left, right))

    messages = []
    for node in schedule["nodes"]:
        kind = node["kind"]
        inputs = [messages[i] for i in node["inputs"]]
        if kind == "leaf":
            message = Message(node["wire"], (), ("leaf", leaf))
        elif kind == "permute":
            message = inputs[0]
            tensor = local_gate(tensor, negation, (message.wire,))
            message = Message(message.wire, message.controls, ("permute", message, node["factor"]))
        elif kind == "check":
            left, right = inputs
            tensor = local_gate(tensor, check, (left.wire, right.wire))
            message = Message(right.wire, tuple(node["controls"]), ("check", left, right, left.wire))
            ledger["check_nodes"] += 1
        else:
            message = bit(*inputs)
        messages.append(message)
    message = messages[schedule["output_header"]]
    Fourier = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)])/sqrt(3)
    T = local_gate(tensor, Fourier.conj().T, (message.wire,)).reshape(D, D)
    residual = float(np.max(abs(T.conj().T @ T-np.eye(D))))
    if residual > 1e-10:
        raise ArithmeticError("full-domain root unitary check failed")
    ledger.update({"root": tree["root"], "physical_variables": tree["variables"],
                   "CORDIC_steps": steps, "full_domain_unitarity_residual": residual,
                   "upstream_herald_tables_exponential_reference_only": True,
                   "coherent_header_arithmetic_assembled_here": False,
                   "herald_dephasing_or_original_output_cloning": False,
                   "uniform_header_schedule": schedule})
    return T, ledger


def emit_qutrit_negation(circuit, q):
    """Two-qubit qutrit negation: 0->0, 1->2, 2->1, and unused 3 (|11>)->3."""
    circuit.cx(q[0], q[1])
    circuit.cx(q[1], q[0])
    circuit.cx(q[0], q[1])


def emit_qutrit_shift(circuit, target_q, sign, controls=()):
    """Cyclic F3 shift on {0,1,2} fixing unused 3 (|11>), controlled by controls."""
    if sign not in (1, -1):
        raise ValueError("F3 shift sign must be +1 or -1")
    controls = tuple(controls)

    def swap_01():
        circuit.x(target_q[1])
        circuit.mcx([*controls, target_q[1]], target_q[0])
        circuit.x(target_q[1])

    def swap_12():
        circuit.mcx([*controls, target_q[0]], target_q[1])
        circuit.mcx([*controls, target_q[1]], target_q[0])
        circuit.mcx([*controls, target_q[0]], target_q[1])

    if sign == 1:
        swap_12()
        swap_01()
    else:
        swap_01()
        swap_12()


def emit_qutrit_add_or_check(circuit, left_q, right_q, kind):
    """Total 4-qubit permutation for (i,j)->((i+j)%3,j) or ((i-j)%3,j) on {0,1,2}^2.

    Any basis state with i=3 or j=3 (unused |11> encoding) is fixed identically.
    """
    if kind not in ("add", "check"):
        raise ValueError("add or check qutrit permutation required")
    s1 = 1 if kind == "add" else -1
    circuit.x(right_q[1])
    emit_qutrit_shift(circuit, left_q, s1, controls=(right_q[0], right_q[1]))
    circuit.x(right_q[1])
    circuit.x(right_q[0])
    emit_qutrit_shift(circuit, left_q, -s1, controls=(right_q[0], right_q[1]))
    circuit.x(right_q[0])


def group_sparse_operations(operations):
    """Group contiguous X/CX/CCX/MCX permutation runs without altering gate semantics."""
    blocks, perm = [], []
    for mask, state, target, angle in operations:
        if angle is None:
            perm.append((mask, state, 1 << target))
        else:
            if perm:
                blocks.append((True, tuple(perm)))
                perm = []
            blocks.append((False, (mask, state, target, angle)))
    if perm:
        blocks.append((True, tuple(perm)))
    return tuple(blocks)


def apply_grouped_gates(blocks, amplitudes, *, inverse=False):
    """Execute every compiled gate on sparse basis words without herald tables."""
    amplitudes = dict(amplitudes)
    for is_perm, data in (reversed(blocks) if inverse else blocks):
        if is_perm:
            result = {}
            ops = tuple(reversed(data)) if inverse else data
            for word, amp in amplitudes.items():
                w = word
                for mask, state, bit in ops:
                    if (w & mask) == state:
                        w ^= bit
                if w in result:
                    raise ArithmeticError("noninjective supposedly reversible gate block")
                result[w] = amp
            amplitudes = result
        else:
            mask, state, target, angle = data
            angle = -angle if inverse else angle
            c, s = math.cos(angle / 2), math.sin(angle / 2)
            bit = 1 << target
            result = {}
            for word, amp in amplitudes.items():
                if (word & mask) != state:
                    result[word] = result.get(word, 0) + amp
                else:
                    flipped = word ^ bit
                    result[word] = result.get(word, 0) + c * amp
                    result[flipped] = result.get(flipped, 0) + (-s if (word & bit) else s) * amp
            amplitudes = result
    return amplitudes


@dataclass
class RootProgram:
    circuit: QuantumCircuit
    operations: tuple
    grouped_operations: tuple
    graph_length: int
    root: int
    steps: int
    mu: tuple
    schedule: dict
    data_wires: tuple
    work_wires: tuple
    ledger: dict

    def encode_data(self, word):
        word = tuple(word)
        if len(word) != self.graph_length or any(type(d) is not int or not 0 <= d <= 3 for d in word):
            raise ValueError("one two-qubit qutrit value in 0..3 per physical wire required")
        state = 0
        for v, d in enumerate(word):
            state |= (d & 1) << self.data_wires[v][0]
            state |= ((d >> 1) & 1) << self.data_wires[v][1]
        return state


def compile_root_program(graph, tree, mu=PHYSICAL, *, steps=5, max_gates=5_000_000):
    """Lower root_schedule into an actual uniform arithmetic quantum circuit.

    No herald histories are enumerated and no classical CORDIC digits are
    injected as advice. Check heralds remain immutable; temporary fiber
    headers and w0+w1 sums are uncomputed before t can change; persistent
    headers are reversed in reverse DAG order at the end without undoing
    physical qutrit gates. Unused |11> encodings receive total unitary
    completions throughout.
    """
    mu = spectrum(mu)
    natural(steps, "CORDIC steps", 1)
    natural(max_gates, "explicit reference gate cap", 1)
    schedule = root_schedule(graph, tree)
    if tree["root"] not in tree["variables"]:
        raise ValueError("tree root must belong to tree variables")
    denominator = lcm(*(p.denominator for p in mu))
    leaf_header = Header(tuple(int(p * denominator) for p in mu), denominator)
    leaf_w = leaf_header.width

    circuit = QuantumCircuit()

    def reg(size, name):
        if size == 0:
            return ()
        r = QuantumRegister(size, name)
        circuit.add_register(r)
        return tuple(r)

    data_wires = tuple(reg(2, f"q{v}") for v in range(graph.length))
    data_qubits = circuit.num_qubits

    nodes = schedule["nodes"]
    active_widths, out_widths, in_widths = [], [], []
    max_msg_w = 1
    max_fiber_cap_w = 1
    for node in nodes:
        kind = node["kind"]
        cap = denominator ** node["leaf_count"]
        cap_w = cap.bit_length()
        if kind == "leaf":
            in_widths.append(0)
            out_widths.append(leaf_w)
            active_widths.append(leaf_w)
        elif kind == "permute":
            child = node["inputs"][0]
            in_widths.append(active_widths[child])
            out_widths.append(0)
            active_widths.append(active_widths[child])
        else:
            l_id, r_id = node["inputs"]
            w_in = max(active_widths[l_id], active_widths[r_id])
            w_out = 2 * w_in + 2
            in_widths.append(w_in)
            out_widths.append(w_out)
            active_widths.append(min(w_out, cap_w))
            max_msg_w = max(max_msg_w, w_in)
            if kind == "bit":
                max_fiber_cap_w = max(max_fiber_cap_w, min(w_out, cap_w))

    header_alloc, header_active = [], []
    for i, node in enumerate(nodes):
        kind = node["kind"]
        if kind == "permute":
            child = node["inputs"][0]
            w0, w1, w2 = header_active[child]
            header_alloc.append(())
            header_active.append((w0, w2, w1) if node["factor"] == 2 else (w0, w1, w2))
        else:
            w_out, w_act = out_widths[i], active_widths[i]
            raw = reg(3 * w_out, f"h{i}")
            triples_full = tuple(raw[j * w_out:(j + 1) * w_out] for j in range(3))
            triples_act = tuple(t[:w_act] for t in triples_full)
            header_alloc.append(triples_full)
            header_active.append(triples_act)

    zero_pad = reg(3 * max_msg_w + 2, "zpad")
    msg_scratch = reg(2 * max_msg_w + 3, "mscratch")

    has_bit = any(n["kind"] == "bit" for n in nodes)
    if has_bit:
        max_fiber_out_w = 2 * max_msg_w + 2
        fiber_reg = reg(3 * max_fiber_out_w, "fiber")
        # Since w0 + w1 + w2 <= capacity < 2**cap_w, w0 + w1 fits in max_fiber_cap_w bits.
        sum01_reg = reg(max_fiber_cap_w + 1, "sum01")
        vrot01_max = variable_rotation(max_fiber_cap_w, steps, (0, 1), max_gates=max_gates)
        rot_work = reg(len(vrot01_max.work), "rotwork")
    else:
        fiber_reg = sum01_reg = rot_work = ()

    def pad_triple(triple_wires, target_w):
        res, offset = [], 0
        for w_wires in triple_wires:
            need = target_w - len(w_wires)
            res.extend(w_wires)
            if need > 0:
                res.extend(zero_pad[offset:offset + need])
                offset += need
        return tuple(res)

    def append_mapped(subcircuit, mapping):
        for inst in subcircuit.data:
            circuit.append(inst.operation, [mapping[subcircuit.find_bit(q).index] for q in inst.qubits])

    def build_msg_mapping(prog, left_triple, right_triple, selector_wires, out_triple):
        mapping = [None] * prog.circuit.num_qubits
        l_pad = pad_triple(left_triple, prog.width)
        r_pad = pad_triple(right_triple, prog.width)
        out_flat = tuple(q for grp in out_triple for q in grp)
        for old, new in ((prog.left, l_pad), (prog.right, r_pad),
                         (prog.selector, selector_wires), (prog.output, out_flat),
                         (prog.scratch, msg_scratch[:len(prog.scratch)])):
            for idx, wire in zip(old, new):
                mapping[idx] = wire
        return mapping

    persistent_actions = []
    check_nodes = bit_compressions = 0
    for i, node in enumerate(nodes):
        kind = node["kind"]
        if kind == "leaf":
            for j, val in enumerate(leaf_header.weights):
                for b in range(leaf_w):
                    if (val >> b) & 1:
                        circuit.x(header_alloc[i][j][b])
            persistent_actions.append(("leaf", i, None, None))
        elif kind == "permute":
            emit_qutrit_negation(circuit, data_wires[node["wire"]])
            persistent_actions.append(("permute", i, None, None))
        elif kind == "check":
            l_id, r_id = node["inputs"]
            l_wire, r_wire = nodes[l_id]["wire"], nodes[r_id]["wire"]
            emit_qutrit_add_or_check(circuit, data_wires[l_wire], data_wires[r_wire], "check")
            prog = message_program(in_widths[i], "check")
            mapping = build_msg_mapping(prog, header_active[l_id], header_active[r_id],
                                        data_wires[l_wire], header_alloc[i])
            append_mapped(prog.circuit, mapping)
            persistent_actions.append(("check", i, prog, mapping))
            check_nodes += 1
        elif kind == "bit":
            l_id, r_id = node["inputs"]
            l_wire, r_wire = nodes[l_id]["wire"], nodes[r_id]["wire"]
            w_in = in_widths[i]
            prog_bit = message_program(w_in, "bit")
            map_bit = build_msg_mapping(prog_bit, header_active[l_id], header_active[r_id],
                                        zero_pad[-2:], header_alloc[i])
            append_mapped(prog_bit.circuit, map_bit)
            persistent_actions.append(("bit", i, prog_bit, map_bit))
            emit_qutrit_add_or_check(circuit, data_wires[l_wire], data_wires[r_wire], "add")
            prog_fib = message_program(w_in, "fiber")
            w_out = prog_fib.output_width
            fib_triples = tuple(fiber_reg[j * w_out:(j + 1) * w_out] for j in range(3))
            map_fib = build_msg_mapping(prog_fib, header_active[l_id], header_active[r_id],
                                        data_wires[l_wire], fib_triples)
            append_mapped(prog_fib.circuit, map_fib)
            w_f = active_widths[i]
            w0_w, w1_w, w2_w = (t[:w_f] for t in fib_triples)
            adder_qc = QuantumCircuit(*circuit.qregs)
            for src, dst in zip(w0_w, sum01_reg[:w_f]):
                adder_qc.cx(src, dst)
            append_adder(adder_qc, w1_w, sum01_reg[:w_f], msg_scratch[0], carry=sum01_reg[w_f])
            for inst in adder_qc.data:
                circuit.append(inst.operation, inst.qubits)
            vrot01 = variable_rotation(w_f, steps, (0, 1), max_gates=max_gates)
            vrot02 = variable_rotation(w_f, steps, (0, 2), max_gates=max_gates)
            for vrot, a_w, b_w in ((vrot01, w0_w, w1_w),
                                   (vrot02, sum01_reg[:w_f], w2_w)):
                vmap = [None] * vrot.circuit.num_qubits
                for old, new in ((vrot.a, a_w), (vrot.b, b_w),
                                 (vrot.data, data_wires[r_wire]), (vrot.work, rot_work[:len(vrot.work)])):
                    for idx, wire in zip(old, new):
                        vmap[idx] = wire
                append_mapped(vrot.circuit, vmap)
            for inst in reversed(adder_qc.data):
                circuit.append(inst.operation, inst.qubits)
            for inst in reversed(prog_fib.circuit.data):
                circuit.append(inst.operation, [map_fib[prog_fib.circuit.find_bit(q).index] for q in inst.qubits])
            bit_compressions += 1

    for node_id in schedule["cleanup_order_header_ids"]:
        kind, idx, prog, mapping = persistent_actions[node_id]
        if kind == "leaf":
            for j, val in enumerate(leaf_header.weights):
                for b in range(leaf_w):
                    if (val >> b) & 1:
                        circuit.x(header_alloc[idx][j][b])
        elif kind in ("check", "bit"):
            for inst in reversed(prog.circuit.data):
                circuit.append(inst.operation, [mapping[prog.circuit.find_bit(q).index] for q in inst.qubits])

    if len(circuit.data) > max_gates:
        raise ValueError(f"UNKNOWN: explicit reference cap; {len(circuit.data)} logical gates required")
    operations = sparse_gate_program(circuit)
    grouped = group_sparse_operations(operations)
    data_indices = tuple(
        tuple(circuit.find_bit(q).index for q in wires) for wires in data_wires
    )
    work_indices = tuple(range(data_qubits, circuit.num_qubits))
    ledger = {
        "root": schedule["root"],
        "physical_variables": tree["variables"],
        "CORDIC_steps": steps,
        "check_nodes": check_nodes,
        "bit_compressions": bit_compressions,
        "actual_qubits_including_data_headers_and_work": circuit.num_qubits,
        "data_qubits": data_qubits,
        "work_and_header_qubits": len(work_indices),
        "actual_logical_gates_before_root_Fourier": len(operations),
        "actual_maximum_controls": max((mask.bit_count() for mask, _, _, _ in operations), default=0),
        "active_header_widths_by_node": active_widths,
        "allocated_header_widths_by_node": out_widths,
        "upstream_herald_history_enumeration_used": False,
        "classical_CORDIC_digits_injected_as_advice": False,
        "temporary_fibers_uncomputed_before_frequency_change": True,
        "persistent_headers_cleaned_in_reverse_DAG_order": True,
        "unused_11_encoding_total_unitary_completion": True,
        "coherent_header_arithmetic_assembled_here": True,
        "herald_dephasing_or_original_output_cloning": False,
        "uniform_header_schedule": schedule,
    }
    return RootProgram(circuit, operations, grouped, graph.length, schedule["root"],
                       steps, mu, schedule, data_indices, work_indices, ledger)


def _apply_root_fourier(amplitudes, root_wires, *, inverse_fourier=True):
    """Apply F3^dagger (+) 1 (or F3 (+) 1 when inverse_fourier=False) on root_wires."""
    q0, q1 = root_wires
    b0, b1 = 1 << q0, 1 << q1
    mask = b0 | b1
    Fourier = np.array([[OMEGA**(i*j) for j in range(3)] for i in range(3)]) / sqrt(3)
    U = np.eye(4, dtype=complex)
    U[:3, :3] = Fourier.conj().T if inverse_fourier else Fourier
    result = {}
    for word, amp in amplitudes.items():
        d = ((word >> q0) & 1) | (((word >> q1) & 1) << 1)
        base = word & ~mask
        for out_d in range(4):
            coeff = U[out_d, d]
            if coeff != 0:
                nw = base | ((out_d & 1) << q0) | (((out_d >> 1) & 1) << q1)
                result[nw] = result.get(nw, 0) + coeff * amp
    return result


def apply_compiled_root(program, amplitudes, *, inverse=False):
    """Execute the lowered root program (including root inverse F3) on sparse states."""
    root_wires = program.data_wires[program.root]
    if not inverse:
        after_tree = apply_grouped_gates(program.grouped_operations, amplitudes, inverse=False)
        return _apply_root_fourier(after_tree, root_wires, inverse_fourier=True)
    before_tree = _apply_root_fourier(amplitudes, root_wires, inverse_fourier=False)
    return apply_grouped_gates(program.grouped_operations, before_tree, inverse=True)


def compiled_root_matrix(program):
    """Extract the 3^m x 3^m unitary matrix from actual gate execution on each basis word."""
    m = program.graph_length
    if m > 5:
        raise ValueError("UNKNOWN: full 3^m basis-by-basis compiled matrix extraction cap")
    words = tuple(product(range(3), repeat=m))
    D = len(words)
    T = np.zeros((D, D), dtype=complex)
    work_mask = ~((1 << (2 * m)) - 1)
    max_garbage = 0.0
    for col, word in enumerate(words):
        out = apply_compiled_root(program, {program.encode_data(word): 1.0 + 0.0j})
        garbage = sum(abs(amp)**2 for w_int, amp in out.items() if (w_int & work_mask) != 0)
        max_garbage = max(max_garbage, float(garbage))
        for row, target_word in enumerate(words):
            T[row, col] = out.get(program.encode_data(target_word), 0.0)
    if max_garbage > 1e-13:
        raise ArithmeticError("compiled root circuit left nonzero probability in arithmetic work qubits")
    residual = float(np.max(abs(T.conj().T @ T - np.eye(D))))
    if residual > 1e-10:
        raise ArithmeticError("compiled full-domain root unitary check failed")
    ledger = dict(program.ledger, full_domain_unitarity_residual=residual,
                  max_basis_work_garbage_probability=max_garbage)
    return T, ledger


def replay_compiled_root_control(graph, tree, mu=PHYSICAL, *, steps=3, seed=2026):
    """Replay full complex states (including invalid |11> encodings) against root_transform."""
    program = compile_root_program(graph, tree, mu=mu, steps=steps)
    T_ref, _ = root_transform(graph, tree, mu=mu, steps=steps)
    rng = np.random.default_rng(seed)
    m = graph.length
    words3 = list(product(range(3), repeat=m))
    psi3 = rng.normal(size=len(words3)) + 1j * rng.normal(size=len(words3))
    psi3 /= np.linalg.norm(psi3)
    source3 = {program.encode_data(w): complex(amp) for w, amp in zip(words3, psi3)}
    out3 = apply_compiled_root(program, source3)
    work_mask = ~((1 << (2 * m)) - 1)
    garbage3 = float(sum(abs(amp)**2 for w_int, amp in out3.items() if (w_int & work_mask) != 0))
    actual_vec = np.array([out3.get(program.encode_data(w), 0.0) for w in words3])
    expected_vec = T_ref @ psi3
    ref_error = float(np.linalg.norm(actual_vec - expected_vec))
    rec3 = apply_compiled_root(program, out3, inverse=True)
    inv_error3 = float(sqrt(sum(abs(rec3.get(k, 0) - source3.get(k, 0))**2 for k in rec3.keys() | source3.keys())))

    # Also test a complex superposition including unused |11> (value 3) encodings on physical wires
    words4 = list(product(range(4), repeat=m))
    sample_idx = rng.choice(len(words4), size=min(len(words4), 32), replace=False)
    invalid_words = [words4[i] for i in sample_idx]
    if not any(3 in w for w in invalid_words):
        invalid_words[0] = (3,) + invalid_words[0][1:]
    psi4 = rng.normal(size=len(invalid_words)) + 1j * rng.normal(size=len(invalid_words))
    psi4 /= np.linalg.norm(psi4)
    source4 = {program.encode_data(w): complex(amp) for w, amp in zip(invalid_words, psi4)}
    out4 = apply_compiled_root(program, source4)
    garbage4 = float(sum(abs(amp)**2 for w_int, amp in out4.items() if (w_int & work_mask) != 0))
    norm4 = float(sqrt(sum(abs(amp)**2 for amp in out4.values())))
    rec4 = apply_compiled_root(program, out4, inverse=True)
    inv_error4 = float(sqrt(sum(abs(rec4.get(k, 0) - source4.get(k, 0))**2 for k in rec4.keys() | source4.keys())))
    if max(ref_error, garbage3, inv_error3, garbage4, abs(norm4 - 1.0), inv_error4) > 1e-11:
        raise ArithmeticError("compiled root replay, cleanup, relative phase, or |11> completion failed")
    return {
        "root": program.root,
        "physical_qutrits": m,
        "distinct_leaves": program.schedule["distinct_physical_leaves"],
        "normalized_spectrum": [str(x) for x in program.mu],
        "CORDIC_steps": steps,
        "actual_qubits": program.circuit.num_qubits,
        "actual_logical_gates_before_root_Fourier": len(program.operations),
        "reference_statevector_norm_error": ref_error,
        "valid_subspace_work_garbage_probability": garbage3,
        "valid_subspace_inverse_error": inv_error3,
        "full_4m_including_11_work_garbage_probability": garbage4,
        "full_4m_including_11_norm": norm4,
        "full_4m_including_11_inverse_error": inv_error4,
        "upstream_herald_history_enumeration_used": False,
        "classical_CORDIC_digits_injected_as_advice": False,
    }


class BlockDecoder:
    """Sequential U, coherent root SUM, U-adjoint; retained records and F3 map."""

    def __init__(self, graph, depth, mu=PHYSICAL, *, steps=None, reverse=False, compiled=False):
        if type(reverse) is not bool or type(compiled) is not bool:
            raise ValueError("Boolean root-order and compiled controls required")
        if compiled and steps is None:
            raise ValueError("compiled uniform arithmetic decoder requires explicit integer CORDIC steps")
        self.code, self.mu = matrix_data(graph.H), spectrum(mu)
        self.partition = tree_partition(graph, depth)
        self.recovery = erasure_recovery(graph.H, self.partition["good"])
        if self.recovery["status"] != "EXACT_PUBLIC_LEFT_INVERSE":
            raise ValueError("UNKNOWN: erasure restriction is not injective")
        self.labels = tuple(product(range(3), repeat=self.code["dimension"]))
        self.words = tuple(product(range(3), repeat=graph.length))
        self.records = tuple(product(range(3), repeat=len(self.partition["good"])))
        if graph.length+2*self.code["dimension"]+len(self.partition["good"]) > 10:
            raise ValueError("UNKNOWN: full reference cap, not a graph exclusion")
        self.roots, self.ledgers, self.programs = [], [], []
        R, D = len(self.records), len(self.words)
        for j, tree in enumerate(self.partition["trees"]):
            if compiled:
                program = compile_root_program(graph, tree, mu, steps=steps)
                T, ledger = compiled_root_matrix(program)
                T_ref, _ = root_transform(graph, tree, mu, steps=steps)
                op_diff = float(np.linalg.norm(T - T_ref, 2))
                if op_diff > 1e-11:
                    raise ArithmeticError("compiled root unitary disagrees with Givens reference")
                ledger["operator_norm_difference_from_Givens_reference"] = op_diff
                self.programs.append(program)
            else:
                T, ledger = root_transform(graph, tree, mu, steps=steps)
            permutation = []
            for record in self.records:
                for word in self.words:
                    target = list(record)
                    target[j] = (target[j]+word[tree["root"]]) % 3
                    permutation.append(index(target)*D+index(word))
            self.roots.append((T, np.array(permutation), np.argsort(permutation)))
            self.ledgers.append(ledger)
        if reverse:
            self.roots.reverse()
        self.reverse = reverse
        self.compiled = compiled
        M = self.recovery["codeword_from_good"]
        self.estimates = [tuple(sum(a*b for a, b in zip(M[v], r)) % 3
                                for v in self.code["information_coordinates"]) for r in self.records]
        permutation = [index(tuple((a+b) % 3 for a, b in zip(u, e)))*R+j
                       for u in self.labels for j, e in enumerate(self.estimates)]
        self.recover = np.array(permutation), np.argsort(permutation)

    def apply(self, state, *, inverse=False, wrong_root_adjoint=False):
        N, R, D = len(self.labels), len(self.records), len(self.words)
        state = np.array(state, copy=True)
        if state.ndim != 4 or state.shape[1:] != (N, R, D):
            raise ValueError("batch x estimate x retained-record x physical-data tensor required")

        def recover(value):
            flat = value.reshape(-1, N*R, D)
            output = np.empty_like(flat)
            output[:, self.recover[int(inverse)], :] = flat
            return output.reshape(value.shape)

        if inverse:
            state = recover(state)
        for T, forward, backward in reversed(self.roots) if inverse else self.roots:
            state = state @ T.T
            flat = state.reshape(-1, R*D)
            output = np.empty_like(flat)
            output[:, backward if inverse else forward] = flat
            state = output.reshape(state.shape) @ (T.T if wrong_root_adjoint else T.conj())
        return state if inverse else recover(state)


def word_control(decoder):
    code = decoder.code
    _, states, codewords = sources(code, decoder.mu)
    N, R, D = len(decoder.labels), len(decoder.records), len(decoder.words)
    batch = np.zeros((N, N, R, D), complex)
    batch[:, 0, 0] = states
    actual = decoder.apply(batch)
    errors = [max(0., 1-float((abs(actual[u, u])**2).sum())) for u in range(N)]
    marginal = np.zeros((N, len(decoder.roots)))
    for i, (T, _, _) in enumerate(decoder.roots):
        # Ledger order must follow the root sequence, including reversal.
        ledger = decoder.ledgers[-1-i if decoder.reverse else i]
        observed = states @ T.T
        for u, word in enumerate(codewords):
            marginal[u, i] = max(0., 1-sum(abs(a)**2 for a, y in zip(observed[u], decoder.words)
                                         if y[ledger["root"]] == word[ledger["root"]]))
    gao = np.minimum(1., 4*marginal.sum(axis=1))
    if any(e > b+1e-10 for e, b in zip(errors, gao)):
        raise ArithmeticError("sequential retained-record error violates the sufficient Gao bound")
    return {"error_by_codeword": errors, "mean_word_error": float(np.mean(errors)),
            "original_state_marginal_root_errors": marginal.tolist(),
            "Gao_upper_by_codeword_numeric": gao.tolist(), "independent_root_errors_assumed": False}


def sampler_state(decoder, offsets, *, wrong_adjoint=False):
    code = decoder.code
    offsets = tuple(offsets)
    if len(offsets) != code["length"] or any(type(x) is not int or x not in (0, 1, 2) for x in offsets):
        raise ValueError("canonical unchanged offsets required")
    N, R, D = len(decoder.labels), len(decoder.records), len(decoder.words)
    initial = np.zeros((N, N, R, D), complex)
    initial[:, :, 0] = prepare_source(code, decoder.mu, offsets)
    actual = decoder.apply(initial)
    actual = subtract_label(actual, decoder.labels)
    actual = decoder.apply(actual, inverse=not wrong_adjoint)
    phi, _, _ = sources(code, decoder.mu)
    ideal = np.zeros_like(actual)
    syndrome = tuple(sum(a*b for a, b in zip(g, offsets)) % 3 for g in code["basis_G"])
    for j, word in enumerate(decoder.words):
        if tuple(sum(a*b for a, b in zip(g, word)) % 3 for g in code["basis_G"]) == syndrome:
            ideal[0, 0, 0, j] = sqrt(N)*phi[j]
    return actual, ideal


def audit_case(graph, depth, *, steps=None, reverse=False, wrong_adjoint=False, compiled=False):
    decoder = BlockDecoder(graph, depth, steps=steps, reverse=reverse, compiled=compiled)
    word = word_control(decoder)
    rows = []
    for J in product(range(3), repeat=graph.length):
        actual, ideal = sampler_state(decoder, J, wrong_adjoint=wrong_adjoint)
        probabilities = (abs(actual)**2).sum(axis=(0, 1, 2))
        output, target, partition = native_distribution(decoder.code, decoder.mu, J, probabilities)
        distance = float((abs(actual-ideal)**2).sum())
        TV = float(abs(output-target).sum()/2)
        if abs(float(probabilities.sum())-1) > 1e-10:
            raise ArithmeticError("unconditional decoder output is not normalized")
        if not wrong_adjoint and partition and TV > min(1., 2*sqrt(distance))+1e-10:
            raise ArithmeticError("normalization-aware comparison bound failed")
        rows.append({"offsets": J, "target_empty": not bool(partition), "state_distance_squared": distance,
                     "unconditional_TV_with_ABSTAIN": TV, "ABSTAIN_probability": float(output[-1]),
                     "all_work_and_source_label_zero_probability": float((abs(actual[0, 0, 0])**2).sum())})
    mean_distance = float(np.mean([r["state_distance_squared"] for r in rows]))
    residual = abs(mean_distance-2*word["mean_word_error"])
    if not wrong_adjoint and residual > 1e-10:
        raise ArithmeticError("all-offset retained-record Parseval identity failed")
    return {"H": graph.H, "sockets": graph.sockets, "partition": decoder.partition,
            "erasure_recovery": decoder.recovery, "root_gate_ledgers": decoder.ledgers,
            "root_order_reversed": reverse, "compiled_uniform_arithmetic": compiled,
            "word_control": word, "all_original_offsets": rows,
            "mean_unconditional_TV": float(np.mean([r["unconditional_TV_with_ABSTAIN"] for r in rows])),
            "mean_state_distance_squared": mean_distance, "Parseval_identity_residual": residual,
            "wrong_adjoint_countercontrol": wrong_adjoint,
            "reference_qutrits_including_ALL_records": graph.length+2*decoder.code["dimension"]+len(decoder.records[0]),
            "no_postselection_reset_or_input_conditioning": True,
            "these_are_mechanism_controls_not_regular_ensemble_samples": True}


def saved_topology_controls():
    original = json.loads(SOURCE.read_text())
    results = []
    for source in original["classical_original_dual_CSP_controls"]:
        graph = SocketGraph(tuple(zip(*source["forms_H_transpose"])), source["sockets"])
        variables, checks = graph.adjacency()
        if any(len(row) != 3 for row in variables) or any(len(row) != 6 for row in checks):
            raise ArithmeticError("saved original input is not raw (3,6)-regular")
        cases = []
        for depth in range(3):
            partition = tree_partition(graph, depth)
            recovery = erasure_recovery(graph.H, partition["good"])
            schedules = [root_schedule(graph, tree) for tree in partition["trees"]]
            cases.append({"depth": depth, "good": partition["good"], "bad": partition["bad"],
                          "erasure_recovery": recovery, "root_gate_execution_performed": False,
                          "root_schedule_leaf_counts": [s["distinct_physical_leaves"] for s in schedules],
                          "root_schedule_header_bits": [s["signed_trine_persistent_header_bits_sufficient"] for s in schedules]})
        results.append({"spins": source["spins"], "seed": source["seed"],
                        "original_offsets": source["original_offsets"], "cases": cases,
                        "raw_socket_count": len(graph.sockets), "source_rerolled_or_conditioned": False,
                        "classical_exact_pool_previously_completed": source["spins"] in (16, 32)})
    return results


def run_controls():
    dependencies = [Path(__file__), SOURCE, ROOT/"theorems/ternary_decoded_sampler.py",
                    ROOT/"theorems/ternary_coherent_reliability.py",
                    ROOT/"theorems/ternary_cordic_step.py",
                    ROOT/"theorems/ternary_coloring_bpqm.py"]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}
    duplicate = SocketGraph.simple(((1, 2, 1), (1, 2, 1)))
    cyclic = SocketGraph.simple(((1, 1, 1, 0), (1, 2, 0, 1)))
    nested = SocketGraph.simple(((1, 0, 0, 0, 0), (2, 1, 2, 0, 0), (0, 0, 1, 2, 1)))
    cases = [audit_case(duplicate, 1, steps=steps, reverse=reverse)
             for steps, reverse in ((None, False), (5, False), (5, True))]
    cases.append(audit_case(cyclic, 2))
    compiled_cases = [
        audit_case(duplicate, 1, steps=3, reverse=False, compiled=True),
        audit_case(duplicate, 1, steps=3, reverse=True, compiled=True),
    ]
    compiled_roots = [
        replay_compiled_root_control(duplicate, tree_partition(duplicate, 1)["trees"][0], steps=5, seed=2026),
        replay_compiled_root_control(cyclic, tree_partition(cyclic, 2)["trees"][0], steps=3, seed=2027),
        replay_compiled_root_control(nested, tree_partition(nested, 2)["trees"][0],
                                     mu=(Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)), steps=3, seed=2028),
    ]
    fault = audit_case(duplicate, 1, steps=5, wrong_adjoint=True)
    saved = saved_topology_controls()
    if hashes != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies}:
        raise RuntimeError("source or dependency changed during the live run")
    return {"schema_version": 2, "status": "UNIFORM_ARITHMETIC_HEADER_DAG_LOWERED_AND_REPLAYED_REVIEW_PENDING",
            "source_sha256": hashes, "finite_controls": cases,
            "compiled_uniform_arithmetic_sampler_controls": compiled_cases,
            "compiled_uniform_arithmetic_root_replays": compiled_roots,
            "wrong_adjoint_countercontrol": fault,
            "unchanged_native_socket_controls": saved,
            "certificate_entry_depth_resource_floor": regular_tree_size(13),
            "conditional_asymptotic_schedule_checks": [sufficient_depth_contract(n) for n in (32, 64, 10**6, 10**30)],
            "literature": ["https://arxiv.org/html/2609.05857v1#S4.SS3"],
            "polynomial_topology_and_erasure_map_implemented": True,
            "uniform_arithmetic_whole_receiver_assembled": True,
            "finite_block_ensemble_accuracy_certified": False,
            "quantum_speedup_or_classical_hardness_established": False,
            "local_derivation_independently_reviewed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"],
                      "controls": [{"reversed": c["root_order_reversed"],
                                    "word_error": c["word_control"]["mean_word_error"],
                                    "mean_TV": c["mean_unconditional_TV"],
                                    "Parseval_residual": c["Parseval_identity_residual"]}
                                   for c in report["finite_controls"]],
                      "compiled_roots": [{"root": r["root"], "qutrits": r["physical_qutrits"],
                                          "qubits": r["actual_qubits"],
                                          "gates": r["actual_logical_gates_before_root_Fourier"],
                                          "ref_error": r["reference_statevector_norm_error"],
                                          "garbage": r["full_4m_including_11_work_garbage_probability"]}
                                         for r in report["compiled_uniform_arithmetic_root_replays"]],
                      "wrong_adjoint_Parseval_residual": report["wrong_adjoint_countercontrol"]["Parseval_identity_residual"],
                      "saved_good_counts": [[len(d["good"]) for d in s["cases"]]
                                            for s in report["unchanged_native_socket_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
