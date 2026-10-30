import json

import pytest

import verify as v


def record(data, severity="information"):
    return json.dumps({"severity": severity, "data": data})


def test_foundational_axioms_and_multiline_diagnostic():
    output = record("'A' depends on axioms: [propext,\n Classical.choice, Quot.sound]")
    assert v.parse_axioms(output, ("A",)) == {"A": ["propext", "Classical.choice", "Quot.sound"]}


def test_axiom_free_statement_is_not_a_missing_record():
    assert v.parse_axioms(record("'A' does not depend on any axioms"), ("A",)) == {"A": []}


def test_complete_manifest_covers_lie_constructors_and_all_theorems():
    assert len(v.THEOREMS) == 75
    assert len(v.DECLARATIONS) == len(set(v.DECLARATIONS)) == 99
    assert v.LIE_PREFIX+"cover" in v.DECLARATIONS
    assert v.LIE_PREFIX+"evaluationHom" in v.DECLARATIONS
    assert v.DILATION_PREFIX+"dilationEquiv" in v.DECLARATIONS
    assert v.DILATION_PREFIX+"dilation_lie" in v.DECLARATIONS
    assert v.CENTRAL_PREFIX+"central_instrument" in v.DECLARATIONS
    assert v.CENTRAL_PREFIX+"CancellationCertificate" in v.DECLARATIONS
    output = "\n".join(record(f"'{name}' depends on axioms: [propext]")
                       for name in v.DECLARATIONS)
    assert set(v.parse_axioms(output)) == set(v.DECLARATIONS)


def test_omitting_constructor_audit_is_not_accepted():
    output = "\n".join(record(f"'{name}' depends on axioms: [propext]")
                       for name in v.THEOREMS)
    with pytest.raises(ValueError, match="incomplete"):
        v.parse_axioms(output)


def test_omitting_the_actual_automorphism_is_not_accepted():
    output = "\n".join(record(f"'{name}' depends on axioms: [propext]")
                       for name in v.DECLARATIONS if name != v.DILATION_PREFIX+"dilationEquiv")
    with pytest.raises(ValueError, match="incomplete"):
        v.parse_axioms(output)


def test_replacing_bracket_proof_with_an_axiom_is_not_accepted():
    output = "\n".join(record(f"'{name}' depends on axioms: "
                                + ("[AssumedDilationLie]" if name == v.DILATION_PREFIX+"dilation_lie" else "[propext]"))
                       for name in v.DECLARATIONS)
    with pytest.raises(ValueError, match="unapproved axiom"):
        v.parse_axioms(output)


def test_omitting_full_central_instrument_is_not_accepted():
    output = "\n".join(record(f"'{name}' depends on axioms: [propext]")
                       for name in v.DECLARATIONS if name != v.CENTRAL_PREFIX+"central_instrument")
    with pytest.raises(ValueError, match="incomplete"):
        v.parse_axioms(output)


def test_assumed_normalized_channel_cannot_replace_physical_proof():
    output = "\n".join(record(f"'{name}' depends on axioms: "
                                + ("[AssumedIdealChannel]" if name == v.CENTRAL_PREFIX+"central_instrument" else "[propext]"))
                       for name in v.DECLARATIONS)
    with pytest.raises(ValueError, match="unapproved axiom"):
        v.parse_axioms(output)


@pytest.mark.parametrize("output", [
    "",
    record("'A' depends on axioms: [sorryAx]"),
    record("'A' depends on axioms: [UnprovedReesTheorem]"),
    record("'B' depends on axioms: [propext]"),
    record("'A' depends on axioms: [propext]", "warning"),
    record("unknown import", "error"),
    record("'A' depends on axioms: [propext]")+"\n"+record("'A' depends on axioms: [propext]"),
    record("ordinary informational message"),
    "malformed json"
])
def test_audit_rejects_missing_or_untrusted_evidence(output):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        v.parse_axioms(output, ("A",))
