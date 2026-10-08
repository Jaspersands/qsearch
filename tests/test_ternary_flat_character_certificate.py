from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from ternary_covariant_noise import CovariantRecord
from ternary_flat_character_certificate import (
    Cyclotomic, DERIVATION, NEGATIVE_SOURCE, REPORT, ResourceLimit,
    _pi_interval, compile_layout, mixture_matrix, native_nonextension_controls,
    positive_weight_certificate, round_harmonic_score, verify_certificate,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


def records(c):
    return tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                 for r in c["records"])


def check(c, original=None, extension=None, **kwargs):
    return verify_certificate(records(c), c["layout"]["base_frequencies"],
                              c["original_moment_matrix"] if original is None else original,
                              c["extension_moment_matrix"] if extension is None else extension, **kwargs)


@pytest.mark.parametrize("index", [0, 1])
def test_exact_native_flat_certificate_recovers_atoms_without_truth_input(artifact, index):
    c = artifact["native_controls"][index]
    verified = check(c)
    assert json.loads(json.dumps(verified)) == c["verification"]
    assert verified["character_distribution_certified"]
    assert verified["PSD_certified_by_positive_character_reconstruction"]
    assert verified["rank_original_exact"] == verified["rank_extension_exact"] == 3
    assert len(verified["character_atoms"]) == 3
    assert not verified["floating_PSD_or_rank_tolerance_used"]
    assert not verified["classical_completion_algorithm_supplied"]
    assert not verified["native_noisy_recovery_proved"]
    assert verified["input_max_rational_coefficient_bits"] > 0
    assert verified["retained_coordinate_operator_atom_max_coefficient_bits"] > 0
    assert verified["classical_extension_compact_JSON_bytes"] == len(json.dumps(c["extension_moment_matrix"], separators=(",", ":")))
    assert not verified["all_internal_intermediate_bit_costs_certified"]


def test_exact_nonrational_weight_positivity_and_native_extraction(artifact):
    c = artifact["nonrational_positive_weight_countercontrol"]
    verified = check(c)
    assert verified["character_distribution_certified"]
    assert verified["rank_extension_exact"] == 2
    for a in verified["character_atoms"]:
        sign = a["positive_weight_certificate"]
        assert sign["interval_uses_only_exact_rational_arithmetic"]
        assert Fraction(sign["lower"]) > 0
        assert sign["Machin_arctangent_terms"] == sign["cosine_Taylor_terms"]


