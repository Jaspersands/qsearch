"""Exhaustive merge checks at every grade, by an exact reduction.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-05-rees-receiver-sims.md.

Setting: the sparse module-by-module simulation of theorems/rees_circuit_sparse.py
(SparseEngine: source from its gate list or the exact coset density,
instrument exponents read off its gate list, Schur-product merge fed by the
merge gate lists proved by rees_circuit_general.prove_merge). Before this
file the merges were checked on all (label tuple, witness) pairs only where
that set is small (grades 4 and 3 for two n5(F_5) subgroups; at grade 2 the
set has (p^M - 1) |K^perp|^(M-1) elements, up to 3.0e17), and sampled
otherwise.

Reduction (every step but (R) is an exact finite computation):
 (E1) label law: prob(lam) = 1/|K^perp| on K^perp, 0 elsewhere (exact);
 (E2) exponential form: for EVERY lam in K^perp the conditioned branch
      phi_lam has the support of phi_0 and phi_lam(g) = zeta^(e_lam(g)) phi_0(g)
      row by row, with e_lam = sum_j c_j W_j for lam = sum_j c_j b_j over a
      basis b of K^perp (W: support -> F_p^k), and phi_0 constant on its
      support (exact, all lam);
 (E3) for EVERY nonempty set T of nonzero scalars with |T| <= M, the
      zero-label merge with witness values T (each once, and once with the
      first value repeated to arity M) equals rho_(H_(d-1)) exactly, and on
      its support Sigma_T = {g : delta_t(g) in supp phi_0 for all t in T}
      the vectors t^(-d) W(delta_t g) (t in T) coincide.
 (R)  [argued, five lines; its algebraic core is Lean-checked in
      formal/Formal/ReesMergeReduction.lean (merge_product_eq_of_labels,
      zero_product_indicator), round 2] For labels lam_i = sum_j c_ij b_j and a witness s
      (sum_i s_i^d lam_i = 0, s != 0) with value set T = {s_i != 0},
      F(g) = prod_(s_i != 0) phi_lam_i(delta_si g)
           = F_0(g) zeta^(sum_ij c_ij W_j(delta_si g)),
      F_0 = prod phi_0 o delta_si is the zero-label merge (by (E2) phi_0 is
      constant on its support, so multiplicities change only the scale, and
      the support is Sigma_T). By (E3) W_j(delta_si g) = s_i^d tau_j(g) on
      Sigma_T, so the exponent is sum_j tau_j(g) sum_i s_i^d c_ij = 0 by the
      witness equation (b is a basis). Hence F = F_0, and the merge output is
      rho_(H_(d-1)) for every (lam, s).
So (E1)-(E3) cover all (p^M - 1) |K^perp|^(M-1) (label tuple, witness)
pairs at every grade. Independent cross-checks: direct merges on random
witness pairs (and non-witness negative controls), and the direct exhaustive
counts of 2026-11-03-rees-circuit-3 where they exist.

Inputs per grade: the source at the top (from its gate list, or the exact
coset density of exp(h~) when the top group is too large), then the exact
rho_(H_(d-1)), which (E1)-(E3) show is every merge output.
No claim gate is touched: coherent_receiver_implemented stays False.
"""
from __future__ import annotations

import argparse
import json
import random
import resource
import time
from fractions import Fraction
from itertools import combinations, product

import numpy as np

from theorems.rees_circuit_general import (
    Config, all_witnesses, allowed_labels, prove_merge, stage_indices,
)
from theorems.rees_circuit_sparse import SPARSE_STATUS, SparseEngine, SState, n5_instances
from theorems.rees_end_to_end_sim import cyc_canon, filiform5, nullspace, rref, span_elements

STATUS = {**SPARSE_STATUS, "status": "exhaustive_merge_checks_by_exact_reduction_finite_instances",
          "coherent_receiver_implemented": False}


def truth_state(cfg, inst, d):
    idx = np.sort(stage_indices(cfg, inst.log_h, d)).astype(np.int64)
    V = np.zeros((len(idx), cfg.p), dtype=np.int64)
    V[:, 0] = 1
    return SState(d, Fraction(1), idx, V)


