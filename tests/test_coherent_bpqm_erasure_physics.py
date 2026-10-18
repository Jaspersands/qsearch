"""Native instruments, exact erasure rank, raw topology and all workspace."""

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Operator, Statevector
from scipy.linalg import hadamard

import theorems.coherent_bpqm_erasure as workbench
from theorems.coherent_bpqm_erasure import (
    REPORT, CodeProblem, TreeCompilationLimit, decoder_program, erasure_plan,
    codeword_error_floor, duplicate_clause_reduction, finite_control,
    raw_edges, readout_program, recovery_map, run_controls,
    socket_plan, tree_partition, word_control,
)
from theorems.coherent_bpqm_tree import root_program


PROBLEM = CodeProblem(5, (25, 26, 12))


def native_word_state(problem, c, word):
    gamma = (1 - np.sqrt(1 - float(c) ** 2)) / 2
    encoded = problem.encode(word)
    return np.array([np.sqrt(gamma ** (x ^ encoded).bit_count() *
                            (1 - gamma) ** (problem.length - (x ^ encoded).bit_count()))
                     for x in range(1 << problem.length)])


def independent_projector_histories(problem, c, depth, reverse=False):
    plan = erasure_plan(problem, depth)
    good = plan["partition"]["good"]
    sequence = list(enumerate(good))
    if reverse:
        sequence.reverse()
    size = 1 << problem.length
    projectors = {}
    for index, root in sequence:
        U = Operator(root_program(problem, c, root, depth=depth)[0]).data
        signs = 1 - 2 * ((np.arange(size) >> root) & 1)
        observable = U.conj().T @ (signs[:, None] * U)
        projectors[index] = ((np.eye(size) + observable) / 2, (np.eye(size) - observable) / 2)
    histories = []
    for bits in range(1 << len(good)):
        product = np.eye(size, dtype=complex)
        for index, _ in sequence:
            product = projectors[index][(bits >> index) & 1] @ product
        histories.append(product)
    return plan, histories


@pytest.mark.parametrize("depth", [0, 1, 2])
def test_raw_multigraph_partition_matches_independent_breadth_first_tree_test(depth):
    for problem in (PROBLEM, CodeProblem(4, (7, 11)), CodeProblem(6, (7, 28, 49))):
        graph = nx.MultiGraph()
        graph.add_nodes_from(("v", i) for i in range(problem.length))
        for i, h in enumerate(problem.checks):
            for v in range(problem.length):
                if (h >> v) & 1:
                    graph.add_edge(("c", i), ("v", v))
        expected = []
        for v in range(problem.length):
            distances = nx.single_source_shortest_path_length(graph, ("v", v), cutoff=2 * depth)
            checks = [node for node, distance in distances.items() if node[0] == "c" and distance < 2 * depth]
            neighborhood = nx.MultiGraph()
            neighborhood.add_node(("v", v))
            for node in checks:
                for left, right in graph.edges(node):
                    neighborhood.add_edge(left, right)
            supported = all(graph.degree(node) > 1 for node in checks)
            if nx.is_tree(neighborhood) and supported:
                expected.append(v)
        assert tree_partition(problem, depth)["good"] == expected


def test_raw_parallel_edges_are_not_erased_by_binary_cancellation():
    problem = CodeProblem(2, (0,))
    canonical = tree_partition(problem, 1)
    raw = tree_partition(problem, 1, check_variables=[[0, 0]])
    assert canonical["good"] == [0, 1]
    assert raw["good"] == [1]
    assert raw["excluded"][0]["reason"] == "repeated_physical_variable_or_parallel_edge"
    assert erasure_plan(problem, 1, check_variables=[[0, 0]])["recovery"]["status"] == "ERASURE_NOT_UNIQUELY_RECOVERABLE"
    with pytest.raises(ValueError, match="multiplicities"):
        raw_edges(problem, [[0]])


def test_compilation_caps_are_not_reclassified_as_cyclic_or_unrecoverable_graphs():
    problem = CodeProblem(11, (2047,))
    plan = erasure_plan(problem, 1)
    assert plan["partition"]["good"] == list(range(11))
    assert plan["recovery"]["status"] == "EXACT_PUBLIC_LEFT_INVERSE"
    with pytest.raises(TreeCompilationLimit, match="compiler cap"):
        decoder_program(problem, "13/20", 1)


