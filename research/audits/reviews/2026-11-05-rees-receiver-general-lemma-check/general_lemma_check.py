"""Sanity check for research/audits/reviews/2026-11-05-rees-receiver-general-lemma.md.

(1) Hypothesis (D1) of Theorem 2 read off the compiled n4(F_5) coherent program:
    every label register is used other than as a control exactly twice, by its
    preparation QFT and by its instrument's inverse QFT, and never afterwards;
    every oracle-output register is written by its oracle call only.
(2) Hypothesis (D2c): in the assembled program each merge block is
    U_SDE, then per child ctrl_i, bch_i, ctrl_i^-1, then U_SDE^-1 (item level).
(3) Lemma 1 toy on S_3: for a right-translation circuit the reduced state of the
    control register is the same for every LEFT coset of a non-normal S and
    differs between RIGHT cosets.
(4) Per block: the witness circuit class, block_structure, prove_controlled_merge,
    sde_exhaustive at grade 3, and children i > 0 equal child 0 under register renaming.
"""
import itertools, json, sys, time
import numpy as np

t0 = time.time()
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
import theorems.rees_circuit_mono_c3 as R
import theorems.rees_circuit_mono as M
from theorems.rees_coherent_sde import Macro

cfg, insts, ts, steps, an = R.setup("n4_f5")
out = {"setup_seconds": round(time.time()-t0, 1), "steps": len(steps), "anatomy_ok": an["ok"]}

# ---- (1) labels and oracle outputs
regs = M._registers(ts)
label_rows, y_rows = [], []
for kind, reg in regs:
    w = set(reg)
    nc_steps = [i for i, s in enumerate(steps) if s[3] & w]
    if kind.startswith("label"):
        comps = [steps[i][2] for i in nc_steps]
        kinds = [steps[i][0] for i in nc_steps]
        ok = (len(nc_steps) == 2 and kinds == ["qft", "qft_dg"] and comps == ["instrument_qft"]*2
              and set(steps[nc_steps[0]][1]) == w and set(steps[nc_steps[1]][1]) == w)
        label_rows.append(ok)
    elif kind == "oracle_output":
        ok = len(nc_steps) == 1 and steps[nc_steps[0]][0] == "oracle"
        y_rows.append(ok)
out["D1_labels_noncontrol_only_prep_qft_and_instrument_qft_dg"] = {"registers": len(label_rows), "all_ok": all(label_rows)}
out["A2_oracle_outputs_written_only_by_oracle"] = {"registers": len(y_rows), "all_ok": all(y_rows)}
sched, ok_sched = M.measurement_schedule(ts, steps, level=2)
out["measurement_schedule_level2_check"] = bool(ok_sched)
lh = R.lemma_hypotheses_check(ts, steps, an)
out["lemma_hypotheses_check_ok"] = lh["ok"]

# ---- (2) block structure at item level
def same(a, b):
    if isinstance(a, Macro) and isinstance(b, Macro):
        return (a.kind, a.coeff, a.args, a.inv) == (b.kind, b.coeff, b.args, b.inv)
    return (not isinstance(a, Macro)) and (not isinstance(b, Macro)) and a == b

def inv(items):
    return [it.inverse() if isinstance(it, Macro) else it for it in reversed(items)]

