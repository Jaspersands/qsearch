"""Exact end-to-end simulation of the mixed spectral source (rem:mixed-source) in the Rees core.

The paper's Remark rem:mixed-source replaces the flat wedge Omega_V of
Corollary cor:subspace-hsp by the product Psi = tensor_l Omega_(ran Q_l) of
top wedges of the distinct threshold projectors

    Q_l in {1[rho >= t_j]},  t_j = w(1 + a/M_0 + j),  w = delta/(16 rbar),

and says Psi can be fed to the four-step zero-moment design of
cor:subspace-hsp. This file runs that substitution on small groups. It
imports theorems/rees_end_to_end_sim.py and does not edit it.

Setting. G = (L, BCH) for L = Heis(F_3), Heis(F_5) or n4(F_5). R is the
LEFT-regular representation of G on C[G] (d = |G|, a permutation action).
For a hidden H, rho is a nonflat density whose eigenvectors are "atoms"

    u_(x, lam) = sum_(h in H) omega^(-lam(h)) e_(h*x),

with lam a linear functional on log H vanishing on [h, h], so that
R(h') u = omega^(lam(h')) u for h' in H. Atoms on distinct right cosets Hx
(or with distinct characters on one coset) are orthogonal, have integer
entries in Z[zeta_p] and squared norm |H|. Eigenvalues are exact rationals,
some degenerate, one possibly below w (a tail the flag drops).

What is EXACT (Z[zeta_p] integers, Python Fractions):
* the grid, every threshold projector and every distinct flag, for EVERY
  offset a in {0, ..., M_0 - 1}; the identities 0 <= B <= rho,
  Tr(rho - B) < delta/8, K <= rbar, sum r_l <= min(rbar(rbar+1)/2, 16 rbar/delta)
  and the margin count (#bad offsets <= rbar);
* phi_l(g) = <Omega_l|R(g)^(tensor r_l)|Omega_l> = det(B_l^+ R(g) B_l)/|H|^(r_l)
  for every g in G, as a cyclotomic integer over an integer; the ray
  stabilizer {g : |phi(g)| = 1} by exact comparison with zeta^k |H|^r; the
  phase on it as an exponent mod p, compared with prod_l det(R|_(Q_l));
* the design lift: F(x) = prod_(s in S) phi(E_s x) on the cover G~ is
  exactly 1 on {x : E_s x in Stab for all s} and that set is exp(hlift);
* the ideal (ell -> infinity) lifted source, which is then run through the
  UNCHANGED exact Rees core (ExactBackend, brute-force SDE at the
  Chevalley-Warning arity, exact stage-output and label-law grading).

What is FLOAT: the global gap delta (min trace distance over g outside H),
the wedge gap |phi(g)| <= 1 - delta^2/8, the wedge-determinant identity
against explicit antisymmetric tensors (Heis(F_3) only), and the finite-ell
dense runs on the Heisenberg covers through DenseBackend, where the address
density sigma_ell[a, b] = F(b^-1 * a)^ell / |G~| is built from the formula
after one explicit controlled-R circuit check.

What this does NOT do: it supplies the spectrum and eigenvectors of rho as
REFERENCE access to build the ideal Psi. It does not run the copies-only
rank learner, the density-matrix-exponentiation threshold instrument or the
growth instrument of part (ii), it implements no coherent receiver, and the
permutation family here has a classical solution (read H off the atoms). A
finite run can only falsify the remark, never prove it.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import permutations, product
import json
from math import ceil
import random
import time

import numpy as np

from theorems.rees_end_to_end_sim import (
    DenseBackend, ExactBackend, ExactState, HiddenInstance, NilGroup, cyc_canon, cyc_mul,
    expected_stage_indices, filiform4, grade_run, heisenberg, intersect, make_cover, nullspace, rref,
    run_rees, span_elements, stage_outputs_correct,
)


# ---------------------------------------------------------------- designs

DESIGNS = {(3, 2): (1, 1, 1, 2, 2, 2), (5, 2): (1, 2, 3, 4), (5, 3): (1, 2, 3, 4)}


def check_design(S, p, c):
    """Zero moments sum_s s^j = 0 (j = 1..c), nonzero points, >= c distinct."""
    return (all(s % p for s in S) and len(set(S)) >= c
            and all(sum(pow(s, j, p) for s in S) % p == 0 for j in range(1, c+1)))


# ---------------------------------------------------------------- atoms and rho

def _sign(perm):
    s, seen = 1, set()
    for i in range(len(perm)):
        if i in seen:
            continue
        j, n = i, 0
        while j not in seen:
            seen.add(j)
            j, n = perm[j], n+1
        s *= (-1)**(n-1)
    return s


@dataclass
class Atom:
    """An H-eigenvector with R(h) v = omega^(lam(h)) v, stored as a dense
    (|G|, p) array of canonical Z[zeta_p] entries. Plain atoms are
    u_(x, lam) = sum_h omega^(-lam.h) e_(h*x); `combine` forms u_a +- u_b for two
    atoms with the same character on different cosets."""
    lam: tuple
    vec: np.ndarray
    norm2: int
    cosets: tuple           # coset representatives used (for reporting)

    @property
    def support(self):
        return np.nonzero(self.vec.any(axis=1))[0]


@dataclass
class MixedState:
    """rho = sum_i lambda_i |v_i><v_i| / ||v_i||^2 with exact rational lambda_i and
    mutually orthogonal H-eigenvectors v_i."""
    inst: HiddenInstance
    atoms: list
    weights: list           # Fractions, sum 1
    label: str = ""

    @property
    def rank(self):
        return sum(1 for w in self.weights if w)


def character_functionals(inst):
    """Basis of linear functionals on L vanishing on [h, h], independent on log h
    (so lam . v is a character of H by Lazard and exponent p)."""
    alg, h = inst.algebra, inst.log_h
    if not h:
        return []
    derived = rref([alg.bracket(a, b) for a in h for b in h], alg.p)
    funcs = nullspace(derived, alg.dim, alg.p) if derived else [
        tuple(int(i == j) for j in range(alg.dim)) for i in range(alg.dim)]
    out, seen = [], []
    for f in funcs:
        vals = tuple(sum(a*b for a, b in zip(f, v)) % alg.p for v in h)
        if any(vals) and len(rref(seen+[vals], alg.p)) > len(seen):
            seen.append(vals)
            out.append(f)
    return out


def _conj(v, p):
    return cyc_canon(v[..., (-np.arange(p)) % p])


def _shift(v, k, p):
    """zeta^k * v."""
    return cyc_canon(v[..., (np.arange(p)-k) % p])


def make_atom(inst, x, lam):
    G, p = inst.group, inst.algebra.p
    H = G.decode(inst.subgroup)
    pts = G.encode(G.mul(H, np.array(x, dtype=np.int64)[None, :]))
    expo = (-(H @ np.array(lam, dtype=np.int64))) % p
    vec = np.zeros((G.order, p), dtype=np.int64)
    vec[pts, expo] = 1
    return Atom(tuple(int(v) for v in lam), cyc_canon(vec), len(pts), (tuple(x),))


def combine(a, b, sign):
    if a.lam != b.lam or a.norm2 != b.norm2:
        raise ValueError("combine needs equal characters and norms")
    return Atom(a.lam, cyc_canon(a.vec+sign*b.vec), a.norm2+b.norm2, a.cosets+b.cosets)


def check_atom_is_eigenvector(inst, atom, lmul):
    """Exact: R(h) v = omega^(lam(h)) v for every h in H, i.e.
    v[h*y] = omega^(-lam(h)) v[y]."""
    G, p = inst.group, inst.algebra.p
    for hidx, h in zip(inst.subgroup, G.decode(inst.subgroup)):
        k = int(np.dot(atom.lam, h)) % p
        if (atom.vec[lmul[hidx]] != _shift(atom.vec, -k, p)).any():
            return False
    return True


def inner(ua, ub, p):
    """<u_a, u_b> as a canonical Z[zeta_p] vector."""
    return cyc_canon(cyc_mul(_conj(ua.vec, p), ub.vec, p).sum(axis=0)[None, :])[0]


def atoms_orthonormal_up_to_norm(atoms, p):
    for i, j in product(range(len(atoms)), repeat=2):
        ip = inner(atoms[i], atoms[j], p)
        want = np.zeros(p, dtype=np.int64)
        if i == j:
            want[0] = atoms[i].norm2
        if (ip != want).any():
            return False
    return True


# ---------------------------------------------------------------- exact overlaps

def gram_all(ua, ub, lmul, p):
    """<u_a, R(g) u_b> for EVERY g at once: (|G|, p) canonical array.
    (R(g)u_b)[g*z] = u_b[z], so the sum runs over z in supp(u_b)."""
    nG = lmul.shape[0]
    out = np.zeros((nG, p), dtype=np.int64)
    ca = _conj(ua.vec, p)
    for z in ub.support:
        out += cyc_mul(ca[lmul[:, z]], ub.vec[z][None, :], p)
    return cyc_canon(out)


def det_all(entries, r, p):
    """Leibniz determinant of an r x r matrix of (|G|, p) cyclotomic arrays."""
    nG = entries[0][0].shape[0]
    total = np.zeros((nG, p), dtype=np.int64)
    for perm in permutations(range(r)):
        term = None
        for i in range(r):
            term = entries[i][perm[i]] if term is None else cyc_mul(term, entries[i][perm[i]], p)
        total = total+_sign(perm)*term
    return cyc_canon(total)


@dataclass
class FlagOverlap:
    """phi(g) = prod_l N_l(g)/D_l on G, exactly classified; D_l = prod ||v_i||^2."""
    ranks: tuple
    numer: list             # per flag: (|G|, p) canonical cyclotomic numerators
    denom: list             # per flag: det(B_l^+ B_l), a positive integer (orthogonal basis)
    unit: np.ndarray        # bool: phi(g) is a root of unity (exact)
    phase: np.ndarray       # exponent k with phi(g) = omega^k where unit, else -1
    modulus: np.ndarray     # float |phi(g)|
    complex_value: np.ndarray


def flag_overlap(inst, flags, lmul):
    """flags: list of lists of mutually orthogonal atoms (each a basis of one Q_l).
    |phi| = 1 forces phi = det(R(g)|_V), a p-th root of unity (R(g)^p = 1), so
    'N == zeta^k D for some k' is an exact test of ray stabilization."""
    p = inst.algebra.p
    nG = lmul.shape[0]
    zeta = np.exp(2j*np.pi*np.arange(p)/p)
    unit, phase = np.ones(nG, dtype=bool), np.zeros(nG, dtype=np.int64)
    value = np.ones(nG, dtype=complex)
    numer, denom = [], []
    for basis in flags:
        r = len(basis)
        E = [[gram_all(basis[i], basis[j], lmul, p) for j in range(r)] for i in range(r)]
        N = det_all(E, r, p)
        D = 1
        for u in basis:
            D *= u.norm2
        numer.append(N)
        denom.append(D)
        value *= (N @ zeta)/D
        hit = np.full(nG, -1, dtype=np.int64)
        for k in range(p):
            target = np.zeros(p, dtype=np.int64)
            target[k] = D
            target = cyc_canon(target)
            hit[(N == target[None, :]).all(axis=1)] = k
        unit &= hit >= 0
        phase = np.where(hit >= 0, (phase+hit) % p, phase)
    phase = np.where(unit, phase, -1)
    return FlagOverlap(tuple(len(b) for b in flags), numer, denom, unit, phase,
                       np.abs(value), value)


# ---------------------------------------------------------------- spectral grid

@dataclass
class Grid:
    delta: Fraction
    rbar: int
    w: Fraction
    J: int
    M0: int
    beta: Fraction


def make_grid(delta, rbar, beta=Fraction(1, 2)):
    w = Fraction(delta)/(16*rbar)
    J = ceil(1/w)
    M0 = 1
    while M0 < 8*rbar/beta:
        M0 *= 2
    return Grid(Fraction(delta), rbar, w, J, M0, beta)


def thresholds(grid, a):
    return [grid.w*(1+Fraction(a, grid.M0)+j) for j in range(grid.J)]


def flags_for_offset(state, grid, a):
    """Distinct nonzero threshold projectors (atom-index sets, ranks strictly
    decreasing) and the exact part-(i) identities for this offset.

    count_i = #{j : lambda_i >= t_j}; P_j = {i : count_i > j}; B = w count_i on
    atom i. For J <= 5000 the count is also taken by brute force over all J
    thresholds and compared with w max(0, floor(lambda/w - a/M_0))."""
    lam, w, J = state.weights, grid.w, grid.J
    off = Fraction(a, grid.M0)
    counts = [min(J, max(0, (x/w-1-off).__floor__()+1)) for x in lam]
    brute = None
    if J <= 5000:
        ts = thresholds(grid, a)
        brute = [sum(1 for t in ts if x >= t) for x in lam]
    levels = sorted({c for c in counts if c > 0}, reverse=True)
    distinct = [frozenset(i for i, c in enumerate(counts) if c >= v) for v in sorted(levels)]
    b = [w*c for c in counts]
    floor_formula = [w*max(0, (x/w-off).__floor__()) for x in lam]
    margin = w/(4*grid.M0)

    def dist(x):
        j = min(J-1, max(0, round(float(x/w-1-off))))
        return min(abs(x-w*(1+off+k)) for k in (j-1, j, j+1) if 0 <= k < J)

    checks = {
        "B_formula": b == floor_formula and (brute is None or brute == counts),
        "0<=B<=rho": all(0 <= bi <= x for bi, x in zip(b, lam)),
        "Tr(rho-B)<delta/8": sum(x-bi for x, bi in zip(lam, b)) < grid.delta/8,
        "nested": all(distinct[i+1] < distinct[i] for i in range(len(distinct)-1)),
        "K<=rbar": len(distinct) <= grid.rbar,
        "sum_ranks_bound": sum(len(q) for q in distinct) <= min(
            Fraction(grid.rbar*(grid.rbar+1), 2), 16*grid.rbar/grid.delta),
        "good_margin": all(dist(x) >= margin for x in set(lam) if x),
    }
    return distinct, checks


def flag_functional(state, distinct):
    """lambda_Psi = sum_l sum_(i in Q_l) lam_i: the functional on L whose
    restriction to log H gives the phase prod_l det(R|_(Q_l))."""
    p, m = state.inst.algebra.p, state.inst.algebra.dim
    out = [0]*m
    for q in distinct:
        for i in q:
            out = [(u+v) % p for u, v in zip(out, state.atoms[i].lam)]
    return tuple(out)


def predicted_phase_failure(cover, inst, assignment):
    """Theory: with points s_k each using a Psi of functional lam_k, the in-coset
    phase at C = sum_j t^j C_j in hlift is sum_j sum_k s_k^j lam_k(C_j). It is
    nonzero for some C iff some basis vector of some h cap gamma_j gives a nonzero
    value. assignment: list of (s, lam)."""
    p, m = cover.p, cover.algebra.dim
    for j, basis in enumerate(cover.series, 1):
        for C in intersect(inst.log_h, basis, p, m) if inst.log_h else []:
            if sum(pow(s, j, p)*sum(a*b for a, b in zip(lam, C)) for s, lam in assignment) % p:
                return True
    return False


# ---------------------------------------------------------------- instances

@dataclass
class MixedCase:
    name: str
    state: MixedState
    delta_promise: Fraction
    rbar: int
    expect_ok: bool = True          # False for negative controls
    note: str = ""


def _left_mult_table(G):
    E = G.elements()
    return np.stack([G.encode(G.mul(E, E[z][None, :])) for z in range(G.order)], axis=1)
    # table[g, z] = index of g * z


def trace_distance_gap(state, lmul):
    """Float: min over g outside H of TD(rho, R(g) rho R(g)^+), and the argmin.
    rho lives on span(atoms); both states live on span(atoms, R(g) atoms)."""
    inst = state.inst
    G, p = inst.group, inst.algebra.p
    zeta = np.exp(2j*np.pi*np.arange(p)/p)
    nG = G.order
    U = np.stack([(a.vec @ zeta)/np.sqrt(a.norm2) for a in state.atoms], axis=1)
    lam = np.array([float(x) for x in state.weights])
    Hset = set(inst.subgroup.tolist())
    best, arg = np.inf, None
    for g in range(nG):
        if g in Hset:
            continue
        V = np.zeros_like(U)
        V[lmul[g]] = U                      # (R(g)u)[g*z] = u[z]
        Qm, _ = np.linalg.qr(np.hstack([U, V]))
        A, B = Qm.conj().T @ U, Qm.conj().T @ V
        diff = (A*lam) @ A.conj().T-(B*lam) @ B.conj().T
        td = 0.5*np.abs(np.linalg.eigvalsh(diff)).sum()
        if td < best:
            best, arg = td, g
    return (float(best) if arg is not None else None), arg


def _pick_cosets(inst, k, rng):
    """k distinct right cosets H x (as representatives x in L coordinates)."""
    G = inst.group
    H = G.decode(inst.subgroup)
    seen, reps = set(), []
    order = list(range(G.order))
    rng.shuffle(order)
    for idx in order:
        x = G.decode(np.array(idx))
        coset = frozenset(G.encode(G.mul(H, x[None, :])).tolist())
        if coset not in seen:
            seen.add(coset)
            reps.append(tuple(int(v) for v in x))
            if len(reps) == k:
                break
    return reps


WEIGHT_PROFILES = {
    # nonflat; degenerate pair; tail below w for any delta <= 1/2 with rbar >= 4
    "A": [Fraction(2, 5), Fraction(1, 4), Fraction(1, 4), Fraction(99, 1000), Fraction(1, 1000)],
    "B": [Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)],
    # two eigenvalues 1/100 apart: closer than w = 1/96 at delta = 1/2, rbar = 3,
    # so the offset decides whether they share a flag level
    "C": [Fraction(41, 100), Fraction(2, 5), Fraction(19, 100)],
}


def build_state(inst, profile, rng, label="", mix=None):
    """Orthogonal H-eigenvectors on random distinct (right coset, character)
    pairs. With mix (profiles A and C by default) the two TOP eigenvectors are
    u_a + u_b and u_a - u_b for atoms with one character on two cosets, so they
    overlap with their translates for many g outside H; the degenerate pair of
    profile A spans an H-invariant plane."""
    weights = WEIGHT_PROFILES[profile]
    mix = profile in ("A", "C") if mix is None else mix
    funcs = character_functionals(inst)
    p, m = inst.algebra.p, inst.algebra.dim
    need = len(weights)+(1 if mix else 0)
    reps = _pick_cosets(inst, need, rng)
    pairs = [(x, coeffs) for x in reps for coeffs in product(range(p), repeat=len(funcs))]
    if len(pairs) < need or (mix and len(reps) < 2):
        return None

    def lam_of(coeffs):
        lam = [0]*m
        for c, f in zip(coeffs, funcs):
            lam = [(a+c*b) % p for a, b in zip(lam, f)]
        return tuple(lam)

    rng.shuffle(pairs)
    atoms = []
    if mix:
        x0, coeffs = pairs[0]
        x1 = next(x for x in reps if x != x0)
        pairs = [q for q in pairs if q not in ((x0, coeffs), (x1, coeffs))]
        ua, ub = make_atom(inst, x0, lam_of(coeffs)), make_atom(inst, x1, lam_of(coeffs))
        atoms += [combine(ua, ub, 1), combine(ua, ub, -1)]
    for x, coeffs in pairs[:len(weights)-len(atoms)]:
        atoms.append(make_atom(inst, x, lam_of(coeffs)))
    return MixedState(inst, atoms, list(weights),
                      label or f"profile {profile}{' mixed-top-pair' if mix else ''}")


def helmert(k):
    """Rows of an orthogonal integer matrix with first row all ones."""
    rows = [[1]*k]
    for j in range(1, k):
        rows.append([1]*j+[-j]+[0]*(k-j-1))
    return rows


def build_delocalized_state(inst, z, rng):
    """Profile D: atoms u_k on the p cosets H z^k x0 (z central, z^k outside H),
    one character, combined by the Helmert matrix. z fixes the full span but no
    smaller flag, so 0 < |phi(z^m)| < 1 and the finite-ell source is NOT already
    the coset state. Weights (p, p-1, ..., 1)/(p(p+1)/2)."""
    G, p = inst.group, inst.algebra.p
    zc = np.array(z, dtype=np.int64)
    if int(G.encode(zc)) in set(inst.subgroup.tolist()):
        return None
    funcs = character_functionals(inst)
    lam = [0]*inst.algebra.dim
    for f in funcs:
        c = rng.randrange(p)
        lam = [(u+c*v) % p for u, v in zip(lam, f)]
    x0 = np.array(_pick_cosets(inst, 1, rng)[0], dtype=np.int64)
    atoms, cur = [], x0
    for _ in range(p):
        atoms.append(make_atom(inst, tuple(int(v) for v in cur), tuple(lam)))
        cur = G.mul(zc, cur)
    vecs = []
    for row in helmert(p):
        vec = sum(c*u.vec for c, u in zip(row, atoms))
        vecs.append(Atom(tuple(lam), cyc_canon(vec), sum(c*c for c in row)*atoms[0].norm2,
                         tuple(u.cosets[0] for u in atoms)))
    total = p*(p+1)//2
    weights = [Fraction(p-k, total) for k in range(p)]
    return MixedState(inst, vecs, weights, f"profile D delocalized z={tuple(z)}")


def heis_subgroups():
    return [("trivial", ()), ("<x> non-normal", ((1, 0, 0),)), ("<y+z> non-normal", ((0, 1, 1),)),
            ("<x+2y+z> non-normal", ((1, 2, 1),)), ("Z(G)", ((0, 0, 1),)),
            ("<x,z> normal", ((1, 0, 0), (0, 0, 1)))]


def n4_subgroups():
    return [("<e2> non-normal", ((0, 1, 0, 0),)), ("<e1+e3> non-normal", ((1, 0, 1, 0),)),
            ("<e2,e4> non-normal", ((0, 1, 0, 0), (0, 0, 0, 1))), ("Z(G)", ((0, 0, 0, 1),)),
            ("<e3,e4> = gamma_2", ((0, 0, 1, 0), (0, 0, 0, 1)))]


def groups(include_n4=True):
    out = [(heisenberg(3), heis_subgroups()), (heisenberg(5), heis_subgroups())]
    if include_n4:
        out.append((filiform4(5), n4_subgroups()))
    return out


# ---------------------------------------------------------------- the lifted source

@dataclass
class LiftedSource:
    """F(x) = prod_(s in S) phi(E_s x) on the cover, classified exactly."""
    support: np.ndarray     # indices x with F(x) == 1 exactly
    unit: np.ndarray        # all E_s x in Stab (exact)
    phase: np.ndarray       # exponent of F on `unit` (exact), -1 elsewhere
    value: np.ndarray       # complex F (float)
    max_off_modulus: float  # max |F| off the unit set


def lift_source(cover, inst, overlap, design):
    p = cover.p
    G = inst.group
    Gt = cover.stage_group(cover.c)
    elems = Gt.elements()
    unit = np.ones(Gt.order, dtype=bool)
    phase = np.zeros(Gt.order, dtype=np.int64)
    value = np.ones(Gt.order, dtype=complex)
    for s in design:
        img = G.encode(elems @ cover.evaluation_matrix(s) % p)
        unit &= overlap.unit[img]
        phase = (phase+np.where(overlap.unit[img], overlap.phase[img], 0)) % p
        value *= overlap.complex_value[img]
    phase = np.where(unit, phase, -1)
    off = ~unit
    return LiftedSource(np.nonzero(unit & (phase == 0))[0], unit, phase, value,
                        float(np.abs(value[off]).max()) if off.any() else 0.0)


def lifted_exact_state(cover, lifted):
    """Ideal ell -> infinity source as an ExactState: c(y) = conj F(y)^ell -> the
    in-coset phase (zero for a correct design). rho[u, v] = c(u^-1 v)/|G~|."""
    p = cover.p
    Gt = cover.stage_group(cover.c)
    v = np.zeros((Gt.order, p), dtype=np.int64)
    on = np.nonzero(lifted.unit)[0]
    v[on, (-lifted.phase[on]) % p] = 1
    return ExactState(cover.c, Fraction(1), cyc_canon(v))


class SourceExactBackend(ExactBackend):
    """The unchanged exact core, with its oracle source replaced by a given state."""

    def __init__(self, cover, state):
        super().__init__(cover)
        self._state = state

    def prepare_source(self, oracle):
        return self._state, {"lifted_order": int(np.count_nonzero(self._state.v.any(axis=1))),
                             "source": "mixed_spectral_design"}


class SourceDenseBackend(DenseBackend):
    def __init__(self, cover, rho):
        super().__init__(cover)
        self._rho = rho

    def prepare_source(self, oracle):
        return (self.cover.c, self._rho), {"source": "mixed_spectral_design_finite_ell"}


def _no_oracle(_x):
    raise AssertionError("the mixed-source run must not query the oracle")


def dense_sigma(cover, lifted, ell):
    """sigma_ell[a, b] = F(b^-1 * a)^ell / |G~|."""
    Gt = cover.stage_group(cover.c)
    E = Gt.elements()
    idx = np.stack([Gt.encode(Gt.mul(Gt.inv(E[b])[None, :], E)) for b in range(Gt.order)], axis=1)
    return (lifted.value[idx]**ell)/Gt.order          # idx[a, b] = b^-1 * a


def dense_coset_state(cover, d, indices):
    G = cover.stage_group(d)
    E = G.elements()
    member = np.zeros(G.order, dtype=bool)
    member[indices] = True
    diff = np.stack([G.encode(G.mul(G.inv(E[u])[None, :], E)) for u in range(G.order)])
    return member[diff].astype(complex)/G.order


def trace_distance(a, b):
    return 0.5*float(np.abs(np.linalg.eigvalsh(a-b)).sum())


# ---------------------------------------------------------------- one case

def analyse_case(cover, case, lmul, design, *, offsets=None, run_core=True, seed=0,
                 whole_support=False, gap=None):
    """Exact part (i) over every offset, then the exact core on one or more offsets."""
    st, inst = case.state, case.state.inst
    p = cover.p
    grid = make_grid(case.delta_promise, case.rbar)
    td_min, td_arg = gap if gap is not None else trace_distance_gap(st, lmul)
    out = {"case": case.name, "instance": inst.name, **inst.flags(), "rank": st.rank,
           "weights": [str(x) for x in st.weights], "delta_promise": str(case.delta_promise),
           "true_min_td": td_min, "promise_true": td_min is None or td_min >= float(case.delta_promise),
           "rbar": case.rbar, "w": str(grid.w), "J": grid.J, "M0": grid.M0, "design": list(design),
           "expect_ok": case.expect_ok, "note": case.note}
    Hset = np.zeros(inst.group.order, dtype=bool)
    Hset[inst.subgroup] = True
    cache, per_offset, bad_margin = {}, [], 0
    for a in range(grid.M0):
        distinct, checks = flags_for_offset(st, grid, a)
        if whole_support:
            distinct = [frozenset(i for i, x in enumerate(st.weights) if x)]
        bad_margin += not checks["good_margin"]
        key = tuple(sorted(tuple(sorted(q)) for q in distinct))
        if key not in cache:
            flags = [[st.atoms[i] for i in sorted(q)] for q in distinct]
            ov = flag_overlap(inst, flags, lmul)
            # predicted phase on H: prod_l det(R|Q_l) = prod over atoms of chi_i^(#flags containing i)
            Hc = inst.group.decode(inst.subgroup)
            pred = np.zeros(len(Hc), dtype=np.int64)
            for q in distinct:
                for i in q:
                    pred = (pred+Hc @ np.array(st.atoms[i].lam)) % p
            off = ~Hset
            cache[key] = {
                "ranks": [len(q) for q in distinct],
                "ray_stabilizer_equals_H": bool((ov.unit == Hset).all()),
                "phase_is_det_character": bool((ov.phase[inst.subgroup] == pred).all()),
                "max_off_H_overlap": float(ov.modulus[off].max()) if off.any() else None,
                "_ov": ov,
            }
        per_offset.append({"a": a, "flags": key, **{k: v for k, v in checks.items()}})
    gap_bound = 1-float(case.delta_promise)**2/8
    summary = {k: v for k, v in out.items()}
    summary.update({
        "offsets": grid.M0, "distinct_flag_sets": len(cache),
        "bad_margin_offsets": bad_margin, "bad_margin_within_rbar": bad_margin <= case.rbar,
        "all_offsets_identities": all(all(v for k, v in r.items() if k not in ("a", "flags", "good_margin"))
                                      for r in per_offset),
        "all_offsets_ray_stabilizer_H": all(c["ray_stabilizer_equals_H"] for c in cache.values()),
        "all_offsets_phase_det_character": all(c["phase_is_det_character"] for c in cache.values()),
        "all_offsets_gap": all(c["max_off_H_overlap"] is None or c["max_off_H_overlap"] <= gap_bound+1e-12
                               for c in cache.values()),
        "flag_sets": [{k: v for k, v in c.items() if k != "_ov"} for c in cache.values()],
        "offsets_wrong_stabilizer": sum(not cache[r["flags"]]["ray_stabilizer_equals_H"] for r in per_offset),
    })
    rng = random.Random(seed)
    if offsets is None:     # one random offset per distinct flag set, at most three
        reps = {}
        for a in rng.sample(range(grid.M0), grid.M0):
            reps.setdefault(per_offset[a]["flags"], a)
        chosen = sorted(reps.values())[:3]
    else:
        chosen = offsets
    runs = []
    for a in chosen:
        key = per_offset[a]["flags"]
        ov = cache[key]["_ov"]
        lifted = lift_source(cover, inst, ov, design)
        expected = expected_stage_indices(cover, inst.log_h, cover.c)
        flagsets = [frozenset(q) for q in key]
        run = {"offset": a, "flag_ranks": cache[key]["ranks"],
               "theory_predicts_phase_failure": predicted_phase_failure(
                   cover, inst, [(s, flag_functional(st, flagsets)) for s in design]),
               "unit_set_equals_exp_hlift": bool(np.array_equal(np.nonzero(lifted.unit)[0], expected)),
               "in_coset_phases_all_zero": bool((lifted.phase[lifted.unit] == 0).all()),
               "max_off_coset_modulus": lifted.max_off_modulus,
               "registers_per_Psi": int(sum(ov.ranks))}
        if run_core:
            state = lifted_exact_state(cover, lifted)
            backend = SourceExactBackend(cover, state)
            try:
                recovered, rec = run_rees(cover, _no_oracle, backend, seed=seed+a, keep_states=True)
                g = grade_run(cover, inst, recovered, rec, backend)
                run.update(check_raised=None, recovered_equals_log_H=g["recovered_equals_log_H"],
                           recovered_basis=g["recovered_basis"],
                           stage_outputs_equal_rho_H_d=stage_outputs_correct(cover, inst, rec),
                           laws_uniform=all(s["every_source_law_uniform_on_K_perp"]
                                            for s in g["stages"].values()),
                           top_sources=rec.top_sources)
            except ArithmeticError as exc:
                run.update(check_raised=str(exc), recovered_equals_log_H=False,
                           stage_outputs_equal_rho_H_d=False, laws_uniform=False)
        runs.append(run)
    summary["runs"] = runs
    summary["source_correct"] = (summary["all_offsets_ray_stabilizer_H"]
                                 and summary["all_offsets_phase_det_character"]
                                 and all(r["unit_set_equals_exp_hlift"] and r["in_coset_phases_all_zero"]
                                         for r in runs))
    summary["end_to_end_ok"] = summary["source_correct"] and all(
        r.get("recovered_equals_log_H") and r.get("stage_outputs_equal_rho_H_d") and r.get("laws_uniform")
        for r in runs) if run_core else None
    return summary


# ---------------------------------------------------------------- positive cases

def positive_cases(alg, subgroups, seed=1):
    """Two nonflat states per H, each with a TRUE promise delta = floor of the
    measured minimum (to 1/64), rbar = rank (profile A) or rank + 1 (B)."""
    rng = random.Random(seed*1000+alg.p*10+alg.dim)
    cover = make_cover(alg)
    G = HiddenInstance("probe", alg, ()).group
    lmul = _left_mult_table(G)
    cases = []
    for hname, gens in subgroups:
        inst = HiddenInstance(f"{alg.name} H={hname}", alg, gens)
        for profile, slack in (("A", 0), ("B", 1), ("C", 0)):
            for _ in range(20):
                st = build_state(inst, profile, rng)
                if st is None:
                    break
                if not all(check_atom_is_eigenvector(inst, a, lmul) for a in st.atoms) \
                        or not atoms_orthonormal_up_to_norm(st.atoms, alg.p):
                    raise ArithmeticError("atom construction failed")
                td, arg = trace_distance_gap(st, lmul)
                if td is None or td > 1e-6:
                    break
            else:
                raise RuntimeError(f"no state with a positive gap for {inst.name}")
            if st is None:
                continue
            delta = Fraction(1, 2) if td is None else min(Fraction(1, 2), Fraction(int(td*64*0.999), 64))
            if delta <= 0:
                delta = Fraction(int(td*4096*0.999), 4096)
            cases.append((MixedCase(f"{inst.name} {st.label}", st, delta, st.rank+slack), (td, arg)))
        center = tuple(int(i == alg.dim-1) for i in range(alg.dim))
        if int(G.encode(np.array(center))) in set(inst.subgroup.tolist()):
            continue                       # H contains the central z: no profile D
        st = build_delocalized_state(inst, center, rng)
        if not all(check_atom_is_eigenvector(inst, a, lmul) for a in st.atoms) \
                or not atoms_orthonormal_up_to_norm(st.atoms, alg.p):
            raise ArithmeticError("delocalized construction failed")
        td, arg = trace_distance_gap(st, lmul)
        if td is None or td < 1e-6:
            raise RuntimeError(f"profile D has no gap for {inst.name}")
        delta = Fraction(int(td*4096*0.999), 4096)
        cases.append((MixedCase(f"{inst.name} {st.label}", st, delta, st.rank), (td, arg)))
    return cover, lmul, cases


# ---------------------------------------------------------------- negative controls

def _cyclic_state(inst, z, eps, rng):
    """p atoms R(z^k) u on the cosets H z^k x with eigenvalues base + k*eps, where
    z normalizes H and z^k is not in H. Stab(rho) = H; the support is z-invariant."""
    G, p = inst.group, inst.algebra.p
    funcs = character_functionals(inst)
    lam = [0]*inst.algebra.dim
    for f in funcs:
        c = rng.randrange(p)
        lam = [(a+c*b) % p for a, b in zip(lam, f)]
    x = _pick_cosets(inst, 1, rng)[0]
    atoms, zk = [], np.zeros(len(z), dtype=np.int64)
    for k in range(p):
        xk = tuple(int(v) for v in G.mul(zk, np.array(x)))
        atoms.append(make_atom(inst, xk, tuple(lam)))
        zk = G.mul(zk, np.array(z))
    base = (1-eps*Fraction(p*(p-1), 2))/p
    weights = [base+k*eps for k in range(p)]
    return MixedState(inst, atoms, weights, f"cyclic z={tuple(z)} eps={eps}")


def negative_controls(seed=3):
    """Each control must make the substitution FAIL a check.

    (a) whole support: the flat top wedge of supp(rho) for a nonflat rho whose
        support is invariant under z outside H (the withdrawn shortcut);
    (b) overstated delta: true gap ~ (p-1)eps is tiny, the promise says 1/4, so
        rounding merges the p eigenvalues and z fixes every flag;
    (c) no design: Psi fed through the c-point lift (points 1..c) of
        lem:copy-lift, so the determinant character is not cancelled;
    (d) mixed offsets: the design block uses Psi from two different offsets
        whose determinant characters differ (rem:mixed-source: "the same
        offset must be used for every copy")."""
    rng = random.Random(seed)
    rows = []
    for alg in (heisenberg(3), heisenberg(5)):
        cover = make_cover(alg)
        design = DESIGNS[(alg.p, cover.c)]
        inst = HiddenInstance(f"{alg.name} H=<x> non-normal", alg, ((1, 0, 0),))
        lmul = _left_mult_table(inst.group)
        z = (0, 0, 1)
        # (a) and (b)
        st = _cyclic_state(inst, z, Fraction(1, 2000), rng)
        gap = trace_distance_gap(st, lmul)
        for kind, delta, whole in (("whole_support_wedge", Fraction(1, 2), True),
                                   ("overstated_delta", Fraction(1, 2), False),
                                   ("true_delta_same_state", None, False)):
            dl = delta if delta is not None else Fraction(int(gap[0]*4096*0.999), 4096)
            case = MixedCase(f"{inst.name} {kind}", st, dl, st.rank, expect_ok=(kind == "true_delta_same_state"))
            grid = make_grid(dl, st.rank)
            offs = sorted(random.Random(seed).sample(range(grid.M0), 3))
            if kind == "overstated_delta":      # also one offset where all p levels merge
                merged = [a for a in range(grid.M0) if len(flags_for_offset(st, grid, a)[0]) == 1]
                offs = sorted(set(offs[:2]+merged[:1]))
            res = analyse_case(cover, case, lmul, design, offsets=offs, whole_support=whole, gap=gap, seed=seed)
            row = _control_row(kind, res)
            row["offsets_with_wrong_stabilizer"] = res.get("offsets_wrong_stabilizer")
            rows.append(row)
        # (c) no design: points 1..c; the expected outcome comes from the moment formula
        points = tuple(range(1, cover.c+1))
        for hname, gens in (("Z(G)", ((0, 0, 1),)), ("<x> non-normal", ((1, 0, 0),))):
            ih = HiddenInstance(f"{alg.name} H={hname}", alg, gens)
            for _ in range(30):     # want a state whose flag character is nontrivial on H
                stc = build_state(ih, "A", rng)
                gapc = trace_distance_gap(stc, lmul)
                if gapc[0] is None or gapc[0] < 1e-6:
                    continue
                dc = min(Fraction(1, 2), Fraction(int(gapc[0]*64*0.999), 64))
                grid = make_grid(dc, stc.rank)
                a = random.Random(seed).randrange(grid.M0)
                lam = flag_functional(stc, flags_for_offset(stc, grid, a)[0])
                if any(sum(u*v for u, v in zip(lam, h)) % alg.p for h in ih.log_h):
                    break
            predicted = predicted_phase_failure(cover, ih, [(s, lam) for s in points])
            case = MixedCase(f"{ih.name} no_design", stc, dc, stc.rank, expect_ok=not predicted,
                             note="expected outcome from sum_j (sum_s s^j) lam(h cap gamma_j)")
            res = analyse_case(cover, case, lmul, points, offsets=[a], gap=gapc, seed=seed)
            rows.append(_control_row("no_design_c_point_lift", res))
        # (d) mixed offsets inside one design block
        rows.append(mixed_offset_control(alg, cover, design, lmul, rng))
    return rows


def _control_row(kind, res):
    runs = res["runs"]
    failed = (not res["all_offsets_ray_stabilizer_H"]
              or any(not r["unit_set_equals_exp_hlift"] or not r["in_coset_phases_all_zero"]
                     or not r.get("recovered_equals_log_H") or not r.get("stage_outputs_equal_rho_H_d")
                     for r in runs))
    return {"control": kind, "case": res["case"], "expect_ok": res["expect_ok"],
            "promise_true": res["promise_true"], "true_min_td": res["true_min_td"],
            "delta_promise": res["delta_promise"],
            "ray_stabilizer_H_every_offset": res["all_offsets_ray_stabilizer_H"],
            "runs": [{k: r.get(k) for k in ("offset", "flag_ranks", "unit_set_equals_exp_hlift",
                                             "in_coset_phases_all_zero", "recovered_equals_log_H",
                                             "stage_outputs_equal_rho_H_d", "check_raised", "recovered_basis")}
                     for r in runs],
            "failure_detected": failed,
            "matches_prediction": failed == (not res["expect_ok"])}


def mixed_offset_control(alg, cover, design, lmul, rng):
    """Find two offsets with different flag characters; alternate them across
    the design points and check the in-coset phase."""
    inst = HiddenInstance(f"{alg.name} H=<x> non-normal", alg, ((1, 0, 0),))
    for _ in range(40):
        st = build_state(inst, "C", rng)
        td, _ = trace_distance_gap(st, lmul)
        delta = min(Fraction(1, 2), Fraction(int(td*64*0.999), 64))
        grid = make_grid(delta, st.rank)
        by_char = {}
        Hc = inst.group.decode(inst.subgroup)
        for a in range(grid.M0):
            distinct, _ = flags_for_offset(st, grid, a)
            char = np.zeros(len(Hc), dtype=np.int64)
            for q in distinct:
                for i in q:
                    char = (char+Hc @ np.array(st.atoms[i].lam)) % alg.p
            by_char.setdefault(tuple(char.tolist()), (a, distinct))
        if len(by_char) >= 2:
            (a1, f1), (a2, f2) = list(by_char.values())[:2]
            break
    else:
        return {"control": "mixed_offsets", "case": inst.name, "expect_ok": False,
                "failure_detected": None, "matches_prediction": False, "note": "no pair of offsets found"}
    ov1 = flag_overlap(inst, [[st.atoms[i] for i in sorted(q)] for q in f1], lmul)
    ov2 = flag_overlap(inst, [[st.atoms[i] for i in sorted(q)] for q in f2], lmul)
    p = cover.p
    G, Gt = inst.group, cover.stage_group(cover.c)
    elems = Gt.elements()
    unit = np.ones(Gt.order, dtype=bool)
    phase = np.zeros(Gt.order, dtype=np.int64)
    for k, s in enumerate(design):
        ov = ov1 if k % 2 == 0 else ov2
        img = G.encode(elems @ cover.evaluation_matrix(s) % p)
        unit &= ov.unit[img]
        phase = (phase+np.where(ov.unit[img], ov.phase[img], 0)) % p
    bad = bool((phase[unit] != 0).any())
    predicted = predicted_phase_failure(cover, inst, [
        (s, flag_functional(st, f1 if k % 2 == 0 else f2)) for k, s in enumerate(design)])
    # correct runs for each single offset, for comparison
    single = []
    for ov in (ov1, ov2):
        lf = lift_source(cover, inst, ov, design)
        single.append(bool((lf.phase[lf.unit] == 0).all()))
    lifted = LiftedSource(np.nonzero(unit & (phase == 0))[0], unit, np.where(unit, phase, -1),
                          np.ones(Gt.order, dtype=complex), 0.0)
    state = lifted_exact_state(cover, lifted)
    backend = SourceExactBackend(cover, state)
    run = {}
    try:
        recovered, rec = run_rees(cover, _no_oracle, backend, seed=11, keep_states=True)
        run = {"recovered_equals_log_H": rref(recovered, p) == rref(inst.log_h, p),
               "stage_outputs_equal_rho_H_d": stage_outputs_correct(cover, inst, rec), "check_raised": None}
    except ArithmeticError as exc:
        run = {"recovered_equals_log_H": False, "stage_outputs_equal_rho_H_d": False, "check_raised": str(exc)}
    failed = bad or not run["stage_outputs_equal_rho_H_d"]
    return {"control": "mixed_offsets", "case": f"{inst.name} {st.label}", "expect_ok": not predicted,
            "predicted_failure": predicted,
            "offsets": [a1, a2], "flag_ranks": [[len(q) for q in f1], [len(q) for q in f2]],
            "single_offset_phases_cancel": single, "alternating_phase_nonzero_somewhere": bad,
            "runs": [run], "failure_detected": failed, "matches_prediction": failed == predicted}


# ---------------------------------------------------------------- float cross-checks

def wedge_identity_check(seed=0, trials=6):
    """Heis(F_3), d = 27: <Omega|R(g)^(tensor r)|Omega> from explicit
    antisymmetric tensors equals det(B^+ R(g) B)/det(B^+ B), r = 2, 3."""
    rng = np.random.default_rng(seed)
    alg = heisenberg(3)
    inst = HiddenInstance("Heis(F_3) H=<x>", alg, ((1, 0, 0),))
    G = inst.group
    lmul = _left_mult_table(G)
    d, worst = G.order, 0.0
    for r in (2, 3):
        for _ in range(trials):
            B = rng.normal(size=(d, r))+1j*rng.normal(size=(d, r))
            omega = np.zeros(d**r, dtype=complex)
            for perm in permutations(range(r)):
                vec = np.array([1.0+0j])
                for i in perm:
                    vec = np.kron(vec, B[:, i])
                omega += _sign(perm)*vec
            omega /= np.linalg.norm(omega)
            g = int(rng.integers(G.order))
            P = np.zeros((d, d))
            P[lmul[g], np.arange(d)] = 1          # R(g) e_z = e_(g*z)
            moved = np.zeros((d,)*r, dtype=complex)
            moved[np.ix_(*([lmul[g]]*r))] = omega.reshape((d,)*r)
            lhs = np.vdot(omega, moved.ravel())
            rhs = np.linalg.det(B.conj().T @ P @ B)/np.linalg.det(B.conj().T @ B)
            worst = max(worst, abs(lhs-rhs))
    return worst


def circuit_check(seed=0):
    """Heis(F_3) cover (81 addresses): ONE design point, a rank-2 flag, explicit
    state sum_a |a> R(E_s a)^(tensor 2) |Omega> / 9, target traced out, versus
    the formula sigma[a, b] = phi(E_s(b^-1 * a))/81."""
    rng = random.Random(seed)
    alg = heisenberg(3)
    cover = make_cover(alg)
    inst = HiddenInstance("Heis(F_3) H=Z(G)", alg, ((0, 0, 1),))
    st = build_state(inst, "A", rng)
    G = inst.group
    lmul = _left_mult_table(G)
    basis = st.atoms[:2]          # the mixed pair u_a +- u_b
    ov = flag_overlap(inst, [basis], lmul)
    d, p = G.order, alg.p
    zeta = np.exp(2j*np.pi*np.arange(p)/p)
    B = np.stack([a.vec @ zeta for a in basis], axis=1)
    omega = np.kron(B[:, 0], B[:, 1])-np.kron(B[:, 1], B[:, 0])
    omega /= np.linalg.norm(omega)
    Gt = cover.stage_group(cover.c)
    E = Gt.elements()
    s = 2
    img = G.encode(E @ cover.evaluation_matrix(s) % p)
    psi = np.zeros((Gt.order, d*d), dtype=complex)
    for a in range(Gt.order):
        perm = lmul[img[a]]
        # (R(g) tensor R(g)) e_(y1,y2) = e_(g y1, g y2)
        idx = (perm[:, None]*d+perm[None, :]).ravel()
        out = np.zeros(d*d, dtype=complex)
        out[idx] = omega
        psi[a] = out
    sigma = psi.conj() @ psi.T/Gt.order          # sigma[b, a]... take transpose below
    sigma = sigma.T                               # sigma[a, b] = <U_b Omega | U_a Omega>/N
    lf = LiftedSource(None, None, None, ov.complex_value[img], 0.0)
    # formula with one point: F(x) = phi(E_s x)
    formula = dense_sigma(cover, lf, 1)
    homo = all((G.mul(G.inv(G.decode(img[b]))[None, :], G.decode(img[a])[None, :])
                == G.decode(img[Gt.encode(Gt.mul(Gt.inv(E[b])[None, :], E[a][None, :]))[0]])[None, :]).all()
               for a in range(Gt.order) for b in range(Gt.order))
    return float(np.abs(sigma-formula).max()), homo


def finite_ell_dense(cover, case, lmul, design, ells, seed=0):
    """Float: build sigma_ell, check TD(sigma_ell, rho_Htilde) <= sqrt(N)(1-gamma)^ell/2,
    the top label law TV <= that TD, and run the unchanged DenseBackend core."""
    st, inst = case.state, case.state.inst
    grid = make_grid(case.delta_promise, case.rbar)
    a = random.Random(seed).randrange(grid.M0)
    distinct, _ = flags_for_offset(st, grid, a)
    ov = flag_overlap(inst, [[st.atoms[i] for i in sorted(q)] for q in distinct], lmul)
    lifted = lift_source(cover, inst, ov, design)
    expected = expected_stage_indices(cover, inst.log_h, cover.c)
    target = dense_coset_state(cover, cover.c, expected)
    N = cover.stage_group(cover.c).order
    gamma = float(case.delta_promise)**2/8
    rows = []
    for ell in ells:
        sigma = dense_sigma(cover, lifted, ell)
        td = trace_distance(sigma, target)
        bound = np.sqrt(N)*(1-gamma)**ell/2
        backend = SourceDenseBackend(cover, sigma)
        recovered, rec = run_rees(cover, _no_oracle, backend, seed=seed, keep_states=True)
        top_law = rec.label_laws[cover.c][0]
        ideal = SourceExactBackend(cover, lifted_exact_state(cover, lifted)).label_probabilities(
            lifted_exact_state(cover, lifted))
        tv = 0.5*sum(abs(float(top_law.get(k, 0))-float(ideal.get(k, 0))) for k in set(top_law) | set(ideal))
        stage_td = []
        for d, states in rec.stage_states.items():
            tgt = dense_coset_state(cover, d, expected_stage_indices(cover, inst.log_h, d))
            stage_td += [trace_distance(s[1], tgt) for s in states]
        rows.append({"ell": ell, "td_sigma_rho_Htilde": td, "bound": float(bound),
                     "td_within_bound": td <= bound+1e-12, "top_label_tv": tv,
                     "top_label_tv_within_td": tv <= td+1e-9,
                     "recovered_equals_log_H": rref(recovered, cover.p) == rref(inst.log_h, cover.p),
                     "max_stage_output_td": max(stage_td) if stage_td else 0.0})
    return {"case": case.name, "offset": a, "rows": rows}


# ---------------------------------------------------------------- report

def report(include_n4=True, seed=1, n4_runs=True):
    t0 = time.time()
    positives, dense_rows = [], []
    for alg, subgroups in groups(include_n4):
        cover, lmul, cases = positive_cases(alg, subgroups, seed=seed)
        design = DESIGNS[(alg.p, cover.c)]
        if not check_design(design, alg.p, cover.c):
            raise ArithmeticError("design moments do not vanish")
        for case, gap in cases:
            run_core = n4_runs or alg.dim == 3
            positives.append(analyse_case(cover, case, lmul, design, gap=gap, seed=seed, run_core=run_core))
        if alg.dim == 3:
            for case, gap in [c for c in cases if "profile D" in c[0].name]+cases[:1]:
                dense_rows.append(finite_ell_dense(cover, case, lmul, design, (1, 4, 16, 64), seed=seed))
    controls = negative_controls()
    wedge_err = wedge_identity_check()
    circ_err, homo = circuit_check()
    core_rows = [r for r in positives if r["end_to_end_ok"] is not None]
    return {
        "status": "exact_small_instance_substitution_with_reference_spectra_not_a_receiver",
        "spectrum_supplied_as_reference": True, "part_ii_instruments_simulated": False,
        "coherent_receiver_implemented": False,
        "cases": len(positives), "core_runs": sum(len(r["runs"]) for r in core_rows),
        "all_promises_true": all(r["promise_true"] for r in positives),
        "all_part_i_identities_every_offset": all(r["all_offsets_identities"] for r in positives),
        "all_bad_margin_within_rbar": all(r["bad_margin_within_rbar"] for r in positives),
        "all_ray_stabilizers_H_every_offset": all(r["all_offsets_ray_stabilizer_H"] for r in positives),
        "all_phases_det_character": all(r["all_offsets_phase_det_character"] for r in positives),
        "all_gaps_delta2_over_8": all(r["all_offsets_gap"] for r in positives),
        "all_sources_correct": all(r["source_correct"] for r in positives),
        "all_end_to_end_ok": all(r["end_to_end_ok"] for r in core_rows),
        "dense_finite_ell": dense_rows,
        "dense_all_within_bound": all(x["td_within_bound"] and x["top_label_tv_within_td"]
                                      for d in dense_rows for x in d["rows"]),
        "negative_controls": controls,
        "negative_controls_match_prediction": all(c["matches_prediction"] for c in controls),
        "wedge_identity_max_error": wedge_err, "circuit_formula_max_error": circ_err,
        "evaluation_homomorphism_all_pairs_heis3": homo,
        "positives": positives, "seconds": round(time.time()-t0, 1),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--no-n4", action="store_true", help="skip n4(F_5)")
    parser.add_argument("--out", help="write JSON here")
    args = parser.parse_args()
    res = report(include_n4=not args.no_n4)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(json.dumps(res, indent=1, default=str)+"\n")
    for r in res["positives"]:
        print(r["case"], "| delta", r["delta_promise"], "td", round(r["true_min_td"] or -1, 4),
              "| flag sets", r["distinct_flag_sets"], "| source", r["source_correct"],
              "| e2e", r["end_to_end_ok"])
    for c in res["negative_controls"]:
        print("control", c["control"], c["case"], "failure_detected", c["failure_detected"],
              "matches", c["matches_prediction"])
    for k, v in res.items():
        if not isinstance(v, (list, dict)):
            print(k, v)


if __name__ == "__main__":
    main()
