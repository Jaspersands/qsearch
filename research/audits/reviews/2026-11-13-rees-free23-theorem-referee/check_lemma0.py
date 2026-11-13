"""Checks of the group code and of Lemma 0 on TRUE copies (AI-written, pending human review).
  1. BCH associativity; random automorphisms are group automorphisms (sigma(ab) = sigma(a)sigma(b)).
  2. For random hard H (and random sigma applied to the labelled copy), the front-end x-state is flat with
     root-of-unity ratios, its exponent is a cubic with no constant term, and it equals Lemma 0's
     (A1 x + A2 x^2 + A3 x^3)/f(e) under ONE sign convention for all copies; the base point is a global phase.
  3. Spoiled copies (lam.e = 0) are recorded separately (Lemma 0 does not apply).
Usage: python check_lemma0.py p ncopies seed"""
import sys, numpy as np
from ref_core import *

p, ncop, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
F = Field(p); G = Group(F); rng = np.random.default_rng(seed)
a, b, c = rng.integers(0, p, (3, 400, 5))
assert (bch(bch(a, b, F), c, F) == bch(a, bch(b, c, F), F)).all()
for _ in range(20):
    S = random_aut(F, rng)
    assert ((bch(a, b, F) @ S.T) % p == bch((a @ S.T) % p, (b @ S.T) % p, F)).all()
print('p=%d: BCH associative on 400 triples; 20 random automorphisms are homomorphisms' % p)

conv_ok = {c: 0 for c in CONVS}; n_ok = n_spoiled = spo_delta = spo_deriv0 = 0; sectors = {}; nonflat = 0
for it in range(ncop):
    while True:
        eta = rng.integers(0, p, 5)
        if eta[0] % p or eta[1] % p: break
    S = random_aut(F, rng) if it % 2 else None
    lam, psi = labelled_copy(G, eta, rng, S)
    etap = (S @ eta) % p if S is not None else eta
    if lam == (0, 0): continue
    fe = FrontEnd(F, lam, rng); y, phi = fe.run(psi, rng)
    if fe.f(etap[:2]) == 0:
        n_spoiled += 1
        # spoiled copy: x-state should be a delta at x0 with (A1 + 2 A2 x0 + 3 A3 x0^2)(theta) = 0 (convention CONV)
        sup = np.flatnonzero(np.abs(phi) > 1e-9)
        A = [int(a @ etap) % p for a in fe.A_forms((-1, -1, 1))]
        if len(sup) == 1:
            x0 = int(sup[0]); spo_delta += 1
            spo_deriv0 += int((A[0] + 2 * A[1] * x0 + 3 * A[2] * x0 * x0) % p == 0)
        continue
    sectors[y[2]] = sectors.get(y[2], 0) + 1
    try: E = phase_exponents(phi, F)
    except AssertionError: nonflat += 1; continue
    for cv in CONVS:
        conv_ok[cv] += int((lemma0_predict(fe, etap, cv, F) - E).any() == False)
    n_ok += 1
print('p=%d: %d non-spoiled copies (%d spoiled skipped), non-flat %d, label-sector l counts %s' % (p, n_ok, n_spoiled, nonflat, sectors))
print('  spoiled copies: x-state a single delta in %d/%d; at the delta, d/dx[f(e)P] = A1 + 2A2 x0 + 3A3 x0^2 = 0 in %d/%d' % (spo_delta, n_spoiled, spo_deriv0, spo_delta))
print('  conventions matching ALL copies:', [c for c, v in conv_ok.items() if v == n_ok], ' (counts %s)' % conv_ok)

# base-point independence: same H, same label, same chart, same y => phi equal up to global phase
eta = np.array([1, 2, 3, 4, 5]) % p; agree = tot = 0
for it in range(ncop):
    lam, psi = labelled_copy(G, eta, rng)
    if lam == (0, 0): continue
    fe = FrontEnd(F, lam, rng)
    if fe.f(eta[:2]) == 0: continue
    y, phi = fe.run(psi, rng)
    E = phase_exponents(phi, F)
    for cv in [c for c, v in conv_ok.items() if v == n_ok]:
        agree += int(not (lemma0_predict(fe, eta, cv, F) - E).any()); tot += 1
print('  fixed H, fresh base points: %d/%d agree with the closed form' % (agree, tot))
