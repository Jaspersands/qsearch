"""Decisive native test of a proposed conjugate-register quadratic-DQI repair.

The pair-to-bilinear transform is constructive, and a public scaled-Vandermonde
decoder erases weight<=1 error labels. But it prepares a DIFFERENT objective.
Diagonal forms become unrestricted linear OPI; rank-one forms also absorb
into ordinary linear predicates. No repaired
max-QUADSAT algorithm, novelty, classical hardness or speedup is claimed.
Dense arrays/explicit target lists here are bounded physical calibrations.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, isqrt, prod, sqrt
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_opi import ring

REPORT = ROOT/"research/classical_baselines/conjugate_chirp_repair.json"


@dataclass(frozen=True)
class QuadraticInput:
    prime: int
    dimension: int
    points: tuple[int, ...]
    target_lists: tuple[tuple[int, ...], ...]
    form_kind: str = "diagonal"

    def __post_init__(self):
        ring(self.prime)
        integer(self.dimension, "polynomial coordinates", 2, len(self.points))
        if self.form_kind not in ("diagonal", "rank_one"):
            raise ValueError("explicit diagonal or rank-one quadratic form required")
        if (type(self.points) is not tuple or not self.points or len(set(self.points)) != len(self.points)
                or any(type(a) is not int or not 0 < a < self.prime for a in self.points)
                or type(self.target_lists) is not tuple or len(self.target_lists) != len(self.points)
                or any(type(row) is not tuple or not 0 < len(row) < self.prime
                       or row != tuple(sorted(set(row)))
                       or any(type(a) is not int or not 0 <= a < self.prime for a in row) for row in self.target_lists)):
            raise ValueError("canonical distinct points and explicit nontrivial target lists required")

    def coordinates(self, coefficients):
        coefficients = tuple(coefficients)
        if (len(coefficients) != self.dimension
                or any(type(a) is not int or not 0 <= a < self.prime for a in coefficients)):
            raise ValueError("canonical native coordinate vector required")
        return coefficients

    def values(self, coefficients):
        coefficients = self.coordinates(coefficients)
        out = []
        for a in self.points:
            y = 0
            for coefficient in reversed(coefficients):
                y = (y*a+coefficient) % self.prime
            out.append(y)
        return tuple(out)

    def good_direction(self, r):
        r = self.coordinates(r)
        return all(r) if self.form_kind == "diagonal" else all(self.values(r))

    def quadratic_values(self, x):
        x = self.coordinates(x)
        if self.form_kind == "diagonal":
            return self.values(tuple(a*a % self.prime for a in x))
        return tuple(a*a % self.prime for a in self.values(x))

    def specification(self):
        return {"prime": self.prime, "dimension": self.dimension, "points": list(self.points),
                "explicit_target_lists": [list(row) for row in self.target_lists],
                "form_kind": self.form_kind,
                "quadratic_forms": ("C_i=diag(1,a_i,...,a_i^(n-1))" if self.form_kind == "diagonal"
                                    else "C_i=v_i*v_i^T, v_i=(1,a_i,...,a_i^(n-1))"),
                "lists_are_given_explicitly_not_hidden_oracles": True,
                "small_controls_are_not_claimed_hard_instances": True}


def decode_weight_one(problem, r, syndrome):
    """Public decoder, no true error label as input and no field-value search.

    Diagonal: divide s_j by r_j, then recover a_i=s_1/s_0 and y_i=s_0.
    Rank-one: s_j=y_i*R(a_i)*a_i^j; then y_i=s_0/R(a_i).
    Return a canonical error-basis index or None outside the promise.
    """
    p = problem.prime
    r, syndrome = problem.coordinates(r), problem.coordinates(syndrome)
    if not problem.good_direction(r):
        return None
    if problem.form_kind == "diagonal":
        syndrome = tuple(s*pow(int(a), -1, p) % p for s, a in zip(syndrome, r))
    if not any(syndrome):
        return 0
    if not syndrome[0]:
        return None
    a = syndrome[1]*pow(syndrome[0], -1, p) % p
    if a not in problem.points or any(z != syndrome[0]*pow(a, j, p) % p for j, z in enumerate(syndrome)):
        return None
    i = problem.points.index(a)
    beta = 1 if problem.form_kind == "diagonal" else problem.values(r)[i]
    y = syndrome[0]*pow(beta, -1, p) % p
    return 1+i*(p-1)+y-1


def postselection_bound(prime, dimension, list_densities, degree):
    """Exact Cauchy bound for any normalized shell weights through this degree.

    |P|^2 <= sum_(k<=ell) binom(m,k)*A^(2k). Conditioning a paired output on
    z=0 succeeds at most this/p^n, even after the public good-r projection.
    A bounds every centered unit-variance local predicate. This is a bound
    on THIS repair, not a lower bound on other preparation algorithms.
    """
    ring(prime)
    integer(dimension, "output coordinates", 1, 4096)
    densities = tuple(map(Fraction, list_densities))
    if not densities or any(not 0 < rho < 1 or (rho*prime).denominator != 1 for rho in densities):
        raise ValueError("nontrivial exact input-list densities realizable over Fp required")
    integer(degree, "shell polynomial degree", 0, len(densities))
    if (dimension+degree+3)*prime.bit_length()+(degree+1)*len(densities).bit_length() > 12000:
        raise ValueError("UNKNOWN: exact bound serialization cap, not a mathematical failure")
    A2 = max(max(rho/(1-rho), (1-rho)/rho) for rho in densities)
    height = sum(Fraction(comb(len(densities), k))*A2**k for k in range(degree+1))
    probability = min(Fraction(1), height/prime**dimension)
    return {"prime_decimal": str(prime), "dimension": dimension, "constraints": len(densities),
            "list_densities_exact": list(map(str, densities)), "one_register_basis_size_decimal": str(prime**dimension),
            "filter_degree": degree, "squared_local_magnitude_bound": str(A2),
            "squared_filter_height_bound": str(height), "z_zero_probability_upper": str(probability),
            "straight_repetitions_expected_lower": str(1/probability),
            "repetitions_pay_both_chirps_and_error_state_preparation": True,
            "bound_applies_only_to_proposed_z_zero_repair": True,
            "all_state_preparation_algorithms_lower_bounded": False}


def _vectors(p, n):
    return np.array(list(product(range(p), repeat=n)), dtype=np.int64)


def diagonal_score_washout_bound(prime, dimension, list_densities):
    """Uniform-in-q expected-score bound for x_j=(r_j+q_j/r_j)/2.

    Assumes the standard Weil Kloosterman bound and quadratic Gauss identity.
    The reciprocal-square character splits into Kloosterman+Salie sums, each
    at most2*sqrt(p). Conditional coordinates are independent. Fourier
    Cauchy then bounds each arbitrary input-list expectation. This does NOT
    bound score tails, whole output TV or alternative quantum algorithms.
    """
    ring(prime)
    integer(dimension, "original quadratic coordinates", 1, 4096)
    densities = tuple(map(Fraction, list_densities))
    if not densities or any(not 0 < rho < 1 or (rho*prime).denominator != 1 for rho in densities):
        raise ValueError("nontrivial exact input-list densities realizable over Fp required")
    if (2*dimension+3)*prime.bit_length()+len(densities).bit_length() > 12000:
        raise ValueError("UNKNOWN: exact bound serialization cap, not a mathematical failure")
    root = isqrt(prime)
    eta = min(Fraction(1), Fraction(4*(root+1), prime-1))
    sigma = min(Fraction(1), Fraction(1, root))
    paired, uniform = [], []
    for rho in densities:
        size = int(rho*prime)
        numerator = (prime-1)*size*(prime-size)
        ceiling = isqrt(numerator)
        ceiling += int(ceiling*ceiling < numerator)
        prefactor = Fraction(ceiling, prime)
        cap = max(rho, 1-rho)
        paired.append(min(cap, prefactor*eta**dimension))
        uniform.append(min(cap, prefactor*sigma**dimension))
    paired_mean, uniform_mean = sum(paired)/len(densities), sum(uniform)/len(densities)
    return {"prime_decimal": str(prime), "dimension": dimension, "constraints": len(densities),
            "list_densities_exact": list(map(str, densities)),
            "one_coordinate_character_modulus_upper": str(eta),
            "uniform_x_one_coordinate_Gauss_upper": str(sigma),
            "paired_expected_satisfied_fraction_bias_upper": str(paired_mean),
            "uniform_classical_x_expected_fraction_bias_upper": str(uniform_mean),
            "paired_minus_uniform_classical_expected_fraction_advantage_upper": str(min(Fraction(1), paired_mean+uniform_mean)),
            "paired_bound_uniform_over_arbitrary_input_q_distribution": True,
            "r_uniform_independent_over_Fp_star_and_all_a_i_nonzero_required": True,
            "score_tails_or_full_output_TV_bounded": False,
            "external_Weil_Kloosterman_bound_assumed_not_formally_verified_here": True,
            "local_derivation_review_pending": True}


def reciprocal_character_control(prime, coefficient, frequency):
    """Finite independent sum calibration; not a proof of the external Weil bound."""
    ring(prime)
    integer(prime, "finite exponential-sum calibration prime", 3, 257)
    integer(coefficient, "fixed q coordinate", 0, prime-1)
    integer(frequency, "nonzero additive frequency", 1, prime-1)
    p, c, b = prime, coefficient, frequency
    e = lambda z: np.exp(2j*np.pi*(z % p)/p)
    chi = lambda z: 0 if z % p == 0 else (1 if pow(z % p, (p-1)//2, p) == 1 else -1)
    A, B = b*pow(4, -1, p) % p, b*c*c*pow(4, -1, p) % p
    direct = sum(e(b*pow((r+c*pow(r, -1, p))*pow(2, -1, p) % p, 2, p)) for r in range(1, p))/(p-1)
    K = sum(e(A*z+B*pow(z, -1, p)) for z in range(1, p))
    S = sum(chi(z)*e(A*z+B*pow(z, -1, p)) for z in range(1, p))
    predicted = e(b*c*pow(2, -1, p))*(K+S)/(p-1)
    G = sum(e(z*z) for z in range(p))
    salie = (G*chi(B)*sum(e(v) for v in range(p) if v*v % p == 4*A*B % p)
             if B else G*chi(A))
    return {"prime": p, "coefficient": c, "frequency": b,
            "direct_character_modulus": float(abs(direct)), "Kloosterman_modulus": float(abs(K)),
            "Salie_modulus": float(abs(S)), "decomposition_error": float(abs(direct-predicted)),
            "Salie_Gauss_identity_error": float(abs(S-salie)),
            "standard_uniform_character_upper": min(1.0, 4*sqrt(p)/(p-1))}


def diagonal_tail_bound(prime, dimension, constraints, gap, moment_pairs):
    """Separate joint-moment tail certificate for THIS diagonal paired readout.

    k=2s joint indicators differ from independent uniforms by at most
    delta_k=ceil(sqrt(p))^k*eta^floor(n/k). A nonzero k-term exponential
    sequence cannot have k consecutive zeros (Vandermonde invertibility).
    Comparing centered moments costs at most (2m)^k*delta_k. Symmetrization
    gives the independent moment <=(2s-1)!!*m^s. No full-output TV claim.
    """
    ring(prime)
    integer(dimension, "diagonal coordinates", 2, 4096)
    integer(constraints, "distinct nonzero evaluation points", dimension, min(prime-1, 65536))
    integer(moment_pairs, "centered even-moment half-order", 1, min(32, dimension//2))
    gap = Fraction(gap)
    if not 0 < gap < 1:
        raise ValueError("fixed positive satisfied-fraction gap below one required")
    k, s, p = 2*moment_pairs, moment_pairs, prime
    if ((dimension//k+k+3)*p.bit_length()+k*(gap.numerator.bit_length()+gap.denominator.bit_length()) > 12000):
        raise ValueError("UNKNOWN: exact tail-bound serialization cap")
    root = isqrt(p)+1
    eta = min(Fraction(1), Fraction(4*root, p-1))
    joint = min(Fraction(1), root**k*eta**(dimension//k))
    pairings = prod(range(1, 2*s, 2))
    independent = Fraction(pairings, constraints**s)/gap**k
    dependency = (2/gap)**k*joint
    return {"prime_decimal": str(p), "dimension": dimension, "constraints": constraints,
            "satisfied_fraction_gap_exact": str(gap), "even_centered_moment_order": k,
            "event": "satisfied_fraction >= mean_i(|F_i|/p) + gap",
            "minimum_nonzero_Fourier_coordinates_for_k_constraints": dimension//k,
            "joint_indicator_independence_error_upper": str(joint),
            "independent_centered_moment_upper": str(pairings*constraints**s),
            "independent_tail_contribution_upper": str(independent),
            "joint_dependence_tail_contribution_upper": str(dependency),
            "tail_probability_upper": str(min(Fraction(1), independent+dependency)),
            "any_input_q_distribution_covered_for_THIS_readout": True,
            "distinct_nonzero_points_and_independent_uniform_Fp_star_r_required": True,
            "polynomial_repetition_consequence_requires_logp_polynomial_in_n": True,
            "external_Weil_bound_and_local_derivation_review_pending": True,
            "full_output_TV_or_other_quantum_algorithms_bounded": False}


def _index(vectors, p):
    n = vectors.shape[-1]
    return sum(vectors[..., j]*p**(n-1-j) for j in range(n))


def native_control(problem, weights=(Fraction(3, 5), Fraction(4, 5))):
    """Execute both chirps, coordinate bijection, QFT, decoder erasure and inverse.

    Error-label input preparation and reversible decoder gates are NOT compiled.
    Finite error alphabet and explicit lists charge classical tables honestly.
    """
    p, n, m = problem.prime, problem.dimension, len(problem.points)
    weights = tuple(map(Fraction, weights))
    if len(weights) != 2 or sum(x*x for x in weights) != 1:
        raise ValueError("two exactly normalized rational shell weights required")
    Q, D = p**n, 1+m*(p-1)
    if D*Q*Q > 2_000_000:
        raise ValueError("UNKNOWN: exponential native-calibration cap, not algorithmic hardness")
    vectors = _vectors(p, n)
    evaluations = np.array([problem.values(tuple(map(int, x))) for x in vectors])
    quadratics = np.array([problem.quadratic_values(tuple(map(int, x))) for x in vectors])
    local, coefficients = [], [complex(float(weights[0]))]
    for target in problem.target_lists:
        rho = Fraction(len(target), p)
        g = np.array([float(Fraction(int(x in target))-rho)/sqrt(float(rho*(1-rho))) for x in range(p)])
        local.append(g)
        fourier = np.fft.fft(g)/p
        coefficients.extend(float(weights[1])*fourier[1:]/sqrt(m))
    coefficients = np.array(coefficients)
    if abs(np.vdot(coefficients, coefficients).real-1) > 1e-12:
        raise ArithmeticError("input shell/Fourier coefficients are not normalized")
    # Literal labeled pair in (error,x,z) order, not an assumed bilinear state.
    source = np.empty((D, Q, Q), dtype=complex)
    source[0] = coefficients[0]/Q
    for i in range(m):
        phase = (quadratics[:, i, None]-quadratics[None, :, i]) % p
        for y in range(1, p):
            e = 1+i*(p-1)+y-1
            source[e] = coefficients[e]*np.exp(2j*np.pi*y*phase/p)/Q
    inverse2 = pow(2, -1, p)
    # r=x-z, u=x+z; this is a bijection in odd characteristic.
    r = vectors[:, None, :]
    u = vectors[None, :, :]
    x_map = _index((u+r)*inverse2 % p, p)
    z_map = _index((u-r)*inverse2 % p, p)
    ru = source[:, x_map, z_map]
    transformed = np.fft.fftn(ru.reshape((D, Q)+(p,)*n), axes=tuple(range(2, n+2)), norm="ortho").reshape(D, Q, Q)
    good = np.array([problem.good_direction(tuple(map(int, r))) for r in vectors])
    if not any(good):
        raise ValueError("UNKNOWN: this calibration has no good direction")
    expected = np.zeros_like(transformed)
    for r_index, r_vector in enumerate(vectors):
        for e in range(D):
            if not e:
                syndrome = np.zeros(n, dtype=np.int64)
            else:
                i, y0 = divmod(e-1, p-1)
                a, y = problem.points[i], y0+1
                syndrome = np.array([int(r_vector[j] if problem.form_kind == "diagonal" else evaluations[r_index, i])
                                     *y*pow(a, j, p) % p for j in range(n)])
            expected[e, r_index, int(_index(syndrome, p))] = coefficients[e]/sqrt(Q)
    phase_transform_error = float(np.max(np.abs(transformed-expected)))
    # Each (r,syndrome) uses one decoder value to shift EVERY error basis state.
    # Hence the operation extends to a permutation, not a map chosen using true e.
    erased = np.empty_like(transformed)
    decoder_calls = 0
    for r_index, r_vector in enumerate(vectors):
        rv = tuple(map(int, r_vector))
        for k, syndrome in enumerate(vectors):
            decoded = decode_weight_one(problem, rv, tuple(map(int, syndrome)))
            decoder_calls += 1
            erased[:, r_index, k] = np.roll(transformed[:, r_index, k], -(decoded or 0))
    unprojected_leak = float(np.vdot(erased[1:], erased[1:]).real)
    erased[:, ~good, :] = 0
    good_probability = Fraction(int(sum(good)), Q)
    residual_label = float(np.vdot(erased[1:], erased[1:]).real)
    if residual_label > 1e-20:
        raise ArithmeticError("public promised decoder did not erase the error register")
    output_ru = np.fft.ifftn(erased[0].reshape((Q,)+(p,)*n), axes=tuple(range(1, n+1)), norm="ortho").reshape(Q, Q)
    # Independent direct target polynomial, using native predicate values.
    direct = np.empty((Q, Q), dtype=complex)
    vandermonde = np.array([[pow(a, j, p) for j in range(n)] for a in problem.points])
    for j in range(Q):
        argument = (((vectors*vectors[j])@vandermonde.T).T % p if problem.form_kind == "diagonal"
                    else evaluations[j, :, None]*evaluations.T % p)
        direct[j] = (float(weights[0])+float(weights[1])/sqrt(m)*sum(g[arg] for g, arg in zip(local, argument)))/Q
    direct[~good] = 0
    direct_error = float(np.max(np.abs(output_ru-direct)))
    if abs(np.vdot(output_ru, output_ru).real-float(good_probability)) > 1e-12 or direct_error > 1e-12:
        raise ArithmeticError("erased output is not the bilinear filter with charged projection")
    pair = np.empty((Q, Q), dtype=complex)
    pair[x_map, z_map] = output_ru/sqrt(float(good_probability))
    target = (float(weights[0])+float(weights[1])/sqrt(m)*sum(g[quadratics[:, i]] for i, g in enumerate(local)))
    if np.linalg.norm(target) < 1e-14:
        raise ValueError("UNKNOWN: vanishing calibrated target norm, not unsatisfiability")
    target = target/np.linalg.norm(target)
    marginal = pair@pair.conj().T
    fidelity = float(np.vdot(target, marginal@target).real)
    purity = float(np.trace(marginal@marginal).real)
    classical_tv = float(np.abs(np.diag(marginal).real-np.abs(target)**2).sum()/2)
    original_scores = np.array([sum(int(value) in target_set for value, target_set in zip(row, problem.target_lists))
                                for row in quadratics])
    z_zero = float(np.vdot(pair[:, 0], pair[:, 0]).real)
    linear_reduction = None
    if problem.form_kind == "diagonal":
        linear = np.zeros_like(output_ru)
        for j, rv in enumerate(vectors):
            if good[j]:
                indices = _index(vectors*rv % p, p)
                linear[j, indices] = output_ru[j]/sqrt(float(good_probability))
        linear_target = float(weights[0])+float(weights[1])/sqrt(m)*sum(
            g[evaluations[:, i]] for i, g in enumerate(local))
        linear_target /= np.linalg.norm(linear_target)
        product_target = good[:, None]*linear_target[None, :]/sqrt(int(sum(good)))
        product_error = float(np.max(np.abs(linear-product_target)))
        if product_error > 1e-12:
            raise ArithmeticError("paired diagonal output does not factor to ordinary linear DQI")
        probabilities = np.sum(np.abs(linear)**2, axis=0)
        linear_density = linear.T@linear.conj()
        linear_purity = float(np.trace(linear_density@linear_density).real)
        squares = {a*a % p for a in range(p)}
        invalid = [any(int(a) not in squares for a in word) for word in vectors]
        linear_reduction = {"q_equals_componentwise_u_times_r_is_reversible_on_good_r": True,
                            "native_factorization_amplitude_error": product_error,
                            "ordinary_linear_DQI_output_purity": linear_purity,
                            "nonsquare_probability_refers_to_q_not_feasibility_of_reporting_x": True,
                            "output_probability_of_nonsquare_original_coefficients": float(sum(probabilities[invalid]))}
    densities = tuple(Fraction(len(target), p) for target in problem.target_lists)
    bound = postselection_bound(p, n, densities, 1)
    if z_zero > float(Fraction(bound["z_zero_probability_upper"]))+1e-12:
        raise ArithmeticError("native postselection exceeds Cauchy probability bound")
    composed = ([tuple(x for x in range(p) if x*x % p in target) for target in problem.target_lists]
                if problem.form_kind == "rank_one" else None)
    record = {"specification": problem.specification(), "shell_weights_exact": list(map(str, weights)),
              "error_labels": D, "finite_state_amplitudes": D*Q*Q,
              "good_direction_count": int(sum(good)), "good_direction_probability_exact": str(good_probability),
              "decoder_calls_in_exhaustive_reference": decoder_calls,
              "decoder_is_public_and_true_error_is_not_an_argument": True,
              "conjugate_chirp_prepared_from_public_error_label_not_unknown_state_conjugation": True,
              "native_pair_to_bilinear_QFT_max_error": phase_transform_error,
              "good_branch_residual_error_label_mass": residual_label,
              "would_leak_error_label_mass_without_good_projection": unprojected_leak,
              "bilinear_filter_amplitude_max_error": direct_error,
              "original_x_marginal_purity": purity, "original_quadratic_target_fidelity": fidelity,
              "original_x_probability_TV_to_intended_target": classical_tv,
              "uniform_original_satisfied_count_mean": float(np.mean(original_scores)),
              "paired_x_original_satisfied_count_mean": float(np.diag(marginal).real@original_scores),
              "ideal_original_quadratic_filter_satisfied_count_mean": float(np.abs(target)**2@original_scores),
              "z_zero_postselection_probability": z_zero, "postselection_bound": bound,
              "diagonal_expected_score_washout_bound": diagonal_score_washout_bound(p, n, densities)
              if problem.form_kind == "diagonal" else None,
              "native_unrestricted_linear_DQI_reduction": linear_reduction,
              "composed_linear_OPI_target_lists": [list(row) for row in composed] if composed else None,
              "rank_one_original_objective_reduces_exactly_to_linear_OPI": problem.form_kind == "rank_one",
              "paired_diagonal_objective_reduces_to_unrestricted_linear_OPI": problem.form_kind == "diagonal",
              "prepared_objective": ("F_i(sum_j (u_j*r_j)*a_i^j); unrestricted coefficients, NOT x_j^2"
                                     if problem.form_kind == "diagonal" else "F_i(U(a_i)*R(a_i)); NOT F_i(X(a_i)^2)"),
              "general_quadratic_DQI_preparation_repaired": False,
              "general_weight_ell_decoder_executed": False,
              "reversible_decoder_and_predicate_state_preparation_compiled": False,
              "dense_reference_or_list_tables_are_poly_log_prime": False}
    return record, pair, target, good


def run_controls():
    controls = []
    for p, n, points, shifts in ((5, 2, (1, 2, 3), (1, 4, 1)),
                                 (7, 2, (1, 2, 3), (1, 2, 4)),
                                 (5, 3, (1, 2, 3, 4), (1, 4, 1, 4))):
        powers = {x*x % p for x in range(p)}
        lists = tuple(tuple(sorted((t+x) % p for x in powers)) for t in shifts)
        for kind in ("diagonal", "rank_one"):
            problem = QuadraticInput(p, n, points, lists, kind)
            controls.append(native_control(problem)[0])
    scaling = [postselection_bound(p, n, (Fraction((p-1)//2, p),)*(2*n), n//2)
               for p, n in ((101, 16), (257, 32), (65537, 64))]
    washout = [diagonal_score_washout_bound(p, n, (Fraction((p-1)//2, p),)*(2*n))
               for p, n in ((101, 16), (257, 32), (65537, 64))]
    return {"schema_version": "1.0", "subsystem": "conjugate_chirp_repair",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                                  for name in ("prime_character_opi.py", "bpqm_gibbs_frontier.py")},
            "native_controls": controls, "symbolic_postselection_controls_not_statevectors": scaling,
            "symbolic_diagonal_mean_bounds_not_statevectors": washout,
            "symbolic_diagonal_tail_bounds_not_statevectors": [
                diagonal_tail_bound(65537, 1024, 2048, Fraction(1, 5), s) for s in (1, 2, 4, 8)],
            "character_sum_calibrations": [reciprocal_character_control(p, c, b)
                                            for p, c, b in ((29, 0, 1), (29, 7, 3), (101, 41, 17), (257, 93, 102))],
            "accepted_speedup_candidate": False, "new_quantum_algorithm_claimed": False,
            "local_derivation_review_pending": True,
            "literature": ["https://arxiv.org/html/2510.08061",
                           "https://people.math.ethz.ch/~kowalski/elements.pdf",
                           "https://people.math.ethz.ch/~kowalski/exponential-sums-elementary.pdf"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{key: row[key] for key in ("good_direction_probability_exact", "original_x_marginal_purity",
                                                "original_quadratic_target_fidelity", "z_zero_postselection_probability")}
                      for row in report["native_controls"]], indent=2))


if __name__ == "__main__":
    main()
