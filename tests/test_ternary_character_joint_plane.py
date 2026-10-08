import copy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from ternary_character_joint_plane import REPORT, SOURCE_REPORT, audit_joint_planes, complete_order_three_planes, mix_with_identity
from ternary_character_sdp_decoder import character_matrix
from ternary_character_sdp_gap_certificate import quantized_witness


@pytest.mark.parametrize("q", [3, 9, 27])
def test_all_genuine_sectors_pass_joint_laws_at_growing_ambient_root(q):
    nodes = tuple((q//3*x, q//3*y) for x, y in product(range(3), repeat=2))
    description = complete_order_three_planes(nodes, q)
    assert description["complete_planes"] == 1 and description["joint_laws_checked"] == 9
    model = {"nodes": nodes, "dimension": 2, "modulus": q, "matrix_nodes": 9}
    for s in product(range(3), repeat=2):
        witness = quantized_witness(model, character_matrix(model, s))
        certificate = {"seed": 0, "nodes": nodes, "modulus": q, "witness": witness,
                       "cyclic_feasibility": {"all_complete_cyclic_laws_exactly_nonnegative": True}}
        audit = audit_joint_planes(certificate)
        assert audit["negative_joint_laws_certified"] == 0
        assert audit["exact_reality_and_normalization"]
        assert Fraction(audit["minimum_joint_probability_lower_exact"]) >= 0


def test_missing_plane_moments_are_not_invented_and_caps_fail_whole_scan():
    axes = ((0, 0), (1, 0), (2, 0))
    assert complete_order_three_planes(axes, 3)["complete_planes"] == 0
    full = tuple(product(range(3), repeat=3))
    assert complete_order_three_planes(full, 3, max_pairs=1)["status"] == "ORDER_THREE_PLANE_PAIR_CAP_EXHAUSTED"
    assert complete_order_three_planes(full, 3, max_planes=1)["status"] == "ORDER_THREE_PLANE_COUNT_CAP_EXHAUSTED"
    with pytest.raises(ValueError, match="positive whole"):
        complete_order_three_planes(full, 3, max_pairs=0)


def test_plane_basis_independence_and_coverage_in_F3_cube():
    nodes = tuple(product(range(3), repeat=3))
    description = complete_order_three_planes(nodes, 3)
    assert description["represented_order_three_lines"] == 13
    assert description["complete_planes"] == 13
    assert description["incomplete_spanned_planes"] == 0
    for plane in description["planes"]:
        assert len(set(plane["power_entries"])) == 9
        assert len(plane["generators"]) == 2


def test_live_survivors_have_joint_obstructions_despite_exact_cyclic_feasibility():
    report = json.loads(REPORT.read_text())
    parent = json.loads(SOURCE_REPORT.read_text())
    assert [c["negative_joint_laws_certified"] for c in report["controls"]] == [2, 1]
    assert [c["description"]["complete_planes"] for c in report["controls"]] == [243, 227]
    assert not report["accepted_speedup_candidate"]
    for c, p in zip(report["controls"], parent["certificates"]):
        assert p["cyclic_feasibility"]["all_complete_cyclic_laws_exactly_nonnegative"]
        assert int(p["strict_gap_lower_numerator"]) > 0
        assert Fraction(c["minimum_joint_probability_upper_exact"]) < 0
        assert not c["description"]["unrepresented_moments_added"]
        assert c["description"]["incomplete_spanned_planes"] > 0


def test_exact_convex_repair_satisfies_all_cuts_without_removing_the_gap():
    report = json.loads(REPORT.read_text())
    for c in report["all_joint_cuts_survivors"]:
        assert c["status"] == "EXACT_ALL_JOINT_PLANE_CUTS_CHARACTER_GAP"
        assert int(c["strict_gap_lower_numerator"]) > 0
        assert c["all_complete_joint_planes_exactly_nonnegative"]
        assert Fraction(c["joint_feasibility"]["minimum_joint_probability_lower_exact"]) > 0
        assert c["cyclic_feasibility"]["all_complete_cyclic_laws_exactly_nonnegative"]
        assert c["witness"]["identity_weight_numerator"] == 1
        assert c["witness"]["identity_weight_denominator"] == 4
        assert not c["witness"]["new_numerical_factor_or_solver_used"]
        assert not c["population_or_asymptotic_failure_claim"]


@pytest.mark.parametrize("weight", [(0, 4), (-1, 4), (4, 4), (5, 4), (1, 65537), (1.0, 4)])
def test_invalid_convexity_parameters_are_not_PSD_proofs(weight):
    with pytest.raises(ValueError, match="strict convex"):
        mix_with_identity({}, *weight)


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_joint_plane_crosscheck.js"


def test_independent_complete_plane_scan_and_exact_upstream_replay():
    output = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS"
    assert result["complete_order_three_planes"] == 470
    assert result["exact_joint_laws_checked"] == 4230
    assert result["exact_negative_joint_laws"] == 3
    assert result["exact_all_joint_cut_gaps"] == 2
    assert result["exact_mixed_probability_laws_checked"] == 25764


@pytest.mark.parametrize("mutation", ["scope", "source", "missing_plane", "basis", "upper", "count", "empty", "mixture", "mixed_gap", "mixed_law", "missing_survivor"])
def test_joint_law_tampering_is_rejected(tmp_path, mutation):
    report = copy.deepcopy(json.loads(REPORT.read_text()))
    c = report["controls"][0]
    if mutation == "scope":
        report["accepted_speedup_candidate"] = True
    elif mutation == "source":
        report["source_report_sha256"] = "0"*64
    elif mutation == "missing_plane":
        c["description"]["planes"].pop()
    elif mutation == "basis":
        c["description"]["planes"][0]["generators"][1] = c["description"]["planes"][0]["generators"][0]
    elif mutation == "upper":
        c["negative_joint_laws"][0]["joint_probability_upper_numerator"] = "0"
    elif mutation == "count":
        c["description"]["incomplete_spanned_planes"] -= 1
    elif mutation == "empty":
        report["controls"] = []
    elif mutation == "mixture":
        report["all_joint_cuts_survivors"][0]["witness"]["matrix_real_integer"][0][1] += 1
    elif mutation == "mixed_gap":
        report["all_joint_cuts_survivors"][0]["strict_gap_lower_numerator"] = "1"
    elif mutation == "mixed_law":
        report["all_joint_cuts_survivors"][0]["joint_feasibility"]["minimum_joint_probability_lower_exact"] = "1"
    else:
        report["all_joint_cuts_survivors"].pop()
    target = tmp_path/"tampered.json"
    target.write_text(json.dumps(report))
    output = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert output.returncode != 0
