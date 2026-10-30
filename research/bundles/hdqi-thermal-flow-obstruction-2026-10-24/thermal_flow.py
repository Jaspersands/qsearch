"""An all-size thermal-gradient obstruction, not a parent-gap obstruction.

Dense controls are exponential and capped. Large rows use the exact star
sector formula from THERMAL_FLOW.md; no large state or graph is constructed.
"""

from fractions import Fraction as F
from math import isqrt
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import logsumexp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"hdqi-relative-flow-2026-10-24"))
from relative_flow import build_model  # noqa: E402


def degree(d):
    if type(d) is not int or not 2 <= d <= 2**40:
        raise ValueError("integer star degree in [2,2^40] required")
    return d


def log_cosh_minus_one(x):
    if x == 0:
        return -math.inf
    if x < 1:
        return math.log(2)+2*math.log(math.sinh(x/2))
    return x-math.log(2)+2*math.log1p(-math.exp(-x))


def star_formula(d, beta):
    degree(d)
    if isinstance(beta, bool) or not math.isfinite(beta) or not 0 <= beta <= 10:
        raise ValueError("finite 0<=beta<=10 required for this floating ledger")
    r2, a2 = d*d+1, (d-2)**2+1
    r, a = math.sqrt(r2), math.sqrt(a2)
    u, v = beta*r, beta*a
    cu, cv = log_cosh_minus_one(u), log_cosh_minus_one(v)
    log_kz = float(np.logaddexp(0, math.log(d*d/r2)+cu))
    log_kx = float(np.logaddexp(0, cv-math.log(a2)))
    log_initial = math.log1p(d/2)
    log_defect = math.log(4)+float(np.logaddexp(log_kz, math.log(d)+log_kx))-log_initial
    log_evolved = float(logsumexp([
        math.log(d/2), math.log(d*d/r2), math.log(d*d)-2*math.log(r2)+cu,
        math.log(d)-math.log(r2)-math.log(a2)+cv]))-log_initial
    gaussian_sine_square = -math.expm1(-2*u*u)/2
    log_average = float(np.logaddexp(
        math.log1p(-gaussian_sine_square),
        math.log(gaussian_sine_square)+log_evolved if gaussian_sine_square else -math.inf))
    time = math.pi/(4*r)
    return {"d": d, "m": d+1, "beta": beta, "beta_squared_d_plus_one": beta*beta*(d+1),
            "quarter_rotation_time": time,
            "log_sector_weight": -(d-1)*math.log(2),
            "log_initial_gradient_over_sector_weight": log_initial,
            "log_defect_squared_ratio": log_defect,
            "log_trace_metric_defect_bound": math.log(4*d),
            "log_flow_squared_amplification": log_evolved,
            "log_incorrect_thermal_flow_squared_bound": 4*math.sqrt(d)*time,
            "log_phase_forgotten_Gaussian_gradient_squared_ratio_at_s_zero": log_average,
            "log_gaussian_image_gradient_squared_ratio_upper":
                math.log(2)-u*u+u+float(np.logaddexp(0, log_evolved)),
            "floating_values_are_not_interval_certificates": True,
            "parent_gap_disproved": False, "quantum_algorithm_executed": False}


