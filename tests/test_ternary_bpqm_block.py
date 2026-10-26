from fractions import Fraction
import copy
from itertools import product
from math import sqrt

import numpy as np
import pytest

from theorems import ternary_bpqm_block as block
from theorems.ternary_coloring_bpqm import PHYSICAL, bit_spectrum, check_branches
from theorems.ternary_decoded_sampler import matrix_data, sources


def duplicate_graph():
    return block.SocketGraph.simple(((1, 2, 1), (1, 2, 1)))


def cyclic_graph():
    return block.SocketGraph.simple(((1, 1, 1, 0), (1, 2, 0, 1)))


def test_extrinsic_policy_excludes_one_raw_edge_not_all_edges_to_its_check():
    graph = block.SocketGraph(((0, 1),), ((0, 0, 1), (0, 0, 2), (1, 0, 1)))
    partition = block.tree_partition(graph, 1)
    assert partition["good"] == [1]
    assert partition["bad"][0]["root"] == 0
    assert partition["bad"][0]["reason"] == "repeated_physical_variable_or_parallel_socket"
    assert block.tree_partition(block.SocketGraph.simple(graph.H), 1)["good"] == [0, 1]
    assert partition["outgoing_edges"] == (0, 2)


def test_cyclic_full_graph_can_have_valid_tree_messages_without_cloning():
    graph = duplicate_graph()
    partition = block.tree_partition(graph, 1)
    assert partition["good"] == [0, 1, 2]
    assert all(tree["variables"] == [0, 1, 2] for tree in partition["trees"])
    assert block.tree_partition(graph, 2)["good"] == []
    assert not partition["compilation_failure_reclassified_as_bad_topology"]


def test_true_erasure_recovery_on_a_cyclic_graph_uses_coefficients_not_binary_rank():
    graph = cyclic_graph()
    partition = block.tree_partition(graph, 2)
    assert partition["good"] == [2, 3]
    recovery = block.erasure_recovery(graph.H, partition["good"])
    assert recovery["status"] == "EXACT_PUBLIC_LEFT_INVERSE"
    assert recovery["erased_column_rank"] == 2
    for c in product(range(3), repeat=4):
        if any(sum(a*b for a, b in zip(row, c)) % 3 for row in graph.H):
            continue
        observed = [c[g] for g in recovery["good"]]
        assert tuple(sum(a*b for a, b in zip(row, observed)) % 3
                     for row in recovery["codeword_from_good"]) == c
    failure = block.erasure_recovery(((1, 1, 1, 0), (1, 1, 0, 1)), [2, 3])
    assert failure["status"] == "ERASURE_NOT_UNIQUELY_RECOVERABLE"
    assert failure["kernel_codeword"] == [2, 1, 0, 0]


def test_complete_small_matrix_restriction_census_agrees_with_direct_codewords():
    for row in product(range(3), repeat=3):
        H = (row, row)  # Retain dependent and zero checks.
        codewords = [c for c in product(range(3), repeat=3)
                     if not sum(a*b for a, b in zip(row, c)) % 3]
        for flags in product((0, 1), repeat=3):
            good = [j for j, flag in enumerate(flags) if flag]
            recovery = block.erasure_recovery(H, good)
            fibers = {tuple(c[g] for g in good) for c in codewords}
            injective = len(fibers) == len(codewords)
            assert injective == (recovery["status"] == "EXACT_PUBLIC_LEFT_INVERSE")
            if injective:
                for c in codewords:
                    assert tuple(sum(row[j]*c[g] for j, g in enumerate(good)) % 3
                                 for row in recovery["codeword_from_good"]) == c
            else:
                witness = recovery["kernel_codeword"]
                assert any(witness) and all(witness[g] == 0 for g in good)
                assert sum(a*b for a, b in zip(row, witness)) % 3 == 0


def test_inconsistent_good_outcomes_are_not_postselected_or_silently_repaired():
    recovery = block.erasure_recovery(((1, 1, 1), (0, 1, 1)), [0, 1])
    M = recovery["codeword_from_good"]
    c = [sum(a*b for a, b in zip(row, (1, 0))) % 3 for row in M]
    assert c[:2] == [1, 0]
    assert any(sum(a*b for a, b in zip(row, c)) % 3 for row in ((1, 1, 1), (0, 1, 1)))
    assert not recovery["postselection_on_consistency"]