blocks = {}
for d in (2, 3):
    comps = {f"sde_grade{d}", f"witness_control_grade{d}", f"bch_merge_grade{d}"}
    idx = [i for i, (c, _) in enumerate(ts.items) if c in comps]
    groups, g = [], [idx[0]]
    for i in idx[1:]:
        if i == g[-1]+1:
            g.append(i)
        else:
            groups.append(g); g = [i]
    groups.append(g)
    res = []
    for g in groups:
        items = [ts.items[i] for i in g]
        sde = [it for c, it in items if c == f"sde_grade{d}"]
        n = len(sde)
        ok_sde = n % 2 == 0 and all(same(a, b) for a, b in zip(sde[n//2:], inv(sde[:n//2])))
        cs = [c for c, _ in items]
        pre = len(list(itertools.takewhile(lambda c: c == f"sde_grade{d}", cs)))
        suf = len(list(itertools.takewhile(lambda c: c == f"sde_grade{d}", reversed(cs))))
        ok_pos = pre == suf == n//2
        mid = items[pre:len(items)-suf]
        # runs of equal component; ctrl_i^-1 and ctrl_{i+1} share a run, split by the length L of ctrl_0
        runs = [(c, [it for _, it in grp]) for c, grp in itertools.groupby(mid, key=lambda t: t[0])]
        ok_mid, kids = True, 0
        if not runs or runs[0][0] != f"witness_control_grade{d}":
            ok_mid = False
        else:
            L = len(runs[0][1]); cur = runs[0][1]; r = 1
            while r < len(runs):
                if runs[r][0] != f"bch_merge_grade{d}" or r+1 >= len(runs) or runs[r+1][0] != f"witness_control_grade{d}":
                    ok_mid = False; break
                wrun = runs[r+1][1]
                if len(wrun) not in (L, 2*L) or not all(same(a, b) for a, b in zip(wrun[:L], inv(cur))):
                    ok_mid = False; break
                kids += 1
                cur = wrun[L:]; r += 2
            ok_mid = ok_mid and cur == []
        res.append({"items": len(items), "sde_half": n//2, "U_then_Uinv": ok_sde, "sde_prefix_suffix": ok_pos,
                    "children_ctrl_bch_ctrlinv": ok_mid, "children": kids})
    blocks[d] = res
out["D2c_block_structure_item_level"] = {d: {"blocks": len(r), "all_ok": all(x["U_then_Uinv"] and x["sde_prefix_suffix"] and x["children_ctrl_bch_ctrlinv"] for x in r),
                                             "children_per_block": sorted({x["children"] for x in r})} for d, r in blocks.items()}

# ---- (3) Lemma 1 toy on S_3
perms = list(itertools.permutations(range(3)))
idx = {g: i for i, g in enumerate(perms)}
def mul(a, b):  # (a*b)(i) = a(b(i))
    return tuple(a[b[i]] for i in range(3))
def inv_(a):
    r = [0]*3
    for i, ai in enumerate(a): r[ai] = i
    return tuple(r)
S = [(0, 1, 2), (1, 0, 2)]           # <(12)>, not normal
def reduced_Q(coset):
    # X uniform on coset, Q uniform on S_3, |x>|q> -> |x q^-1>|q>; rho_Q[q,q'] = <C q^-1 | C q'^-1>
    n = len(perms); rho = np.zeros((n, n))
    for q in perms:
        for qq in perms:
            A = {mul(x, inv_(q)) for x in coset}; B = {mul(x, inv_(qq)) for x in coset}
            rho[idx[q], idx[qq]] = len(A & B)/len(coset)/n
    return rho
left = [sorted({mul(g, s) for s in S}) for g in perms]
right = [sorted({mul(s, g) for s in S}) for g in perms]
left = [list(t) for t in {tuple(c) for c in left}]
right = [list(t) for t in {tuple(c) for c in right}]
rl = [reduced_Q(c) for c in left]; rr = [reduced_Q(c) for c in right]
out["toy_S3"] = {"left_cosets_equal_reduced_Q": all(np.allclose(r, rl[0]) for r in rl),
                 "right_cosets_equal_reduced_Q": all(np.allclose(r, rr[0]) for r in rr),
                 "n_left": len(left), "n_right": len(right)}

# ---- (4) per-block: which witness circuit, its footprint, the symbolic merge proof, U_SDE exhaustive at grade 3
import theorems.rees_circuit_coherent as C
out["cfg_dims"] = list(map(int, cfg.dims))
out["blocks"] = {}
for d, blk in ts.blocks.items():
    row = {"witness_circuit": type(blk.sde).__name__, "p_g_d_M": [blk.p, blk.g, blk.d, blk.M],
           "block_structure": C.block_structure(blk)}
    pm = C.prove_controlled_merge(blk)
    row["prove_controlled_merge_proved"] = pm["proved"]
    if blk.p**(blk.M*blk.g) <= 10**5:
        row["sde_exhaustive"] = C.sde_exhaustive(blk)
    # children i > 0: ctrl_i + bch_i + ctrl_i^-1 equals child 0's program under S_0 -> S_i, x_0 -> x_i
    from theorems.rees_coherent_sde import Prog
    base = Prog(blk.ctrl[0]+blk.bch[0]+blk.ctrl[0].inverse())
    rel = []
    for i in range(1, blk.M):
        wmap = {w: w for w in range(blk.nw)}
        wmap.update(zip(blk.S[0], blk.S[i]))
        for j in range(blk.nx):
            wmap.update(zip(blk.x[0][j], blk.x[i][j]))
        other = Prog(blk.ctrl[i]+blk.bch[i]+blk.ctrl[i].inverse())
        rm = C.remap(base, wmap)
        rel.append(len(rm) == len(other) and all(same(a, b) for a, b in zip(rm, other)))
    row["children_equal_child0_under_register_renaming"] = all(rel)
    out["blocks"][d] = row
out["seconds"] = round(time.time()-t0, 1)
print(json.dumps(out, indent=1, default=str))
