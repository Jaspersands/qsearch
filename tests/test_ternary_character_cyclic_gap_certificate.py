import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from ternary_character_cyclic_gap_certificate import (
    CYCLIC_DERIVATION, CYCLIC_REPORT, ORIGINAL_GAP_REPORT, REPORT, exact_cyclic_feasibility,
)
from ternary_character_sdp_decoder import character_matrix, compile_model
from ternary_character_sdp_gap_certificate import quantized_witness
from ternary_covariant_noise import CovariantRecord


@pytest.mark.parametrize("q", [3, 9])
def test_true_character_mixtures_pass_every_exact_law_at_actual_orders(q):
    records = (CovariantRecord((1,), (2,), (0, 0), q),)
    model = compile_model(records)
    for secret in range(q):
        witness = quantized_witness(model, character_matrix(model, (secret,)))
        audit = exact_cyclic_feasibility(model["nodes"], q, witness)
        assert audit["all_complete_cyclic_laws_exactly_nonnegative"]
        assert audit["exact_reality_and_normalization_from_conjugate_powers"]
        assert audit["complete_cyclic_probabilities_exact_lower_checked"] > 0
        assert Fraction(audit["minimum_complete_cyclic_probability_lower_exact"]) >= 0


def test_old_feasible_SDP_points_fail_strengthened_exact_admission():
    old = json.loads(ORIGINAL_GAP_REPORT.read_text())
    for certificate in old["certificates"]:
        audit = exact_cyclic_feasibility(certificate["nodes"], certificate["modulus"], certificate["witness"])
        assert certificate["witness"]["PSD_certified"]
        assert not audit["all_complete_cyclic_laws_exactly_nonnegative"]
        assert Fraction(audit["minimum_complete_cyclic_probability_lower_exact"]) < 0


def test_invalid_exact_moment_records_do_not_enter_certificate():
    with pytest.raises(ValueError, match="exact integer"):
        exact_cyclic_feasibility(((0,), (1,), (2,)), 3, {
            "moment_scale": 16, "matrix_real_integer": [[16.0]*3]*3, "matrix_imag_integer": [[0]*3]*3})


def test_live_strengthened_gaps_pin_ancestry_and_charge_every_law():
    report = json.loads(REPORT.read_text())
    for field, path in (("cyclic_decoder_report_sha256", CYCLIC_REPORT), ("original_gap_report_sha256", ORIGINAL_GAP_REPORT),
                        ("cyclic_derivation_sha256", CYCLIC_DERIVATION)):
        assert report[field] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert not report["asymptotic_impossibility_or_speedup_claim"]
    assert not report["numerical_optimizer_reexecuted"] and not report["new_independent_experiment"]
    assert [c["seed"] for c in report["certificates"]] == [93017, 93018]
    for certificate in report["certificates"]:
        audit = certificate["cyclic_feasibility"]
        assert certificate["status"] == "EXACT_FINITE_SDP_CHARACTER_GAP"
        assert certificate["witness"]["PSD_certified"]
        assert int(certificate["strict_gap_lower_numerator"]) > 0
        assert audit["all_complete_cyclic_laws_exactly_nonnegative"]
        assert audit["complete_cyclic_probabilities_exact_lower_checked"] == audit["description"]["constraints"]
        assert Fraction(audit["minimum_complete_cyclic_probability_lower_exact"]) > 0
        assert not audit["global_cross_cycle_character_realizability_certified"]


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_cyclic_gap_certificate_crosscheck.js"


def test_independent_strengthened_primal_and_complete_census_replay():
    output = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS" and result["exact_strengthened_gaps"] == 2
    assert result["full_root_secrets_checked"] == 590490
    assert result["exact_complete_cyclic_probabilities_checked"] > 20000
    assert not result["numerical_eigenvalues_or_solver_status_trusted"]


@pytest.mark.parametrize("mutation", ["scope", "parent", "missing_cycle", "order", "minimum", "count", "reality", "factor", "census", "empty"])
def test_strengthened_certificate_tampering_is_rejected(tmp_path, mutation):
    report = copy.deepcopy(json.loads(REPORT.read_text()))
    c = report["certificates"][0]
    audit = c["cyclic_feasibility"]
    if mutation == "scope":
        report["asymptotic_impossibility_or_speedup_claim"] = True
    elif mutation == "parent":
        report["cyclic_decoder_report_sha256"] = "0"*64
    elif mutation == "missing_cycle":
        audit["description"]["groups"].pop()
    elif mutation == "order":
        audit["description"]["groups"][0]["order"] *= 3
    elif mutation == "minimum":
        audit["minimum_complete_cyclic_probability_lower_exact"] = "1"
    elif mutation == "count":
        audit["complete_cyclic_probabilities_exact_lower_checked"] -= 1
    elif mutation == "reality":
        c["witness"]["matrix_imag_integer"][0][0] = 1
    elif mutation == "factor":
        c["witness"]["factor_lower_triangle_integer"][0][0] = 2**25
    elif mutation == "census":
        c["character_census"]["secrets_checked"] -= 1
    else:
        report["certificates"] = []
    target = tmp_path/"tampered.json"
    target.write_text(json.dumps(report))
    output = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert output.returncode != 0
