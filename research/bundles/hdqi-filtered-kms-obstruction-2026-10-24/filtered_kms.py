"""Exact star-sector identities for two distinct thermal proof obstructions.

The parent remains gapped on the certified examples. Large rows are analytic
ledgers, not simulations; only dense_control builds matrices (at most 256^2).
"""

from fractions import Fraction as F
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-thermal-flow-obstruction-2026-10-24"))
from thermal_flow import build_model, degree, log_cosh_minus_one  # noqa: E402
from relative_flow import graph_phase  # noqa: E402


def parameters(d, beta, s=0.0):
    degree(d)
    if isinstance(beta, bool) or not math.isfinite(beta) or not 0 <= beta <= 10:
        raise ValueError("finite 0<=beta<=10 required for the floating ledger")
    if isinstance(s, bool) or not math.isfinite(s) or abs(s) > 1e6:
        raise ValueError("finite |s|<=1e6 required for the floating ledger")


def log_cosh(x):
    x = abs(x)
    return float(np.logaddexp(x, -x)) - math.log(2)


def star_formula(d, beta, s=0.0):
    """Per-sector-weight forms; logarithms avoid rare-sector underflow.

    The log zero-frequency bound is None when u<=1, where the deliberately
    loose thermal-filter envelope is not useful. No numerical row is an
    interval certificate; rational_certificate supplies separate exact bounds.
    """
    parameters(d, beta, s)
    r2, a2 = d*d+1, (d-2)**2+1
    r, ra = math.sqrt(r2), math.sqrt(a2)
    u, v = beta*r, beta*ra
    delta = 4 / (r*ra*(r*ra+1+d*(d-2)))
    difference = (4*d-4)/(r+ra)
    total = r+ra
    log_gradient = float(logsumexp([
        math.log(d/2), math.log(d*d/r2),
        math.log(d*d)-2*math.log(r2)+log_cosh_minus_one(u),
        math.log(d)-math.log(r2)-math.log(a2)+log_cosh_minus_one(v)]))
    leaf_terms = [math.log(2-delta)+log_cosh(beta*difference/2),
                  math.log(delta)+log_cosh(beta*total/2)]
    log_leaf_raw = float(logsumexp(leaf_terms))
    log_leaf_filtered = float(logsumexp([
        leaf_terms[0]-(beta*difference)**2/4,
        leaf_terms[1]-(beta*total)**2/4]))
    center = math.log(d*d/r2)
    sine = math.sin(2*u*s)
    center_extra = (-u*u+log_cosh(u)-math.log(r2)+2*math.log(abs(sine))
                    if sine else -math.inf)
    integrated_extra = -u*u+log_cosh_minus_one(u)-math.log(2*r2)
    raw = float(np.logaddexp(center, math.log(d/4)+log_leaf_raw))
    filtered = float(logsumexp([center, center_extra, math.log(d/4)+log_leaf_filtered]))
    integrated = float(logsumexp([center, integrated_extra, math.log(d/4)+log_leaf_filtered]))
    bound = None
    if u > 1:
        log_one_minus_envelope = math.log(-math.expm1(-u*(u-1)/2))
        bound = math.log(d*d)-2*math.log(r2)+log_cosh(u)+2*log_one_minus_envelope-log_gradient
    return {"d": d, "m": d+1, "beta": beta, "s": s,
            "beta_squared_d_plus_one": beta*beta*(d+1),
            "log_sector_weight": -(d-1)*math.log(2),
            "one_minus_sector_axis_overlap": delta,
            "log_same_KMS_gradient_over_sector_weight": log_gradient,
            "log_same_KMS_filter_commutator_ratio_lower": bound,
            "log_raw_physical_form_over_sector_weight": raw,
            "log_filtered_physical_form_over_sector_weight": filtered,
            "log_integrated_physical_form_over_sector_weight": integrated,
            "log_filtered_to_raw_physical_form_ratio": filtered-raw,
            "log_integrated_to_raw_physical_form_ratio": integrated-raw,
            "filtered_witness_Rayleigh_lower": d*d/r2,
            "log_filtered_witness_Rayleigh_upper": 0.25+math.log1p(d/2),
            "floating_values_are_not_interval_certificates": True,
            "parent_gap_disproved": False, "quantum_algorithm_executed": False}


