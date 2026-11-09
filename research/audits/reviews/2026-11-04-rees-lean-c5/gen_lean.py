"""Print the Lean `have` block of degree-4/5 rewrite rules for BCHClassFive.lean."""
from fractions import Fraction as Q
import rules5 as R

def word(w):
    s = w[-1]
    for ch in reversed(w[:-1]):
        s = f"⁅{ch}, {s}⁆"
    return s

def lin(d):
    parts = []
    for w in sorted(d):
        c = d[w]
        assert c.denominator == 1
        k = abs(c.numerator)
        for _ in range(k):
            parts.append(('+' if c > 0 else '-', word(w)))
    s = ''
    for i, (sg, t) in enumerate(parts):
        if i == 0:
            s += t if sg == '+' else f"-{t}"
        else:
            s += f" {sg} {t}"
    return s or '0'

JAC4C = {('x','y','x','y'): 'x y', ('x','z','x','z'): 'x z', ('y','z','y','z'): 'y z'}
names = {}
out = []
for n, piv, inst in ((4, R.PIV4, R.INST4), (5, R.PIV5, R.INST5)):
    for k, (col, v, cert) in enumerate(piv):
        nm = f"r{n}{chr(ord('a') + k)}"
        names[col] = nm
        rhs = lin(R.RULES[n][col])
        out.append(f"  have {nm} : {word(col)} =\n      {rhs} := by")
        if col in JAC4C:
            out.append(f"    exact jacobi4c {JAC4C[col]}")
            continue
        assert len(cert) == 1
        (i, c), = cert.items()
        U, V = inst[i][0]
        out.append(f"    have e := lie_skew ({word(U)} : L) {word(V)}")
        lower = 'jacobi3 x y z' + ''.join(f", {names[w]}" for w in R.RULES.get(4, {}) if n == 5)
        out.append(f"    simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,\n"
                   f"      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, {lower}] at e")
        # goal: LHS - RHS = c([U,V]+[V,U]) = -c (e.lhs - e.rhs)
        coef = -c
        assert coef in (1, -1)
        out.append(f"    linear_combination (norm := module) {'e' if coef == 1 else '-e'}")
print('\n'.join(out))
print('-- simp names:', ', '.join(names[w] for n in (4, 5) for w in R.RULES[n]))
