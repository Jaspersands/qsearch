"""Item C exact checks: free-Lie pullback for the metacyclic group C_{p^2} x| C_p.

Run: /opt/anaconda3/bin/python research/audits/reviews/2026-11-02-rees-extensions/C/metacyclic_cover_check.py

G is realised by normal forms a^i b^j, (i mod p^2, j mod p), with b a b^-1 = a^(1+p).
No Lie chart of G is used to evaluate Phi: Phi is built from black-box group words
(powers, ADD_2 and BRACKET_2 of class two), as the paper's Prop prop:black-box (i) says.
The cover is F = F_{2,2} over Z/p^2: coordinates (c1, c2, c3) on x1, x2, [x1, x2].

Checks (all exhaustive unless marked sampled):
  1. Phi is a group homomorphism (F, BCH) -> G and is surjective.
  2. Phi's fibres are additive cosets of ker(pi): ker pi is an abelian-HSP instance on (F, +).
  3. Omega_1(G) = <a^p, b> has order p^2; Phi(Omega_1(F)) = Phi(pF) = <a^p> = agemo_1(G).
  4. Every preimage of b has order p^2; Phi(p x1) = a^p.
  5. Phi^{-1}(Omega_1(G)) = {x : p x in ker pi}.
  6. For every subgroup H of G, the ring-to-field outer recursion (Thm ring-to-field (iii)),
     run on the explicit cover F with hidden K = Phi^{-1}(H), never needs ker Phi or
     Omega_1(G), stays inside N, terminates within log_p|F| = 6 local calls, returns K,
     and Phi(K) = H.  It also records where the naive socle push-forward misses H cap Omega_1(G).
  7. Chart acquisition: F / ker pi is a Lazard ring Z/p^2 + Z/p of class 2 with |F/ker| = |G|.
"""
import itertools
import random
import sys


