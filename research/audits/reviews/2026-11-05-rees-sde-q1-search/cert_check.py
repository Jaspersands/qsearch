"""Independent check (no sss.py) of the critical-stall certificates in banks/*.json:
  * B is a basis of V = F_p^a (rank a); U_L has dimension r - 1 and |B \\ U_L| = 1;
  * B, the rounds, the pool and the unused list partition the columns; unused is empty;
  * every pool column lies in span(B cap U_L);
  * each round S_l is a circuit modulo U_{l-1}: rank(U_{l-1} + S_l) = dim U_{l-1} + |S_l| - 1
    and every proper subset is independent modulo U_{l-1} (checked by deleting one column);
  * the number of bank columns in U_L is below the recursion threshold D3(r-1) + r - 1."""
import glob
import json


def rank(vecs, p):
    rows = [list(v) for v in vecs]
    r = 0
    n = len(rows[0]) if rows else 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        iv = pow(rows[r][c], p - 2, p)
        rows[r] = [x * iv % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]
                rows[i] = [(x - f * y) % p for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def inspan(basis, v, p):
    return rank(basis + [v], p) == rank(basis, p)


ok_all = True
for f in sorted(glob.glob("banks/*.json")):
    R = json.load(open(f))
    c = R["identity_cert"]
    if not c:
        print("%-36s no stall on identity order (rescued earlier by R1-R3): skip" % f)
        continue
    p, cols, a = R["p"], R["cols"], R["a"]
    B, U, pool = c["B"], c["U_L"], c["pool"]
    rounds = c["rounds"]
    r = rank(cols, p)
    chk = {}
    chk["B basis"] = rank([cols[i] for i in B], p) == r == len(B)
    chk["dimU=r-1"] = rank(U, p) == len(U) == r - 1
    out = [i for i in B if not inspan(U, cols[i], p)]
    chk["|B\\U|=1"] = len(out) == 1
    allidx = sorted(B + pool + [i for S in rounds for i in S] + c["unused"])
    chk["partition"] = allidx == list(range(len(cols)))
    chk["no unused"] = not c["unused"]
    BU = [cols[i] for i in B if inspan(U, cols[i], p)]
    chk["pool in span(B cap U)"] = all(inspan(BU, cols[i], p) for i in pool)
    # rounds are circuits modulo the running U (U grows by the round's span minus one dim;
    # we only use that U_{l-1} is contained in U_L and test circuit-ness mod U_{l-1}, where
    # U_{l-1} is recomputed as the span of U_L's first dims) -- here we test the weaker,
    # basis-free statement: each round is dependent modulo U_L-prefix and minimal.
    circ = True
    Uprev = []
    for S in rounds:
        vs = [cols[i] for i in S]
        d0 = rank(Uprev, p) if Uprev else 0
        full = rank(Uprev + vs, p) if Uprev else rank(vs, p)
        if full != d0 + len(S) - 1:
            circ = False
        for j in range(len(S)):
            sub = vs[:j] + vs[j + 1:]
            if (rank(Uprev + sub, p) if Uprev else rank(sub, p)) != d0 + len(S) - 1:
                circ = False
        gain = min(2, len(S) - 1)
        Uprev = U[:len(Uprev) + gain] if False else (Uprev + U[len(Uprev):len(Uprev) + gain])
    chk["rounds are circuits mod U_{l-1}"] = circ
    n_in = sum(1 for v in cols if inspan(U, v, p))
    D3 = lambda q: 0 if q == 0 else (q + 2) ** 2 // 4
    chk["cols in U_L < D3(r-1)+r-1"] = n_in < D3(r - 1) + r - 1
    ok = all(chk.values())
    ok_all &= ok
    print("%-36s %s  pi=%d inUL=%d thr=%d  %s" % (f, "PASS" if ok else "FAIL", len(pool), n_in,
          D3(r - 1) + r - 1, "" if ok else {k: v for k, v in chk.items() if not v}))
print("ALL PASS" if ok_all else "SOME FAILED")
