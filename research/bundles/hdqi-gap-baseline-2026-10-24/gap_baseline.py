"""Analytic gap certificate and spectral-clipping comparator; not quantum runs."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh
from scipy.special import gammaln, logsumexp

ROOT = Path(__file__).resolve().parent
FILTER = ROOT.parent / "hdqi-filtered-parent-2026-10-24"
sys.path.insert(0, str(FILTER))
from filtered_parent import (LCU_NORM, build_model, control_graphs, filtered_parent)  # noqa: E402


def _parameters(mass, beta):
    if not math.isfinite(mass) or mass < 0 or not math.isfinite(beta) or beta < 0:
        raise ValueError("finite nonnegative squared-coupling mass and beta required")


def gap_certificate(mass, beta):
    _parameters(mass, beta)
    perturbation = math.sqrt(5) / 2 * LCU_NORM * beta * math.sqrt(mass)
    return {"squared_coupling_mass": mass, "beta": beta,
            "row_perturbation_bound": perturbation,
            "gap_lower_bound": max(0.0, 1 - perturbation)**2,
            "status": "positive_bound" if perturbation < 1 else "inconclusive",
            "scope": "canonical filtered parent, not an arbitrary Gibbs sampler"}


def clipping_plan(mass, beta, epsilon, norm_sum=None):
    _parameters(mass, beta)
    if not math.isfinite(epsilon) or not 0 < epsilon < 1:
        raise ValueError("0<epsilon<1 required")
    if norm_sum is not None and (not math.isfinite(norm_sum) or norm_sum < 0):
        raise ValueError("finite nonnegative public norm sum required")
    if norm_sum is not None and norm_sum < math.sqrt(mass):
        raise ValueError("public norm sum is inconsistent with squared coupling mass")
    log_tail_budget = math.log(64 / epsilon**2)
    cut = beta * mass + math.sqrt(mass * (beta*beta*mass + 2*log_tail_budget))
    spectral_cap = norm_sum is not None and norm_sum <= cut
    if spectral_cap:
        cut = norm_sum
    log_p = -beta * cut + 2 * math.log1p(-epsilon/8)
    return {"squared_coupling_mass": mass, "beta": beta, "epsilon": epsilon,
            "cut": cut, "clipping_absent_by_norm_bound": spectral_cap,
            "weighted_bad_tail_bound": 0.0 if spectral_cap or mass == 0 else epsilon**2/64,
            "log2_success_lower_bound": log_p / math.log(2),
            "log2_amplitude_amplification_scale": -log_p / (2*math.log(2)),
            "log2_filter_operator_tolerance": (math.log(epsilon/8) + log_p/2) / math.log(2),
            "clipping_trace_distance_budget": epsilon/4,
            "filter_trace_distance_budget": epsilon/4,
            "remaining_implementation_budget": epsilon/2,
            "quantum_circuit_executed": False}


def spectral_control(energies, weights, beta, cut):
    """Classical control from an explicitly supplied spectral distribution."""
    energies, weights = np.asarray(energies), np.asarray(weights)
    if (energies.ndim != 1 or weights.shape != energies.shape
            or not np.all(np.isfinite(energies)) or not np.all(np.isfinite(weights))
            or np.any(weights < 0) or not np.isclose(weights.sum(), 1)):
        raise ValueError("normalized finite positive spectral distribution required")
    if not math.isfinite(beta) or not math.isfinite(cut) or beta < 0 or cut < 0:
        raise ValueError("beta and cutoff must be nonnegative")
    mask = weights > 0
    energies, weights = energies[mask], weights[mask]
    log_weights = np.log(weights)
    log_z = float(logsumexp(log_weights - beta*energies))
    log_g = np.minimum(0, -beta*(energies + cut)/2)
    log_p = float(logsumexp(log_weights + 2*log_g))
    ideal = np.sqrt(weights) * np.exp(-beta*energies/2 - log_z/2)
    actual = np.sqrt(weights) * np.exp(log_g - log_p/2)
    # Difference of normalized vectors is stable near fidelity one.
    distance = float(np.linalg.norm(ideal - actual))
    overlap = float(np.dot(ideal, actual))
    trace_distance = distance * math.sqrt(max(0, (1 + overlap)/2))
    bad = energies < -cut
    log_bad = float(logsumexp(log_weights[bad] - beta*energies[bad])) if np.any(bad) else None
    return {"log_partition": log_z, "log_success": log_p,
            "trace_distance": trace_distance, "log_weighted_bad_tail": log_bad,
            "spectral_points": len(energies)}


def binomial_spectrum(m):
    """Easy commuting control only: the exact spectrum of sum_i X_i."""
    k = np.arange(m + 1)
    log_weights = gammaln(m + 1) - gammaln(k + 1) - gammaln(m - k + 1) - m*math.log(2)
    weights = np.exp(log_weights - logsumexp(log_weights))
    return m - 2*k, weights


def build_receipt():
    finite = []
    for name, model in control_graphs().items():
        if model.m > 5:
            continue
        mass = sum(j*j for j in model.couplings)
        for beta in (.05, .2, .5):
            certificate = gap_certificate(mass, beta)
            parent, _ = filtered_parent(model, beta)
            gap = float(eigh(parent, eigvals_only=True)[1])
            finite.append({"graph": name, "certificate": certificate, "finite_gap": gap,
                           "bound_respected": bool(gap + 1e-11 >= certificate["gap_lower_bound"])})
    plan = clipping_plan(64, .1, .1, 64)
    energies, weights = binomial_spectrum(64)
    control = spectral_control(energies, weights, .1, plan["cut"])
    # Parameter-only ledgers, not generated graph instances or quantum runs.
    regimes = []
    for exponent in (4, 8, 12, 20):
        degree, vertices = 2**exponent, 2**(2*exponent)
        beta = math.sqrt(.01/(degree+1))
        regimes.append({"vertices": vertices, "degree": degree,
                        "instance_constructed": False,
                        "gap_certificate": gap_certificate(vertices, beta),
                        "clipping_plan": clipping_plan(vertices, beta, .01, vertices)})
    sources = [ROOT / "gap_baseline.py", ROOT / "test_gap_baseline.py", ROOT / "GAP_AND_BASELINE.md",
               FILTER / "filtered_parent.py", FILTER.parent / "hdqi-parent-gap-2026-10-23/parent_gap.py"]
    return {"schema": "hdqi-mass-gap-and-clipping-v1",
            "status": "certified_mass_regime_not_degree_regime_breakthrough",
            "claims": {"uniform_degree_gap_proved": False, "quantum_circuit_executed": False,
                       "quantum_speedup_established": False, "novelty_established": False,
                       "independently_reviewed": False},
            "finite_gap_controls": finite,
            "commuting_clipping_control": {"plan": plan, "reference": control},
            "parameter_ledgers_only": regimes,
            "sha256": {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = build_receipt()
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"output": str(args.output.resolve()), "status": receipt["status"],
                      "finite_gap_controls": len(receipt["finite_gap_controls"])}))
