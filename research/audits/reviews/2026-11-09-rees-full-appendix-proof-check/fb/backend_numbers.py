"""fb check 5: arithmetic consistency of the numbers in appendix-backends.tex.

Recomputes from the formulas of the paper (Lemma lem:qft-mod, Theorem thm:uniform-compilation(iii)/(i),
Chevalley-Warning and triangular arities) and compares with the printed numbers:
 (t, r, tau) from eta; 3 pi 2^-tau; TV bounds per terminal sample and per run; transform counts and
 non-|0> transform counts; per-transform gate count implied by the printed totals versus the Lemma bound;
 the ancilla pool 4b+2t+1 and qubit totals; oracle-call, BCH-pass and bracket counts; arities;
 the pair count (p^M - 1)|K^perp|^(M-1); the label-tuple counts 5^12, 3^18, 7^3*7^6, 390625, 729.
"""
import math
from fractions import Fraction

def params(N, eta):
    b = math.ceil(math.log2(N))
    t = math.ceil(math.log2(36 * N / eta ** 2))
    r = math.ceil(math.log2(6 * math.sqrt(2) * math.pi * t / eta))
    tau = math.ceil(math.log2(3 * math.pi * (b + 3) / eta))
    return b, t, r, tau

def lemma_gate_bound(b, t, r, tau):
    return 328 * b * b + 92 * b * t + 2 * t * r + (b + 5) * tau + 26 * t + 240 * b + 60

def kappa(d, p):
    return math.gcd(d, p - 1)

def transforms(dims, arities, m):
    """dims g_1..g_c, arities {d: M_d}; returns (total, non_zero_input) per terminal sample,
    counted as in thm:uniform-compilation(iii): source n, merge node 2 g_d per instrument + D_{d-1}, readout m."""
    c = len(dims); n = sum(dims)
    D = lambda k: sum(dims[:k])
    # number of sources per terminal sample
    P = 1
    for d in range(2, c + 1):
        P *= arities[d]
    total = P * n
    nonzero = 0
    nodes_above = 1   # number of grade-d nodes = prod_{d' < d} M_{d'}
    counts = {}
    for d in range(2, c + 1):
        nd = 1
        for dd in range(2, d):
            nd *= arities[dd]
        per_node = arities[d] * 2 * dims[d - 1] + D(d - 1)
        total += nd * per_node
        nonzero += nd * arities[d] * dims[d - 1]
        counts[d] = nd
    total += m
    nonzero += m
    return total, nonzero, P

