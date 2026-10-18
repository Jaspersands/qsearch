"""Independent natural-Hamiltonian checks, precision traps and readout scope."""
from fractions import Fraction
from itertools import product
from math import pi
import json

import numpy as np
import pytest

from conditional_boson_dynamics import (
    DensityForceModel,DynamicsLimit,certified_pair,exact_configuration_reference,
    estimate_pauli,uniform_fock_cutoff_bound,fock_reference,pauli_action,run_controls,
    weak_hopping_readout_budget,
    exact_low_weight_readout,
    REPORT,
)


def midpoint(record): return (Fraction(record["lower"])+Fraction(record["upper"]))/2


def revival(force=Fraction(1,2)):
    return DensityForceModel((1,),(0,),((force,),),(0,))


@pytest.fixture(scope="module")
def report(): return run_controls()


def test_same_final_boson_state_does_not_make_controlled_geometric_phase_global(report):
    Y,X = report["physical_controls"][:2]
    assert midpoint(Y["analytic_reference"]) == 1
    assert midpoint(X["analytic_reference"]) == 0
    assert abs(Y["finite_Fock_reference"]["Pauli_expectation"]-1) < 1e-9
    assert abs(X["finite_Fock_reference"]["Pauli_expectation"]) < 1e-9
    # Ignoring the force-dependent closed-loop phase instead predicts |+>.
    assert not report["general_Hubbard_Holstein_or_joint_sampling_dequantized"]


@pytest.mark.parametrize("pauli", ["".join(p) for p in product("IXYZ",repeat=2)])
def test_every_two_control_Pauli_matches_actual_Hamiltonian_evolution(pauli):
    model = DensityForceModel((1,),(Fraction(1,7),),((Fraction(1,3),Fraction(-1,4)),),
                              (Fraction(2,9),Fraction(-1,11)),((0,1,Fraction(3,13)),))
    reference = exact_configuration_reference(model,Fraction(4,7),pauli)
    local = exact_low_weight_readout(model,Fraction(4,7),pauli)
    assert max(Fraction(reference["lower"]),Fraction(local["lower"])) <= min(Fraction(reference["upper"]),Fraction(local["upper"]))
    physical = fock_reference(model,Fraction(4,7),pauli,24)
    bound = uniform_fock_cutoff_bound(model,Fraction(4,7),24)
    assert abs(float(midpoint(reference))-physical["Pauli_expectation"]) <= float(Fraction(bound["Pauli_expectation_error_upper"]))+1e-10
    assert abs(physical["norm_squared"]-1) < 1e-10
    assert not physical["floating_sparse_reference_is_formally_certified"]


def test_multiple_modes_and_force_signs_preserve_actual_branch_interference():
    model = DensityForceModel((1,Fraction(3,2)),(Fraction(1,5),Fraction(-1,7)),
                              ((Fraction(1,4),Fraction(-1,5)),(Fraction(-1,6),Fraction(1,8))),
                              (Fraction(1,11),Fraction(-2,13)))
    for pauli in ("XY","YY","ZX"):
        reference = exact_configuration_reference(model,Fraction(5,9),pauli)
        physical = fock_reference(model,Fraction(5,9),pauli,12)
        assert abs(float(midpoint(reference))-physical["Pauli_expectation"]) < 1e-8


def test_independent_dense_Hamiltonian_replay_including_noncommuting_hopping():
    from scipy.linalg import expm
    cutoff = 8
    omega,g,E,J = Fraction(3,2),Fraction(1,3),Fraction(2,5),Fraction(1,7)
    X,Y = np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]])
    occupation = np.diag([0,1])
    a = np.diag(np.sqrt(np.arange(1,cutoff)),1)
    I = np.eye(cutoff)
    H = (np.kron(np.eye(2),float(omega)*a.T@a)
         +np.kron(occupation,float(g)*(a+a.T)+float(E)*I)+float(J)*np.kron(X,I))
    initial = np.zeros(2*cutoff,complex);initial[0]=initial[cutoff]=1/np.sqrt(2)
    state = expm(-1j*pi*4/7*H)@initial
    expected = np.vdot(state,np.kron(Y,I)@state).real
    model = DensityForceModel((omega,),(0,),((g,),),(E,))
    actual = fock_reference(model,Fraction(4,7),"Y",cutoff,hopping=(J,))
    assert abs(actual["Pauli_expectation"]-expected) < 1e-11


