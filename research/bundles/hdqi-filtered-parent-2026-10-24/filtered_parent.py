"""Bounded real-time-filtered HDQI parent: finite reference controls only.

The circuit construction is described in FILTERED_PARENT.md. Dense diagonalization
here checks it; it is not the proposed quantum implementation or a gap proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigh, expm
from scipy.special import ndtr

DEPENDENCY = Path(__file__).resolve().parent.parent / "hdqi-parent-gap-2026-10-23"
sys.path.insert(0, str(DEPENDENCY))
from parent_gap import build_model, commutator, control_graphs, parents  # noqa: E402

LCU_NORM = math.exp(1 / 8)


def graph_phase(model):
    return np.diag([(-1) ** sum((y >> i & 1) * (y >> j & 1) for i, j in model.edges)
                    for y in range(1 << model.m)])


def sech(x):
    absolute = np.abs(x)
    return 2 * np.exp(-absolute) / (1 + np.exp(-2 * absolute))


def filtered_jump(model, beta, i, s=0.0):
    """Q_i(s) on coefficient labels, from exact finite spectral calculus."""
    if not math.isfinite(beta) or beta < 0 or not math.isfinite(s):
        raise ValueError("finite beta>=0 and finite s required")
    if not isinstance(i, int) or not 0 <= i < model.m:
        raise ValueError("invalid jump index")
    energies, u = eigh(model.h)
    frequencies = energies[:, None] - energies[None, :]
    argument = beta * frequencies
    weights = np.exp(-argument**2 / 8 - argument / 4 + 1j * s * argument)
    left = u @ ((u.T @ model.z[i] @ u) * weights) @ u.T
    phase = graph_phase(model)
    return (model.z[i] @ left - phase @ left.conj() @ phase) / 2


def _parent_with_kernels(model, beta, filter_fn, characteristic):
    if model.m > 5:
        raise ValueError("reference contraction costs O(16^m) storage; require m<=5")
    if not math.isfinite(beta) or beta < 0:
        raise ValueError("finite beta>=0 required")
    energies, u = eigh(model.h)
    phase = graph_phase(model)
    omega = energies[:, None] - energies[None, :]
    delta = (energies[:, None, None, None] + energies[None, None, None, :]
             - energies[None, :, None, None] - energies[None, None, :, None])
    chi2, chi4 = characteristic(beta * omega), characteristic(beta * delta)
    filter_values = filter_fn(beta * omega)
    terms = []
    for zi in model.z:
        matrix = (u.T @ zi @ u) * filter_values
        diagonal = u @ ((matrix.T @ matrix) * chi2) @ u.T
        insertion = u.T @ zi @ phase @ u
        cross = np.einsum("ba,bc,cd,abcd->ad", matrix, insertion, matrix,
                          chi4, optimize=True)
        cross = u @ cross @ u.T @ phase
        term = (diagonal + phase @ diagonal @ phase - cross - cross.T) / 4
        terms.append((term + term.T) / 2)
    return sum(terms), terms


def filtered_parent(model, beta):
    """Exact time integral as a dense reference contraction, no time quadrature.

    The outer density is 2 sech(2 pi s), with characteristic sech(omega/4).
    The four-index frequency contraction is exponential, and never used as
    an assumed efficient access primitive.
    """
    return _parent_with_kernels(model, beta,
                                lambda x: np.exp(-x*x/8 - x/4),
                                lambda x: sech(x/4))


def quadrature_plan(model, beta, delta):
    """Conservative operator-error budget for an explicit real-time LCU grid.

    No spectral gap, Hamiltonian eigenvalue, state-preparation oracle, or
    imaginary-time access enters this plan. Counts are resource upper bounds,
    not a claim that the grid/circuit was executed.
    """
    if not math.isfinite(beta) or beta <= 0 or not math.isfinite(delta) or not 0 < delta < 1:
        raise ValueError("beta>0 and 0<delta<1 required; beta=0 has exact parent N")
    m, lam, c = model.m, sum(abs(x) for x in model.couplings), LCU_NORM
    outer_cut = math.log(16 * m * c*c / (math.pi * delta)) / (2 * math.pi)
    outer_step = delta / (8 * m * beta * max(lam, 1e-300) * c*c)
    outer_bins = max(1, math.ceil(2 * outer_cut / outer_step))
    eta = delta / (4 * m * c)
    inner_cut = math.sqrt(math.log(2 * c / eta) / 2)
    inner_step = eta / (c * (1 + 2 * beta * lam))
    inner_bins = max(1, math.ceil(2 * inner_cut / inner_step))
    actual_outer_step = 2 * outer_cut / outer_bins
    actual_inner_step = 2 * inner_cut / inner_bins
    inner_bound = c * (math.exp(-2 * inner_cut**2)
                       + (1 + 2 * beta * lam) * actual_inner_step / 2)
    tail = m * c*c * 4 / math.pi * math.exp(-2 * math.pi * outer_cut)
    outer_error = 2 * m * beta * lam * c*c * actual_outer_step
    filter_error = 2 * m * c * inner_bound
    return {"m": m, "beta": beta, "requested_operator_error": delta,
            "public_pauli_norm_sum": lam, "jump_lcu_normalization": c,
            "parent_lcu_normalization_bound": m * c*c,
            "outer_cut": outer_cut, "outer_bins": outer_bins,
            "inner_cut": inner_cut, "inner_bins": inner_bins,
            "largest_real_time": beta * (outer_cut + inner_cut),
            "outer_tail_error_bound": tail, "outer_bin_error_bound": outer_error,
            "filter_error_bound": filter_error,
            "total_analytic_error_bound": tail + outer_error + filter_error,
            "unbudgeted_errors": ["weight/phase arithmetic rounding", "Hamiltonian simulation error"],
            "circuit_executed": False}


def _bins(cut, count):
    endpoints = np.linspace(-cut, cut, count + 1)
    return endpoints, (endpoints[:-1] + endpoints[1:]) / 2


def discrete_parent_control(model, beta, delta):
    """Classical spectral reference of the priced quadrature, not a circuit."""
    plan = quadrature_plan(model, beta, delta)
    if plan["inner_bins"] > 100000 or plan["outer_bins"] > 100000:
        raise ValueError("control grid too large; resource ledger is not an execution request")
    ve, v = _bins(plan["inner_cut"], plan["inner_bins"])
    se, s = _bins(plan["outer_cut"], plan["outer_bins"])
    vw = np.diff(ndtr(2 * ve))
    # Stable CDF of 2 sech(2 pi s).
    scdf = np.where(se <= 0, 2 / math.pi * np.arctan(np.exp(-2 * math.pi * np.abs(se))),
                    1 - 2 / math.pi * np.arctan(np.exp(-2 * math.pi * np.abs(se))))
    sw = np.diff(scdf)

    def weighted_cosine(values, nodes, weights, offset=0):
        answer = np.zeros_like(values)
        for node, weight in zip(nodes, weights):
            answer += weight * np.cos(node * (values + offset))
        return answer

    parent, terms = _parent_with_kernels(
        model, beta,
        lambda x: LCU_NORM * weighted_cosine(x, v, vw, 1),
        lambda x: weighted_cosine(x, s, sw))
    return parent, terms, plan


def taylor_coefficients(model):
    """Exact dyadic beta coefficients; sech time law has variance 1/16."""
    phase = graph_phase(model)
    first, second = np.zeros_like(model.h), np.zeros_like(model.h)
    for zi, ni in zip(model.z, model.occupations):
        ci = commutator(model.h, zi)
        di = commutator(model.h, ci)
        q1 = (-zi @ ci + phase @ ci @ phase) / 8
        q_noise = (zi @ ci + phase @ ci @ phase) / 2
        mean_q2 = -(zi @ di - phase @ di @ phase) / 16
        first += ni @ q1 + q1.T @ ni
        second += (ni @ mean_q2 + mean_q2.T @ ni + q1.T @ q1
                   + q_noise.T @ q_noise / 16)
    generator = (model.k + phase @ model.k @ phase) / 4
    rotated_second = (second + commutator(generator, first)
                      + commutator(generator, commutator(generator, model.number)) / 2)
    return first, rotated_second, generator


def one_excitation_prediction(model):
    js = np.array(model.couplings)
    adjacency = np.zeros((model.m, model.m))
    for i, j in model.edges:
        adjacency[i, j] = adjacency[j, i] = 1
    return np.diag(-js*js/2 + adjacency @ (js*js) / 4) - 3/4 * js[:, None] * adjacency * js[None, :]


def build_receipt():
    models = {name: model for name, model in control_graphs().items() if model.m <= 5}
    spectra, algebra = [], []
    for name, model in models.items():
        first, coefficient, generator = taylor_coefficients(model)
        slots = [1 << i for i in range(model.m)]
        algebra.append({"graph": name,
                        "linear_cancel_exact": bool(np.array_equal(first + commutator(generator, model.number), np.zeros_like(first))),
                        "one_excitation_identity_exact": bool(np.array_equal(coefficient[np.ix_(slots, slots)], one_excitation_prediction(model))),
                        "gap_beta2_coefficient": float(eigh(one_excitation_prediction(model), eigvals_only=True)[0])})
        for beta in (.1, .3, .6):
            parent, terms = filtered_parent(model, beta)
            pilot = parents(model, beta)["pilot"]
            ev = eigh(parent, eigvals_only=True)
            spectra.append({"graph": name, "m": model.m, "beta": beta,
                            "kappa": beta*beta*model.degree,
                            "kappa_with_isolated_guard": beta*beta*(model.degree + 1),
                            "finite_gap": float(ev[1]), "ground_eigenvalue": float(ev[0]),
                            "gap_above_reference_diagnostic_floor": bool(ev[1] > 1e-11),
                            "pilot_residual": float(np.linalg.norm(parent @ pilot)),
                            "largest_term_norm": float(max(eigh(term, eigvals_only=True)[-1] for term in terms))})
    edge = models["edge"]
    exact, _ = filtered_parent(edge, .3)
    discrete, _, plan = discrete_parent_control(edge, .3, .05)
    root = Path(__file__).resolve().parent
    sources = [root / "filtered_parent.py", root / "test_filtered_parent.py",
               root / "FILTERED_PARENT.md", DEPENDENCY / "parent_gap.py"]
    return {"schema": "hdqi-filtered-parent-control-v1",
            "status": "bounded_constructive_parent_with_unproved_uniform_gap",
            "prior_art": ["https://arxiv.org/html/2604.22996v1", "https://arxiv.org/html/2610.03697v1"],
            "claims": {"uniform_gap_proved": False, "quantum_circuit_executed": False,
                       "quantum_speedup_established": False, "novelty_established": False,
                       "independently_reviewed": False},
            "scope": "Own kernel/access derivation and dense controls; no polynomial state-preparation theorem.",
            "dense_reference_warning": "Floating-point spectra are not certified eigenvalue intervals; values below 1e-11 are unresolved diagnostics.",
            "algebra": algebra, "finite_spectra": spectra,
            "priced_quadrature_control": {"plan": plan,
                                         "measured_operator_error": float(np.linalg.norm(exact - discrete, 2))},
            "commuting_temperature_guard": {"m": 1, "degree": 0, "beta": 10,
                                            "exact_gap": math.exp(-100) * math.cosh(10),
                                            "meaning": "beta^2*d alone cannot constrain edgeless inputs; product-state preparation remains easy"},
            "sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in sources}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = build_receipt()
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"output": str(args.output.resolve()), "status": receipt["status"],
                      "finite_spectra": len(receipt["finite_spectra"]),
                      "quadrature_error": receipt["priced_quadrature_control"]["measured_operator_error"]}))


if __name__ == "__main__":
    main()
