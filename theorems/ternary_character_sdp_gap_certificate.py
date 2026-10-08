"""Exact finite non-tightness certificates for the native character SDP.

A numerical matrix is only a proposal. Dyadic primal feasibility, PSD residual
dominance, rational trigonometric bounds and ALL-secret upper bounds are exact.
The exhaustive verifier is bounded research analysis, never a decoder input.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from ternary_character_sdp_decoder import REPORT as SOURCE_REPORT, compile_model
from ternary_covariant_noise import CovariantRecord, root_digits

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_character_sdp_gap_certificate.json"
DERIVATION = ROOT / "research/TERNARY_CHARACTER_SDP_GAP_CERTIFICATE.md"


def floor_rational(x):
    return x.numerator//x.denominator


def ceil_rational(x):
    return -floor_rational(-x)


@lru_cache(None)
def pi_interval():
    """Machin identity with alternating rational remainders, then dyadic rounding."""
    def atan_interval(denominator):
        x = Fraction(1, denominator)
        value = sum(((-1)**k*x**(2*k+1)/ (2*k+1) for k in range(40)), Fraction())
        return value, value+x**81/81
    a, b = atan_interval(5), atan_interval(239)
    lower, upper = 16*a[0]-4*b[1], 16*a[1]-4*b[0]
    scale = 2**64
    return Fraction(floor_rational(lower*scale), scale), Fraction(ceil_rational(upper*scale), scale)


@lru_cache(None)
def root_intervals(q):
    root_digits(q)
    if q > 81:
        raise ValueError("exact finite root interval table capped at81")
    lo, hi = pi_interval()
    midpoint = (lo+hi)/2
    remainder = Fraction(22, 7)**41/math.factorial(41)
    scale = 2**48
    result = []
    for e in range(q):
        if not e:
            result.append({"cos_lower": scale, "cos_upper": scale, "sin_lower": 0, "sin_upper": 0})
            continue
        signed = e if 2*e <= q else e-q
        angle = 2*midpoint*signed/q
        angle_error = (hi-lo)*abs(signed)/q
        cosine = sum(((-1)**k*angle**(2*k)/math.factorial(2*k) for k in range(21)), Fraction())
        sine = sum(((-1)**k*angle**(2*k+1)/math.factorial(2*k+1) for k in range(21)), Fraction())
        error = angle_error+remainder
        result.append({"cos_lower": floor_rational((cosine-error)*scale),
                       "cos_upper": ceil_rational((cosine+error)*scale),
                       "sin_lower": floor_rational((sine-error)*scale),
                       "sin_upper": ceil_rational((sine+error)*scale)})
    return tuple(result)


def exact_psd_residual(integer_matrix, integer_factor, scale):
    """A=L*L^T+R, with exact diagonally-dominant R>=0 (all dyadic)."""
    A, L = np.asarray(integer_matrix), np.asarray(integer_factor)
    if A.dtype != np.int64 or L.dtype != np.int64 or A.shape != L.shape or len(A.shape) != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("same-sized exact int64 square matrices required")
    if type(scale) is not int or scale <= 0 or not np.array_equal(A, A.T):
        raise ValueError("positive scale and exact symmetric matrix required")
    N = len(A)
    maximum_A, maximum_L = max(abs(int(x)) for x in A.flat), max(abs(int(x)) for x in L.flat)
    if maximum_A*scale+N*maximum_L**2 >= 2**63:
        raise ValueError("exact residual multiplication exceeds int64 scope")
    residual = A*scale-L @ L.T
    margins = tuple(int(residual[i, i])-sum(abs(int(residual[i, j])) for j in range(N) if j != i)
                    for i in range(N))
    return {"PSD_certified": min(margins) >= 0, "minimum_integer_diagonal_dominance_margin": str(min(margins)),
            "matrix_dimension": N, "residual_denominator": str(scale*scale)}


def quantized_witness(model, matrix):
    """Only the public numerical moment point is used, never truth or heldout data."""
    K, q, nodes, scale = model["matrix_nodes"], model["modulus"], model["nodes"], 2**24
    groups = {}
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            d = tuple((x-y) % q for x, y in zip(a, b))
            groups.setdefault(d, []).append(matrix[i, j])
    moments, zero = {}, (0,)*model["dimension"]
    moments[zero] = (scale, 0)
    for d, values in groups.items():
        if d in moments:
            continue
        opposite = tuple(-x % q for x in d)
        average = (np.mean(values)+np.mean(groups[opposite]).conjugate())/2*(31/32)
        value = (int(round(average.real*scale)), int(round(average.imag*scale)))
        moments[d], moments[opposite] = value, (value[0], -value[1])
    re, im = np.zeros((K, K), np.int64), np.zeros((K, K), np.int64)
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            re[i, j], im[i, j] = moments[tuple((x-y) % q for x, y in zip(a, b))]
    realification = np.block([[re, -im], [im, re]])
    try:
        factor = np.linalg.cholesky(realification/scale-np.eye(2*K)/64)
    except np.linalg.LinAlgError:
        return {"status": "NUMERICAL_FACTOR_PROPOSAL_FAILED", "PSD_certified": False}
    integer_factor = np.rint(factor*scale).astype(np.int64)
    audit = exact_psd_residual(realification, integer_factor, scale)
    if not audit["PSD_certified"]:
        return {"status": "EXACT_RESIDUAL_DOMINANCE_FAILED", **audit}
    return {"status": "EXACT_DYADIC_FEASIBLE_MOMENT_POINT", **audit,
            "moment_scale": scale, "matrix_real_integer": re.tolist(), "matrix_imag_integer": im.tolist(),
            "factor_lower_triangle_integer": [row[:i+1].tolist() for i, row in enumerate(integer_factor)],
            "numerical_factor_precision_is_not_trusted_by_verifier": True,
            "identity_mixture_weight": "1/32", "factor_proposal_subtracted_identity": "1/64"}


def objective_lower(records, native_nodes, witness, roots):
    re, im = witness["matrix_real_integer"], witness["matrix_imag_integer"]
    q, value = records[0].modulus, 0
    for record, (a, c) in zip(records, native_nodes):
        for i, j, exponent in ((a, 0, record.outcome[0]), (c, 0, record.outcome[1]),
                               (a, c, (record.outcome[0]-record.outcome[1]) % q)):
            real, imaginary = re[i][j], im[i][j]
            root = roots[exponent]
            value += real*root["cos_lower" if real >= 0 else "cos_upper"]
            value += imaginary*root["sin_lower" if imaginary >= 0 else "sin_upper"]
    return value


def exhaustive_character_bounds(records, roots, max_secrets=600000, batch_size=4096):
    n, q, M = len(records[0].first), records[0].modulus, len(records)
    if type(max_secrets) is not int or max_secrets < 1 or type(batch_size) is not int or batch_size < 1:
        raise ValueError("positive complete verification and batch caps required")
    G = q**n
    if G > max_secrets:
        return {"status": "COMPLETE_SECRET_CENSUS_CAP_EXHAUSTED", "required_secrets": G,
                "partial_census_certifies_global_upper": False}
    if n*q*q >= 2**63 or 3*M*max(abs(r[k]) for r in roots for k in ("cos_lower", "cos_upper")) >= 2**63:
        raise ValueError("exact integer character census exceeds int64 scope")
    A = np.asarray([(r.first, r.second) for r in records], dtype=np.int64).reshape(-1, n)
    Y = np.asarray([r.outcome for r in records], dtype=np.int64)
    lower = np.asarray([r["cos_lower"] for r in roots], np.int64)
    upper = np.asarray([r["cos_upper"] for r in roots], np.int64)
    best_upper, best_lower, upper_witness, lower_witness = -2**63, -2**63, None, None
    for start in range(0, G, batch_size):
        ids = np.arange(start, min(start+batch_size, G), dtype=np.int64)
        secrets = np.array([(ids//q**j) % q for j in range(n)], dtype=np.int64).T
        residual = (Y[None, :, :]-secrets.dot(A.T).reshape(len(ids), M, 2)) % q
        first, second = residual[:, :, 0], residual[:, :, 1]
        difference = (first-second) % q
        lo = (lower[first]+lower[second]+lower[difference]).sum(axis=1)
        hi = (upper[first]+upper[second]+upper[difference]).sum(axis=1)
        i, j = int(np.argmax(lo)), int(np.argmax(hi))
        if int(lo[i]) > best_lower:
            best_lower, lower_witness = int(lo[i]), secrets[i].tolist()
        if int(hi[j]) > best_upper:
            best_upper, upper_witness = int(hi[j]), secrets[j].tolist()
    return {"status": "ALL_FULL_ROOT_SECRETS_EXACT_INTERVAL_BOUNDED", "secrets_checked": G,
            "paired_score_features_checked": 3*M*G, "score_denominator": str(2**48),
            "global_character_score_upper_numerator": str(best_upper),
            "feasible_character_score_lower_numerator": str(best_lower),
            "upper_witness": upper_witness, "lower_witness": lower_witness,
            "exhaustive_verification_used_by_decoder": False,
            "exact_identity_of_unique_optimal_secret_certified": False}


def certify_control(control, max_secrets=600000):
    decoded = control["decoder"]
    if decoded["candidate"] is None:
        return {"status": "NO_NUMERICAL_PRIMAL_PROPOSAL", "seed": control["seed"]}
    records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                    for r in control["training_records"])
    K = decoded["model"]["matrix_nodes"]
    model = compile_model(records, max_matrix_nodes=K)
    X = np.array(decoded["solver"]["matrix_real"])+1j*np.array(decoded["solver"]["matrix_imag"])
    witness = quantized_witness(model, X)
    if not witness["PSD_certified"]:
        return {"seed": control["seed"], **witness}
    roots = root_intervals(records[0].modulus)
    census = exhaustive_character_bounds(records, roots, max_secrets=max_secrets)
    output = {"seed": control["seed"], "dimension": model["dimension"], "modulus": model["modulus"],
              "nodes": model["nodes"], "native_nodes": model["native_nodes"],
              "witness": witness, "root_interval_denominator": str(2**48),
              "root_intervals": roots, "character_census": census,
              "finite_counterexample_is_population_or_asymptotic_failure": False,
              "certification_uses_truth_or_holdout": False}
    if census["status"] != "ALL_FULL_ROOT_SECRETS_EXACT_INTERVAL_BOUNDED":
        return {"status": "NO_COMPLETE_CHARACTER_UPPER", **output}
    lower = objective_lower(records, model["native_nodes"], witness, roots)
    upper = int(census["global_character_score_upper_numerator"])*witness["moment_scale"]
    gap = lower-upper
    return {"status": "EXACT_FINITE_SDP_CHARACTER_GAP" if gap > 0 else "NO_POSITIVE_GAP_CERTIFIED", **output,
            "SDP_feasible_score_lower_numerator": str(lower),
            "all_character_score_upper_same_scale_numerator": str(upper),
            "strict_gap_lower_numerator": str(gap), "score_common_denominator": str(2**72),
            "strict_gap_per_qutrit_approximation_NOT_certificate": gap/2**72/len(records),
            "exact_SDP_optimum_or_dual_certificate_required": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE_REPORT.read_text())
    selected = [c for c in source["native_controls"] if c["seed"] in (93017, 93018)]
    report = {"status": "EXACT_FINITE_NATIVE_CHARACTER_SDP_GAP_RESEARCH_ONLY",
              "source_report_sha256": hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest(),
              "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
              "certificates": [certify_control(c) for c in selected],
              "numerical_solver_status_used_as_proof": False, "asymptotic_impossibility_or_speedup_claim": False}
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "certificates": [
        {"seed": c["seed"], "status": c["status"], "gap_per_qutrit": c.get("strict_gap_per_qutrit_approximation_NOT_certificate")}
        for c in report["certificates"]]}, indent=2))


if __name__ == "__main__":
    main()
