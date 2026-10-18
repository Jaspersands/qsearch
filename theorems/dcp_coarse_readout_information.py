"""Native linear-information readouts: mod2/width3n versus mod4/width5n.

This proves a conditional information lower bound, NOT an efficient decoder,
new source reduction, speedup, or advantage over measuring the original qubits.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_block_observables import information,measurement_channel
from theorems.dcp_nonlinear_fiber_pairing import phase_value
from theorems.dcp_quadratic_fiber_coordinates import coordinate_plan

REPORT = ROOT/"research/phase_workbench/dcp_coarse_readout_information.json"


def raw_information_rate_lower(visibility,terms=16):
    v = Fraction(visibility)
    if not 0 <= v <= 1:
        raise ValueError("original visibility must lie in [0,1]")
    integer(terms,"positive entropy-series terms",1,64)
    # ln2 < 7/10 because exp(7/10) > 1+7/10+(7/10)^2/2+(7/10)^3/6 > 2.
    # Uniform dyadic phase grids retain nonnegative extra cos^(2k) Fourier terms.
    return Fraction(10,7)*sum((v**(2*k)*Fraction(comb(2*k,k),4**k*2*k*(2*k-1))
                              for k in range(1,terms+1)),Fraction(0))


def native_frontier(n,*,coarse_bits=1,width_multiple=3):
    integer(n,"native components",2,4096)
    integer(coarse_bits,"coarse bits",1,2)
    integer(width_multiple,"original width multiple",1,5)
    m,t = width_multiple*n,n+8
    alpha = raw_information_rate_lower(Fraction(n-1,n))
    lower = max(Fraction(0),m*alpha-coarse_bits*n)
    failure = Fraction(3**m-1,1 << (t*n))
    exponent = n*n+(8-(3**width_multiple-1).bit_length())*n
    if failure >= Fraction(1,1 << exponent):
        raise ArithmeticError("native signed-relation union bound failed")
    constant = Fraction(1,4) if (coarse_bits,width_multiple)==(1,3) else Fraction(1,16) if (coarse_bits,width_multiple)==(2,5) else Fraction(0)
    uniform_linear = n*constant if n >= 64 else Fraction(0)
    if lower < uniform_linear:
        raise ArithmeticError("rational native linear-information constant failed")
    return {"components":n,"physical_width":m,"original_phase_bits":t,
            "measured_coarse_bits_per_component":coarse_bits,
            "original_Z_marginal_visibility_lower_bound":str(Fraction(n-1,n)),
            "raw_X_information_per_original_qubit_lower_bits_exact":str(alpha),
            "secret_coset_entropy_charged_bits":coarse_bits*n,
            "discard_syndrome_fixed_X_information_lower_bits_exact":str(lower),
            "retained_joint_syndrome_X_information_lower_bits_exact":str(lower),
            "uniform_n_ge_64_information_lower_bits_exact":str(uniform_linear),
            "full_frequency_noninjectivity_probability_power_of_two_upper_exponent":exponent,
            "bound_is_pointwise_on_every_full_frequency_injective_matrix":True,
            "pointwise_syndrome_information_lower_bound_claimed":False,
            "uniform_original_and_residual_secret_priors_required":True,
            "source_original_phase_qubits_per_attempt":m,
            "actual_syndrome_CX_CCX_gate_count_upper":coarse_bits*n*m,
            "actual_terminal_H_gates":m,
            "same_discarded_syndrome_law_via_product_twirl_phase_gate_count_upper":((1 << coarse_bits)-1)*m,
            "product_twirl_phase_gate":"Z" if coarse_bits==1 else "S",
            "product_twirl_needs_coherent_syndrome_register":False,
            "parity_only_can_clear_measured_linear_constraints_with_Clifford_gates":coarse_bits==1,
            "parity_compression_CNOT_count_upper":n*(m-n) if coarse_bits==1 and m>=2*n else None,
            "compressed_free_wires":"m-rank(A mod2)" if coarse_bits==1 else "mod4 fiber still constrained quadratically",
            "fresh_independent_phase_source_after_compression":False,
            "extra_arithmetic_scratch_qubits":0,
            "all_syndrome_branches_retained_or_physically_discarded_without_postselection":True,
            "requires_random_XY_masks_or_collective_terminal_measurement":False,
            "full_secret_identification_or_efficient_inference_proved":False,
            "information_lower_bound_is_a_sample_complexity_upper_bound":False,
            "beats_original_raw_phase_qubit_measurement_baseline":False,
            "actual_natural_source_noise_certified":False,
            "uniform_prior_bound_valid_for_arbitrary_adaptive_posteriors":False}


def product_twirl_plan(labels,phase_bits,dual,*,coarse_bits=2):
    A = matrix(labels)
    integer(phase_bits,"original phase bits",3,4096)
    integer(coarse_bits,"coarse bits",1,2)
    G = 1 << coarse_bits
    n,m = len(A),len(A[0])
    if n*m>100000 or any(a >= 1 << phase_bits for row in A for a in row):
        raise ValueError("UNKNOWN: canonical bounded product-twirl plan required")
    u = tuple(dual)
    if len(u)!=n:
        raise ValueError("one uniform mod4 twirl value per source component required")
    for value in u:
        integer(value,"public coarse twirl value",0,G-1)
    gates = []
    for i in range(m):
        gates.extend([["Z" if coarse_bits==1 else "S",i]]*(sum(u[l]*(A[l][i]%G) for l in range(n))%G))
        gates.append(["H",i])
    return {"original_phase_wires":m,"public_dual_values":list(u),
            "gates":gates,"terminal_Z_measurement_wires":list(range(m)),
            "uniform_random_bits_per_packet":coarse_bits*n,"extra_zero_qubits":0,
            "coarse_bits_per_component":coarse_bits,
            "pointwise_z_channel_equality_is_after_ignoring_twirl_values":True,
            "twirl_values_may_be_retained_without_weakening_information_lower_bound":True,
            "complete_twirl_and_syndrome_instruments_are_identical":False,
            "same_discarded_syndrome_fixed_X_channel":True,
            "baseline_requires_actual_unknown_secret_phase_qubits":True,
            "classical_simulation_of_unknown_secret_data_supplied":False,
            "hardware_transpilation_or_execution_performed":False}


def finite_control(labels,t,visibility,*,common_mode=False,coarse_bits=2):
    A = matrix(labels)
    integer(t,"finite original phase bits",3,8)
    integer(coarse_bits,"coarse bits",1,2)
    v = Fraction(visibility)
    if not 0 <= v <= 1:
        raise ValueError("visibility outside[0,1]")
    if type(common_mode) is not bool:
        raise ValueError("explicit Boolean common-mode noise control required")
    n,m = len(A),len(A[0])
    G = 1 << coarse_bits
    q,Q,M = 1 << t,1 << (t-coarse_bits),1 << m
    if m > 8 or q**n*M > 100000 or any(a >= q for row in A for a in row):
        raise ValueError("UNKNOWN: bounded full-original-secret likelihood calibration cap")
    secrets = list(product(range(q),repeat=n))
    signs = np.array([[1-2*(z >> i & 1) for i in range(m)] for z in range(M)])
    raw = np.array([np.prod((1+signs*(1 if common_mode else float(v))*np.cos(2*np.pi*(np.array(s)@np.array(A)%q)/q))/2,axis=1)
                    for s in secrets])
    if common_mode:
        raw = (1+float(v))/2*raw+(1-float(v))/2*raw[:,np.arange(M)^(M-1)]
    lumped = raw.reshape([G,Q]*n+[M]).mean(axis=tuple(2*l for l in range(n))).reshape(Q**n,M)
    C = measurement_channel(A,t,1 if common_mode else v,coarse_bits=coarse_bits)
    joint = C["probabilities"]
    if common_mode:
        joint = (1+float(v))/2*joint+(1-float(v))/2*joint[:,:,np.arange(M)^(M-1)]
    pinched = joint.sum(axis=1)
    residual = float(np.max(np.abs(lumped-pinched)))
    raw_info = information(raw)["uniform_secret_mutual_information_bits"]
    pinched_info = information(pinched)["uniform_secret_mutual_information_bits"]
    joint_info = information(joint)["uniform_secret_mutual_information_bits"]
    frequencies = [phase_value(A,x,q) for x in range(M)]
    injective = len(set(frequencies)) == M
    alpha = raw_information_rate_lower(v)
    lower = max(Fraction(0),m*alpha-coarse_bits*n) if injective else None
    uniform_residual = float(np.max(np.abs(raw.mean(axis=0)-1/M)))
    if (residual > 1e-11 or raw_info-pinched_info > coarse_bits*n+1e-11 or
        pinched_info > joint_info+1e-11 or (injective and
        (uniform_residual > 1e-11 or raw_info+1e-11 < float(m*alpha) or pinched_info+1e-11 < float(lower)))):
        raise ArithmeticError("actual full measurement refutes entropy-chain bound")
    result = {"full_labels":[list(row) for row in A],"original_phase_bits":t,"visibility_exact":str(v),
            "measured_coarse_bits_per_component":coarse_bits,
            "original_noise_model":"shared all-wire Z fault" if common_mode else "independent original Z faults",
            "full_frequency_map_injective":injective,
            "exported_product_twirl_plan":product_twirl_plan(A,t,[1]*n,coarse_bits=coarse_bits),
            "raw_full_original_secret_information_bits":raw_info,
            "pinched_residual_secret_X_information_bits":pinched_info,
            "joint_syndrome_X_information_bits":joint_info,
            "charged_secret_coset_information_loss_bits":raw_info-pinched_info,
            "raw_output_uniformity_residual":uniform_residual,
            "actual_pinching_vs_classical_secret_coset_average_residual":residual,
            "certified_information_lower_bits_exact":str(lower) if lower is not None else None,
            "all_original_secrets_enumerated":len(secrets),
            "all_residual_secrets_enumerated":Q**n,
            "selected_fixture_is_native_source_average_evidence":False,
            "likelihood_tables_are_polynomial_decoders":False}
    if coarse_bits==1:
        result["parity_compression_plan_on_example_measured_zero_syndrome"] = coordinate_plan(A,t,[0]*n,coarse_bits=1)
        result["actual_compiler_must_use_realized_syndrome_not_postselect_zero"] = True
    return result


def build_report():
    return {"status":"NATIVE_COARSE_READOUT_LINEAR_INFORMATION_DECODER_OPEN",
            "finite_controls":[finite_control(A,t,v) for A,t,v in (
                (((1,2,4,8,16),),6,Fraction(1)),
                (((1,2,4,8,16),),6,Fraction(7,8)),
                (((1,2,4,8,16),),6,Fraction(0)),
                (((1,2,4,0,0,0),(0,0,0,1,2,4)),4,Fraction(3,4)),
                (((0,0,0,0,0),),4,Fraction(1)))]+
                [finite_control(((1,2,4,8,16),),6,Fraction(31,32),common_mode=True)]+
                [finite_control(((1,2,4,8,16),),6,v,coarse_bits=1) for v in (Fraction(1),Fraction(3,4),Fraction(0))],
            "native_frontiers":[native_frontier(n,coarse_bits=b,width_multiple=w) for b,w in ((1,3),(2,5)) for n in (16,32,64,128,256,1024)],
            "entropy_series_log_constant_certificate":{"exp_7_over_10_degree3_lower_exact":"12013/6000",
                                                       "therefore_inverse_ln2_strictly_larger_than":"10/7"},
            "actual_positive_information_lower_bound_not_Holevo_only":True,
            "any_secret_independent_correlated_Z_fault_distribution_with_marginal_visibility_lower_bound_covered":True,
            "general_nonunital_noise_or_secret_dependent_faults_covered":False,
            "mod4_width3n_upper_bound_does_not_cover_mod2_or_every_packet_width":True,
            "full_secret_negation_alias_of_real_readout_removed":False,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,
            "novelty_claim":False,"efficient_decoder_supplied":False,
            "actual_natural_source_noise_certified":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"native_frontiers":[
        {"n":c["components"],"coarse_bits":c["measured_coarse_bits_per_component"],"width":c["physical_width"],
         "information_lower_bits":float(Fraction(c["discard_syndrome_fixed_X_information_lower_bits_exact"]))}
        for c in report["native_frontiers"]],"efficient_decoder":False}))


if __name__ == "__main__":
    main()
