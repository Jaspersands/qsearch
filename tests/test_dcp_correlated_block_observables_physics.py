from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
from scipy.linalg import hadamard

from theorems.dcp_correlated_block_observables import (
    REPORT, analyze, build_report, information, measurement_channel,
    minimum_signed_relation, native_blindness_frontier, native_collision_census,
    native_collision_moment, native_readout_information_frontier, product_twirl_distribution,
)
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_correlated_block_observables_crosscheck.js"
A=((1,0,5,1),(0,1,1,2))


@pytest.fixture(scope="module")
def report():
    return build_report()


@pytest.mark.parametrize("v",[Fraction(0),Fraction(1,2),Fraction(7,8),Fraction(1)])
def test_complete_joint_law_matches_direct_projected_density_and_H_readout(v):
    C=measurement_channel(A,4,v)
    H=hadamard(16)/4
    for s,secret in enumerate(C["secrets"]):
        rho=density(A,4,secret,v)
        for y,indices in enumerate(C["fibers"]):
            projected=np.zeros((16,16),dtype=complex)
            projected[np.ix_(indices,indices)]=rho[np.ix_(indices,indices)]
            expected=np.diag(H@projected@H.T).real
            assert np.allclose(C["probabilities"][s,y],expected,atol=1e-13)
        assert C["probabilities"][s].sum()==pytest.approx(1)


def test_BSC_convolution_equals_explicit_independent_error_masks():
    clean=measurement_channel(A,4,1)["probabilities"]
    v=Fraction(7,8)
    p=(1-v)/2
    expected=np.zeros_like(clean)
    for e in range(16):
        weight=float(p**e.bit_count()*(1-p)**(4-e.bit_count()))
        expected+=weight*clean[:,:,np.arange(16)^e]
    assert np.allclose(expected,measurement_channel(A,4,v)["probabilities"],atol=1e-13)


def test_uniform_low_marginals_can_hide_nonzero_secret_dependent_degree_three_bias():
    v=Fraction(7,8)
    C=measurement_channel(A,4,v)
    P,H=C["probabilities"],C["Walsh_matrix"]
    assert minimum_signed_relation(A)["minimum_nonzero_signed_support"]==3
    for u in range(1,16):
        if u.bit_count()<=2:
            assert np.max(np.abs(P@H[:,u]))<1e-12
    y=1+4  # Syndrome(1,1), fiber addresses3 and4.
    assert C["syndrome_probabilities"][y]==pytest.approx(1/8)
    for secret,bias in (((0,0),float(v**3)),((1,0),0),((2,0),-float(v**3))):
        s=C["secrets"].index(secret)
        conditional=np.dot(P[s,y],H[:,7])/C["syndrome_probabilities"][y]
        assert conditional==pytest.approx(bias,abs=1e-12)
    assert information(P)["uniform_secret_mutual_information_bits"]>0.08


def test_all_two_qubit_reduced_states_are_diagonal_and_secret_independent():
    def reduce(rho,support):
        mask=sum(1 << i for i in support)
        result=np.zeros((1 << len(support),)*2,dtype=complex)
        for x,y in product(range(16),repeat=2):
            if (x & (15^mask))==(y & (15^mask)):
                i=sum((x >> k & 1) << j for j,k in enumerate(support))
                j=sum((y >> k & 1) << r for r,k in enumerate(support))
                result[i,j]+=rho[x,y]
        return result
    C=measurement_channel(A,4,Fraction(7,8))
    reference={}
    for secret in ((0,0),(1,0),(2,3)):
        rho=density(A,4,secret,Fraction(7,8))
        for y,indices in enumerate(C["fibers"]):
            if not indices:
                continue
            block=np.zeros((16,16),dtype=complex)
            block[np.ix_(indices,indices)]=rho[np.ix_(indices,indices)]/C["syndrome_probabilities"][y]
            for size in (1,2):
                for support in combinations(range(4),size):
                    reduced=reduce(block,support)
                    assert np.allclose(reduced,np.diag(np.diag(reduced)))
                    key=y,support
                    if key in reference:
                        assert np.allclose(reduced,reference[key])
                    else:
                        reference[key]=reduced


def test_product_twirl_reproduces_discarded_syndrome_only():
    C=measurement_channel(A,4,Fraction(7,8))
    P=C["probabilities"]
    for s,secret in enumerate(C["secrets"]):
        baseline=product_twirl_distribution(A,4,secret,Fraction(7,8))
        assert np.allclose(baseline,P[s].sum(axis=0),atol=1e-13)
    joint=information(P)["uniform_secret_mutual_information_bits"]
    discarded=information(P.sum(axis=1))["uniform_secret_mutual_information_bits"]
    assert joint>discarded+0.06


def test_easy_selected_product_control_is_matched_by_baseline_not_a_collective_signal(report):
    C=report["finite_controls"][1]
    joint=C["joint_syndrome_and_X_information"]
    discarded=C["discarded_syndrome_X_information"]
    assert joint["uniform_secret_mutual_information_bits"]==pytest.approx(discarded["uniform_secret_mutual_information_bits"])
    assert joint["optimal_one_copy_Bayes_guess_probability"]==pytest.approx(discarded["optimal_one_copy_Bayes_guess_probability"])
    assert C["efficient_decoder_or_quantum_advantage_claimed"] is False
    assert C["twirl_requires_single_qubit_source_measurement_access"] is True
    assert C["classical_unknown_secret_DCP_simulation_supplied"] is False


