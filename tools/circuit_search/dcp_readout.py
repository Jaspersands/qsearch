"""Search local readout circuits for DCP phase packets: product, adaptive and collective.

    python tools/circuit_search/dcp_readout.py                     # all instances, writes research/audits/
    python tools/circuit_search/dcp_readout.py --instances mod64 --restarts 20

Each packet is one qubit rho(theta, gamma) = (I + gamma cos(theta) X + gamma sin(theta) Y) / 2,
matching theorems/dcp_multi_packet_collective_helstrom_product_likelihood_bridge.py.
The task is binary: H0 (secret 0) against H1 (secret s*, or s* with unknown sign).
Scores are total-variation distances between outcome laws (success = (1 + TV) / 2).

Search spaces, all built from one single-qubit rotation per wire, a Z measurement and
classical feed-forward (circuit-expressible, no entangling gate):

- product: each wire measured along its own Bloch direction, outcomes combined optimally;
- adaptive: wires measured in sequence, each direction chosen by the earlier outcomes;
- collective: the Helstrom optimum over all joint measurements (the upper bound).

The recorded mod-64 instance (headers 16 and 17, secret 1, pure packets) has X-basis
0.7745, local-Helstrom product 0.7410 and collective 0.8801.
"""

from __future__ import annotations

import argparse
import datetime as dt
import itertools
import json
import math
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

Hypothesis = list[tuple[float, list[np.ndarray]]]  # mixture of product states: (weight, Bloch vector per wire)

PAULI = (
    np.array([[0, 1], [1, 0]], dtype=complex),
    np.array([[0, -1j], [1j, 0]], dtype=complex),
    np.array([[1, 0], [0, -1]], dtype=complex),
)
INSTANCES = {
    "mod64": ([2 * math.pi * 16 / 64, 2 * math.pi * 17 / 64], [1.0, 1.0]),
    "single": ([math.pi / 3], [0.85]),
    "two_packet": ([math.pi / 3, math.pi / 2], [0.85, 0.8]),
    "three_packet": ([math.pi / 4, math.pi / 3, 2 * math.pi / 3], [0.85, 0.8, 0.75]),
}


def bloch(theta: float, gamma: float) -> np.ndarray:
    return np.array([gamma * math.cos(theta), gamma * math.sin(theta), 0.0])


def direction(alpha: float, beta: float) -> np.ndarray:
    return np.array([math.sin(alpha) * math.cos(beta), math.sin(alpha) * math.sin(beta), math.cos(alpha)])


def known_secret_hypotheses(thetas, gammas) -> tuple[Hypothesis, Hypothesis]:
    h0 = [(1.0, [bloch(0.0, g) for g in gammas])]
    h1 = [(1.0, [bloch(t, g) for t, g in zip(thetas, gammas)])]
    return h0, h1


def unknown_sign_hypotheses(thetas, gammas) -> tuple[Hypothesis, Hypothesis]:
    """H1 is the equal mixture over s* and -s* (all packet angles flip together)."""
    h0 = [(1.0, [bloch(0.0, g) for g in gammas])]
    h1 = [
        (0.5, [bloch(t, g) for t, g in zip(thetas, gammas)]),
        (0.5, [bloch(-t, g) for t, g in zip(thetas, gammas)]),
    ]
    return h0, h1


def density_matrix(h: Hypothesis) -> np.ndarray:
    total = None
    for weight, vectors in h:
        term = np.array([[1.0]], dtype=complex)
        for r in vectors:
            term = np.kron(term, 0.5 * (np.eye(2) + sum(r[i] * PAULI[i] for i in range(3))))
        total = weight * term if total is None else total + weight * term
    return total


def collective_tv(h0: Hypothesis, h1: Hypothesis) -> float:
    return float(0.5 * np.abs(np.linalg.eigvalsh(density_matrix(h0) - density_matrix(h1))).sum())


def partial_transpose(rho: np.ndarray, subsystems, wires: int) -> np.ndarray:
    """Transpose the listed qubits of a 2^wires x 2^wires matrix."""
    t = rho.reshape((2,) * (2 * wires))
    axes = list(range(2 * wires))
    for q in subsystems:
        axes[q], axes[wires + q] = axes[wires + q], axes[q]
    return t.transpose(axes).reshape(rho.shape)


def _psd_part(x: np.ndarray) -> np.ndarray:
    x = 0.5 * (x + x.conj().T)
    w, v = np.linalg.eigh(x)
    return (v * np.clip(w, 0, None)) @ v.conj().T


