"""Exact logarithms of the class-four subgroup words, in the Lean normal-form basis."""
import importlib.util, sys, io
from fractions import Fraction as Q
spec = importlib.util.spec_from_file_location('m', 'bch4_model.py')
m = importlib.util.module_from_spec(spec); _o = sys.stdout; sys.stdout = io.StringIO(); spec.loader.exec_module(m); sys.stdout = _o
B = [tuple(w) for w in ['xy', 'xxy', 'yxy', 'xxxy', 'xyxy', 'yyxy']]
x, y = m.gen('x'), m.gen('y')
def show(nm, e, extra=()):
    d = m.express(e, list(extra) + B) if e else {}
    print(nm, {''.join(k): str(v) for k, v in d.items()})
bch = m.bch; sc = m.sc; neg = m.neg; add = m.add; rn = m.rn
conj = bch(bch(x, y), neg(x)); show('conj = bch(bch a b)(-a) - b', add(conj, neg(y)))
C = lambda a, b: m.comm(a, b)
c1 = C(x, y); show('C(a,b)', c1)
c2x = C(x, c1); show('C(a,C(a,b))', c2x)
c2y = C(y, c1); show('C(b,C(a,b))', c2y)
show('C(a,C(a,C(a,b)))', C(x, c2x)); show('C(b,C(a,C(a,b)))', C(y, c2x)); show('C(b,C(b,C(a,b)))', C(y, c2y))
bw = bch(bch(bch(bch(bch(c1, sc(Q(-1,2), c2x)), sc(Q(-1,2), c2y)), sc(Q(1,3), rn('xxxy'))), sc(Q(1,4), rn('xyxy'))), sc(Q(1,3), rn('yyxy')))
assert bw == rn('xy'); print('bracketWord ok')
s0 = bch(bch(x, y), sc(Q(-1,2), rn('xy'))); show('s0 - a - b', add(s0, neg(x), neg(y)))
s1 = bch(bch(s0, sc(Q(1,6), c2x)), sc(Q(1,3), c2y)); show('s1 - a - b', add(s1, neg(x), neg(y)))
s2 = add(s1, sc(Q(-5,24), rn('xxxy')), sc(Q(-3,8), rn('xyxy')), sc(Q(-11,24), rn('yyxy')))
assert s2 == add(x, y); print('addWord ok')
