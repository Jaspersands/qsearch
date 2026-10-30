import json

import pytest

import verify as base
import verify_group_bridge as bridge


def diagnostics(names, axiom="propext"):
    return "\n".join(json.dumps({"severity": "information",
                                "data": f"'{name}' depends on axioms: [{axiom}]"}) for name in names)


def test_full_declaration_manifest_matches_audit():
    assert len(bridge.THEOREMS) == 14
    assert len(bridge.DECLARATIONS) == len(set(bridge.DECLARATIONS)) == 26
    assert (bridge.ROOT/"AuditGroupBridge.lean").read_text() == bridge.expected_audit()
    assert set(base.parse_axioms(diagnostics(bridge.DECLARATIONS), bridge.DECLARATIONS)) == set(bridge.DECLARATIONS)


@pytest.mark.parametrize("missing", ["groupCover", "evaluationGroupHom", "dilationGroupEquiv",
                                     "actual_tuple_hides", "highestGroup_central", "PolynomialGroupLaw"])
def test_omitting_operational_constructor_or_boundary_is_rejected(missing):
    names = [name for name in bridge.DECLARATIONS if name != bridge.PREFIX+missing]
    with pytest.raises(ValueError, match="incomplete"):
        base.parse_axioms(diagnostics(names), bridge.DECLARATIONS)


@pytest.mark.parametrize("axiom", ["sorryAx", "AssumedCoverHomomorphism", "AssumedBCHTheorem"])
def test_unapproved_axioms_do_not_replace_the_bridge(axiom):
    with pytest.raises(ValueError, match="unapproved axiom"):
        base.parse_axioms(diagnostics(bridge.DECLARATIONS, axiom), bridge.DECLARATIONS)


def test_changed_base_is_not_silently_reblessed():
    bridge.validate_base_record({"theorem_count": 75}, {"theorem_count": 75})
    with pytest.raises(ValueError, match="frozen receipt"):
        bridge.validate_base_record({"theorem_count": 74}, {"theorem_count": 75})


def test_axiom_audit_does_not_erase_mathematical_hypotheses():
    scope = bridge.scope_report()
    assert scope["base_polynomial_group_law_is_explicit_hypothesis"]
    assert scope["cover_group_maps_are_constructed_not_assumed"]
    for name in ("base_lazard_bch_theorem_formalized", "graded_quotient_chain_formalized",
                 "efficient_cancellation_implemented", "formalizes_full_Rees_algorithm",
                 "quantum_execution", "new_algorithm_or_novelty_claim"):
        assert not scope[name]
