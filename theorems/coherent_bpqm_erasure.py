"""Known BPQM/linear-erasure mechanism, executed with every record retained.

This bounded coherent implementation is a falsification reference, NOT the
uniform reliability-register compiler or a random-regular block-error proof.
Topology checks keep raw parallel edges. Erasure rank is tested exactly;
finite gate programs never clone data, measure heralds, or query a PGM table.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from theorems.affine_cluster_native_probe import socket_instance
from theorems.bpqm_gibbs_frontier import exact_gibbs, integer, rational
from theorems.coherent_bpqm_tree import TreeCompilationLimit, root_program
from theorems.coherent_local_gibbs import CodeProblem, _channel, _spin_readout, source_circuit
from theorems.linear_erasure_prange_duality import null_basis
from theorems.xor_factor_reference import ExactXorReference

REPORT = ROOT / "research/phase_workbench/coherent_bpqm_erasure.json"


def raw_edges(problem, check_variables=None):
    if check_variables is None:
        check_variables = [[j for j in range(problem.length) if (h >> j) & 1] for h in problem.checks]
    if len(check_variables) != len(problem.checks):
        raise ValueError("one raw adjacency list per public parity check required")
    incidence = [[] for _ in range(problem.length)]
    checks, edges = [], []
    for index, (variables, h) in enumerate(zip(check_variables, problem.checks)):
        parity = 0
        members = []
        for v in variables:
            integer(v, "raw variable endpoint", 0, problem.length - 1)
            parity ^= 1 << v
            edge = len(edges)
            edges.append((index, v))
            members.append(edge)
            incidence[v].append(edge)
        if parity != h:
            raise ValueError("raw edge multiplicities do not reduce to the public binary check")
        checks.append(members)
    return incidence, checks, edges


def tree_partition(problem, depth, *, check_variables=None):
    """Conservative FULL-root neighborhoods, not the paper's dv-1 edge policy.

    Cycles, including parallel edges, are structural exclusions. Compilation
    caps/precision failures are never silently classified as bad graph nodes.
    """
    integer(depth, "finite actual check depth", 0, problem.length)
    incidence, checks, edges = raw_edges(problem, check_variables)
    good, excluded, neighborhoods = [], [], []
    for root in range(problem.length):
        variables_seen, checks_seen = set(), set()
        reason = None

        def visit(v, parent, remaining):
            nonlocal reason
            if v in variables_seen:
                reason = "repeated_physical_variable_or_parallel_edge"
                return
            variables_seen.add(v)
            if not remaining:
                return
            for edge in incidence[v]:
                if edge == parent:
                    continue
                check, _ = edges[edge]
                if check in checks_seen:
                    reason = "repeated_check_or_parallel_edge"
                    return
                checks_seen.add(check)
                children = [other for other in checks[check] if other != edge]
                if not children:
                    reason = "fixed_bit_check_needs_separate_primitive"
                    return
                for other in children:
                    visit(edges[other][1], other, remaining - 1)
                    if reason:
                        return

        visit(root, None, depth)
        record = {"root": root, "variables": sorted(variables_seen), "check_indices": sorted(checks_seen)}
        if reason:
            excluded.append({"root": root, "reason": reason})
        else:
            good.append(root)
            neighborhoods.append(record)
    return {"depth": depth, "good": good, "excluded": excluded, "tree_neighborhoods": neighborhoods,
            "uses_full_root_not_extrinsic_edge_policy": True,
            "raw_edge_count": len(edges), "raw_parallel_edges_preserved": True}


def recovery_map(problem, good):
    """Public GF(2) left inverse; arbitrary inconsistent outcome words get a total map.

    We do NOT reject/postselect inconsistent estimates. Exact recovery is
    guaranteed when all good estimates are correct and restriction is injective.
    """
    if (not isinstance(good, (list, tuple)) or len(set(good)) != len(good)
            or any(type(v) is not int or not 0 <= v < problem.length for v in good)):
        raise ValueError("distinct canonical good-coordinate indices required")
    basis, free = problem.structure
    k = len(basis)
    restricted = [sum(((g >> v) & 1) << i for i, g in enumerate(basis)) for v in good]
    pivots = {}
    for index, value in enumerate(restricted):
        provenance = 1 << index
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value, provenance
                break
            row, old = pivots[pivot]
            value, provenance = value ^ row, provenance ^ old
    erased = [v for v in range(problem.length) if v not in good]
    if len(pivots) != k:
        witness_info = null_basis(tuple(restricted), k)[0]
        witness = problem.encode(witness_info)
        assert witness and all(not ((witness >> v) & 1) for v in good)
        return {"status": "ERASURE_NOT_UNIQUELY_RECOVERABLE", "good": list(good), "erased": erased,
                "information_rank_seen": len(pivots), "information_bits": k,
                "undetermined_codeword_hex": hex(witness), "minimum_distance_oracle_used": False}
    masks = []
    for i in range(k):
        target, mask = 1 << i, 0
        while target:
            row, old = pivots[target.bit_length() - 1]
            target, mask = target ^ row, mask ^ old
        masks.append(mask)
        assert sum(((mask & sum(((g >> v) & 1) << j for j, v in enumerate(good))).bit_count() % 2) << t
                   for t, g in enumerate(basis)) == 1 << i
    return {"status": "EXACT_PUBLIC_LEFT_INVERSE", "good": list(good), "erased": erased,
            "information_bits": k, "information_coordinates": list(free), "information_rank_seen": k,
            "information_from_good_masks_hex": list(map(hex, masks)),
            "linear_recovery_CNOTs": sum(mask.bit_count() for mask in masks),
            "inconsistent_outcomes_postselected_or_rejected": False,
            "minimum_distance_oracle_used": False}


def erasure_plan(problem, depth, *, check_variables=None):
    partition = tree_partition(problem, depth, check_variables=check_variables)
    return {"length": problem.length, "checks_hex": list(map(hex, problem.checks)),
            "partition": partition, "recovery": recovery_map(problem, partition["good"]),
            "quantum_circuit_executed": False, "asymptotic_error_or_gate_bound_certified": False}


def codeword_error_floor(problem, c, witness, *, bits=80):
    """Genie-aided binary Helstrom lower bound from a public nonzero codeword.

    Partition C into pairs {u,u+w}. Even revealing the pair leaves two pure
    states of overlap c^wt(w). This is a WORD-decoding bound, never a Gibbs
    sampling bound. Square-root enclosures use exact integer arithmetic.
    """
    c = rational(c)
    integer(witness, "nonzero canonical codeword witness", 1, (1 << problem.length) - 1)
    integer(bits, "rational enclosure precision", 1, 4096)
    if not 0 <= c < 1 or any((h & witness).bit_count() % 2 for h in problem.checks):
        raise ValueError("valid channel overlap and a true kernel codeword required")
    weight = witness.bit_count()
    squared_overlap = c ** (2 * weight)
    radicand = 1 - squared_overlap
    scale = 1 << bits
    floor = math.isqrt(radicand.numerator * scale * scale // radicand.denominator)
    low_root = Fraction(floor, scale)
    high_root = low_root if low_root * low_root == radicand else Fraction(floor + 1, scale)
    return {"witness_hex": hex(witness), "weight": weight, "overlap_c_exact": str(c),
            "binary_squared_overlap_exact": str(squared_overlap),
            "any_decoder_average_word_error_lower_exact": str(max(Fraction(0), (1 - high_root) / 2)),
            "binary_Helstrom_error_upper_exact": str((1 - low_root) / 2),
            "pair_identity_revealed_to_receiver_in_lower_bound": True,
            "a_Gibbs_TV_or_sampling_lower_bound": False}


def duplicate_clause_reduction(model, c):
    """Exact classical factor identity; weighted output is not the regular ensemble."""
    c = rational(c)
    if not 0 <= c < 1:
        raise ValueError("overlap in [0,1) required")
    groups = {}
    for index, (mask, sign) in enumerate(model.clauses):
        groups.setdefault(mask, []).append((index, sign))
    result = []
    constant = Fraction(1)
    retained = 0
    for mask, members in groups.items():
        positive = sum(not sign for _, sign in members)
        negative = len(members) - positive
        plus = (1 + c) ** positive * (1 - c) ** negative
        minus = (1 - c) ** positive * (1 + c) ** negative
        normalization = plus if mask == 0 else (plus + minus) / 2
        effective = Fraction(0) if mask == 0 else (plus - minus) / (plus + minus)
        retained += bool(mask and effective)
        constant *= normalization
        result.append({"mask_hex": hex(mask), "original_coordinates": [i for i, _ in members],
                       "positive_clauses": positive, "negative_clauses": negative,
                       "effective_signed_overlap_exact": str(effective),
                       "spin_independent_factor_exact": str(normalization),
                       "factor_dropped_as_constant": not bool(mask and effective)})
    return {"groups": result, "original_clause_count": len(model.clauses),
            "nonconstant_weighted_clause_count": retained, "constant_weight_factor_exact": str(constant),
            "identity": "product original (1+c*J*parity) = constant*product retained (1+c_eff*parity)",
            "normalized_Gibbs_distribution_unchanged": True,
            "weighted_output_has_original_regular_ensemble_or_common_overlap": False,
            "this_is_not_a_Gibbs_sampler_or_a_quantum_advantage_claim": True}


def decoder_program(problem, c, depth, *, check_variables=None, reverse=False):
    """V=successive U_i/copy/adjoint; append linear output XORs, retain V's records."""
    c, _ = _channel(c)
    if type(reverse) is not bool:
        raise ValueError("Boolean root-order flag required")
    plan = erasure_plan(problem, depth, check_variables=check_variables)
    recovery = plan["recovery"]
    if recovery["status"] != "EXACT_PUBLIC_LEFT_INVERSE":
        raise TreeCompilationLimit("UNKNOWN: erased coordinates are not uniquely recoverable")
    good = plan["partition"]["good"]
    m, k, count = problem.length, recovery["information_bits"], len(good)
    if m > 10:
        raise TreeCompilationLimit("UNKNOWN: explicit coherent-herald compiler cap, not a graph failure")
    circuit = QuantumCircuit(m + k + count)
    ledgers = []
    sequence = list(enumerate(good))
    if reverse:
        sequence.reverse()
    expected = {r["root"]: r for r in plan["partition"]["tree_neighborhoods"]}
    for index, root in sequence:
        local, ledger = root_program(problem, c, root, depth=depth)
        if ledger["distinct_original_channels_used"] != expected[root]["variables"]:
            raise ArithmeticError("raw tree and actual gate program use different physical variables")
        if Counter(ledger["checks_used"]) != Counter(problem.checks[i] for i in expected[root]["check_indices"]):
            raise ArithmeticError("raw tree and actual gate program use different check equations")
        circuit.compose(local, qubits=range(m), inplace=True)
        circuit.cx(root, m + k + index)
        circuit.compose(local.inverse(), qubits=range(m), inplace=True)
        ledgers.append(ledger)
    for i, text_mask in enumerate(recovery["information_from_good_masks_hex"]):
        mask = int(text_mask, 16)
        for j in range(count):
            if (mask >> j) & 1:
                circuit.cx(m + k + j, m + i)
    counts = circuit.count_ops()
    return circuit, {**plan, "overlap_c_exact": str(c), "record_order_reversed": reverse,
                     "good_root_programs": ledgers, "retained_good_record_qubits": count,
                     "estimate_qubits": k, "decoder_one_qubit_Euler_gates": int(counts.get("u", 0)),
                     "decoder_CNOTs": int(counts.get("cx", 0)), "global_PGM_table_entries": 0,
                     "original_outputs_cloned": False, "intermediate_heralds_measured_or_reset": False,
                     "explicit_herald_tables_can_be_exponential": True,
                     "uniform_reliability_register_compiler_implemented": False}