def _row_exponents(V0, s0, V1, s1, p):
    """e[r] with s1*V1[r] = zeta^e[r] * s0*V0[r] exactly, or None."""
    lhs = V1*(s1.numerator*s0.denominator)
    e = np.full(len(V0), -1, dtype=np.int64)
    for k in range(p):
        rk = cyc_canon(np.roll(V0, k, axis=1))*(s0.numerator*s1.denominator)
        hit = (rk == lhs).all(axis=1) & (e < 0)
        e[hit] = k
    return None if (e < 0).any() else e


def branch_structure(eng, st, allowed, d):
    """(E1) and (E2). Returns (ok flags, phi_0, W, basis)."""
    p = eng.p
    probs, states = eng.label_law(st)
    law_ok = all(pr == (Fraction(1, len(allowed)) if lam in set(allowed) else 0) for lam, pr in probs.items())
    g = eng.cfg.dims[d-1]
    zero = (0,)*g
    phi0 = states[zero]
    V0 = phi0.V
    const_ok = bool((V0 == V0[0]).all()) and not V0[0, 1:].any()
    basis = [tuple(int(x) for x in b) for b in rref(allowed, p)] if any(any(l) for l in allowed) else []
    k = len(basis)
    same_support = True
    E = {}
    for lam in allowed:
        ph = states[lam]
        if len(ph.idx) != len(phi0.idx) or (ph.idx != phi0.idx).any():
            same_support = False
            E[lam] = None
            continue
        E[lam] = _row_exponents(V0, phi0.scale, ph.V, ph.scale, p)
    expo_ok = same_support and all(v is not None for v in E.values())
    W = np.zeros((len(phi0.idx), k), dtype=np.int64)
    lin_ok = expo_ok
    if expo_ok:
        for j, b in enumerate(basis):
            W[:, j] = E[b]
        B = np.array(basis, dtype=np.int64).reshape(k, g) if k else np.zeros((0, g), dtype=np.int64)
        for lam in allowed:
            if k:
                # coordinates c of lam in the basis (rref basis: solve by least squares mod p via enumeration)
                c = _coords(lam, B, p)
                pred = (W @ np.array(c, dtype=np.int64)) % p
            else:
                pred = np.zeros(len(phi0.idx), dtype=np.int64)
            if not np.array_equal(pred, E[lam] % p):
                lin_ok = False
                break
    flags = {"label_law_uniform_on_K_perp": bool(law_ok), "phi0_constant_on_support": const_ok,
             "branches_share_support": bool(same_support), "branches_are_monomial_twists": bool(expo_ok),
             "twist_exponent_linear_in_label": bool(lin_ok), "K_perp_size": len(allowed), "K_perp_dim": k,
             "branch_support": int(len(phi0.idx)), "labels_checked": len(allowed)}
    return flags, phi0, W, basis


def _coords(lam, B, p):
    """Coordinates of lam in the rref basis B (pivot entries), verified."""
    piv = [int(np.nonzero(r)[0][0]) for r in B]
    c = [int(lam[j]) % p for j in piv]
    if tuple(int(x) for x in (np.array(c, dtype=np.int64) @ B) % p) != tuple(int(x) % p for x in lam):
        raise ArithmeticError("label not in the span of the basis")
    return c