@pytest.mark.parametrize("q", [3, 9, 27, 81])
def test_cyclotomic_root_retains_entire_prime_power(q):
    f = Cyclotomic(q)
    assert f.z**q == f.K.one
    assert f.z**(q//3) != f.K.one
    assert f.degree == 2*q//3
    assert f.conjugate(f.z) == f.powers[-1]
    assert f.decode(f.encode(f.z**(q-1)+f.K.convert(Fraction(1, 7)))) == f.z**(q-1)+f.K.convert(Fraction(1, 7))


@pytest.mark.parametrize("bad", [1, 5, 9.0, True])
def test_cyclotomic_schema_does_not_accept_a_wrong_root_or_numeric_type(bad):
    with pytest.raises(ValueError):
        Cyclotomic(bad)


@pytest.mark.parametrize("raw", [[1], ["0"], ["0", "1"], ["0.5"], ["2/4"]])
def test_exact_input_rejects_floats_and_noncanonical_polynomial_coefficients(raw):
    f = Cyclotomic(9)
    with pytest.raises(ValueError):
        f.decode(raw)


def test_algebraic_sign_unknown_and_negative_are_not_promoted_to_PSD():
    f = Cyclotomic(9)
    p = (f.K.convert(2)+f.z+f.powers[-1])/f.K.convert(4)
    assert positive_weight_certificate(f, p)["status"] == "POSITIVE"
    assert positive_weight_certificate(f, -p)["status"] == "NEGATIVE"
    assert positive_weight_certificate(f, p, max_terms=0)["status"] == "UNKNOWN_ALGEBRAIC_WEIGHT_SIGN"
    assert positive_weight_certificate(f, f.z)["status"] == "REJECTED_NONREAL_CHARACTER_WEIGHT"
    assert positive_weight_certificate(f, f.K.zero)["status"] == "ZERO"


def test_rational_Machin_identity_and_alternating_interval_nesting():
    a = Fraction(1, 5)
    a2 = 2*a/(1-a*a)
    a4 = 2*a2/(1-a2*a2)
    b = Fraction(1, 239)
    assert a4 == Fraction(120, 119)
    assert (a4-b)/(1+a4*b) == 1
    lo, hi = _pi_interval(8)
    lo2, hi2 = _pi_interval(16)
    assert lo < lo2 < hi2 < hi
    assert Fraction(314, 100) < lo < hi < Fraction(22, 7)


@pytest.mark.parametrize("index", [0, 1])
def test_compiled_translation_layout_retains_every_native_frequency_and_integer_loop(artifact, index):
    c = artifact["native_controls"][index]
    layout = compile_layout(records(c))
    assert json.loads(json.dumps(layout)) == c["layout"]
    q = c["records"][0]["modulus"]
    assert all(x["integer_multiplier"] == q and x["endpoint_offset"] == 0 for x in layout["basis_q_loops"])
    assert all(layout["offsets"][t["endpoint_offset"]] == layout["base_frequencies"][t["base_frequency_index"]] for t in layout["base_targets"])
    assert layout["dense_classical_moment_entries"] == len(layout["extension_frequencies"])**2


def test_unit_rank_failure_stays_unknown():
    r = (CovariantRecord((1, 0), (1, 0), (0, 0), 9),)
    assert compile_layout(r)["status"] == "UNKNOWN_NO_FULL_UNIT_DIFFERENCE_BASIS"


def test_whole_object_caps_cannot_accept_a_truncated_matrix(artifact):
    c = artifact["native_controls"][0]
    with pytest.raises(ResourceLimit):
        compile_layout(records(c), max_offsets=2)
    with pytest.raises(ResourceLimit):
        compile_layout(records(c), max_nodes=5)
    with pytest.raises(ResourceLimit):
        compile_layout(records(c), max_entries=10)
    assert check(c, max_nodes=5)["status"] == "UNKNOWN_RESOURCE_LIMIT"
    assert check(c, max_field_degree=2)["status"] == "UNKNOWN_RESOURCE_LIMIT"


def test_original_moment_block_cannot_be_replaced_to_get_flatness(artifact):
    c = artifact["native_controls"][0]
    original = deepcopy(c["original_moment_matrix"])
    original[0][0] = ["1/2"]
    result = check(c, original=original)
    assert result["status"] == "REJECTED_EXACT_CERTIFICATE"
    assert "changed the retained" in result["issues"][0]


def test_equal_difference_and_Hermiticity_are_not_just_checked_at_the_anchor(artifact):
    c = artifact["native_controls"][0]
    raw = deepcopy(c["extension_moment_matrix"])
    raw[-1][-2] = ["1/7"]
    raw[-2][-1] = ["1/7"]
    result = check(c, extension=raw)
    assert result["status"] == "REJECTED_EXACT_CERTIFICATE"
    assert not result["character_distribution_certified"]


def test_nonflat_PSD_character_distribution_is_not_called_nonrepresentable(artifact):
    c = artifact["native_controls"][0]
    N, V = len(c["layout"]["extension_frequencies"]), len(c["layout"]["base_frequencies"])
    original = [[["1"] if i == j else [] for j in range(V)] for i in range(V)]
    extension = [[["1"] if i == j else [] for j in range(N)] for i in range(N)]
    result = check(c, original=original, extension=extension)
    assert result["status"] == "REJECTED_EXACT_CERTIFICATE"
    assert "not flat" in result["issues"][0]
    assert "CHARACTER_DISTRIBUTION_SATURATION" not in result["status"]


@pytest.mark.parametrize("nonrational", [False, True])
def test_flat_indefinite_signed_character_mixture_cannot_fake_PSD(artifact, nonrational):
    c = artifact["native_controls"][0]
    f = Cyclotomic(9)
    p = -(f.K.convert(2)+f.z+f.powers[-1])/f.K.convert(4) if nonrational else -f.K.convert(Fraction(1, 2))
    atoms = (((0, 0), f.K.one-p), ((1, 3), p))
    M = mixture_matrix(f, c["layout"]["extension_frequencies"], atoms)
    old = M.extract(c["layout"]["original_block_indices"], c["layout"]["original_block_indices"])
    result = check(c, original=f.encode_matrix(old), extension=f.encode_matrix(M))
    assert result["status"] == "REJECTED_NONPOSITIVE_CHARACTER_WEIGHT"
    assert result["issues"][0]["sign"]["status"] == "NEGATIVE"


def test_existing_native_nonextension_falsifiers_reject_before_resource_caps(artifact):
    controls = native_nonextension_controls()
    assert json.loads(json.dumps(controls)) == artifact["native_nonextension_controls"]
    for c in controls:
        assert c["verification"]["status"] == "REJECTED_CHARACTER_DISTRIBUTION_SATURATION"
        assert not c["verification"]["character_distribution_certified"]
        assert c["saturation_guard_runs_before_extension_construction"]


def test_extraction_is_outcome_blind_but_rounding_uses_actual_outcomes(artifact):
    c = artifact["native_controls"][0]
    changed = tuple(CovariantRecord(r.first, r.second, (2, 3), r.modulus) for r in records(c))
    result = verify_certificate(changed, c["layout"]["base_frequencies"], c["original_moment_matrix"], c["extension_moment_matrix"])
    assert json.loads(json.dumps(result)) == c["verification"]
    rounded = round_harmonic_score(changed, result)
    assert rounded["status"] == "CLASSICAL_CHARACTER_DOMINATES_VERIFIED_NATIVE_HARMONIC_SCORE"
    assert rounded["selected_score"] != c["harmonic_score_rounding"]["selected_score"]
    assert not rounded["held_out_native_prediction_verified"]
    assert not rounded["native_log_likelihood_is_this_score"]


def test_rounding_requires_a_verified_distribution():
    r = (CovariantRecord((1,), (2,), (0, 0), 9),)
    with pytest.raises(ValueError, match="verified positive"):
        round_harmonic_score(r, {"character_distribution_certified": False})


def test_live_artifact_has_no_decoder_or_quantum_claim_and_pins_sources(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert artifact["native_nonextension_source_sha256"] == hashlib.sha256(NEGATIVE_SOURCE.read_bytes()).hexdigest()
    for key in ("completion_solver_implemented", "approximate_flatness_proved", "native_noisy_decoder_supplied", "quantum_speedup_proved", "candidate_record_accepted"):
        assert not artifact[key]


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_flat_character_certificate_crosscheck.js"


def test_independent_cyclotomic_character_reconstruction_checker():
    p = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    r = json.loads(p.stdout)
    assert r["status"] == "PASS"
    assert r["exact_cyclotomic_moment_entries"] == 11436
    assert r["positive_character_atoms"] == 8
    assert r["nonrational_weight_intervals"] == 2
    assert r["retained_native_nonextension_falsifiers"] == 3
    assert not r["native_noisy_decoder_supplied"]


@pytest.mark.parametrize("mutation", ["moment", "original", "weight", "secret", "rank", "loop", "trace", "sign", "rounding", "source", "claim"])
def test_independent_checker_rejects_forged_flat_distribution_artifacts(tmp_path, mutation, artifact):
    r = deepcopy(artifact)
    c = r["native_controls"][0]
    if mutation == "moment":
        c["extension_moment_matrix"][-1][-1] = ["1/2"]
    elif mutation == "original":
        c["original_moment_matrix"][0][0] = ["1/2"]
    elif mutation == "weight":
        c["verification"]["character_atoms"][0]["weight"] = ["1/3"]
    elif mutation == "secret":
        c["verification"]["character_atoms"][0]["secret"][0] += 1
    elif mutation == "rank":
        c["verification"]["rank_extension_exact"] += 1
    elif mutation == "loop":
        c["layout"]["basis_q_loops"][0]["integer_multiplier"] = 3
    elif mutation == "trace":
        c["layout"]["addition_trace"].pop()
    elif mutation == "sign":
        r["nonrational_positive_weight_countercontrol"]["verification"]["character_atoms"][0]["positive_weight_certificate"]["lower"] = "1"
    elif mutation == "rounding":
        c["harmonic_score_rounding"]["mixture_score"] = ["1"]
    elif mutation == "source":
        c["original_ring_labels"][0][0][0] += 1
    elif mutation == "claim":
        c["verification"]["native_noisy_recovery_proved"] = True
    target = tmp_path/"corrupt.json"
    target.write_text(json.dumps(r))
    p = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert p.returncode != 0
