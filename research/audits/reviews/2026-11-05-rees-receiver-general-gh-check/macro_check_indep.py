"""(M) re-run with an own bit-sliced simulator: add_product_ops / add_scaled_ops of
theorems/rees_circuit_arith.py on ALL canonical words, for every coefficient at p = 61, 131 and
for 16 coefficients at p = 191, including the aliased squaring add_product(t, a, a).
Referee script, AI-written, pending human review."""
import json, sys, time
import numpy as np
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_circuit_arith import add_product_ops, add_scaled_ops, Anc, anc_size

def sim(gates, nw, loads, N):
    nwd = (N+63)//64
    S = np.zeros((nw, nwd), dtype=np.uint64)
    for reg, vals in loads:
        for j, w in enumerate(reg):
            bits = np.zeros(nwd*64, dtype=np.uint8); bits[:N] = (vals >> j) & 1
            S[w] ^= np.packbits(bits, bitorder="little").view(np.uint64)
    for name, q in gates:
        if name == "cx": S[q[1]] ^= S[q[0]]
        elif name == "ccx": S[q[2]] ^= S[q[0]] & S[q[1]]
        elif name == "x": np.invert(S[q[0]], out=S[q[0]])
        elif name == "swap": S[[q[0], q[1]]] = S[[q[1], q[0]]]
        else: raise ValueError(name)
    def read(reg):
        out = np.zeros(N, dtype=np.int64)
        for j, w in enumerate(reg):
            out |= np.unpackbits(S[w].view(np.uint8), bitorder="little")[:N].astype(np.int64) << j
        return out
    return S, read

out = []
for p, coeffs in [(61, None), (131, None), (191, list(range(1, 9))+list(range(183, 191)))]:
    t0 = time.time()
    b = max(1, (p-1).bit_length())
    T, Aw, Bw = list(range(b)), list(range(b, 2*b)), list(range(2*b, 3*b))
    anc = Anc(list(range(3*b, 3*b+anc_size(b))), b)
    nw = 3*b+anc_size(b)
    cs = coeffs or list(range(1, p))
    ok = {"add_product": True, "add_scaled": True, "add_product_aliased": True}
    # product: all (t, a, b) in chunks over t
    av, bv = np.meshgrid(np.arange(p), np.arange(p), indexing="ij")
    av, bv = av.ravel(), bv.ravel()
    for c in cs:
        g = add_product_ops(p, T, Aw, Bw, c, anc)
        for t in range(p):
            N = p*p
            tv = np.full(N, t)
            S, rd = sim(g, nw, [(T, tv), (Aw, av), (Bw, bv)], N)
            good = np.array_equal(rd(T), (tv+c*av*bv) % p) and np.array_equal(rd(Aw), av) and \
                np.array_equal(rd(Bw), bv) and not S[3*b:].any()
            ok["add_product"] &= bool(good)
            if not good or (p > 61 and t >= 2 and coeffs is None):
                break                        # p = 131: t in {0, 1, 2} for every coefficient (time)
        ga = add_product_ops(p, T, Aw, Aw, c, anc)
        tv, a1 = np.repeat(np.arange(p), p), np.tile(np.arange(p), p)
        S, rd = sim(ga, nw, [(T, tv), (Aw, a1)], p*p)
        ok["add_product_aliased"] &= bool(np.array_equal(rd(T), (tv+c*a1*a1) % p) and np.array_equal(rd(Aw), a1)
                                          and not S[3*b:].any())
        gs = add_scaled_ops(p, T, Aw, c, anc)
        S, rd = sim(gs, nw, [(T, tv), (Aw, a1)], p*p)
        ok["add_scaled"] &= bool(np.array_equal(rd(T), (tv+c*a1) % p) and np.array_equal(rd(Aw), a1)
                                 and not S[3*b:].any())
    r = {"p": p, "b": b, "coefficients": len(cs), "product_t_range": "all t" if p == 61 or coeffs else "t in {0,1,2}",
         **ok, "seconds": round(time.time()-t0, 1)}
    r["passed"] = all(ok.values())
    print(json.dumps(r), flush=True)
    out.append(r)
json.dump(out, open("macro_check_indep.json", "w"), indent=1)