def subset_checks(eng, phi0, W, d, M, target, phase_power=None):
    """(E3) for every nonempty T subset of F_p^*, |T| <= M."""
    cfg, p = eng.cfg, eng.p
    law = cfg.laws[d]
    G0 = law.decode(phi0.idx)
    n_sets = merges = 0
    ok_merge = ok_phase = True
    bad = []
    for r in range(1, min(M, p-1)+1):
        for T in combinations(range(1, p), r):
            n_sets += 1
            variants = [list(T)]
            if len(T) < M:
                variants.append([T[0]]*(M-len(T)+1)+list(T[1:]))
            for sv in variants:
                out = eng.merge([phi0]*len(sv), sv)
                merges += 1
                if not out.equals_indicator(target):
                    ok_merge = False
                    bad.append(("merge", T))
            # support Sigma_T inside G_d and the phase condition
            t1 = T[0]
            inv = np.array(cfg.scales(d, pow(t1, -1, p)), dtype=np.int64)
            gset = (G0*inv[None, :]) % p
            pos = {}
            keep = np.ones(len(gset), dtype=bool)
            for t in T:
                y = law.encode((gset*np.array(cfg.scales(d, t), dtype=np.int64)[None, :]) % p)
                ps = np.minimum(np.searchsorted(phi0.idx, y), len(phi0.idx)-1)
                keep &= phi0.idx[ps] == y
                pos[t] = ps
            if W.shape[1]:
                ref = None
                for t in T:
                    e = d if phase_power is None else phase_power      # test hook (wrong power)
                    tau = (W[pos[t][keep]]*pow(pow(t, e, p), -1, p)) % p
                    if ref is None:
                        ref = tau
                    elif not np.array_equal(ref, tau):
                        ok_phase = False
                        bad.append(("phase", T))
                        break
    return {"value_sets": n_sets, "zero_label_merges": merges, "zero_label_merges_equal_rho": ok_merge,
            "phase_condition_holds": ok_phase, "failures": bad[:5]}


def direct_crosscheck(eng, states, allowed, d, M, target, rng, n=60, negatives=6):
    """Direct merges on random (label tuple, witness) pairs, and non-witness controls."""
    p = eng.p
    good = cases = 0
    neg_detected = neg = 0
    enumerate_ok = p**M <= 200_000
    g = len(allowed[0])
    for _ in range(n):
        if enumerate_ok:
            labels = tuple(rng.choice(allowed) for _ in range(M))
            wits = all_witnesses(labels, d, p)
            s = wits[rng.randrange(len(wits))]
        else:          # random s with s_M != 0, random lam_1..lam_(M-1), lam_M solving the witness equation
            s = [rng.randrange(p) for _ in range(M-1)]+[rng.randrange(1, p)]
            labels = [rng.choice(allowed) for _ in range(M-1)]
            acc = [sum(pow(si, d, p)*l[j] for si, l in zip(s, labels)) % p for j in range(g)]
            c = (-pow(pow(s[-1], d, p), -1, p)) % p
            labels = tuple(labels+[tuple(int(c*a % p) for a in acc)])
            if labels[-1] not in set(allowed):
                raise ArithmeticError("K_perp is not a subspace")
        act = [states[lam] for lam, si in zip(labels, s) if si]
        out = eng.merge(act, [int(x) for x in s if x])
        cases += 1
        good += out.equals_indicator(target)
    nz = [l for l in allowed if any(l)]
    for _ in range(negatives if nz else 0):
        labels = tuple(rng.choice(nz) for _ in range(M))
        for _try in range(50):
            s = [rng.randrange(p) for _ in range(M)]
            tot = [sum(pow(si, d, p)*l[j] for si, l in zip(s, labels)) % p for j in range(len(labels[0]))]
            if any(s) and any(tot):
                break
        else:
            continue
        neg += 1
        act = [states[lam] for lam, si in zip(labels, s) if si]
        try:
            out = eng.merge(act, [int(x) for x in s if x])
            neg_detected += not out.equals_indicator(target)
        except ArithmeticError:
            neg_detected += 1
    return {"direct_witness_merges": cases, "direct_equal_rho": good == cases,
            "non_witness_controls": neg, "non_witness_detected": neg_detected}


def covered_pairs(p, M, K):
    return (p**M-1)*K**(M-1)