def readout_program(problem, c, signs, depth, *, reverse=False, skip_adjoint=False):
    decoder, ledger = decoder_program(problem, c, depth, reverse=reverse)
    m, k = problem.length, ledger["recovery"]["information_bits"]
    count = ledger["retained_good_record_qubits"]
    circuit = source_circuit(problem, c, signs)
    if count:
        circuit.add_register(QuantumRegister(count, "good_records"))
    mapping = [*range(m), *range(m + k, m + 2 * k), *range(m + 2 * k, m + 2 * k + count)]
    circuit.compose(decoder, qubits=mapping, inplace=True)
    for i in range(k):
        circuit.cx(m + k + i, m + i)
    if not skip_adjoint:
        circuit.compose(decoder.inverse(), qubits=mapping, inplace=True)
    for j in range(m):
        if (signs >> j) & 1:
            circuit.z(j)
    circuit.h(range(m))
    counts = circuit.count_ops()
    ledger.update({"actual_total_qubits": circuit.num_qubits,
                   "total_one_qubit_gates_including_source_and_adjoints": sum(int(v) for g, v in counts.items() if g != "cx"),
                   "total_CNOTs_including_source_and_adjoints": int(counts.get("cx", 0)),
                   "postselection_used": False, "skip_adjoint_fault": skip_adjoint,
                   "rotation_synthesis_error_certified": False})
    return circuit, ledger