def test_adding_real_noncommuting_hopping_falsifies_the_H0_only_readout_model(report):
    control = report["noncommuting_scope_falsifier"]
    assert abs(control["no_hopping"]["Pauli_expectation"]-control["with_hopping"]["Pauli_expectation"]) > Fraction(1,50)
    assert not control["no_hopping"]["noncommuting_hopping_included"]
    assert control["with_hopping"]["noncommuting_hopping_included"]
    assert not control["H0_estimator_claimed_valid_after_adding_hopping"]
    assert not control["perturbative_readout_budget"]["H0_estimator_with_reduced_error_budget_suffices"]


def test_small_nonzero_hopping_has_a_paid_classical_readout_error_budget():
    model = revival()
    t,J,eps = Fraction(1,2),Fraction(1,10000),Fraction(1,10)
    budget = weak_hopping_readout_budget(model,t,(J,),eps)
    error = Fraction(budget["additional_Pauli_expectation_error_upper"])
    assert budget["H0_estimator_with_reduced_error_budget_suffices"]
    assert Fraction(budget["remaining_additive_error_budget"])+error == eps
    a = fock_reference(model,t,"X",24)["Pauli_expectation"]
    b = fock_reference(model,t,"X",24,hopping=(J,))["Pauli_expectation"]
    assert abs(a-b) <= float(error)+1e-10
    assert not budget["large_bound_is_evidence_of_quantum_advantage"]


def test_endpoint_vacuum_return_alone_does_not_certify_a_small_Fock_cutoff():
    model = revival(Fraction(2))
    ideal = exact_configuration_reference(model,2,"X")
    assert midpoint(ideal) == 1
    # Infinite oscillator is exactly back in vacuum; a dimension2 oscillator
    # still evolves incorrectly because of INTERMEDIATE boundary population.
    wrong = fock_reference(model,2,"X",2)
    assert abs(wrong["Pauli_expectation"]-1) > 0.1
    bound = uniform_fock_cutoff_bound(model,2,2)
    assert bound["includes_intermediate_boundary_leakage"]
    assert Fraction(bound["state_2norm_error_upper"]) == 2


def test_finite_Fock_annihilators_do_not_obey_the_infinite_CCR():
    cutoff = 5
    a = np.diag(np.sqrt(np.arange(1,cutoff)),1)
    commutator = a@a.T-a.T@a
    expected = np.eye(cutoff);expected[-1,-1] -= cutoff
    np.testing.assert_allclose(commutator,expected,atol=1e-14)
    assert not np.allclose(commutator,np.eye(cutoff))


def test_binary64_cannot_silently_erase_exact_large_force_differences(report):
    force = 2**80
    assert float(force) == float(force+1)
    model = DensityForceModel((1,),(force,),((1,),),(0,))
    with pytest.raises(DynamicsLimit,match="PRECISION_CAP"):
        certified_pair(model,Fraction(1,3),"X",(0,),max_precision_bits=64)
    row = certified_pair(model,Fraction(1,3),"X",(0,),max_precision_bits=256)
    assert row["precision_bits"] >= 128
    assert Fraction(row["upper"])-Fraction(row["lower"]) <= Fraction(2,2**40)
    assert abs(midpoint(row)-1) > Fraction(1,3)  # float forces would give1.
    assert report["large_force_exact_input_pair"] == row


def test_independent_high_precision_branch_calculation_checks_the_large_force_phase():
    import mpmath as mp
    force = 2**80
    model = DensityForceModel((1,),(force,),((1,),),(0,))
    row = certified_pair(model,Fraction(1,3),"X",(0,))
    with mp.workdps(180):
        theta = mp.pi/3
        a,b = mp.mpf(force),mp.mpf(force+1)
        alpha,beta = a*(mp.exp(-1j*theta)-1),b*(mp.exp(-1j*theta)-1)
        overlap = mp.exp(-abs(alpha)**2/2-abs(beta)**2/2+mp.conj(beta)*alpha)
        expected = (overlap*mp.exp(1j*(a*a-b*b)*(theta-mp.sin(theta)))).real
        lo,hi = Fraction(row["lower"]),Fraction(row["upper"])
        assert mp.mpf(lo.numerator)/lo.denominator <= expected <= mp.mpf(hi.numerator)/hi.denominator