def exhaustive_instance(cfg, inst, eng=None, *, source="gates", seed=0, direct=60, log=print, source_state=None):
    eng = eng or SparseEngine(cfg)
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    t0 = time.time()
    row = {"instance": inst.name, "normal": bool(inst.normal), "dim_h": len(inst.log_h), "grades": {}}
    if source_state is not None:
        st = source_state
        row["source"] = "given"
    elif source == "gates":
        st, S, info = eng.source(inst)
        row["source"] = {"mode": "gate list on all addresses", **info,
                         "equals_rho_lift": bool(info["coset_state"] and
                                                 np.array_equal(np.sort(S), stage_indices(cfg, inst.log_h, c)))}
        row["source_seconds"] = round(time.time()-t0, 1)
    else:
        st = truth_state(cfg, inst, c)
        row["source"] = {"mode": "exact coset density of exp(h~) (not from the gate list)"}
    ok = row["source"] == "given" or row["source"].get("equals_rho_lift", True)
    if log:
        log(inst.name, "source", row["source"] if isinstance(row["source"], str) else row["source"].get("mode"),
            ok, round(time.time()-t0, 1), "s")
    for d in range(c, 1, -1):
        t1 = time.time()
        allowed = allowed_labels(cfg, inst.log_h, d)
        M = cfg.arity[d]
        target = stage_indices(cfg, inst.log_h, d-1)
        flags, phi0, W, basis = branch_structure(eng, st, allowed, d)
        sub = subset_checks(eng, phi0, W, d, M, target)
        _, states = eng.label_law(st)
        cross = direct_crosscheck(eng, states, allowed, d, M, target, rng, n=direct)
        g_ok = all(v for k, v in flags.items() if isinstance(v, bool)) and sub["zero_label_merges_equal_rho"] and \
            sub["phase_condition_holds"] and cross["direct_equal_rho"] and \
            cross["non_witness_detected"] == cross["non_witness_controls"]
        row["grades"][d] = {"arity": M, **flags, **sub, **cross,
                            "pairs_covered": covered_pairs(p, M, len(allowed)), "exhaustive": bool(g_ok),
                            "input_support": int(len(st)), "target_support": int(len(target)),
                            "seconds": round(time.time()-t1, 1)}
        if log:
            log(inst.name, f"grade {d}", g_ok, row["grades"][d]["pairs_covered"], "pairs", row["grades"][d]["seconds"], "s")
        ok = ok and g_ok
        st = truth_state(cfg, inst, d-1)
    probs = eng.readout(st)
    hp = {tuple(int(x) for x in r) for r in span_elements(nullspace(inst.log_h, cfg.m, p), cfg.m, p)}
    row["readout_uniform_on_h_perp"] = set(probs) == hp and all(v == Fraction(1, len(hp)) for v in probs.values())
    row["passed"] = bool(ok and row["readout_uniform_on_h_perp"])
    row["seconds"] = round(time.time()-t0, 1)
    return row


def source_sampled_check(cfg, inst, n=1 << 14, seed=0):
    """The source gate list (generator backend) run bit-level on n random
    addresses x, on x*s for random s in exp(h~) and on x*u for random u not in
    exp(h~): the oracle key must agree on x, x*s and differ on x, x*u; the
    address must come back and the evaluation workspace must be clean.
    [sampled]: for top groups too large to evaluate on all addresses."""
    from theorems.rees_circuit_general import BitSim, compile_ops, source_circuit, wires_of
    rng = np.random.default_rng(seed)
    p, c = cfg.p, cfg.c
    law = cfg.laws[c]
    qc, B, (a_reg, a, w_reg, w, labels) = source_circuit(cfg, inst)
    pos = {q: i for i, q in enumerate(qc.qubits)}
    ops = compile_ops(qc.data[len(a):], pos)
    nS = len(stage_indices(cfg, inst.log_h, c))
    Sidx = np.sort(stage_indices(cfg, inst.log_h, c))
    X = rng.integers(0, p, size=(n, cfg.width[c]))
    s_el = law.decode(Sidx[rng.integers(0, len(Sidx), size=n)])
    U = rng.integers(0, p, size=(n, cfg.width[c]))
    inS = np.isin(law.encode(U), Sidx)
    U, keepn = U[~inS], int((~inS).sum())
    rows = np.concatenate([X, law.mul(X, s_el), law.mul(X[:keepn], U)])
    sim = BitSim(qc.num_qubits, len(rows))
    a_w, w_w = wires_of(a, pos), wires_of(w, pos)
    sim.load(a_w, rows)
    sim.run(ops)
    addr_ok = bool((sim.read(a_w) == rows).all())
    clean = bool((sim.read(w_w) == 0).all())
    key = np.zeros(len(rows), dtype=object)
    k = np.zeros(len(rows), dtype=np.int64)
    lb = cfg.label_bits
    keys = [sim.read_bits([pos[q] for q in y]) for y in labels]
    K = np.stack(keys, axis=1)
    same = bool((K[:n] == K[n:2*n]).all())
    differ = bool((K[:keepn] != K[2*n:]).any(axis=1).all())
    return {"mode": "sampled", "addresses": int(n), "S_translates": int(n), "non_S_translates": keepn,
            "address_unchanged": addr_ok, "workspace_clean": clean, "key_constant_on_S_cosets": same,
            "key_separates_non_S": differ, "S_order": int(nS),
            "passed": addr_ok and clean and same and differ}


