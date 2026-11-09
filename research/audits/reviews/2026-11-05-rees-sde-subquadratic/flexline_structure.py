"""Exact check of Proposition 2.
(i)  A circuit has a flexible line  <=>  a class-restricted contraction (alpha, beta) exists on
     the class set C of delta (beta : C -> F_p constant on classes).
(ii) The flexible lines are exactly F_p * Lambda(b o delta) for column-dependent b in F_p^S
     (b nonconstant) such that for every nu in Z_kappa some s_nu has
     b_i + s_nu in Q_{-(nu + cls delta_i)} U {0} for all i.  (The class-constant b of (i) give
     only some of these lines; an earlier version of this script tested equality with those
     and found it false, which is why (ii) is stated with column-dependent b.)  Condition: alpha_nu + beta_c in Q_{-(nu+c)} U {0} for all nu in Z_kappa, c in C,
beta nonconstant on C.  We enumerate ALL beta : C -> F_p (|C| <= 3 or small p) and compare
the resulting set of lines with the flexible lines computed from R(S).
Usage: python flexline_structure.py
"""
import itertools, random
from common import F, realizable
from circuit_flex import flexible_lines, make_circuit, canon

def q_ok(Fd, y, m):
    """y in Q_m U {0}  (Q_m = g^m P)."""
    y %= Fd.p
    return y == 0 or Fd.cls(y) == m % Fd.k

def contraction_lines(Fd, cols, delta, q):
    p, k = Fd.p, Fd.k
    cl = [Fd.cls(d) for d in delta]
    C = sorted(set(cl))
    lines = set()
    for beta_vals in itertools.product(range(p), repeat=len(C)):
        if len(set(beta_vals)) == 1:
            continue
        beta = dict(zip(C, beta_vals))
        if not all(any(all(q_ok(Fd, al + beta[c], -(nu + c)) for c in C) for al in range(p)) for nu in range(k)):
            continue
        w = [sum(beta[cl[i]] * delta[i] * cols[i][t] for i in range(len(cols))) % p for t in range(q)]
        assert any(w)
        lines.add(canon(w, p))
    return lines

def column_lines(Fd, cols, delta, q):
    p, k = Fd.p, Fd.k
    cl = [Fd.cls(d) for d in delta]
    n = len(cols)
    lines = set()
    for rest in itertools.product(range(p), repeat=n - 1):
        b = (0,) + rest
        if len(set(b)) == 1:
            continue
        if not all(any(all(q_ok(Fd, b[i] + s, -(nu + cl[i])) for i in range(n)) for s in range(p)) for nu in range(k)):
            continue
        w = [sum(b[i] * delta[i] * cols[i][t] for i in range(n)) % p for t in range(q)]
        if any(w):
            lines.add(canon(w, p))
    return lines

def main():
    rng = random.Random(5)
    cases = [(13, 2, 2), (7, 2, 2), (13, 3, 2), (7, 3, 2), (13, 4, 2), (17, 4, 2), (37, 4, 2), (29, 4, 2),
             (11, 5, 2), (31, 5, 2), (13, 2, 3), (13, 3, 3), (13, 4, 3), (17, 4, 3)]
    agree = agree2 = total = 0
    for p, k, q in cases:
        Fd = F(p, k)
        rows = []
        for t in range(8):
            pat = None if t < 6 else ([c % k for c in range(q + 1)] if t == 6 else [0] * q + [1])
            cols, delta = make_circuit(Fd, rng, q, pat)
            if len({Fd.cls(d) for d in delta}) == 1:
                continue
            R = realizable(Fd, cols, q)
            fl = flexible_lines(Fd, R, q)
            cl_lines = contraction_lines(Fd, cols, delta, q)
            total += 1
            ok = (bool(fl) == bool(cl_lines)) and cl_lines <= fl
            agree += ok
            ok2 = (fl == column_lines(Fd, cols, delta, q)) if p ** q <= 3000 else None
            agree2 += bool(ok2) if ok2 is not None else 0
            rows.append(f"C={sorted({Fd.cls(d) for d in delta})} flex={len(fl)} classconst={len(cl_lines)} (i)={ok} (ii)={ok2}")
        print(f"p={p} kappa={k} q={q}: " + " | ".join(rows), flush=True)
    print(f"TOTAL {total} circuits; (i) existence equivalence and inclusion hold in {agree}; (ii) exact set equality checked and true in {agree2} (checked only when p^q <= 3000)")


if __name__ == "__main__":
    main()
