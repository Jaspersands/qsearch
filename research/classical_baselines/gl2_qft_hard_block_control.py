"""Finite falsifier for toolbox 2608.28573, central-trivial A_gamma block.

Exact Sage finite fields, 200-bit complex arithmetic. This is NOT a quantum
execution, an all-q proof, or a synthesis of the exceptional preparation.
The latter resource obligation is audited separately from Lemma B.3.
"""
import json
from pathlib import Path

from sage.all import ComplexField, GF, identity_matrix, matrix, vector


C = ComplexField(200)


def root(n):
    return C.zeta(n)


def peak(a):
    return max(abs(z) for z in a.list())


def control(p):
    f, e = GF(p), GF(p**2, name="u")
    h = e.multiplicative_generator()
    g = f((h ** (p + 1)).list()[0])
    n = h ** (p - 1)
    lf = {g**j: j for j in range(p - 1)}
    le = {h**j: j for j in range(p*p - 1)}
    ln = {n**j: j for j in range(p + 1)}
    gf = [sum(root(p - 1)**(a*j) * root(p)**int(x)
              for x, j in lf.items()) for a in range(p - 1)]
    ge = [sum(root(p*p - 1)**(a*j) * root(p)**int(x.trace())
              for x, j in le.items()) for a in range(p*p - 1)]
    cs = list(range(1, (p + 1)//2))
    ps = list(range(1, (p - 1)//2))
    ss = [0, (p - 1)//2]
    physical = [("C", j) for j in cs] + [("P", j) for j in ps]
    physical += [("S", j) for j in ss]
    rows = physical + [("D", j) for j in ss]
    rows += [("AP", j) for j in ps] + [("AC", j) for j in cs]
    idx = {x: j for j, x in enumerate(rows)}
    assert len(physical) == p and len(rows) == 2*p
    sq = lambda x: C(x).sqrt()

    # Literal published columns, independent of the branching construction.
    target = matrix(C, 2*p, p)
    for kind, k in physical:
        i = idx[kind, k]
        target[i, 0] = {"C": 1/sq(p+1), "P": 1/sq(p-1),
                        "S": sq(C(p)/(p*p-1))}[kind]
        for a in range(p-1):
            sign = (-1)**a
            if kind == "C":
                # nu(n)=exp(2 pi i k/(p+1)); pullback z/z^p has minus sign.
                m = -(p-1)*k - (p+1)*a
                value = -sign*ge[m % (p*p-1)]/sq(p*(p*p-1))
            elif kind == "P":
                value = sign*gf[(k-a) % (p-1)]*gf[(-k-a) % (p-1)]
                value /= (p-1)*sq(p)
            else:
                value = sign*gf[(k-a) % (p-1)]**2/((p-1)*sq(p+1))
            target[i, a+1] = value

    d = identity_matrix(C, p)
    invft = matrix(C, p, p)
    invft[0, 0] = 1
    for a in range(p-1):
        if (2*a) % (p-1):
            d[a+1, a+1] = (-1)**a*gf[(-2*a) % (p-1)]/sq(p)
        for t, logt in lf.items():
            invft[int(t), a+1] = root(p-1)**(-a*logt)/sq(p-1)

    # B_1: field t -> split/non-split ratio, including both boundary columns.
    branch = matrix(C, 2*p, p)
    for t in f:
        col = int(t)
        if t == 0 or t == f(1)/4:
            branch[0, col] = 1/sq(2)
            branch[p-1, col] = (1 if t == 0 else -1)/sq(2)
            continue
        roots = [x for x in f if x*x-x+t == 0]
        if roots:
            assert len(roots) == 2
            for x in roots:
                branch[lf[x/(1-x)], col] = 1/sq(2)
        else:
            roots = [x for x in e if x*x-x+e(t) == 0]
            assert len(roots) == 2
            for x in roots:
                branch[p-1+ln[x/x**p], col] = -1/sq(2)
    ft = matrix(C, 2*p, 2*p)
    for mod, off in [(p-1, 0), (p+1, p-1)]:
        for a in range(mod):
            for j in range(mod):
                ft[off+a, off+j] = root(mod)**(a*j)/sq(mod)

    # R_fix, including every unused antisymmetric and determinant output.
    fix = matrix(C, 2*p, 2*p)
    for kind, anti, mod, off, reps in [
            ("P", "AP", p-1, 0, ps), ("C", "AC", p+1, p-1, cs)]:
        for j in reps:
            fix[idx[kind, j], off+j] = 1/sq(2)
            fix[idx[kind, j], off+mod-j] = 1/sq(2)
            fix[idx[anti, j], off+j] = 1/sq(2)
            fix[idx[anti, j], off+mod-j] = -1/sq(2)
    for a, b in [(0, 0), ((p-1)//2, (p+1)//2)]:
        fix[idx["S", a], a] = sq(C(p+1)/(2*p))
        fix[idx["D", a], a] = sq(C(p-1)/(2*p))
        fix[idx["S", a], p-1+b] = sq(C(p-1)/(2*p))
        fix[idx["D", a], p-1+b] = -sq(C(p+1)/(2*p))

    # Literal exceptional two-plane correction. Its efficient preparations
    # are a separate written obligation, not inferred from this dense check.
    exc = identity_matrix(C, 2*p)
    for a in ss:
        u = target.column(a+1)
        v = vector(C, 2*p)
        v[idx["D", a]] = 1
        outer = lambda x, y: x.column()*y.conjugate().row()
        reflection = identity_matrix(C, 2*p)
        reflection += (-(-1)**a/sq(p)-1)*outer(u, u)
        reflection += ((-1)**a/sq(p)-1)*outer(v, v)
        reflection += sq(C(p-1)/p)*(outer(u, v)+outer(v, u))
        exc = reflection*exc
    before = fix*ft*branch*invft*d
    actual = exc*before
    errors = {
        "branch_isometry": peak(branch.conjugate_transpose()*branch-identity_matrix(C,p)),
        "label_unitarity": peak(fix.conjugate_transpose()*fix-identity_matrix(C,2*p)),
        "target_isometry": peak(target.conjugate_transpose()*target-identity_matrix(C,p)),
        "full_column_difference": peak(actual-target),
        "unused_output_leakage": peak(actual[p:]),
    }
    mutant = peak(before-target)
    assert max(errors.values()) < C(2)**(-150), (p, errors)
    assert mutant > C(1)/10
    return {"q": p, "gamma": "trivial", "columns": p,
            "max_entry_errors": {k: str(v) for k,v in errors.items()},
            "omitted_exceptional_correction_error": str(mutant)}


if __name__ == "__main__":
    result = {"scope": "finite 200-bit classical matrix identity falsifier; NOT quantum execution",
              "source": "arXiv:2608.28573 equations 129-151",
              "predeclared_primes": [3,5,7], "precision_bits": 200,
              "controls": [control(p) for p in [3,5,7]]}
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "controls": 3, "columns": 15,
                      "artifact": str(path)}))