def filiform6(p):
    from theorems.rees_end_to_end_sim import lie_from_brackets
    return lie_from_brackets(f"n6(F_{p})", p, 6, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1}})


def _u(n, *ones):
    v = [0]*n
    for i in ones:
        v[i] += 1
    return tuple(v)


N6_SUBGROUPS = [("trivial", ()), ("<e1> non-normal", (_u(6, 0),)), ("<e2> non-normal", (_u(6, 1),)),
                ("<e3> non-normal", (_u(6, 2),)), ("Z(G) = <e6>", (_u(6, 5),)),
                ("<e2,e6> non-normal", (_u(6, 1), _u(6, 5))), ("<e1+e2+e6> non-normal", (_u(6, 0, 1, 5),)),
                ("<e5,e6> = gamma_4", (_u(6, 4), _u(6, 5)))]


def family(alg, p, names=None):
    from theorems.rees_circuit_general import Hidden
    if alg == "n5":
        return Config(filiform5(p)), n5_instances(p, names=None)
    if alg == "n6":
        a = filiform6(p)
        return Config(a), [Hidden(f"{a.name} H={n}", a, g) for n, g in N6_SUBGROUPS]
    raise ValueError(alg)


def merge_proofs(cfg, log=print):
    out = {}
    for d in range(2, cfg.c+1):
        for s in range(1, cfg.p):
            t = time.time()
            out[f"d{d}_s{s}"] = prove_merge(cfg, d, s)
            if log:
                log("prove_merge", d, s, out[f"d{d}_s{s}"], round(time.time()-t, 1), "s")
    return out


def report(p=5, names=None, source="gates", out_path=None, proofs=True, seeds=(), log=print, alg="n5",
           max_support=2_000_000):
    from theorems.rees_circuit_sparse import run_algorithm_sparse
    t0 = time.time()
    cfg, insts = family(alg, p)
    eng = SparseEngine(cfg)
    res = {**STATUS, "config": cfg.name(), "group_orders": {d: int(cfg.laws[d].order) for d in cfg.laws},
           "arity": dict(cfg.arity), "rows": [], "seeded_runs": []}

    def dump():
        res["seconds"] = round(time.time()-t0, 1)
        res["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(res, fh, indent=1, default=str)
    if proofs:
        res["merge_proofs"] = merge_proofs(cfg, log)
        dump()
    for inst in insts:
        if names and not any(n in inst.name for n in names):
            continue
        t1 = time.time()
        nS = len(stage_indices(cfg, inst.log_h, cfg.c))
        biggest = nS*p**max(cfg.dims[d-1] for d in range(2, cfg.c+1))
        if nS > max_support:
            res["rows"].append({"instance": inst.name, "skipped": f"|exp(h~)| = {nS} rows; the conditioned "
                                f"states need up to {biggest} rows (budget {max_support})"})
            if log:
                log(inst.name, "skipped", nS)
            dump()
            continue
        if source == "gates":
            st, S, info = eng.source(inst)
            srow = {"mode": "gate list on all addresses", **info,
                    "equals_rho_lift": bool(info["coset_state"] and
                                            np.array_equal(np.sort(S), stage_indices(cfg, inst.log_h, cfg.c))),
                    "seconds": round(time.time()-t1, 1)}
            del S
        else:
            st = truth_state(cfg, inst, cfg.c)
            srow = {"mode": "exact coset density of exp(h~) (not from the gate list)", "equals_rho_lift": True,
                    "gate_list_sampled_check": source_sampled_check(cfg, inst)}
        if log:
            log(inst.name, "source", srow["mode"], srow["equals_rho_lift"], round(time.time()-t1, 1), "s")
        row = exhaustive_instance(cfg, inst, eng, source_state=st, log=log)
        row["source"] = srow
        row["passed"] = bool(row["passed"] and srow["equals_rho_lift"])
        res["rows"].append(row)
        dump()
        for sd in seeds:
            t1 = time.time()
            _, r = run_algorithm_sparse(cfg, inst, eng, seed=sd, top=st)
            rr = {"instance": inst.name, "seed": sd, "top": srow["mode"],
                  "seconds": round(time.time()-t1, 1), **r}
            res["seeded_runs"].append(rr)
            if log:
                log(json.dumps(rr))
            dump()
    dump()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=5)
    ap.add_argument("--alg", choices=["n5", "n6"], default="n5")
    ap.add_argument("--max-support", type=int, default=2_000_000)
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--source", choices=["gates", "truth"], default="gates")
    ap.add_argument("--no-proofs", action="store_true")
    ap.add_argument("--seeds", nargs="*", type=int, default=[])
    ap.add_argument("--out")
    a = ap.parse_args()
    report(a.p, a.names, a.source, a.out, not a.no_proofs, tuple(a.seeds),
           log=lambda *x: print(*x, flush=True), alg=a.alg, max_support=a.max_support)


