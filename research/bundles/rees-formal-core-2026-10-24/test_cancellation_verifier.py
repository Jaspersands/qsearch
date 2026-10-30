import json

import pytest

import verify as base
import verify_group_bridge as bridge
import verify_cancellation as cancellation


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_manifest_includes_constructors_and_physical_conclusion():
    assert len(cancellation.THEOREMS) == 15
    assert len(cancellation.DECLARATIONS) == len(set(cancellation.DECLARATIONS)) == 28
    assert (cancellation.ROOT/"AuditCancellation.lean").read_text() == cancellation.expected_audit()
    assert set(base.parse_axioms(diagnostics(cancellation.DECLARATIONS), cancellation.DECLARATIONS)) == set(cancellation.DECLARATIONS)


@pytest.mark.parametrize("missing", ["automorphismCertificate", "controlledAction", "moment_cancels",
                                     "publicDilation_hidden", "publicDilation_center", "reesCertificate",
                                     "rees_instrument", "quotientRelation_iff"])
def test_missing_operational_or_support_obligation_rejected(missing):
    names = [name for name in cancellation.DECLARATIONS if name != cancellation.PREFIX+missing]
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics(names), cancellation.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumedCancellation", "AssumedIdealChannel"])
def test_unapproved_axioms_cannot_supply_the_certificate(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(cancellation.DECLARATIONS, axiom), cancellation.DECLARATIONS)


def test_changed_frozen_group_bridge_rejected():
    with pytest.raises(ValueError, match="frozen receipt"):
        bridge.validate_base_record({"combined_theorem_count": 88}, {"combined_theorem_count": 89})


def test_scope_keeps_algorithmic_and_arithmetic_obligations_open():
    scope = cancellation.scope_report()
    for name in ("cancellation_certificate_constructed", "actual_rees_top_grade_instantiated",
                 "all_measurement_records_included", "arbitrary_address_reference_matrix",
                 "nonzero_moment_witness_is_explicit_hypothesis",
                 "complete_fourier_characters_are_explicit_hypothesis",
                 "base_polynomial_group_law_is_explicit_hypothesis"):
        assert scope[name]
    for name in ("base_lazard_bch_theorem_formalized", "diagonal_solver_implemented",
                 "graded_quotient_chain_formalized", "formalizes_full_Rees_algorithm",
                 "quantum_execution", "new_algorithm_or_novelty_claim"):
        assert not scope[name]
