"""Source-weighted rank/depth cut for fixed native orbit filters.

LOCAL DERIVATION / REVIEW PENDING. This audits a specific two-reflection
receiver, not arbitrary collective measurements or quantum algorithms.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json

from flint import fmpz_poly
import numpy as np

from cyclic_centre_state_hsp_receiver import integer
from cyclotomic_rescaling_gate import pairing
from native_orbit_source_access import ROOT, inverse
from native_state_hsp_bridge import NativeGroup, ring_words

REPORT = ROOT/"research/reductions/native_noncentral_filter_tradeoff.json"
X = fmpz_poly([0, 1])


def amplitude_polynomial(iterations):
    integer(iterations, "relative iterations", 0)
    a, b = fmpz_poly([1]), fmpz_poly([3, -4])
    if iterations == 0:
        return a
    for _ in range(1, iterations):
        a, b = b, 2*(1-2*X)*b-a
    return b


def second_kind_polynomial(degree):
    integer(degree, "second-kind polynomial degree", 0)
    a, b = fmpz_poly([1]), fmpz_poly([2, -4])
    if degree == 0:
        return a
    for _ in range(1, degree):
        a, b = b, 2*(1-2*X)*b-a
    return b


def coefficients(p):
    return [str(p[i]) for i in range(len(p))]


def amplification_sos(iterations):
    """Exact interval-[0,1] SOS for (2k+1)^2*x-x*a_k(x)^2."""
    a = amplitude_polynomial(iterations)
    n = 2*iterations+1
    lhs = n*n*X-X*a*a
    rhs = fmpz_poly([])
    terms = []
    for d in range(1, 2*iterations+1):
        if d % 2:
            p, weight, factor = amplitude_polynomial((d-1)//2), 4*(n-d), "x_squared"
            rhs += weight*X*X*p*p
        else:
            p, weight, factor = second_kind_polynomial(d//2-1), 16*(n-d), "x_squared_times_one_minus_x"
            rhs += weight*X*X*(1-X)*p*p
        terms.append({"separation": d, "positive_weight": weight, "nonnegative_interval_factor": factor,
                      "squared_polynomial_ascending_integer_coefficients": coefficients(p)})
    if lhs != rhs:
        raise ArithmeticError("relative-amplification interval SOS does not reconstruct the exact gap")
    return {"iterations": iterations, "amplitude_polynomial_ascending_integer_coefficients": coefficients(a),
            "exact_gap_polynomial_ascending_integer_coefficients": coefficients(lhs), "positive_SOS_terms": terms,
            "inequality": "x*a_k(x)^2 <= (2k+1)^2*x for every x in [0,1]"}


def spectral_probability(x, iterations):
    x = Fraction(x)
    if not 0 <= x <= 1:
        raise ValueError("compressed projector spectrum must lie in [0,1]")
    a = amplitude_polynomial(iterations)
    value = Fraction()
    for i in reversed(range(len(a))):
        value = value*x+int(a[i])
    return x*value*value


def rank_depth_ledger(level, dimension, rank, iterations, original_copies=1):
    for x, name, minimum in ((level,"native level",1), (dimension,"native dimension",1),
                             (rank,"group filter rank",1), (iterations,"iterations",0),
                             (original_copies,"original source copies",1)):
        integer(x, name, minimum)
    if rank > 3**(level*dimension+1):
        raise ValueError("filter rank exceeds the group register dimension")
    numerator = rank*(2*iterations+1)**2
    exponent = level*dimension
    return {"native_level": level, "native_dimension": dimension,
            "original_IID_native_copies_in_same_group_orbit": original_copies,
            "group_filter_rank": rank, "relative_iterations": iterations,
            "raw_success_probability_upper_bound": {"cap": 1, "numerator": numerator,
                                                     "denominator": {"base": 3, "exponent": exponent}},
            "same_group_orbit_copy_count_does_not_change_group_marginal": True,
            "known_controlled_original_R_calls": original_copies*(2*iterations+1),
            "same_group_coordinate_trits": exponent+1,
            "rank_is_not_qubits_or_memory_bits": True,
            "filter_must_be_independent_of_observed_native_frequency_labels": True,
            "label_adaptive_filters_covered": False,
            "different_or_adaptive_filters_covered": False,
            "arbitrary_noncentral_or_collective_receivers_covered": False,
            "unknown_seed_reflection_used": False}


def tensor(items):
    out = np.array([1.]) if items[0].ndim == 1 else np.ones((1,1))
    for item in items:
        out = np.kron(out, item)
    return out


def apply_filter(state, kind, pair_index, zero_rotation_mask):
    out = np.zeros_like(state)
    if kind == "identity_coordinate":
        out[0] = state[0]
    elif kind == "public_hidden_generator_pair":
        out[0] = out[pair_index] = (state[0]+state[pair_index])/2
    elif kind == "zero_rotation_coordinates":
        out[zero_rotation_mask] = state[zero_rotation_mask]
    else:
        raise ValueError("unknown public filter")
    return out


def native_control(level, secret, copies):
    integer(copies, "original copies", 1)
    if level not in (1,2) or copies not in (1,2):
        raise ValueError("complete noncentral controls use levels1-2 and copies1-2")
    G, labels = NativeGroup(level), ring_words(level)
    secret = G.vector((secret,))
    elements = tuple(((b,), t) for b, t in product(labels, range(3)))
    N, D = len(elements), 3**copies
    guess = G.hidden_elements(((1,0),))[1]  # Public fixed guess, never the tested secret.
    pair_index = elements.index(guess)
    H = set(G.hidden_elements(secret))
    matches = guess in H
    zero_rotation = np.array([t == 0 for _,t in elements])
    kinds = ("identity_coordinate", "public_hidden_generator_pair", "zero_rotation_coordinates")
    histories = {kind: np.zeros(7) for kind in kinds}
    density = np.zeros((N,N), complex)
    direct_diagonal = direct_separate = 0.
    maximum_polynomial_error = 0.
    normalizer = len(labels)**copies
    for cohort in product(labels, repeat=copies):
        states = [G.supplied_phase_state((a,), secret) for a in cohort]
        seed = tensor(states)
        actions = np.array([tensor([G.induced_action((a,), g) for a in cohort]) for g in elements])
        prepared = np.einsum("gij,j->gi", actions, seed)/np.sqrt(N)
        density += prepared@prepared.conj().T/normalizer
        E = (np.eye(D)+actions[pair_index]+actions[pair_index].conj().T)/3
        direct_diagonal += float(np.vdot(seed,E@seed).real)/normalizer
        single_probabilities = []
        for a, psi in zip(cohort, states):
            R = G.induced_action((a,), guess)
            E1 = (np.eye(3)+R+R.conj().T)/3
            single_probabilities.append(float(np.vdot(psi,E1@psi).real))
        direct_separate += float(np.prod(single_probabilities))/normalizer
        for kind in kinds:
            PV = apply_filter(actions/np.sqrt(N), kind, pair_index, zero_rotation)
            C = np.einsum("gji,gjk->ik", actions.conj()/np.sqrt(N), PV)
            eigenvalues, eigenvectors = np.linalg.eigh(C)
            state = prepared.copy()
            for iteration in range(7):
                good = apply_filter(state, kind, pair_index, zero_rotation)
                histories[kind][iteration] += float(np.vdot(good,good).real)/normalizer
                # Spectral evaluation avoids cancellation of high-degree coefficients.
                ak = np.ones(D)
                bk = 3-4*eigenvalues
                if iteration:
                    for _ in range(1, iteration):
                        ak, bk = bk, 2*(1-2*eigenvalues)*bk-ak
                    ak = bk
                predicted_seed = eigenvectors@(ak*(eigenvectors.conj().T@seed))
                predicted = apply_filter(np.einsum("gij,j->gi", actions, predicted_seed)/np.sqrt(N), kind, pair_index, zero_rotation)
                maximum_polynomial_error = max(maximum_polynomial_error,float(np.linalg.norm(good-predicted)))
                reflected = state-2*good
                returned = np.einsum("gji,gj->i",actions.conj(),reflected)/np.sqrt(N)
                state = 2*np.einsum("gij,j->gi",actions,returned)/np.sqrt(N)-reflected
    target = np.array([[int(G.compose(inverse(G,h),g) in H)/N for h in elements] for g in elements])
    density_error = float(np.linalg.norm(density-target))
    if max(density_error, maximum_polynomial_error) > 2e-11:
        raise ArithmeticError("actual diagonal-copy orbit or noncentral polynomial law failed")
    expected_diagonal = Fraction(1) if matches else Fraction(1,3)
    expected_separate = expected_diagonal**copies
    if max(abs(direct_diagonal-float(expected_diagonal)),abs(direct_separate-float(expected_separate))) > 2e-11:
        raise ArithmeticError("matched direct stabilizer measurement baseline failed")
    controls = []
    for kind in kinds:
        rank = len(labels) if kind == "zero_rotation_coordinates" else 1
        rows = []
        for k, actual in enumerate(histories[kind]):
            if kind == "identity_coordinate":
                exact = spectral_probability(Fraction(1,N),k)
            elif kind == "zero_rotation_coordinates":
                exact = spectral_probability(Fraction(1,3),k)
            else:
                high = spectral_probability(Fraction(2,N),k)
                low = spectral_probability(Fraction(1,2*N),k)
                exact = high if matches else (high+2*low)/3
            if abs(actual-float(exact)) > 2e-11:
                raise ArithmeticError("noncentral native source law differs from exact spectral mixture")
            bound = min(Fraction(1),Fraction(rank*(2*k+1)**2,3**level))
            if exact > bound:
                raise ArithmeticError("source-weighted rank/depth upper bound is violated")
            rows.append({"iterations": k, "actual_raw_success_probability": float(actual),
                         "exact_raw_success_probability": str(exact), "exact_rank_depth_upper_bound": str(bound),
                         "known_original_controlled_R_calls": copies*(2*k+1)})
        controls.append({"public_group_filter":kind,"group_filter_rank":rank,
                         "source_weighted_iteration_history":rows,
                         "high_rank_filter_has_a_single_public_rotation_digit_test":kind=="zero_rotation_coordinates"})
    return {"native_level":level,"native_secret":secret[0],"original_source_copies":copies,
            "group_dimension":N,"seed_dimension_per_public_label_cohort":D,
            "complete_public_label_cohort_count":normalizer,
            "public_fixed_generator_guess":guess,"fixed_guess_matches_hidden_generator":matches,
            "same_group_coset_density_error":density_error,
            "maximum_actual_vs_seed_polynomial_good_vector_error":maximum_polynomial_error,
            "noncentral_filters":controls,
            "direct_order_three_stabilizer_baseline":{
                "projector":"(I+R(k)+R(k)^dagger)/3 for PUBLIC fixed guess k",
                "actual_diagonal_tensor_acceptance":direct_diagonal,"exact_diagonal_tensor_acceptance":str(expected_diagonal),
                "actual_separate_copy_all_acceptance":direct_separate,"exact_separate_copy_all_acceptance":str(expected_separate),
                "separate_copy_false_guess_acceptance":"(1/3)^M under the unconditioned IID original source",
                "hidden_generator_search_space": {"base":3,"exponent":level},
                "known_controlled_original_R_calls_for_separate_copy_baseline": copies,
                "baseline_ignores_information_in_the_recorded_public_labels": True,
                "no_lower_bound_on_label_aware_inference_claimed": True,
                "efficient_full_secret_search_supplied":False,"classical_dequantization_claimed":False},
            "unknown_seed_reflection_supplied":False,"full_depth_receiver_supplied":False}


def label_adaptive_relocation_control(level):
    """Public abelian-frequency filter relocates, rather than decodes, a seed."""
    if level not in (3,4):
        raise ValueError("growing-root relocation calibration uses levels3-4")
    G, label = NativeGroup(level), ((1,0),)
    words = ring_words(level)
    elements = tuple(((b,),t) for b,t in product(words,range(3)))
    N, E = len(elements), len(words)
    characters = np.array([np.exp(2j*np.pi*float(pairing(label[0],b,level))) for b in words])
    P = np.zeros((N,N),complex)
    for t in range(3):
        indices = np.arange(t,N,3)
        P[np.ix_(indices,indices)] = np.outer(characters,characters.conj())/E
    actions = np.array([G.induced_action(label,g) for g in elements])
    V = actions.reshape(N*3,3)/np.sqrt(N)
    PV = (P@V.reshape(N,9)).reshape(N*3,3)
    C = V.conj().T@PV
    if np.linalg.norm(C-np.eye(3)/3)>2e-11:
        raise ArithmeticError("label-adaptive abelian filter does not have scalar compressionI/3")
    # Arbitrary reference-entangled seed: no unknown preparation/reflection oracle.
    seed = np.array([[1,0],[0,1],[1j,0]],complex)/np.sqrt(3)
    state = (V@seed).reshape(N,3,2)
    histories = []
    for k in range(3):
        good = (P@state.reshape(N,6)).reshape(N,3,2)
        exact = spectral_probability(Fraction(1,3),k)
        probability = float(np.vdot(good,good).real)
        scalar = Fraction()
        a = amplitude_polynomial(k)
        for i in reversed(range(len(a))):
            scalar = scalar/3+int(a[i])
        decoded = np.zeros_like(seed)
        for t in range(3):
            block = good[t::3,0,:]
            decoded[t] = characters.conj()@block/np.sqrt(E)
        decoded *= np.sqrt(3)/float(scalar)
        other_seed = good[:,1:,:]
        error = float(np.linalg.norm(decoded-seed))
        if max(abs(probability-float(exact)),error,float(np.linalg.norm(other_seed)))>2e-11:
            raise ArithmeticError("noncentral frequency success is not reference-preserving seed relocation")
        histories.append({"iterations":k,"actual_raw_success_probability":probability,
                          "exact_raw_success_probability":str(exact),"raw_failure_probability":1-probability,
                          "normalized_reference_entangled_seed_relocation_error":error,
                          "known_controlled_original_R_calls":2*k+1})
        reflected = state-2*good
        returned = np.einsum("gji,gjr->ir",actions.conj(),reflected)/np.sqrt(N)
        state = 2*np.einsum("gij,jr->gir",actions,returned)/np.sqrt(N)-reflected
    return {"native_level":level,"group_dimension":N,"public_frequency_label":label,
            "label_adaptive_group_filter_rank":3,
            "selected_abelian_frequency_is_the_observed_native_label":True,
            "filter_depends_on_secret":False,
            "known_abelian_frequency_recipe":"QFT on the normal translation coordinates; retain the observed label and all three rotations.",
            "compressed_operator":"I_seed/3",
            "source_label_blind_rank_bound_at_zero_iterations_NOT_APPLICABLE":str(Fraction(9,N)),
            "conditional_original_seed_and_reference_recovered_in_rotation_register":True,
            "seed_qutrit_output_is_known_basis_state_on_success":True,
            "source_copies_used":1,
            "iteration_histories":histories,
            "new_secret_information_extracted":False,
            "unknown_seed_reflection_supplied":False,
            "no_cloning_or_deterministic_success_claimed":True,
            "full_depth_secret_decoder_supplied":False}


def run_controls():
    return {"status":"NATIVE_NONCENTRAL_FIXED_FILTER_RANK_DEPTH_AUDIT_REVIEW_PENDING",
            "exact_amplification_interval_SOS_certificates":[amplification_sos(k) for k in range(9)],
            "complete_actual_native_controls":[native_control(r,s,m) for r in (1,2) for s in ((1,0),(2,0)) for m in (1,2)],
            "growing_root_label_adaptive_countercontrols":[label_adaptive_relocation_control(r) for r in (3,4)],
            "growing_rank_depth_ledgers":[rank_depth_ledger(r,n,n*r+1,n*r,n*r) for r,n in ((2,1),(8,8),(32,32),(128,128))],
            "bound":"p_k <= min(1,(2k+1)^2*rank(P)/3^(nr))",
            "same_group_diagonal_tensor_orbit_group_marginal_independent_of_copy_count":True,
            "only_fixed_filter_two_reflection_sequences_covered":True,
            "group_filter_must_ignore_observed_frequency_labels_for_exponential_rank_bound":True,
            "label_adaptive_filters_ruled_out":False,
            "rank_lower_bound_is_a_memory_lower_bound":False,
            "arbitrary_adaptive_collective_or_high_rank_receivers_ruled_out":False,
            "new_quantum_speedup_claimed":False,"novelty_claimed":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    out = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":out["status"],"complete_native_controls":len(out["complete_actual_native_controls"]),
                      "exact_SOS_certificates":len(out["exact_amplification_interval_SOS_certificates"])}))


if __name__ == "__main__":
    main()