if __name__ == "__main__":
    main()


# ====================================================================== round 2: power-class SDE solver, seeded runs

def power_class_sde(labels, d, p, rng, cap=5_000_000):
    """Exact and complete classical solver of sum_i s_i^d lambda_i = 0, s != 0:
    enumerate u in P^M with P = {x^d : x in F_p} (the d-th powers and 0), keep the
    nonzero u with sum_i u_i lambda_i = 0, and lift each u_i to an s_i with
    s_i^d = u_i. |P| = 1 + (p-1)/gcd(d, p-1), so the search has |P|^M points
    instead of p^M (n6(F_7), d = 3, M = 10: 3^10 = 59049 instead of 7^10).
    The witness is drawn with the weight prod_i #{s_i : s_i^d = u_i} of u, i.e.
    uniformly among ALL witnesses s, the distribution of brute_force_sde.
    Returns (s, number of witnesses s)."""
    lab = np.array(labels, dtype=np.int64)
    M = len(lab)
    pre = {}
    for x in range(p):
        pre.setdefault(pow(x, d, p), []).append(x)
    P = np.array(sorted(pre), dtype=np.int64)
    if len(P)**M > cap:
        raise ValueError("power-class search too large")
    idx = np.array(list(product(range(len(P)), repeat=M)), dtype=np.int64).reshape(-1, M)
    U = P[idx]
    ok = ~((U @ lab) % p).any(axis=1) & U.any(axis=1)
    sols = U[ok]
    if not len(sols):
        return None, 0
    mult = np.array([len(pre[int(v)]) for v in P], dtype=np.int64)
    w = np.prod(mult[idx[ok]], axis=1)
    total = int(w.sum())
    r = rng.randrange(total)
    k = int(np.searchsorted(np.cumsum(w), r, side="right"))
    s = tuple(int(rng.choice(pre[int(v)])) for v in sols[k])
    return s, total


def solve_sde_pc(labels, d, p, rng):
    """solve_sde with the power-class search in place of brute force: the IS solver
    where the arity reaches its column count (as before), else power_class_sde."""
    from theorems.rees_is_sde_solver import columns_required, is_sde_solve
    cols = [tuple(int(x) for x in l) for l in labels]
    rank = len(rref(cols, p))
    if len(cols) >= columns_required(p, d, rank):
        return tuple(int(x) for x in is_sde_solve(p, d, cols).s), "is"
    s, _ = power_class_sde(cols, d, p, rng)
    if s is None:
        raise ArithmeticError("no witness")
    return s, "power_class"


