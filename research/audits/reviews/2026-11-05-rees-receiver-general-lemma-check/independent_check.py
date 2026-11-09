"""Independent checks for the general-lemma report (reviewer, 2026-11-05).

(I1) D1 from the raw flattened gate payloads (not the `nc` field): after the
     qft_dg of each label register, its wires are never a gate target, never in
     a SWAP, qft, oracle or measurement; list the components that still read it.
(I2) Every merge block of the assembled n4(F_5) program equals the MergeBlock
     program blk.prog (the object prove_controlled_merge / sde_exhaustive /
     block_structure run on), flattened, under ONE injective wire map phi, gate
     by gate; phi sends lam/x/Q to the right tree registers and every other
     block wire into the arithmetic ancilla + block-workspace pool.
(I3) The root block's U (first half of its sde_grade2 gates) equals the gate
     list of CoherentSDEK2(5, 2, 2) -- the circuit of exhaustive_p5_a2.json --
     under one injective wire map psi with psi(L[c][r]) = label of root child c,
     psi(S[c]) = phi(blk.S[c]), psi(workspace) inside ancilla + pool.
"""
import json, sys, time
t0 = time.time()
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
import theorems.rees_circuit_mono_c3 as R
import theorems.rees_circuit_mono as M
import theorems.rees_circuit_coherent as C
from theorems.rees_coherent_sde_k2 import CoherentSDEK2

cfg, insts, ts, steps, an = R.setup("n4_f5")
p = ts.p
out = {}

# ---------------- (I1)
readers = {}
ok1 = True
nlab = 0
for kind, reg in M._registers(ts):
    if not kind.startswith("label"):
        continue
    nlab += 1
    w = set(reg)
    i0 = [i for i, s in enumerate(steps) if s[0] == "qft_dg" and set(s[1]) == w]
    assert len(i0) == 1
    i0 = i0[0]
    for j in range(i0+1, len(steps)):
        kd, pl, comp = steps[j][0], steps[j][1], steps[j][2]
        if kd == "perm":
            for g, q in pl:
                if g == "swap":
                    if set(q) & w:
                        ok1 = False
                elif q[-1] in w:
                    ok1 = False
                elif set(q[:-1]) & w:
                    readers[comp] = readers.get(comp, 0)+1
        elif kd in ("qft", "qft_dg"):
            if set(pl) & w:
                ok1 = False
        elif kd == "oracle":
            if (set(pl[0]) | set(pl[1])) & w:
                ok1 = False
        elif kd == "measure":
            if {x for q in pl for x in q} & w:
                ok1 = False
out["I1_labels_control_only_after_qft_dg"] = {"label_registers": nlab, "ok": ok1,
                                               "components_reading_labels_after": sorted(readers)}

# ---------------- (I2)
def wires(regs):
    return [x for r in regs for x in r]

pool_anc = set(ts.pool) | set(ts.anc.all)
root = ts.tree
groups = {}
for d in (2, 3):
    comps = {f"sde_grade{d}", f"witness_control_grade{d}", f"bch_merge_grade{d}"}
    idx = [i for i, s in enumerate(steps) if s[2] in comps]
    gs, g = [], [idx[0]]
    for i in idx[1:]:
        if i == g[-1]+1:
            g.append(i)
        else:
            gs.append(g); g = [i]
    gs.append(g)
    groups[d] = gs

def match(ref_gates, ts_gates):
    phi, inv_ = {}, {}
    if len(ref_gates) != len(ts_gates):
        return None, f"length {len(ref_gates)} vs {len(ts_gates)}"
    for (ga, qa), (gb, qb) in zip(ref_gates, ts_gates):
        if ga != gb or len(qa) != len(qb):
            return None, "gate mismatch"
        for a, b in zip(qa, qb):
            if phi.setdefault(a, b) != b or inv_.setdefault(b, a) != a:
                return None, "map not injective/consistent"
    return phi, "ok"

def block_gates(g):
    gl = []
    for i in g:
        assert steps[i][0] == "perm"
        gl.extend(steps[i][1])
    return gl

res2 = []
parents = [(2, root, groups[2][0])] + [(3, kid, groups[3][j]) for j, kid in enumerate(root["kids"])]
for d, node, g in parents:
    blk = ts.blocks[d]
    ref = C.flatten(blk.prog, p, blk.anc)
    tsg = block_gates(g)
    phi, why = match(ref, tsg)
    row = {"grade": d, "gates": len(ref), "match": why}
    if phi is not None:
        kids = node["kids"]
        okl = all([phi.get(x) for x in wires(blk.lam[i])] == wires(kids[i]["z"]) for i in range(blk.M))
        okx = all([phi.get(x) for x in wires(blk.x[i])] == wires(kids[i]["reg"]) for i in range(blk.M))
        okq = [phi.get(x) for x in wires(blk.Q)] == wires(node["reg"])
        io = set(wires([q for r in blk.lam for q in r])) | set(wires([q for r in blk.x for q in r])) | set(wires(blk.Q))
        okw = all(phi[x] in pool_anc for x in phi if x not in io)
        row.update({"labels_to_children_labels": okl, "x_to_children_registers": okx, "Q_to_node_register": okq,
                    "all_other_block_wires_in_anc_or_pool": okw})
        if d == 2:
            root_phi, root_blk, root_g = phi, blk, g
    res2.append(row)
out["I2_blocks_equal_MergeBlock_prog_under_wire_map"] = res2

# ---------------- (I3)
circ = CoherentSDEK2(5, 2, 2)
cg = circ.flatten()
sde_steps = [i for i in root_g if steps[i][2] == "sde_grade2"]
sg = []
for i in sde_steps:
    sg.extend(steps[i][1])
half = len(sg)//2
psi, why = match(cg, sg[:half])
r3 = {"circuit_gates": len(cg), "ts_U_gates": half, "match": why,
      "U_inverse_is_reversed_U": sg[half:] == sg[:half][::-1]}
if psi is not None:
    kids = root["kids"]
    r3["L_to_root_children_labels"] = all([psi.get(x) for x in wires(circ.L[c])] == wires(kids[c]["z"]) for c in range(circ.M))
    r3["S_to_block_S"] = all([psi.get(x) for x in circ.S[c]] == [root_phi[x] for x in root_blk.S[c]] for c in range(circ.M))
    r3["workspace_in_anc_or_pool"] = all(psi[x] in pool_anc for x in psi if x not in circ.io_wires)
out["I3_root_U_equals_exhaustively_checked_circuit"] = r3
out["seconds"] = round(time.time()-t0, 1)
print(json.dumps(out, indent=1))
