"""Macro contract (M) on canonical words, extended beyond p <= 13.
Report: ../2026-11-05-rees-receiver-general-gh.md, Section 2.6.

For every odd prime p in the stated range and EVERY coefficient kappa in 1..p-1,
the gate lists add_scaled_ops(p, t, a, kappa) and add_product_ops(p, t, a, b, kappa)
of theorems/rees_circuit_arith.py (imported read-only), and the aliased squaring
add_product_ops(p, t, a, a, kappa), are run (bit-sliced, exact) on ALL canonical
operand words with the 3b+5 ancillas at 0, and must give
  t <- t + kappa*a(*b) mod p, operands restored, ancillas 0.
Statically, no operand wire is ever the target of a gate (the (A4) part used by
deferred measurement). AI-written, pending human review.
"""
from __future__ import annotations

import argparse
import json
import sys
import time

REPO = "/Users/jaspersands/Developer/qsearch"
sys.path.insert(0, REPO)

import numpy as np  # noqa: E402

from theorems.rees_circuit_arith import Anc, add_product_ops, add_scaled_ops, anc_size  # noqa: E402
from theorems.rees_coherent_sde import BitSim  # noqa: E402


def is_prime(n):
    return n > 1 and all(n % q for q in range(2, int(n**0.5)+1))


def targets(g):
    name, q = g
    return set(q) if name == "swap" else {q[-1]}


def run(p, kind):
    b = max(1, (p-1).bit_length())
    if kind == "scaled":
        t, a = list(range(b)), list(range(b, 2*b))
        ops_args, n_ops, base = (t, a), 2, 2*b
    elif kind == "product":
        t, a, bb = list(range(b)), list(range(b, 2*b)), list(range(2*b, 3*b))
        ops_args, n_ops, base = (t, a, bb), 3, 3*b
    else:                                   # aliased squaring
        t, a = list(range(b)), list(range(b, 2*b))
        ops_args, n_ops, base = (t, a, a), 2, 2*b
    nw = base+anc_size(b)
    A = Anc(list(range(base, nw)), b)
    N = p**n_ops
    idx = np.arange(N, dtype=np.int64)
    vals = [(idx // p**i) % p for i in range(n_ops)]
    ok = {"value": True, "operands_restored": True, "ancillas_zero": True, "operands_never_targeted": True}
    operand_wires = set(ops_args[1]) | (set(ops_args[2]) if kind == "product" else set())
    for coeff in range(1, p):
        ops = (add_scaled_ops(p, t, a, coeff, A) if kind == "scaled"
               else add_product_ops(p, *ops_args, coeff, A))
        gates = list(ops)
        tg = set()
        for g in gates:
            tg |= targets(g)
        ok["operands_never_targeted"] &= not (tg & operand_wires)
        sim = BitSim(nw, N)
        regs = [t, a] + ([bb] if kind == "product" else [])
        for r, v in zip(regs, vals):
            sim.load(r, v)
        sim.run(gates)
        if kind == "scaled":
            want = (vals[0]+coeff*vals[1]) % p
        elif kind == "product":
            want = (vals[0]+coeff*vals[1]*vals[2]) % p
        else:
            want = (vals[0]+coeff*vals[1]*vals[1]) % p
        ok["value"] &= bool(np.array_equal(sim.read(t), want))
        ok["operands_restored"] &= all(np.array_equal(sim.read(r), v) for r, v in zip(regs[1:], vals[1:]))
        ok["ancillas_zero"] &= not any(sim.wire_nonzero(w) for w in range(base, nw))
    return {"p": p, "kind": kind, "coefficients": p-1, "inputs_per_coefficient": int(N), **ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pmax", type=int, default=127)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    t0 = time.time()
    rows = []
    for p in range(17, args.pmax+1):
        if not is_prime(p):
            continue
        for kind in ("scaled", "product", "square"):
            r = run(p, kind)
            rows.append(r)
            print(json.dumps(r), flush=True)
        with open(args.out, "w") as f:
            json.dump({"rows": rows, "all_ok": all(all(r[k] for k in ("value", "operands_restored", "ancillas_zero",
                                                                         "operands_never_targeted")) for r in rows),
                       "seconds": round(time.time()-t0, 1)}, f, indent=1)


if __name__ == "__main__":
    main()