def test_complete_dephasing_and_singleton_fibers_leave_no_secret_readout_information():
    C=measurement_channel(A,4,0)
    assert np.allclose(C["probabilities"],C["syndrome_probabilities"][None,:,None]/16)
    assert information(C["probabilities"])["uniform_secret_mutual_information_bits"]==pytest.approx(0,abs=1e-12)
    S=analyze(((1,2),),3,1)
    assert S["minimum_signed_relation_diagnostic"]["minimum_nonzero_signed_support"] is None
    assert S["all_X_outcomes_k_wise_uniform_conditional_on_syndrome"]==2
    assert S["joint_syndrome_and_X_information"]["uniform_secret_mutual_information_bits"]==pytest.approx(0,abs=1e-12)


def test_exact_integer_chernoff_bound_dominates_signed_relation_union():
    assert 17**8 < 1 << 33
    for n in range(2,129):
        F=native_blindness_frontier(n)
        k=n//4
        exact=Fraction(sum(comb(4*n,w)*(1 << w) for w in range(1,k+1)),1 << (2*n))
        E=F["any_signed_relation_through_degree_k_probability_power_of_two_upper_exponent"]
        assert exact<=Fraction(1,1 << E)
        if n%4==0:
            assert E==n//4
        assert F["joint_high_degree_X_correlations_excluded"] is False
        assert F["local_measurement_circuits_or_full_output_decoders_ruled_out"] is False


def test_native_full_label_collision_formula_and_even_secret_counterexample():
    rows=native_collision_census()
    assert len(rows)==6
    expected={"1":Fraction(21,8),"1/2":Fraction(201,128),"0":Fraction(11,8)}
    for row in rows:
        assert row["all_original_label_matrices"]==4096
        if row["fixed_residual_secret"]==1:
            assert Fraction(row["primitive_secret_formula_exact_rational"])==expected[row["visibility_exact"]]
            assert row["native_mean_uniform_reference_collision_multiplier"]==pytest.approx(float(expected[row["visibility_exact"]]),abs=1e-12)
        else:
            assert row["primitive_secret_formula_exact_rational"] is None
    assert rows[3]["native_mean_uniform_reference_collision_multiplier"]==pytest.approx(17/4)
    assert rows[3]["native_mean_uniform_reference_collision_multiplier"]>float(expected["1"])


def test_collision_zero_noise_and_dephasing_limits_and_scope():
    for n in (1,2,3):
        for m in range(1,9):
            zero=native_collision_moment(n,m,0)
            middle=native_collision_moment(n,m,Fraction(1,2))
            clean=native_collision_moment(n,m,1)
            assert zero==1+Fraction(4**n-1,1 << m)
            assert 1<=zero<=middle<=clean
    with pytest.raises(ValueError,match="UNKNOWN"):
        native_collision_moment(1,3,1,secret_has_odd_component=False)
    with pytest.raises(ValueError):
        native_collision_moment(1,3,1,phase_bits=3)


def test_native_readout_information_bound_charges_exception_and_Fano_samples():
    from math import log2
    for n in (16,32,64,128,256):
        F=native_readout_information_frontier(n)
        h=F["mean_information_bits_per_fixed_readout_batch_upper"]["dyadic_correction_exponent"]
        upper=1+Fraction(1,1 << h)
        kappa=native_collision_moment(n,3*n,1)
        assert log2(float(kappa))+5*n*2.0**(-n)<=float(upper)
        target=Fraction(3*F["residual_secret_entropy_bits"],4)-2
        attempts=F["three_quarter_negation_orbit_identification_attempt_lower_bound"]
        assert attempts*upper>=target and (attempts-1)*upper<target
        assert F["raw_original_qubits_lower_bound_for_that_orbit_target"]==3*n*attempts
        assert not F["three_quarter_full_secret_identification_target_attainable"]
        assert not F["adaptively_secret_aligned_bases_or_other_collective_measurements_covered"]
        assert not F["polynomial_sample_lower_bound_is_a_general_algorithmic_no_go"]
    F=native_readout_information_frontier(64)
    assert F["retained_block_Holevo_lower_bits_IF_full_injective"]==50
    assert F["mean_information_bits_per_fixed_readout_batch_upper"]["dyadic_correction_exponent"]==10


def test_diagnostic_and_likelihood_work_caps_return_unknown_not_a_no_go():
    for operation in (lambda:measurement_channel(((1,)*9,),4,1),
                      lambda:measurement_channel(((1,1),(1,2)),8,1),
                      lambda:minimum_signed_relation(((1,)*9,))):
        with pytest.raises(ValueError,match="UNKNOWN"):
            operation()
    for bad in ([[0.2,0.2]], [[-1,2]], [[float("nan"),1]]):
        with pytest.raises(ValueError):
            information(bad)


def test_live_artifact_and_independent_direct_sum_replay(report):
    assert json.loads(REPORT.read_text())==report
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    out=json.loads(result.stdout)
    assert out["status"]=="ok" and out["full_outcome_controls_replayed"]==3


@pytest.mark.parametrize("field",["mutual_information","Bayes","claimed_advantage","local_circuit_no_go"])
def test_independent_checker_rejects_forged_likelihoods_or_scope(report,tmp_path,field):
    payload=deepcopy(report)
    C=payload["finite_controls"][0]
    if field=="mutual_information":
        C["joint_syndrome_and_X_information"]["uniform_secret_mutual_information_bits"]+=0.1
    elif field=="Bayes":
        C["joint_syndrome_and_X_information"]["optimal_one_copy_Bayes_guess_probability"]+=0.1
    elif field=="claimed_advantage":
        C["efficient_decoder_or_quantum_advantage_claimed"]=True
    else:
        payload["native_joint_information_blindness_frontiers"][0]["local_measurement_circuits_or_full_output_decoders_ruled_out"]=True
    path=tmp_path/"forged.json"
    path.write_text(json.dumps(payload))
    result=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
    assert result.returncode!=0


def test_readonly_cli_preserves_live_artifact():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-correlated-block-observables","--no-write"],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert REPORT.read_bytes()==before
