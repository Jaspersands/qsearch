"""Round 3 (2026-11-05): the exact output law of the assembled class-three
coherent terminal sample (n4(F_5)) and deterministic merge checkpoints at c = 3.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-05-rees-receiver-round3.md (run JSONs in the
folder of the same name).

Object. The terminal sample of theorems/rees_circuit_coherent.TerminalSample
for the class-three filiform algebra over F_5 (1198 qubits, 2 694 596
X/CX/CCX/SWAP gates, 176 exact QFT_5, 36 oracle calls), flattened by
rees_circuit_mono.compile_program. Its program is: six grade-2 subtrees (each:
two top sources with three oracle calls and a grade-3 instrument, the
preparation of Q_2, the grade-3 merge block), the grade-2 instrument on each
Q_2, the preparation of Q_1, the grade-2 merge block and the final QFT.

Method (nothing is measured before the readout; every gate of the parts below
acts in program order on the exact joint state over Z[zeta_5]):

Phase A (one grade-2 subtree): the two sources are run on the whole address
superposition (78125 rows each) with their oracle calls; checkpoint KS (the
source state is sum_x |x>|key(x)> with the left cosets of exp(h~) as key fibres,
clean workspace). The oracle outputs are then CONDITIONED on the key of one
coset (default: the identity coset). This is exact for the output law by the
coset-symmetry reduction (proved in the report, Section 2): the oracle outputs
are never touched again; every later gate acting on the source's address
commutes with the left translation x -> g x (the instrument is a central
translation; the merge is the right translation x -> x * t, proved for all
inputs by the symbolic replay prove_controlled_merge); so every coset branch
gives the same conditional law, with equal weights. The instrument follows
(gate level), checked against the instrument formula (K2). Q_2 is prepared and
the state is written exactly as an orthogonal sum over the hub values (both
grade-3 labels and Q_2): PackedHub keeps hub-classical wires as arrays over the
hubs and each child as bit-packed rows (hub, address) with Z[zeta_5]
amplitudes; it is HubState (round 2) with packed columns and chunking over
hubs (hubs never interact: the hub wires are only controls in the merge). The
grade-3 merge block (U_SDE, the witness-controlled BCH merges, U_SDE^-1) is
executed gate by gate. Checkpoints: K3 (workspace unentangled at the merge
component boundaries; each child already translated after its own merge), K4
(every row of every child equals its pre-merge row right-translated by
-delta_(s_i)(sigma(q)), with s the independent reference witness; labels and
Q_2 unchanged; witness and workspace 0), and K5_2: the reduced state of Q_2,
for every grade-3 label pair, is exactly proportional to rho_(H_2) (left
cosets of H_2 in G_2); the grade-3 label law is uniform on (K_3^perp)^2.

Phase B (the root): by the same symmetry at grade 2 (the grade-2 instrument is
a central translation of Q_2 and the grade-2 merge a right translation of
Q_2, proved by the symbolic replay), once K5_2 holds exactly, each Q_2 may be
replaced by the state of one left coset gH_2 (default g = e); the grade-2
instruments, the preparation of Q_1, the grade-2 merge block and the final QFT
are then executed gate by gate on the six children, with round-2's HubState
over (grade-2 labels, Q_1) and checkpoints K2_2, K3, K4, K5. When K_2^perp = 0
(gamma_2 and <e1+e2,e3>) the grade-2 labels are deterministic and this is the
exact output law of the whole terminal sample. Otherwise there are
|K_2^perp|^6 label tuples (5^6 or 25^6) and the root is run conditionally on
stated label tuples: the exact conditional law given those labels.

What this does NOT do: the explicit QFT of lem:qft-mod (QFT_p is exact);
kappa_d >= 3; general (G, H); an exact law at c = 3 for the seven subgroups
with K_2^perp != 0 (only conditional on chosen grade-2 label tuples); any
asymptotic statement. It flips no claim gate: coherent_receiver_implemented
stays False.
"""
from __future__ import annotations

import argparse
import copy
import math
from fractions import Fraction
import hashlib
import json
import resource
import time

import numpy as np

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
import theorems.rees_circuit_mono as M

STATUS = {"status": "exact_level0_law_class3_by_coset_symmetry_and_hub_decomposition_finite_instances",
          "coherent_receiver_implemented": False, "general_instances": False, "qft_synthesised": False,
          "speedup_claim_allowed": False, "review": "AI-checked, pending human review"}

WORK_ROLES = ("arith_ancilla", "evaluation_w", "block_workspace_pool")
ONES = np.uint64(0xFFFFFFFFFFFFFFFF)


# ====================================================================== small helpers

def pack(bits):
    bits = np.asarray(bits, dtype=np.uint8)
    by = np.packbits(bits, bitorder="little")
    nwords = (len(bits)+63)//64
    out = np.zeros(nwords*8, dtype=np.uint8)
    out[:len(by)] = by
    return out.view(np.uint64)


def unpack(col, N):
    return np.unpackbits(col.view(np.uint8), bitorder="little")[:N]


