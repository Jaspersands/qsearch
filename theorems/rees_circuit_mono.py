"""Monolithic simulation of the assembled coherent terminal-sample circuit.

AI-checked, pending human review. Report:
research/audits/reviews/2026-11-05-rees-receiver-sims.md.

What is simulated. The complete coherent terminal sample of
theorems/rees_circuit_coherent.TerminalSample (Heis(F_3), c = 2, 182 qubits;
n4(F_5), c = 3, 1198 qubits) is executed item by item, in program order, on
ONE joint state of all its qubits: every X/CX/CCX/SWAP of every flattened
arithmetic macro (rees_circuit_arith gate lists), every exact QFT_p and
QFT_p^dagger, every table-oracle call U_f|w>|y> = |w>|y xor f(w)>, and the
final readout. No module is simulated separately and nothing is composed
through prop:descent: the reduced states, witnesses and merges all arise
from the gates acting on the joint state.

State representation (exact). The joint state is kept as a product of
factors. Every wire is either a classical constant (a basis value shared by
all branches, e.g. |0> workspace) or a column of exactly one factor; a factor
is a sparse superposition sum_r a_r |bits_r> over its wires, with a_r an
exact element of Z[zeta_p] (integer coefficient vector, last coefficient 0
after canonicalisation) and the bits stored bit-sliced (one packed uint64
column per wire). A gate on wires of two factors merges them (tensor
product of the rows); a wire that is constant over all rows of its factor is
split off (exact: the factor is then a product with that wire). A rational
common factor of all amplitudes of a factor is divided out (irrelevant for
the probabilities, which are ratios). QFT_p on a register groups the rows
that agree on all other wires of the factor (exact keys, numpy unique) and
sums zeta^(+-xy) a_r.

Deferred measurement (exact equivalence, not an approximation). A register
may be measured in the computational basis as soon as every later item uses
its wires only as controls of X/CX/CCX gates (never as a target, never inside
a QFT, an oracle output or a measurement): a computational-basis measurement
commutes with every gate that is block diagonal in that register's basis, so
the joint law of all later outcomes is unchanged. The schedule is computed
from the flattened gate list (measurement_schedule) and checked there.
level=1 measures only registers that no later item touches at all (oracle
outputs after their call; children and their labels after the parent's
merge); level=2 also measures each instrument label right after its
QFT_p^dagger (the label wires are afterwards only CX controls inside U_SDE
and U_SDE^-1). Each measurement is SAMPLED with its Born probabilities (float
weights computed from the exact amplitudes), so one run of the circuit is
one quantum trajectory, and the readout sample has exactly the circuit's
output law. The final conditional readout law of the trajectory is computed
EXACTLY in Z[zeta_p] and compared with the uniform law on h^perp.

Round 2 (2026-11-05, report 2026-11-05-rees-receiver-round2.md): HubState and
exact_level0_law compute the EXACT output law of the whole class-2 circuit
with nothing measured before the readout (Heis(F_3), all 19 subgroups), with
checkpoints K1-K5 against module-level reference states computed from h; see
the section "round 2" below.

What this does NOT do: a 2^n statevector; an exact output law at c = 3 (there
only sampled trajectories, each exact); the explicit QFT of
lem:qft-mod (QFT_p is the exact unitary, as in the coherent backend);
kappa_d >= 3 grades; general (G, H); anything asymptotic. It flips no claim
gate: coherent_receiver_implemented stays False.
"""
from __future__ import annotations

import argparse
import json
import random
import resource
import sys
import time
from collections import Counter
from math import gcd

import numpy as np

import theorems.rees_circuit_coherent as C
import theorems.rees_circuit_general as G
from theorems.rees_coherent_sde import Macro, Prog
from theorems.rees_end_to_end_sim import nullspace, rref, span_elements

STATUS = {"status": "monolithic_trajectory_simulation_of_assembled_coherent_terminal_sample_finite_instances",
          "coherent_receiver_implemented": False, "general_instances": False, "qft_synthesised": False,
          "independent_review": False, "speedup_claim_allowed": False,
          "review": "AI-checked, pending human review"}

ONES = np.uint64(0xFFFFFFFFFFFFFFFF)


class BudgetExceeded(RuntimeError):
    pass


# ====================================================================== Z[zeta_p] helpers

def cyc_canon(a):
    return a - a[..., -1:]


def cyc_product_rows(a, b, p):
    """Row-wise products a_i * b_j for all (i, j), flattened i-major: (Na*Nb, p)."""
    Na, Nb = len(a), len(b)
    out = np.zeros((Na, Nb, p), dtype=np.int64)
    for i in range(p):
        ai = a[:, i]
        if not ai.any():
            continue
        for j in range(p):
            bj = b[:, j]
            if bj.any():
                out[:, :, (i+j) % p] += np.outer(ai, bj)
    return out.reshape(Na*Nb, p)


def cyc_norm2(a, p):
    """a * conj(a) per row, canonical (N, p)."""
    conj = a[:, (-np.arange(p)) % p]
    out = np.zeros_like(a)
    for i in range(p):
        out += np.roll(a[:, i:i+1]*conj, i, axis=1)
    return cyc_canon(out)


def cyc_to_complex(a, p):
    w = np.exp(2j*np.pi*np.arange(p)/p)
    return a.astype(np.float64) @ w


def cyc_roll_rows(a, shift, p):
    """Row r multiplied by zeta^shift[r]."""
    idx = (np.arange(p)[None, :] - shift[:, None]) % p
    return np.take_along_axis(a, idx, axis=1)


# ====================================================================== bit columns

def _mask(N):
    nwords = (N+63)//64
    m = np.full(nwords, ONES, dtype=np.uint64)
    r = N % 64
    if r:
        m[-1] = np.uint64((1 << r)-1)
    return m


def _pack(bits):
    by = np.packbits(bits.astype(np.uint8), bitorder="little")
    nwords = (len(bits)+63)//64
    out = np.zeros(nwords*8, dtype=np.uint8)
    out[:len(by)] = by
    return out.view(np.uint64)


def _unpack(col, N):
    return np.unpackbits(col.view(np.uint8), bitorder="little")[:N]


class Factor:
    __slots__ = ("N", "cols", "amp", "mask")

    def __init__(self, N, cols, amp):
        self.N, self.cols, self.amp = N, cols, amp
        self.mask = _mask(N)


# ====================================================================== the joint state

