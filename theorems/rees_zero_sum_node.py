"""The zero-sum node at the grade kappa_d = p - 1 of the Rees Schedule 3 forest.

At a grade d with kappa_d = gcd(d, p-1) = p-1 (inside the paper's range d <= c < p this forces
d = p-1 and p = c+1), every nonzero d-th power in F_p equals 1, so the scalar diagonal equation

    sum_i s_i^d lambda_i = 0,   s != 0                                   (sde-target)

holds exactly when T = supp(s) is a nonempty zero-sum subset of the bank, and then
s = 1_T is a witness as well. This module provides

* the node's two classical searches (exhaustive over the 2^M - 1 nonempty subsets in a fixed
  public order, and the reachable-sum dynamic programme of cost M * min(2^M, p^a));
* the exact witness check of (F5);
* the arities: the second-moment arity (randomized node, bank event <= tau) and the
  Chevalley-Warning / Davenport arity g(p-1)+1 (deterministic node, never aborts);
* exact probabilities that an i.i.d. uniform bank on F_p^a has no nonempty zero-sum subset,
  against the second-moment bound (p^a - 1)/(2^M - 1);
* the budget of Theorem thm:free-coordinate(iii) at p = c+1 with the Schedule 1 grade replaced
  by either zero-sum node (reusing theorems/rees_fcs_budget.py read-only).

All arithmetic is exact (integers, Fractions); log2 only for printing. Finite computations
test displayed inequalities and small cases, never the theorem.

Run:  /opt/anaconda3/bin/python -m theorems.rees_zero_sum_node [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from theorems import rees_fcs_budget as fb

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "research" / "audits" / "reviews" / "2026-11-04-rees-zero-sum-node" / "zero_sum_budget.json"


# ----------------------------------------------------------------------------- the node

def is_witness(labels, s, p: int, d: int) -> bool:
    """Exact check of (F5): s != 0 and sum_i s_i^d lambda_i = 0 over F_p."""
    if len(s) != len(labels) or not any(x % p for x in s):
        return False
    g = len(labels[0]) if labels else 0
    acc = [0] * g
    for lam, si in zip(labels, s):
        w = pow(si % p, d, p)
        if w:
            for j in range(g):
                acc[j] = (acc[j] + w * lam[j]) % p
    return not any(acc)


def exhaustive_zero_sum(labels, p: int):
    """First nonempty T (in increasing binary-mask order) with sum_T lambda = 0.

    Returns (s, examined): s = 1_T as a 0/1 tuple, or None if no zero-sum subset exists,
    and the number of subsets examined. Cost: 2^M - 1 subsets, each sum updated from the
    previous mask by one vector addition along a Gray code would also do; here the masks are
    taken in increasing order and the sum is recomputed incrementally from mask & (mask-1)."""
    M = len(labels)
    if M == 0:
        return None, 0
    g = len(labels[0])
    sums = [None] * (1 << M)
    sums[0] = (0,) * g
    for mask in range(1, 1 << M):
        low = (mask & -mask).bit_length() - 1
        prev = sums[mask & (mask - 1)]
        lam = labels[low]
        cur = tuple((a + b) % p for a, b in zip(prev, lam))
        sums[mask] = cur
        if not any(cur):
            return tuple((mask >> i) & 1 for i in range(M)), mask
    return None, (1 << M) - 1


def dp_zero_sum(labels, p: int):
    """Reachable-sum dynamic programme: R_j = nonempty subset sums of lambda_1..lambda_j,
    one representative subset per value. Exact: 0 in R_M iff a zero-sum subset exists.

    Returns (s, max_reachable): s = 1_T or None, and max_j |R_j| (<= min(2^M - 1, p^a))."""
    M = len(labels)
    parent = {}          # value -> (previous value or None, index added)
    biggest = 0
    for i, lam in enumerate(labels):
        lam = tuple(x % p for x in lam)
        new = {}
        if lam not in parent:
            new[lam] = (None, i)
        for v in list(parent):
            w = tuple((a + b) % p for a, b in zip(v, lam))
            if w not in parent and w not in new:
                new[w] = (v, i)
        parent.update(new)
        biggest = max(biggest, len(parent))
        zero = tuple(0 for _ in lam)
        if zero in parent:
            s = [0] * M
            v = zero
            while v is not None:
                prev, j = parent[v]
                s[j] = 1
                v = prev
            return tuple(s), biggest
    return None, biggest


# ----------------------------------------------------------------------------- probabilities

def second_moment_bound(p: int, a: int, M: int) -> F:
    """Pr[no nonempty zero-sum subset] <= Var X / (E X)^2 = (p^a - 1)/(2^M - 1), where X counts
    zero-sum nonempty subsets of M i.i.d. uniform labels on a dimension-a space."""
    return F(p ** a - 1, 2 ** M - 1)


def count_moments(p: int, a: int, M: int):
    """Exact E[X] and E[X^2] by enumeration of all p^(aM) banks (tiny cases only)."""
    V = list(product(range(p), repeat=a))
    n = 0
    s1 = 0
    s2 = 0
    none = 0
    for bank in product(V, repeat=M):
        X = 0
        for mask in range(1, 1 << M):
            acc = [0] * a
            for i in range(M):
                if (mask >> i) & 1:
                    for j in range(a):
                        acc[j] += bank[i][j]
            if all(x % p == 0 for x in acc):
                X += 1
        n += 1
        s1 += X
        s2 += X * X
        none += X == 0
    return F(s1, n), F(s2, n), F(none, n)


def predicted_moments(p: int, a: int, M: int):
    N = 2 ** M - 1
    pi = F(1, p ** a)
    return N * pi, N * pi * (1 - pi) + (N * pi) ** 2


def exact_zero_sum_free_probability(p: int, a: int, M: int, *, max_states: int = 3_000_000) -> F:
    """Pr[M i.i.d. uniform elements of F_p^a have no nonempty zero-sum subset], exactly.

    Dynamic programme over the set N of nonempty subset sums (a bitmask over the p^a group
    elements); a state dies when 0 enters N. By GL(a,p)-invariance of the uniform law and of
    zero-sum-freeness, the first label may be fixed to e_1 (if nonzero; a zero label is itself a
    zero-sum subset), contributing the factor (p^a - 1)/p^a."""
    q = p ** a
    if M == 0:
        return F(1)
    if a == 0:
        return F(0)
    elems = list(product(range(p), repeat=a))
    index = {v: i for i, v in enumerate(elems)}
    add = [[index[tuple((x + y) % p for x, y in zip(u, v))] for v in elems] for u in elems]
    zero = index[(0,) * a]
    e1 = index[(1,) + (0,) * (a - 1)]
    states = {1 << e1: 1}
    for _ in range(M - 1):
        nxt = {}
        for N, cnt in states.items():
            members = [i for i in range(q) if (N >> i) & 1]
            for lam in range(q):
                if lam == zero:
                    continue
                newN = N | (1 << lam)
                row = add[lam]
                for i in members:
                    newN |= 1 << row[i]
                if (newN >> zero) & 1:
                    continue
                nxt[newN] = nxt.get(newN, 0) + cnt
        states = nxt
        if len(states) > max_states:
            raise MemoryError(f"state count {len(states)} exceeds {max_states}")
    alive = sum(states.values())
    return F(q - 1, q) * F(alive, q ** (M - 1))


# ----------------------------------------------------------------------------- arities

def zero_sum_arity_explicit(p: int, g: int, tau: F) -> int:
    """M = 1 + (least k >= 0 with 2^k >= p^g / tau) = ceil(g log2 p + log2(1/tau)) + 1 in exact
    form. Then 2^M - 1 >= 2 p^g/tau - 1 >= p^g/tau, so (p^g - 1)/(2^M - 1) < tau."""
    target = F(p ** g) / tau
    k = 0
    while 2 ** k < target:
        k += 1
    return k + 1


def zero_sum_arity_least(p: int, g: int, tau: F) -> int:
    """Least M with (p^g - 1)/(2^M - 1) <= tau."""
    M = 1
    while second_moment_bound(p, g, M) > tau:
        M += 1
    return M


def davenport_arity(p: int, g: int) -> int:
    """g(p-1)+1 columns: a nonempty zero-sum subset always exists (Chevalley-Warning)."""
    return g * (p - 1) + 1


# ----------------------------------------------------------------------------- budget at p = c+1

def filiform_profile(r: int):
    """Filiform algebra of dimension m = r+2 and class c = r+1: g_d = m - d for d >= 2."""
    m = r + 2
    return tuple([m] + [m - d for d in range(2, r + 2)])


def budget_p_c_plus_1(profile, p: int, eps: F = F(1, 3), variant: str = "least", explicit_fcs=False):
    """thm:free-coordinate(iii), rule (R1)-(R4), at a prime with Gamma_0 = {p-1} nonempty, with the
    Gamma_0 grade run by
      variant = "S1"        Schedule 1 at B_d(g_d) (the paper's rule; reproduces B.5),
      variant = "least"     the randomized zero-sum node at the least second-moment arity,
      variant = "explicit"  the randomized zero-sum node at zero_sum_arity_explicit,
      variant = "davenport" the deterministic zero-sum node at g_d(p-1)+1.
    Other grades exactly as theorems.rees_fcs_budget.free_coordinate_iii (which this calls)."""
    base = fb.free_coordinate_iii(p, profile, eps, explicit=explicit_fcs)
    c, S, n = base["c"], base["S"], base["n"]
    g = {d: profile[d - 1] for d in range(1, c + 1)}
    zs = [d for d, gr in base["grades"].items() if gr["cls"] == "0"]
    assert zs == [p - 1], (zs, p)
    d0 = p - 1
    tau = eps / (9 * (c - 1) * S * n[d0])
    if variant == "S1":
        M0 = base["grades"][d0]["M"]
        bank0 = F(0)
    elif variant == "least":
        M0 = zero_sum_arity_least(p, g[d0], tau)
        bank0 = second_moment_bound(p, g[d0], M0)
    elif variant == "explicit":
        M0 = zero_sum_arity_explicit(p, g[d0], tau)
        bank0 = second_moment_bound(p, g[d0], M0)
    elif variant == "davenport":
        M0 = davenport_arity(p, g[d0])
        bank0 = F(0)
    else:
        raise ValueError(variant)
    assert bank0 <= tau
    P = base["P"] // base["grades"][d0]["M"] * M0
    Q = c * S * P
    nodes0 = S * n[d0]
    # Error budget of lem:fc-forest(b) with Gamma_0 added to the bank sum; |Gamma_F u Gamma_0| <= c-1.
    bank = base["bank"] + nodes0 * bank0
    budget_ok = base["rank"] <= eps / 3 and bank <= eps / 9 and base["capped"] <= eps / 9
    # Classical search cost at the zero-sum grade (subset-sum steps, i.e. vector additions).
    if variant == "S1":      # 2^M0 would be astronomically large; not a zero-sum search
        exhaustive_per_node = dp_per_node = None
    else:
        exhaustive_per_node = 2 ** M0 - 1
        dp_per_node = M0 * min(2 ** M0 - 1, p ** g[d0])
    return dict(variant=variant, p=p, c=c, m=profile[0], profile=list(profile), S=S, d0=d0,
                g_d0=g[d0], n_d0=n[d0], tau_d0=tau, M_d0=M0, bank_d0=bank0, P=P, Q=Q,
                log2_Q=math.log2(Q), log2_Gprime=sum(profile[1:2]) * math.log2(p),
                fcs_max_trial_cap=base["max_cap"], fcs_total_trials=base["total"], B=base["B"],
                zs_nodes=nodes0, exhaustive_steps_per_node=exhaustive_per_node,
                dp_steps_per_node=dp_per_node,
                log2_exhaustive_total=math.log2(nodes0 * exhaustive_per_node) if variant != "S1" else None,
                log2_dp_total=math.log2(nodes0 * dp_per_node) if variant != "S1" else None,
                bank_total=bank, budget_ok=budget_ok,
                arities={d: (M0 if d == d0 else gr["M"]) for d, gr in base["grades"].items()},
                schedules={d: ("ZS-" + variant if d == d0 else gr["schedule"]) for d, gr in base["grades"].items()})


CASES = ((3, 5), (5, 7), (9, 11))   # (r, p) with c = r+1, p = c+1


def _jsonable(x):
    if isinstance(x, F):
        return {"num": str(x.numerator), "den": str(x.denominator), "log2": fb.log2_exact(x) if x else None}
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, int) and x.bit_length() > 52:
        return {"int": str(x), "log2": math.log2(x)}
    return x


def build() -> dict:
    rows = []
    for r, p in CASES:
        prof = filiform_profile(r)
        assert len(prof) == r + 1 and p == r + 2
        for variant in ("S1", "least", "explicit", "davenport"):
            rows.append(budget_p_c_plus_1(prof, p, variant=variant))
    return {"source": "theorems/rees_zero_sum_node.py", "eps": "1/3", "rows": _jsonable(rows)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)
    data = build()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    for row in data["rows"]:
        lg = lambda v: v["log2"] if isinstance(v, dict) else math.log2(v) if v else 0
        print(f"r={row['c']-1} c={row['c']} p={row['p']} {row['variant']:>9}: M_c={row['M_d0'] if not isinstance(row['M_d0'], dict) else row['M_d0']['int']}"
              f" log2Q={row['log2_Q']:.1f} log2|G'|={row['log2_Gprime']:.1f}"
              f" bank_c={lg(row['bank_d0']) if row['bank_d0'] else '0'}"
              f" exh={row['log2_exhaustive_total']} dp={row['log2_dp_total']} ok={row['budget_ok']}")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