def tail_mask(N):
    m = np.full((N+63)//64, ONES, dtype=np.uint64)
    if N % 64:
        m[-1] = np.uint64((1 << (N % 64))-1)
    return m


def touched_wires(step):
    kind, payload = step[0], step[1]
    if kind == "perm":
        return {w for _, q in payload for w in q}
    if kind in ("qft", "qft_dg"):
        return set(payload)
    if kind == "oracle":
        return set(payload[0]) | set(payload[1])
    return {w for q in payload for w in q}


def values_to_bits(vals, regs_count, nb):
    """(N, k) coordinate values -> (N, k*nb) bits (register-major, bit i = wire i)."""
    vals = np.asarray(vals, dtype=np.int64)
    out = np.zeros((len(vals), regs_count*nb), dtype=np.uint8)
    for j in range(regs_count):
        for i in range(nb):
            out[:, j*nb+i] = (vals[:, j] >> i) & 1
    return out


def cyc_eq_up_to_scalar(act, ref, p):
    """act = c * ref row by row for ONE nonzero c in Q(zeta_p) (global scalar)."""
    if act.shape != ref.shape or not len(act):
        return False
    a0, r0 = act[:1], ref[:1]
    if not M.cyc_canon(r0).any():
        return False
    lhs = M.cyc_mul_rows(act, np.repeat(r0, len(act), axis=0), p)
    rhs = M.cyc_mul_rows(ref, np.repeat(a0, len(ref), axis=0), p)
    return bool(np.array_equal(M.cyc_canon(lhs), M.cyc_canon(rhs)))


def group_inverse(X, p):
    """Inverse in exponential coordinates (BCH): exp(X)^-1 = exp(-X)."""
    return (-np.asarray(X, dtype=np.int64)) % p


# ====================================================================== program anatomy (c = 3)

def left_coset_ids(law, S):
    """Same output as rees_circuit_mono._left_coset_ids (min index of x S for every
    x), with min(|S|, |G|/|S|) vectorized passes instead of |S|: for a large S it
    walks the cosets (one pass of |S| products per coset)."""
    S = np.asarray(S, dtype=np.int64)
    n = law.order
    if len(S)**2 <= n:
        return M._left_coset_ids(law, S)
    Sel = law.decode(S)
    ids = np.full(n, -1, dtype=np.int64)
    x0 = 0
    while x0 < n:
        if ids[x0] < 0:
            mem = law.encode(law.mul(np.repeat(law.decode(np.array([x0]))[0][None, :], len(Sel), axis=0), Sel))
            ids[mem] = mem.min()
        x0 += 1
        while x0 < n and ids[x0] >= 0:
            x0 += 1
    return ids


def anatomy(ts, steps):
    """Partition of the flattened c = 3 program: per grade-2 node j its Phase-A
    range (sources, grade-3 instruments, Q_2 preparation, grade-3 merge), its
    grade-2 instrument steps, and the root (Q_1 preparation, grade-2 merge,
    final QFT). Checks that every Phase-A step of node j touches only node j's
    wires and the shared workspace, every instrument step only Q_2j, z2_j and
    workspace, every root step only Q_1, the Q_2's, the z2's and workspace."""
    if ts.cfg.c != 3:
        raise ValueError("anatomy is for class 3")
    T = [touched_wires(s) for s in steps]
    work = {w for w in range(ts.nw) if ts.role[w] in WORK_ROLES}
    root = ts.tree
    Q1 = set(M._wires(root["reg"]))
    nodes = []
    for j, k in enumerate(root["kids"]):
        q2 = set(M._wires(k["reg"]))
        z2 = set(M._wires(k["z"]))
        srcw = set()
        for s in k["kids"]:
            srcw |= set(M._wires(s["reg"])) | set(M._wires(s["ys"])) | set(M._wires(s["z"]))
        first = min(i for i, t in enumerate(T) if t & srcw)
        inst_all = [i for i, t in enumerate(T) if t & z2]
        inst = [inst_all[0]]                      # the instrument: the first contiguous run on z2
        for i in inst_all[1:]:
            if i != inst[-1]+1:
                break
            inst.append(i)
        a_end = min(inst)-1
        rngA = list(range(first, a_end+1))
        okA = all(T[i] <= (srcw | q2 | work) for i in rngA)
        okI = all(T[i] <= (q2 | z2 | work) for i in inst) and all(steps[i][2].startswith("instrument") for i in inst)
        merge = [i for i in rngA if steps[i][2].endswith("grade3")]
        qprep = [i for i in rngA if steps[i][2] == "q_prep_qft"]
        nodes.append({"j": j, "node": k, "A": (first, a_end), "inst": (min(inst), max(inst)),
                      "merge": (min(merge), max(merge)), "q_prep": (min(qprep), max(qprep)),
                      "merge_contiguous": merge == list(range(min(merge), max(merge)+1)),
                      "phaseA_footprint_ok": okA, "instrument_footprint_ok": okI,
                      "q2": sorted(q2), "z2": sorted(z2), "srcw": srcw})
    covered = set()
    for n in nodes:
        covered |= set(range(n["A"][0], n["A"][1]+1)) | set(range(n["inst"][0], n["inst"][1]+1))
    rootsteps = [i for i in range(len(steps)) if i not in covered]
    allq2 = set().union(*[set(n["q2"]) for n in nodes])
    allz2 = set().union(*[set(n["z2"]) for n in nodes])
    okR = all(T[i] <= (Q1 | allq2 | allz2 | work) for i in rootsteps)
    split = max(i for i in rootsteps if steps[i][2] == "q_prep_qft")
    final = min(i for i in rootsteps if steps[i][2] == "final_qft")
    root_info = {"steps": rootsteps, "split": split, "final": final, "root_footprint_ok": okR,
                 "root_after_all_subtrees": min(rootsteps) > max(covered),
                 "q_prep": [i for i in rootsteps if steps[i][2] == "q_prep_qft"]}
    return {"nodes": nodes, "root": root_info, "work": sorted(work),
            "ok": all(n["phaseA_footprint_ok"] and n["instrument_footprint_ok"] and n["merge_contiguous"]
                      for n in nodes) and okR and root_info["root_after_all_subtrees"]}


def subtree_relabeling_check(ts, steps, an):
    """The Phase-A and instrument step lists of nodes 1..5 equal those of node 0
    gate for gate under one wire bijection that fixes the shared workspace."""
    work = set(an["work"])
    n0 = an["nodes"][0]

    def seq(n):
        a0, a1 = n["A"]
        i0, i1 = n["inst"]
        return [steps[i] for i in range(a0, a1+1)] + [steps[i] for i in range(i0, i1+1)]
    base = seq(n0)
    res = []
    for n in an["nodes"][1:]:
        other = seq(n)
        ok = len(other) == len(base)
        wmap = {}

        def bind(a, b):
            if a in work or b in work:
                return a == b
            if wmap.setdefault(a, b) != b:
                return False
            return True
        if ok:
            for s0, s1 in zip(base, other):
                if s0[0] != s1[0] or s0[2] != s1[2]:
                    ok = False
                    break
                if s0[0] == "perm":
                    if len(s0[1]) != len(s1[1]):
                        ok = False
                        break
                    for (g0, q0), (g1, q1) in zip(s0[1], s1[1]):
                        if g0 != g1 or len(q0) != len(q1) or not all(bind(a, b) for a, b in zip(q0, q1)):
                            ok = False
                            break
                elif s0[0] in ("qft", "qft_dg"):
                    ok = len(s0[1]) == len(s1[1]) and all(bind(a, b) for a, b in zip(s0[1], s1[1]))
                elif s0[0] == "oracle":
                    ok = all(len(x) == len(y) and all(bind(a, b) for a, b in zip(x, y))
                             for x, y in zip(s0[1], s1[1]))
                if not ok:
                    break
        ok = ok and len(set(wmap.values())) == len(wmap)
        res.append(bool(ok))
    return {"nodes_1_to_5_equal_node_0_up_to_wire_bijection": all(res), "per_node": res}


def lemma_hypotheses_check(ts, steps, an):
    """Footprint hypotheses (2) and (3) of Lemmas A and B (report, Section 2),
    read off the flattened program. For every top source: its oracle outputs Y
    are never touched after the source end (the step before the first QFT of its
    instrument); every later step touching its address belongs to its own
    instrument or to the controlled merge components of its parent's grade-3
    block. For every grade-2 node: after its grade-3 merge block, the traced
    wires of the subtree (addresses, oracle outputs, grade-3 labels) are never
    touched, and every later step touching Q_2 belongs to its grade-2
    instrument or to the controlled merge components of the root block. The
    readout (final_qft) acts on Q_1 only."""
    T = [touched_wires(s_) for s_ in steps]
    allowA = lambda c: c.startswith("instrument") or c in ("witness_control_grade3", "bch_merge_grade3")
    allowQ = lambda c: c.startswith("instrument") or c in ("witness_control_grade2", "bch_merge_grade2")
    src_rows, node_rows = [], []
    allA = [set(M._wires(s_["reg"])) for n in an["nodes"] for s_ in n["node"]["kids"]]
    allQ2 = [set(n["q2"]) for n in an["nodes"]]

    def merge_interval(R_, after, comps_ok, others):
        """The steps after `after` that touch R_ in merge components form one
        interval of merge-component steps that touches no other child."""
        idx = [i for i in range(after+1, len(steps)) if T[i] & R_ and comps_ok(steps[i][2])
               and not steps[i][2].startswith("instrument")]
        if not idx:
            return False
        lo, hi = min(idx), max(idx)
        return all(comps_ok(steps[i][2]) and not steps[i][2].startswith("instrument") and
                   not any(T[i] & o for o in others) for i in range(lo, hi+1))
    for n in an["nodes"]:
        traced = set()
        for s_ in n["node"]["kids"]:
            A = set(M._wires(s_["reg"]))
            Y = set(M._wires(s_["ys"]))
            Z = set(M._wires(s_["z"]))
            traced |= A | Y | Z
            firstq = min(i for i, st_ in enumerate(steps) if st_[0] == "qft" and set(st_[1]) <= Z)
            send = firstq-1
            last_oracle = max(i for i, st_ in enumerate(steps) if st_[0] == "oracle" and T[i] & Y)
            comps = sorted({steps[i][2] for i in range(send+1, len(steps)) if T[i] & A})
            y_after = any(T[i] & Y for i in range(send+1, len(steps)))
            inst_run = [i for i in range(send+1, len(steps)) if T[i] & A and steps[i][2].startswith("instrument")]
            # its own instrument: the instrument steps on its label register Z, from the first QFT on Z
            z_inst = [i for i in range(send+1, len(steps)) if T[i] & Z and steps[i][2].startswith("instrument")]
            others_A = [o for o in allA if o != A]
            inst_contig = bool(inst_run) and inst_run == list(range(inst_run[0], inst_run[-1]+1)) and \
                bool(z_inst) and firstq <= inst_run[0] and inst_run[-1] <= max(z_inst) and \
                not any(T[i] & o for i in inst_run for o in others_A)
            mi = merge_interval(A, send, allowA, [o for o in allA if o != A])
            src_rows.append({"node": n["j"], "source_end": send, "last_oracle_call": last_oracle,
                             "components_touching_address_after_source_end": comps,
                             "instrument_contiguous_and_own": inst_contig, "merge_one_interval_no_other_child": mi,
                             "ok": bool(last_oracle < send and not y_after and all(allowA(c) for c in comps)
                                        and inst_contig and mi)})
        m1 = n["merge"][1]
        Q2 = set(n["q2"])
        traced_after = any(T[i] & traced for i in range(m1+1, len(steps)))
        comps = sorted({steps[i][2] for i in range(m1+1, len(steps)) if T[i] & Q2})
        mi = merge_interval(Q2, m1, allowQ, [o for o in allQ2 if o != Q2])
        # every instrument step touching Q_2 is in this node's own grade-2 instrument
        q_inst = [i for i in range(m1+1, len(steps)) if T[i] & Q2 and steps[i][2].startswith("instrument")]
        own_inst = bool(q_inst) and all(n["inst"][0] <= i <= n["inst"][1] for i in q_inst)
        node_rows.append({"node": n["j"], "traced_wires_touched_after_grade3_merge": bool(traced_after),
                          "components_touching_Q2_after_grade3_merge": comps,
                          "merge_one_interval_no_other_child": mi, "instrument_is_own_grade2_instrument": own_inst,
                          "ok": bool(not traced_after and all(allowQ(c) for c in comps) and mi and own_inst)})
    Q1 = set(M._wires(ts.root))
    fin = [i for i in range(len(steps)) if steps[i][2] == "final_qft"]
    fin_ok = bool(fin) and all(T[i] <= Q1 for i in fin) and fin == list(range(fin[0], len(steps)))
    return {"sources": src_rows, "grade2_nodes": node_rows, "readout_on_Q1_only_and_last": fin_ok,
            "ok": all(r["ok"] for r in src_rows+node_rows) and fin_ok}


# ====================================================================== PackedHub

class _Rows:
    """One child: rows (hub index, src row) with bit-packed local wire columns."""

    def __init__(self, hub_of_row, src, H):
        self.h = hub_of_row
        self.src = src
        self.N = len(src)
        self.cnt = np.bincount(hub_of_row, minlength=H)
        self.cols = {}
        self.bc = {}                     # broadcast cache of hub-classical controls
        self.mask = tail_mask(self.N)

    def broadcast(self, vals):
        return pack(vals[self.h])


class PackedHub:
    """Exact state sum_h |c(h)> (x) prod_e |psi_e(h)> over the hubs h of one chunk:
    hub-classical wires are uint8 arrays over the hubs; each child e is a set of
    rows (h, local bits) whose amplitudes are fixed (only permutation gates act
    in a merge segment). A gate touching only hub-classical wires acts on the
    arrays; a gate touching wires of one child acts on its packed columns (a
    hub-classical target is first moved into that child, a hub-classical control
    is broadcast); a gate touching two children raises (it never happens in a
    merge block: the children stay separate). A local wire that becomes 0 on all
    rows returns to the hub arrays (exact: it is then the constant 0)."""

    def __init__(self, H, hub_init, engines):
        self.H = H
        self.hub = {w: np.asarray(v, dtype=np.uint8).copy() for w, v in hub_init.items()}
        self.E = engines
        self.owner = {}
        for k, e in enumerate(engines):
            for w in e.cols:
                self.owner[w] = k
        self.gates = 0

    def _hubval(self, w):
        v = self.hub.get(w)
        if v is None:
            v = np.zeros(self.H, dtype=np.uint8)
            self.hub[w] = v
        return v

    def _invalidate(self, w):
        for e in self.E:
            e.bc.pop(w, None)

    def _ctrl_col(self, e, k, w):
        if self.owner.get(w) == k:
            return e.cols[w]
        c = e.bc.get(w)
        if c is None:
            c = e.broadcast(self._hubval(w))
            e.bc[w] = c
        return c

    def gate(self, name, q):
        self.gates += 1
        if name == "swap":
            a, b = q
            oa, ob = self.owner.pop(a, None), self.owner.pop(b, None)
            va = self.E[oa].cols.pop(a) if oa is not None else self.hub.pop(a, None)
            vb = self.E[ob].cols.pop(b) if ob is not None else self.hub.pop(b, None)
            self._invalidate(a)
            self._invalidate(b)
            if ob is not None:
                self.E[ob].cols[a] = vb
                self.owner[a] = ob
            elif vb is not None:
                self.hub[a] = vb
            if oa is not None:
                self.E[oa].cols[b] = va
                self.owner[b] = oa
            elif va is not None:
                self.hub[b] = va
            return
        t, ctrls = q[-1], q[:-1]
        ks = {self.owner[w] for w in q if w in self.owner}
        if not ks:
            v = self._hubval(t)
            if ctrls:
                m = self._hubval(ctrls[0])
                for c in ctrls[1:]:
                    m = m & self._hubval(c)
                np.bitwise_xor(v, m, out=v)
            else:
                np.bitwise_xor(v, 1, out=v)
            self._invalidate(t)
            return
        if len(ks) > 1:
            raise AssertionError(f"gate {name}{tuple(q)} joins two children")
        k = ks.pop()
        e = self.E[k]
        if self.owner.get(t) != k:
            e.cols[t] = e.broadcast(self._hubval(t))
            self.hub.pop(t, None)
            self._invalidate(t)
            self.owner[t] = k
        col = e.cols[t]
        if ctrls:
            m = self._ctrl_col(e, k, ctrls[0])
            if len(ctrls) > 1:
                m = m & self._ctrl_col(e, k, ctrls[1])
                for c in ctrls[2:]:
                    m &= self._ctrl_col(e, k, c)
            np.bitwise_xor(col, m, out=col)
        else:
            np.bitwise_xor(col, e.mask, out=col)

    def run(self, gates):
        g = self.gate
        for name, q in gates:
            g(name, q)

    def delocalize_zeros(self, wires):
        for w in wires:
            k = self.owner.get(w)
            if k is None:
                continue
            e = self.E[k]
            if not e.cols[w].any():
                del e.cols[w]
                del self.owner[w]
                self.hub[w] = np.zeros(self.H, dtype=np.uint8)
                self._invalidate(w)

    def local_wires(self):
        return set(self.owner)

    def read(self, k, wires):
        """Values (N,) of a register (bit i = wires[i]) on child k's rows (local or hub)."""
        e = self.E[k]
        out = np.zeros(e.N, dtype=np.int64)
        for i, w in enumerate(wires):
            if self.owner.get(w) == k:
                out |= unpack(e.cols[w], e.N).astype(np.int64) << i
            elif w in self.owner:
                raise AssertionError("wire of another child")
            else:
                out |= self._hubval(w)[e.h].astype(np.int64) << i
        return out

    def hubreg(self, wires):
        out = np.zeros(self.H, dtype=np.int64)
        for i, w in enumerate(wires):
            if w in self.owner:
                raise ValueError("register is not hub-classical")
            out |= self._hubval(w).astype(np.int64) << i
        return out


# ====================================================================== Phase A

def _regs_values(st, regs, nb):
    """Joint rows of the factors holding regs: (values (N, len regs), amp, extra wires in those factors)."""
    A, B, amp = M.joint_rows(st, M._wires(regs))
    return M._bits_to_values(A, nb, len(regs)), amp, B.shape[1]


condition_on_coset = M.condition_on_coset


def instrument_reference(law, top, coset_idx, g, p):
    """Rows (x', lam) -> amplitude of the instrument applied to sum_(x in coset)|x>:
    psi(x', lam) = sum_z zeta^(-lam.z) [x' z in coset], z central (top coordinates)."""
    from itertools import product as iprod
    X = law.decode(np.asarray(coset_idx, dtype=np.int64))
    Z = np.array(list(iprod(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
    keys, exps = [], []
    for zv in Z:
        zinv = np.zeros((1, law.n), dtype=np.int64)
        zinv[0, top] = (-zv) % p
        xp = law.encode(law.mul(X, zinv))
        for li, lam in enumerate(Z):
            keys.append(xp*len(Z)+li)
            exps.append(np.full(len(xp), int(-np.dot(lam, zv)) % p))
    keys = np.concatenate(keys)
    exps = np.concatenate(exps)
    uk, inv = np.unique(keys, return_inverse=True)
    amp = np.zeros((len(uk), p), dtype=np.int64)
    np.add.at(amp, (inv.ravel(), exps), 1)
    amp = M.cyc_canon(amp)
    keep = amp.any(axis=1)
    return uk[keep], amp[keep], len(Z)


def _instrument_check(st, cfg, d, a_regs, z_regs, coset_idx):
    """K2 for a pure coset input: the joint rows of (address, label) equal the
    instrument reference up to one global scalar; no other wire entangled."""
    p, nb = cfg.p, cfg.enc.nb
    law = cfg.laws[d]
    g = cfg.dims[d-1]
    A, B, amp = M.joint_rows(st, M._wires(a_regs)+M._wires(z_regs))
    if B.shape[1]:
        return False
    x = law.encode(M._bits_to_values(A[:, :len(a_regs)*nb], nb, len(a_regs)))
    lam = M._bits_to_values(A[:, len(a_regs)*nb:], nb, len(z_regs))
    li = np.zeros(len(lam), dtype=np.int64)
    for j in range(g):
        li = li*p+lam[:, j]
    keys = x*p**g+li
    nz = M.cyc_canon(amp).any(axis=1)
    keys, amp = keys[nz], amp[nz]
    order = np.argsort(keys)
    keys, amp = keys[order], amp[order]
    rk, ra, _ = instrument_reference(law, cfg.top(d), coset_idx, g, p)
    return bool(np.array_equal(keys, rk) and cyc_eq_up_to_scalar(amp, ra, p))


def _child_rows(st, cfg, d, a_regs, z_regs):
    """Joint rows of a child (address, label): (x index, label tuple index, amp)."""
    p, nb = cfg.p, cfg.enc.nb
    law = cfg.laws[d]
    A, B, amp = M.joint_rows(st, M._wires(a_regs)+M._wires(z_regs))
    if B.shape[1]:
        raise AssertionError("child entangled with other wires")
    xv = M._bits_to_values(A[:, :len(a_regs)*nb], nb, len(a_regs))
    lam = M._bits_to_values(A[:, len(a_regs)*nb:], nb, len(z_regs))
    nz = M.cyc_canon(amp).any(axis=1)
    return xv[nz], lam[nz], M.cyc_canon(amp[nz])


def autocorrelation(law, X, amp, p, chunk=64):
    """A(u) = <phi| R_u |phi> = sum_x conj(phi(x u)) phi(x) for all u in G (dense (order, p))."""
    A = np.zeros((law.order, p), dtype=np.int64)
    Xi = group_inverse(X, p)
    ca = M.cyc_conj(amp)
    for a in range(0, len(X), chunk):
        sl = slice(a, min(len(X), a+chunk))
        U = law.encode(law.mul(Xi[sl][:, None, :], X[None, :, :]))       # x_a^-1 x_b
        V = M.cyc_mul_rows(amp[sl][:, None, :], ca[None, :, :], p)          # phi(x_a) conj(phi(x_b))
        np.add.at(A, U.ravel(), V.reshape(-1, p))
    return M.cyc_canon(A)


def phase_a(ts, inst, steps, an, j=0, *, coset_x0=0, chunk_rows=3_000_000, checks=True, log=None,
            direct_gram=False, return_rows=False, sources_only=False, hub_range=None):
    """Phase A for grade-2 node j (see the module docstring). Returns a dict with
    the checkpoints and the exact reduced state of Q_2 (as proportionality to
    rho_(H_2) per grade-3 label pair)."""
    cfg, p = ts.cfg, ts.p
    nb = cfg.enc.nb
    law3, law2 = cfg.laws[3], cfg.laws[2]
    t0 = time.time()
    nd = an["nodes"][j]
    node = nd["node"]
    srcs = node["kids"]
    table = np.asarray(inst.oracle_table, dtype=np.int64)
    S3 = G.stage_indices(cfg, inst.log_h, 3)
    cids = left_coset_ids(law3, S3)
    work = [w for w in an["work"]]
    out = {"name": inst.name, "normal": bool(inst.normal), "node": j, "coset_x0": int(coset_x0)}
    ck = {"KS_source_state_is_coset_superposition": [], "K0_workspace_clean": [],
          "K1c_conditioned_support_is_one_left_coset": [], "K2_instrument_equals_reference": []}
    # source end (before its instrument's first QFT) and instrument end, per source
    send, iend = {}, {}
    for si, s in enumerate(srcs):
        zw = set(M._wires(s["z"]))
        firstq = min(i for i, st_ in enumerate(steps) if st_[0] == "qft" and set(st_[1]) <= zw)
        send[firstq-1] = si
        e_ = firstq
        while touched_wires(steps[e_+1]) & zw and steps[e_+1][2].startswith("instrument"):
            e_ += 1
        iend[e_] = si
    st = M.FactorState(ts.nw, p, max_rows=2_000_000, max_bytes=2.5e9)
    a0, a1 = nd["A"]
    m0, m1 = nd["merge"]
    coset_of = {}
    for i in range(a0, m0):
        kind, payload, comp, nc, _ = steps[i]
        if kind == "perm":
            st.run(payload)
            st.split_constants(nc)
        elif kind in ("qft", "qft_dg"):
            st.qft(payload, inverse=(kind == "qft_dg"))
        elif kind == "oracle":
            st.oracle(payload[0], payload[1], table, nb, cfg.m, cfg.label_bits)
        else:
            raise ValueError(kind)
        if i in send:
            s = srcs[send[i]]
            ck["K0_workspace_clean"].append(all(st.owner[w] < 0 and st.cval[w] == 0 for w in work))
            if checks:
                ck["KS_source_state_is_coset_superposition"].append(
                    M.source_coset_check(st, cfg, s["reg"], s["ys"], cids, work))
            condition_on_coset(st, cfg, s["reg"], s["ys"], coset_x0)
            xv, _, _ = _regs_values(st, s["reg"], nb)
            xs = np.sort(law3.encode(xv))
            ref = np.sort(np.nonzero(cids == cids[coset_x0])[0])
            ck["K1c_conditioned_support_is_one_left_coset"].append(bool(np.array_equal(xs, ref)))
            coset_of[send[i]] = ref
        if i in iend:
            s = srcs[iend[i]]
            ck["K0_workspace_clean"].append(all(st.owner[w] < 0 and st.cval[w] == 0 for w in work))
            if checks:
                ck["K2_instrument_equals_reference"].append(
                    _instrument_check(st, cfg, 3, s["reg"], s["z"], coset_of[iend[i]]))
    if sources_only:
        out["checkpoint_counts"] = {k: len(v) for k, v in ck.items() if isinstance(v, list)}
        out["address_rows_per_source"] = int(law3.order)
        out["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
        out["checkpoints"] = {k: (bool(all(v)) if isinstance(v, list) else v) for k, v in ck.items() if v}
        out["all_checkpoints_pass"] = bool(all(out["checkpoints"].values()))
        out["seconds"] = round(time.time()-t0, 1)
        return out
    # ---- rows of the children and of Q_2
    kids = []
    for s in srcs:
        xv, lam, amp = _child_rows(st, cfg, 3, s["reg"], s["z"])
        li = lam @ (p**np.arange(lam.shape[1]-1, -1, -1))
        kids.append({"x": xv, "lam": li, "amp": amp, "xw": M._wires(s["reg"]), "zw": M._wires(s["z"])})
    Mk = len(kids)
    qv, qamp, extra = _regs_values(st, node["reg"], nb)
    nQ = law2.order
    out["Q2_uniform"] = bool(len(qv) == nQ and len(np.unique(law2.encode(qv))) == nQ and extra == 0
                             and (M.cyc_canon(qamp) == M.cyc_canon(qamp[:1])).all())
    qorder = np.argsort(law2.encode(qv))
    qv = qv[qorder]                                   # hub q index = encoded element
    q2w = M._wires(node["reg"])
    mw = set()
    for i in range(m0, m1+1):
        mw |= touched_wires(steps[i])
    io = set(q2w) | {w for k in kids for w in k["xw"]+k["zw"]}
    const_ok = all(st.owner[w] < 0 for w in mw - io)
    out["merge_inputs_other_wires_constant"] = bool(const_ok)
    out["oracle_outputs_constant_after_conditioning"] = bool(all(st.owner[w] < 0 for s in srcs
                                                                 for w in M._wires(s["ys"])))
    cval = {w: st.cval[w] for w in mw - io}
    del st
    labs = [np.unique(k["lam"]) for k in kids]
    nL = [len(lb) for lb in labs]
    nT = int(np.prod(nL))                             # label tuples
    H = nT*nQ
    out["hubs"] = int(H)
    rows_by_lab = [{int(l): np.nonzero(k["lam"] == l)[0] for l in lb} for k, lb in zip(kids, labs)]
    tot_rows = sum(nQ*(nT//nL[i])*len(kids[i]["lam"]) for i in range(Mk))
    out["total_child_rows"] = int(tot_rows)
    radix = np.cumprod([1]+nL[::-1])[:-1][::-1]       # mixed radix, child 0 most significant

    def digits(a):
        return [(a // int(radix[i])) % nL[i] for i in range(Mk)]
    # ---- reference witness per label tuple, translations per hub
    blk = ts.blocks[3]
    g3 = cfg.dims[2]
    lab_tuples = [tuple(int(labs[i][d]) for i, d in enumerate(digits(a))) for a in range(nT)]

    def lam_vec(li):
        return np.array([(li // p**(g3-1-r)) % p for r in range(g3)], dtype=np.int64)
    L = np.stack([np.stack([lam_vec(l) for l in lt], axis=1) for lt in lab_tuples])   # (T, g, M)
    s_ref = np.asarray(C.sde_reference(p, 3, L), dtype=np.int64)
    out["reference_witness_solves"] = bool((s_ref % p != 0).any(axis=1).all() and not (
        np.einsum("hgm,hm->hg", L, s_ref**3) % p).any())
    tq = {}
    for pi in range(nT):
        for i in range(Mk):
            tq[(pi, i)] = C._witness_bound_g(blk, np.full(nQ, s_ref[pi, i]), qv)    # (nQ, n)
    # ---- merge segment, chunked over hubs
    gates_seg = [(i, steps[i]) for i in range(m0, m1+1)]
    for i, s_ in gates_seg:
        if s_[0] != "perm":
            raise ValueError("non-permutation step in the merge segment")
    bounds = [i for i in range(m0, m1+1) if i == m1 or steps[i+1][2] != steps[i][2]]
    wc_ends = [i for i in bounds if steps[i][2].startswith("witness_control")][1:]
    if len(wc_ends) != Mk:
        raise AssertionError(f"{len(wc_ends)} witness-control boundaries for {Mk} children")
    child_end = {i: ci for ci, i in enumerate(wc_ends)}
    zw_all = [w for k in kids for w in k["zw"]]
    xall = {w for k in kids for w in k["xw"]}
    k3_unent, k3_child, k4_child, k4_hub, k4_clean = [], [], [], [], []
    sig = hashlib.sha256()
    hubs_per_chunk = max(1, int(chunk_rows // max(1, (tot_rows/H))))
    nchunks = 0
    keep_rows = [] if return_rows else None
    hr0, hr1 = (0, H) if hub_range is None else (max(0, int(hub_range[0])), min(H, int(hub_range[1])))
    out["hub_range"] = [int(hr0), int(hr1)]
    # K5_2 below is computed from the K4 descriptor over all q; on a partial hub range it is valid only
    # together with K4 on the other ranges (combine_hub_ranges)
    out["K5_2_conditional_on_K4_on_other_hub_ranges"] = bool((hr0, hr1) != (0, H))
    for h0 in range(hr0, hr1, hubs_per_chunk):
        h1 = min(hr1, h0+hubs_per_chunk)
        hh = np.arange(h0, h1)
        pidx, qi = hh // nQ, hh % nQ
        dig = digits(pidx)
        hub_init = {}
        labv = [labs[kk][dig[kk]] for kk in range(Mk)]
        for kk in range(Mk):
            vec = np.stack([(labv[kk] // p**(g3-1-r)) % p for r in range(g3)], axis=1)
            bits = values_to_bits(vec, g3, nb)
            for c_, w in enumerate(kids[kk]["zw"]):
                hub_init[w] = bits[:, c_]
        bits = values_to_bits(qv[qi], len(node["reg"]), nb)
        for c_, w in enumerate(q2w):
            hub_init[w] = bits[:, c_]
        for w, v in cval.items():
            if v:
                hub_init[w] = np.ones(h1-h0, dtype=np.uint8)
        engines = []
        for kk in range(Mk):
            per = [rows_by_lab[kk][int(l)] for l in labv[kk]]
            cnts = np.array([len(x) for x in per])
            hub_of_row = np.repeat(np.arange(h1-h0), cnts)
            src = np.concatenate(per) if per else np.zeros(0, dtype=np.int64)
            e = _Rows(hub_of_row, src, h1-h0)
            xb = values_to_bits(kids[kk]["x"][src], len(srcs[kk]["reg"]), nb)
            for c_, w in enumerate(kids[kk]["xw"]):
                e.cols[w] = pack(xb[:, c_])
            engines.append(e)
        ph = PackedHub(h1-h0, hub_init, engines)
        hub0 = {w: ph.hub[w].copy() for w in zw_all+q2w}

        def translated(kk):
            e = ph.E[kk]
            xr = srcs[kk]["reg"]
            xo = np.stack([ph.read(kk, list(r)) for r in xr], axis=1)
            xin = kids[kk]["x"][e.src]
            tt = np.empty((e.N, law3.n), dtype=np.int64)
            ph_ = pidx[e.h]
            for pi in np.unique(ph_):
                sel = ph_ == pi
                tt[sel] = tq[(int(pi), kk)][qi[e.h[sel]]]
            return bool(np.array_equal(xo, law3.mul(xin, tt))), xo
        for i, s_ in gates_seg:
            ph.run(s_[1])
            ph.delocalize_zeros(s_[3])
            if checks and i in bounds:
                k3_unent.append(not (ph.local_wires() & set(work)))
                if i in child_end:
                    k3_child.append(translated(child_end[i])[0])
        # K4
        res = [translated(kk) for kk in range(Mk)]
        k4_child.append(all(r[0] for r in res))
        k4_hub.append(all(np.array_equal(ph.hub.get(w, np.zeros(h1-h0, np.uint8)), hub0[w]) for w in hub0))
        loc = ph.local_wires() - xall
        dirty = [w for w in ph.hub if w not in hub0 and w not in xall and ph.hub[w].any()]
        k4_clean.append(not loc and not dirty)
        if (loc or dirty) and log:
            log(json.dumps({"K4_dirty_local": sorted(loc)[:20], "K4_dirty_hub": [(w, ts.role[w]) for w in dirty[:20]]}))
        for kk in range(Mk):
            sig.update(res[kk][1].tobytes())
        if return_rows:
            kr = []
            for kk in range(Mk):
                hg = ph.E[kk].h + h0
                sel = (hg // nQ) < 2
                kr.append((hg[sel], ph.E[kk].src[sel], res[kk][1][sel]))
            keep_rows.append((h0, h1, kr))
        nchunks += 1
        del ph, engines
    out["chunks"] = nchunks
    out["final_state_signature"] = sig.hexdigest()
    ck["K3_workspace_unentangled_at_each_merge_component_boundary"] = k3_unent
    ck["K3_child_translated_after_its_own_merge"] = k3_child
    ck["K4_children_equal_reference_translation_every_hub"] = k4_child
    ck["K4_labels_and_Q2_unchanged"] = k4_hub
    ck["K4_witness_and_workspace_zero"] = k4_clean
    # ---- K5_2: reduced state of Q_2 per label tuple, from the K4-verified child states:
    # child i at hub (lambda, q) is R_(t_i(q)) phi_(i, lambda_i) (K4, row by row), so
    # <c_i(q')|c_i(q)> = A_i(t_i(q) t_i(q')^-1) with A_i(u) = <phi_i| R_u |phi_i>
    H2 = G.stage_indices(cfg, inst.log_h, 2)
    lc2 = left_coset_ids(law2, H2)
    ref_pairs = nQ*len(H2)
    k5, consts = [], []
    allowed = set(G.allowed_labels(cfg, inst.log_h, 3))
    norms = [{} for _ in range(Mk)]
    phis = {}
    for kk in range(Mk):
        for l, rws in rows_by_lab[kk].items():
            X = kids[kk]["x"][rws]
            a = kids[kk]["amp"][rws]
            phis[(kk, l)] = (X, a)
            norms[kk][l] = M.cyc_canon(M.cyc_norm2(a, p).sum(axis=0))
    k4ok = all(k4_child) and all(k4_hub) and all(k4_clean)
    rho_sig = hashlib.sha256()
    descs = []
    if k4ok:
        Acache = {}
        degs = np.array(blk.degs)
        for pi, lt in enumerate(lab_tuples):
            sv = s_ref[pi]
            act = [kk for kk in range(Mk) if sv[kk] % p]
            Aa = []
            for kk, l in enumerate(lt):
                key = (kk, l)
                if key not in Acache:
                    Acache[key] = autocorrelation(law3, *phis[key], p)
                Aa.append(Acache[key])
            k0 = act[0]
            D = np.nonzero(Aa[k0].any(axis=1))[0]
            Dinv = group_inverse(law3.decode(D), p)
            t0q = tq[(pi, k0)]
            sinv = pow(int(sv[k0]), p-2, p)
            scale = np.array([pow(sinv, int(dg), p) for dg in degs], dtype=np.int64)
            Qs, Qps, vals = [], [], []
            qch = max(1, 2_000_000 // max(1, len(D)))
            for c0 in range(0, nQ, qch):
                qs = np.arange(c0, min(nQ, c0+qch))
                gq = law3.mul(Dinv[None, :, :], t0q[qs][:, None, :])        # t(q') = u^-1 t(q)
                ok = ~(gq[..., blk.nq:] % p).any(axis=2)
                qq, uu = np.nonzero(ok)
                gsel = gq[qq, uu]
                qprime = (-gsel[:, :blk.nq]*scale) % p
                qpi = law2.encode(qprime)
                v = Aa[k0][D[uu]]
                for o in range(Mk):
                    if o == k0:
                        continue
                    if sv[o] % p:
                        t1 = tq[(pi, o)]
                        u2 = law3.encode(law3.mul(t1[qs[qq]], group_inverse(t1[qpi], p)))
                        v = M.cyc_mul_rows(v, Aa[o][u2], p)
                    else:
                        v = M.cyc_mul_rows(v, np.repeat(Aa[o][:1], len(v), axis=0), p)
                nzv = M.cyc_canon(v).any(axis=1)
                Qs.append(qs[qq][nzv])
                Qps.append(qpi[nzv])
                vals.append(M.cyc_canon(v[nzv]))
            Qs, Qps, vals = np.concatenate(Qs), np.concatenate(Qps), np.concatenate(vals)
            od = np.argsort(Qs*nQ+Qps)
            rho_sig.update((Qs*nQ+Qps)[od].tobytes() + vals[od].tobytes())
            pair_ok = len(Qs) == ref_pairs and len(np.unique(Qs*nQ+Qps)) == len(Qs) and \
                bool((lc2[Qs] == lc2[Qps]).all())
            const_ok = bool((vals == vals[:1]).all()) and not vals[0, 1:].any() and vals[0, 0] > 0
            k5.append(bool(pair_ok and const_ok))
            consts.append(int(vals[0, 0]) if const_ok else None)
            if return_rows and pi < 2:
                descs.append((Qs, Qps, vals))
            if direct_gram and pi < 2:
                out.setdefault("direct_gram_equals_descriptor", []).append(
                    _direct_gram_check(keep_rows, kids, pi, desc=(Qs, Qps, vals), p=p, nQ=nQ))
    out["rho_Q2_signature"] = rho_sig.hexdigest() if k4ok else None
    ck["K5_2_rho_Q2_proportional_to_rho_H2_every_label_tuple"] = k5
    lab_ok = all(set(int(l) for l in labs[kk]) == {int(np.dot(np.array(a), p**np.arange(g3-1, -1, -1)))
                                                   for a in allowed} for kk in range(Mk))
    nv = [v for kk in range(Mk) for v in norms[kk].values()]
    lab_ok = lab_ok and all(np.array_equal(v, nv[0]) for v in nv) and not nv[0][1:].any()
    ck["K5_2_grade3_label_law_uniform_on_Kperp_power_M"] = bool(lab_ok)
    out["label_tuples"] = nT
    out["rho_Q2_scales"] = sorted(set(consts), key=lambda v: (v is None, v))
    out["H2_order"] = int(len(H2))
    # an empty list (check not reached, e.g. K5_2 after a K4 failure) is None, not True
    out["checkpoints"] = {k: ((bool(all(v)) if v else None) if isinstance(v, list) else v) for k, v in ck.items()}
    out["checkpoint_counts"] = {k: len(v) for k, v in ck.items() if isinstance(v, list)}
    out["all_checkpoints_pass"] = bool(all(out["checkpoints"].values()) and out["Q2_uniform"]
                                       and out["merge_inputs_other_wires_constant"]
                                       and out["oracle_outputs_constant_after_conditioning"]
                                       and out["reference_witness_solves"] and all(len(v) for v in ck.values()
                                                                                   if isinstance(v, list)))
    out["seconds"] = round(time.time()-t0, 1)
    out["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
    if log:
        log(json.dumps(out, default=str))
    if return_rows:
        out["_rows"] = (keep_rows, kids, rows_by_lab, labs, qv, descs)
    return out


def combine_hub_ranges(runs):
    """Combine Phase-A runs of one subgroup and node over hub ranges: valid when the
    ranges partition [0, hubs), every run passes all its checkpoints (K3 and K4 on its
    hubs) and all give the identical rho_Q2_signature. Then K4 holds on every hub and
    the K5_2 computed in each run (from the K4 descriptor) applies to the whole node."""
    keys = {(r["name"], r["node"], r["hubs"], r.get("coset_x0")) for r in runs}
    rs = sorted(runs, key=lambda r: r["hub_range"][0])
    H = rs[0]["hubs"] if rs else 0
    edges = [r["hub_range"] for r in rs]
    partition = bool(rs) and edges[0][0] == 0 and edges[-1][1] == H and \
        all(a[1] == b[0] for a, b in zip(edges, edges[1:])) and all(a[0] < a[1] for a in edges)
    sigs = {r.get("rho_Q2_signature") for r in rs}
    ok = len(keys) == 1 and partition and all(r["all_checkpoints_pass"] for r in rs) and len(sigs) == 1 \
        and None not in sigs
    return {"name": rs[0]["name"] if rs else None, "node": rs[0]["node"] if rs else None, "hubs": H,
            "hub_ranges": edges, "ranges_partition_all_hubs": partition, "same_instance_and_node": len(keys) == 1,
            "every_range_passes": all(r["all_checkpoints_pass"] for r in rs),
            "rho_Q2_signature_identical": len(sigs) == 1 and None not in sigs,
            "combined_all_checkpoints_pass_every_hub": bool(ok)}


def _direct_gram_check(keep_rows, kids, pi, desc, p, nQ, n_rows=48, seed=0):
    """Independent computation of rows of rho_Q2 for label tuple pi directly from
    the simulated output rows, without the descriptor: for each sampled q (q = 0
    and n_rows-1 random ones; all q when nQ <= n_rows) and every q', the entry
    prod_i <c_i(q')|c_i(q)> with each inner product summed over equal basis keys
    of the stored rows of child i; compared with the descriptor's entries in
    those rows. Memory is linear in the stored rows."""
    rng = np.random.default_rng(seed)
    qs = np.arange(nQ) if nQ <= n_rows else np.unique(np.concatenate(
        [[0], rng.choice(nQ, n_rows-1, replace=False)]))
    rows = {int(q): None for q in qs}
    for kk in range(len(kids)):
        H_, X_, A_ = [], [], []
        for h0, h1, rr in keep_rows:
            hrow, src, xo = rr[kk]
            sel = (hrow // nQ) == pi
            H_.append(hrow[sel] % nQ)
            X_.append(xo[sel])
            A_.append(kids[kk]["amp"][src[sel]])
        q = np.concatenate(H_)
        xk = np.concatenate(X_)
        amp = np.concatenate(A_)
        key = np.zeros(len(xk), dtype=np.int64)
        for j in range(xk.shape[1]):
            key = key*p+xk[:, j]
        order = np.argsort(key, kind="stable")
        key, q, amp = key[order], q[order], amp[order]
        for qa in rows:
            ia = np.nonzero(q == qa)[0]
            lo = np.searchsorted(key, key[ia], side="left")
            hi = np.searchsorted(key, key[ia], side="right")
            cnt = hi-lo
            ra = np.repeat(ia, cnt)
            rb = np.concatenate([np.arange(l_, h_) for l_, h_ in zip(lo, hi)]) if len(ia) else np.zeros(0, np.int64)
            v = M.cyc_mul_rows(amp[ra], M.cyc_conj(amp[rb]), p)          # <c(q_b)|c(q_a)>
            acc = np.zeros((nQ, p), dtype=np.int64)
            np.add.at(acc, q[rb], v)
            acc = M.cyc_canon(acc)
            rows[qa] = acc if rows[qa] is None else M.cyc_canon(M.cyc_mul_rows(rows[qa], acc, p))
    Qs, Qps, vals = desc
    ok = True
    for qa, r in rows.items():
        nz = np.nonzero(r.any(axis=1))[0]
        sel = Qs == qa
        d_q, d_v = Qps[sel], vals[sel]
        o = np.argsort(d_q)
        ok &= bool(np.array_equal(nz, d_q[o]) and np.array_equal(r[nz], d_v[o]))
    return ok


# ====================================================================== Phase B (root)

def _coset_factor(st, cfg, d, regs, idx):
    """Put the uniform superposition over the group elements idx on regs (one new exact factor)."""
    nb = cfg.enc.nb
    law = cfg.laws[d]
    vals = law.decode(np.asarray(idx, dtype=np.int64))
    bits = values_to_bits(vals, len(regs), nb)
    cols = {w: M._pack(bits[:, c_]) for c_, w in enumerate(M._wires(regs))}
    for w in cols:
        if st.owner[w] >= 0 or st.cval[w]:
            raise AssertionError("wire not fresh")
    amp = np.zeros((len(idx), cfg.p), dtype=np.int64)
    amp[:, 0] = 1
    st._new_factor(len(idx), cols, amp)
    st.split_constants(list(cols))


def _content(a):
    """Integer content (gcd of all coefficients) of an integer array; 0 for the zero array."""
    g = 0
    for v in np.unique(np.abs(np.asarray(a, dtype=object)).ravel()):
        g = math.gcd(g, int(v))
        if g == 1:
            break
    return g


def cyc_mul_rows_exact(a, b, p):
    """cyc_mul_rows for int64 or Python-int (object) arrays, never overflowing:
    switches to object dtype when the int64 bound p*max|a|*max|b| < 2^62 fails."""
    ma, mb = int(np.abs(a).max(initial=0)), int(np.abs(b).max(initial=0))
    if a.dtype != object and b.dtype != object and p*ma*mb < (1 << 62):
        return M.cyc_mul_rows(a, b, p)
    a, b = np.asarray(a, dtype=object), np.asarray(b, dtype=object)
    out = np.zeros(np.broadcast_shapes(a.shape, b.shape), dtype=object)
    for i in range(p):
        ai = a[..., i:i+1]
        if ai.any():
            out = out + np.roll(ai*b, i, axis=-1)
    return M.cyc_canon(out)


def total_gram_exact(hs):
    """HubState.total_gram without overflow: each factor's Gram matrix is divided
    by its integer content (a positive common scalar, so the law and every
    proportionality check are unchanged) and the product is taken in Python
    integers when int64 would not suffice."""
    p = hs.p
    G = M.cyc_mul_rows(hs.hamp[:, None, :], M.cyc_conj(hs.hamp)[None, :, :], p)
    for fid in hs.F:
        Gf = hs.gram(fid)
        g = _content(Gf)
        if g > 1:
            Gf = Gf // g
        G = cyc_mul_rows_exact(G, Gf, p)
    g = _content(G)
    if g > 1:
        G = G // g
    if G.dtype == object and int(np.abs(G).max(initial=0)) < (1 << 62):
        G = G.astype(np.int64)
    return G


def law_signature(probs):
    """SHA-256 of the law as a primitive integer vector (divided by the content of
    all values): equal for two laws exactly when they are proportional."""
    keys = sorted(probs)
    g = _content(np.stack([np.asarray(probs[k], dtype=object) for k in keys])) if keys else 1
    rows = [(k, tuple(int(x)//g for x in probs[k])) for k in keys]
    return hashlib.sha256(repr(rows).encode()).hexdigest()


def phase_b(ts, inst, steps, an, *, cosets=None, label_tuple=None, checks=True, max_rows=8_000_000, log=None,
            return_state=False):
    """Phase B (see the module docstring). cosets: per grade-2 child an element g
    (index in G_2) whose left coset gH_2 replaces Q_2 (default e). label_tuple:
    None (all grade-2 labels kept; feasible when K_2^perp = 0) or a tuple of six
    label indices on which the grade-2 labels are conditioned (exact projector)."""
    cfg, p = ts.cfg, ts.p
    nb = cfg.enc.nb
    law2, law1 = cfg.laws[2], cfg.laws[1]
    t0 = time.time()
    table = None
    H2 = G.stage_indices(cfg, inst.log_h, 2)
    kids_n = [n["node"] for n in an["nodes"]]
    cosets = cosets or [0]*len(kids_n)
    st = M.FactorState(ts.nw, p, max_rows=max_rows, max_bytes=4e9)
    coset_idx = []
    for k, g in zip(kids_n, cosets):
        gidx = np.sort(law2.encode(law2.mul(law2.decode(np.full(len(H2), g)), law2.decode(H2))))
        coset_idx.append(gidx)
        _coset_factor(st, cfg, 2, k["reg"], gidx)
    out = {"name": inst.name, "normal": bool(inst.normal), "cosets": [int(g) for g in cosets],
           "label_tuple": None if label_tuple is None else
           [[int(v) for v in np.atleast_1d(x)] for x in label_tuple]}
    work = an["work"]
    ck = {"K0_workspace_clean": [], "K2_grade2_instrument_equals_reference": []}
    order = []
    for n in an["nodes"]:
        order += list(range(n["inst"][0], n["inst"][1]+1))
    split, final = an["root"]["split"], an["root"]["final"]
    order += [i for i in an["root"]["steps"] if i <= split]
    inst_end = {n["inst"][1]: n["j"] for n in an["nodes"]}
    for i in order:
        kind, payload, comp, nc, _ = steps[i]
        if kind == "perm":
            st.run(payload)
            st.split_constants(nc)
        elif kind in ("qft", "qft_dg"):
            st.qft(payload, inverse=(kind == "qft_dg"))
        else:
            raise ValueError(kind)
        if i in inst_end:
            jj = inst_end[i]
            ck["K0_workspace_clean"].append(all(st.owner[w] < 0 and st.cval[w] == 0 for w in work))
            if checks:
                ck["K2_grade2_instrument_equals_reference"].append(
                    _instrument_check(st, cfg, 2, kids_n[jj]["reg"], kids_n[jj]["z"], coset_idx[jj]))
    g2 = cfg.dims[1]
    # label law of each child after its instrument (uniform on K_2^perp)
    allowed = set(G.allowed_labels(cfg, inst.log_h, 2))
    lab_ok = True
    lab_sets = []
    for k in kids_n:
        xv, lam, amp = _child_rows(st, cfg, 2, k["reg"], k["z"])
        tl = [tuple(int(v) for v in r) for r in lam]
        nrm = {}
        for t, a in zip(tl, M.cyc_norm2(amp, p)):
            nrm[t] = nrm[t]+a if t in nrm else a.copy()
        vals = [M.cyc_canon(v) for v in nrm.values()]
        lab_ok &= set(nrm) == allowed and all(np.array_equal(v, vals[0]) for v in vals) and not vals[0][1:].any()
        lab_sets.append(sorted(nrm))
    ck["K2_grade2_label_law_uniform_on_Kperp"] = [bool(lab_ok)]
    if label_tuple is not None:
        for k, lt in zip(kids_n, label_tuple):
            lt = tuple(int(v) for v in lt)
            zw = M._wires(k["z"])
            fid = st._unify(zw)
            if fid is None:
                if tuple(st.const_value(q) for q in k["z"]) != lt:
                    raise ValueError("label tuple has probability 0")
                continue
            vals = np.stack([st.values(fid, list(q)) for q in k["z"]], axis=1)
            keep = (vals == np.array(lt)[None, :]).all(axis=1)
            if not keep.any():
                raise ValueError("label tuple has probability 0")
            st._select(fid, keep)
    # ---- hub split over (grade-2 labels, Q_1) and the root merge segment
    kids = [(k["reg"], [], k["z"]) for k in kids_n]
    label_wires = [w for k in kids_n for w in M._wires(k["z"])]
    q_wires = M._wires(ts.root)
    hub_wires = label_wires+q_wires
    hs = M.HubState.split(st, hub_wires, max_rows=max_rows)
    del st
    out["hubs"] = hs.H
    lab0 = {w: hs.hub[w].copy() for w in hub_wires}
    child_w = [M._wires(a) for a, _, _ in kids]
    pre = [M.hub_joint_rows(hs, w) for w in child_w]
    blk = ts.blocks[2]
    lam_ref = np.stack([np.stack([sum(lab0[w].astype(np.int64) << b for b, w in enumerate(q)) for q in z], axis=1)
                        for _, _, z in kids], axis=2)
    s_ref = C.sde_reference(p, 2, lam_ref)
    s64 = np.asarray(s_ref, dtype=np.int64)
    ck["K4_reference_witness_solves_sum_s2_lambda_eq_0"] = [bool(
        (s64 % p != 0).any(axis=1).all() and not (np.einsum("hgm,hm->hg", lam_ref.astype(np.int64), s64*s64) % p).any())]
    q_ref = np.stack([sum(lab0[w].astype(np.int64) << b for b, w in enumerate(q)) for q in ts.root], axis=1)

    def translated(ci):
        post = M.hub_joint_rows(hs, child_w[ci])
        if post is None or pre[ci] is None:
            return False
        h0, B0, A0 = pre[ci]
        a = kids[ci][0]
        X = M._bits_to_values(B0[:, :len(a)*nb], nb, len(a))
        Xn = law2.mul(X, C._witness_bound_g(blk, s_ref[:, ci], q_ref)[h0])
        Bn = B0.copy()
        for jj in range(len(a)):
            for bit in range(nb):
                Bn[:, jj*nb+bit] = (Xn[:, jj] >> bit) & 1
        ke, ae = M._sorted_table(h0, Bn, A0)
        ka, aa = M._sorted_table(*post)
        return bool(np.array_equal(ke, ka) and M._unit_ratio(aa, ae, p))
    bounds = [i for i in range(split+1, final) if i+1 == final or steps[i+1][2] != steps[i][2]]
    wc_ends = [i for i in bounds if steps[i][2].startswith("witness_control")][1:]
    if len(wc_ends) != len(kids):
        raise AssertionError("witness-control boundaries")
    child_end = {i: ci for ci, i in enumerate(wc_ends)}
    ck["K3_workspace_unentangled_at_each_merge_component_boundary"] = []
    ck["K3_child_translated_after_its_own_merge"] = []
    i = split
    try:
        for i in range(split+1, final):
            kind, payload, comp, nc, _ = steps[i]
            if kind != "perm":
                raise ValueError("non-permutation step in the root merge")
            hs.run(payload)
            hs.split_constants(nc)
            if checks and i in bounds:
                ck["K3_workspace_unentangled_at_each_merge_component_boundary"].append(
                    all(hs.owner[w] < 0 for w in work))
                if i in child_end:
                    ck["K3_child_translated_after_its_own_merge"].append(translated(child_end[i]))
    except M.BudgetExceeded as e:
        out.update({"budget_exceeded": str(e)[:160], "budget_exceeded_at_step": i, "law_computed": False,
                    "checkpoints": {k: (bool(all(v)) if isinstance(v, list) else v) for k, v in ck.items()},
                    "all_checkpoints_pass": False, "seconds": round(time.time()-t0, 1)})
        return out
    hub_ok = all(hs.owner[w] < 0 for w in hub_wires)
    out["labels_and_Q1_unchanged"] = bool(hub_ok and all(np.array_equal(hs.hub[w], lab0[w]) for w in hub_wires))
    out["workspace_and_witness_clean_every_hub"] = bool(all(hs.owner[w] < 0 and not hs.hub[w].any() for w in work))
    ck["K4_children_equal_reference_translation_every_hub"] = [translated(ci) for ci in range(len(kids))]
    out["hub_joins"] = hs.joins
    out["hub_peak_rows"] = int(hs.peak_rows)
    if not hub_ok:
        out.update({"law_computed": False, "all_checkpoints_pass": False,
                    "checkpoints": {k: (bool(all(v)) if isinstance(v, list) else v) for k, v in ck.items()}})
        return out
    out["final_state_signature"] = M.state_signature(hs)
    # ---- exact readout law and K5
    Gt = total_gram_exact(hs)
    sig_w = [w for w in range(ts.nw) if hs.owner[w] < 0 and w not in set(q_wires)]
    sig = np.stack([hs.hub[w] for w in sig_w], axis=1) if sig_w else np.zeros((hs.H, 0), dtype=np.uint8)
    _, grp = np.unique(sig, axis=0, return_inverse=True)
    grp = grp.ravel()
    same = grp[:, None] == grp[None, :]
    Gt[~same] = 0
    qc = np.stack([hs.value(list(q)) for q in ts.root], axis=1)
    E = law1.elements()
    # P(y) = sum_(h,h') zeta^(y.(q_h - q_h')) Gt[h,h'] = sum_d zeta^(y.d) W(d), W(d) = sum_(q_h - q_h' = d) Gt
    dq = law1.encode((qc[:, None, :]-qc[None, :, :]) % p)
    W = np.zeros((law1.order, p), dtype=Gt.dtype)
    np.add.at(W, dq.ravel(), Gt.reshape(-1, p))
    del dq
    probs = {}
    for y in E:
        e = (E @ y) % p
        tot = np.zeros(p, dtype=Gt.dtype)
        for k in range(p):
            msk = e == k
            if msk.any():
                tot += np.roll(W[msk].sum(axis=0), k)
        tot = M.cyc_canon(tot)
        if tot.any():
            probs[tuple(int(v) for v in y)] = tot
    hp = M.h_perp(cfg, inst.log_h)
    vals = list(probs.values())
    rational = all(not v[1:].any() for v in vals)
    out["readout_law_rational"] = bool(rational)
    out["support_equals_h_perp"] = set(probs) == hp
    out["exact_law_uniform_on_h_perp"] = bool(set(probs) == hp and rational and
                                               all(np.array_equal(v, vals[0]) for v in vals))
    out["law_support_size"] = len(probs)
    out["h_perp_size"] = len(hp)
    out["law_signature"] = law_signature(probs)
    tgt, _ = C.rho_target(cfg, inst.log_h, 1)
    R = np.zeros(tgt.shape+(p,), dtype=Gt.dtype)
    R[..., 0] = tgt
    qidx = law1.encode(qc)
    per, rho_all = [], np.zeros_like(R)
    # group the hubs by the grade-2 label values only (Gt is already 0 between orthogonal hubs)
    labv = np.stack([hs.hub[w] for w in label_wires], axis=1) if label_wires else np.zeros((hs.H, 0), np.uint8)
    _, lgrp = np.unique(labv, axis=0, return_inverse=True)
    lgrp = lgrp.ravel()
    for gval in range(int(lgrp.max())+1):
        hsel = np.nonzero(lgrp == gval)[0]
        rho = np.zeros_like(R)
        sub = Gt[np.ix_(hsel, hsel)]
        np.add.at(rho, (qidx[hsel][:, None].repeat(len(hsel), 1), qidx[hsel][None, :].repeat(len(hsel), 0)), sub)
        rho = M.cyc_canon(rho)
        rho_all += rho
        per.append(M.proportional(rho, R))
    ck["K5_rho_Q1_proportional_to_rho_H1_every_label_tuple"] = [bool(all(per))]
    ck["K5_rho_Q1_proportional_to_rho_H1_total"] = [M.proportional(M.cyc_canon(rho_all), R)]
    out["label_tuples_in_hubs"] = int(lgrp.max())+1
    out["orthogonality_classes_of_hubs"] = int(grp.max())+1
    # an empty list (check not reached, e.g. K5_2 after a K4 failure) is None, not True
    out["checkpoints"] = {k: ((bool(all(v)) if v else None) if isinstance(v, list) else v) for k, v in ck.items()}
    out["checkpoint_counts"] = {k: len(v) for k, v in ck.items() if isinstance(v, list)}
    out["all_checkpoints_pass"] = bool(all(v is True for v in out["checkpoints"].values())
                                       and out["labels_and_Q1_unchanged"]
                                       and out["workspace_and_witness_clean_every_hub"])
    out["law_computed"] = True
    if rational:
        tot = sum(int(v[0]) for v in vals)
        out["law_mass_per_point"] = str(Fraction(int(vals[0][0]), tot)) if out["exact_law_uniform_on_h_perp"] else None
    out["seconds"] = round(time.time()-t0, 1)
    out["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
    if return_state:
        out["_probs"] = probs
    if log:
        log(json.dumps(out, default=str))
    return out


# ====================================================================== the whole terminal sample

def setup(job_name="n4_f5", mutate_block=None):
    if job_name == "n4_f7":
        return setup_f7()
    cfg, insts = M.job(job_name)
    if mutate_block:
        orig = C.MergeBlock
        C.MergeBlock = lambda cfg_, d, mutate=None, _m=mutate_block: orig(cfg_, d, mutate={_m})
        try:
            ts = C.TerminalSample(cfg)
        finally:
            C.MergeBlock = orig
    else:
        ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    an = anatomy(ts, steps)
    return cfg, insts, ts, steps, an


def setup_f7():
    """n4(F_7): the fifth backend (kappa_3 = 3; merge arities M_3 = 3, M_2 = 6).
    Every call that builds a block or reads the reference witness must run
    inside K.kappa_dispatch() (see dispatch())."""
    import theorems.rees_circuit_coherent_k3 as K
    cfg = K.job_config("n4_f7")
    ts = K.TerminalSampleK(cfg)
    steps = M.compile_program(ts)
    an = anatomy(ts, steps)
    return cfg, G.n4_instances(7), ts, steps, an


def dispatch():
    """Context manager routing C.sde_reference to the kappa >= 3 reference (n4(F_7))."""
    import theorems.rees_circuit_coherent_k3 as K
    return K.kappa_dispatch()


def exact_c3(ts, inst, steps, an, *, all_nodes=True, label_tuples=None, chunk_rows=3_000_000, log=None):
    """Phase A on every grade-2 node (or node 0 plus the relabeling check), then
    Phase B: the exact law when K_2^perp = 0, else conditionally on label_tuples."""
    cfg = ts.cfg
    out = {"name": inst.name, "normal": bool(inst.normal), "anatomy_ok": an["ok"]}
    nodes = range(len(an["nodes"])) if all_nodes else [0]
    A = []
    for j in nodes:
        A.append(phase_a(ts, inst, steps, an, j, chunk_rows=chunk_rows, log=log))
    out["phase_a"] = A
    if not all_nodes:
        out["relabeling"] = subtree_relabeling_check(ts, steps, an)
    okA = all(a["all_checkpoints_pass"] for a in A)
    out["phase_a_all_pass"] = okA
    K2 = len(G.allowed_labels(cfg, inst.log_h, 2))
    out["K2perp_size"] = K2
    out["phase_b"] = []
    if not okA:
        return out
    if K2 == 1:
        out["phase_b"].append(phase_b(ts, inst, steps, an, log=log))
        out["exact_law_of_whole_terminal_sample"] = True
    else:
        for lt in (label_tuples or []):
            out["phase_b"].append(phase_b(ts, inst, steps, an, label_tuple=lt, log=log))
        out["exact_law_of_whole_terminal_sample"] = False
    return out


def label_tuple_choices(cfg, inst, n_random=2, seed=0):
    """The zero tuple and n_random random tuples of allowed grade-2 labels."""
    allowed = G.allowed_labels(cfg, inst.log_h, 2)
    rng = np.random.default_rng(seed)
    M2 = cfg.arity[2]
    out = [tuple(tuple(0 for _ in allowed[0]) for _ in range(M2))]
    for _ in range(n_random):
        out.append(tuple(tuple(allowed[int(rng.integers(len(allowed)))]) for _ in range(M2)))
    return out


def report(names=None, out_path=None, all_nodes=True, n_random=2, chunk_rows=3_000_000, log=print):
    cfg, insts, ts, steps, an = setup("n4_f5")
    res = {**STATUS, "config": cfg.name(), "qubits": ts.nw, "anatomy_ok": an["ok"],
           "relabeling": subtree_relabeling_check(ts, steps, an), "runs": []}
    for inst in insts:
        if names and not any(inst.name.endswith("H="+n) for n in names):
            continue
        lts = label_tuple_choices(cfg, inst, n_random=n_random)
        r = exact_c3(ts, inst, steps, an, all_nodes=all_nodes, label_tuples=lts, chunk_rows=chunk_rows, log=log)
        res["runs"].append(r)
        res["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(res, fh, indent=1, default=str)
    return res


def _dump(obj, path):
    if path:
        with open(path, "w") as fh:
            json.dump(obj, fh, indent=1, default=str)


def run_cli(mode, names, out, *, job="n4_f5", nodes=(0,), coset_x0=0, hub_range=None, direct_gram=False,
            tuples=("zero",), n_random=2, cosets=None, seed=0, chunk_rows=3_000_000, sources_only=False,
            phase="A", part=None, mutate_oracle=False, log=print):
    """One guarded run for the report; results are written to `out` after every item."""
    import contextlib
    res = {**STATUS, "mode": mode, "job": job, "runs": []}
    if mode == "heis":
        return heis_reduction_check(names=names, out_path=out, log=log)
    if mode == "neg":
        lt = None
        if "random" in tuples:                     # Phase B controls on a random nonzero grade-2 label tuple
            cfg_, insts_ = M.job(job)
            inst_ = [i for i in insts_ if i.name.endswith("H="+names[0])][0]
            lt = label_tuple_choices(cfg_, inst_, n_random=1, seed=seed)[1]
        return negative_controls_c3(name=names[0], phase=phase, out_path=out, log=log, part=part, label_tuple=lt)
    t0 = time.time()
    cfg, insts, ts, steps, an = setup(job)
    ctx = dispatch() if job == "n4_f7" else contextlib.nullcontext()
    res.update({"config": cfg.name(), "qubits": ts.nw, "steps": len(steps), "anatomy_ok": an["ok"],
                "setup_seconds": round(time.time()-t0, 1)})
    if mode == "relabel":
        res["relabeling"] = subtree_relabeling_check(ts, steps, an)
        res["lemma_hypotheses"] = lemma_hypotheses_check(ts, steps, an)
        _dump(res, out)
        return res
    if mode == "merge":
        with ctx:
            for d in sorted(ts.blocks):
                t1 = time.time()
                pr = C.prove_controlled_merge(ts.blocks[d])
                bs = C.block_structure(ts.blocks[d])
                res["runs"].append({"grade": d, "prove_controlled_merge": pr, "block_structure": bs,
                                    "seconds": round(time.time()-t1, 1)})
                _dump(res, out)
        return res
    rng = np.random.default_rng(seed)
    with ctx:
        for inst in insts:
            if names and not any(inst.name.endswith("H="+n) for n in names):
                continue
            if mutate_oracle:                             # negative control: one changed oracle entry
                bad = copy.copy(inst)
                tab = np.array(inst.oracle_table).copy()
                xm = int(np.nonzero(tab != tab[0])[0][0])
                tab[xm] = tab[0]
                bad.oracle_table = tab
                inst = bad
                res.setdefault("oracle_mutants", []).append({"name": inst.name, "x0": xm})
            if mode == "A":
                x0 = coset_x0
                if x0 is not None and x0 < 0:            # a random address outside exp(h~)
                    S3 = set(G.stage_indices(cfg, inst.log_h, 3).tolist())
                    cand = [x for x in range(cfg.laws[3].order) if x not in S3]
                    x0 = int(rng.choice(cand))
                for j in nodes:
                    r = phase_a(ts, inst, steps, an, j, coset_x0=x0, chunk_rows=chunk_rows, hub_range=hub_range,
                                direct_gram=direct_gram, return_rows=direct_gram, sources_only=sources_only)
                    r.pop("_rows", None)
                    res["runs"].append(r)
                    if log:
                        log(json.dumps({k: r.get(k) for k in ("name", "node", "all_checkpoints_pass", "seconds",
                                                               "max_rss_MB")}), flush=True)
                    _dump(res, out)
            elif mode == "B":
                K2 = len(G.allowed_labels(cfg, inst.log_h, 2))
                cs = None
                if cosets == "random":
                    cs = [int(v) for v in rng.integers(cfg.laws[2].order, size=len(an["nodes"]))]
                if K2 == 1:
                    lts = [None]
                else:
                    allc = label_tuple_choices(cfg, inst, n_random=n_random, seed=seed)
                    lts = [allc[0]] if "zero" in tuples else []
                    lts += allc[1:] if "random" in tuples else []
                for lt in lts:
                    r = phase_b(ts, inst, steps, an, cosets=cs, label_tuple=lt)
                    res["runs"].append(r)
                    if log:
                        log(json.dumps({k: r.get(k) for k in ("name", "label_tuple", "cosets", "all_checkpoints_pass",
                                                               "law_signature", "seconds")}), flush=True)
                    _dump(res, out)
            else:
                raise ValueError(mode)
    res["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
    res["seconds"] = round(time.time()-t0, 1)
    _dump(res, out)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="report", choices=["report", "A", "B", "heis", "neg", "relabel", "merge"])
    ap.add_argument("--job", default="n4_f5")
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--nodes", nargs="*", type=int, default=[0])
    ap.add_argument("--coset-x0", type=int, default=0, help="-1: a random address outside exp(h~)")
    ap.add_argument("--hub-range", nargs=2, type=int)
    ap.add_argument("--direct-gram", action="store_true")
    ap.add_argument("--sources-only", action="store_true")
    ap.add_argument("--mutate-oracle", action="store_true", help="negative control: one changed oracle entry")
    ap.add_argument("--tuples", nargs="*", default=["zero"])
    ap.add_argument("--cosets", default=None)
    ap.add_argument("--phase", default="A")
    ap.add_argument("--part", nargs=2, type=int, help="k n: run the mutants with index = k mod n")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--node0-only", action="store_true")
    ap.add_argument("--n-random", type=int, default=2)
    ap.add_argument("--chunk-rows", type=int, default=3_000_000)
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.mode == "report":
        report(a.names, a.out, all_nodes=not a.node0_only, n_random=a.n_random, chunk_rows=a.chunk_rows)
        return
    run_cli(a.mode, a.names, a.out, job=a.job, nodes=a.nodes, coset_x0=a.coset_x0, hub_range=a.hub_range,
            direct_gram=a.direct_gram, tuples=a.tuples, n_random=a.n_random, cosets=a.cosets, seed=a.seed,
            chunk_rows=a.chunk_rows, sources_only=a.sources_only, phase=a.phase,
            part=tuple(a.part) if a.part else None, mutate_oracle=a.mutate_oracle)




# ====================================================================== validation of the reduction at c = 2

def heis_reduction_check(names=None, x0s=(0, None), seed=3, out_path=None, log=print):
    """For Heis(F_3) (c = 2): the exact level-0 law of round 2 (nothing measured,
    no reduction) against the same computation with every source's oracle
    outputs conditioned on one coset (x0 = 0: the identity coset; None: a random
    address outside exp(h~)). The coset-symmetry reduction predicts equal laws."""
    cfg, insts = M.job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = M.compile_program(ts)
    rng = np.random.default_rng(seed)
    res = {**STATUS, "job": "heis_f3", "rows": []}
    for inst in insts:
        if names and not any(inst.name.endswith("H="+n) for n in names):
            continue
        t0 = time.time()
        base = M.exact_level0_law(ts, inst, steps)
        row = {"name": inst.name, "base_all_checkpoints_pass": base["all_checkpoints_pass"],
               "base_failed_checkpoints": sorted(k for k, v in base.get("checkpoints", {}).items() if v is False),
               "base_uniform": base["exact_law_uniform_on_h_perp"], "conditioned": []}
        S = set(G.stage_indices(cfg, inst.log_h, 2).tolist())
        for x0 in x0s:
            if x0 is None:
                cand = [x for x in range(cfg.laws[2].order) if x not in S]
                if not cand:
                    continue
                x0 = int(rng.choice(cand))
            r = M.exact_level0_law(ts, inst, steps, condition_sources=x0)
            L1 = {k: np.array([v]+[0]*(cfg.p-1)) for k, v in (base["law"] or {}).items()}
            L2 = {k: np.array([v]+[0]*(cfg.p-1)) for k, v in (r["law"] or {}).items()}
            row["conditioned"].append({"x0": x0, "law_equal_to_unreduced": bool(base["law"] is not None and
                                                                               M.laws_proportional(L1, L2, cfg.p)),
                                       "checkpoints_pass": r["all_checkpoints_pass"],
                                       "failed_checkpoints": sorted(k for k, v in r.get("checkpoints", {}).items()
                                                                    if v is False),
                                       "K5_rho_Q_per_label_tuple": r.get("checkpoints", {}).get(
                                           "K5_rho_Q_proportional_to_rho_H1_every_label_tuple"),
                                       "hub_peak_rows": r.get("hub_peak_rows"),
                                       "unreduced_hub_peak_rows": base.get("hub_peak_rows")})
        row["seconds"] = round(time.time()-t0, 1)
        res["rows"].append(row)
        if log:
            log(json.dumps(row, default=str))
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(res, fh, indent=1, default=str)
    res["all_equal"] = all(c["law_equal_to_unreduced"] for r in res["rows"] for c in r["conditioned"])
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(res, fh, indent=1, default=str)
    return res


# ====================================================================== negative controls at c = 3

def drop_gate_at(steps, i, gate_kind, position):
    """Drop one gate of kind gate_kind ('first' or 'middle' of that kind) in perm step i."""
    stp = [list(s) for s in steps]
    s = stp[i]
    ks = [k for k, (g, q) in enumerate(s[1]) if g == gate_kind]
    if s[0] != "perm" or not ks:
        raise LookupError(i)
    k = ks[0] if position == "first" else ks[len(ks)//2]
    gates = list(s[1])
    g, q = gates.pop(k)
    stp[i] = [s[0], gates, s[2], set(s[3]), s[4]]
    return stp, {"step": i, "component": s[2], "dropped": g, "wires": list(q), "position": position}


def _first_perm_step(steps, lo, hi, comp):
    for i in range(lo, hi+1):
        if steps[i][0] == "perm" and steps[i][2] == comp:
            return i
    raise LookupError(comp)


def _failed(r):
    return sorted(k for k, v in r.get("checkpoints", {}).items() if v is False) + \
        [k for k in ("Q2_uniform", "merge_inputs_other_wires_constant", "labels_and_Q1_unchanged",
                     "workspace_and_witness_clean_every_hub") if r.get(k) is False]


def negative_controls_c3(name="<e2> non-normal", phase="A", out_path=None, log=print, label_tuple=None, part=None):
    """Mutants of the n4(F_5) terminal sample, each run deterministically through
    Phase A (node 0: sources, grade-3 instruments, grade-3 merge) or Phase B
    (grade-2 instruments and the root merge). A mutant no check catches is
    compared with the unmutated run (final-state signature): equal = an
    equivalent mutant (the dropped gate never acts on the reachable state)."""
    cfg, insts, ts, steps, an = setup("n4_f5")
    inst = [i for i in insts if i.name.endswith("H="+name)][0]
    lt = label_tuple if label_tuple is not None else (
        None if len(G.allowed_labels(cfg, inst.log_h, 2)) == 1 else label_tuple_choices(cfg, inst, 0)[0])
    out = {**STATUS, "status": f"negative_controls_c3_phase_{phase}", "instance": inst.name, "label_tuple": lt,
           "part": part, "rows": []}

    def runA(ts_, steps_, inst_):
        an_ = anatomy(ts_, steps_)
        return phase_a(ts_, inst_, steps_, an_, 0)

    def runB(ts_, steps_, inst_):
        an_ = anatomy(ts_, steps_)
        return phase_b(ts_, inst_, steps_, an_, label_tuple=lt)
    run = runA if phase == "A" else runB
    base = run(ts, steps, inst)
    out["baseline"] = {"all_checkpoints_pass": base["all_checkpoints_pass"], "failed": _failed(base),
                       "seconds": base["seconds"]}
    if log:
        log(json.dumps(out["baseline"]))

    def dump():
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(out, fh, indent=1, default=str)

    counter = [0]

    def record(desc, ts_, steps_, inst_):
        k = counter[0]
        counter[0] += 1
        if part is not None and k % part[1] != part[0]:
            return
        t0 = time.time()
        try:
            r = run(ts_, steps_, inst_)
            failed = _failed(r)
            row = {**desc, "failed_checks": failed, "detected": bool(failed) or not r.get("all_checkpoints_pass"),
                   "seconds": round(time.time()-t0, 1)}
            if phase == "B" and r.get("law_computed"):
                row["law_uniform"] = r.get("exact_law_uniform_on_h_perp")
                if not row["law_uniform"]:
                    row["detected"] = True
            if not row["detected"]:
                row["final_state_identical_to_unmutated"] = r["final_state_signature"] == base["final_state_signature"]
        except (ArithmeticError, AssertionError, ValueError, LookupError, M.BudgetExceeded) as e:
            row = {**desc, "detected": "exception", "exception": repr(e)[:200], "seconds": round(time.time()-t0, 1)}
        out["rows"].append(row)
        if log:
            log(json.dumps(row, default=str))
        dump()
    n0 = an["nodes"][0]
    if phase == "A":
        bad = copy.copy(inst)
        tab = np.array(inst.oracle_table).copy()
        x0 = int(np.nonzero(tab != tab[0])[0][0])
        tab[x0] = tab[0]
        bad.oracle_table = tab
        record({"mutant": "oracle entry", "x0": x0}, ts, steps, bad)
        plan = [("source_evaluation", "cx", "middle"), ("source_evaluation", "ccx", "middle"),
                ("instrument", "cx", "middle")]
        plan += [(c, k, pos) for c in ("sde_grade3", "witness_control_grade3", "bch_merge_grade3")
                 for k, pos in (("cx", "first"), ("cx", "middle"), ("ccx", "middle"))]
        lo, hi = n0["A"]
    else:
        plan = [("instrument", "cx", "middle")]
        plan += [(c, k, pos) for c in ("sde_grade2", "witness_control_grade2", "bch_merge_grade2")
                 for k, pos in (("cx", "first"), ("cx", "middle"), ("ccx", "middle"))]
        lo, hi = n0["inst"][0], len(steps)-1
    for comp, kind, pos in plan:
        try:
            i = _first_perm_step(steps, lo, hi, comp)
            stp, desc = drop_gate_at(steps, i, kind, pos)
        except LookupError:
            continue
        record({"mutant": "drop gate", **desc}, ts, stp, inst)
    for mut in ("g_sign", "skip_bennett"):
        _, _, tsm, stm, _ = setup("n4_f5", mutate_block=mut)
        record({"mutant": f"MergeBlock {mut} (both grades)"}, tsm, stm, inst)
    det = [r for r in out["rows"]]
    out["summary"] = {"mutants": len(det), "caught": sum(r["detected"] is True for r in det),
                      "equivalent": sum(r.get("final_state_identical_to_unmutated") is True for r in det),
                      "missed": sum(r["detected"] is False and r.get("final_state_identical_to_unmutated") is False
                                    for r in det),
                      "exceptions": sum(r["detected"] == "exception" for r in det)}
    dump()
    return out


if __name__ == "__main__":
    main()
