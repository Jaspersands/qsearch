"""Fail-closed controls for the scoped proof receipt, not tests of Lean's kernel."""

import json

import pytest

import verify


def diagnostic(name, axioms="propext, Classical.choice, Quot.sound"):
    return json.dumps({"severity": "information",
                       "data": f"'{name}' depends on axioms: [{axioms}]"})


def output():
    return "\n".join(diagnostic(name) for name in verify.DECLARATIONS)


def test_complete_audit():
    records = verify.parse_axioms(output())
    assert len(records) == 29
    assert set(records) == set(verify.DECLARATIONS)


def test_axiom_free_declaration():
    name = verify.DECLARATIONS[0]
    replacement = json.dumps({"severity": "information",
                              "data": f"'{name}' does not depend on any axioms"})
    assert verify.parse_axioms(output().replace(diagnostic(name), replacement))[name] == []


@pytest.mark.parametrize("fault", ["missing", "duplicate", "unknown", "custom_axiom",
                                   "sorry", "warning", "error", "unexpected", "bad_json"])
def test_bad_audit_rejected(fault):
    rows = output().splitlines()
    name = verify.DECLARATIONS[0]
    if fault == "missing":
        rows.pop()
    elif fault == "duplicate":
        rows.append(rows[0])
    elif fault == "unknown":
        rows.append(diagnostic("QSearch.Unknown.proof"))
    elif fault in ("custom_axiom", "sorry"):
        rows[0] = diagnostic(name, "UnprovedAssumption" if fault == "custom_axiom" else "sorryAx")
    elif fault in ("warning", "error"):
        rows.append(json.dumps({"severity": fault, "data": "diagnostic"}))
    elif fault == "unexpected":
        rows.append(json.dumps({"severity": "information", "data": "not an axiom report"}))
    else:
        rows.append("not JSON")
    with pytest.raises(ValueError):
        verify.parse_axioms("\n".join(rows))


def test_source_and_audit_manifest():
    verify.validate_declarations((verify.ROOT / "ExteriorCompression.lean").read_text())
    assert (verify.ROOT / "Audit.lean").read_text() == verify.expected_audit()
    assert len(verify.THEOREMS) == 21
    assert len(verify.DEFINITIONS) == 8


@pytest.mark.parametrize("mutation", ["missing", "extra", "lemma", "private", "instance",
                                     "duplicate", "axiom", "sorry", "unsafe"])
def test_changed_declaration_manifest_rejected(mutation):
    source = (verify.ROOT / "ExteriorCompression.lean").read_text()
    if mutation == "missing":
        source = source.replace("theorem shear_apply", "-- theorem shear_apply", 1)
    elif mutation == "extra":
        source += "\ntheorem not_audited : True := True.intro\n"
    elif mutation == "lemma":
        source += "\nlemma not_audited : True := True.intro\n"
    elif mutation == "private":
        source += "\nprivate def not_audited : Nat := 0\n"
    elif mutation == "instance":
        source += "\ninstance : Inhabited Nat := inferInstance\n"
    elif mutation == "duplicate":
        source += "\ntheorem shear_apply : True := True.intro\n"
    else:
        source += f"\n{mutation}\n"
    with pytest.raises(ValueError):
        verify.validate_declarations(source)


def test_arithmetic_source_tampering_rejected(tmp_path, monkeypatch):
    original = verify.ARITHMETIC
    receipt = json.loads((original / "receipt.json").read_text())
    (tmp_path / "receipt.json").write_bytes((original / "receipt.json").read_bytes())
    for name in receipt["source_hashes"]:
        (tmp_path / name).write_bytes((original / name).read_bytes())
    (tmp_path / "exterior_sde.py").write_text("changed source\n")
    monkeypatch.setattr(verify, "ARITHMETIC", tmp_path)
    monkeypatch.setattr(verify, "command", lambda args, cwd: verify.MATHLIB if "rev-parse" in args else "")
    with pytest.raises(ValueError, match="prior arithmetic source changed"):
        verify.verify()


def test_wrong_toolchain_rejected(tmp_path):
    (tmp_path / "lean-toolchain").write_text("leanprover/lean4:v0.0.0\n")
    with pytest.raises(ValueError, match="wrong Lean toolchain"):
        verify.verify(tmp_path)


def test_hashes_bind_exact_bytes(tmp_path):
    (tmp_path / "proof").write_bytes(b"proof\n")
    before = verify.hashes(tmp_path, ("proof",))
    (tmp_path / "proof").write_bytes(b"proof\n\n")
    assert before != verify.hashes(tmp_path, ("proof",))
