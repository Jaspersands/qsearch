from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import subprocess

import pytest

from ternary_continuous_loop_certificate import (
    DERIVATION, PARENT, REPORT, NODES, discover_certificate,
    fixed_function_control, sharpened_envelope, verify_certificate,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.fixture(scope="module")
def parent():
    return json.loads(PARENT.read_text())


def loop_coefficients(parent, i):
    return {(a["beta1_exponent"], a["beta2_exponent"]):
            int(a["coefficient_numerator_over81"]) for a in
            parent["signed_transfer_structure_certificate"]["all_self_loop_Laurent_coefficients"][i]["Laurent_coefficients"]}


@pytest.mark.parametrize("i", range(137))
def test_every_complete_native_self_loop_has_an_exact_positive_sos(parent, artifact, i):
    record = artifact["loop_certificates"][i]
    assert record["state"] == i
    assert verify_certificate(loop_coefficients(parent, i), record["certificate"])


def test_nontrivial_negative_coefficient_loop_can_be_certified_exactly(parent):
    c = loop_coefficients(parent, 136)
    assert any(v < 0 for v in c.values())
    r = discover_certificate(c)
    assert r["status"] == "EXACT_TORUS_SOS"
    assert verify_certificate(c, r)


def test_unknown_is_not_a_proof_and_a_counterexample_does_not_get_accepted():
    # At zero angle this polynomial equals81, but at z=-1 its modulus is83.
    c = {(1, 0): 82, (0, 0): -1}
    r = discover_certificate(c)
    assert r["status"] == "CERTIFICATE_SEARCH_UNKNOWN"
    with pytest.raises(ValueError):
        verify_certificate(c, r)


def test_constant_unit_loop_requires_no_fake_positive_squares():
    r = discover_certificate({(0, 0): 81})
    assert r == {"status": "EXACT_TORUS_SOS", "squares": []}
    assert verify_certificate({(0, 0): 81}, r)


@pytest.mark.parametrize("mutation", ["negative", "coefficient", "missing", "boolean", "nonzero_sum"])
def test_exact_identity_rejects_bad_or_incomplete_square_certificates(artifact, parent, mutation):
    r = deepcopy(artifact["loop_certificates"][136]["certificate"])
    if mutation == "negative":
        r["squares"][0]["weight"] = "-1"
    elif mutation == "coefficient":
        r["squares"][0]["integer_coefficients"][0] += 1
        r["squares"][0]["integer_coefficients"][1] -= 1
    elif mutation == "missing":
        r["squares"].pop()
    elif mutation == "boolean":
        r["squares"][0]["integer_coefficients"][0] = True
    else:
        r["squares"][0]["integer_coefficients"][0] += 1
    with pytest.raises(ValueError):
        verify_certificate(loop_coefficients(parent, 136), r)


def test_large_polynomial_batch_no_longer_evades_continuous_template_bound():
    from ternary_two_layer_path_transfer import family_envelopes
    old = family_envelopes(128, 243, 12800)
    r = sharpened_envelope(128, 243, 12800)
    assert old["all_fixed_continuous_angles_uniform_success_upper"] == "1"
    assert Fraction(r["all_fixed_continuous_angles_uniform_success_upper"]) < Fraction(1, 2**900)
    assert Fraction(r["public_adaptive_four_angle_uniform_success_upper"]) < Fraction(1, 2**160)
    assert r["label_trained_coordinate_angles_or_residual_functions_not_covered"]
    assert r["adaptive_four_angle_bound_requires_original_mismatch_cost_template"]


def test_born_correction_is_not_an_unconditional_copy_count_lower_bound():
    r = sharpened_envelope(128, 243, 1)
    assert Fraction(r["all_fixed_continuous_angles_uniform_success_upper"]) < Fraction(1, 2**900)
    assert r["all_fixed_continuous_angles_Born_success_upper"] == "1"
    assert r["Born_decay_depends_on_original_input_count"]


@pytest.mark.parametrize("i", range(3))
def test_complete_arbitrary_residual_phase_law_and_coordinate_schedule(artifact, i):
    r = artifact["complete_fixed_function_native_controls"][i]
    new = fixed_function_control(r["dimension"], int(r["modulus"]),
        tuple(r["coordinate_beta1_quarters"]), tuple(r["coordinate_beta2_quarters"]),
        tuple(r["full_root_phase1_quarters"]), tuple(r["full_root_phase2_quarters"]))
    assert new == r
    assert new["actual_direct_circuit_uniform_mean_exact"] == new["arbitrary_residual_lattice_transfer_mean_exact"]


def test_phase_tables_are_genuinely_full_group_and_not_coordinate_separable(artifact):
    r = artifact["complete_fixed_function_native_controls"][0]
    f = r["full_root_phase1_quarters"]
    assert (f[4]-f[3]-f[1]+f[0]) % 4 != 0
    r = artifact["complete_fixed_function_native_controls"][1]
    assert len(set(r["coordinate_beta1_quarters"])) == 2


def test_capped_census_rejects_bad_dimensions_and_never_returns_partial_law():
    with pytest.raises(ValueError):
        fixed_function_control(1, 3, (1,), (3,), (0, 1), (0, 1, 2))
    with pytest.raises(ValueError):
        fixed_function_control(1, 9, (1, 1, 1), (3, 3, 3), (0,)*9, (0,)*9)


def test_upstream_hashes_and_unsupported_claims(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert artifact["parent_artifact_sha256"] == hashlib.sha256(PARENT.read_bytes()).hexdigest()
    assert artifact["polynomial_monomials"] == [list(v) for v in NODES]
    assert artifact["all_continuous_self_loop_moduli_at_most_one"]
    assert not any(artifact[k] for k in (
        "general_mixer_or_deeper_circuit_lower_bound", "quantum_speedup_proved",
        "candidate_record_accepted", "novelty_claim"))


CHECKER = "research/certificates/ternary_continuous_loop_certificate_crosscheck.js"


def test_independent_exact_polynomial_checker():
    r = subprocess.run(["node", CHECKER], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["continuous_loops"] == 137


@pytest.mark.parametrize("case", ["sign", "square", "missing", "scope", "mean", "control", "parent"])
def test_independent_checker_rejects_tampered_evidence(artifact, tmp_path, case):
    r = deepcopy(artifact)
    if case == "sign":
        r["loop_certificates"][136]["certificate"]["squares"][0]["weight"] = "-1"
    elif case == "square":
        v = r["loop_certificates"][136]["certificate"]["squares"][0]["integer_coefficients"]
        v[0] += 1; v[1] -= 1
    elif case == "missing":
        r["loop_certificates"].pop()
    elif case == "scope":
        r["sharpened_population_envelopes"][-1]["label_trained_coordinate_angles_or_residual_functions_not_covered"] = False
    elif case == "mean":
        r["sharpened_population_envelopes"][-1]["all_fixed_continuous_angles_uniform_success_upper"] = "0"
    elif case == "control":
        r["complete_fixed_function_native_controls"][0]["arbitrary_residual_lattice_transfer_mean_exact"] = "0"
    else:
        r["parent_artifact_sha256"] = "incorrect"
    p = tmp_path/"bad.json"
    p.write_text(json.dumps(r))
    result = subprocess.run(["node", CHECKER, str(p)], capture_output=True, text=True)
    assert result.returncode != 0