def test_public_left_inverse_really_recovers_erased_information_not_just_good_free_bits():
    plan = erasure_plan(PROBLEM, 1)
    recovery = plan["recovery"]
    good = plan["partition"]["good"]
    assert good == [0, 1, 2] and recovery["erased"] == [3, 4]
    assert list(PROBLEM.structure[1]) == recovery["erased"]
    masks = list(map(lambda x: int(x, 16), recovery["information_from_good_masks_hex"]))
    assert masks == [4, 5]
    for word in range(4):
        encoded = PROBLEM.encode(word)
        observed = sum(((encoded >> v) & 1) << j for j, v in enumerate(good))
        decoded = sum(((observed & mask).bit_count() % 2) << i for i, mask in enumerate(masks))
        assert decoded == word
    # Every one of the 2^|G| record strings has a defined reversible XOR map;
    # inconsistent strings are never used as a hidden postselection test.
    assert recovery["inconsistent_outcomes_postselected_or_rejected"] is False


def test_rank_failure_supplies_an_independent_ambiguity_witness():
    problem = CodeProblem(4, (7, 11))
    plan = erasure_plan(problem, 1)
    recovery = plan["recovery"]
    witness = int(recovery["undetermined_codeword_hex"], 16)
    assert witness == 3 and all((witness & h).bit_count() % 2 == 0 for h in problem.checks)
    assert all(not ((witness >> v) & 1) for v in recovery["good"])
    assert recovery["status"] == "ERASURE_NOT_UNIQUELY_RECOVERABLE"
    with pytest.raises(TreeCompilationLimit, match="uniquely"):
        decoder_program(problem, "13/20", 1)


@pytest.mark.parametrize("good", [[0, 0], [True], [-1], [5]])
def test_invalid_good_coordinate_views_are_rejected(good):
    with pytest.raises(ValueError, match="good-coordinate"):
        recovery_map(PROBLEM, good)


@pytest.mark.parametrize("reverse", [False, True])
def test_actual_sequential_decoder_matches_noncommuting_projector_histories(reverse):
    c = Fraction(13, 20)
    plan, histories = independent_projector_histories(PROBLEM, c, 1, reverse)
    recovery = plan["recovery"]
    masks = [int(text, 16) for text in recovery["information_from_good_masks_hex"]]
    expected = []
    for word in range(4):
        state = native_word_state(PROBLEM, c, word)
        probabilities = [float(np.linalg.norm(K @ state) ** 2) for K in histories]
        assert sum(probabilities) == pytest.approx(1, abs=2e-12)
        expected.append(sum(p for bits, p in enumerate(probabilities)
                            if sum(((bits & mask).bit_count() % 2) << i for i, mask in enumerate(masks)) == word))
    actual = word_control(PROBLEM, c, 1, reverse=reverse)
    assert actual["success_by_codeword"] == pytest.approx(expected, abs=3e-12)
    assert actual["average_word_error"] <= actual["Gao_sufficient_block_error_upper_numerical"] + 1e-11
    assert actual["root_errors_assumed_independent"] is False
    errors = np.array(actual["original_state_root_errors_by_codeword"])
    assert np.max(abs(errors - errors[0])) < 3e-12


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("signs", [0, 5, 31])
def test_entire_readout_state_matches_independent_retained_record_formula(reverse, signs):
    c = Fraction(13, 20)
    plan, histories = independent_projector_histories(PROBLEM, c, 1, reverse)
    masks = [int(x, 16) for x in plan["recovery"]["information_from_good_masks_hex"]]
    estimates = [sum(((b & mask).bit_count() % 2) << i for i, mask in enumerate(masks)) for b in range(8)]
    expected = np.zeros((8, 4, 32), dtype=complex)
    for record, residual in itertools.product(range(8), range(4)):
        for branch in range(8):
            word = residual ^ estimates[branch]
            phase = (-1) ** ((signs & PROBLEM.encode(word)).bit_count() % 2)
            expected[record, residual] += phase * histories[record ^ branch].conj().T @ (
                histories[branch] @ native_word_state(PROBLEM, c, word)) / 2
    phase = np.array([(-1) ** ((signs & y).bit_count() % 2) for y in range(32)])
    expected = (expected * phase) @ hadamard(32).T / np.sqrt(32)
    circuit, _ = readout_program(PROBLEM, c, signs, 1, reverse=reverse)
    actual = Statevector.from_instruction(circuit).data.reshape(8, 4, 4, 32)
    assert np.max(abs(actual[:, 0] - expected)) < 6e-12
    assert np.max(abs(actual[:, 1:])) < 4e-12
    assert np.sum(abs(expected) ** 2) == pytest.approx(1, abs=3e-12)
    # Information-output scratch clears algebraically, but measurement records
    # and the original source label do not generally clear at finite error.
    assert np.sum(abs(expected[1:]) ** 2) > 1e-3