class FactorState:
    """Exact sparse joint state of nw wires over Z[zeta_p] (see module doc)."""

    def __init__(self, nw, p, max_rows=6_000_000, max_bytes=3.0e9):
        self.nw, self.p = nw, p
        self.owner = [-1]*nw
        self.cval = [0]*nw
        self.F = {}
        self._next = 0
        self.max_rows, self.max_bytes = max_rows, max_bytes
        self.peak_rows = 1
        self.peak_bytes = 0
        self.merges = 0

    # -- factor bookkeeping
    def _new_factor(self, N, cols, amp):
        fid = self._next
        self._next += 1
        self.F[fid] = Factor(N, cols, amp)
        for w in cols:
            self.owner[w] = fid
        self._note(self.F[fid])
        return fid

    def _note(self, f):
        self.peak_rows = max(self.peak_rows, f.N)
        b = f.N*(len(f.cols)/8 + 8*self.p)
        self.peak_bytes = max(self.peak_bytes, b)

    def _check_budget(self, N, ncols):
        b = N*(ncols/8 + 8*self.p)*2.5
        if N > self.max_rows or b > self.max_bytes:
            raise BudgetExceeded(f"factor of {N} rows x {ncols} wires (~{b/1e9:.2f} GB) exceeds the budget")

    def _merge(self, f1, f2):
        """Tensor product of two factors; returns the id of the result (f1)."""
        A, B = self.F[f1], self.F[f2]
        N = A.N*B.N
        self._check_budget(N, len(A.cols)+len(B.cols))
        self.merges += 1
        cols = {}
        for w, c in A.cols.items():
            cols[w] = _pack(np.repeat(_unpack(c, A.N), B.N))
        for w, c in B.cols.items():
            cols[w] = _pack(np.tile(_unpack(c, B.N), A.N))
        amp = cyc_product_rows(A.amp, B.amp, self.p)
        A.N, A.cols, A.amp, A.mask = N, cols, self._reduce(amp), _mask(N)
        for w in B.cols:
            self.owner[w] = f1
        del self.F[f2]
        self._note(A)
        return f1

    def _reduce(self, amp):
        amp = cyc_canon(amp)
        g = int(np.gcd.reduce(np.abs(amp).ravel())) if amp.size else 0
        if g > 1:
            amp //= g
        if amp.size and int(np.abs(amp).max()) > (1 << 52):
            raise OverflowError("amplitude coefficients too large for int64")
        return amp

    def _join(self, w, fid):
        """Make wire w a column of factor fid (merging factors if needed); returns fid."""
        o = self.owner[w]
        if o == fid:
            return fid
        if o < 0:
            f = self.F[fid]
            f.cols[w] = f.mask.copy() if self.cval[w] else np.zeros_like(f.mask)
            self.owner[w] = fid
            return fid
        return self._merge(fid, o)

    def _unify(self, wires):
        """One factor holding all of wires (constants join it); None if all constant."""
        fids = sorted({self.owner[w] for w in wires if self.owner[w] >= 0})
        if not fids:
            return None
        fid = fids[0]
        for o in fids[1:]:
            fid = self._merge(fid, o)
        for w in wires:
            fid = self._join(w, fid)
        return fid

    def split_constants(self, wires):
        for w in set(wires):
            fid = self.owner[w]
            if fid < 0:
                continue
            f = self.F[fid]
            c = f.cols[w]
            if not c.any():
                v = 0
            elif np.array_equal(c, f.mask):
                v = 1
            else:
                continue
            del f.cols[w]
            self.owner[w] = -1
            self.cval[w] = v
            if not f.cols:
                del self.F[fid]

    # -- permutation gates
    def x(self, t):
        fid = self.owner[t]
        if fid < 0:
            self.cval[t] ^= 1
        else:
            f = self.F[fid]
            np.bitwise_xor(f.cols[t], f.mask, out=f.cols[t])

    def cx(self, c, t):
        fc = self.owner[c]
        if fc < 0:
            if self.cval[c]:
                self.x(t)
            return
        if self.owner[t] != fc:
            fc = self._join(t, fc)
        f = self.F[fc]
        np.bitwise_xor(f.cols[t], f.cols[c], out=f.cols[t])

    def ccx(self, a, b, t):
        if self.owner[a] < 0:
            if self.cval[a]:
                self.cx(b, t)
            return
        if self.owner[b] < 0:
            if self.cval[b]:
                self.cx(a, t)
            return
        fid = self.owner[a]
        if self.owner[b] != fid:
            fid = self._merge(fid, self.owner[b])
        if self.owner[t] != fid:
            fid = self._join(t, fid)
        f = self.F[fid]
        f.cols[t] ^= f.cols[a] & f.cols[b]

    def swap(self, a, b):
        oa, ob = self.owner[a], self.owner[b]
        ca = self.F[oa].cols.pop(a) if oa >= 0 else None
        cb = self.F[ob].cols.pop(b) if ob >= 0 else None
        if ca is not None:
            self.F[oa].cols[b] = ca
        if cb is not None:
            self.F[ob].cols[a] = cb
        self.owner[a], self.owner[b] = ob, oa
        self.cval[a], self.cval[b] = self.cval[b], self.cval[a]

    def run(self, gates):
        x, cx, ccx, swap = self.x, self.cx, self.ccx, self.swap
        for name, q in gates:
            if name == "cx":
                cx(q[0], q[1])
            elif name == "ccx":
                ccx(q[0], q[1], q[2])
            elif name == "x":
                x(q[0])
            elif name == "swap":
                swap(q[0], q[1])
            else:
                raise ValueError(name)

    # -- register values
    def values(self, fid, reg):
        """Value of reg (wire list, bit i = wire i) on every row of factor fid."""
        f = self.F[fid]
        out = np.zeros(f.N, dtype=np.int64)
        for i, w in enumerate(reg):
            if self.owner[w] == fid:
                out |= _unpack(f.cols[w], f.N).astype(np.int64) << i
            elif self.cval[w]:
                out |= 1 << i
        return out

    def const_value(self, reg):
        return sum(self.cval[w] << i for i, w in enumerate(reg))

    def _select(self, fid, keep):
        f = self.F[fid]
        idx = np.nonzero(keep)[0]
        N = len(idx)
        f.cols = {w: _pack(_unpack(c, f.N)[idx]) for w, c in f.cols.items()}
        f.amp = self._reduce(f.amp[idx])
        f.N, f.mask = N, _mask(N)
        self.split_constants(list(f.cols))

    # -- QFT_p on one qudit register
    def qft(self, reg, inverse=False):
        p = self.p
        sign = -1 if inverse else 1
        if all(self.owner[w] < 0 for w in reg):
            x = self.const_value(reg)
            if x >= p:
                raise ArithmeticError("QFT on a padding word")
            y = np.arange(p, dtype=np.int64)
            amp = np.zeros((p, p), dtype=np.int64)
            amp[y, (sign*x*y) % p] = 1
            cols = {w: _pack((y >> i) & 1) for i, w in enumerate(reg)}
            for w in reg:
                self.cval[w] = 0
            self._new_factor(p, cols, self._reduce(amp))
            self.split_constants(reg)
            return
        fid = self._unify(reg)
        f = self.F[fid]
        xv = self.values(fid, reg)
        if (xv >= p).any():
            raise ArithmeticError("QFT on a padding word")
        others = [w for w in f.cols if w not in set(reg)]
        if others:
            bits = np.stack([_unpack(f.cols[w], f.N) for w in others], axis=1)
            keys = np.packbits(bits, axis=1)
            keys = np.ascontiguousarray(keys).view(np.dtype((np.void, keys.shape[1]))).ravel()
            _, first, inv = np.unique(keys, return_index=True, return_inverse=True)
            inv = inv.ravel()
        else:
            first, inv = np.array([0]), np.zeros(f.N, dtype=np.int64)
        Gn = len(first)
        self._check_budget(Gn*p, len(f.cols))
        new_amp = np.zeros((Gn, p, p), dtype=np.int64)
        for y in range(p):
            rolled = cyc_roll_rows(f.amp, (sign*xv*y) % p, p)
            np.add.at(new_amp[:, y, :], inv, rolled)
        new_amp = cyc_canon(new_amp.reshape(Gn*p, p))
        nz = new_amp.any(axis=1)
        rep = np.repeat(first, p)[nz]
        yv = np.tile(np.arange(p, dtype=np.int64), Gn)[nz]
        N = int(nz.sum())
        cols = {}
        for w in others:
            cols[w] = _pack(_unpack(f.cols[w], f.N)[rep])
        for i, w in enumerate(reg):
            cols[w] = _pack((yv >> i) & 1)
        f.N, f.cols, f.amp, f.mask = N, cols, self._reduce(new_amp[nz]), _mask(N)
        self._note(f)
        self.split_constants(list(cols))

    # -- table oracle y ^= f(w)
    def oracle(self, wreg, yreg, table, nb, m, label_bits):
        p = self.p
        fid = self._unify(list(wreg)+list(yreg)) if any(self.owner[w] >= 0 for w in wreg) else None
        if fid is None:
            word = self.const_value(wreg)
            word = np.array([word], dtype=np.int64)
        else:
            word = self.values(fid, wreg)
        ok = np.ones(len(word), dtype=bool)
        idx = np.zeros(len(word), dtype=np.int64)
        for j in range(m):
            dgt = (word >> (nb*(m-1-j))) & ((1 << nb)-1)
            ok &= dgt < p
            idx = idx*p+np.where(dgt < p, dgt, 0)
        val = np.where(ok, table[idx], 0)
        if fid is None:
            v = int(val[0])
            for bit, w in enumerate(yreg):
                if v >> bit & 1:
                    self.x(w)
            return
        f = self.F[fid]
        for bit, w in enumerate(yreg):
            f.cols[w] ^= _pack((val >> bit) & 1)
        self.split_constants(yreg)

    # -- computational-basis measurement (sampled)
    def measure(self, reg, rng):
        """Sample reg with its Born law; collapse; return (value, prob)."""
        # distinct factors are independent tensor factors: their parts of reg
        # are measured separately (the joint Born law is the product)
        fids = sorted({self.owner[w] for w in reg if self.owner[w] >= 0})
        prob = 1.0
        for fid in fids:
            part = [w for w in reg if self.owner[w] == fid]
            f = self.F[fid]
            v = self.values(fid, part)
            wts = np.abs(cyc_to_complex(f.amp, self.p))**2
            uniq, inv = np.unique(v, return_inverse=True)
            mass = np.bincount(inv.ravel(), weights=wts, minlength=len(uniq))
            mass = mass/mass.sum()
            k = int(rng.choice(len(uniq), p=mass))
            self._select(fid, inv.ravel() == k)
            prob *= float(mass[k])
        return self.const_value(reg), prob

    def live_rows(self):
        return {fid: f.N for fid, f in self.F.items()}


# ====================================================================== program preparation

def compile_program(ts):
    """Flatten the TerminalSample items. Returns a list of steps
    (kind, payload, comp) with kind in perm/qft/qft_dg/oracle/measure, and for
    every step the set of wires used other than as a control."""
    p = ts.p
    steps = []
    for comp, it in ts.items:
        if isinstance(it, Macro) or it[0] in ("x", "cx", "ccx", "swap", "swapreg"):
            gates = C.flatten(Prog([it]), p, ts.anc)
            nc = set()
            for g, q in gates:
                if g == "swap":
                    nc.update(q)
                else:
                    nc.add(q[-1])
            if steps and steps[-1][0] == "perm" and steps[-1][2] == comp and not isinstance(it, Macro) \
                    and not steps[-1][4]:
                steps[-1][1].extend(gates)
                steps[-1][3].update(nc)
            else:
                steps.append(["perm", list(gates), comp, set(nc), isinstance(it, Macro)])
        elif it[0] in ("qft", "qft_dg"):
            reg = tuple(it[1][0])
            steps.append([it[0], reg, comp, set(reg), False])
        elif it[0] == "oracle":
            wreg, yreg = it[1]
            steps.append(["oracle", (tuple(wreg), tuple(yreg)), comp, set(yreg), False])
        elif it[0] == "measure":
            regs = tuple(tuple(q) for q in it[1])
            steps.append(["measure", regs, comp, {w for q in regs for w in q}, False])
        else:
            raise ValueError(it[0])
    return steps


def _registers(ts):
    """Candidate registers for deferred measurement, with a kind tag."""
    regs = []

    def visit(node, is_root):
        if node.get("ys"):
            for y in node["ys"]:
                regs.append(("oracle_output", tuple(y)))
        if node["z"] is not None:
            for q in node["z"]:
                regs.append((f"label_grade{node['d']}", tuple(q)))
        if not is_root:
            regs.append((f"child_grade{node['d']}", tuple(w for q in node["reg"] for w in q)))
        for k in node["kids"]:
            visit(k, False)
    visit(ts.tree, True)
    return regs


def measurement_schedule(ts, steps, level=2):
    """step index -> registers measured right after it. level 1: after the
    last step touching the register at all; level 2: after the last step
    using it other than as a control; level 0: nothing (fully coherent). Also returns the check that every
    scheduled register is afterwards used only as controls (level 2) or not
    at all (level 1)."""
    last_nc, last_any = {}, {}
    for i, (kind, payload, comp, nc, _) in enumerate(steps):
        for w in nc:
            last_nc[w] = i
        if kind == "perm":
            for _, q in payload:
                for w in q:
                    last_any[w] = i
        elif kind == "oracle":
            for w in payload[0]+payload[1]:
                last_any[w] = i
        else:
            for w in nc:
                last_any[w] = i
    sched = {}
    final = len(steps)-1
    if level == 0:                      # nothing measured before the readout
        return sched, True
    for kind, reg in _registers(ts):
        last = last_any if (level == 1 or not kind.startswith("label")) else last_nc
        t = max(last.get(w, -1) for w in reg)
        if t < 0 or t >= final:
            continue
        sched.setdefault(t, []).append((kind, reg))
    # verification: after t, no wire of reg is used other than as a control
    ok = True
    for t, lst in sched.items():
        wires = {w for _, reg in lst for w in reg}
        for kind, payload, comp, nc, _ in steps[t+1:]:
            if nc & wires:
                ok = False
        if level == 1:
            for kind, payload, comp, nc, _ in steps[t+1:]:
                used = set()
                if kind == "perm":
                    used = {w for _, q in payload for w in q}
                elif kind == "oracle":
                    used = set(payload[0]+payload[1])
                else:
                    used = nc
                if used & wires:
                    ok = False
    return sched, ok


# ====================================================================== one terminal sample