@pytest.mark.parametrize("mu", (PHYSICAL, (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7)), (1, 0, 0)))
def test_new_givens_root_matches_independent_density_law_and_codeword_covariance(mu):
    graph = duplicate_graph()
    code = matrix_data(graph.H)
    _, states, codewords = sources(code, mu)
    for tree in block.tree_partition(graph, 1)["trees"]:
        T, ledger = block.root_transform(graph, tree, mu)
        assert np.allclose(T.conj().T @ T, np.eye(27), atol=2e-12)
        root = tree["root"]
        row = graph.H[1]
        incoming = [tuple(mu[-row[root]*row[j]*f % 3] for f in range(3))
                    for j in range(3) if j != root]
        predicted = sum(float(p)*(1-sum(sqrt(float(x)) for x in bit_spectrum(mu, nu))**2/3)
                        for _, p, nu in check_branches(*incoming))
        observed = states @ T.T
        errors = [1-sum(abs(a)**2 for a, y in zip(psi, product(range(3), repeat=3))
                        if y[root] == c[root]) for psi, c in zip(observed, codewords)]
        assert np.allclose(errors, predicted, atol=2e-12)
        assert ledger["upstream_herald_tables_exponential_reference_only"]
        assert not ledger["herald_dephasing_or_original_output_cloning"]


def test_cordic_root_operator_error_obeys_two_givens_bound_not_branch_count():
    graph = duplicate_graph()
    tree = block.tree_partition(graph, 1)["trees"][0]
    exact, ledger = block.root_transform(graph, tree)
    for steps in (2, 4, 8, 12):
        approximate, _ = block.root_transform(graph, tree, steps=steps)
        assert np.linalg.norm(exact-approximate, 2) <= ledger["bit_compressions"]*2**(2-steps)+1e-12
    assert np.array_equal(block.givens_compression((0, 0, 0), 3), np.eye(3))


def test_nested_tree_header_schedule_and_phase_correct_root_against_independent_law():
    graph = block.SocketGraph.simple(((1, 0, 0, 0, 0), (2, 1, 2, 0, 0), (0, 0, 1, 2, 1)))
    tree = block.tree_partition(graph, 2)["trees"][0]
    schedule = block.root_schedule(graph, tree)
    assert schedule["distinct_physical_leaves"] == 5
    assert len(schedule["immutable_herald_wires"]) == 2
    assert len(schedule["retained_compression_garbage"]) == 2
    assert schedule["persistent_header_cleanup_needs_no_physical_gate_reversal"]
    assert schedule["uniform_arithmetic_header_dag_lowered"]
    mu = (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7))

    def law(node):
        output = [(Fraction(1), mu)]
        for check in node["checks"]:
            incoming = [[(p, tuple(nu[child["symbol_factor"]*j % 3] for j in range(3)))
                         for p, nu in law(child["tree"])] for child in check["children"]]
            message = incoming[0]
            for other in incoming[1:]:
                message = [(p*q*r, v) for p, nu in message for q, xi in other
                           for _, r, v in check_branches(nu, xi)]
            output = [(p*q, bit_spectrum(nu, xi)) for p, nu in output for q, xi in message]
        return output

    predicted = sum(float(p)*(1-sum(sqrt(float(x)) for x in nu)**2/3) for p, nu in law(tree["tree"]))
    T, ledger = block.root_transform(graph, tree, mu)
    words = list(product(range(3), repeat=5))
    phi = np.array([sqrt(float(np.prod([mu[y] for y in w]))) for w in words])
    codewords = [c for c in words if all(sum(a*b for a, b in zip(row, c)) % 3 == 0 for row in graph.H[1:])]
    states = np.array([phi*np.array([block.OMEGA**sum(a*b for a, b in zip(c, y)) for y in words]) for c in codewords])
    observed = states @ T.T
    errors = [1-sum(abs(a)**2 for a, y in zip(psi, words) if y[0] == c[0]) for c, psi in zip(codewords, observed)]
    assert np.allclose(errors, predicted, atol=3e-12)
    assert ledger["check_nodes"] == 2 and ledger["bit_compressions"] == 2


def test_compiled_root_program_replays_complex_states_and_invalid_11_encodings():
    graph = duplicate_graph()
    for tree in block.tree_partition(graph, 1)["trees"]:
        replay = block.replay_compiled_root_control(graph, tree, steps=4, seed=404 + tree["root"])
        assert replay["reference_statevector_norm_error"] < 1e-12
        assert replay["valid_subspace_work_garbage_probability"] == 0.0
        assert replay["valid_subspace_inverse_error"] < 1e-12
        assert replay["full_4m_including_11_work_garbage_probability"] == 0.0
        assert replay["full_4m_including_11_inverse_error"] < 1e-12
        assert not replay["upstream_herald_history_enumeration_used"]
        assert not replay["classical_CORDIC_digits_injected_as_advice"]


