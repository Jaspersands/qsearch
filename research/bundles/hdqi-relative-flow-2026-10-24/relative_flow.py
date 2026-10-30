"""Degree-scale real-time gradient bounds: finite controls, not a gap solver.

The universal inequalities are proved in RELATIVE_FLOW.md. Dense matrices
below are only controls. Large graph rows are analytic parameter ledgers.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import ndtr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-filtered-parent-2026-10-24"))
from filtered_parent import LCU_NORM, build_model, commutator, graph_phase  # noqa: E402


def weighted_degree(model):
    totals = [0.0] * model.m
    for i, j in model.edges:
        totals[i] += model.couplings[j] ** 2
        totals[j] += model.couplings[i] ** 2
    return max(totals)


def liouvillian(model, jump=None):
    phase = graph_phase(model)
    result = model.h - phase @ model.h @ phase
    if jump is not None:
        if not isinstance(jump, int) or isinstance(jump, bool) or not 0 <= jump < model.m:
            raise ValueError("invalid tagged jump")
        result = result - 2 * model.couplings[jump] * model.operators[jump]
    return result


def parity_projectors(model):
    identity = np.eye(1 << model.m)
    answer = []
    for i in range(model.m):
        parity = identity.copy()
        for edge in model.edges:
            if i in edge:
                other = edge[1] if edge[0] == i else edge[0]
                parity = parity @ model.z[other]
        answer.append((identity - parity) / 2)
    return answer


def gradient_data(model, jump=None):
    ell = liouvillian(model, jump)
    identity = np.eye(1 << model.m)
    grads = list(model.occupations)
    weight = model.number.copy()
    rho = weighted_degree(model)
    if jump is not None:
        grads = [identity, *grads]
        weight += identity
        rho = max(rho, model.couplings[jump] ** 2)
    gradient = np.vstack(grads)
    defect = np.vstack([commutator(d, ell) for d in grads])
    odd = parity_projectors(model)
    exact_gram = sum(4 * j*j * q for j, q in zip(model.couplings, odd))
    if jump is not None:
        exact_gram += 4 * model.couplings[jump] ** 2 * (identity - 2 * odd[jump])
    return ell, gradient, weight, defect, exact_gram, rho


def relative_norm(matrix, weight):
    """Dense weighted norm; check the nullspace instead of silently dropping it."""
    values = np.diag(weight)
    positive = values > 0
    if np.linalg.norm(matrix[:, ~positive]) > 1e-10:
        raise ValueError("operator does not vanish on seminorm kernel")
    return float(np.linalg.norm(matrix[:, positive] / np.sqrt(values[positive]), 2))


def folded_normal(t):
    """E exp(t|V|) and two derivatives for V~N(0,1/4)."""
    if not math.isfinite(t) or t < 0 or t > 50:
        raise ValueError("require finite 0<=t<=50 for this numerical ledger")
    mgf = 2 * math.exp(t*t / 8) * float(ndtr(t / 2))
    first = t * mgf / 4 + 1 / math.sqrt(2 * math.pi)
    second = (1 / 4 + t*t / 16) * mgf + t / (4 * math.sqrt(2 * math.pi))
    return mgf, first, second


def filter_bounds(beta, rho, s=0.0):
    if any(not math.isfinite(x) for x in (beta, rho, s)) or beta < 0 or rho < 0:
        raise ValueError("finite beta,rho>=0 and finite s required")
    a = 2 * beta * math.sqrt(rho)
    mv, _, _ = folded_normal(a)
    fixed = LCU_NORM * (math.exp(a * abs(s)) * mv - 1)
    result = {"beta": beta, "rho": rho, "beta_squared_rho": beta*beta*rho,
              "fixed_s_relative_commutator_bound": fixed,
              "outer_square_bound_available": False,
              "outer_mean_square_relative_commutator_bound": None,
              "parent_gap_certified": False}
    # The squared estimate needs E exp(2a|S|), not just E exp(a|S|).
    t = 2 * a
    rate = 2 * math.pi
    if t < rate:
        mv, mv1, mv2 = folded_normal(t)
        tail = 4 / math.pi
        ms = 1 + tail * t / (rate - t)
        ms1 = tail * rate / (rate - t)**2
        ms2 = 2 * tail * rate / (rate - t)**3
        square = LCU_NORM**2 * a*a * (mv2 * ms + 2 * mv1 * ms1 + mv * ms2)
        result.update(outer_square_bound_available=True,
                      outer_mean_square_relative_commutator_bound=square)
    return result


def multiplier(ell, beta, s):
    values, vectors = eigh(ell)
    u = beta * values
    return (vectors * np.exp(-u*u / 8 - u / 4 + 1j * s * u)) @ vectors.T


def dense_control(model, beta=0.08, time=0.19, s=0.21):
    rows = []
    for jump in (None, *range(model.m)):
        ell, grad, weight, defect, exact_gram, rho = gradient_data(model, jump)
        actual_gram = defect.T @ defect
        assert np.array_equal(actual_gram, exact_gram)
        assert np.min(np.diag(4 * rho * weight - exact_gram)) >= -1e-12
        relative_defect = relative_norm(defect, weight)
        assert relative_defect <= 2 * math.sqrt(rho) + 1e-10

        evolved = expm(1j * time * ell)
        direct_sum = np.kron(np.eye(grad.shape[0] // ell.shape[0]), evolved)
        flow_norm = relative_norm(grad @ evolved, weight)
        flow_bound = math.exp(2 * abs(time) * math.sqrt(rho))
        comm_norm = relative_norm(grad @ evolved - direct_sum @ grad, weight)
        assert flow_norm <= flow_bound + 1e-10
        assert comm_norm <= flow_bound - 1 + 1e-10

        filt = multiplier(ell, beta, s)
        direct_filter = np.kron(np.eye(grad.shape[0] // ell.shape[0]), filt)
        filter_norm = relative_norm(grad @ filt - direct_filter @ grad, weight)
        bound = filter_bounds(beta, rho, s)
        assert filter_norm <= bound["fixed_s_relative_commutator_bound"] + 1e-10
        row = {"m": model.m, "edges": model.edges, "couplings": model.couplings,
               "tagged_jump": jump, "rho": rho,
               "exact_diagonal_gram_identity": True,
               "defect_relative_norm": relative_defect,
               "defect_bound": 2 * math.sqrt(rho),
               "real_time_gradient_norm": flow_norm, "real_time_bound": flow_bound,
               "real_time_commutator_norm": comm_norm,
               "filter_commutator_norm": filter_norm, **bound}
        if jump is not None:
            # Independent energy-basis construction of Zi L_i(s)|vacuum>.
            energy, u = eigh(model.h)
            omega = beta * (energy[:, None] - energy[None, :])
            left = u @ ((u.T @ model.z[jump] @ u) *
                        np.exp(-omega*omega/8 - omega/4 + 1j*s*omega)) @ u.T
            coefficient = model.z[jump] @ left[:, 0]
            error = float(np.linalg.norm(coefficient - filt[:, 0]))
            assert error < 1e-10
            first_moment = float(np.vdot(coefficient, model.number @ coefficient).real)
            assert first_moment <= bound["fixed_s_relative_commutator_bound"]**2 + 1e-10
            row.update(jump_coefficient_identity_error=error,
                       unnormalized_jump_word_weight=first_moment)
        rows.append(row)
    return rows


def product_weight_counterexample(m, beta):
    if not isinstance(m, int) or isinstance(m, bool) or m < 1 or not math.isfinite(beta) or beta < 0:
        raise ValueError("m>=1 integer and finite beta>=0 required")
    log_cosh = float(np.logaddexp(beta, -beta) - math.log(2))
    return {"m": m, "beta": beta, "anticommutation_degree": 0,
            "log_thermal_over_trace_low_projector_dirichlet_ratio":
                (m - 1) * (beta - log_cosh),
            "log_thermal_over_trace_high_projector_dirichlet_ratio":
                (m - 1) * (-beta - log_cosh),
            "log_kms_over_trace_low_projector_commutator_ratio":
                (m - 1) * beta - m * log_cosh,
            "log_kms_over_trace_high_projector_commutator_ratio":
                -(m - 1) * beta - m * log_cosh,
            "interpretation": "fails dimension-free metric comparison, not a mixing lower bound",
            "easy_product_state": True}


def matching_imaginary_time_counterexample(blocks, tau):
    if not isinstance(blocks, int) or isinstance(blocks, bool) or blocks < 1 or not math.isfinite(tau) or tau < 0:
        raise ValueError("blocks>=1 integer and finite tau>=0 required")
    return {"blocks": blocks, "m": 2 * blocks, "weighted_degree": 1,
            "tau": tau, "log_gradient_amplification_on_eigenoperator":
                2 * math.sqrt(2) * tau * blocks,
            "incorrect_real_time_bound_log": 2 * tau,
            "interpretation": "real-time estimate cannot be analytically continued as a norm bound"}


def run():
    models = [build_model(1, []), build_model(3, [], (1, 0.5, -0.25)),
              build_model(2, [(0, 1)]),
              build_model(4, [(0, 1), (1, 2), (2, 3)], (1, -0.5, 0.25, 1)),
              build_model(5, [(0, j) for j in range(1, 5)]),
              build_model(4, [(0, 1), (2, 3)]),
              build_model(4, [(i, j) for i in range(4) for j in range(i + 1, 4)])]
    rows = [row for model in models for row in dense_control(model)]
    ledgers = []
    for degree in (16, 256, 4096, 65536):
        m = degree*degree + 1
        beta = math.sqrt(0.01 / (degree + 1))
        ledgers.append({"graph": "connected circulant with neighbors +/-1,...,+/-d/2",
                        "dense_instance_constructed": False, "m": m, "degree": degree,
                        "beta_squared_mass": beta*beta*m,
                        "mass_gap_perturbation_radius": math.sqrt(5) / 2 * LCU_NORM * beta * math.sqrt(m),
                        **filter_bounds(beta, degree)})
    sources = (Path(__file__), Path(__file__).with_name("test_relative_flow.py"),
               Path(__file__).with_name("RELATIVE_FLOW.md"), Path(__file__).with_name("HANDOFF.md"),
               ROOT / "hdqi-parent-gap-2026-10-23/parent_gap.py",
               ROOT / "hdqi-filtered-parent-2026-10-24/filtered_parent.py")
    return {"status": "local unreviewed analytic lemmas with finite controls",
            "parent_gap_certified": False, "quantum_preparation_executed": False,
            "novelty_certified": False, "dense_rows": rows, "parameter_only_rows": ledgers,
            "thermal_metric_counterexamples": [product_weight_counterexample(m, 0.1)
                                                for m in (2, 16, 256, 4096)],
            "imaginary_time_counterexamples": [matching_imaginary_time_counterexample(r, 0.1)
                                                 for r in (1, 8, 64, 512)],
            "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sources}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
