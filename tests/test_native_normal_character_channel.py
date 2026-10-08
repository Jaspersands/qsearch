from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from cyclotomic_rescaling_gate import multiply, pairing, reduce_element
from native_normal_character_channel import (
    ROOT, NormalCharacterChannel, conjugate_erase_control, precision_ledger, run_controls,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("r,c", [(4, 1), (5, 2), (6, 2), (6, 3), (7, 2)])
@pytest.mark.parametrize("copies", [1, 2, 3])
def test_deep_normal_channel_aliases_actual_integer_secret_digits(r, c, copies):
    delta = 3**((c+2)//2)
    labels = tuple(((j+1, j),) for j in range(copies))
    C = NormalCharacterChannel(r, c, labels)
    out = C.finite_control(((1, 0),), ((1+delta, 0),))
    assert out["exact_phase_difference_constant_within_each_class"]
    assert out["complete_measured_normal_channel_trace_distance"] < 2e-11
    assert sum(Fraction(b["raw_Born_probability"]) for b in out["complete_character_classes"]) == 1


@pytest.mark.parametrize("r,c", [(3, 1), (4, 2), (5, 2), (6, 3)])
def test_character_hash_is_the_actual_normal_subgroup_eigencharacter(r, c):
    C = NormalCharacterChannel(r, c, (((1, 0),), ((0, 1),), ((2, 1),)))
    pi_c = (1, 0)
    for _ in range(c):
        pi_c = multiply(pi_c, (-1, 1), r)
    roots = ((1, 0), (0, 1), (-1, -1))
    for w, b in product(product(range(3), repeat=C.copies), ((1, 0), (0, 1), (2, 1))):
        full = sum((pairing(multiply(a[0], roots[j], r), multiply(pi_c, b, r), r) for a, j in zip(C.labels, w)), Fraction()) % 1
        reduced = pairing(C.normal_character(w)[0], b, r-c)
        assert full == reduced


def test_collective_pinching_is_not_an_information_loss_claim_for_the_original_input(report):
    controls = report["complete_channels"]
    assert sum(c["exact_phase_difference_constant_within_each_class"] for c in controls) == 4
    for i in (0, 1, 2, 5):
        c = controls[i]
        assert c["complete_measured_normal_channel_trace_distance"] < 2e-11
        assert c["original_and_coherently_retained_character_channel_fidelity"] < 1-1e-8
    for i in (3, 4):
        assert not controls[i]["exact_phase_difference_constant_within_each_class"]
        assert controls[i]["complete_measured_normal_channel_trace_distance"] > .1
    assert not report["multi_output_or_coherent_receiver_ruled_out"]


@pytest.mark.parametrize("r", [2, 4, 16, 128])
def test_last_centre_measurement_has_no_nontrivial_secret_precision_ceiling(r):
    L = precision_ledger(r, 8, r-1)
    assert L["normal_subgroup_is_central"]
    assert L["integer_secret_alias_class"]["exponent"] == 0


def test_normal_character_measurement_and_homomorphic_projection_have_different_ceilings():
    L = precision_ledger(16, 8, 2)
    assert L["maximum_integer_secret_trits_retained_per_coordinate"] == 2
    assert L["integer_secret_alias_class"] == {"base": 3, "exponent": 8*(8-2)}
    assert not L["bound_applies_to_coherently_retained_character_register"]
    assert not L["additional_untouched_original_inputs_covered"]


def test_positive_conjugate_eraser_restores_reference_entanglement_but_does_not_decode(report):
    for c in report["complete_public_conjugate_eraser_controls"]:
        assert c["maximum_feedforward_corrected_joint_vector_error"] < 2e-12
        assert c["maximum_raw_probability_error"] < 2e-12
        assert Fraction(c["exact_raw_probability_of_every_outcome"]) == Fraction(1, c["complete_Fourier_outcome_count"])
        assert c["restores_input_including_reference_entanglement"]
        assert not c["erases_original_word_register"]
        assert not c["decodes_secret"]
        assert not c["undoes_already_classically_measured_normal_character"]


def test_invalid_source_and_invented_branch_supply_are_rejected():
    with pytest.raises(ValueError, match="c<r"):
        NormalCharacterChannel(4, 4, (((1, 0),),))
    with pytest.raises(ValueError, match="canonical"):
        NormalCharacterChannel(4, 2, (((1, 0),),)).normal_character((True,))
    with pytest.raises(ValueError, match="81"):
        conjugate_erase_control(NormalCharacterChannel(6, 1, (((1, 0),),)), np.ones((3, 1))/np.sqrt(3))


def test_independent_exact_channel_replay(report, tmp_path):
    f = tmp_path/"report.json"
    f.write_text(json.dumps(report))
    result = subprocess.run(["node", str(ROOT/"research/certificates/native_normal_character_channel_crosscheck.js"), str(f)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["exact_original_word_phases"] == 66


@pytest.mark.parametrize("mutation", ["phase", "character", "missing_outcome", "probability", "alias", "coherent", "scope", "precision"])
def test_independent_checker_rejects_forged_phase_channels(report, mutation, tmp_path):
    bad = deepcopy(report)
    c = bad["complete_channels"][0]
    if mutation == "phase":
        c["exact_phase_difference_mod1"][1] = "0"
    elif mutation == "character":
        c["normal_characters"][0] = ((0, 0),)
    elif mutation == "missing_outcome":
        c["complete_character_classes"].pop()
    elif mutation == "probability":
        c["complete_character_classes"][0]["raw_Born_probability"] = "1"
    elif mutation == "alias":
        c["exact_phase_difference_constant_within_each_class"] = False
    elif mutation == "coherent":
        c["original_word_register_erased_by_coherent_computation"] = True
    elif mutation == "scope":
        bad["multi_output_or_coherent_receiver_ruled_out"] = True
    else:
        bad["growing_precision_ledgers"][0]["maximum_integer_secret_trits_retained_per_coordinate"] = 1
    f = tmp_path/"bad.json"
    f.write_text(json.dumps(bad))
    result = subprocess.run(["node", str(ROOT/"research/certificates/native_normal_character_channel_crosscheck.js"), str(f)], capture_output=True, text=True)
    assert result.returncode != 0