def test_compiled_nested_five_wire_nonuniform_tree_matches_givens_reference():
    graph = block.SocketGraph.simple(((1, 0, 0, 0, 0), (2, 1, 2, 0, 0), (0, 0, 1, 2, 1)))
    tree = block.tree_partition(graph, 2)["trees"][0]
    mu = (Fraction(1, 7), Fraction(2, 7), Fraction(4, 7))
    replay = block.replay_compiled_root_control(graph, tree, mu=mu, steps=3, seed=2028)
    assert replay["distinct_leaves"] == 5
    assert replay["reference_statevector_norm_error"] < 1e-12
    assert replay["valid_subspace_work_garbage_probability"] == 0.0
    assert replay["full_4m_including_11_work_garbage_probability"] == 0.0
    assert replay["full_4m_including_11_inverse_error"] < 1e-12


@pytest.mark.parametrize("reverse", (False, True))
def test_compiled_block_decoder_and_sampler_match_givens_reference_and_clean_dirty_records(reverse):
    graph = duplicate_graph()
    compiled_decoder = block.BlockDecoder(graph, 1, steps=3, reverse=reverse, compiled=True)
    ref_decoder = block.BlockDecoder(graph, 1, steps=3, reverse=reverse, compiled=False)
    for (T_comp, _, _), (T_ref, _, _), ledger in zip(
        compiled_decoder.roots, ref_decoder.roots, compiled_decoder.ledgers
    ):
        assert np.allclose(T_comp, T_ref, atol=1e-12)
        assert ledger["coherent_header_arithmetic_assembled_here"] is True
        assert ledger["upstream_herald_history_enumeration_used"] is False
        assert ledger["max_basis_work_garbage_probability"] == 0.0

    rng = np.random.default_rng(771 + int(reverse))
    shape = (2, len(compiled_decoder.labels), len(compiled_decoder.records), len(compiled_decoder.words))
    dirty_state = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    dirty_state /= np.linalg.norm(dirty_state)
    out_comp = compiled_decoder.apply(dirty_state)
    out_ref = ref_decoder.apply(dirty_state)
    assert np.allclose(out_comp, out_ref, atol=1e-12)
    assert np.allclose(compiled_decoder.apply(out_comp, inverse=True), dirty_state, atol=1e-12)

    case_comp = block.audit_case(graph, 1, steps=3, reverse=reverse, compiled=True)
    case_ref = block.audit_case(graph, 1, steps=3, reverse=reverse, compiled=False)
    assert case_comp["Parseval_identity_residual"] < 1e-11
    assert case_comp["mean_unconditional_TV"] == pytest.approx(case_ref["mean_unconditional_TV"], abs=1e-12)


def test_forged_tree_cannot_delete_a_coefficient_or_reuse_a_channel():
    graph = duplicate_graph()
    tree = block.tree_partition(graph, 1)["trees"][0]
    mutated = copy.deepcopy(tree)
    mutated["tree"]["checks"][0]["children"][0]["symbol_factor"] = 3
    with pytest.raises(ValueError, match="coefficient"):
        block.root_schedule(graph, mutated)
    mutated = copy.deepcopy(tree)
    mutated["tree"]["checks"][0]["children"].pop()
    with pytest.raises(ValueError, match="socket"):
        block.root_schedule(graph, mutated)


def test_regular_tree_resource_floor_counts_original_outputs_not_reused_messages():
    assert block.regular_tree_size(0)["physical_leaves"] == 1
    assert block.regular_tree_size(1)["physical_leaves"] == 11
    result = block.regular_tree_size(13)
    assert result["physical_leaves"] == 11_111_111_111_111
    assert result["sampler_compressions_per_decoded_root_including_ALL_adjoints"] == 8*(10**13-1)//9


def test_asymptotic_schedule_never_advertises_its_local_error_term_as_finite_accuracy():
    for N in (32, 64, 10**6, 10**30):
        contract = block.sufficient_depth_contract(N)
        t = contract["extra_levels"]
        assert 3**(2**t) >= N**6
        assert t == 0 or 3**(2**(t-1)) < N**6
        assert not contract["finite_N_rank_failure_probability_certified"]
        assert Fraction(contract["whole_sampler_precision_contract"]["total_output_TV_perturbation_upper"]) <= Fraction(1, N)
        if N <= 10**6:
            assert contract["topology_size_status"] == "NO_GOOD_ROOT_POSSIBLE_AT_THIS_SUFFICIENT_DEPTH"
    with pytest.raises(ValueError, match="even"):
        block.sufficient_depth_contract(33)