def cosh_taylor_lower(x, terms):
    if not isinstance(x, F) or x < 0:
        raise ValueError("nonnegative rational argument required")
    if type(terms) is not int or not 0 <= terms <= 128:
        raise ValueError("Taylor order must be an integer in [0,128]")
    term = total = F(1)
    for k in range(1, terms+1):
        term *= x*x/F((2*k-1)*(2*k))
        total += term
    return total


def rational_certificate(d, beta, terms=24):
    degree(d)
    if not isinstance(beta, F) or not 0 <= beta <= 10:
        raise ValueError("exact rational 0<=beta<=10 required")
    T = cosh_taylor_lower(beta*d, terms)
    T_leaf = cosh_taylor_lower(beta*(d-1), terms)
    r2, a2 = d*d+1, (d-2)**2+1
    A, B = F(d*d, r2*r2), F(d, r2*a2)
    C = F(d, 2)+F(d*d, r2)
    u0 = beta*d
    envelope_upper = 1/(1+u0*(u0-1)/2) if u0 > 1 else F(1)
    commutator_lower = A*(1-envelope_upper)**2/(A+B+C/T)
    raw_lower = F(d, 2*r2*a2)*T_leaf
    filtered_upper = F(4, 3)*(1+F(d, 2))
    ratio_upper = filtered_upper/raw_lower
    inside = beta*beta*(d+1) <= F(1, 64)
    return {"d": d, "beta": str(beta), "Taylor_terms": terms,
            "beta_squared_d_plus_one": str(beta*beta*(d+1)),
            "cosh_beta_d_lower": str(T), "cosh_beta_d_minus_one_lower": str(T_leaf),
            "filter_envelope_upper": str(envelope_upper),
            "same_KMS_filter_commutator_ratio_lower": str(commutator_lower),
            "same_KMS_filter_commutator_ratio_exceeds_99_over_100": commutator_lower > F(99, 100),
            "raw_physical_form_over_sector_weight_lower": str(raw_lower),
            "filtered_physical_form_over_sector_weight_upper": str(filtered_upper),
            "filtered_to_raw_physical_form_ratio_upper": str(ratio_upper),
            "filtered_to_raw_physical_form_ratio_below_1_over_100": ratio_upper < F(1, 100),
            "uniform_over_all_filter_times_and_normalized_averages": True,
            "inside_beta_squared_d_plus_one_le_one_over_64": inside,
            "filtered_parent_gap_lower_from_existing_mass_lemma": "25/36" if inside else None,
            "classical_envelope_ratio_upper_from_existing_moment_bound": "128/127" if inside else None,
            "large_matrices_built": False, "parent_gap_disproved": False}


def physical_reference(d, beta):
    parameters(d, beta)
    if d > 7:
        raise ValueError("dense control capped at eight coefficient qubits")
    if beta > 1:
        raise ValueError("dense control requires beta<=1 for numerical conditioning")
    model = build_model(d+1, [(0, j) for j in range(1, d+1)])
    identity = np.eye(len(model.h))
    P = identity.copy()
    for j in range(2, d+1):
        P = P@(identity+model.operators[1]@model.operators[j])/2
    r = math.sqrt(d*d+1)
    W = P@(d*model.operators[0]-model.operators[1])/r
    return model, P, W, expm(-beta*model.h/2)


def kms_squared(x, S):
    value = np.trace(S@x.conj().T@S@x)/len(S)
    if abs(value.imag) > 1e-9 or value.real < -1e-9:
        raise ArithmeticError("invalid dense KMS norm")
    return float(value.real)