def run(p, sample_pairs=None):
    q = p * p
    out = {}

    # ---- black-box group G -------------------------------------------------
    def gmul(g, h):
        (i1, j1), (i2, j2) = g, h
        return ((i1 + i2 * pow(1 + p, j1, q)) % q, (j1 + j2) % p)

    E = (0, 0)

    def gpow(g, n):
        n %= q  # exponent of G divides p^2
        r, b = E, g
        while n:
            if n & 1:
                r = gmul(r, b)
            b = gmul(b, b)
            n >>= 1
        return r

    def ginv(g):
        return gpow(g, q - 1)

    def comm(g, h):  # g^-1 h^-1 g h
        return gmul(gmul(ginv(g), ginv(h)), gmul(g, h))

    half = pow(2, -1, q)

    def ADD(g, h):  # exp(X+Y) = exp X exp Y exp(-[X,Y]/2) in class 2
        return gmul(gmul(g, h), gpow(comm(g, h), -half))

    BRACKET = comm  # exp[X,Y] = (exp X, exp Y) in class 2

    a, b = (1, 0), (0, 1)
    Gel = [(i, j) for i in range(q) for j in range(p)]
    w3 = BRACKET(a, b)

    def Phi(c):
        c1, c2, c3 = c
        return ADD(ADD(gpow(a, c1), gpow(b, c2)), gpow(w3, c3))

    # ---- free cover F_{2,2} over Z/p^2 ---------------------------------------
    Fel = list(itertools.product(range(q), repeat=3))

    def add(u, v):
        return tuple((x + y) % q for x, y in zip(u, v))

    def smul(k, u):
        return tuple((k * x) % q for x in u)

    def br(u, v):
        return (0, 0, (u[0] * v[1] - u[1] * v[0]) % q)

    def fmul(u, v):  # BCH class 2
        return add(add(u, v), smul(half, br(u, v)))

    PhiT = {u: Phi(u) for u in Fel}

    # 1. homomorphism + surjective
    if sample_pairs is None:
        pairs = itertools.product(Fel, Fel)
    else:
        rng = random.Random(p)
        pairs = ((rng.choice(Fel), rng.choice(Fel)) for _ in range(sample_pairs))
    hom_ok = all(PhiT[fmul(u, v)] == gmul(PhiT[u], PhiT[v]) for u, v in pairs)
    surj = set(PhiT.values()) == set(Gel)
    out["1_hom"] = hom_ok
    out["1_hom_mode"] = "exhaustive" if sample_pairs is None else f"sampled {sample_pairs}"
    out["1_surjective"] = surj

    # 2. fibres are additive cosets of ker pi
    ker = frozenset(u for u in Fel if PhiT[u] == E)
    ker_additive = all(add(u, v) in ker for u in ker for v in ker)
    neg = lambda u: smul(-1, u)
    rng = random.Random(1000 + p)
    fib_ok = True
    for _ in range(20000):
        u, v = rng.choice(Fel), rng.choice(Fel)
        if (PhiT[u] == PhiT[v]) != (add(u, neg(v)) in ker):
            fib_ok = False
            break
    out["2_ker_order"] = len(ker)
    out["2_ker_additive_subgroup"] = ker_additive
    out["2_fibres_are_additive_cosets_sampled20000"] = fib_ok

    # 3. Omega_1, agemo, image of the cover socle
    Om1G = {g for g in Gel if gpow(g, p) == E}
    ap = gpow(a, p)
    gen_ap_b = {gmul(gpow(ap, i), gpow(b, j)) for i in range(p) for j in range(p)}
    socF = [u for u in Fel if smul(p, u) == (0, 0, 0)]
    img_soc = {PhiT[u] for u in socF}
    agemo1 = {gpow(g, p) for g in Gel}
    out["3_|Omega1(G)|"] = len(Om1G)
    out["3_Omega1(G)==<a^p,b>"] = Om1G == gen_ap_b
    out["3_|Phi(Omega1(F))|"] = len(img_soc)
    out["3_Phi(Omega1(F))==<a^p>==agemo1(G)"] = img_soc == {gpow(ap, i) for i in range(p)} == agemo1

    # 4. preimages of b, Phi(p x1)
    pre_b = [u for u in Fel if PhiT[u] == b]
    out["4_all_preimages_of_b_have_order_p2"] = all(smul(p, u) != (0, 0, 0) for u in pre_b)
    out["4_Phi(p x1)==a^p"] = PhiT[(p, 0, 0)] == ap

    # 5. Phi^{-1}(Omega_1(G)) = {x : p x in ker}
    lhs = {u for u in Fel if PhiT[u] in Om1G}
    rhs = {u for u in Fel if smul(p, u) in ker}
    out["5_preimage_formula"] = lhs == rhs
    out["5_|Phi^-1(Omega1(G))|"] = len(lhs)

    # 6. ring-to-field outer recursion on the cover, for every subgroup H of G
    def gen_sub(gens):
        S = {E}
        frontier = [E]
        while frontier:
            x = frontier.pop()
            for g in gens:
                y = gmul(x, g)
                if y not in S:
                    S.add(y)
                    frontier.append(y)
        return frozenset(S)

    cyc = {}
    for g in Gel:
        C = gen_sub([g])
        cyc.setdefault(C, g)
    cg = list(cyc.values())
    subs = {gen_sub([g, h]) for g in cg for h in cg}  # p-groups of order p^3 are 2-generated
    out["6_number_of_subgroups"] = len(subs)

    def add_gens(S):
        span = {(0, 0, 0)}
        gens = []
        for x in S:
            if x not in span:
                gens.append(x)
                new = set(span)
                y = x
                while True:
                    shifted = {add(s, y) for s in span}
                    if shifted <= new:
                        break
                    new |= shifted
                    y = add(y, x)
                span = new
        return gens

    worst_calls = 0
    naive_misses = 0
    rec_ok = True
    cls_max = 0
    for H in subs:
        K = frozenset(u for u in Fel if PhiT[u] in H)
        J = frozenset([(0, 0, 0)])
        calls = 0
        while True:
            Jg = add_gens(J)
            N = frozenset(x for x in Fel if all(br(x, j) in J for j in Jg))
            if not K <= N:
                rec_ok = False
                break
            P = frozenset(x for x in N if smul(p, x) in J)  # Omega_1 of N/J, lifted
            Kloc = K & P
            Pg = add_gens(P)
            calls += 1
            if Kloc == J:
                break
            # P/J is an F_p Lie algebra: p P <= J and p[x,y] = [px,y] in [J,N] <= J
            if not all(br(x, y) in P for x in Pg for y in Pg):
                rec_ok = False
            J = Kloc
            if calls > 7:
                rec_ok = False
                break
        if J != K or {PhiT[u] for u in J} != H:
            rec_ok = False
        worst_calls = max(worst_calls, calls)
        naive = {PhiT[u] for u in K if smul(p, u) == (0, 0, 0)}
        if naive != (H & Om1G):
            naive_misses += 1
    out["6_recursion_recovers_K_and_H_for_all_H"] = rec_ok
    out["6_max_local_calls_incl_final_trivial"] = worst_calls
    out["6_log_p|F|"] = 6
    out["6_socle_sections_closed_under_bracket"] = rec_ok
    out["6_subgroups_where_naive_socle_pushforward!=H_cap_Omega1(G)"] = naive_misses

    # 7. chart acquisition from ker pi: |F/ker| and cyclic type
    quot_order = len(Fel) // len(ker)
    # orders of images of x1, x2 in F/ker
    def addorder(u):
        k = 1
        while smul(k, u) not in ker:
            k += 1
        return k
    out["7_|F/ker|==|G|"] = quot_order == len(Gel)
    out["7_orders_of_x1,x2_mod_ker"] = (addorder((1, 0, 0)), addorder((0, 1, 0)))
    return out


if __name__ == "__main__":
    for p, samp in [(3, None), (5, 300000), (7, 300000)]:
        if p == 7 and "--quick" in sys.argv:
            continue
        res = run(p, samp)
        print(f"p={p}")
        for k, v in res.items():
            print(f"  {k}: {v}")
