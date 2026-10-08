from fractions import Fraction
import json
from pathlib import Path
import subprocess

import pytest
import sympy as sp

from ternary_blind_product_gate import (
    blind_product_gate, effects_invariants, example_povms, invariant_product_gate,
    physical_gram_control,
)
from ternary_product_trine import fixed_trine_gate


@pytest.mark.parametrize("name,d,eta,zero", [
    ("computational", Fraction(0), Fraction(0), Fraction(0)),
    ("inverse_F3", Fraction(2, 3), Fraction(0), Fraction(2)),
    ("real_pair_basis", Fraction(1, 3), Fraction(1, 3), Fraction(2, 3)),
    ("real_dense_basis", Fraction(16, 27), Fraction(16, 27), Fraction(0)),
    ("public_half_F3_half_real_dense", Fraction(17, 27), Fraction(8, 27), Fraction(1)),
])
def test_exact_PSD_measurements_have_correct_opposite_and_zero_secret_invariants(name,d,eta,zero):
    inv = effects_invariants(example_povms()[name])
    assert inv["nonzero_diagonal"] == d and inv["opposite_nonzero_secret_Gram"] == eta
    assert inv["zero_diagonal"] == zero and inv["exact_PSD_and_completeness_certified"]


@pytest.mark.parametrize("name", list(example_povms()))
def test_complete_physical_native_label_gram_in_arbitrary_basis(name):
    c = physical_gram_control(example_povms()[name])
    assert c["actual_Born_Gram_residual"] < 2e-12
    assert c["complete_native_label_pairs"] == 81 and c["complete_secret_pairs"] == 81
    assert c["nonprimitive_and_zero_secrets_kept"]


def test_negative_opposite_secret_correlations_are_not_discarded():
    effects = [sp.Matrix([[sp.Rational(1,2), sign*sp.I/2, 0],
                          [-sign*sp.I/2, sp.Rational(1,2), 0],[0,0,0]]) for sign in (1,-1)]
    effects.append(sp.diag(0,0,1))
    inv = effects_invariants(effects)
    assert inv["nonzero_diagonal"] == Fraction(1,3)
    assert inv["opposite_nonzero_secret_Gram"] == -Fraction(1,3)
    assert inv["zero_diagonal"] == 0
    assert physical_gram_control(effects)["actual_Born_Gram_residual"] < 2e-12
    gate = invariant_product_gate([inv]*3, 1, 4)
    assert Fraction(gate["opposite_product_entry"]) == Fraction(2,3)**3-1
    assert Fraction(gate["nonzero_Gram_operator_norm"]) == Fraction(4,3)**3-Fraction(2,3)**3


@pytest.mark.parametrize("r", [8,16,32,64])
def test_universal_fixed_POVM_copy_gate_is_not_label_aware_or_adaptive_lower_bound(r):
    c = blind_product_gate(1,r,r-2)
    fourier = fixed_trine_gate(1,r,r-2)
    assert Fraction(c["nonzero_contribution_advantage_upper_squared"]) == 2*Fraction(fourier["nonzero_contribution_advantage_upper_squared"])
    assert not c["necessary_copy_gate_passed"]
    assert c["opposite_secret_correlations_kept"] and c["different_POVM_per_original_copy_covered"]
    assert c["shared_independent_public_measurement_randomness_covered"]
    for key in ("label_dependent_quantum_measurements_covered", "outcome_adaptive_quantum_measurements_covered", "collective_quantum_measurements_covered", "speedup_claim_allowed"):
        assert not c[key]


def test_exact_Fourier_special_case_and_nonidentical_measurements_match_product_Gram():
    povms=example_povms()
    inv=effects_invariants(povms["inverse_F3"])
    c=invariant_product_gate([inv]*6,1,8)
    f=fixed_trine_gate(1,8,6)
    assert c["opposite_product_entry"] == "0"
    assert c["nonzero_contribution_advantage_upper_squared"] == f["nonzero_contribution_advantage_upper_squared"]
    inv2=effects_invariants(povms["real_pair_basis"])
    mixed=invariant_product_gate([inv,inv2],1,4)
    assert Fraction(mixed["nonzero_product_diagonal"]) == Fraction(11,9)
    assert Fraction(mixed["opposite_product_entry"]) == Fraction(1,3)


def test_measurements_with_invalid_or_unresolved_PSD_are_rejected():
    with pytest.raises(ValueError): effects_invariants([sp.eye(2)])
    with pytest.raises(ValueError): effects_invariants([sp.diag(-1,1,1),sp.diag(2,0,0)])
    with pytest.raises(ValueError): effects_invariants([sp.eye(3)/2])
    with pytest.raises(ValueError): effects_invariants([sp.zeros(3),sp.eye(3)])
    with pytest.raises(ValueError): effects_invariants([sp.Matrix([[1,1,0],[0,1,0],[0,0,1]])])
    t=sp.Symbol("t",real=True)
    with pytest.raises(ValueError): effects_invariants([sp.diag(t,1,1),sp.diag(1-t,0,0)])


def test_zero_copies_and_polynomial_surplus_not_overclaimed():
    assert blind_product_gate(1,4,0)["nonzero_contribution_advantage_upper_squared"] == "0"
    assert blind_product_gate(1,4,20)["necessary_copy_gate_passed"]
    with pytest.raises(ValueError): invariant_product_gate([{"nonzero_diagonal":"1", "opposite_nonzero_secret_Gram":"0"}],1,4)
    assert invariant_product_gate([],1,4)["nonzero_Gram_operator_norm"] == "0"


@pytest.mark.parametrize("mutation", ["PSD", "eta", "scope", "gate", "product", "promotion"])
def test_independent_exact_checker_rejects_corrupted_measurements_or_scope(tmp_path, mutation):
    root=Path(__file__).resolve().parents[1]
    record=json.loads((root/"research/classical_baselines/ternary_blind_product_gate.json").read_text())
    if mutation == "PSD": record["certified_POVM_controls"][0]["effects_Qomega"][0][0][0]=["-1","0"]
    if mutation == "eta": record["certified_POVM_controls"][2]["invariants"]["opposite_nonzero_secret_Gram"]="0"
    if mutation == "scope": record["universal_scaling_gates"][0]["label_dependent_quantum_measurements_covered"]=True
    if mutation == "gate": record["universal_scaling_gates"][0]["necessary_copy_gate_passed"]=True
    if mutation == "product": record["certified_POVM_controls"][2]["eight_copy_scalar_gate"]["opposite_product_entry"]="0"
    if mutation == "promotion": record["all_LOCC_or_general_quantum_lower_bound"]=True
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_blind_product_gate_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode != 0,result.stdout