def dense_control(d, beta, s=0.17):
    formula = star_formula(d, beta, s)
    model, P, W, S = physical_reference(d, beta)
    dimension = len(S)
    w, r = 2.0**(-(d-1)), math.sqrt(d*d+1)
    eigenvalues, vectors = eigh(model.h)
    frequencies = beta*(eigenvalues[:, None]-eigenvalues[None, :])

    def filtered(x, thermal=False):
        exponent = -frequencies**2/8+1j*s*frequencies
        if thermal:
            exponent -= frequencies/4
        return vectors@((vectors.conj().T@x@vectors)*np.exp(exponent))@vectors.conj().T

    gradient = raw = tagged = parent = coefficient_parent = 0.0
    phase = graph_phase(model)
    coefficient_witness = W[:, 0]
    for z in model.z:
        derivative = (W-z@W@z)/2
        gradient += kms_squared(derivative, S)
        raw += kms_squared(z@W-W@z, S)/4
        tagged += float(np.trace(S@derivative.conj().T@(z@S@z)@derivative).real/dimension)
        B = filtered(z)
        parent += kms_squared(B@W-W@B, S)/4
        L = filtered(z, thermal=True)
        Q = (z@L-phase@L.conj()@phase)/2
        coefficient_parent += float(np.linalg.norm(Q@coefficient_witness)**2)
    errors = {"projector": float(np.linalg.norm(P@P-P)),
              "central_projector": max(float(np.linalg.norm(P@o-o@P)) for o in model.operators),
              "anticommuting_witness": float(np.linalg.norm(model.h@W+W@model.h)),
              "thermal_mean_zero": float(abs(np.trace(S@S@W)/dimension)),
              "KMS_variance": abs(kms_squared(W, S)/w-1),
              "same_KMS_gradient": abs(gradient/w-math.exp(formula["log_same_KMS_gradient_over_sector_weight"])),
              "tagged_metric_equals_physical_form": abs(tagged/w-raw/w),
              "raw_physical_form": abs(raw/w-math.exp(formula["log_raw_physical_form_over_sector_weight"])),
              "filtered_physical_form": abs(parent/w-math.exp(formula["log_filtered_physical_form_over_sector_weight"])),
              "direct_coefficient_parent": abs(coefficient_parent/w-parent/w),
              "occupation_commutator_sign": max(float(np.linalg.norm(n@o-o@n-o@z))
                                                 for n, o, z in zip(model.occupations, model.operators, model.z))}
    filter_controls = []
    h = P@model.h/r
    u = beta*r
    for thermal in (False, True):
        FW = filtered(W, thermal)
        commutators = []
        for z in model.z:
            commutators.append((FW-z@FW@z)/2-filtered((W-z@W@z)/2, thermal))
        b = (np.exp(-u*u/2-(u/2 if thermal else 0)+2j*u*s)
             + np.exp(-u*u/2+(u/2 if thermal else 0)-2j*u*s))/2
        projected = h*(np.trace(h@commutators[0])/dimension/w)
        expected = (b-1)*d/(r*r)*h
        errors[f"zero_frequency_projection_{thermal}"] = float(np.linalg.norm(projected-expected))
        measured_ratio = sum(kms_squared(c, S) for c in commutators)/gradient
        exact_component_bound = d*d/r**4*math.cosh(u)*abs(1-b)**2/(gradient/w)
        if measured_ratio+1e-9 < exact_component_bound:
            raise ArithmeticError("zero-frequency lower bound violated")
        if formula["log_same_KMS_filter_commutator_ratio_lower"] is not None:
            if measured_ratio+1e-9 < math.exp(formula["log_same_KMS_filter_commutator_ratio_lower"]):
                raise ArithmeticError("uniform filter lower bound violated")
        filter_controls.append({"filter": "thermal_f" if thermal else "symmetric_g",
                                "measured_same_KMS_commutator_ratio": measured_ratio,
                                "zero_frequency_component_ratio": exact_component_bound})
    if max(errors.values()) > 2e-8:
        raise ArithmeticError("independent physical matrix identity failed")
    return {**formula, "mode": "exponential_dense_identity_control", "dense_dimension": dimension,
            "identity_errors": errors, "filter_controls": filter_controls,
            "same_KMS_gradient": gradient, "raw_physical_form": raw,
            "filtered_physical_form": parent}