def main():
    out = []
    pr = lambda *a: (print(*a), out.append(" ".join(str(x) for x in a)))
    pr("== Lemma qft-mod parameters ==")
    for N, eta, printed in [(3, 1.5e-3, (26, 19, 15)), (5, 2.8e-4, (32, 22, 18)), (3, 1.488e-3, (26, 19, 15)),
                            (5, 2.799e-4, (32, 22, 18)), (5, 2.5e-4, (32, 22, 18))]:
        b, t, r, tau = params(N, eta)
        z = 3 * math.pi * 2 ** (-tau)
        pr(f"N={N} eta={eta}: b={b} (t,r,tau)=({t},{r},{tau}) printed={printed} {'OK' if (t,r,tau)==printed else 'MISMATCH'};"
           f" 3pi2^-tau={z:.4e} eta/(b+3)={eta/(b+3):.4e} {'<=' if z <= eta/(b+3) else '>'}; pool 4b+2t+1={4*b+2*t+1};"
           f" lemma gate bound per transform={lemma_gate_bound(b,t,r,tau)}")

    pr("== transform counts (thm:uniform-compilation(iii) counting) ==")
    H3 = dict(dims=[3, 1], m=3, p=3)
    F35 = dict(dims=[4, 2, 1], m=4, p=5)
    F37 = dict(dims=[4, 2, 1], m=4, p=7)
    F47 = dict(dims=[5, 3, 2, 1], m=5, p=7)
    cases = [("H3 CW", H3, {2: 3}, 24, 6), ("F3(5) CW", F35, {2: 5, 3: 2}, 148, 24),
             ("F3(5) coherent", F35, {2: 6, 3: 2}, 176, 28), ("F3(7) coherent_k3", F37, {2: 6, 3: 3}, 230, None),
             ("F4(7) coherent_c4", F47, {2: 10, 3: 6, 4: 3}, 3330, None)]
    for name, inst, ar, pt, pnz in cases:
        tot, nz, P = transforms(inst["dims"], ar, inst["m"])
        pr(f"{name}: transforms={tot} (printed {pt}) non-|0>={nz} (printed {pnz}) sources/terminal sample={P}")

    pr("== arities ==")
    for name, dims, p in [("H3", [3, 1], 3), ("F3(5)", [4, 2, 1], 5), ("F3(7)", [4, 2, 1], 7), ("F4(5)", [5, 3, 2, 1], 5),
                          ("F4(7)", [5, 3, 2, 1], 7), ("F5(7)", [6, 4, 3, 2, 1], 7)]:
        c = len(dims)
        cw = {d: kappa(d, p) * dims[d - 1] + 1 for d in range(2, c + 1)}
        tri = {d: (dims[d - 1] + 1 if kappa(d, p) == 1 else (dims[d - 1] + 1) * (dims[d - 1] + 2) // 2) for d in range(2, c + 1)}
        ks = {d: kappa(d, p) for d in range(2, c + 1)}
        pr(f"{name}: kappa={ks} CW arities={cw} coherent arities={tri}")

    pr("== TV bounds ==")
    for name, eta, ntr, nnz, N, S, printed_sample, printed_run in [
            ("qft_wire H3", 1.5e-3, 24, 6, 3, 7, 0.0142, 0.0993), ("qft_wire F3(5)", 2.8e-4, 148, 24, 5, 8, 0.0112, 0.0895),
            ("full H3", 1.5e-3, 24, 6, 3, 7, None, 0.0993), ("full F3(5)", 2.5e-4, 176, 28, 5, 8, None, 0.0986)]:
        b, t, r, tau = params(N, eta)
        z = 3 * math.pi * 2 ** (-tau)
        per = nnz * eta + (ntr - nnz) * z
        run = S * per
        pr(f"{name}: per sample={per:.6f} (printed < {printed_sample}) run of {S}={run:.6f} (printed < {printed_run}) "
           f"{'OK' if (printed_sample is None or per < printed_sample) and run < printed_run else 'MISMATCH'}")

    pr("== gate totals ==")
    # per-transform gates implied by printed totals
    for name, gates_tr, ntr, N, eta in [("qft_wire H3", 188952, 24, 3, 1.5e-3), ("qft_wire F3(5)", 1968844, 148, 5, 2.8e-4),
                                        ("full H3", 304234 - 115282, 24, 3, 1.5e-3), ("full F3(5)", 5035924 - 2694596, 176, 5, 2.5e-4)]:
        b, t, r, tau = params(N, eta)
        pr(f"{name}: transform gates={gates_tr} / {ntr} = {Fraction(gates_tr, ntr)} per transform; lemma bound {lemma_gate_bound(b,t,r,tau)}")
    pr(f"qubits: qft_wire H3 82 + (3b+5=11) + pool {4*2+2*26+1} = {82+11+4*2+2*26+1} (printed 154); "
       f"F3(5) 744 + 14 + {4*3+2*32+1} = {744+14+4*3+2*32+1} (printed 835); F4(7) 16302+14={16302+14} (printed 16316)")

    pr("== oracle calls, BCH passes, brackets (first backend) ==")
    def bch_brackets(d):
        return (d - 1) * d * (d + 1) * (d + 2) // 6
    # H3: M2 = 3, c = 2
    pr(f"H3: oracle calls = 3*2 = {3*2} (printed 6); BCH passes = 3*4 = {12} (printed 12)")
    # F3(5): M3=2, M2=5
    pr(f"F3(5): oracle calls = 10*3 = {30} (printed 30); passes = 5*2*4 + 5*4 = {5*2*4+5*4} (printed 60); "
       f"thm(i) brackets = 40*{bch_brackets(3)} + 20*{bch_brackets(2)} = {40*bch_brackets(3)+20*bch_brackets(2)} (printed 880)")
    pr(f"F3(7) coherent_k3 oracle outputs: 18 sources * 3 calls * 4 coords * 3 bits = {18*3*4*3} (printed 648)")
    pr(f"F4(7) coherent_c4 oracle outputs: 180 sources * 4 calls * 5 coords * 3 bits = {180*4*5*3} (printed 10800)")

    pr("== label tuple / pair counts ==")
    pr(f"(5^7-1)*125^6 = {(5**7-1)*125**6:.3e} (printed up to 3.0e17)")
    pr(f"F3(5) coherent grade-2 labels: 25^6 = {25**6} = 5^12 = {5**12}; grade-3 label pairs 5^2 = 25; Q at grade 3: 5^6; "
       f"25*5^6 = {25*5**6} (printed 390625)")
    pr(f"H3 merge block inputs: labels 3^3, Q 3^3, children 3*4 coords -> 3^(3+3+12) = 3^18 = {3**18}; labels*Q values 3^3*3^3 = {3**6} (printed 729);"
       f" children support (3^6)^3 = {(3**6)**3:.2e} (printed 3.9e8)")
    pr(f"F3(7) grade-3 block: label triples 7^3, q in G_2 (D_2 = 6): 7^6 -> 7^9 = {7**9}")
    pr(f"F5(7): grade-3 cubes in F_7 = {sorted({pow(x,3,7) for x in range(7)})}; 3^10 = {3**10} vs 7^10 = {7**10}")
    pr(f"hlift dims: F4(7) h=gamma_2: 3+3+2+1 = 9 -> 7^9; F5(7) h=gamma_4: 2+2+2+2+1 = 9 -> 7^9")
    pr(f"Heisenberg F_3 subgroup count: 1 + 13 + 4 + 1 = {1+13+4+1}; normal subgroups containing Z: Z, 4 maximal, G = 6")
    open(__file__.replace('.py', '.out'), 'w').write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
