"""Tests for DCP shifted-box producer, equal-label heralding, and collective majority audit."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import dcp_collective_majority_purification_audit as M
from native_basis_lottery import _certificate_int


def stored():
    return json.loads(M.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/dcp_collective_majority_purification_audit_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=M.ROOT,
    )


def test_shifted_box_source_producer_matches_exact_balanced_bad_register_law():
    rep = stored()
    ctrls = rep["shifted_box_source_controls"]
    assert len(ctrls) == 3
    assert ctrls[0]["explicit_cell_intersection_verified"]
    assert ctrls[1]["explicit_cell_intersection_verified"]
    for c in ctrls:
        assert c["translation_symmetry_B0_equals_B1"]
        assert c["exact_bad_zero_conditional_probability"] == "1/2"
        p_good = Fraction(c["exact_good_register_probability"])
        p_bad = Fraction(c["exact_bad_register_probability"])
        assert p_good + p_bad == 1
        assert p_bad <= Fraction(c["additive_union_bad_probability_upper"])
        audit = c["produced_phase_density_audit"]
        assert audit["PRIVATE_density_zero_population"] == "1/2"
        assert Fraction(audit["PRIVATE_density_phase_visibility"]) == p_good
    with pytest.raises(ValueError):
        M.shifted_box_source_producer(4, (4,), 16, 3, "bad-shift")


def test_equal_label_collision_heralding_dichotomy():
    rep = stored()
    for h in rep["equal_label_heralding_controls"]:
        v1 = Fraction(h["left_visibility_v1"])
        v2 = Fraction(h["right_visibility_v2"])
        assert Fraction(h["product_visibility_v1_v2"]) == v1 * v2
        assert h["difference_branch_has_zero_label"]
        assert Fraction(h["difference_branch_X_plus_acceptance"]) == (1 + v1 * v2) / 2
        assert h["difference_branch_estimates_v1_v2_without_secret_s"]
        assert not h["difference_branch_carries_hidden_secret_information"]
        assert not h["postselecting_difference_branch_leaves_surviving_label_k_copy"]


@pytest.mark.parametrize("R,v", ((1, "1/2"), (3, "1/2"), (5, "1/3"), (7, "1/4"), (9, "1/5")))
def test_product_X_majority_vote_equals_collective_helstrom_optimum(R, v):
    res = M.exact_majority_vote_ledger(R, v)
    assert res["product_X_majority_equals_collective_Helstrom_optimum"]
    assert res["exact_majority_vote_success_probability"] == res["exact_collective_Helstrom_success_probability"]
    assert res["fidelity_chain_inequality_verified"]
    assert not res["entangling_collective_POVM_can_beat_X_majority_at_parity_label"]
    v_maj_sq = Fraction(res["v_maj_squared"])
    fvdg_sq = Fraction(res["fuchs_van_de_graaf_1_minus_fidelity_sq_upper"])
    lin_sq = Fraction(res["linear_R_v_squared_upper"])
    assert v_maj_sq <= fvdg_sq <= lin_sq
    with pytest.raises(ValueError):
        M.exact_majority_vote_ledger(4, "1/2")


def test_end_to_end_purified_lineage_profiles():
    rep = stored()
    profs = rep["end_to_end_purified_lineage_profiles"]
    assert len(profs) == 4
    for p in profs:
        copies = _certificate_int(p["minimum_odd_target_copies_by_fvdg_bound"])
        leaves_per = _certificate_int(p["disjoint_leaves_per_target_copy"])
        total_leaves = _certificate_int(p["minimum_total_disjoint_original_leaves"])
        assert copies % 2 == 1 and copies >= 1
        assert total_leaves == copies * leaves_per
        assert not p["collective_entangling_parity_readout_reduces_copy_requirement"]


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["shifted_box_controls"] == 3
    assert out["heralding_controls"] == 3
    assert out["majority_helstrom_controls"] == 5
    assert out["purified_lineage_profiles"] == 4
    assert out["full_dcp_solver_supplied"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "box-good-cells",
        "box-p-bad",
        "box-visibility",
        "herald-v-prod",
        "herald-diff-label",
        "herald-secret-flag",
        "maj-success",
        "maj-helstrom",
        "maj-fvdg",
        "prof-copies",
        "prof-total-leaves",
        "solver-claim",
        "no-go-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_box_heralding_and_majority_tampering(kind):
    p = deepcopy(stored())
    b0 = p["shifted_box_source_controls"][0]
    h0 = p["equal_label_heralding_controls"][0]
    m1 = p["collective_majority_helstrom_controls"][1]
    pr0 = p["end_to_end_purified_lineage_profiles"][0]

    if kind == "box-good-cells":
        b0["good_interior_pair_cells_G"] += 1
    elif kind == "box-p-bad":
        b0["exact_bad_register_probability"] = "0"
    elif kind == "box-visibility":
        b0["produced_phase_density_audit"]["PRIVATE_density_phase_visibility"] = "1"
    elif kind == "herald-v-prod":
        h0["product_visibility_v1_v2"] = "1"
    elif kind == "herald-diff-label":
        h0["difference_branch_z1"]["output_audit"]["measured_Fourier_label"] = 1
    elif kind == "herald-secret-flag":
        h0["difference_branch_carries_hidden_secret_information"] = True
    elif kind == "maj-success":
        m1["exact_majority_vote_success_probability"] = "1"
    elif kind == "maj-helstrom":
        m1["exact_collective_Helstrom_success_probability"] = "1"
    elif kind == "maj-fvdg":
        m1["fuchs_van_de_graaf_1_minus_fidelity_sq_upper"] = "0"
    elif kind == "prof-copies":
        pr0["minimum_odd_target_copies_by_fvdg_bound"] = 1
    elif kind == "prof-total-leaves":
        pr0["minimum_total_disjoint_original_leaves"] = 1
    elif kind == "solver-claim":
        p["full_bad_register_dcp_solver_supplied"] = True
    elif kind == "no-go-claim":
        p["general_dcp_or_dhsp_no_go_claimed"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["dcp_physical_bad_register_lineage.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