def ppt_bound(h0: Hypothesis, h1: Hypothesis) -> dict | None:
    """The best two-outcome measurement whose effects stay positive under partial transpose across
    every cut. Every local protocol (one-way, two-way, any number of rounds) is such a measurement,
    so this bounds them all from above. Returns the solver's primal value and a rigorous upper bound
    rebuilt from its dual: for PSD B, C_S, D_S with R = delta - B + sum_S PT_S(C_S - D_S) <= 0,
    every PPT effect M has tr(M delta) <= tr(B) + sum_S tr(D_S); a positive top eigenvalue of R is
    absorbed into B. None if cvxpy is missing."""
    try:
        import cvxpy as cp
    except ImportError:
        return None
    delta = density_matrix(h0) - density_matrix(h1)
    d = delta.shape[0]
    wires = int(round(math.log2(d)))
    m = cp.Variable((d, d), hermitian=True)
    eye = np.eye(d)
    upper_c = eye - m >> 0
    constraints = [m >> 0, upper_c]
    cuts = []
    for size in range(1, wires):
        for cut in itertools.combinations(range(1, wires), size):
            pt = m
            for q in cut:
                pt = cp.partial_transpose(pt, [2] * wires, q)
            pt = 0.5 * (pt + pt.H)
            lower, upper = pt >> 0, eye - pt >> 0
            constraints += [lower, upper]
            cuts.append((cut, lower, upper))
    problem = cp.Problem(cp.Maximize(cp.real(cp.trace(m @ delta))), constraints)
    with warnings.catch_warnings():  # "may be inaccurate": the dual certificate below is exact regardless
        warnings.simplefilter("ignore", UserWarning)
        problem.solve(solver=cp.CLARABEL if "CLARABEL" in cp.installed_solvers() else None)
    b = _psd_part(np.asarray(upper_c.dual_value))
    residual = delta - b
    dual = 0.0
    for cut, lower, upper in cuts:
        c, dd = _psd_part(np.asarray(lower.dual_value)), _psd_part(np.asarray(upper.dual_value))
        residual = residual + partial_transpose(c - dd, cut, wires)
        dual += float(np.trace(dd).real)
    slack = max(0.0, float(np.linalg.eigvalsh(0.5 * (residual + residual.conj().T)).max()))
    dual += float(np.trace(b).real) + slack * d
    return {"primal": float(problem.value), "upper": dual, "status": problem.status}


def ppt_tv(h0: Hypothesis, h1: Hypothesis) -> float | None:
    """Certified upper bound on every local protocol, capped at the collective optimum."""
    bound = ppt_bound(h0, h1)
    return None if bound is None else min(bound["upper"], collective_tv(h0, h1))


def _coin_tv(p0: list[float], p1: list[float]) -> float:
    tv = 0.0
    for bits in itertools.product((0, 1), repeat=len(p0)):
        a = math.prod(p0[j] if b == 0 else 1 - p0[j] for j, b in enumerate(bits))
        c = math.prod(p1[j] if b == 0 else 1 - p1[j] for j, b in enumerate(bits))
        tv += 0.5 * abs(a - c)
    return tv


def x_basis_tv(thetas, gammas) -> float:
    return _coin_tv([0.5 * (1 + g) for g in gammas], [0.5 * (1 + g * math.cos(t)) for t, g in zip(thetas, gammas)])


def local_helstrom_product_tv(thetas, gammas) -> float:
    """Each wire measured in its own single-wire Helstrom basis; outcomes combined optimally."""
    h0, h1 = known_secret_hypotheses(thetas, gammas)
    dirs = []
    for r0, r1 in zip(h0[0][1], h1[0][1]):
        diff = r0 - r1
        dirs.append(diff / np.linalg.norm(diff) if np.linalg.norm(diff) > 0 else np.array([0.0, 0.0, 1.0]))
    return product_tv(h0, h1, dirs)


def _distribution(h: Hypothesis, chooser, order: tuple[int, ...]) -> dict[tuple[int, ...], float]:
    law: dict[tuple[int, ...], float] = {}
    for outcome in itertools.product((1, -1), repeat=len(order)):
        p = 0.0
        for weight, vectors in h:
            term = weight
            for k, wire in enumerate(order):
                n = chooser(outcome[:k], k)
                term *= 0.5 * (1 + outcome[k] * float(n @ vectors[wire]))
            p += term
        law[outcome] = p
    return law


def product_tv(h0: Hypothesis, h1: Hypothesis, dirs: list[np.ndarray]) -> float:
    order = tuple(range(len(dirs)))
    a = _distribution(h0, lambda prefix, k: dirs[k], order)
    b = _distribution(h1, lambda prefix, k: dirs[k], order)
    return 0.5 * sum(abs(a[o] - b[o]) for o in a)


def adaptive_distribution(h: Hypothesis, tree: dict[tuple[int, ...], np.ndarray], order: tuple[int, ...]):
    return _distribution(h, lambda prefix, k: tree[prefix], order)


