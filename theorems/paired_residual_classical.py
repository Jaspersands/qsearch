"""Feasible classical search in the paired residual problem's information manifold.

Exact field updates and a scoped uniform-component mean bound. Greedy adaptive
search, information-set re-anchoring, 2-coordinate block moves, and simulated
annealing are deliberately OUTSIDE that bound; no classical hardness is inferred.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import exp
from pathlib import Path
import random
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.nonlinear_residual_lift import canonical, evaluate, load_reference
from theorems.paired_residual_decoder import REPORT as QUANTUM_REPORT, parameters
from theorems.prime_character_finite_readout import sqrt_interval
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT/"research/classical_baselines/paired_residual_classical.json"


@dataclass(frozen=True)
class Problem:
    p: int
    n: int
    multipliers: tuple[int, ...]
    allowed: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        parameters(self.p, len(self.multipliers), self.n)
        if self.p > 65521:
            raise ValueError("bounded int64 reference, not a large-field theorem limit")
        canonical(self.multipliers, self.M, self.p)
        if 0 in self.multipliers or len(self.allowed) != self.M:
            raise ValueError("nonzero multipliers and one explicit set per pair required")
        for row in self.allowed:
            canonical(row, (self.p-1)//2, self.p)
            if len(set(row)) != len(row):
                raise ValueError("halfset symbols must be distinct")

    @property
    def M(self):
        return len(self.multipliers)

    @property
    def K(self):
        return self.n//2

    def table(self):
        result = np.zeros((self.M, self.p), dtype=bool)
        for i, row in enumerate(self.allowed):
            result[i, list(row)] = True
        return result

    def values(self, coefficients):
        c = canonical(coefficients, self.n, self.p)
        return (np.array([evaluate(c, a, self.p) for a in range(1, self.M+1)], dtype=np.int64),
                np.array([evaluate(c, self.p-a, self.p) for a in range(1, self.M+1)], dtype=np.int64))

    def residuals(self, x, y):
        return (y+np.asarray(self.multipliers)*(x*x % self.p)) % self.p

    def independent_score(self, coefficients):
        c = canonical(coefficients, self.n, self.p)
        return sum((evaluate(c, self.p-a, self.p)
                    + b*evaluate(c, a, self.p)**2) % self.p in allowed
                   for a, (b, allowed) in enumerate(zip(self.multipliers, self.allowed), 1))


def information_map(problem, positions):
    """Exact paired Lagrange maps: dx_i=A_ij dx_j+B_ij dy_j."""
    I = tuple(positions)
    if len(I) != problem.K or len(set(I)) != len(I) or any(type(i) is not int or not 0 <= i < problem.M for i in I):
        raise ValueError("exactly K distinct public information pairs required")
    p, M, K = problem.p, problem.M, problem.K
    nodes = [(i+1)**2 % p for i in I]
    weights = []
    for z in nodes:
        denominator = 1
        for other in nodes:
            if z != other:
                denominator = denominator*(z-other) % p
        weights.append(pow(denominator, -1, p))
    L = np.zeros((M, K), dtype=np.int64)
    indexed = {i: j for j, i in enumerate(I)}
    for i in range(M):
        if i in indexed:
            L[i, indexed[i]] = 1
            continue
        z = (i+1)**2 % p
        numerator = 1
        for node in nodes:
            numerator = numerator*(z-node) % p
        for j, node in enumerate(nodes):
            L[i, j] = numerator*pow(z-node, -1, p)*weights[j] % p
    ratio = np.array([[(i+1)*pow(j+1, -1, p) % p for j in I] for i in range(M)], dtype=np.int64)
    inv2 = pow(2, -1, p)
    A = (L*((1+ratio)*inv2 % p)) % p
    B = (L*((1-ratio)*inv2 % p)) % p
    return A, B


def coefficients_from_information(problem, positions, x, y):
    p = problem.p
    nodes = [(i+1)**2 % p for i in positions]
    E = [(int(x[i])+int(y[i]))*pow(2, -1, p) % p for i in positions]
    O = [(int(x[i])-int(y[i]))*pow(2*(i+1), -1, p) % p for i in positions]
    even, _ = interpolate(p, nodes, E)
    odd, _ = interpolate(p, nodes, O)
    result = []
    for j in range(problem.K):
        result.extend((int(even[j]), int(odd[j])))
    return tuple(result)


def random_information_witness(problem, positions, seed):
    """Sample a uniform feasible starting polynomial on information set I."""
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative integer seed required")
    I = tuple(positions)
    information_map(problem, I)
    rng = random.Random(seed)
    x = np.zeros(problem.M, dtype=np.int64)
    y = np.zeros(problem.M, dtype=np.int64)
    for anchor in I:
        xj = rng.randrange(problem.p)
        rj = rng.choice(problem.allowed[anchor])
        x[anchor] = xj
        y[anchor] = (rj - problem.multipliers[anchor]*xj*xj) % problem.p
    c = coefficients_from_information(problem, I, x, y)
    vx, vy = problem.values(c)
    vr = problem.residuals(vx, vy)
    if not all(int(vr[i]) in problem.allowed[i] for i in I):
        raise ArithmeticError("sampled information witness failed its own information set")
    return c


def residual_polynomial(problem, x, y, A, B, anchor, kind):
    """All native residuals as degree <=4 polynomials in the intrinsic delta."""
    p = problem.p
    b = np.asarray(problem.multipliers, dtype=np.int64)
    if kind == "root":
        bj, xj = problem.multipliers[anchor], int(x[anchor])
        l1, l2 = (A-2*bj*xj*B) % p, (-bj*B) % p
        r1, r2 = (B-2*bj*xj*A) % p, (-bj*A) % p
        c0 = problem.residuals(x, y)
        c1 = (r1+2*b*x*l1) % p
        c2 = (r2+b*((l1*l1+2*x*l2) % p)) % p
        c3 = (2*b*(l1*l2 % p)) % p
        c4 = (b*(l2*l2 % p)) % p
        return np.stack((c0, c1, c2, c3, c4))
    if kind == "residual":
        return np.stack((problem.residuals(x, y), (A+2*b*x*B) % p, (b*(B*B % p)) % p))
    raise ValueError("root or allowed-residual intrinsic coordinate required")


def evaluate_residual_polynomial(coefficients, deltas, p):
    result = np.zeros((len(deltas), coefficients.shape[1]), dtype=np.int64)
    for row in reversed(coefficients):
        result = (result*np.asarray(deltas)[:, None]+row) % p
    return result


def intrinsic_displacement(problem, x, y, anchor, kind, symbol):
    p = problem.p
    if type(symbol) is not int or not 0 <= symbol < p:
        raise ValueError("canonical new information symbol required")
    if kind == "root":
        dx = (symbol-int(x[anchor])) % p
        dy = -problem.multipliers[anchor]*(symbol*symbol-int(x[anchor])**2) % p
        return dx, dy
    if kind == "residual":
        if symbol not in problem.allowed[anchor]:
            raise ValueError("new residual must remain in its actual halfset")
        return 0, (symbol-int(problem.residuals(x, y)[anchor])) % p
    raise ValueError("unknown intrinsic coordinate")


def move(problem, x, y, A, B, anchor, kind, symbol):
    dx, dy = intrinsic_displacement(problem, x, y, anchor, kind, symbol)
    return (x+A*dx+B*dy) % problem.p, (y+B*dx+A*dy) % problem.p


def block_move(problem, x, y, A, B, j1, j2, anchor1, anchor2, kind1, symbol1, kind2, symbol2):
    """Exact 2-coordinate block move preserving all K information predicates."""
    if j1 == j2 or anchor1 == anchor2:
        raise ValueError("two distinct information coordinates required for a block move")
    dx1, dy1 = intrinsic_displacement(problem, x, y, anchor1, kind1, symbol1)
    dx2, dy2 = intrinsic_displacement(problem, x, y, anchor2, kind2, symbol2)
    p = problem.p
    nx = (x + A[:, j1]*dx1 + B[:, j1]*dy1 + A[:, j2]*dx2 + B[:, j2]*dy2) % p
    ny = (y + B[:, j1]*dx1 + A[:, j1]*dy1 + B[:, j2]*dx2 + A[:, j2]*dy2) % p
    return nx, ny


def greedy_search(problem, coefficients, *, positions=None, max_sweeps=2, batch=128):
    """Full-coordinate scans; no incomplete scan updates or uncounted restarts."""
    if type(max_sweeps) is not int or max_sweeps < 1 or type(batch) is not int or batch < 1:
        raise ValueError("positive complete-sweep and batch budgets required")
    I = tuple(range(problem.K)) if positions is None else tuple(positions)
    start = time.perf_counter()
    A, B = information_map(problem, I)
    x, y = problem.values(coefficients)
    table = problem.table()
    index = np.arange(problem.M)
    current = int(table[index, problem.residuals(x, y)].sum())
    if not all(table[i, problem.residuals(x, y)[i]] for i in I):
        raise ValueError("starting polynomial must already pass every information pair")
    initial = current
    setup_seconds = time.perf_counter()-start
    trace, proposed, improvements = [], 0, 0
    stopped = "SWEEP_BUDGET_EXHAUSTED"
    for sweep in range(max_sweeps):
        changed = False
        for j, anchor in enumerate(I):
            for kind in ("root", "residual"):
                symbols = np.arange(problem.p, dtype=np.int64) if kind == "root" else np.array(sorted(problem.allowed[anchor]), dtype=np.int64)
                old_symbol = int(x[anchor]) if kind == "root" else int(problem.residuals(x, y)[anchor])
                curve = residual_polynomial(problem, x, y, A[:, j], B[:, j], anchor, kind)
                before, best, chosen = current, current, old_symbol
                for offset in range(0, len(symbols), batch):
                    part = symbols[offset:offset+batch]
                    residual = evaluate_residual_polynomial(curve, (part-old_symbol) % problem.p, problem.p)
                    scores = table[index[None, :], residual].sum(axis=1)
                    proposed += len(part)
                    location = int(np.argmax(scores))
                    if int(scores[location]) > best:
                        best, chosen = int(scores[location]), int(part[location])
                if best > current:
                    x, y = move(problem, x, y, A[:, j], B[:, j], anchor, kind, chosen)
                    actual = int(table[index, problem.residuals(x, y)].sum())
                    if actual != best or not all(table[i, problem.residuals(x, y)[i]] for i in I):
                        raise ArithmeticError("intrinsic move lost feasibility or its reported score")
                    current, changed = best, True
                    improvements += 1
                trace.append({"sweep": sweep, "information_pair": anchor, "kind": kind,
                              "proposals": len(symbols), "before": before, "after": current,
                              "chosen_symbol": chosen, "strict_improvement": current > before})
        if not changed:
            stopped = "COMPLETE_INTRINSIC_COORDINATE_FIXED_POINT"
            break
    result = coefficients_from_information(problem, I, x, y)
    check_x, check_y = problem.values(result)
    if (not np.array_equal(x, check_x) or not np.array_equal(y, check_y)
            or problem.independent_score(result) != current):
        raise ArithmeticError("final original-polynomial reconstruction failed")
    return {"status": stopped, "initial_score": initial, "final_score": current,
            "coefficients": list(result), "information_pairs": list(I),
            "trace": trace, "strict_improvements": improvements,
            "work": {"candidate_evaluations": proposed, "predicate_lookups": proposed*problem.M,
                     "complete_coordinate_scans": len(trace), "sweeps_completed": sweep+1,
                     "setup_seconds": setup_seconds, "total_seconds": time.perf_counter()-start,
                     "restarts": 0, "hidden_oracle_or_lift": False},
            "original_Horner_and_full_value_replay": True,
            "global_optimum_or_classical_lower_bound_claimed": False,
            "full_classical_portfolio_complete": False}


def block_search(problem, coefficients, *, positions=None, proposals=2048, seed=8201):
    """Joint 2-coordinate block-move search with complete proposal accounting."""
    if type(proposals) is not int or proposals < 1 or type(seed) is not int or seed < 0:
        raise ValueError("positive block-proposal budget and nonnegative seed required")
    I = tuple(range(problem.K)) if positions is None else tuple(positions)
    if problem.K < 2:
        raise ValueError("at least two information pairs required for block moves")
    start = time.perf_counter()
    A, B = information_map(problem, I)
    x, y = problem.values(coefficients)
    table = problem.table()
    index = np.arange(problem.M)
    r = problem.residuals(x, y)
    if not all(table[i, r[i]] for i in I):
        raise ValueError("starting polynomial must pass every information pair")
    initial = current = int(table[index, r].sum())
    rng = random.Random(seed)
    improvements = 0
    accepted_moves = []
    for step in range(proposals):
        j1, j2 = rng.sample(range(problem.K), 2)
        anchor1, anchor2 = I[j1], I[j2]
        kind1 = "root" if rng.randrange(2) == 0 else "residual"
        kind2 = "root" if rng.randrange(2) == 0 else "residual"
        sym1 = rng.randrange(problem.p) if kind1 == "root" else rng.choice(problem.allowed[anchor1])
        sym2 = rng.randrange(problem.p) if kind2 == "root" else rng.choice(problem.allowed[anchor2])
        nx, ny = block_move(problem, x, y, A, B, j1, j2, anchor1, anchor2, kind1, sym1, kind2, sym2)
        nr = problem.residuals(nx, ny)
        score = int(table[index, nr].sum())
        if score > current:
            if not all(table[i, nr[i]] for i in I):
                raise ArithmeticError("block move violated an information constraint")
            x, y, current = nx, ny, score
            improvements += 1
            accepted_moves.append({"step": step, "anchors": [anchor1, anchor2],
                                   "kinds": [kind1, kind2], "symbols": [sym1, sym2],
                                   "new_score": score})
    result = coefficients_from_information(problem, I, x, y)
    if problem.independent_score(result) != current:
        raise ArithmeticError("block-search polynomial reconstruction failed")
    return {"method": "two_coordinate_block_search", "seed": seed,
            "information_pairs": list(I), "initial_score": initial, "final_score": current,
            "strict_improvements": improvements, "accepted_moves": accepted_moves,
            "coefficients": list(result),
            "work": {"candidate_evaluations": proposals,
                     "predicate_lookups": proposals*problem.M,
                     "total_seconds": time.perf_counter()-start},
            "original_Horner_and_full_value_replay": True}


def annealing_search(problem, coefficients, *, positions=None, steps=1024,
                     t_start=1.2, t_end=0.15, seed=8301):
    """Metropolis intrinsic search over single and 2-coordinate moves."""
    if type(steps) is not int or steps < 1 or type(seed) is not int or seed < 0:
        raise ValueError("positive step budget and nonnegative seed required")
    if t_start <= 0 or t_end <= 0 or t_end > t_start:
        raise ValueError("positive cooling schedule t_start >= t_end > 0 required")
    I = tuple(range(problem.K)) if positions is None else tuple(positions)
    start = time.perf_counter()
    A, B = information_map(problem, I)
    x, y = problem.values(coefficients)
    table = problem.table()
    index = np.arange(problem.M)
    r = problem.residuals(x, y)
    if not all(table[i, r[i]] for i in I):
        raise ValueError("starting polynomial must pass every information pair")
    initial = current = best = int(table[index, r].sum())
    best_x, best_y = x.copy(), y.copy()
    rng = random.Random(seed)
    accepted_steps = 0
    downhill_accepted = 0
    for step in range(steps):
        frac = step/max(1, steps-1)
        temp = t_start*((t_end/t_start)**frac)
        if problem.K >= 2 and rng.randrange(4) == 0:
            j1, j2 = rng.sample(range(problem.K), 2)
            a1, a2 = I[j1], I[j2]
            k1 = "root" if rng.randrange(2) == 0 else "residual"
            k2 = "root" if rng.randrange(2) == 0 else "residual"
            s1 = rng.randrange(problem.p) if k1 == "root" else rng.choice(problem.allowed[a1])
            s2 = rng.randrange(problem.p) if k2 == "root" else rng.choice(problem.allowed[a2])
            nx, ny = block_move(problem, x, y, A, B, j1, j2, a1, a2, k1, s1, k2, s2)
        else:
            j = rng.randrange(problem.K)
            anchor = I[j]
            kind = "root" if rng.randrange(2) == 0 else "residual"
            sym = rng.randrange(problem.p) if kind == "root" else rng.choice(problem.allowed[anchor])
            nx, ny = move(problem, x, y, A[:, j], B[:, j], anchor, kind, sym)
        nr = problem.residuals(nx, ny)
        score = int(table[index, nr].sum())
        delta = score - current
        if delta >= 0 or rng.random() < exp(delta/temp):
            x, y, current = nx, ny, score
            accepted_steps += 1
            if delta < 0:
                downhill_accepted += 1
            if score > best:
                if not all(table[i, nr[i]] for i in I):
                    raise ArithmeticError("annealing state violated an information constraint")
                best = score
                best_x, best_y = nx.copy(), ny.copy()
    result = coefficients_from_information(problem, I, best_x, best_y)
    if problem.independent_score(result) != best:
        raise ArithmeticError("annealing best-polynomial reconstruction failed")
    return {"method": "intrinsic_simulated_annealing", "seed": seed,
            "information_pairs": list(I), "initial_score": initial,
            "final_current_score": current, "best_score": best,
            "accepted_steps": accepted_steps, "downhill_accepted_steps": downhill_accepted,
            "temperature_schedule": [t_start, t_end],
            "coefficients": list(result),
            "work": {"candidate_evaluations": steps,
                     "predicate_lookups": steps*problem.M,
                     "total_seconds": time.perf_counter()-start},
            "original_Horner_and_full_value_replay": True}


def portfolio_campaign(problem, fixed_point_coefficients, *, seed=8101, batch=512):
    """Matched classical portfolio: re-anchoring escape, multi-I starts, block moves, and annealing.

    Retains all runs (including non-improving runs and weaker starts) with complete budgets.
    """
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative portfolio seed required")
    start = time.perf_counter()
    table = problem.table()
    x0, y0 = problem.values(fixed_point_coefficients)
    r0 = problem.residuals(x0, y0)
    passing0 = [i for i in range(problem.M) if table[i, r0[i]]]
    rng = random.Random(seed)

    # 1. Fixed-point escape by pivoting to a new information set I_reanchored <= passing(c_632)
    I_reanchored = tuple(sorted(rng.sample(passing0, problem.K)))
    reanchored = greedy_search(problem, fixed_point_coefficients,
                               positions=I_reanchored, max_sweeps=1, batch=batch)
    escaped_coefficients = tuple(reanchored["coefficients"])

    # 2. Independent information-set start (freshly sampled feasible witness on a distinct I_fresh)
    I_fresh = tuple(sorted(rng.sample(range(problem.M), problem.K)))
    fresh_start = random_information_witness(problem, I_fresh, seed+17)
    fresh_greedy = greedy_search(problem, fresh_start,
                                 positions=I_fresh, max_sweeps=1, batch=batch)

    # 3. Joint 2-coordinate block-move search from the re-anchored witness
    block_run = block_search(problem, escaped_coefficients,
                             positions=I_reanchored, proposals=2048, seed=seed+31)

    # 4. Simulated annealing search from the block-search witness
    anneal_run = annealing_search(problem, block_run["coefficients"],
                                  positions=I_reanchored, steps=1024, seed=seed+47)

    runs = [
        {"run_label": "reanchored_information_set_escape",
         "initial_score": reanchored["initial_score"],
         "final_score": reanchored["final_score"],
         "information_pairs": reanchored["information_pairs"],
         "strict_improvements": reanchored["strict_improvements"],
         "work": reanchored["work"],
         "coefficients": reanchored["coefficients"]},
        {"run_label": "independent_information_set_restart",
         "initial_score": fresh_greedy["initial_score"],
         "final_score": fresh_greedy["final_score"],
         "information_pairs": fresh_greedy["information_pairs"],
         "strict_improvements": fresh_greedy["strict_improvements"],
         "work": fresh_greedy["work"],
         "coefficients": fresh_greedy["coefficients"]},
        {"run_label": "two_coordinate_block_move_search",
         "initial_score": block_run["initial_score"],
         "final_score": block_run["final_score"],
         "information_pairs": block_run["information_pairs"],
         "strict_improvements": block_run["strict_improvements"],
         "work": block_run["work"],
         "coefficients": block_run["coefficients"]},
        {"run_label": "intrinsic_simulated_annealing",
         "initial_score": anneal_run["initial_score"],
         "final_score": anneal_run["best_score"],
         "information_pairs": anneal_run["information_pairs"],
         "accepted_steps": anneal_run["accepted_steps"],
         "downhill_accepted_steps": anneal_run["downhill_accepted_steps"],
         "work": anneal_run["work"],
         "coefficients": anneal_run["coefficients"]},
    ]
    best_run = max(runs, key=lambda row: row["final_score"])
    best_coeffs = tuple(best_run["coefficients"])
    if problem.independent_score(best_coeffs) != best_run["final_score"]:
        raise ArithmeticError("portfolio best witness failed independent Horner replay")
    total_candidates = sum(row["work"]["candidate_evaluations"] for row in runs)
    total_lookups = sum(row["work"]["predicate_lookups"] for row in runs)
    return {
        "seed": seed,
        "starting_fixed_point_score": int(problem.independent_score(fixed_point_coefficients)),
        "best_portfolio_score": best_run["final_score"],
        "best_run_label": best_run["run_label"],
        "best_coefficients": list(best_coeffs),
        "escaped_initial_single_coordinate_fixed_point": (
            best_run["final_score"] > int(problem.independent_score(fixed_point_coefficients))
        ),
        "runs": runs,
        "total_work": {
            "portfolio_runs": len(runs),
            "candidate_evaluations": total_candidates,
            "predicate_lookups": total_lookups,
            "total_seconds": time.perf_counter()-start,
        },
        "all_runs_and_nonimproving_trajectories_retained": True,
        "original_Horner_and_full_value_replay": True,
        "full_classical_portfolio_complete": False,
    }


def uniform_component_bound(p, M, n, pins=None):
    """Uniform target law conditioned on passing predicates, NOT adaptive search."""
    parameters(p, M, n)
    K = n//2
    pins = K if pins is None else pins
    if type(pins) is not int or not 0 <= pins <= K:
        raise ValueError("at most one complete information set of pinned pairs")
    rho = Q(p-1, 2*p)
    energy = Q(p*p-1, p**K) if pins == K else Q(0)
    tv = min(Q(1), sqrt_interval(energy)[1]/2)
    mean = min(Q(1), Q(pins, M)+Q(M-pins, M)*min(Q(1), rho+tv))
    return {"p": p, "M": M, "n": n, "pins": pins, "rho": str(rho),
            "unforced_pair_chi_square_upper_exact": str(energy),
            "unforced_pair_TV_upper_exact": str(tv),
            "uniform_component_mean_upper_exact": str(mean),
            "uniform_conditioned_polynomial_count_decimal": str((p*((p-1)//2))**pins*p**(n-2*pins)),
            "scope": "uniform original-code law conditioned on at most K specified pair passes; positive mixtures only",
            "input_sets_may_be_fixed_adversarial": True,
            "adaptive_within_component_search_covered": False,
            "full_unforced_joint_distribution_identified": False}


def conditional_control():
    """All original coefficient vectors; no sampler approximation in the control."""
    problem = Problem(7, 4, (1, 3, 5), ((0, 1, 2), (1, 2, 4), (2, 3, 6)))
    records = []
    for pins in (1, 2):
        counts = np.zeros((7, 7), dtype=np.int64)
        accepted = 0
        total_score = 0
        for c in product(range(7), repeat=4):
            x, y = problem.values(c)
            r = problem.residuals(x, y)
            if all(int(r[i]) in problem.allowed[i] for i in range(pins)):
                accepted += 1
                total_score += sum(int(v) in row for v, row in zip(r, problem.allowed))
                counts[x[-1], y[-1]] += 1
        tv = sum((abs(Q(int(v), accepted)-Q(1, 49)) for v in counts.flat), Q(0))/2
        energy = sum((49*(Q(int(v), accepted)-Q(1, 49))**2 for v in counts.flat), Q(0))
        bound = uniform_component_bound(7, 3, 4, pins)
        if tv > Q(bound["unforced_pair_TV_upper_exact"]) or energy > Q(bound["unforced_pair_chi_square_upper_exact"]):
            raise ArithmeticError("conditional Fourier bound failed")
        records.append({"pins": pins, "accepted_polynomials": accepted,
                        "pair_counts": counts.tolist(), "pair_TV_exact": str(tv),
                        "pair_chi_square_exact": str(energy),
                        "mean_fraction_exact": str(Q(total_score, 3*accepted)), "bound": bound})
    return {"rows": records, "calibration_only": True}


def run_audit(reference, max_sweeps):
    chain, allowed, provenance = load_reference(reference)
    quantum = json.loads(QUANTUM_REPORT.read_text())
    certificate = quantum["certificate"]
    p, M, n = certificate["p"], certificate["M"], certificate["n"]
    if (p, M, n) != (2053, 1026, 204):
        raise ValueError("changed saved paired target; reconsider the experiment contract")
    if quantum["native"]["parent_provenance"]["arrays_sha256"] != provenance["arrays_sha256"]:
        raise ValueError("paired and classical artifacts refer to different source tables")
    problem = Problem(p, n, tuple(chain.multipliers[:M]), tuple(tuple(sorted(row)) for row in allowed[:M]))
    initial = quantum["native"]["one_information_set_comparator"]["coefficients"]
    initial_score = problem.independent_score(initial)
    if initial_score != quantum["native"]["one_information_set_comparator"]["passing_tests"]:
        raise ArithmeticError("saved starting polynomial does not replay")
    bound = uniform_component_bound(p, M, n)
    gap = max(Q(0), Q(certificate["conditional_mean_lower_exact"])-Q(bound["uniform_component_mean_upper_exact"]))
    native_search = greedy_search(problem, initial, max_sweeps=max_sweeps)
    portfolio = portfolio_campaign(problem, native_search["coefficients"])
    result = {"schema": "paired-residual-classical-v2", "status": "LOCAL_DERIVATION_REVIEW_PENDING",
              "parent_provenance": provenance, "paired_problem_report_sha256": hashlib.sha256(QUANTUM_REPORT.read_bytes()).hexdigest(),
              "same_paired_instance_and_starting_polynomial": True,
              "uniform_component_bound": bound,
              "conditional_on_paired_quantum_derivation_mixture_TV_gap_lower": str(gap),
              "conditional_control": conditional_control(),
              "native_search": native_search,
              "portfolio_campaign": portfolio,
              "quantum_advantage_or_general_classical_hardness_established": False}
    result["dependencies"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), ROOT/"theorems/paired_residual_decoder.py",
                     ROOT/"theorems/prime_character_opi.py",
                     ROOT/"theorems/prime_character_finite_readout.py",
                     ROOT/"theorems/nonlinear_residual_lift.py")}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--max-sweeps", type=int, default=2)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_audit(args.reference, args.max_sweeps)
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
    native = result["native_search"]
    portfolio = result["portfolio_campaign"]
    print(json.dumps({"status": native["status"], "initial_score": native["initial_score"],
                      "final_score": native["final_score"],
                      "best_portfolio_score": portfolio["best_portfolio_score"],
                      "escaped_fixed_point": portfolio["escaped_initial_single_coordinate_fixed_point"],
                      "work": native["work"],
                      "portfolio_work": portfolio["total_work"],
                      "uniform_component_mean_upper": float(Q(result["uniform_component_bound"]["uniform_component_mean_upper_exact"])),
                      "full_classical_portfolio_complete": False}, indent=2))


if __name__ == "__main__":
    main()