@pytest.mark.parametrize("reverse", (False, True))
@pytest.mark.parametrize("steps", (None, 5))
def test_whole_decoder_is_total_on_complex_dirty_records_and_estimate_inputs(reverse, steps):
    decoder = block.BlockDecoder(duplicate_graph(), 1, steps=steps, reverse=reverse)
    rng = np.random.default_rng(972)
    shape = (2, len(decoder.labels), len(decoder.records), len(decoder.words))
    state = rng.normal(size=shape)+1j*rng.normal(size=shape)
    state /= np.linalg.norm(state)
    actual = decoder.apply(state)
    assert np.linalg.norm(actual) == pytest.approx(1)
    assert np.allclose(decoder.apply(actual, inverse=True), state, atol=3e-12)
    # A wrong local adjoint is also unitary: norm alone must not validate it.
    broken = decoder.apply(state, wrong_root_adjoint=True)
    assert np.linalg.norm(broken) == pytest.approx(1)
    assert np.linalg.norm(broken-actual) > 0.1


@pytest.mark.parametrize("graph,depth", ((duplicate_graph(), 1), (cyclic_graph(), 2)))
def test_word_error_keeps_every_sequential_readout_and_satisfies_gao(graph, depth):
    decoder = block.BlockDecoder(graph, depth, steps=5)
    control = block.word_control(decoder)
    assert np.all(np.array(control["error_by_codeword"]) <= np.array(control["Gao_upper_by_codeword_numeric"])+1e-12)
    assert not control["independent_root_errors_assumed"]
    assert max(control["error_by_codeword"]) < 1


def test_complete_offset_sampler_identity_includes_all_retained_records_and_empty_targets():
    case = block.audit_case(duplicate_graph(), 1, steps=5)
    assert len(case["all_original_offsets"]) == 27
    assert case["Parseval_identity_residual"] < 1e-11
    assert case["reference_qutrits_including_ALL_records"] == 10
    assert any(r["target_empty"] for r in case["all_original_offsets"])
    assert any(r["all_work_and_source_label_zero_probability"] < 0.99 for r in case["all_original_offsets"])
    assert case["mean_state_distance_squared"] == pytest.approx(2*case["word_control"]["mean_word_error"])


def test_wrong_global_adjoint_fails_parseval_even_though_normalization_passes():
    case = block.audit_case(duplicate_graph(), 1, steps=5, wrong_adjoint=True)
    assert case["Parseval_identity_residual"] > 0.01


def test_saved_original_sockets_are_used_without_sat_or_coefficient_filtering():
    cases = block.saved_topology_controls()
    assert [(c["spins"], c["seed"]) for c in cases] == [(16, 711), (32, 712)]
    for case in cases:
        assert case["raw_socket_count"] == 6*case["spins"]
        assert not case["source_rerolled_or_conditioned"]
        assert len(case["original_offsets"]) == 2*case["spins"]
        assert all(not c["root_gate_execution_performed"] for c in case["cases"])
    small, larger = cases
    assert [len(c["good"]) for c in small["cases"]] == [32, 9, 0]
    assert [len(c["good"]) for c in larger["cases"]] == [64, 33, 0]
    assert larger["cases"][1]["erasure_recovery"]["erased_column_rank"] == 31
    assert larger["cases"][1]["erasure_recovery"]["status"] == "EXACT_PUBLIC_LEFT_INVERSE"
    assert larger["cases"][1]["root_schedule_leaf_counts"] == [11]*33


def test_unit_checks_are_explicit_compiler_failure_not_graph_erasure():
    graph = block.SocketGraph.simple(((1, 1, 1), (1, 0, 0)))
    partition = block.tree_partition(graph, 1)
    assert 0 in partition["good"]
    with pytest.raises(ValueError, match="unit parity check"):
        block.root_transform(graph, partition["trees"][0])


def test_compile_root_program_cap_and_missing_steps_fail_closed():
    graph = duplicate_graph()
    tree = block.tree_partition(graph, 1)["trees"][0]
    with pytest.raises(ValueError, match="reference cap"):
        block.compile_root_program(graph, tree, steps=5, max_gates=100)
    with pytest.raises(ValueError, match="CORDIC steps"):
        block.BlockDecoder(graph, 1, compiled=True)


@pytest.mark.parametrize("H,sockets", [
    (((0,),), ((0, 0, 1),)), (((1,),), ((0, 0, 3),)),
    (((1,),), ((True, 0, 1),)), (((1,),), ((0, 1, 1),)),
])
def test_malformed_or_altered_socket_source_rejected(H, sockets):
    with pytest.raises(ValueError):
        block.SocketGraph(H, sockets)


def test_bad_outgoing_erasure_and_caps_are_not_silent_success():
    with pytest.raises(ValueError, match="outgoing"):
        block.tree_partition(duplicate_graph(), 1, outgoing=(None, None, None))
    with pytest.raises(ValueError, match="distinct"):
        block.erasure_recovery(((1, 1, 1),), [0, 0])
    with pytest.raises(ValueError, match="not injective"):
        block.BlockDecoder(duplicate_graph(), 2)
    with pytest.raises(ValueError, match="canonical"):
        block.canonical_matrix(((True, 0),))