def adaptive_tv(h0: Hypothesis, h1: Hypothesis, tree: dict, order: tuple[int, ...]) -> float:
    a, b = adaptive_distribution(h0, tree, order), adaptive_distribution(h1, tree, order)
    return 0.5 * sum(abs(a[o] - b[o]) for o in a)


def _rotation_to_z(n: np.ndarray) -> np.ndarray:
    """Unitary U with U (n . sigma) U^dagger = Z: R_y(-alpha) R_z(-beta)."""
    alpha = math.acos(max(-1.0, min(1.0, float(n[2]))))
    beta = math.atan2(float(n[1]), float(n[0]))
    rz = np.array([[np.exp(1j * beta / 2), 0], [0, np.exp(-1j * beta / 2)]])
    ry = np.array([[math.cos(alpha / 2), math.sin(alpha / 2)], [-math.sin(alpha / 2), math.cos(alpha / 2)]], dtype=complex)
    return ry @ rz


def _on_wire(op: np.ndarray, wire: int, wires: int) -> np.ndarray:
    out = np.array([[1.0]], dtype=complex)
    for j in range(wires):
        out = np.kron(out, op if j == wire else np.eye(2))
    return out


def simulate_adaptive_circuit(rho: np.ndarray, tree: dict, order: tuple[int, ...]) -> dict[tuple[int, ...], float]:
    """Density-matrix run of the circuit: rotate, measure Z, feed the outcome forward."""
    wires = len(order)
    law: dict[tuple[int, ...], float] = {}

    def run(state: np.ndarray, prefix: tuple[int, ...]) -> None:
        k = len(prefix)
        if k == wires:
            law[prefix] = float(np.real(np.trace(state)))
            return
        u = _on_wire(_rotation_to_z(tree[prefix]), order[k], wires)
        rotated = u @ state @ u.conj().T
        for outcome in (1, -1):
            proj = _on_wire(0.5 * (np.eye(2) + outcome * PAULI[2]), order[k], wires)
            run(proj @ rotated @ proj, prefix + (outcome,))

    run(rho, ())
    return law


@dataclass
class SearchResult:
    tv: float
    order: tuple[int, ...]
    angles: dict[str, list[float]]
    evaluations: int = 0
    extra: dict = field(default_factory=dict)


def _prefixes(wires: int) -> list[tuple[int, ...]]:
    return [p for k in range(wires) for p in itertools.product((1, -1), repeat=k)]