def test_exact_dimensionless_products_precede_binary64_in_Fock_reference():
    clock = 2**1200
    model = DensityForceModel((clock,),(0,),((clock//2,),),(0,))
    t = Fraction(2,clock)
    assert midpoint(exact_configuration_reference(model,t,"Y")) == 1
    actual = fock_reference(model,t,"Y",24)
    assert abs(actual["Pauli_expectation"]-1) < 1e-9


def test_scalar_estimator_scales_in_input_bits_not_oscillator_Fock_dimension(report):
    result = report["64_control_seeded_estimator"]
    assert result["sample_count"] == 128
    assert result["configuration_random_bits_charged"] == 64*128
    assert not result["bosonic_cutoff_materialized"]
    assert not result["all_joint_measurement_outcomes_sampled"]
    assert not result["relative_error_for_tiny_expectations_certified"]
    assert result["coverage_requires_IID_uniform_random_bits"]
    assert not result["seeded_replay_is_a_certified_IID_source"]
    assert result["observable"] == "X"*64
    local = report["64_control_exact_local_readout"]
    assert local["flipped_assignments"] == 2
    assert local["analytically_summed_control_bits"] == 63
    assert local["no_statistical_sampling"]


def test_all_three_control_Paulis_with_mixed_quadratic_energy_match_analytic_sum():
    model = DensityForceModel((1,Fraction(2,3)),(Fraction(1,7),Fraction(1,11)),
                              ((Fraction(1,4),Fraction(-1,5),Fraction(2,7)),(Fraction(-1,8),Fraction(1,6),Fraction(1,9))),
                              (Fraction(1,2),Fraction(1,3),Fraction(-2,5)),
                              ((0,1,Fraction(2,5)),(1,2,Fraction(-1,7)),(0,2,Fraction(3,8))))
    for pauli in map("".join,product("IXYZ",repeat=3)):
        expected = exact_configuration_reference(model,Fraction(3,5),pauli)
        actual = exact_low_weight_readout(model,Fraction(3,5),pauli)
        assert max(Fraction(expected["lower"]),Fraction(actual["lower"])) <= min(Fraction(expected["upper"]),Fraction(actual["upper"]))


def test_exact_local_readout_never_enumerates_the_unflipped_control_space(monkeypatch):
    import conditional_boson_dynamics as module
    n = 72
    model = DensityForceModel((1,),(Fraction(1,7),),((Fraction(1,11),)*n,),(Fraction(1,13),)*n)
    original = module.product
    def bounded(*args,**kwargs):
        assert kwargs.get("repeat",0) <= 1
        return original(*args,**kwargs)
    monkeypatch.setattr(module,"product",bounded)
    result = exact_low_weight_readout(model,Fraction(3,7),"Y"+"I"*(n-1))
    assert result["flipped_assignments"] == 2
    assert result["analytically_summed_control_bits"] == n-1
    with pytest.raises(DynamicsLimit,match="FLIP_WEIGHT_CAP"):
        exact_low_weight_readout(model,1,"X"*n,max_flipped_assignments=8)


def test_analytic_free_bit_sum_also_pays_large_force_phase_precision():
    model = DensityForceModel((1,),(2**80,),((1,Fraction(2,5)),),(0,0),((0,1,Fraction(1,7)),))
    with pytest.raises(DynamicsLimit,match="PRECISION_CAP"):
        exact_low_weight_readout(model,Fraction(1,3),"XI",max_precision_bits=64)
    local = exact_low_weight_readout(model,Fraction(1,3),"XI")
    full = exact_configuration_reference(model,Fraction(1,3),"XI")
    assert local["max_precision_bits_used"] >= 128
    assert max(Fraction(local["lower"]),Fraction(full["lower"])) <= min(Fraction(local["upper"]),Fraction(full["upper"]))


def test_MC_interval_uses_a_paid_Hoeffding_bound_and_certified_arithmetic():
    model = revival()
    eps,b = Fraction(1,2),4
    result = estimate_pauli(model,Fraction(1,3),"X",epsilon=eps,failure_bits=b,seed=780123)
    exact = exact_configuration_reference(model,Fraction(1,3),"X")
    lo,hi = map(Fraction,result["confidence_interval"])
    assert lo <= midpoint(exact) <= hi  # calibration, not a proof of coverage.
    assert result["sample_count"]*eps*eps >= 8*(b+1)
    arithmetic = tuple(map(Fraction,result["arithmetic_sample_mean_interval"]))
    assert arithmetic[1]-arithmetic[0] <= eps/4
    assert Fraction(result["failure_probability_model_upper"]) == Fraction(1,2**b)


def test_no_hidden_full_state_or_configuration_table_in_the_large_estimator(monkeypatch):
    import conditional_boson_dynamics as module
    def forbidden(*args,**kwargs): raise AssertionError("exponential oracle/reference invoked")
    n = 96
    model = DensityForceModel((1,),(0,),((Fraction(1,11),)*n,),(Fraction(1,13),)*n)
    monkeypatch.setattr(module,"fock_reference",forbidden)
    monkeypatch.setattr(module,"exact_configuration_reference",forbidden)
    monkeypatch.setattr(module,"product",forbidden)
    result = estimate_pauli(model,Fraction(2,5),"X"+"I"*(n-1),epsilon=Fraction(1,2),failure_bits=2,seed=88119)
    assert result["configuration_random_bits_charged"] == n*result["sample_count"]


@pytest.mark.parametrize("count", [101,128,129,130,257])
def test_large_Y_counts_use_exact_fourth_roots_not_floating_complex_powers(count):
    other,phase = pauli_action("Y"*count,(0,)*count)
    assert phase == (1,1j,-1,-1j)[count % 4]
    assert other == (1,)*count


@pytest.mark.parametrize("override", [
    {"frequencies":(0,)},{"frequencies":(-1,)},{"frequencies":(1.0,)},
    {"force_offsets":(True,)},{"force_matrix":((1,2),)},
    {"diagonal_pairs":((0,0,1),)},{"diagonal_pairs":((0,1,1),)},
])
def test_invalid_physical_and_inexact_input_promises_fail_closed(override):
    data = dict(frequencies=(1,),force_offsets=(0,),force_matrix=((1,),),diagonal_linear=(0,))
    with pytest.raises(ValueError): DensityForceModel(**(data|override))


def test_unknown_precision_sampling_and_reference_caps_do_not_become_hardness():
    model = revival()
    with pytest.raises(DynamicsLimit,match="SAMPLE_CAP"):
        estimate_pauli(model,1,"X",epsilon=Fraction(1,1000),max_samples=100)
    with pytest.raises(DynamicsLimit,match="STATE_CAP"):
        fock_reference(model,1,"X",24,max_states=4)
    with pytest.raises(DynamicsLimit,match="CONFIGURATION_REFERENCE_CAP"):
        exact_configuration_reference(model,1,"X",max_configurations=1)
    with pytest.raises(DynamicsLimit,match="TIME_ENERGY_CAP"):
        fock_reference(model,10**9,"X",24)
    with pytest.raises(ValueError): certified_pair(model,1.0,"X",(0,))
    with pytest.raises(ValueError): certified_pair(model,1,"Q",(0,))
    with pytest.raises(ValueError): certified_pair(model,1,"X",(True,))


def test_live_artifact_preserves_exact_inputs_source_hash_and_scope(report):
    if not REPORT.exists(): pytest.skip("live artifact has not been generated yet")
    data = json.loads(REPORT.read_text())
    assert data["dependency_sha256"] == report["dependency_sha256"]
    assert data["large_force_exact_input_pair"]["time_in_pi_units"] == "1/3"
    assert data["64_control_seeded_estimator"]["time_in_pi_units"] == "2/7"
    assert data["64_control_exact_local_readout"] == report["64_control_exact_local_readout"]
    assert data["64_control_model"] == json.loads(json.dumps(report["64_control_model"]))
    assert not data["general_Hubbard_Holstein_or_joint_sampling_dequantized"]
    assert not data["accepted_speedup_candidate"]
