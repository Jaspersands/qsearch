"""Direct full-secret DCP readout from an accessible purified witness finder.

LOCAL DERIVATION / REVIEW PENDING. No efficient finder or novelty claimed.
No parity chart, binary rank abort, matching or final-bit completion needed.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_bell_inference_kernel import exact
from dcp_dense_phase_transport import group_index, group_vector
from dcp_partial_witness_readout import correlated_attempt_failure_bound
from dcp_physical_phase_noise import read
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/dcp_direct_witness_filter.json"


def purified_finder_interface_gate(*, known_uniform_bounded_circuit=False,
                                   accessible_purification_and_inverse=False,
                                   preserves_classical_target_register=False,
                                   verifiable_boolean_output=False,
                                   native_independent_target_coverage_proved=False,
                                   no_unknown_state_or_unavailable_oracle_inverse=False):
    declarations = {
        "known uniform bounded circuit": known_uniform_bounded_circuit,
        "accessible retained purification and circuit inverse": accessible_purification_and_inverse,
        "unchanged classical target control": preserves_classical_target_register,
        "verified Boolean witness output": verifiable_boolean_output,
        "native IID labels and independent full-target coverage": native_independent_target_coverage_proved,
        "no unavailable unknown-state or oracle inverse": no_unknown_state_or_unavailable_oracle_inverse,
    }
    return {"issues": [key for key, value in declarations.items() if not value],
            "obligations_satisfied_as_declared": all(declarations.values()),
            "declarations_prove_an_algorithm": False,
            "deterministic_canonical_output_or_uniform_fiber_state_required": False,
            "arbitrary_measured_output_only_black_box_suffices": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def direct_filter_resource_certificate(n, modulus_bits, overhead_bits, coverage_lower_bound,
                                       attempts, *, markov_factor=4):
    _positive_integer(n, "dimension")
    _positive_integer(modulus_bits, "full modulus bits")
    _positive_integer(attempts, "preallocated complete attempts")
    if modulus_bits < 2 or type(overhead_bits) is not int or overhead_bits < 0:
        raise ValueError("modulus>=4 and nonnegative density overhead required")
    beta = Fraction(coverage_lower_bound)
    if not 0 < beta <= 1:
        raise ValueError("positive unconditional verified target coverage required")
    m = n * modulus_bits + overhead_bits
    verification = (attempts - 1).bit_length() + 32
    M = m + verification
    ideal = beta**2 / (1 << overhead_bits)
    amplification = correlated_attempt_failure_bound(ideal, Fraction(M, n*modulus_bits), attempts,
                                                     markov_factor=markov_factor, verification_states=verification)
    return {"status": "CONDITIONAL_DIRECT_FULL_SECRET_FILTER_NOT_SOLVER",
            "dimension": n, "full_modulus_bits": modulus_bits, "density_overhead_bits": overhead_bits,
            "original_phase_states_per_filter_attempt": m,
            "original_states_per_complete_attempt": M,
            "original_states_preallocated_for_all_attempts": attempts*M,
            "fresh_candidate_verification_states": verification,
            "assumed_unconditional_full_target_witness_coverage_lower_bound": exact(beta),
            "ideal_full_secret_success_per_original_attempt_lower_bound": exact(ideal),
            "finder_calls_per_attempt": {"forward_known_purified_circuit": 1, "inverse_known_purified_circuit": 1},
            "target_or_label_dependent_output_garbage_allowed_if_accessibly_uncomputed": True,
            "deterministic_witness_fiber_uniformity_or_canonicalization_required": False,
            "parity_measurement_binary_rank_rejection_or_target_alignment_required": False,
            "full_secret_top_bit_completion_required": False,
            "amplification": amplification,
            "full_secret_failure_bound_below_one_third_as_declared": read(amplification[
                "total_algorithm_failure_probability_upper_bound"]) < Fraction(1,3),
            "native_lattice_state_supply_gauge_lineage_and_gate_precision_composed": False,
            "finder_coverage_is_assumed_not_measured_by_scaling_ledger": True,
            "uniform_polynomial_finder_supplied": False,
            "independent_mathematical_review": False,
            "candidate_record_accepted": False, "novelty_claim": False, "speedup_claim_allowed": False}


def _source(labels, modulus, maximum_width=5):
    if type(modulus) is not int or modulus < 4 or modulus & (modulus-1):
        raise ValueError("power-of-two full modulus>=4 required")
    A = tuple(tuple(row) for row in labels)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty rectangular label matrix required")
    n, m = len(A), len(A[0])
    if m > maximum_width or modulus**n > 16 or any(type(a) is not int or not 0 <= a < modulus for row in A for a in row):
        raise ValueError("canonical labels within bounded calibration budget required")
    targets = [group_index(tuple(sum(a*(x>>i&1) for i,a in enumerate(row)) % modulus for row in A), modulus)
               for x in range(1 << m)]
    return A, targets, modulus**n


def bounded_purified_filter_control(labels, modulus, solver_unitaries, *, maximum_width=5):
    """Simulate actual compute/verify/XOR/uncompute, with arbitrary solver garbage."""
    A, targets, G = _source(labels, modulus, maximum_width)
    n, N = len(A), len(targets)
    if len(solver_unitaries) != G:
        raise ValueError("one known target-controlled unitary per bounded target required")
    U = [np.asarray(matrix, dtype=complex) for matrix in solver_unitaries]
    D = U[0].shape[0] if U[0].ndim == 2 else 0
    if not D or D % N or D > 128 or any(matrix.shape != (D,D) or not np.isfinite(matrix).all() for matrix in U):
        raise ValueError("bounded unitary workspace with explicit witness and history registers required")
    unitarity = max(float(np.max(np.abs(matrix.conj().T@matrix-np.eye(D)))) for matrix in U)
    if unitarity > 1e-10:
        raise ValueError("solver is not an accessible unitary purification")
    weights = [float(sum(abs(matrix[w,0])**2 for w in range(D) if targets[w%N] == t)) for t,matrix in enumerate(U)]
    clean_columns = np.zeros((G,N),dtype=complex)
    # For each original word, target is computed before the solver is invoked.
    for x,t in enumerate(targets):
        state = np.zeros((N,D,2),dtype=complex)
        state[x,:,0] = U[t][:,0]
        flagged = np.zeros_like(state)
        for w in range(D):
            valid = targets[w%N] == t
            flag = int(valid and w%N == x)
            flagged[x,w,flag] = state[x,w,0]
        erased = np.zeros_like(state)
        for y,w,flag in itertools.product(range(N),range(D),(0,1)):
            erased[y^(w%N),w,flag] = flagged[y,w,flag]
        cleaned = np.einsum("ab,xbh->xah",U[t].conj().T,erased)
        assert np.max(np.abs(cleaned[1:,0,1])) < 1e-12
        clean_columns[t,x] = cleaned[0,0,1]
        assert abs(clean_columns[t,x] - sum(abs(U[t][w,0])**2 for w in range(x,D,N))) < 1e-12
    predicted = np.zeros_like(clean_columns)
    for x,t in enumerate(targets):
        predicted[t,x] = sum(abs(U[t][w,0])**2 for w in range(x,D,N))
    operator_residual = float(np.max(np.abs(clean_columns-predicted)))
    operator_norm = float(np.linalg.norm(clean_columns,2))
    assert operator_norm <= 1+1e-10
    herald = sum(a*a for a in weights)/N
    correct = sum(weights)**2/(N*G)
    secret_residual = 0.0
    for s_index in range(G):
        secret = group_vector(s_index,n,modulus)
        phase = np.array([np.exp(2j*np.pi*sum(a*b for a,b in zip(secret,group_vector(t,n,modulus)))/modulus)
                          for t in targets]) / math.sqrt(N)
        selected = clean_columns @ phase
        expected = np.array([weights[t]*np.exp(2j*np.pi*sum(a*b for a,b in zip(secret,group_vector(t,n,modulus)))/modulus)
                             for t in range(G)]) / math.sqrt(N)
        assert np.max(np.abs(selected-expected)) < 1e-12
        amplitude = sum(selected[t]*np.exp(-2j*np.pi*sum(a*b for a,b in zip(secret,group_vector(t,n,modulus)))/modulus)
                        for t in range(G)) / math.sqrt(G)
        secret_residual = max(secret_residual,abs(abs(amplitude)**2-correct))
        assert abs(float(np.vdot(selected,selected).real)-herald) < 1e-12
    assert secret_residual < 1e-12
    return {"labels": A, "full_modulus": modulus, "physical_width": len(A[0]),
            "workspace_basis_dimension": D, "target_verified_output_probabilities": weights,
            "bounded_solver_output_columns": [[{"real": float(a.real), "imag": float(a.imag)} for a in matrix[:,0]]
                                              for matrix in U],
            "unconditional_independent_target_witness_coverage": sum(weights)/G,
            "clean_filter_matrix": clean_columns.real.tolist(),
            "clean_filter_operator_residual": operator_residual,
            "clean_filter_operator_norm": operator_norm, "solver_unitarity_residual": unitarity,
            "herald_probability_after_all_workspace_zero_projection": herald,
            "correct_full_secret_probability_for_every_secret": correct,
            "which_target_solver_output_kept_correct_probability": sum(weights)/(N*G),
            "conditional_correct_readout_given_herald": correct/herald if herald else 0.0,
            "fixed_secret_controls": G, "fixed_secret_probability_residual": secret_residual,
            "bounded_matrix_fixture_is_uniform_polynomial_finder": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _unitary_with_first_column(column, seed):
    rng = np.random.default_rng(seed)
    first = np.asarray(column,dtype=complex)
    if not np.isclose(np.vdot(first,first),1):
        raise ValueError("normalized purified solver output required")
    matrix = rng.normal(size=(len(first),len(first))) + 1j*rng.normal(size=(len(first),len(first)))
    matrix[:,0] = first
    Q,_ = np.linalg.qr(matrix)
    Q[:,0] *= np.vdot(Q[:,0],first)
    assert np.max(np.abs(Q[:,0]-first)) < 1e-12
    return Q


def bounded_tagged_solver_fixture(labels, modulus, target_successes, *, seed=317):
    """Every target has orthogonal history; success amplitudes have random phases."""
    A,targets,G = _source(labels,modulus)
    N,D = len(targets), len(targets)*G
    if len(target_successes) != G or D>128:
        raise ValueError("bounded per-target probabilities required")
    rng = np.random.default_rng(seed)
    unitaries=[]
    for t,coverage in enumerate(target_successes):
        coverage=float(coverage)
        valid=[x for x in range(N) if targets[x]==t]
        invalid=[x for x in range(N) if targets[x]!=t]
        if not 0<=coverage<=1 or (coverage and not valid) or (coverage<1 and not invalid):
            raise ValueError("coverage incompatible with actual physical fibers")
        column=np.zeros(D,dtype=complex)
        for words,mass in ((valid,coverage),(invalid,1-coverage)):
            if not mass:
                continue
            amplitudes=rng.normal(size=len(words))+1j*rng.normal(size=len(words))
            amplitudes*=math.sqrt(mass)/np.linalg.norm(amplitudes)
            for x,a in zip(words,amplitudes):
                column[t*N+x]=a
        unitaries.append(_unitary_with_first_column(column,seed+t))
    return unitaries


def run_controls():
    controls=[]
    for A,q,weights in ((((1,1,2),),4,(Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1))),
                         (((2,0,2),),4,(Fraction(1),Fraction(0),Fraction(1,2),Fraction(0))),
                         (((1,0,2,0),(0,1,0,2)),4,(Fraction(1,2),)*16)):
        # The n2 fixture is capped at128 workspace states: no target history tags there.
        if len(weights)*(1<<len(A[0]))>128:
            rng=np.random.default_rng(401)
            matrices=[]
            _,targets,G=_source(A,q)
            for t,coverage in enumerate(weights):
                column=np.zeros(len(targets),dtype=complex)
                for valid,mass in ((True,float(coverage)),(False,1-float(coverage))):
                    words=[x for x in range(len(targets)) if (targets[x]==t)==valid]
                    phases=np.exp(1j*rng.uniform(0,2*np.pi,size=len(words)))
                    for x,a in zip(words,phases*math.sqrt(mass/len(words))):
                        column[x]=a
                matrices.append(_unitary_with_first_column(column,401+t))
        else:
            matrices=bounded_tagged_solver_fixture(A,q,weights)
        controls.append(bounded_purified_filter_control(A,q,matrices))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "known_purified_quantum_finder_controls": controls,
            "conditional_raw_full_secret_resource_ledgers": [direct_filter_resource_certificate(
                n,4*n+1,d,Fraction(1,n*n),(1<<(40+d))*n**4)
                for n,d in ((8,0),(8,16),(16,0),(16,16),(32,0))],
            "claim_gate": {"known_purified_quantum_finder_noncanonical_outputs_allowed": True,
                           "raw_phase_source_needs_no_parity_rank_alignment_or_completion": True,
                           "output_only_measured_black_box_automatically_suffices": False,
                           "quantum_arithmetic_finder_constructed": False,
                           "independent_mathematical_review": False,
                           "full_native_lattice_composition_verified": False,
                           "candidate_record_accepted": False,"novelty_claim": False,"speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__),ROOT/"theorems/dcp_partial_witness_readout.py",
                                            ROOT/"theorems/dcp_dense_phase_transport.py",ROOT/"theorems/dcp_physical_phase_noise.py")}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args=parser.parse_args()
    report=run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"claim_gate":report["claim_gate"]},indent=2))


if __name__ == "__main__":
    main()