def _optimize(objective, size: int, restarts: int, seed: int, starts: list[np.ndarray] = ()) -> tuple[float, np.ndarray, int]:
    from scipy.optimize import minimize

    rng = np.random.default_rng(seed)
    best_value, best_x, calls = -1.0, None, 0
    candidates = list(starts) + [rng.uniform(0, math.pi, size) * np.tile([1.0, 2.0], size // 2) for _ in range(restarts)]
    for x0 in candidates:
        result = minimize(lambda x: -objective(x), x0, method="Nelder-Mead",
                          options={"xatol": 1e-11, "fatol": 1e-13, "maxiter": 40000, "maxfev": 40000, "adaptive": True})
        polish = minimize(lambda x: -objective(x), result.x, method="Powell", options={"xtol": 1e-11, "ftol": 1e-14})
        calls += result.nfev + polish.nfev
        value = -float(polish.fun)
        if value > best_value:
            best_value, best_x = value, polish.x
    return best_value, best_x, calls


def search_product(h0: Hypothesis, h1: Hypothesis, restarts: int = 10, seed: int = 0) -> SearchResult:
    wires = len(h0[0][1])

    def objective(x):
        return product_tv(h0, h1, [direction(x[2 * j], x[2 * j + 1]) for j in range(wires)])

    x_start = np.tile([math.pi / 2, 0.0], wires)
    value, x, calls = _optimize(objective, 2 * wires, restarts, seed, [x_start])
    return SearchResult(value, tuple(range(wires)), {f"wire{j}": [float(x[2 * j]), float(x[2 * j + 1])] for j in range(wires)}, calls)


def search_adaptive(h0: Hypothesis, h1: Hypothesis, restarts: int = 10, seed: int = 0) -> SearchResult:
    wires = len(h0[0][1])
    prefixes = _prefixes(wires)
    best: SearchResult | None = None
    total_calls = 0
    for order in itertools.permutations(range(wires)):
        def tree_of(x, order=order):
            return {p: direction(x[2 * i], x[2 * i + 1]) for i, p in enumerate(prefixes)}

        def objective(x, order=order):
            return adaptive_tv(h0, h1, tree_of(x), order)

        value, x, calls = _optimize(objective, 2 * len(prefixes), restarts, seed, [np.tile([math.pi / 2, 0.0], len(prefixes))])
        total_calls += calls
        if best is None or value > best.tv:
            angles = {"/".join(map(str, p)) or "root": [float(x[2 * i]), float(x[2 * i + 1])] for i, p in enumerate(prefixes)}
            best = SearchResult(value, order, angles)
    assert best is not None
    best.evaluations = total_calls
    return best


def evaluate(thetas, gammas, restarts: int, seed: int, unknown_sign: bool) -> dict:
    h0, h1 = (unknown_sign_hypotheses if unknown_sign else known_secret_hypotheses)(thetas, gammas)
    wires = len(thetas)
    product = search_product(h0, h1, restarts, seed)
    adaptive = search_adaptive(h0, h1, restarts, seed)
    collective = collective_tv(h0, h1)
    row = {
        "x_basis": product_tv(h0, h1, [direction(math.pi / 2, 0.0)] * wires),
        "best_product": product.tv,
        "best_adaptive": adaptive.tv,
        "collective": collective,
        "adaptive_gap_to_collective": collective - adaptive.tv,
        "best_product_angles": product.angles,
        "best_adaptive_protocol": {"order": list(adaptive.order), "angles": adaptive.angles},
        "circuits_evaluated": product.evaluations + adaptive.evaluations,
    }
    if not unknown_sign:
        row["local_helstrom_product"] = local_helstrom_product_tv(thetas, gammas)
    bound = ppt_bound(h0, h1)
    if bound is not None:
        upper = min(bound["upper"], collective)
        row.update({
            "ppt_primal": bound["primal"],
            "ppt_upper": upper,
            "certified_local_gap": collective - upper,
            "open_window": upper - adaptive.tv,
        })
    return row


def run(names: list[str], restarts: int, seed: int) -> dict:
    instances = []
    for name in names:
        thetas, gammas = INSTANCES[name]
        instances.append({
            "name": name,
            "thetas": thetas,
            "gammas": gammas,
            "known_secret": evaluate(thetas, gammas, restarts, seed, unknown_sign=False),
            "unknown_sign": evaluate(thetas, gammas, restarts, seed, unknown_sign=True),
        })
    return {
        "generated_by": "tools/circuit_search/dcp_readout.py",
        "generated_on": dt.date.today().isoformat(),
        "seed": seed,
        "restarts": restarts,
        "score": "total-variation distance between outcome laws; success probability = (1 + TV) / 2",
        "instances": instances,
    }


def render(result: dict) -> str:
    lines = [
        "# Local Readout Search on DCP Phase Packets",
        "",
        f"Generated {result['generated_on']} by `tools/circuit_search/dcp_readout.py` (seed {result['seed']}, "
        f"{result['restarts']} restarts per search). Not a registry entry; for the research agents to evaluate.",
        "",
        "Scores are total-variation distances between the outcome laws under H0 and H1 (success = (1 + TV) / 2).",
        "Product and adaptive receivers use one single-qubit rotation per wire, a Z measurement and classical",
        "feed-forward. No entangling gate is used. Collective is the Helstrom optimum over all joint measurements.",
        "",
        "PPT bound is a certified upper bound on every local protocol, including two-way and multi-round ones:",
        "the best measurement whose effects stay positive under partial transpose across every cut, solved as an",
        "SDP and certified by a repaired dual solution. Certified gap = collective - PPT bound: no local protocol",
        "of any kind gets closer to the collective score. Open window = PPT bound - best adaptive: the range a",
        "richer local protocol than this search covers could still gain.",
        "",
    ]
    for setting, heading in (("known_secret", "Known secret"), ("unknown_sign", "Unknown sign of the secret")):
        lines += [f"## {heading}", "",
                  "| Instance | X basis | Local Helstrom product | Best product | Best adaptive | PPT bound | Collective "
                  "| Certified gap | Open window |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for inst in result["instances"]:
            row = inst[setting]
            local = f"{row['local_helstrom_product']:.4f}" if "local_helstrom_product" in row else "-"
            ppt = f"{row['ppt_upper']:.4f}" if "ppt_upper" in row else "-"
            gap = f"{max(row['certified_local_gap'], 0.0):.1e}" if "ppt_upper" in row else "-"
            window = f"{max(row['open_window'], 0.0):.1e}" if "ppt_upper" in row else "-"
            lines.append(
                f"| {inst['name']} | {row['x_basis']:.4f} | {local} | {row['best_product']:.4f} | "
                f"{row['best_adaptive']:.4f} | {ppt} | {row['collective']:.4f} | {gap} | {window} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--instances", default=",".join(INSTANCES))
    parser.add_argument("--restarts", type=int, default=12)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", type=Path, help="JSON path; default research/audits/circuit_search_dcp_readout.json")
    args = parser.parse_args(argv)
    result = run(args.instances.split(","), args.restarts, args.seed)
    out = args.out or args.root / "research" / "audits" / "circuit_search_dcp_readout.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    out.with_name("CIRCUIT_SEARCH_DCP_READOUT.md").write_text(render(result), encoding="utf-8")
    print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