def test_record_erasure_does_not_automatically_make_cyclic_readout_exact():
    result = finite_control(PROBLEM, "13/20", 1)
    assert result["mean_unconditional_TV"] > .1
    assert result["worst_unconditional_TV"] > .2
    assert min(r["data_purity"] for r in result["all_sign_cases"]) < .99
    assert all(r["classical_exact_factor_reference_executed"] for r in result["all_sign_cases"])
    assert result["postselection_or_workspace_reset_used"] is False
    assert result["mean_unconditional_TV"] <= result["reliable_decoding_sqrt_error_comparator"] + 1e-10


def test_word_failure_probability_is_not_a_linear_TV_budget():
    result = finite_control(PROBLEM, "1/5", 1)
    assert result["mean_unconditional_TV"] > 10 * result["word_control"]["average_word_error"]
    assert result["mean_unconditional_TV"] <= result["reliable_decoding_sqrt_error_comparator"] + 1e-10


def test_orthogonal_channel_control_has_exact_uniform_Gibbs_readout_without_postselection():
    result = finite_control(PROBLEM, "0", 1)
    assert abs(result["word_control"]["average_word_error"]) < 1e-12
    assert result["worst_unconditional_TV"] < 1e-11
    assert not result["postselection_or_workspace_reset_used"]


def test_actual_source_adjoint_and_all_record_gates_are_charged():
    circuit, ledger = readout_program(PROBLEM, "13/20", 5, 1)
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    assert compiled.num_qubits == ledger["actual_total_qubits"] == 12
    assert compiled.count_ops().get("cx", 0) == ledger["total_CNOTs_including_source_and_adjoints"]
    assert compiled.count_ops().get("u", 0) == ledger["total_one_qubit_gates_including_source_and_adjoints"]
    assert ledger["retained_good_record_qubits"] == 3
    assert ledger["global_PGM_table_entries"] == 0
    assert ledger["original_outputs_cloned"] is False
    assert ledger["intermediate_heralds_measured_or_reset"] is False
    assert ledger["uniform_reliability_register_compiler_implemented"] is False
    faulty, _ = readout_program(PROBLEM, "13/20", 5, 1, skip_adjoint=True)
    assert np.linalg.norm(Statevector.from_instruction(circuit).data - Statevector.from_instruction(faulty).data) > .1


