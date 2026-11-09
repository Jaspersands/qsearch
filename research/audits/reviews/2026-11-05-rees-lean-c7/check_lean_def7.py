"""Parse the `bch` definition out of formal/Formal/BCHClassSeven.lean (the Lean
text itself, not the generator's data) and compare it, in the free associative
algebra, with Dynkin's formula (dynkin7.py). Closes the loop between the
independent coefficients and the statement Lean checks."""
import re, sys
from fractions import Fraction as Q
import dynkin7 as D

# usage: check_lean_def7.py [7|6]  (class seven by default; 6 checks BCHClassSix.bch)
CLS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
NAME = {7: 'BCHClassSeven', 6: 'BCHClassSix'}[CLS]
path = f'/Users/jaspersands/Developer/qsearch/formal/Formal/{NAME}.lean'
D.N = CLS
src = open(path).read()
body = src.split('def bch (x y : L) : L :=', 1)[1].split('\n\n', 1)[0]
toks = re.findall(r'⁅|⁆|\(|\)|,|\+|-|•|⁻¹|:|/|[0-9]+|[A-Za-z]+', body)
pos = 0
def peek(): return toks[pos] if pos < len(toks) else None
def eat(t=None):
    global pos
    tok = toks[pos]
    assert t is None or tok == t, (t, tok, pos)
    pos += 1
    return tok
def add(a, b, s=1):
    out = dict(a)
    for w, c in b.items():
        out[w] = out.get(w, 0) + s * c
    return {w: c for w, c in out.items() if c}
def mul(a, b):
    out = {}
    for u, cu in a.items():
        for v, cv in b.items():
            out[u + v] = out.get(u + v, 0) + cu * cv
    return {w: c for w, c in out.items() if c}
def expr():
    v = term()
    while peek() in ('+', '-'):
        s = 1 if eat() == '+' else -1
        v = add(v, term(), s)
    return v
def term():
    if peek() == '(':  # either a scalar `(n : F)⁻¹`, `(n / d : F)` or a parenthesised sum
        save = pos
        eat('(')
        if toks[pos].isdigit() and toks[pos + 1] in (':', '/'):
            num = Q(int(eat()))
            if peek() == '/':
                eat('/'); num /= int(eat())
            eat(':'); eat('F'); eat(')')
            if peek() == '⁻¹':
                eat(); num = 1 / num
            eat('•')
            return {w: num * c for w, c in atom().items()}
        globals()['pos'] = save
    return atom()
def atom():
    t = peek()
    if t == '(':
        eat('('); v = expr(); eat(')'); return v
    if t == '⁅':
        eat('⁅'); a = expr(); eat(','); b = expr(); eat('⁆')
        return add(mul(a, b), mul(b, a), -1)
    if t in ('x', 'y'):
        eat(); return {(t,): Q(1)}
    raise ValueError((t, pos))
lean_law = expr()
assert pos == len(toks), (pos, len(toks))
Z = D.dynkin()
assert lean_law == Z, 'Lean bch differs from Dynkin'
print(f'Lean text of {NAME}.bch parsed: {len(lean_law)} associative words, equal to Dynkin\'s formula through degree {CLS}')
