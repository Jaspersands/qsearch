"""Pytest suite for `theorems/planted_qary_classical_attack_threshold_bridge.py`."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from itertools import product
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.planted_qary_classical_attack_threshold_bridge import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_free_support_and_classical_attacks,
    build_planted_qary_classical_attack_threshold_bridge_report,
    projective_free_coordinate_rref_search,
    determinant_gap_counterfamily,
    exact_reducedness,
    lll_alpha,
)
from theorems.planted_qary_usvp_source import canonical_sign, generate_source, PublicQaryLattice


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = (
    ROOT
    / "research"
    / "certificates"
    / "planted_qary_classical_attack_threshold_bridge_crosscheck.js"
)


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "planted-qary-classical-attack-threshold-bridge-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("n", "m", "q", "support", "seed"),
    [
        (4, 2, 257, 3, 11),
        (6, 3, 1009, 4, 17),
        (8, 4, 65537, 6, 23),
        (10, 6, 1000003, 8, 29),
    ],
)
def test_projective_free_coordinate_rref_search_recovers_plant_with_exact_state_count(
    n: int, m: int, q: int, support: int, seed: int
) -> None:
    gen = generate_source(
        n=n,
        m=m,
        q=q,
        gap=2,
        support=support,
        plant_seed=seed,
        matrix_seed=seed + 400,
    )
    res = projective_free_coordinate_rref_search(gen.problem)
    assert res["projective_free_states_checked"] == (3 ** (n - m) - 1) // 2
    assert res["projective_free_states_checked"] < res["ambient_mitm_states"]
    assert tuple(res["recovered_vector"]) == canonical_sign(gen.private.plant)


def test_classical_attack_thresholds_and_free_support_bounds() -> None:
    rows = audit_free_support_and_classical_attacks()
    assert len(rows) == 6
    for row in rows:
        assert row["free_support_within_sharp_bounds"] is True
        assert row["sparse_column_immune_at_s_ge_3"] is True
        assert row["public_lll_recovered_planted_vector"] is True
        assert row["projective_rref_recovered_planted_vector"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_planted_qary_classical_attack_threshold_bridge_report()
    assert all(report["verification"].values())
    assert ARTIFACT_PATH.exists()
    saved = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert saved == report

    proc = subprocess.run(
        ["node", str(CROSSCHECK_JS)],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"
    assert payload["instances_verified"] == 6


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "theorems.planted_qary_classical_attack_threshold_bridge",
            "--no-write",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "planted_qary_classical_attack_threshold_bridge"
    assert all(out["verification"].values())


def test_correct_LLL_constant_and_exact_returned_basis_certificate():
    assert lll_alpha(Fraction(3,4)) == 2
    assert lll_alpha(Fraction(3,4), Fraction(51,100)) == Fraction(10000,4899)
    assert lll_alpha(Fraction(1)) == Fraction(4,3)
    valid = exact_reducedness(((1,0),(0,1)))
    assert valid["lovasz_verified"] and valid["size_reduction_verified"]
    assert exact_reducedness(((1,0),(2,1)))["size_reduction_verified"] is False
    assert exact_reducedness(((2,0),(0,1)))["lovasz_verified"] is False
    with pytest.raises(ValueError): exact_reducedness(((1,0),(2,0)))
    with pytest.raises(ValueError): exact_reducedness(((1,0,0),(0,1,0)))


@pytest.mark.parametrize("delta,eta", [(Fraction(1,4),Fraction(1,2)),(True,Fraction(1,2)),(0.75,Fraction(1,2)),(1,Fraction(1))])
def test_invalid_or_rounded_LLL_parameters_rejected(delta,eta):
    with pytest.raises(ValueError): lll_alpha(delta,eta)


def test_determinant_counterfamily_has_unique_plant_but_fixed_successive_gap():
    family = determinant_gap_counterfamily()
    u,v = family["ordinary_integer_kernel_basis"]
    assert sum(a*b for a,b in zip(u,v)) == 0
    for row in family["controls"]:
        P = row["public_problem"]
        problem = PublicQaryLattice(P["prime"],P["H"])
        small = [x for x in product(range(-2,3),repeat=5)
                 if 0 < sum(a*a for a in x) <= 5 and problem.member(x)]
        assert {sum(a*a for a in x) for x in small} == {4,5}
        shortest = {x for x in small if sum(a*a for a in x)==4}
        assert shortest == {tuple(u),tuple(-a for a in u)}
        assert problem.prime**2 > family["maximum_constraint_row_squared_norm"]*family["proof_radius_squared"]
        assert row["lambda1_squared"] == 4 and row["lambda2_squared"] == 5
    assert len({row["determinant"] for row in family["controls"]}) == 4
    assert family["determinant_growth_proves_successive_gap_growth"] is False


def test_polynomial_not_constant_space_and_unknown_enumeration_cap():
    gen = generate_source(n=6,m=3,q=1009,gap=2,support=4,plant_seed=17,matrix_seed=417)
    result = projective_free_coordinate_rref_search(gen.problem)
    assert result["constant_working_space"] is False
    assert result["auxiliary_table_entries_stored"] == 0
    with pytest.raises(ValueError,match="UNKNOWN"):
        projective_free_coordinate_rref_search(gen.problem,max_states=1)


def test_finite_recovery_does_not_promote_isolation_or_monotonicity():
    report = build_planted_qary_classical_attack_threshold_bridge_report()
    assert all(value is False for value in report["unresolved_or_withdrawn_claims"].values())
    for row in report["classical_attack_threshold_audit"]:
        assert row["lambda2_isolation_premise_verified"] is False
        assert row["LLL_reducedness_certificate"]["actual_lambda2_certified"] is False
        assert "lll_theoretical_norm_sq_ceiling_alpha_4_3" not in row
    assert isinstance(report["classical_attack_threshold_audit"][-1]["q"],str)
    assert int(report["classical_attack_threshold_audit"][-1]["q"]) > 2**80


@pytest.mark.parametrize("mutation",["H","LLL","transform","constant","RREF","prime","lambda2","counterfamily"])
def test_independent_checker_rejects_actual_mathematical_tampering(tmp_path,mutation):
    report = deepcopy(build_planted_qary_classical_attack_threshold_bridge_report())
    row = report["classical_attack_threshold_audit"][0]
    if mutation == "H": row["public_problem"]["H"][0][0] += 1
    elif mutation == "LLL": row["public_LLL_vector"] = [0]*row["n"]
    elif mutation == "transform": row["public_LLL_unimodular_transform"][0][0] += 1
    elif mutation == "constant": report["LLL_parameter_arithmetic"]["delta_3_4_eta_1_2_alpha"] = {"numerator":"4","denominator":"3"}
    elif mutation == "RREF": row["projective_RREF_vector"] = [0]*row["n"]
    elif mutation == "prime": row["public_problem"]["prime_certificate"]["witness"] = 1
    elif mutation == "lambda2": row["lambda2_isolation_premise_verified"] = True
    else: report["determinant_growth_counterfamily"]["controls"][0]["lambda2_squared"] = 6
    target = tmp_path / "certificate.json"
    target.write_text(json.dumps(report))
    done = subprocess.run(["node",str(CROSSCHECK_JS),str(target)],capture_output=True,text=True)
    assert done.returncode != 0