def test_raw_regular_socket_plan_is_public_and_does_not_compile_or_simulate(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("no quantum execution licensed by a topology/rank plan")
    monkeypatch.setattr(workbench, "root_program", forbidden)
    result = socket_plan(128, 71)
    source, plan = result["source"], result["plan"]
    assert source["spins"] == 128 and source["clauses"] == 256
    assert source["conditioned_on_rank_girth_sign_or_success"] is False
    assert result["source_rejected_or_rerolled"] is False
    assert result["quantum_circuit_compiled_or_executed"] is False
    raw = result["raw_check_variables"]
    assert all(len(check) == 6 for check in raw)
    assert all(sum(row.count(v) for row in raw) == 3 for v in range(256))
    good = plan["partition"]["good"]
    assert len(good) == 192 and plan["recovery"]["status"] == "EXACT_PUBLIC_LEFT_INVERSE"
    problem = CodeProblem(256, tuple(int(h, 16) for h in plan["checks_hex"]))
    # Replay the whole left inverse on basis codewords, without enumerating 2^k words.
    masks = [int(x, 16) for x in plan["recovery"]["information_from_good_masks_hex"]]
    for i, codeword in enumerate(problem.structure[0]):
        observed = sum(((codeword >> v) & 1) << j for j, v in enumerate(good))
        assert sum(((mask & observed).bit_count() % 2) << j for j, mask in enumerate(masks)) == 1 << i


def test_source_rank_failures_are_retained_with_actual_codeword_witnesses():
    result = socket_plan(256, 29)
    recovery = result["plan"]["recovery"]
    assert recovery["status"] == "ERASURE_NOT_UNIQUELY_RECOVERABLE"
    witness = int(recovery["undetermined_codeword_hex"], 16)
    checks = list(map(lambda h: int(h, 16), result["plan"]["checks_hex"]))
    assert witness and all((witness & h).bit_count() % 2 == 0 for h in checks)
    assert all(not ((witness >> v) & 1) for v in recovery["good"])


def test_exact_genie_floor_does_not_turn_word_decoding_into_a_sampling_gate():
    result = socket_plan(256, 29)
    record = result["word_error_floor_not_a_sampling_obstruction"]
    assert record["weight"] == 2
    lower = Fraction(record["any_decoder_average_word_error_lower_exact"])
    upper = Fraction(record["binary_Helstrom_error_upper_exact"])
    squared_overlap = Fraction(record["binary_squared_overlap_exact"])
    assert Fraction(4, 100) < lower < upper < Fraction(5, 100)
    assert (1 - 2 * upper) ** 2 <= 1 - squared_overlap <= (1 - 2 * lower) ** 2
    assert upper - lower <= Fraction(1, 2 ** 81)
    assert record["a_Gibbs_TV_or_sampling_lower_bound"] is False
    with pytest.raises(ValueError, match="kernel"):
        codeword_error_floor(PROBLEM, "13/20", 1)


def test_small_binary_state_helstrom_spectrum_replays_the_analytic_word_floor():
    # The two codewords differ on exactly two positions; the other wires
    # are irrelevant even after revealing their pair label.
    problem = CodeProblem(2, (3,))
    c = Fraction(13, 20)
    a, b = native_word_state(problem, c, 0), native_word_state(problem, c, 1)
    numerical = .5 - np.sum(abs(np.linalg.eigvalsh(np.outer(a, a) - np.outer(b, b)))) / 4
    record = codeword_error_floor(problem, c, 3)
    assert numerical == pytest.approx(float(Fraction(record["any_decoder_average_word_error_lower_exact"])), abs=2e-15)


def replay_factor_identity(model, c, reduction, spin_word):
    c = Fraction(c)
    original = np.prod([Fraction(1) + c * (-1) ** ((mask & spin_word).bit_count() + sign)
                        for mask, sign in model.clauses])
    rebuilt = Fraction(reduction["constant_weight_factor_exact"])
    for group in reduction["groups"]:
        if not group["factor_dropped_as_constant"]:
            rebuilt *= 1 + Fraction(group["effective_signed_overlap_exact"]) * (
                (-1) ** ((int(group["mask_hex"], 16) & spin_word).bit_count()))
    assert original == rebuilt


def test_duplicate_and_opposite_clauses_have_an_exact_classical_Gibbs_reduction():
    from theorems.bpqm_gibbs_frontier import XorIsing
    model = XorIsing(3, ((1, 1), (1, 1), (3, 0), (3, 1), (0, 1), (7, 0)))
    reduction = duplicate_clause_reduction(model, "13/20")
    assert reduction["nonconstant_weighted_clause_count"] == 2
    groups = {int(g["mask_hex"], 16): g for g in reduction["groups"]}
    assert Fraction(groups[1]["effective_signed_overlap_exact"]) == -2 * Fraction(13, 20) / (1 + Fraction(13, 20) ** 2)
    assert groups[3]["factor_dropped_as_constant"] and groups[0]["factor_dropped_as_constant"]
    for word in range(8):
        replay_factor_identity(model, "13/20", reduction, word)
    assert reduction["weighted_output_has_original_regular_ensemble_or_common_overlap"] is False


def test_large_ambiguity_is_duplicate_unary_factors_not_a_Gibbs_hardness_witness():
    from theorems.bpqm_gibbs_frontier import XorIsing
    result = socket_plan(256, 29)
    members = result["source"]["clause_masks_hex_and_signs"]
    assert members[160] == members[189] and int(members[160][0], 16).bit_count() == 1
    model = XorIsing(256, tuple((int(mask, 16), sign) for mask, sign in members))
    reduction = result["exact_classical_duplicate_factor_reduction"]
    assert any(160 in g["original_coordinates"] and 189 in g["original_coordinates"] for g in reduction["groups"])
    for word in (0, (1 << 256) - 1, 1 << 149):
        replay_factor_identity(model, "13/20", reduction, word)


def test_live_artifact_replays_with_no_uniform_compiler_or_separation_promotion():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(workbench.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert not report["accepted_speedup_candidate"]
    assert not report["asymptotic_gate_or_classical_separation_proved"]
    assert report["known_mechanism_not_a_novel_quantum_algorithm"]
    assert len(report["unfiltered_socket_topology_and_rank_controls"]) == 6