def word_control(problem, c, depth, *, reverse=False):
    decoder, ledger = decoder_program(problem, c, depth, reverse=reverse)
    m, k, count = problem.length, ledger["estimate_qubits"], ledger["retained_good_record_qubits"]
    if decoder.num_qubits > 18:
        raise TreeCompilationLimit("UNKNOWN: finite word-error statevector cap")
    _, gamma = _channel(c)
    successes, marginal_errors = [], []
    for word in range(1 << k):
        encoded = problem.encode(word)
        source = QuantumCircuit(decoder.num_qubits)
        for j in range(m):
            source.ry(2 * math.asin(math.sqrt(gamma)), j)
            if (encoded >> j) & 1:
                source.x(j)
        state = Statevector.from_instruction(source)
        probabilities = state.evolve(decoder).probabilities().reshape(1 << count, 1 << k, 1 << m)
        successes.append(float(probabilities[:, word, :].sum()))
        errors = []
        for root in ledger["partition"]["good"]:
            U = root_program(problem, c, root, depth=depth)[0]
            root_distribution = state.evolve(U, qargs=range(m)).probabilities([root])
            errors.append(float(root_distribution[1 - ((encoded >> root) & 1)]))
        marginal_errors.append(errors)
    gao = min(1., 4 * max(map(sum, marginal_errors), default=0.))
    error = 1 - float(np.mean(successes))
    if error > gao + 2e-11:
        raise ArithmeticError("actual sequential decoder violates its Gao sufficient bound")
    return {"success_by_codeword": successes, "average_word_error": error,
            "worst_word_error": 1 - min(successes),
            "original_state_root_errors_by_codeword": marginal_errors,
            "Gao_sufficient_block_error_upper_numerical": gao,
            "root_errors_assumed_independent": False,
            "numerical_calibration_not_certified_gate_error": True}