def run_algorithm_sparse_pc(cfg, inst, eng, seed=0, extra_samples=4, top=None, log=None):
    """rees_circuit_sparse.run_algorithm_sparse with solve_sde_pc (same structure:
    sampled labels, classical witness, Schur-product merge, readout); the witness
    equation is re-checked for every merge."""
    rng = random.Random(seed)
    p, c = cfg.p, cfg.c
    if top is None:
        top, _, _ = eng.source(inst)
    law_cache = {}
    from collections import Counter
    stats = Counter()

    def law_of(st, key):
        if key not in law_cache:
            law_cache[key] = eng.label_law(st)
        return law_cache[key]

    def sample(probs):
        keys = [k for k in probs if probs[k]]
        return rng.choices(keys, weights=[float(probs[k]) for k in keys], k=1)[0]

    def make(d):
        if d == c:
            stats["top_sources"] += 1
            probs, states = law_of(top, ("top",))
            lam = sample(probs)
            return lam, states[lam]
        kids = [make(d+1) for _ in range(cfg.arity[d+1])]
        labels = [k[0] for k in kids]
        s, used = solve_sde_pc(labels, d+1, p, rng)
        tot = [sum(pow(si, d+1, p)*l[j] for si, l in zip(s, labels)) % p for j in range(len(labels[0]))]
        if any(tot) or not any(s):
            raise ArithmeticError("not a witness")
        stats[f"solver_{used}_d{d+1}"] += 1
        out = eng.merge([k[1] for k in kids], s)                  # as run_algorithm_sparse
        if d == 1:
            return None, out
        probs, states = law_of(out, out.key())
        lam = sample(probs)
        return lam, states[lam]

    samples = []
    t0 = time.time()
    for n in range(cfg.m+extra_samples):
        _, st = make(1)
        probs = eng.readout(st)
        samples.append(sample(probs))
        if log:
            log("terminal sample", n, round(time.time()-t0, 1), "s")
    got = rref(nullspace(samples, cfg.m, p), p)
    return got, {"oracle_queries": len(cfg.points)*stats["top_sources"], **dict(stats),
                 "recovered": got == rref(inst.log_h, p), "terminal_samples": len(samples)}


def seeded_report(alg="n6", p=7, names=None, seeds=(1,), out_path=None, max_support=2_000_000, log=print):
    """Seeded recovery runs from the exact coset density of exp(h~) (computed from h,
    not from oracle queries; as in report()), with the power-class solver."""
    t0 = time.time()
    cfg, insts = family(alg, p)
    eng = SparseEngine(cfg)
    res = {**STATUS, "config": cfg.name(), "arity": dict(cfg.arity), "solver": "IS where it applies, else "
           "power-class search (power_class_sde)", "top": "exact coset density of exp(h~) (truth_state)",
           "seeded_runs": []}
    for inst in insts:
        if names and not any(n in inst.name for n in names):
            continue
        nS = len(stage_indices(cfg, inst.log_h, cfg.c))
        if nS > max_support:
            res["seeded_runs"].append({"instance": inst.name, "skipped": f"|exp(h~)| = {nS}"})
            if out_path:
                with open(out_path, "w") as fh:
                    json.dump(res, fh, indent=1, default=str)
            continue
        top = truth_state(cfg, inst, cfg.c)
        for sd in seeds:
            t1 = time.time()
            _, r = run_algorithm_sparse_pc(cfg, inst, eng, seed=sd, top=top, log=log)
            rr = {"instance": inst.name, "normal": bool(inst.normal), "seed": sd,
                  "seconds": round(time.time()-t1, 1), **r}
            res["seeded_runs"].append(rr)
            if log:
                log(json.dumps(rr))
            res["seconds"] = round(time.time()-t0, 1)
            res["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
            if out_path:
                with open(out_path, "w") as fh:
                    json.dump(res, fh, indent=1, default=str)
    res["seconds"] = round(time.time()-t0, 1)
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(res, fh, indent=1, default=str)
    return res
