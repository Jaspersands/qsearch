import json

import numpy as np
import pytest

import verify as base
import verify_group_bridge as bridge
import verify_recursive_source as recursive


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_complete_manifest_and_scoped_audit():
    assert len(recursive.THEOREMS) == 25
    assert len(recursive.DECLARATIONS) == len(set(recursive.DECLARATIONS)) == 47
    assert (recursive.ROOT/"AuditRecursiveSource.lean").read_text() == recursive.expected_audit()
    assert set(base.parse_axioms(diagnostics(recursive.DECLARATIONS), recursive.DECLARATIONS)) == set(recursive.DECLARATIONS)


@pytest.mark.parametrize("declaration", [
    recursive.STAGE+"stepCertificate", recursive.STAGE+"reesStep",
    recursive.STAGE+"record_mass_complete", recursive.STAGE+"record_scaled_sources",
    recursive.TREE+"rees_record_tree", recursive.TREE+"rees_average_tree",
    recursive.TREE+"rees_tree_leafCount", recursive.TREE+"duplicate_children_pay_separately",
    recursive.TREE+"plan_packet_nonempty",
])
def test_missing_scientific_obligations_rejected(declaration):
    names = [name for name in recursive.DECLARATIONS if name != declaration]
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics(names), recursive.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumeDesiredSource", "CloneQuantumInput"])
def test_unapproved_proof_dependencies_rejected(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(recursive.DECLARATIONS, axiom), recursive.DECLARATIONS)


def test_frozen_algebra_cannot_change_unnoticed():
    with pytest.raises(ValueError, match="frozen receipt"):
        bridge.validate_base_record({"combined_theorem_count": 141}, {"combined_theorem_count": 142})


def test_scope_preserves_imported_obligations():
    scope = recursive.scope_report()
    for key in ("actual_adjacent_Rees_instruments_instantiated",
                "recursive_record_and_averaged_source_identity_checked",
                "independent_tensor_input_required",
                "complete_characters_and_nonzero_moment_witnesses_required",
                "top_stage_source_preparation_is_explicit_input"):
        assert scope[key]
    for key in ("arbitrary_correlated_input_supported", "adaptive_cross_packet_source_reuse_supported",
                "native_to_top_source_channel_formalized", "final_fourier_recovery_formalized",
                "diagonal_solver_implemented", "end_to_end_complexity_formalized",
                "formalizes_full_Rees_algorithm", "quantum_execution", "new_algorithm_or_novelty_claim"):
        assert not scope[key]


@pytest.mark.parametrize("correlation", ["entangled", "separable_shared_record"])
def test_correct_marginals_do_not_replace_independent_sources(correlation):
    # Exact dyadic entries: the same controlled permutation distinguishes
    # joint sources even though every one-register marginal is I/2.
    x = np.array([[0., 1.], [1., 0.]])
    joint_action = np.kron(x, x)
    independent = np.eye(4)/4
    if correlation == "entangled":
        correlated = np.array([[1., 0., 0., 1.], [0., 0., 0., 0.],
                               [0., 0., 0., 0.], [1., 0., 0., 1.]])/2
    else:
        # Equal mixture of |++><++| and |--><--|: no entanglement needed.
        correlated = (np.eye(4)+joint_action)/4
    for state in (independent, correlated):
        tensor = state.reshape(2, 2, 2, 2)
        assert np.array_equal(np.trace(tensor, axis1=0, axis2=2), np.eye(2)/2)
        assert np.array_equal(np.trace(tensor, axis1=1, axis2=3), np.eye(2)/2)
        assert np.linalg.eigvalsh(state)[0] >= 0
    assert np.trace(joint_action@independent) == 0
    assert np.trace(joint_action@correlated) == 1
    independent_output = np.eye(2)/2
    correlated_output = np.ones((2, 2))/2
    assert np.linalg.norm(independent_output-correlated_output, ord="nuc")/2 == .5