def finite_control(problem, c, depth, *, reverse=False):
    m, k = problem.length, len(problem.structure[0])
    decoder, ledger = decoder_program(problem, c, depth, reverse=reverse)
    if m > 7 or decoder.num_qubits + k > 18:
        raise TreeCompilationLimit("UNKNOWN: full-sign quantum calibration cap")
    results = []
    for signs in range(1 << m):
        circuit, resources = readout_program(problem, c, signs, depth, reverse=reverse)
        state = Statevector.from_instruction(circuit).data
        environment_data = state.reshape(-1, 1 << m)
        probabilities = (abs(environment_data) ** 2).sum(axis=0)
        spin, abort = _spin_readout(problem, probabilities)
        target = np.array(list(map(float, exact_gibbs(problem.ising(signs), c))))
        reference = ExactXorReference(problem.ising(signs), c)
        factor_target = [float(reference.probability(x)) for x in range(1 << len(problem.checks))]
        if np.max(abs(target - factor_target)) > 1e-13:
            raise ArithmeticError("classical factor reference disagrees with native Gibbs law")
        rho = environment_data.T @ environment_data.conj()
        joint = (abs(state) ** 2).reshape(1 << ledger["retained_good_record_qubits"], 1 << k, 1 << k, 1 << m)
        results.append({"signs": signs, "spin_probabilities": list(map(float, spin)),
                        "unconditional_TV_including_abort": float((abs(spin - target).sum() + abort) / 2),
                        "abort_probability": float(abort), "data_purity": float(np.trace(rho @ rho).real),
                        "all_workspace_and_source_label_zero_probability": float(joint[0, 0, 0, :].sum()),
                        "classical_exact_factor_reference_executed": True,
                        "classical_reference_exponential_in_width_not_a_general_polynomial_sampler": True,
                        "total_CNOTs": resources["total_CNOTs_including_source_and_adjoints"]})
    word = word_control(problem, c, depth, reverse=reverse)
    return {"length": m, "checks_hex": list(map(hex, problem.checks)), "overlap_c_exact": str(rational(c)),
            "decoder_ledger": ledger, "word_control": word, "all_sign_cases": results,
            "mean_unconditional_TV": float(np.mean([r["unconditional_TV_including_abort"] for r in results])),
            "worst_unconditional_TV": max(r["unconditional_TV_including_abort"] for r in results),
            "reliable_decoding_sqrt_error_comparator": math.sqrt(max(0., word["average_word_error"])),
            "postselection_or_workspace_reset_used": False,
            "native_statevector_simulation_executed": True, "quantum_hardware_executed": False,
            "these_are_declared_mechanism_controls_not_random_regular_samples": True}


