import argparse
from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest

from theorems.dcp_noise_matched_source import (
    CONTRACT_ID,
    PREMISES,
    build_report,
    first_level_census,
    product_source_certificate,
    replacement_actions,
    require_premises,
)
from qsearch import command_dcp_noise_matched_source


def test_build_report_structure_and_guardrails():
    report = build_report()
    assert report["contract_id"] == CONTRACT_ID
    assert report["status"] == "CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"
    assert report["accepted_speedup_candidate"] is False
    assert report["novelty_claim"] is False
    assert report["actual_natural_source_noise_certified"] is False
    assert report["external_theorem_review_complete"] is False
    assert report["source_quantum_preparations_executed"] == 0

    assert len(report["two_level_exact_censuses"]) == 2
    for census in report["two_level_exact_censuses"]:
        assert census["exact_joint_label_visibility_law_restored"] is True
        assert census["original_higher_labels_retained"] is False

    scope = report["scope"]
    assert scope["abstract_balanced_product_source_family_closed_under_this_channel"] is True
    assert scope["all_joint_natural_lattice_noise_models_covered"] is False
    assert scope["exponential_recursive_supply_or_visibility_loss_removed"] is False


def test_replacement_actions_validation_and_output():
    premises = dict(PREMISES)
    rec = replacement_actions(Fraction(3, 4), 2, 1, premises=premises)
    assert rec["paid_qubit_consumed_before_zero_coin"] is True
    assert rec["public_visibility_record_retained"] is True
    assert rec["unknown_preparation_inverse_used"] is False
    assert rec["hardware_backend_executed"] is False
    assert rec["visibility"] == {"denominator_binary_exponent": 2, "numerator_hex": "0x3"}
    assert rec["zero_label_coin_probability"] == {"denominator_binary_exponent": 2, "numerator_hex": "0x1"}

    # Premise mismatch
    bad_premises = dict(PREMISES)
    bad_premises["original_diagonal_is_flat"] = False
    with pytest.raises(ValueError, match="UNRESOLVED"):
        replacement_actions(Fraction(3, 4), 2, 1, premises=bad_premises)


def test_product_source_certificate_checks_correlation():
    premises = dict(PREMISES)
    counts = first_level_census()
    cert = product_source_certificate(counts, 8, Fraction(3, 4), premises=premises)
    assert cert["exact_joint_label_visibility_law_restored"] is True
    assert cert["output_modulus"] == 8

    # Correlated counts should raise ValueError
    correlated_counts = dict(counts)
    first_key = next(iter(correlated_counts))
    correlated_counts[first_key] += 1
    with pytest.raises(ValueError, match="correlated"):
        product_source_certificate(correlated_counts, 8, Fraction(3, 4), premises=premises)


def test_command_dcp_noise_matched_source_no_write(capsys):
    args = argparse.Namespace(no_write=True)
    ret = command_dcp_noise_matched_source(args)
    assert ret == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING"
    assert payload["abstract_noisy_source_closed"] is True
    assert payload["actual_natural_source_certified"] is False


def test_nodejs_crosscheck():
    js_path = Path("research/certificates/dcp_noise_matched_source_crosscheck.js")
    result = subprocess.run(["node", str(js_path)], capture_output=True, text=True, check=True)
    out = json.loads(result.stdout)
    assert out["status"] == "ok"
    assert out["exact_source_levels"] == 2
    assert out["actual_natural_source_noise_certified"] is False