def rational_countercertificate(d, beta, terms=24):
    """Strict counterexample certificates using rational arithmetic only.

    cosh(beta*r)>=sum_{k=0}^terms (beta*d)^(2k)/(2k)!, r>=d.
    At t=pi/(4r), exp(4sqrt(d)t)<=1/(1-22/(7sqrt(d))).
    """
    degree(d)
    root = isqrt(d)
    if root*root != d or root < 4:
        raise ValueError("a square degree with sqrt(d)>=4 is required")
    if not isinstance(beta, F) or beta < 0:
        raise ValueError("exact nonnegative rational beta required")
    if type(terms) is not int or not 0 <= terms <= 128:
        raise ValueError("bounded nonnegative Taylor order required")
    x2 = (beta*d)**2
    term, lower = F(1), F(1)
    for k in range(1, terms+1):
        term *= x2/F((2*k-1)*(2*k))
        lower += term
    r2 = d*d+1
    initial = F(d+2, 2)
    flow_lower = (F(d, 2)+F(d*d, r2)+F(d*d, r2*r2)*(lower-1))/initial
    flow_bound_upper = 1/(1-F(22, 7*root))
    defect_lower = 4*(1+F(d*d, r2)*(lower-1)+d)/initial
    inside = beta*beta*(d+1) <= F(1, 64)
    return {"d": d, "beta": str(beta), "beta_squared_d_plus_one": str(beta*beta*(d+1)),
            "Taylor_terms": terms, "cosh_lower": str(lower),
            "flow_squared_ratio_lower": str(flow_lower),
            "incorrect_flow_squared_bound_upper": str(flow_bound_upper),
            "flow_bound_strictly_falsified": flow_lower > flow_bound_upper,
            "defect_squared_ratio_lower": str(defect_lower),
            "incorrect_defect_squared_bound": 4*d,
            "defect_bound_strictly_falsified": defect_lower > 4*d,
            "inside_beta_squared_d_plus_one_le_one_over_64": inside,
            "filtered_parent_gap_lower_from_existing_mass_lemma": "25/36" if inside else None,
            "classical_envelope_ratio_upper_from_existing_moment_bound": "128/127" if inside else None,
            "large_matrices_built": False, "parent_gap_disproved": False}


def dense_control(d, beta, s=0.17):
    degree(d)
    if d > 7:
        raise ValueError("dense reference capped at eight coefficient qubits")
    formula = star_formula(d, beta)
    if not math.isfinite(s):
        raise ValueError("finite filter time required")
    model = build_model(d+1, [(0, j) for j in range(1, d+1)])
    dim = len(model.h)
    identity = np.eye(dim)
    P = identity.copy()
    for j in range(2, d+1):
        P = P @ (identity+model.operators[1]@model.operators[j])/2
    Y = 1j*model.operators[0]@model.operators[1]
    witness = P@Y
    thermal = expm(-beta*model.h/2)

    def kms_norm_squared(x):
        value = np.trace(thermal@x.conj().T@thermal@x)/dim
        if abs(value.imag) > 1e-10 or value.real < -1e-10:
            raise ArithmeticError("invalid dense KMS norm")
        return float(value.real)

    def gradient(x):
        return sum(kms_norm_squared((x-z@x@z)/2) for z in model.z)

    gram = gradient(witness)
    defect = sum(kms_norm_squared(op@(z@witness@z)-(z@witness@z)@op)
                 for op, z in zip(model.operators, model.z))
    time = formula["quarter_rotation_time"]
    unitary = expm(1j*time*model.h)
    evolved = unitary@witness@unitary.conj().T
    rotated = P@(d*model.operators[0]-model.operators[1])/math.sqrt(d*d+1)
    evolved_gram = gradient(evolved)
    energy, vectors = eigh(model.h)
    u = beta*(energy[:, None]-energy[None, :])
    spectral_witness = vectors.T.conj()@witness@vectors
    filtered = vectors@(spectral_witness*np.exp(-u*u/8-u/4+1j*s*u))@vectors.T.conj()
    filtered_gram = gradient(filtered)
    w = 2.0**(-(d-1))
    errors = {
        "projector": float(np.linalg.norm(P@P-P)),
        "central_projector": max(float(np.linalg.norm(P@op-op@P)) for op in model.operators),
        "Hermitian_witness": float(np.linalg.norm(witness-witness.conj().T)),
        "quarter_rotation_identity": float(np.linalg.norm(evolved-rotated)),
        "initial_gradient": abs(gram/w-(1+d/2)),
        "defect_ratio": abs(defect/gram-math.exp(formula["log_defect_squared_ratio"])),
        "flow_ratio": abs(evolved_gram/gram-math.exp(formula["log_flow_squared_amplification"]))}
    if max(errors.values()) > 1e-9:
        raise ArithmeticError("independent dense star identity failed")
    filter_upper = math.exp(formula["log_gaussian_image_gradient_squared_ratio_upper"])
    if filtered_gram/gram > filter_upper+1e-9:
        raise ArithmeticError("Gaussian image bound failed")
    return {**formula, "dense_dimension": dim, "identity_errors": errors,
            "initial_KMS_gradient": gram, "defect_squared_ratio": defect/gram,
            "flow_squared_ratio": evolved_gram/gram,
            "filtered_image_gradient_squared_ratio": filtered_gram/gram,
            "filter_time_s": s, "mode": "exponential_dense_identity_control"}
