"""Print the polynomial definitions for BCHClassFiveSubgroups.lean (letters a, b)."""
from fractions import Fraction as Q
import words5 as W

def word(w, a='a', b='b'):
    mp = {'x': a, 'y': b}
    s = mp[w[-1]]
    for ch in reversed(w[:-1]):
        s = f"⁅{mp[ch]}, {s}⁆"
    return s

def coef(q):
    if q.denominator == 1:
        return f"({q.numerator} : F)"
    return f"({q.numerator} / {q.denominator} : F)"

def poly(A, a='a', b='b', indent='    '):
    terms = []
    for w, c in sorted(A.items(), key=lambda kv: (len(kv[0]), kv[0])):
        t = word(w, a, b)
        terms.append(t if c == 1 else f"{coef(c)} • {t}")
    out, line = [], ''
    for i, t in enumerate(terms):
        piece = t if i == 0 else f" + {t}"
        if len(line) + len(piece) > 84:
            out.append(line); line = indent + piece.lstrip()
            if i: line = indent + "+ " + t
        else:
            line += piece
    out.append(line)
    return '\n'.join(out)

if __name__ == '__main__':
    for nm, A in [('commPoly', W.c2), ('p3x', W.c3x), ('p3y', W.c3y), ('p4xx', W.c4xx), ('p4yx', W.c4yx), ('p4yy', W.c4yy)]:
        print(f"def {nm} (a b : L) : L :=\n  {poly(A)}\n")