class _RecordedMatching(random.Random):
    def shuffle(self, values):
        super().shuffle(values)
        self.raw_matching = list(values)


def socket_plan(spins, seed, depth=1):
    rng = _RecordedMatching(seed)
    model, source = socket_instance(spins, rng)
    m = len(model.clauses)
    raw = [[] for _ in range(spins)]
    for variable in range(m):
        for check in rng.raw_matching[3 * variable:3 * (variable + 1)]:
            raw[check].append(variable)
    checks = tuple(sum(((mask >> i) & 1) << j for j, (mask, _) in enumerate(model.clauses)) for i in range(spins))
    problem = CodeProblem(m, checks)
    plan = erasure_plan(problem, depth, check_variables=raw)
    floor = None
    if plan["recovery"]["status"] == "ERASURE_NOT_UNIQUELY_RECOVERABLE":
        floor = codeword_error_floor(problem, "13/20", int(plan["recovery"]["undetermined_codeword_hex"], 16))
    return {"seed": seed, "source": source, "raw_check_variables": raw, "plan": plan,
            "word_error_floor_not_a_sampling_obstruction": floor,
            "exact_classical_duplicate_factor_reduction": duplicate_clause_reduction(model, "13/20"),
            "source_rejected_or_rerolled": False, "quantum_circuit_compiled_or_executed": False,
            "large_instance_decoder_execution_error_or_Gibbs_TV_measured": False}


def run_controls():
    cases = [finite_control(CodeProblem(5, (25, 26, 12)), c, 1, reverse=reverse)
             for c in ("1/5", "13/20") for reverse in (False, True)]
    failure = erasure_plan(CodeProblem(4, (7, 11)), 1)
    sockets = [socket_plan(spins, seed) for spins in (64, 128, 256) for seed in (29, 71)]
    helpers = ("coherent_bpqm_tree.py", "coherent_local_gibbs.py", "bpqm_gibbs_frontier.py",
               "affine_cluster_native_probe.py", "xor_factor_reference.py", "linear_erasure_prange_duality.py")
    return {"schema_version": "coherent-bpqm-erasure-v1", "finite_controls": cases,
            "underdetermined_erasure_falsifier": failure, "unfiltered_socket_topology_and_rank_controls": sockets,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "runtime_versions": {"qiskit": qiskit.__version__, "numpy": np.__version__},
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest() for name in helpers},
            "literature": ["https://arxiv.org/html/2609.05857", "https://arxiv.org/html/2609.40345v1"],
            "known_mechanism_not_a_novel_quantum_algorithm": True, "accepted_speedup_candidate": False,
            "asymptotic_gate_or_classical_separation_proved": False, "local_derivation_review_pending": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"finite_controls": [{"c": r["overlap_c_exact"], "reverse": r["decoder_ledger"]["record_order_reversed"],
                                           "mean_TV": r["mean_unconditional_TV"], "worst_TV": r["worst_unconditional_TV"],
                                           "word_error": r["word_control"]["average_word_error"]} for r in report["finite_controls"]],
                      "socket_controls": [{"spins": r["source"]["spins"], "seed": r["seed"],
                                            "good": len(r["plan"]["partition"]["good"]),
                                            "erasure_status": r["plan"]["recovery"]["status"]} for r in report["unfiltered_socket_topology_and_rank_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