def h_perp(cfg, log_h):
    """h^perp in F_p^m (grade-one readout space) as a set of tuples."""
    p, m = cfg.p, cfg.m
    basis = nullspace([list(v) for v in log_h], m, p) if log_h else [[int(i == j) for j in range(m)] for i in range(m)]
    return {tuple(int(x) for x in v) for v in span_elements(basis, m, p)}


def run_terminal_sample(ts, inst, steps, sched, rng, *, max_rows=6_000_000, max_bytes=3.0e9, log=None,
                        source_check=False):
    cfg, p = ts.cfg, ts.p
    nb, m = cfg.enc.nb, cfg.m
    table = np.asarray(inst.oracle_table, dtype=np.int64)
    st = FactorState(ts.nw, p, max_rows=max_rows, max_bytes=max_bytes)
    t0 = time.time()
    counts = Counter()
    measured = Counter()
    readout = None
    src_checks = []
    if source_check:                     # round 2: checkpoint KS after every top-grade source
        src_at = source_check_points(ts, steps)
        cids = _left_coset_ids(cfg.laws[cfg.c], G.stage_indices(cfg, inst.log_h, cfg.c))
        work_w = [w for w in range(ts.nw) if ts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool")]
    for i, (kind, payload, comp, nc, _) in enumerate(steps):
        if kind == "perm":
            st.run(payload)
            st.split_constants(nc)
            counts["gates"] += len(payload)
        elif kind in ("qft", "qft_dg"):
            st.qft(payload, inverse=(kind == "qft_dg"))
            counts[kind] += 1
        elif kind == "oracle":
            st.oracle(payload[0], payload[1], table, nb, m, cfg.label_bits)
            counts["oracle_calls"] += 1
        elif kind == "measure":
            readout = payload
        if source_check and i in src_at:          # source complete, before any of its measurements
            a_regs, y_regs = src_at[i]
            src_checks.append(source_coset_check(st, cfg, a_regs, y_regs, cids, work_w))
        for tag, reg in sched.get(i, ()):
            st.measure(reg, rng)
            measured[tag.split("_grade")[0]] += 1
    # final readout law of this trajectory, exactly
    regs = [list(q) for q in readout]
    allw = [w for q in regs for w in q]
    fid = st._unify(allw)
    clean = all(st.owner[w] < 0 and st.cval[w] == 0 for w in range(ts.nw)
                if ts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool"))
    other = [w for w in st.F[fid].cols if w not in set(allw)] if fid is not None else []
    if fid is None:
        ks = [tuple(st.const_value(q) for q in regs)]
        norms = np.array([[1]+[0]*(p-1)], dtype=np.int64)
    else:
        f = st.F[fid]
        vals = np.stack([st.values(fid, q) for q in regs], axis=1)
        nrm = cyc_norm2(f.amp, p)
        keyv = [tuple(int(x) for x in r) for r in vals]
        acc = {}
        for k, a in zip(keyv, nrm):
            acc[k] = acc[k]+a if k in acc else a.copy()
        ks = sorted(acc)
        norms = cyc_canon(np.array([acc[k] for k in ks], dtype=np.int64))
    hp = h_perp(cfg, inst.log_h)
    supp = {k for k, a in zip(ks, norms) if a.any()}
    exact_uniform = supp == hp and all(np.array_equal(norms[0], a) for a in norms if a.any())
    fl = np.abs(cyc_to_complex(norms, p).real)
    probs = fl/fl.sum()
    sample = ks[int(rng.choice(len(ks), p=probs))]
    return {"sample": sample, "support_in_h_perp": supp <= hp, "exactly_uniform_on_h_perp": bool(exact_uniform),
            "support_size": len(supp), "h_perp_size": len(hp), "workspace_clean": bool(clean),
            "readout_factor_extra_wires": len(other), "peak_rows": st.peak_rows,
            "peak_MB": round(st.peak_bytes/1e6, 1), "factor_merges": st.merges, "counts": dict(counts),
            "measured_registers": dict(measured), "seconds": round(time.time()-t0, 2),
            **({"source_checks": len(src_checks), "source_checks_pass": bool(all(src_checks))} if source_check else {})}


def run_recovery(ts, inst, steps, sched, seed, extra=4, **kw):
    cfg = ts.cfg
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(cfg.m+extra):
        rows.append(run_terminal_sample(ts, inst, steps, sched, rng, **kw))
    samples = [list(r["sample"]) for r in rows]
    rec = rref(nullspace(samples, cfg.m, cfg.p), cfg.p) == rref(inst.log_h, cfg.p)
    return {"recovered": bool(rec), "terminal_samples": len(rows), "rows": rows}


# ====================================================================== instances and report

def job(job_name):
    cfg = C.job_config(job_name)
    if job_name == "heis_f3":
        insts = G.heis3_instances()
    elif job_name == "n4_f5":
        insts = G.n4_instances(5)
    else:
        raise ValueError(job_name)
    return cfg, insts


def estimate(ts, inst):
    """Cost estimate before a run: qubits, gates, QFTs, oracle calls and an
    upper estimate of the largest factor (Q register uniform on G_(c-1) times
    one child of |S| x p^(g_c) rows)."""
    cfg = ts.cfg
    S = len(G.stage_indices(cfg, inst.log_h, cfg.c))
    nQ = cfg.laws[cfg.c-1].order if cfg.c >= 2 else 1
    return {"qubits": ts.nw, "S": S, "Q_uniform_rows": nQ,
            "est_peak_rows_top_merge": int(nQ*S*cfg.p**cfg.dims[cfg.c-1])}


def report(jobs=("heis_f3", "n4_f5"), seeds=(20261105,), levels=(2,), names=None, out_path=None, log=print,
           max_rows=6_000_000, max_bytes=3.0e9):
    out = {**STATUS, "runs": {}}
    for jn in jobs:
        cfg, insts = job(jn)
        ts = C.TerminalSample(cfg)
        t0 = time.time()
        steps = compile_program(ts)
        cnt = ts.counts()
        info = {"config": cfg.name(), "qubits": ts.nw, "gates": cnt["total"]["gates"],
                "qft_calls": cnt["total"].get("qft_calls", 0), "oracle_calls": cnt["total"].get("oracle_calls", 0),
                "compile_seconds": round(time.time()-t0, 2), "structure": ts.structure(), "levels": {}}
        for level in levels:
            sched, ok = measurement_schedule(ts, steps, level)
            lv = {"schedule_verified": ok, "measured_registers": sum(len(v) for v in sched.values()),
                  "subgroups": []}
            for inst in insts:
                if names and not any(n in inst.name for n in names):
                    continue
                est = estimate(ts, inst)
                for seed in seeds:
                    t1 = time.time()
                    try:
                        r = run_recovery(ts, inst, steps, sched, seed, max_rows=max_rows, max_bytes=max_bytes)
                        row = {"name": inst.name, "normal": bool(inst.normal), "seed": seed, "estimate": est,
                               "recovered": r["recovered"], "terminal_samples": r["terminal_samples"],
                               "all_support_in_h_perp": all(x["support_in_h_perp"] for x in r["rows"]),
                               "all_exactly_uniform": all(x["exactly_uniform_on_h_perp"] for x in r["rows"]),
                               "all_workspace_clean": all(x["workspace_clean"] for x in r["rows"]),
                               "peak_rows": max(x["peak_rows"] for x in r["rows"]),
                               "peak_MB": max(x["peak_MB"] for x in r["rows"]),
                               "seconds": round(time.time()-t1, 1), "samples": [x["sample"] for x in r["rows"]],
                               "per_sample": [{k: v for k, v in x.items() if k != "sample"} for x in r["rows"]]}
                    except BudgetExceeded as e:
                        row = {"name": inst.name, "normal": bool(inst.normal), "seed": seed, "estimate": est,
                               "skipped": str(e), "seconds": round(time.time()-t1, 1)}
                    lv["subgroups"].append(row)
                    log(json.dumps({k: v for k, v in row.items() if k not in ("per_sample", "samples")}))
                    if out_path:
                        info["levels"][str(level)] = lv
                        out["runs"][jn] = info
                        with open(out_path, "w") as fh:
                            json.dump(out, fh, indent=1, default=str)
            info["levels"][str(level)] = lv
        out["runs"][jn] = info
    out["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
    if out_path:
        with open(out_path, "w") as fh:
            json.dump(out, fh, indent=1, default=str)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="+", default=["heis_f3", "n4_f5"])
    ap.add_argument("--seeds", nargs="+", type=int, default=[20261105])
    ap.add_argument("--levels", nargs="+", type=int, default=[2])
    ap.add_argument("--names", nargs="*")
    ap.add_argument("--max-rows", type=int, default=6_000_000)
    ap.add_argument("--out")
    a = ap.parse_args()
    report(a.jobs, tuple(a.seeds), tuple(a.levels), a.names, a.out, max_rows=a.max_rows)


if __name__ == "__main__":
    main()


# ====================================================================== round 2: exact output law (level 0)
#
# AI-checked, pending human review. Report:
# research/audits/reviews/2026-11-05-rees-receiver-round2.md.
#
# The level-0 run (nothing measured before the readout) does not fit as one
# product of factors when S is small: after the merge block the three children
# and Q share one factor of up to 27 * 243^3 = 3.9e8 rows. HubState writes the
# SAME joint state exactly as an orthogonal sum over the basis values h of a set
# of "hub" wires (the instrument labels and the root Q register),
#     |Psi> = sum_h |c(h)> (x) prod_f |psi_f(h)>,
# where c(h) assigns a basis value to every wire that is not in a factor (the
# hub wires and every wire whose value is a function of h, e.g. the witness
# register and clean workspace), and each factor f stores its rows for all h
# at once (row = (h, bits), amplitude in Z[zeta_p]). This is a representation,
# not an approximation or a measurement: every gate is applied to it exactly
# (a gate with a local control and a hub-classical target moves the target
# into the factor), the factors of the same h are joined on h when a gate
# needs it, and a factor wire that is constant within every h returns to c(h).
# The labels and Q are used only as controls after the split (verified on the
# gate list), so the children stay in separate factors and the state needs
# |hubs| * (sum of child rows) rows instead of the product. The final readout
# law is computed exactly from the Gram matrices of the factors:
#     P(y) = sum_{h,h' : c(h) = c(h') off Q} zeta^(y.(q_h - q_h')) prod_f <psi_f(h')|psi_f(h)>.

def cyc_mul_rows(a, b, p):
    """Row-wise products a_r * b_r in Z[zeta_p]; a, b (N, p)."""
    out = np.zeros(np.broadcast_shapes(a.shape, b.shape), dtype=np.int64)
    for i in range(p):
        ai = a[..., i:i+1]
        if ai.any():
            out += np.roll(ai*b, i, axis=-1)
    return cyc_canon(out)


def cyc_conj(a):
    p = a.shape[-1]
    return a[..., (-np.arange(p)) % p]


class HFactor:
    __slots__ = ("h", "cols", "amp", "_cnt")

    def __init__(self, h, cols, amp):
        self.h, self.cols, self.amp = h, cols, amp
        self._cnt = None


class HubState:
    """Exact joint state as an orthogonal sum over hub values (see the comment
    above). Wires are either local (a column of exactly one factor) or
    hub-classical (a uint8 array over the hubs)."""

    def __init__(self, nw, p, H, max_rows=8_000_000):
        self.nw, self.p, self.H = nw, p, H
        self.owner = [-1]*nw
        self.hub = {}
        self.F = {}
        self._next = 0
        self.hamp = np.zeros((H, p), dtype=np.int64)
        self.hamp[:, 0] = 1
        self.max_rows = max_rows
        self.peak_rows = 0
        self.joins = 0

    # -- construction from a FactorState: split over the values of hub_wires
    @classmethod
    def split(cls, st, hub_wires, max_rows=8_000_000):
        p, nw = st.p, st.nw
        hub_wires = list(dict.fromkeys(hub_wires))
        hset = set(hub_wires)
        parts = []                                    # (fid, hub wires in it, vals, idx per row)
        for fid, f in st.F.items():
            hw = [w for w in hub_wires if st.owner[w] == fid]
            if hw:
                bits = np.stack([_unpack(f.cols[w], f.N) for w in hw], axis=1)
                vals, idx = np.unique(bits, axis=0, return_inverse=True)
                parts.append((fid, hw, vals, idx.ravel()))
            else:
                parts.append((fid, [], np.zeros((1, 0), dtype=np.uint8), np.zeros(f.N, dtype=np.int64)))
        radix = [len(v) for _, _, v, _ in parts]
        H = int(np.prod(radix)) if radix else 1
        hs = cls(nw, p, H, max_rows=max_rows)
        strides = np.cumprod([1]+radix[:-1]) if radix else []
        hidx = np.arange(H, dtype=np.int64)
        for w in range(nw):
            if st.owner[w] < 0:
                hs.hub[w] = np.full(H, st.cval[w], dtype=np.uint8)
        for (fid, hw, vals, idx), n, stv in zip(parts, radix, strides):
            f = st.F[fid]
            digit = (hidx//stv) % n
            for k, w in enumerate(hw):
                hs.hub[w] = vals[digit, k].astype(np.uint8)
            order = np.argsort(idx, kind="stable")
            cnt = np.bincount(idx, minlength=n)
            start = np.concatenate([[0], np.cumsum(cnt)[:-1]])
            per_h = cnt[digit]
            rep_h = np.repeat(hidx, per_h)
            off = np.concatenate([[0], np.cumsum(per_h)[:-1]])
            k = np.arange(len(rep_h)) - np.repeat(off, per_h)
            rows = order[start[digit[rep_h]]+k]
            others = [w for w in f.cols if w not in hset]
            amp = f.amp[rows]
            if others:
                cols = {w: _unpack(f.cols[w], f.N)[rows].astype(np.uint8) for w in others}
                hs._new(HFactor(rep_h, cols, amp))
            else:
                if len(rows) != H:
                    raise AssertionError("factor without local wires must have one row per hub")
                hs.hamp = cyc_mul_rows(hs.hamp, amp, p)
        hs.hamp = hs._reduce(hs.hamp)
        for fid in list(hs.F):
            hs.split_constants(list(hs.F[fid].cols))
        return hs

    def _new(self, f):
        fid = self._next
        self._next += 1
        self.F[fid] = f
        for w in f.cols:
            self.owner[w] = fid
        self.peak_rows = max(self.peak_rows, len(f.h))
        return fid

    def _reduce(self, amp):
        amp = cyc_canon(amp)
        g = int(np.gcd.reduce(np.abs(amp).ravel())) if amp.size else 0
        if g > 1:
            amp //= g
        if amp.size and int(np.abs(amp).max()) > (1 << 52):
            raise OverflowError("amplitude coefficients too large for int64")
        return amp

    def _counts(self, f):
        if f._cnt is None:
            f._cnt = np.bincount(f.h, minlength=self.H)
            if f._cnt.min() < 1:
                raise AssertionError("a hub lost all rows of a factor")
        return f._cnt

    def _join(self, f1, f2):
        """Tensor product of two factors for every hub (rows paired on h)."""
        A, B = self.F[f1], self.F[f2]
        cA, cB = self._counts(A), self._counts(B)
        n = cA*cB
        tot = int(n.sum())
        if tot > self.max_rows:
            raise BudgetExceeded(f"hub join of {tot} rows exceeds the budget")
        self.joins += 1
        sA = np.concatenate([[0], np.cumsum(cA)[:-1]])
        sB = np.concatenate([[0], np.cumsum(cB)[:-1]])
        hh = np.repeat(np.arange(self.H), n)
        off = np.concatenate([[0], np.cumsum(n)[:-1]])
        k = np.arange(tot) - np.repeat(off, n)
        ia = sA[hh] + k//cB[hh]
        ib = sB[hh] + k % cB[hh]
        cols = {w: c[ia] for w, c in A.cols.items()}
        cols.update({w: c[ib] for w, c in B.cols.items()})
        A.h, A.cols, A.amp, A._cnt = hh, cols, self._reduce(cyc_mul_rows(A.amp[ia], B.amp[ib], self.p)), None
        for w in B.cols:
            self.owner[w] = f1
        del self.F[f2]
        self.peak_rows = max(self.peak_rows, tot)
        return f1

    def _unify(self, fids):
        fids = sorted(fids)
        fid = fids[0]
        for o in fids[1:]:
            fid = self._join(fid, o)
        return fid

    def _col(self, fid, w):
        if self.owner[w] == fid:
            return self.F[fid].cols[w]
        if self.owner[w] >= 0:
            raise AssertionError("wire in another factor")
        return self.hub[w][self.F[fid].h]

    def _localize(self, w, fid):
        f = self.F[fid]
        f.cols[w] = self.hub.pop(w)[f.h]
        self.owner[w] = fid

    def gate(self, name, q):
        if name == "swap":
            a, b = q
            oa, ob = self.owner[a], self.owner[b]
            va = self.F[oa].cols.pop(a) if oa >= 0 else self.hub.pop(a)
            vb = self.F[ob].cols.pop(b) if ob >= 0 else self.hub.pop(b)
            if ob >= 0:
                self.F[ob].cols[a] = vb
            else:
                self.hub[a] = vb
            if oa >= 0:
                self.F[oa].cols[b] = va
            else:
                self.hub[b] = va
            self.owner[a], self.owner[b] = ob, oa
            return
        t = q[-1]
        ctrls = q[:-1]
        fids = {self.owner[w] for w in q if self.owner[w] >= 0}
        if not fids:
            v = self.hub[t]
            if ctrls:
                m = self.hub[ctrls[0]]
                for c in ctrls[1:]:
                    m = m & self.hub[c]
                np.bitwise_xor(v, m, out=v)
            else:
                np.bitwise_xor(v, 1, out=v)
            return
        fid = self._unify(fids) if len(fids) > 1 else fids.pop()
        if self.owner[t] < 0:
            self._localize(t, fid)
        f = self.F[fid]
        if ctrls:
            m = self._col(fid, ctrls[0])
            for c in ctrls[1:]:
                m = m & self._col(fid, c)
            np.bitwise_xor(f.cols[t], m, out=f.cols[t])
        else:
            np.bitwise_xor(f.cols[t], 1, out=f.cols[t])

    def run(self, gates):
        for name, q in gates:
            self.gate(name, q)

    def split_constants(self, wires):
        for w in set(wires):
            fid = self.owner[w]
            if fid < 0:
                continue
            f = self.F[fid]
            cnt = self._counts(f)
            start = np.concatenate([[0], np.cumsum(cnt)[:-1]])
            col = f.cols[w]
            vals = col[start]
            if not np.array_equal(col, np.repeat(vals, cnt)):
                continue
            del f.cols[w]
            self.owner[w] = -1
            self.hub[w] = vals.astype(np.uint8)
            if not f.cols:
                if len(f.h) != self.H:
                    raise AssertionError("distinct rows with equal bits")
                self.hamp = self._reduce(cyc_mul_rows(self.hamp, f.amp, self.p))
                del self.F[fid]

    def value(self, reg):
        """Value of a hub-classical register for every hub (raises if local)."""
        out = np.zeros(self.H, dtype=np.int64)
        for i, w in enumerate(reg):
            if self.owner[w] >= 0:
                raise ValueError("register is not hub-classical")
            out |= self.hub[w].astype(np.int64) << i
        return out

    # -- exact Gram matrices
    def gram(self, fid):
        """G[h, h'] = <psi_f(h')|psi_f(h)> in Z[zeta_p], dense (H, H, p)."""
        from scipy import sparse
        f, p, H = self.F[fid], self.p, self.H
        ws = sorted(f.cols)
        bits = np.stack([f.cols[w] for w in ws], axis=1)
        keys = np.packbits(bits, axis=1)
        keys = np.ascontiguousarray(keys).view(np.dtype((np.void, keys.shape[1]))).ravel()
        _, kid = np.unique(keys, return_inverse=True)
        kid = kid.ravel()
        K = int(kid.max())+1
        mats = [sparse.csr_matrix((f.amp[:, i], (f.h, kid)), shape=(H, K)) for i in range(p)]
        out = np.zeros((H, H, p), dtype=np.int64)
        for i in range(p):
            if not mats[i].nnz:
                continue
            for j in range(p):
                if not mats[j].nnz:
                    continue
                prod_ = (mats[i] @ mats[j].T).toarray()
                out[:, :, (i-j) % p] += prod_.astype(np.int64)
        return cyc_canon(out)

    def total_gram(self):
        """prod_f G_f[h, h'] * hamp[h] conj(hamp[h']) (no masking)."""
        p = self.p
        G = cyc_mul_rows(self.hamp[:, None, :], cyc_conj(self.hamp)[None, :, :], p)
        for fid in self.F:
            Gf = self.gram(fid)
            # bound the product before multiplying (review finding 10): |entry| <= p*max|G|*max|Gf|
            if p * int(np.abs(G).max()) * int(np.abs(Gf).max()) >= (1 << 62):
                raise OverflowError("Gram entries too large")
            G = cyc_mul_rows(G, Gf, p)
        return G


def _wires(regs):
    return [w for q in regs for w in q]


def child_registers(ts):
    """For a class-2 terminal sample: per child (address regs, oracle output regs, label regs)."""
    if ts.cfg.c != 2:
        raise ValueError("exact level-0 law implemented for class 2")
    return [(k["reg"], k["ys"], k["z"]) for k in ts.tree["kids"]]


def hub_split_point(ts, steps):
    """Index of the last Q-preparation step of the root; the hub split is right after it."""
    return max(i for i, s in enumerate(steps) if s[2] == "q_prep_qft")


def hub_condition(ts, steps, split, hub_wires):
    """After the split and before the final QFT no step uses a hub wire other
    than as a control (the condition under which the children stay separate;
    exactness of HubState does not depend on it)."""
    final = min(i for i, s in enumerate(steps) if s[2] == "final_qft")
    hw = set(hub_wires)
    bad = [i for i in range(split+1, final) if steps[i][3] & hw]
    kinds = {steps[i][0] for i in range(split+1, final)}
    return {"hub_wires_only_controls": not bad, "segment_kinds": sorted(kinds), "final_qft_step": final}


def _left_coset_ids(law, S):
    """Canonical left-coset id (min index of x S) for every x of the group."""
    X = law.elements()
    Sel = law.decode(np.asarray(S, dtype=np.int64))
    ids = np.full(law.order, np.iinfo(np.int64).max, dtype=np.int64)
    for s in Sel:
        ids = np.minimum(ids, law.encode(law.mul(X, s[None, :])))
    return ids


def _reg_values(st, fid, regs, rows=None):
    """Values (N, len(regs)) of registers on the rows of factor fid of a FactorState (constants allowed)."""
    return np.stack([st.values(fid, list(q)) for q in regs], axis=1)


def joint_rows(st, wires):
    """Rows of the tensor product of all factors of a FactorState that hold any
    of wires: returns (bits of wires (N, len), bits of the other wires of those
    factors (N, k), amp (N, p)). Constants are filled in. No mutation."""
    p = st.p
    fids = sorted({st.owner[w] for w in wires if st.owner[w] >= 0})
    N = 1
    amp = np.zeros((1, p), dtype=np.int64)
    amp[0, 0] = 1
    cols = {}
    for fid in fids:
        f = st.F[fid]
        ia = np.repeat(np.arange(N), f.N)
        ib = np.tile(np.arange(f.N), N)
        cols = {w: c[ia] for w, c in cols.items()}
        for w, c in f.cols.items():
            cols[w] = _unpack(c, f.N)[ib]
        amp = cyc_mul_rows(amp[ia], f.amp[ib], p)
        N = len(ia)
    A = np.stack([cols[w] if w in cols else np.full(N, st.cval[w], dtype=np.uint8) for w in wires], axis=1) \
        if wires else np.zeros((N, 0), dtype=np.uint8)
    rest = [w for w in sorted(cols) if w not in set(wires)]
    B = np.stack([cols[w] for w in rest], axis=1) if rest else np.zeros((N, 0), dtype=np.uint8)
    return A, B, amp


def gram_by_keys(akey, bkey, amp, nA, p):
    """R[a, a'] = sum over rows with equal bkey of amp conj(amp'), dense (nA, nA, p)."""
    from scipy import sparse
    _, bk = np.unique(bkey, return_inverse=True)
    bk = bk.ravel()
    K = int(bk.max())+1 if len(bk) else 1
    mats = [sparse.csr_matrix((amp[:, i], (akey, bk)), shape=(nA, K)) for i in range(p)]
    out = np.zeros((nA, nA, p), dtype=np.int64)
    for i in range(p):
        for j in range(p):
            if mats[i].nnz and mats[j].nnz:
                out[:, :, (i-j) % p] += (mats[i] @ mats[j].T).toarray().astype(np.int64)
    return cyc_canon(out)


def _rowkey(B):
    if B.shape[1] == 0:
        return np.zeros(len(B), dtype=np.int64)
    keys = np.packbits(B.astype(np.uint8), axis=1)
    return np.ascontiguousarray(keys).view(np.dtype((np.void, keys.shape[1]))).ravel()


def proportional(Gm, R):
    """Gm = c R in Z[zeta_p] for one rational c > 0 (R has a positive rational diagonal entry)."""
    if Gm.shape != R.shape:
        return False
    diag = [i for i in range(R.shape[0]) if R[i, i, 0] and not R[i, i, 1:].any()]
    if not diag:
        return False
    i = diag[0]
    r0, g0 = int(R[i, i, 0]), Gm[i, i]
    if g0[1:].any() or g0[0] == 0 or (g0[0] > 0) != (r0 > 0):
        return False
    return bool(np.array_equal(Gm*r0, R*int(g0[0])))


def _bits_to_values(B, nb, ncoord):
    """(N, ncoord*nb) bit matrix (register-major, bit i = wire i) -> (N, ncoord) values."""
    out = np.zeros((len(B), ncoord), dtype=np.int64)
    for j in range(ncoord):
        for i in range(nb):
            out[:, j] |= B[:, j*nb+i].astype(np.int64) << i
    return out


def child_reference_rdm(cfg, log_h, with_label):
    """Module-level reference for one child, from h (not from the oracle):
    the purification sum_x |x>|coset(x S)> of the coset density of S = exp(h~)
    in G_c, optionally followed by the instrument formula (label lambda, x' = x z^-1):
    psi(x', lam; k) = sum_z zeta^(-lam.z) [coset(x' z) = k]. Returns the exact
    reduced density on (x[, lam]) as (n, n, p), index = x (* p^g + lam)."""
    p, d = cfg.p, cfg.c
    law = cfg.laws[d]
    ids = _left_coset_ids(law, G.stage_indices(cfg, log_h, d))
    nX = law.order
    if not with_label:
        akey = np.arange(nX)
        amp = np.zeros((nX, p), dtype=np.int64)
        amp[:, 0] = 1
        return gram_by_keys(akey, ids, amp, nX, p)
    g = cfg.dims[d-1]
    from itertools import product as iprod
    Z = np.array(list(iprod(range(p), repeat=g)), dtype=np.int64).reshape(-1, g)
    X = law.elements()
    top = cfg.top(d)
    rows_a, rows_k, rows_e = [], [], []
    for lam_i, lam in enumerate(Z):
        for zv in Z:
            zfull = np.zeros((1, law.n), dtype=np.int64)
            zfull[0, top] = zv
            xz = law.encode(law.mul(X, zfull))          # x' z
            e = int(-np.dot(lam, zv)) % p
            rows_a.append(np.arange(nX)*len(Z)+lam_i)
            rows_k.append(ids[xz])
            rows_e.append(np.full(nX, e))
    a = np.concatenate(rows_a)
    k = np.concatenate(rows_k)
    e = np.concatenate(rows_e)
    # sum duplicates (same (a, k)) exactly
    key = a*law.order+k
    uk, inv = np.unique(key, return_inverse=True)
    amp = np.zeros((len(uk), p), dtype=np.int64)
    np.add.at(amp, (inv.ravel(), e), 1)
    amp = cyc_canon(amp)
    keep = amp.any(axis=1)
    return gram_by_keys((uk//law.order)[keep], (uk % law.order)[keep], amp[keep], nX*len(Z), p)


def child_monolithic_rdm(st, cfg, a_regs, z_regs, other_wires_ok=True):
    """Exact reduced density of the monolithic state on a child's address
    (and label) registers, everything else in those factors traced out."""
    p, d = cfg.p, cfg.c
    law = cfg.laws[d]
    nb = cfg.enc.nb
    wires = _wires(a_regs)+(_wires(z_regs) if z_regs else [])
    A, B, amp = joint_rows(st, wires)
    x = law.encode(_bits_to_values(A[:, :len(a_regs)*nb], nb, len(a_regs)))
    if z_regs:
        lam = _bits_to_values(A[:, len(a_regs)*nb:], nb, len(z_regs))
        li = np.zeros(len(lam), dtype=np.int64)
        for j in range(lam.shape[1]):
            li = li*p+lam[:, j]
        akey = x*p**len(z_regs)+li
        n = law.order*p**len(z_regs)
    else:
        akey, n = x, law.order
    if (A.astype(np.int64) >= 0).all() and len(akey) and akey.max() >= n:
        raise ArithmeticError("padding word in a child register")
    return gram_by_keys(akey, _rowkey(B), amp, n, p)


def hub_joint_rows(hs, wires):
    """Rows (h, bits of wires, amp) of the tensor product, for every hub, of the
    factors holding any of wires; None if one of those factors also holds a wire
    outside wires (the child is then not a separate tensor factor). No mutation."""
    p, H = hs.p, hs.H
    wset = set(wires)
    fids = sorted({hs.owner[w] for w in wires if hs.owner[w] >= 0})
    for fid in fids:
        if not set(hs.F[fid].cols) <= wset:
            return None
    h = np.arange(H, dtype=np.int64)
    cols = {}
    amp = np.zeros((H, p), dtype=np.int64)
    amp[:, 0] = 1
    for fid in fids:
        f = hs.F[fid]
        cA, cB = np.bincount(h, minlength=H), hs._counts(f)
        n = cA*cB
        sA = np.concatenate([[0], np.cumsum(cA)[:-1]])
        sB = np.concatenate([[0], np.cumsum(cB)[:-1]])
        hh = np.repeat(np.arange(H), n)
        off = np.concatenate([[0], np.cumsum(n)[:-1]])
        k = np.arange(int(n.sum())) - np.repeat(off, n)
        ia, ib = sA[hh] + k//cB[hh], sB[hh] + k % cB[hh]
        cols = {w: c[ia] for w, c in cols.items()}
        cols.update({w: c[ib] for w, c in f.cols.items()})
        amp = cyc_mul_rows(amp[ia], f.amp[ib], p)
        h = hh
    B = np.stack([cols[w] if w in cols else hs.hub[w][h] for w in wires], axis=1).astype(np.uint8)
    return h, B, amp


def _unit_ratio(act, exp, p):
    """True iff act = u * exp row by row for ONE unit u = +-zeta^k."""
    if act.shape != exp.shape:
        return False
    for sgn in (1, -1):
        for k in range(p):
            if np.array_equal(cyc_canon(act), cyc_canon(sgn*np.roll(exp, k, axis=1))):
                return True
    return False


def _sorted_table(h, B, amp):
    key = np.concatenate([h[:, None].astype(np.int64), B.astype(np.int64)], axis=1)
    order = np.lexsort(key.T[::-1])
    return key[order], amp[order]


def exact_level0_law(ts, inst, steps, *, checkpoints=True, max_rows=8_000_000, log=None, return_state=False,
                     condition_sources=None):
    """The exact output law of the WHOLE class-2 coherent terminal sample with
    nothing measured before the readout (level 0), for one hidden subgroup, by
    the hub decomposition above; plus checkpoint comparisons of the monolithic
    state with module-level reference states computed from h (not from the
    oracle):
      K1 after each source (oracle calls done): the child's reduced density on
         its address equals the coset density of S = exp(h~) in G_2;
      K2 after each instrument: its reduced density on (address, label) equals
         the instrument formula applied to that coset density;
      K4 after the merge block, for every hub h = (labels, q): each child is its
         pre-merge state right-translated by -delta_(s_i)(sigma(q)), with s the
         independent reference witness (sde_reference); labels and Q unchanged;
         witness register and all workspace 0;
      K5 the reduced state of Q is proportional to rho_(H_1) (rho_target) for
         every label tuple separately and in total; the label law is uniform on
         (K^perp)^M; the readout law is exactly uniform on h^perp.
    Exactness: every amplitude is in Z[zeta_p]; the split is a change of
    representation, not a measurement."""
    cfg, p = ts.cfg, ts.p
    nb, m = cfg.enc.nb, cfg.m
    t0 = time.time()
    table = np.asarray(inst.oracle_table, dtype=np.int64)
    kids = child_registers(ts)
    split = hub_split_point(ts, steps)
    label_wires = [w for _, _, z in kids for w in _wires(z)]
    q_wires = _wires(ts.root)
    hub_wires = label_wires+q_wires
    cond = hub_condition(ts, steps, split, hub_wires)
    ck = {"K1_source_rdm_equals_coset_density": [], "K2_instrument_rdm_equals_reference": []}
    first_inst, last_inst = {}, {}
    for i, (a, ys, z) in enumerate(kids):
        zw = set(_wires(z))
        idx = [j for j, s in enumerate(steps) if s[0] in ("qft", "qft_dg") and set(s[1]) <= zw]
        first_inst[min(idx)] = i
        last_inst[max(idx)] = i
    ref1 = child_reference_rdm(cfg, inst.log_h, False) if checkpoints else None
    ref2 = child_reference_rdm(cfg, inst.log_h, True) if checkpoints else None
    st = FactorState(ts.nw, p, max_rows=max_rows, max_bytes=4e9)
    work = [w for w in range(ts.nw) if ts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool")]
    ck["K0_workspace_clean_after_each_source_and_instrument"] = []
    i = -1

    def partial(e, where):
        res = {"name": inst.name, "normal": bool(inst.normal), **cond, "budget_exceeded": str(e)[:160],
               "budget_exceeded_at_step": where, "law_computed": False,
               "checkpoints": {k: (bool(all(v)) if isinstance(v, list) else v) for k, v in ck.items()},
               "checkpoint_detail": {k: v for k, v in ck.items() if isinstance(v, list)},
               "all_checkpoints_pass": False, "seconds": round(time.time()-t0, 1)}
        if log:
            log(json.dumps(res, default=str))
        return res
    try:
        for i in range(split+1):
            kind, payload, comp, nc, _ = steps[i]
            if checkpoints and i in first_inst:
                a, ys, z = kids[first_inst[i]]
                ck["K0_workspace_clean_after_each_source_and_instrument"].append(
                    all(st.owner[w] < 0 and st.cval[w] == 0 for w in work))
                ck["K1_source_rdm_equals_coset_density"].append(
                    proportional(child_monolithic_rdm(st, cfg, a, None), ref1))
            if condition_sources is not None and i in first_inst:
                # round 3: condition the oracle outputs on the key of the coset of the address
                # condition_sources (exact projector; the coset-symmetry reduction says the law is unchanged)
                a, ys, z = kids[first_inst[i]]
                condition_on_coset(st, cfg, a, ys, int(condition_sources))
            if kind == "perm":
                st.run(payload)
                st.split_constants(nc)
            elif kind in ("qft", "qft_dg"):
                st.qft(payload, inverse=(kind == "qft_dg"))
            elif kind == "oracle":
                st.oracle(payload[0], payload[1], table, nb, m, cfg.label_bits)
            else:
                raise ValueError(kind)
            if checkpoints and i in last_inst and condition_sources is None:
                a, ys, z = kids[last_inst[i]]
                ck["K0_workspace_clean_after_each_source_and_instrument"].append(
                    all(st.owner[w] < 0 and st.cval[w] == 0 for w in work))
                ck["K2_instrument_rdm_equals_reference"].append(
                    proportional(child_monolithic_rdm(st, cfg, a, z), ref2))
        pre_peak = st.peak_rows
        hs = HubState.split(st, hub_wires, max_rows=max_rows)
        del st
        lab0 = {w: hs.hub[w].copy() for w in hub_wires}
        child_w = [_wires(a)+_wires(ys) for a, ys, _ in kids]
        pre = [hub_joint_rows(hs, w) for w in child_w] if checkpoints else None
        final = cond["final_qft_step"]
        if checkpoints:
            # reference witness and translation from the label and Q values at the split
            blk, law2 = ts.blocks[2], cfg.laws[2]

            def val0(q):
                return sum(lab0[w].astype(np.int64) << k for k, w in enumerate(q))
            lam_ref = np.stack([np.stack([val0(q) for q in z], axis=1) for _, _, z in kids], axis=2)  # (H, g, M)
            s_ref = C.sde_reference(p, 2, lam_ref)
            # the reference witness itself: nonzero and sum_i s_i^2 lambda_i = 0 for every hub value
            s64 = np.asarray(s_ref, dtype=np.int64)
            ck["K4_reference_witness_solves_sum_s2_lambda_eq_0"] = bool(
                (s64 % p != 0).any(axis=1).all()
                and not (np.einsum("hgm,hm->hg", lam_ref.astype(np.int64), s64*s64) % p).any())
            q_ref = np.stack([val0(q) for q in ts.root], axis=1)

            def translated(ci):
                """child ci equals its pre-merge state right-translated by -delta_(s_i)(sigma(q)), every hub."""
                post = hub_joint_rows(hs, child_w[ci])
                if post is None or pre[ci] is None:
                    return False
                h0, B0, A0 = pre[ci]
                a = kids[ci][0]
                X = _bits_to_values(B0[:, :len(a)*nb], nb, len(a))
                Xn = law2.mul(X, C._witness_bound_g(blk, s_ref[:, ci], q_ref)[h0])
                Bn = B0.copy()
                for j in range(len(a)):
                    for bit in range(nb):
                        Bn[:, j*nb+bit] = (Xn[:, j] >> bit) & 1
                ke, ae = _sorted_table(h0, Bn, A0)
                ka, aa = _sorted_table(*post)
                return bool(np.array_equal(ke, ka) and _unit_ratio(aa, ae, p))
            # K3: at every component boundary of the merge segment no workspace wire is entangled
            # (all are functions of labels and q); at the end of child i's (ctrl, bch, ctrl^-1) the
            # child is already its reference translation
            bounds = [i for i in range(split+1, final) if i+1 == final or steps[i+1][2] != steps[i][2]]
            # ctrl_i^-1 and ctrl_{i+1} share one component name, so the witness-control
            # boundaries are [end ctrl_0, end ctrl_0^-1 ctrl_1, ..., end ctrl_{M-1}^-1]; child i
            # has finished its own merge at the (i+1)-th of them (review finding 1)
            wc_ends = [i for i in bounds if steps[i][2].startswith("witness_control")][1:]
            if len(wc_ends) != len(kids):
                raise AssertionError(f"{len(wc_ends)} witness-control boundaries for {len(kids)} children")
            child_end = {i: ci for ci, i in enumerate(wc_ends)}
            ck["K3_workspace_unentangled_at_each_merge_component_boundary"] = []
            ck["K3_child_translated_after_its_own_merge"] = []
        for i in range(split+1, final):
            kind, payload, comp, nc, _ = steps[i]
            if kind != "perm":
                raise ValueError(f"unexpected {kind} inside the merge segment")
            hs.run(payload)
            hs.split_constants(nc)
            if checkpoints and i in bounds:
                ck["K3_workspace_unentangled_at_each_merge_component_boundary"].append(
                    all(hs.owner[w] < 0 for w in work))
                if i in child_end:
                    ck["K3_child_translated_after_its_own_merge"].append(translated(child_end[i]))
    except BudgetExceeded as e:
        return partial(e, i)
    # ---- K4
    out = {"name": inst.name, "normal": bool(inst.normal), "hubs": hs.H, **cond,
           "pre_split_peak_rows": int(pre_peak), "hub_peak_rows": int(hs.peak_rows), "hub_joins": hs.joins}
    hub_ok = all(hs.owner[w] < 0 for w in hub_wires)
    out["labels_and_Q_unchanged"] = bool(hub_ok and all(np.array_equal(hs.hub[w], lab0[w]) for w in hub_wires))
    clean = all(hs.owner[w] < 0 and not hs.hub[w].any() for w in range(ts.nw)
                if ts.role[w] in ("arith_ancilla", "evaluation_w", "block_workspace_pool"))
    out["workspace_and_witness_clean_every_hub"] = bool(clean)
    if checkpoints:
        k4 = [translated(i) for i in range(len(kids))]
        ck["K4_children_equal_reference_translation_every_hub"] = k4
    # ---- law and K5
    if not hub_ok:
        out.update({"law_computed": False, "checkpoints": {k: (bool(all(v)) if isinstance(v, list) else v)
                                                           for k, v in ck.items()}, "all_checkpoints_pass": False})
        if return_state:
            out["_state"] = hs
        return out
    Gt = hs.total_gram()
    sig_w = [w for w in range(ts.nw) if hs.owner[w] < 0 and w not in set(q_wires)]
    sig = np.stack([hs.hub[w] for w in sig_w], axis=1) if sig_w else np.zeros((hs.H, 0), dtype=np.uint8)
    _, grp = np.unique(sig, axis=0, return_inverse=True)
    grp = grp.ravel()
    same = grp[:, None] == grp[None, :]
    Gt[~same] = 0
    qc = np.stack([hs.value(list(q)) for q in ts.root], axis=1)
    law1 = cfg.laws[1]
    E = law1.elements()
    probs = {}
    for y in E:
        yq = (qc @ y) % p
        e = (yq[:, None]-yq[None, :]) % p
        tot = np.zeros(p, dtype=np.int64)
        for k in range(p):
            msk = e == k
            if msk.any():
                tot += np.roll(Gt[msk].sum(axis=0), k)
        tot = cyc_canon(tot)
        if tot.any():
            probs[tuple(int(v) for v in y)] = tot
    hp = h_perp(cfg, inst.log_h)
    vals = list(probs.values())
    rational = all(not v[1:].any() for v in vals)
    out["readout_law_rational"] = bool(rational)
    out["support_equals_h_perp"] = set(probs) == hp
    out["exact_law_uniform_on_h_perp"] = bool(set(probs) == hp and rational and
                                               all(np.array_equal(v, vals[0]) for v in vals))
    out["law"] = {str(k): int(v[0]) for k, v in sorted(probs.items())} if rational else None
    if checkpoints:
        tgt, _ = C.rho_target(cfg, inst.log_h, 1)
        R = np.zeros(tgt.shape+(p,), dtype=np.int64)
        R[..., 0] = tgt
        qidx = law1.encode(qc)
        rho_all = np.zeros_like(R)
        per = []
        traces = []
        for gval in range(int(grp.max())+1):
            hsel = np.nonzero(grp == gval)[0]
            rho = np.zeros_like(R)
            sub = Gt[np.ix_(hsel, hsel)]
            np.add.at(rho, (qidx[hsel][:, None].repeat(len(hsel), 1), qidx[hsel][None, :].repeat(len(hsel), 0)), sub)
            rho = cyc_canon(rho)
            rho_all += rho
            per.append(proportional(rho, R))
            tr = cyc_canon(sum(rho[j, j] for j in range(len(rho))))
            traces.append(tr)
        K = len(G.allowed_labels(cfg, inst.log_h, 2))
        k5_tuple = bool(all(per))
        k5_law = bool(len(traces) == K**len(kids) and all(np.array_equal(t, traces[0]) for t in traces))
        ck["K5_rho_Q_proportional_to_rho_H1_total"] = proportional(cyc_canon(rho_all), R)
        out["label_tuples"] = len(traces)
        if condition_sources is None:
            ck["K5_rho_Q_proportional_to_rho_H1_every_label_tuple"] = k5_tuple
            ck["K5_label_law_uniform_on_Kperp_M"] = k5_law
        else:
            # Conditioned sources (round 3): an address can become hub-classical (one row per hub), so the
            # orthogonality classes above are finer than the label tuples. Group by the label wires only
            # (Gt is already 0 between orthogonal hubs, so this traces the address out).
            lab_w = [w for w in hub_wires if w not in set(q_wires)]
            labv = np.stack([hs.hub[w] for w in lab_w], axis=1) if lab_w else np.zeros((hs.H, 0), np.uint8)
            _, lg = np.unique(labv, axis=0, return_inverse=True)
            lg = lg.ravel()
            per2, tr2 = [], []
            for gval in range(int(lg.max())+1):
                hsel = np.nonzero(lg == gval)[0]
                rho = np.zeros_like(R)
                sub = Gt[np.ix_(hsel, hsel)]
                np.add.at(rho, (qidx[hsel][:, None].repeat(len(hsel), 1),
                                qidx[hsel][None, :].repeat(len(hsel), 0)), sub)
                rho = cyc_canon(rho)
                per2.append(proportional(rho, R))
                tr2.append(cyc_canon(sum(rho[j, j] for j in range(len(rho)))))
            ck["K5_rho_Q_proportional_to_rho_H1_every_label_tuple"] = bool(all(per2))
            ck["K5_label_law_uniform_on_Kperp_M"] = bool(len(tr2) == K**len(kids) and
                                                         all(np.array_equal(t, tr2[0]) for t in tr2))
            out["K5_per_orthogonality_class_when_conditioned"] = {"rho_Q": k5_tuple, "label_law": k5_law,
                                                                  "classes": len(traces), "label_tuples": len(tr2)}
            out["label_tuples"] = len(tr2)
    out["checkpoints"] = {k: (bool(all(v)) if isinstance(v, list) else v) for k, v in ck.items()}
    out["checkpoint_detail"] = {k: v for k, v in ck.items() if isinstance(v, list)}
    out["all_checkpoints_pass"] = bool(all(out["checkpoints"].values()) and out["labels_and_Q_unchanged"]
                                       and out["workspace_and_witness_clean_every_hub"])
    out["seconds"] = round(time.time()-t0, 1)
    if log:
        log(json.dumps({k: v for k, v in out.items() if k not in ("law",)}, default=str))
    if return_state:
        out["_state"] = hs
    return out


def plain_level0_law(ts, inst, steps, max_rows=8_000_000, max_bytes=4e9):
    """Level-0 output law from one FactorState (no hub split): {y: Z[zeta_p] vector}.
    Fits only when the oracle outputs take few values (large S)."""
    cfg, p = ts.cfg, ts.p
    table = np.asarray(inst.oracle_table, dtype=np.int64)
    st = FactorState(ts.nw, p, max_rows=max_rows, max_bytes=max_bytes)
    readout = None
    for kind, payload, comp, nc, _ in steps:
        if kind == "perm":
            st.run(payload)
            st.split_constants(nc)
        elif kind in ("qft", "qft_dg"):
            st.qft(payload, inverse=(kind == "qft_dg"))
        elif kind == "oracle":
            st.oracle(payload[0], payload[1], table, cfg.enc.nb, cfg.m, cfg.label_bits)
        else:
            readout = payload
    regs = [list(q) for q in readout]
    allw = _wires(regs)
    A, B, amp = joint_rows(st, allw)
    vals = _bits_to_values(A, cfg.enc.nb, len(regs))
    nrm = cyc_norm2(amp, p)
    acc = {}
    for k, a in zip(map(tuple, vals.tolist()), nrm):
        acc[k] = acc[k]+a if k in acc else a.copy()
    return {k: cyc_canon(v) for k, v in acc.items() if cyc_canon(v).any()}


def laws_proportional(L1, L2, p):
    """Two exact laws {y: Z[zeta] vector} with rational entries are proportional (positive)."""
    if set(L1) != set(L2):
        return False
    if any(v[1:].any() for v in list(L1.values())+list(L2.values())):
        return False
    t1 = sum(int(v[0]) for v in L1.values())
    t2 = sum(int(v[0]) for v in L2.values())
    return all(int(L1[k][0])*t2 == int(L2[k][0])*t1 for k in L1)


def exact_report(names=None, out_path=None, plain_crosscheck_max_S=81, plain_min_S=9, seeds=(1, 2), log=print,
                 max_rows=8_000_000):
    """Round 2: exact level-0 output law of the whole Heis(F_3) terminal sample for
    every subgroup, with checkpoints; cross-check against a plain level-0
    FactorState run where that fits (|S| >= plain_min_S); seeded recoveries
    sampled from the exact law."""
    cfg, insts = job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = compile_program(ts)
    cnt = ts.counts()
    out = {**STATUS, "status": "exact_level0_output_law_of_assembled_coherent_terminal_sample_finite_instances",
           "config": cfg.name(), "qubits": ts.nw, "gates": cnt["total"]["gates"],
           "qft_calls": cnt["total"].get("qft_calls", 0), "oracle_calls": cnt["total"].get("oracle_calls", 0),
           "subgroups": []}
    t0 = time.time()
    for inst in insts:
        if names and not any(n in inst.name for n in names):
            continue
        r = exact_level0_law(ts, inst, steps, max_rows=max_rows)
        S = len(G.stage_indices(cfg, inst.log_h, 2))
        r["S"] = S
        if plain_min_S <= S <= plain_crosscheck_max_S:
            t1 = time.time()
            try:
                L = plain_level0_law(ts, inst, steps)
                hl = {tuple(int(x) for x in k.strip("()").split(", ")): np.array([v]+[0]*(cfg.p-1))
                      for k, v in (r["law"] or {}).items()}
                r["plain_level0_law_equal"] = laws_proportional(L, hl, cfg.p)
            except BudgetExceeded as e:
                r["plain_level0_law_equal"] = f"skipped: {e}"
            r["plain_seconds"] = round(time.time()-t1, 1)
        if r.get("law"):
            keys = sorted(r["law"])
            w = np.array([r["law"][k] for k in keys], dtype=float)
            rec = []
            for sd in seeds:
                rng = np.random.default_rng(sd)
                smp = [list(int(x) for x in keys[i].strip("()").split(", "))
                       for i in rng.choice(len(keys), size=cfg.m+4, p=w/w.sum())]
                rec.append(rref(nullspace(smp, cfg.m, cfg.p), cfg.p) == rref(inst.log_h, cfg.p))
            r["seeded_recoveries_from_exact_law"] = rec
        out["subgroups"].append(r)
        if log:
            log(json.dumps({k: v for k, v in r.items() if k not in ("law", "checkpoint_detail")}, default=str))
        out["seconds"] = round(time.time()-t0, 1)
        out["max_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20, 1)
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(out, fh, indent=1, default=str)
    return out


def state_signature(hs):
    """Canonical bytes of a HubState (equal signatures => equal states; equal states
    with different factor partitions give different signatures, which is conservative)."""
    import hashlib
    hsh = hashlib.sha256()
    for w in range(hs.nw):
        if hs.owner[w] < 0:
            hsh.update(b"c%d" % w + hs.hub[w].tobytes())
    hsh.update(cyc_canon(hs.hamp).tobytes())
    for fid in sorted(hs.F, key=lambda f: min(hs.F[f].cols)):
        f = hs.F[fid]
        ws = sorted(f.cols)
        hsh.update(repr(ws).encode())
        B = np.stack([f.cols[w] for w in ws], axis=1)
        k, a = _sorted_table(f.h, B, f.amp)
        hsh.update(k.tobytes() + cyc_canon(a).tobytes())
    return hsh.hexdigest()


def mutate_steps(steps, comp_prefix, gate_kind, position):
    """Drop one gate (kind cx/ccx; 'first' or 'middle' of that kind) in the first
    perm step of a component. Returns (new steps, description)."""
    stp = [list(s) for s in steps]
    for i, s in enumerate(stp):
        if s[0] == "perm" and s[2].startswith(comp_prefix):
            ks = [j for j, (g, q) in enumerate(s[1]) if g == gate_kind]
            if not ks:
                continue
            k = ks[0] if position == "first" else ks[len(ks)//2]
            gates = list(s[1])
            g, q = gates.pop(k)
            stp[i] = [s[0], gates, s[2], set(s[3]), s[4]]
            return stp, {"step": i, "component": comp_prefix, "dropped": g, "wires": list(q), "position": position}
    raise LookupError(comp_prefix)


def negative_controls(names=("<[(1, 0, 0)]> non-normal", "<[(0, 0, 1)]> normal",
                             "<[(1, 0, 0), (0, 0, 1)]> normal", "<[]> normal"),
                      out_path=None, log=print):
    """Every mutant run through exact_level0_law: which checks detect it
    (deterministic), and, if none does, whether its final state equals the
    unmutated one exactly (an equivalent mutant on that instance)."""
    import copy
    cfg, insts = job("heis_f3")
    ts = C.TerminalSample(cfg)
    steps = compile_program(ts)
    sel = [i for i in insts if any(i.name.endswith("H="+n) for n in names)]
    base = {}
    out = {**STATUS, "status": "negative_controls_exact_level0", "baseline": {}, "mutants": []}

    def summary(r):
        ck = r.get("checkpoints", {})
        failed = sorted(k for k, v in ck.items() if v is False)
        if not r.get("labels_and_Q_unchanged", True):
            failed.append("labels_and_Q_unchanged")
        if not r.get("workspace_and_witness_clean_every_hub", True):
            failed.append("workspace_clean")
        law_known = r.get("law_computed", True)
        res = {"law_uniform": bool(r.get("exact_law_uniform_on_h_perp", False)) if law_known else None,
               "failed_checks": failed,
               "detected": bool(failed) or (law_known and not r.get("exact_law_uniform_on_h_perp", False))}
        if "budget_exceeded" in r:
            res["budget_exceeded_at_step"] = r["budget_exceeded_at_step"]
            res["budget_exceeded"] = r["budget_exceeded"]
            if not failed:
                res["detected"] = "undecided (over budget before any check failed)"
        return res

    def dump():
        if out_path:
            with open(out_path, "w") as fh:
                json.dump(out, fh, indent=1, default=str)

    for inst in sel:
        r = exact_level0_law(ts, inst, steps, return_state=True)
        base[inst.name] = state_signature(r.pop("_state"))
        out["baseline"][inst.name] = summary(r)
        if log:
            log("baseline", inst.name, out["baseline"][inst.name])

    def run(desc, ts_, steps_, inst_, compare_to):
        try:
            r = exact_level0_law(ts_, inst_, steps_, return_state=True)
            hs = r.pop("_state", None)
            row = {**desc, "instance": inst_.name, **summary(r)}
            if row["detected"] is False:
                row["final_state_identical_to_unmutated"] = state_signature(hs) == compare_to
        except (ArithmeticError, AssertionError, ValueError) as e:
            row = {**desc, "instance": inst_.name, "detected": "exception", "exception": repr(e)[:160]}
        out["mutants"].append(row)
        if log:
            log(json.dumps(row, default=str))
        dump()

    for inst in sel:
        bad = copy.copy(inst)
        tab = np.array(inst.oracle_table).copy()
        x0 = int(np.nonzero(tab != tab[0])[0][0]) if (tab != tab[0]).any() else None
        if x0 is not None:
            tab[x0] = tab[0]
            bad.oracle_table = tab
            run({"mutant": "oracle entry", "x0": x0}, ts, steps, bad, base[inst.name])
    for comp in ("source_evaluation", "instrument", "sde_grade2", "witness_control_grade2", "bch_merge_grade2"):
        for kind in ("cx", "ccx"):
            for pos in ("first", "middle"):
                try:
                    stp, desc = mutate_steps(steps, comp, kind, pos)
                except LookupError:
                    continue
                for inst in sel:
                    run({"mutant": "drop gate", **desc}, ts, stp, inst, base[inst.name])
    orig = C.MergeBlock
    for mut in ("g_sign", "skip_bennett", "skip_ctrl_inv", "skip_sde_inv"):
        C.MergeBlock = lambda cfg_, d, mutate=None, _m=mut: orig(cfg_, d, mutate={_m})
        try:
            tsm = C.TerminalSample(cfg)
        finally:
            C.MergeBlock = orig
        stm = compile_program(tsm)
        for inst in sel:
            run({"mutant": f"MergeBlock {mut}"}, tsm, stm, inst, base[inst.name])
    dump()
    return out


# ---------------------------------------------------------------- round 2: per-trajectory source checkpoint (KS)

def _source_nodes(ts):
    out = []

    def visit(node):
        if node.get("ys"):
            out.append(node)
        for k in node["kids"]:
            visit(k)
    visit(ts.tree)
    return out


def source_check_points(ts, steps):
    """For every top-grade source: the step right before its instrument's first QFT
    (all oracle calls done and the evaluation workspace uncomputed) -> (address regs,
    output regs)."""
    pts = {}
    for node in _source_nodes(ts):
        zw = set(_wires(node["z"]))
        j = min(k for k, s in enumerate(steps) if s[0] == "qft" and set(s[1]) <= zw)
        last = tuple(node["ys"][-1])
        if not max(k for k, s in enumerate(steps) if s[0] == "oracle" and tuple(s[1][1]) == last) < j:
            raise AssertionError("instrument before the last oracle call")
        pts[j-1] = (node["reg"], node["ys"])
    return pts


def delay_oracle_measurements(ts, steps, sched):
    """Move each oracle-output measurement of a schedule to the source's check point
    (right before its instrument; valid: no step after its oracle call touches an
    oracle output), so that checkpoint KS sees the whole source state before
    anything is measured."""
    pts = source_check_points(ts, steps)
    last_of = {}
    for i, (a, ys) in pts.items():
        for y in ys:
            last_of[tuple(y)] = i
    new = {}
    for t, lst in sched.items():
        for tag, reg in lst:
            tt = last_of.get(tuple(reg), t) if tag == "oracle_output" else t
            new.setdefault(max(t, tt), []).append((tag, reg))
    return new


def source_coset_check(st, cfg, a_regs, y_regs, coset_ids, work=()):
    """KS: the joint state of a source's address and oracle outputs (before any
    measurement) is sum_x |x>|key(x)>: every address once, equal amplitudes, no
    other wire entangled, and the fibres of key are exactly the left cosets of
    S = exp(h~) (module-level reference, from h); and every workspace wire in
    `work` is the constant 0 (review finding 4)."""
    if not all(st.owner[w] < 0 and st.cval[w] == 0 for w in work):
        return False
    nb = cfg.enc.nb
    law = cfg.laws[cfg.c]
    A, B, amp = joint_rows(st, _wires(a_regs)+_wires(y_regs))
    if B.shape[1]:
        return False
    x = law.encode(_bits_to_values(A[:, :len(a_regs)*nb], nb, len(a_regs)))
    if len(x) != law.order or len(np.unique(x)) != law.order:
        return False
    if not (cyc_canon(amp) == cyc_canon(amp[:1])).all():
        return False
    key = _rowkey(A[:, len(a_regs)*nb:])
    _, ki = np.unique(key, return_inverse=True)
    ki = ki.ravel()
    cid = coset_ids[x]
    pairs = len(np.unique(ki*law.order+cid))
    return bool(pairs == ki.max()+1 == len(np.unique(cid)))


def trajectory_controls(job_name="heis_f3", names=None, n=20, seed=7, out_path=None, log=print, mutants=("oracle",)):
    """Level-2 trajectories with checkpoint KS (oracle-output measurements delayed
    to the end of each source): per-trajectory catch rates for one changed oracle
    entry, and the false-alarm rate on the unmutated oracle."""
    import copy
    cfg, insts = job(job_name)
    ts = C.TerminalSample(cfg)
    steps = compile_program(ts)
    s2, ok = measurement_schedule(ts, steps, 2)
    sched = delay_oracle_measurements(ts, steps, s2)
    out = {**STATUS, "job": job_name, "schedule_verified": ok, "rows": []}
    rng = np.random.default_rng(seed)
    for inst in insts:
        if names and not any(inst.name.endswith("H="+nm) or nm == inst.name for nm in names):
            continue
        bad = copy.copy(inst)
        tab = np.array(inst.oracle_table).copy()
        x0 = int(np.nonzero(tab != tab[0])[0][0])
        tab[x0] = tab[0]
        bad.oracle_table = tab
        for label, ii in (("unmutated", inst), ("oracle entry changed", bad)):
            ks = law_bad = 0
            t0 = time.time()
            for _ in range(n):
                r = run_terminal_sample(ts, ii, steps, sched, rng, source_check=True)
                ks += not r["source_checks_pass"]
                law_bad += not (r["exactly_uniform_on_h_perp"] and r["workspace_clean"])
            row = {"instance": inst.name, "oracle": label, "x0": x0 if ii is bad else None, "trajectories": n,
                   "caught_by_KS": ks, "caught_by_readout_law": law_bad, "seconds": round(time.time()-t0, 1)}
            out["rows"].append(row)
            if log:
                log(json.dumps(row))
            if out_path:
                with open(out_path, "w") as fh:
                    json.dump(out, fh, indent=1, default=str)
    return out


# ====================================================================== round 3: coset conditioning of a source
#
# AI-checked, pending human review. Report:
# research/audits/reviews/2026-11-05-rees-receiver-round3.md.

def condition_on_coset(st, cfg, a_regs, y_regs, x0):
    """Exact conditioning of a top source's oracle outputs on the key of the left
    coset of the address x0 (the projector onto one value of the output
    register; amplitudes stay exact, the state is not renormalised). Returns the
    key bits. Used by the coset-symmetry reduction of round 3: the conditional
    output law does not depend on the coset, so it equals the level-0 law."""
    nb = cfg.enc.nb
    law = cfg.laws[cfg.c]
    A, B, amp = joint_rows(st, _wires(a_regs)+_wires(y_regs))
    x = law.encode(_bits_to_values(A[:, :len(a_regs)*nb], nb, len(a_regs)))
    rows = np.nonzero(x == x0)[0]
    if len(rows) != 1:
        raise AssertionError("address x0 not present exactly once")
    key = A[rows[0], len(a_regs)*nb:]
    yw = _wires(y_regs)
    fid = st._unify(yw)
    if fid is None:
        return key
    f = st.F[fid]
    keep = np.ones(f.N, dtype=bool)
    for bit, w in zip(key, yw):
        col = _unpack(f.cols[w], f.N) if st.owner[w] == fid else np.full(f.N, st.cval[w], dtype=np.uint8)
        keep &= col == bit
    st._select(fid, keep)
    return key
