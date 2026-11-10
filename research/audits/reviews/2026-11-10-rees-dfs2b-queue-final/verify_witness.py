"""Independent check of two-level contraction witnesses (kappa, p, g, beta, alpha).

AI-written (10 Nov 2026), pending human review. Written from the definition in
appendix-schedule2.tex (subsection app:s2-contraction); shares no code with dfs2b.c.

Definition used. Let kappa | p - 1, h = (p-1)/kappa, Q_0 = {x^kappa : x != 0}. g is a coset
generator if g^h has multiplicative order exactly kappa; put z_m = g^m. Let
W = {w in F_p^kappa : sum_m z_m w_m = 0}. A two-level contraction is C in F_p^{kappa x kappa}
with every C_ij in Q_0 or 0, C_00 != 0, and sum_ij C_ij X_ij = 0 for all X in W (x) W.
The witness (beta, alpha) defines C_ij = z_i z_j (alpha_j + beta_i) (decoupled form).

Checks, all exact:
 (1) p prime, p = 1 mod kappa, all entries in [0, p);
 (2) g^h has order exactly kappa (so g is a coset generator);
 (3) every C_ij is 0 or satisfies C_ij^h = 1 (i.e. lies in Q_0), and C_00 != 0;
 (4) C annihilates W (x) W, tested on the basis w^(k) = e_k - z_k e_0, k = 1..kappa-1
     (z_0 = 1), i.e. sum_ij C_ij w^(k)_i w^(l)_j = 0 for all k, l. This does not use the
     normal-form lemma.
Usage: python -I verify_witness.py witnesses.json > verify_witness.out
"""
import json, sys


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_factors(n):
    out, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def check(k, p, g, beta, alpha):
    errs = []
    if not is_prime(p):
        errs.append("p not prime")
    if (p - 1) % k:
        errs.append("p != 1 mod kappa")
    if len(beta) != k or len(alpha) != k or any(not 0 <= x < p for x in beta + alpha):
        errs.append("bad vector length or range")
        return errs
    h = (p - 1) // k
    zeta = pow(g, h, p)
    if pow(zeta, k, p) != 1 or any(pow(zeta, k // q, p) == 1 for q in prime_factors(k)):
        errs.append("g is not a coset generator")
    z = [pow(g, m, p) for m in range(k)]
    C = [[z[i] * z[j] * (alpha[j] + beta[i]) % p for j in range(k)] for i in range(k)]
    if C[0][0] == 0:
        errs.append("C_00 = 0")
    for i in range(k):
        for j in range(k):
            c = C[i][j]
            if c and pow(c, h, p) != 1:
                errs.append(f"C_{i}{j} not in Q_0")
    for a in range(1, k):
        for b in range(1, k):
            # w^(a) = e_a - z_a e_0, w^(b) = e_b - z_b e_0
            s = (C[a][b] - z[b] * C[a][0] - z[a] * C[0][b] + z[a] * z[b] * C[0][0]) % p
            if s:
                errs.append(f"W(x)W pairing nonzero at ({a},{b})")
    return errs


ws = json.load(open(sys.argv[1]))
bad, seen = 0, set()
for w in ws:
    e = check(w["k"], w["p"], w["g"], w["beta"], w["alpha"])
    seen.add((w["k"], w["p"]))
    if e:
        bad += 1
        print("BAD", w["k"], w["p"], w["file"], e)
    elif w.get("show"):
        print("ok ", w["k"], w["p"], "g =", w["g"])
print(f"witness lines checked: {len(ws)}; distinct (kappa,p): {len(seen)}; bad: {bad}")
# negative control: a corrupted witness must fail
w = dict(ws[0]); w["alpha"] = list(w["alpha"]); w["alpha"][1] = (w["alpha"][1] + 1) % w["p"]
print("negative control (alpha_1 + 1) rejected:", bool(check(w["k"], w["p"], w["g"], w["beta"], w["alpha"])))
