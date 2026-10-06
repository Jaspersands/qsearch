"""Singer hidden-shift access audit: reconstruct geometry, expose residual DLog.

LOCAL DERIVATION / REVIEW PENDING. No novel algorithm or accepted candidate.
FLINT implements finite fields and linear algebra. Tables/QFTs are calibration.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import fq_default_ctx, nmod_mat
from sympy import factorint, isprime

from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/singer_residual_hardness.json"


def singer_parameters(q, m):
    _integer(q, "base field order", 2)
    _integer(m, "extension degree", 2)
    if not (q & (q-1) == 0 or isprime(q)):
        raise ValueError("implemented parameter ledgers require prime or power-of-two base order")
    return ((q**m-1)//(q-1), (q**(m-1)-1)//(q-1), (q**(m-2)-1)//(q-1))


def _coords(x, m):
    return list(map(int, x.to_list()))+[0]*(m-len(x.to_list()))


def classical_residual_comparator(p, degree):
    return {"source": "https://arxiv.org/abs/1906.10668",
            "theorem": "1.1, v2 statement inspected",
            "prime_characteristic": p, "absolute_extension_degree": degree,
            "expected_time_bound": "(p*degree)^(2*log2(degree)+O(1))",
            "quasipolynomial_for_fixed_characteristic": True,
            "implemented_here": False, "runtime_measurement_claim": False}


def public_field(q, m):
    """Bounded calibration setup; factorization/primitive certificate is NOT free."""
    singer_parameters(q, m)
    if not isprime(q) or q > 31 or (q**m-1).bit_length() > 64:
        raise ValueError("FLINT controls support prime q<=31 and field size<=2^64")
    K = fq_default_ctx(q, m, fq_type="FQ_NMOD")
    order = q**m-1
    factors = {int(p): int(e) for p, e in factorint(order).items()}
    alpha = None
    for index in range(1, 256):
        coefficients, value = [], index
        for _ in range(m):
            coefficients.append(value % q)
            value //= q
        trial = K(coefficients)
        if not trial.is_zero() and all(trial**(order//p) != K.one() for p in factors):
            alpha = trial
            break
    if alpha is None:
        raise ValueError("bounded primitive-element calibration search failed")
    return K, alpha, {"base_prime": q, "extension_degree": m,
                      "modulus_coefficients": list(map(int, K.modulus().coeffs())),
                      "primitive_element_coefficients": _coords(alpha, m),
                      "multiplicative_order_factorization": {str(p): e for p, e in factors.items()},
                      "setup_factorization_not_claimed_polynomial_time": True}


def trace_reconstruct(K, alpha, oracle, full_trace_values=False):
    q, m = int(K.characteristic()), int(K.degree())
    if q != 2 and not full_trace_values:
        raise ValueError("a membership bit is a trace value ONLY over F_2")
    basis = [K.gen()**j for j in range(m)]
    rows = [[int((alpha**i*e).trace()) for e in basis] for i in range(m)]
    records, values = [], []
    for i in range(m):
        observed = oracle(i)
        if type(observed) is not int or not 0 <= observed < (q if full_trace_values else 2):
            raise ValueError("canonical declared oracle output required")
        value = observed if full_trace_values else 1-observed
        records.append({"exponent": i, "oracle_output": observed})
        values.append([value])
    A = nmod_mat(rows, q)
    z = A.solve(nmod_mat(values, q))
    beta = K([int(z[i, 0]) for i in range(m)])
    if beta.is_zero():
        raise ValueError("nonzero hidden field element required by this source promise")
    return beta, {"method": "full-trace-linear-system" if full_trace_values else "binary-membership-linear-system",
                  "oracle_evaluations": m, "queries": records, "trace_system": rows,
                  "recovered_normal_coefficients": _coords(beta, m),
                  "residual_target_coefficients": _coords(beta**(q-1), m),
                  "classical_shift_decoder_completed": False}


def positive_hyperplane_reconstruct(K, alpha, oracle, seed, max_queries):
    q, m = int(K.characteristic()), int(K.degree())
    v, _, _ = singer_parameters(q, m)
    _integer(max_queries, "query budget")
    rng, rows, records, accepted = random.Random(seed), [], [], []
    basis = [K.gen()**j for j in range(m)]
    rank = 0
    for _ in range(max_queries):
        exponent = rng.randrange(v)
        observed = oracle(exponent)
        if type(observed) is not int or observed not in (0, 1):
            raise ValueError("membership oracle must return a bit")
        if observed:
            point = alpha**exponent
            row = [int((point*e).trace()) for e in basis]
            new_rank = nmod_mat(rows+[row], q).rank()
            if new_rank > rank:
                rows.append(row)
                accepted.append({"exponent": exponent, "point_coefficients": _coords(point, m)})
                rank = new_rank
        records.append({"exponent": exponent, "oracle_output": observed, "rank_after_query": rank})
        if rank == m-1:
            break
    if rank != m-1:
        return None, {"method": "positive-membership-hyperplane", "oracle_evaluations": len(records),
                      "queries": records, "rank": rank, "budget_exhausted": True}
    nullspace, nullity = nmod_mat(rows, q).nullspace()
    assert nullity == 1
    vector = [int(nullspace[j, 0]) for j in range(m)]
    scalar = pow(next(x for x in vector if x), -1, q)
    normal = K([(x*scalar) % q for x in vector])
    return normal, {"method": "positive-membership-hyperplane", "oracle_evaluations": len(records),
                    "queries": records, "rank": rank, "budget_exhausted": False,
                    "independent_positive_points": accepted, "trace_constraint_matrix": rows,
                    "recovered_normal_coefficients": _coords(normal, m),
                    "residual_target_coefficients": _coords(normal**(q-1), m),
                    "normal_known_only_up_to_base_field_scalar": True,
                    "classical_shift_decoder_completed": False}


def reconstruction_query_law(q, m):
    v, k, _ = singer_parameters(q, m)
    progress = [Fraction(q**(m-1)-q**r, q**m-1) for r in range(m-1)]
    expected = sum((1/p for p in progress), Fraction(0))
    bound = q*(m-1)+Fraction(q*q, (q-1)**2)
    assert expected < bound
    return {"base_field_order": str(q), "extension_degree": m,
            "projective_group_order": str(v), "membership_density": rational(Fraction(k, v)),
            "rank_progress_probabilities": [rational(p) for p in progress],
            "expected_classical_membership_queries": rational(expected),
            "strict_expected_query_upper": rational(bound),
            "query_cost_polynomial_for_fixed_or_polynomial_q": True,
            "polynomial_in_log_q_without_restriction": False,
            "discrete_log_runtime_not_included": True}


def _sqrt_upper(x, bits):
    scaled = x.numerator << (2*bits)
    root = math.isqrt(scaled//x.denominator)
    if root*root*x.denominator < scaled:
        root += 1
    return Fraction(root, 1 << bits)


def sparse_membership_gate(v, k, queries):
    _integer(v, "number of shifted hypotheses", 2)
    _integer(k, "base subset cardinality", 1)
    _integer(queries, "membership queries", 0)
    if k >= v:
        raise ValueError("proper nonempty membership subset required")
    bits = v.bit_length()+8
    upper = min(Fraction(1), (_sqrt_upper(Fraction(1, v), bits)+2*queries*_sqrt_upper(Fraction(k, v), bits))**2)
    return {"hypotheses": str(v), "marked_points": str(k), "queries": queries,
            "average_shift_recovery_success_upper": rational(upper),
            "dyadic_square_root_precision_bits": bits,
            "uniform_shift_prior": True, "initial_memory_secret_independent": True,
            "all_shifted_membership_oracles_share_one_public_base": True,
            "query_and_reference_ancillas_and_adaptivity_allowed": True,
            "white_box_normal_or_trace_value_oracle_covered": False,
            "general_full_oracle_DHSP_lower_bound": False,
            "independent_review": False}


def injectivization_gate(q, m):
    v, k, lam = singer_parameters(q, m)
    density, influence = Fraction(k, v), Fraction(2*(k-lam), v)
    necessary = (v-1+k-1)//k
    threshold = 2*v.bit_length()+6
    sufficient = (threshold*influence.denominator+influence.numerator-1)//influence.numerator
    return {"base_field_order": str(q), "extension_degree": m,
            "projective_group_order": str(v), "membership_density": rational(density),
            "exact_nonzero_shift_influence": rational(influence),
            "necessary_boolean_offsets_for_any_injective_tuple": str(necessary),
            "sufficient_random_offsets_for_failure_at_most_one_over_64": str(sufficient),
            "sufficient_bound_uses_one_minus_gamma_at_most_exp_minus_gamma": True,
            "logarithmic_offsets_require_influence_bounded_below": True,
            "packing_offsets_into_one_oracle_value_is_not_free": True}


def classical_control(q, m, shift, seed):
    K, alpha, public = public_field(q, m)
    v, _, _ = singer_parameters(q, m)
    _integer(shift, "hidden shift", 0)
    if shift >= v:
        raise ValueError("canonical projective hidden shift required")
    beta = alpha**shift
    queries = []

    def membership(exponent):
        _integer(exponent, "oracle exponent", 0)
        if exponent >= v:
            raise ValueError("canonical cyclic membership query required")
        answer = int((beta*alpha**exponent).trace() == 0)
        queries.append((exponent, answer))
        return answer

    if q == 2:
        normal, result = trace_reconstruct(K, alpha, membership)
    else:
        normal, result = positive_hyperplane_reconstruct(K, alpha, membership, seed, 16*q*m)
    assert result["oracle_evaluations"] == len(queries)
    result.update(public, hidden_shift_calibration=str(shift), seed=seed, projective_group_order=str(v),
                  oracle_shift_convention="D_s(k)=D(k+s); target is multiplicative exponent s",
                  query_law=reconstruction_query_law(q, m),
                  source_table_built_by_decoder=False, inverse_or_discrete_log_called_by_decoder=False,
                  candidate_record_accepted=False, speedup_claim_allowed=False)
    if normal is None:
        return result
    target, generator = normal**(q-1), alpha**(q-1)
    result.update(residual_generator_coefficients=_coords(generator, m),
                  normal_line_verified_by_secret_only_for_calibration=target == generator**shift,
                  residual_problem="finite-field discrete logarithm in order-v subgroup",
                  residual_already_solved_quantumly_by_Shor=True,
                  classical_residual_comparator=classical_residual_comparator(q, m),
                  polynomial_time_classical_full_recovery_claim=False)
    if v <= 128:
        power = K.one()
        for exponent in range(v):
            if power == target:
                result["bounded_exhaustive_residual_shift_control"] = exponent
                result["bounded_residual_field_multiplications"] = exponent
                break
            power *= generator
    else:
        result["bounded_exhaustive_residual_shift_control"] = None
    return result


def spectral_control(values, group, shift):
    v = len(values)
    if v < 3 or v > 256 or any(type(x) is not int or x not in (0, 1) for x in values):
        raise ValueError("bounded literal membership controls required")
    if group not in ("cyclic", "boolean") or group == "boolean" and v & (v-1):
        raise ValueError("known cyclic or Boolean group required")
    if type(shift) is not int or not 0 <= shift < v:
        raise ValueError("canonical shift required")
    translated = lambda x, s: (x-s) % v if group == "cyclic" else x ^ s
    k = sum(values)
    correlations = [sum(values[x]*values[translated(x, s)] for x in range(v)) for s in range(1, v)]
    if not 0 < k < v or len(set(correlations)) != 1 or correlations[0] >= k:
        raise ValueError("a verified nontrivial difference set is required")
    lam, r = correlations[0], k-correlations[0]
    F = (np.exp(2j*np.pi*np.outer(np.arange(v), np.arange(v))/v) if group == "cyclic" else
         np.array([[(-1)**((i & j).bit_count()) for j in range(v)] for i in range(v)]))/np.sqrt(v)
    fourier_sum = np.sqrt(v)*(F @ np.array(values))
    correction = np.ones(v, dtype=complex)
    correction[1:] = np.conj(fourier_sum[1:])/math.sqrt(r)
    phase = np.array([(-1)**values[translated(x, shift)] for x in range(v)])/np.sqrt(v)
    transformed = F @ phase
    rows = []
    a, b = 1-2*k/v, 2*math.sqrt(r)/v
    for trivial_phase in (1, -1):
        phases = correction.copy()
        phases[0] = trivial_phase
        final = F.conj().T @ (phases*transformed)
        exact_target = (trivial_phase*a-b*(v-1))**2/v
        other_probability = (trivial_phase*a+b)**2/v
        rows.append({"trivial_character_phase": trivial_phase,
                     "executed_target_success": float(abs(final[shift])**2),
                     "complete_normalized_target_formula": exact_target,
                     "each_non_target_probability_formula": other_probability,
                     "final_probabilities": (np.abs(final)**2).tolist(),
                     "final_norm": float(np.vdot(final, final).real)})
    return {"group": group, "domain_size": v, "membership_values": list(values),
            "oracle_shift_convention": "values_s(x)=values(x-s); target is translation s",
            "hidden_shift_calibration": shift, "difference_set_size": k, "difference_parameter": lam,
            "flat_nontrivial_fourier_magnitude_residual": float(np.max(np.abs(np.abs(fourier_sum[1:])-math.sqrt(r)))),
            "leading_fourier_target_term_NOT_probability": rational(Fraction(4*r, v)),
            "unnormalized_r_instead_of_sqrt_r_norm_countercontrol": rational(Fraction((v-2*k)**2+4*r*r*(v-1), v*v)),
            "phase_correction_tables_only_for_calibration": True,
            "efficient_coherent_phase_recipe_proved_by_this_module": False,
            "zero_character_controls": rows, "speedup_claim_allowed": False}


def run_controls():
    classical = [classical_control(q, m, s, seed) for q, m in ((2, 3), (2, 4), (2, 8), (2, 16), (2, 32), (2, 64), (3, 3), (3, 8), (5, 3), (5, 6), (7, 3)) for seed, s in ((42011, 1), (42012, singer_parameters(q, m)[0]//2))]
    spectral = []
    for q, m in ((2, 3), (2, 4), (3, 3), (5, 3), (13, 3)):
        K, alpha, _ = public_field(q, m)
        v = singer_parameters(q, m)[0]
        spectral.append(spectral_control([int((alpha**x).trace() == 0) for x in range(v)], "cyclic", 1))
    for p in (7, 11):
        squares = {x*x % p for x in range(1, p)}
        spectral.append(spectral_control([int(x in squares) for x in range(p)], "cyclic", 2))
    spectral.append(spectral_control([int((x&1)*((x>>1)&1) ^ ((x>>2)&1)*((x>>3)&1)) for x in range(16)], "boolean", 3))
    scaling = []
    for bits in (8, 16, 32, 64, 128):
        q, m = 1 << bits, 3
        v, k, _ = singer_parameters(q, m)
        scaling.append({"base_field_bits": bits, "query_gate": sparse_membership_gate(v, k, bits**2),
                        "injectivization": injectivization_gate(q, m), "reconstruction": reconstruction_query_law(q, m),
                        "classical_residual_comparator": classical_residual_comparator(2, bits*m)})
    return {"status": "SINGER_RESIDUAL_DLOG_AND_SPARSE_ACCESS_SCREEN_LOCAL_DERIVATION_REVIEW_PENDING",
            "classical_geometry_controls": classical, "spectral_normalization_controls": spectral,
            "growing_base_field_ledgers": scaling,
            "claim_gate": {"candidate_record_accepted": False, "new_quantum_algorithm": False,
                           "full_classical_dequantization": False, "general_DHSP_lower_bound": False,
                           "independent_review": False, "novelty_claim": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "geometry_controls": len(report["classical_geometry_controls"]),
                      "spectral_controls": len(report["spectral_normalization_controls"]), "candidate_accepted": False}))


if __name__ == "__main__":
    main()
