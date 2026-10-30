import json

import pytest

import verify as base
import verify_group_bridge as bridge
import verify_quotients as quotients


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_manifest_covers_all_chain_constructors():
    assert len(quotients.THEOREMS) == 38
    assert len(quotients.DECLARATIONS) == len(set(quotients.DECLARATIONS)) == 64
    assert (quotients.ROOT/"AuditQuotients.lean").read_text() == quotients.expected_audit()
    assert set(base.parse_axioms(diagnostics(quotients.DECLARATIONS), quotients.DECLARATIONS)) == set(quotients.DECLARATIONS)


@pytest.mark.parametrize("missing", ["tailIdeal", "imageGroup", "stageGroupProjection",
                                     "stageSection_right_inverse", "step_kernel_central_and_scaled",
                                     "first_stage_recovers_all_h"])
def test_missing_structural_obligation_rejected(missing):
    names = [name for name in quotients.DECLARATIONS if name != quotients.PREFIX+missing]
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics(names), quotients.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumedQuotientBCH"])
def test_group_structure_cannot_be_replaced_by_unapproved_axioms(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(quotients.DECLARATIONS, axiom), quotients.DECLARATIONS)


def test_changed_frozen_central_step_rejected():
    with pytest.raises(ValueError, match="frozen receipt"):
        bridge.validate_base_record({"combined_theorem_count": 103}, {"combined_theorem_count": 104})


def test_scope_does_not_promote_group_chain_to_quantum_algorithm():
    scope = quotients.scope_report()
    for name in ("actual_graded_tail_ideals_constructed", "quotient_group_laws_constructed_from_base",
                 "central_scalar_kernels_checked", "hidden_images_and_public_sections_checked",
                 "terminal_stage_retains_all_original_hidden_subspace",
                 "truncated_nonzero_evaluation_shortcut_falsified",
                 "base_polynomial_group_law_is_explicit_hypothesis"):
        assert scope[name]
    for name in ("base_lazard_bch_theorem_formalized", "recursive_quantum_instrument_composed",
                 "fourier_recovery_formalized", "diagonal_solver_implemented",
                 "formalizes_full_Rees_algorithm", "quantum_execution", "new_algorithm_or_novelty_claim"):
        assert not scope[name]
