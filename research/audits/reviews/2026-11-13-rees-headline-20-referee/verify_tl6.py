"""Headline-20 referee: independent check of the author's RC(6;Z6->{0}) certificates
(v2/certs_tl6_all.json) from fragment.tex def:rc.  Own primitive-root routine; D-class of x is
the unique i with (x*xi^{-i})^{(p-1)/D} = 1."""
import json, sys
SRC = "../2026-11-13-rees-headline-below-38/v2/certs_tl6_all.json"
def pf(n):
    out = []; d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0: n //= d
        d += 1 if d == 2 else 2
    if n > 1: out.append(n)
    return out
def lpr(p):
    fs = pf(p - 1); g = 2
    while any(pow(g, (p - 1) // q, p) == 1 for q in fs): g += 1
    return g
def isprime(n):
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def dclass(x, p, D, xi):
    e = (p - 1) // D; inv = pow(xi, p - 2, p); y = x % p
    for i in range(D):
        if pow(y, e, p) == 1: return i
        y = y * inv % p
    raise ValueError
def check(p, D, alpha, beta, xi):
    R = sorted(beta); K = {0}
    if sorted(R) != list(range(D)) or len(alpha) != D: return "shape"
    s = (alpha[0] + beta[0]) % p
    if s == 0 or dclass(s, p, D, xi) != 0: return "a0+b0"
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0: continue
            if (dclass(v, p, D, xi) + i + j) % D not in K: return f"cell {i},{j}"
    return "ok"
d = json.load(open(SRC)); D = d["D"]; B = d["bound"]; F = d["found"]
assert D == 6 and B == 837384
ok = bad = 0; badl = []; gmis = 0
for ps, c in F.items():
    p = int(ps); assert isprime(p) and p % 6 == 1 and p < B
    xi = lpr(p)
    if c["g"] != xi: gmis += 1
    beta = {int(k): v for k, v in c["beta"].items()}
    r = check(p, D, c["alpha"], beta, xi)
    if r == "ok": ok += 1
    else: bad += 1; badl.append((p, r))
allp = [q for q in range(7, B, 6) if isprime(q)]
missing = [q for q in allp if str(q) not in F]
m2520 = [q for q in allp if q % 2520 == 1]
print("primes =1 mod 6 below", B, ":", len(allp))
print("certificates:", len(F), "accepted", ok, "rejected", bad, badl[:5], "g mismatches", gmis)
print("missing:", len(missing), "max", max(missing), missing)
print("primes =1 mod 2520 below bound:", len(m2520), "all certified:", all(str(q) in F for q in m2520),
      "accepted:", sum(check(q, 6, F[str(q)]["alpha"], {int(k): v for k, v in F[str(q)]["beta"].items()}, lpr(q)) == "ok" for q in m2520))
# negative controls: perturb one alpha entry for the first 20 2520-class certs; must be rejected mostly
import random; random.seed(7); rej = 0
for q in m2520[:20]:
    c = F[str(q)]; a = list(c["alpha"]); j = random.randrange(1, 6); a[j] = (a[j] + random.randrange(1, q)) % q
    rej += check(q, 6, a, {int(k): v for k, v in c["beta"].items()}, lpr(q)) != "ok"
print("perturbed controls rejected:", rej, "/ 20")
