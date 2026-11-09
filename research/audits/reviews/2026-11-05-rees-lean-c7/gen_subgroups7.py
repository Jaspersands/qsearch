"""Write formal/Formal/BCHClassSevenSubgroups.lean from the exact model words7.py.
Design aid only: Lean checks every identity independently.

Differences from the class-six generator: the BCH law is the septic one, the
degree-six commutators now carry degree-seven tails (defs `p6...`), eighteen
central degree-seven commutators are added, and `val_bracketWord`,
`val_addWord` are proved in stages: one lemma per factor, from the exact value
after the previous factor (defs `bwStage k`, `awStage k`) to the next."""
from fractions import Fraction as Q
import json, os, sys
import rules2_7 as R2
import words7 as W

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '2026-11-05-rees-lean-c6'))
import rules2 as R2six  # class-six two-letter rules, reused by name
assert R2.RULES[6] == R2six.RULES[6] and R2.RULES[4] == R2six.RULES[4]
assert not R2.RULES[5] and not R2.RULES.get(7)

def word(w, a='a', b='b'):
    mp = {'x': a, 'y': b}
    s = mp[w[-1]]
    for ch in reversed(w[:-1]):
        s = f"⁅{mp[ch]}, {s}⁆"
    return s

def coef(q, F='F'):
    if q.denominator == 1:
        return f"({q.numerator} : {F})"
    return f"({q.numerator} / {q.denominator} : {F})"

def poly(A, a='a', b='b', indent='    ', F='F'):
    terms = []
    for w, c in sorted(A.items(), key=lambda kv: (len(kv[0]), kv[0])):
        t = word(w, a, b)
        terms.append(t if c == 1 else f"{coef(c, F)} • {t}")
    out, line = [], ''
    for i, t in enumerate(terms):
        piece = t if i == 0 else f" + {t}"
        if len(line) + len(piece) > 84:
            out.append(line); line = indent + "+ " + t
        else:
            line += piece
    out.append(line)
    return '\n'.join(out)

def intlin(d, a='a', b='b'):
    parts = []
    for w in sorted(d):
        c = d[w]; assert c.denominator == 1
        parts += [('+' if c > 0 else '-', word(w, a, b))] * abs(c.numerator)
    s = ''
    for i, (sg, t) in enumerate(parts):
        s += (t if sg == '+' else f"-{t}") if i == 0 else f" {sg} {t}"
    return s

PR = (2, 3, 5, 7)
def smooth(n):
    e = []
    for p in PR:
        k = 0
        while n % p == 0: n //= p; k += 1
        e.append(k)
    assert n == 1, n
    return tuple(e)

# all denominators that occur, plus the class-six list
dens = {2, 12, 24, 120, 240, 360, 720, 1440, 1120, 2520, 5040, 10080, 30240}
for A in [W.C[n][2] for n in W.C] + W.BW_STAGES + W.AW_STAGES:
    dens |= {c.denominator for c in A.values()}
dens |= {t.denominator for _, t in W.fac} | {t.denominator for _, t in W.afac}
NUMS = sorted(n for n in {d for d in dens if d > 1} | {4, 6, 8, 16, 36, 48, 72, 144, 180} if n not in PR)
NE = ', '.join([f'NeZero.ne ({q} : F)' for q in PR] + [f'ne{n} (F := F)' for n in NUMS])
NEP = NE.replace('(F := F)', '(F := ZMod p)').replace(' : F)', ' : ZMod p)')
T6 = 'two6a a b, two6b a b, two6c a b'
SIMP = f"""add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, {T6}"""

def zq(q):
    if q.denominator == 1:
        return f"({q.numerator} : ZMod p)"
    if q < 0:
        return f"(-({-q.numerator} / {q.denominator}) : ZMod p)"
    return f"({q.numerator} / {q.denominator} : ZMod p)"

LINT = json.load(open(os.path.join(HERE, 'lint7.json'))) if os.path.exists(os.path.join(HERE, 'lint7.json')) else {}

out = []
P = out.append
P(f'''import Formal.BCHClassSeven
import Formal.BCHClassSixSubgroups
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-seven BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 7` (so every
prime `p ≥ 11`). The words were designed with the exact rational model
`research/audits/reviews/2026-11-05-rees-lean-c7/words7.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of two
  degree-three, three degree-four, six degree-five, nine degree-six and eighteen
  central degree-seven iterated commutators, has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-7 (one, two, three, six, nine and eighteen of them) has logarithm
  exactly `x + y`.

Both values are computed in stages: `bwStage k` and `awStage k` are the exact
logarithms after the first `k` correction factors, and one lemma per factor
(`bwStep_k`, `awStep_k`) passes from one stage to the next. Each stage is a
polynomial in normal form, so no single proof expands more than one product.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`), no degree-five
rule, the three degree-six rules `two6a`-`two6c` of `BCHClassSixSubgroups`, and
no degree-seven rule (the eighteen words `a·w`, `w` a degree-six normal word,
are independent).
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassSevenSubgroups

open LieModule QSearch.BCHClassSeven
open QSearch.BCHClassFour (jacobi4c)
open QSearch.BCHClassSixSubgroups (two6a two6b two6c)

noncomputable section

section Numerals

variable {{F : Type*}} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]
  [NeZero (7 : F)]
''')
for n in NUMS:
    a, b, c, d = smooth(n)
    P(f'''theorem ne{n} : ({n} : F) ≠ 0 := by
  have := smooth7_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F))
    (NeZero.ne (7 : F)) {a} {b} {c} {d}
  norm_num at this; exact this
''')
P('''end Numerals

section SepticPart

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket (coefficient one) added to its first argument. -/
theorem z7_peel_left1 (h : ClassSeven L) (u v p q : L) :
    z7 (F := F) (u + ⁅p, q⁆) v = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

set_option linter.unusedSimpArgs false in
/-- `z7` vanishes when its second argument is a multiple of a bracket. -/
theorem z7_bracket_right (h : ClassSeven L) (u p q : L) (t : F) :
    z7 (F := F) u (t • ⁅p, q⁆) = 0 := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, lie_smul, height, smul_zero, add_zero, sub_zero, sub_self, neg_zero]

/-- `z7 b (-b) = 0`. -/
theorem z7_self_neg (b : L) : z7 (F := F) b (-b) = 0 := by
  simp [z7]

end SepticPart

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)] in
theorem oct_central (hnil : lowerCentralSeries F L L 7 = ⊥) (a b c d e f g k : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
  classSeven_of_lowerCentralSeries hnil a b c d e f g k
''')
FIVE = [n for n, _, _ in W.FIVE]
LNAME = {'c2': 'commPoly', 'c3x': 'p3x', 'c3y': 'p3y', 'c4xx': 'p4xx', 'c4yx': 'p4yx', 'c4yy': 'p4yy'}
for n in FIVE:
    LNAME['c5' + n] = 'p5' + n
for n in W.USED6:
    LNAME[n] = 'p6' + n[2:]
DOC = {'c2': 'The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form.'}
def gdesc(nm):
    l, inner, _ = W.C[nm]
    if nm == 'c2':
        return 'C(x,y)'
    return f"C({l}, {gdesc(inner)})"
DEFORDER = ['c2', 'c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n in FIVE] + W.USED6
FFREE = set()
for nm in DEFORDER:
    A = W.C[nm][2]
    if all(c == 1 for c in A.values()):
        FFREE.add(LNAME[nm])
    doc = DOC.get(nm, f"The logarithm of `{gdesc(nm)}`.")
    P(f"/-- {doc} -/\ndef {LNAME[nm]} (a b : L) : L :=\n  {poly(A)}\n")
def ap(nm, F='F'):
    return nm if nm in FFREE else f"{nm} (F := {F})"
UNF = ', '.join(LNAME[n] for n in DEFORDER)

def ne_for(omit, F='F'):
    keep = [q for q in PR if str(q) not in omit]
    hs = [f'NeZero.ne ({q} : {F})' for q in keep]
    if omit:  # the composite `neN` lemmas need all four instances
        return ', '.join(hs)
    return ', '.join(hs + [f'ne{n} (F := {F})' for n in NUMS])

def tactic_tail(lint, F='F', field_list=None):
    if lint.get('closes'):
        return ''
    fl = field_list if field_list is not None else ne_for(lint.get('omit', []), F)
    tail = f"  all_goals match_scalars\n  all_goals (try field_simp [{fl}])\n"
    return tail if lint.get('noring') else tail + "  all_goals ring\n"

def lemma(name, lhs, rhs, doc, unf):
    lint = LINT.get(name, {})
    omit = lint.get('omit', [])
    s = ''
    if omit:
        s += 'omit ' + ' '.join(f'[NeZero ({q} : F)]' for q in omit) + ' in\n'
    s += "set_option maxHeartbeats 0 in\n"
    s += f"/-- {doc} -/\ntheorem {name} (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :\n    {lhs} =\n      {rhs} := by\n"
    s += "  have height := oct_central hnil\n  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm\n"
    s += f"  simp only [{unf}, {SIMP}]\n"
    s += tactic_tail(lint)
    P(s)

Q1 = W.bch(W.bch(W.X, W.Y), W.neg(W.X))
assert W.deg(Q1, 1) == W.Y
P(f"/-- The logarithm of `x y x⁻¹`, in normal form. -/\ndef commStage1 (a b : L) : L :=\n  {poly(Q1)}\n")
B6 = 'QSearch.BCHClassSix.bch (F := F)'
lemma('commStage1_eq', f'{B6} ({B6} a b) (-a) + z7 (F := F) a b + z7 (F := F) (a + b) (-a)',
      'commStage1 (F := F) a b', 'The septic law at `(x y, x⁻¹)`, after removing the central parts.',
      'QSearch.BCHClassSix.bch, z7, commStage1')
lemma('commStage1_comm', f'{B6} (commStage1 (F := F) a b) (-b)', 'commPoly (F := F) a b',
      'The sextic law at `(x y x⁻¹, y⁻¹)`.', 'QSearch.BCHClassSix.bch, commStage1, commPoly')
P(f'''/-- The commutator polynomial, derived from the septic BCH law. -/
theorem bch_comm (hnil : lowerCentralSeries F L L 7 = ⊥) (a b : L) :
    bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b) =
      commPoly (F := F) a b := by
  have h := classSeven_of_lowerCentralSeries hnil
  have z1 : z7 (F := F) (bch (F := F) a b) (-a) = z7 (F := F) (a + b) (-a) := by
    rw [bch_shape a b]
    simp only [z7_peel_left h]
  have b1 : {B6} (bch (F := F) a b) (-a) = {B6} ({B6} a b) (-a) + z7 (F := F) a b := by
    rw [bch_eq_six_add a b, six_central_left _ _ _ (fun w => z7_central h a b w)]
  have z2 : z7 (F := F) (commStage1 (F := F) a b) (-b) = 0 := by
    unfold commStage1
    simp only [z7_peel_left h, z7_peel_left1 h, z7_self_neg]
  rw [bch_eq_six_add (bch (F := F) a b) (-a), z1, b1, commStage1_eq hnil,
    bch_eq_six_add (commStage1 (F := F) a b) (-b), z2, add_zero, commStage1_comm hnil]
''')
def lhs_of(nm):
    l, inner, _ = W.C[nm]
    inner_t = 'commPoly (F := F) a b' if inner == 'c2' else f"{ap(LNAME[inner])} a b"
    return f"commPoly (F := F) {'a' if l == 'x' else 'b'} ({inner_t})"
VALNAME = {'c3x': 'left', 'c3y': 'right', 'c4xx': 'll', 'c4yx': 'rl', 'c4yy': 'rr'}
for n in FIVE:
    VALNAME['c5' + n] = n
for n in W.USED6 + W.USED7:
    VALNAME[n] = n[2:]
for nm in ['c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n in FIVE] + W.USED6:
    lemma(f'commPoly_{VALNAME[nm]}', lhs_of(nm), f"{ap(LNAME[nm])} a b", f"`{gdesc(nm)}`.", UNF)
for nm in W.USED7:
    lemma(f'commPoly_{VALNAME[nm]}', lhs_of(nm), intlin(W.C[nm][2]),
          'A degree-seven commutator is its central bracket.', UNF)
P('''end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]
  {hnil : lowerCentralSeries F L L 7 = ⊥}

/-- Our commutator convention is `x * y * x⁻¹ * y⁻¹`. -/
def comm (x y : BCH F L hnil) : BCH F L hnil := x * y * x⁻¹ * y⁻¹

theorem comm_mem (H : Subgroup (BCH F L hnil)) {x y : BCH F L hnil}
    (hx : x ∈ H) (hy : y ∈ H) : comm x y ∈ H :=
  H.mul_mem (H.mul_mem (H.mul_mem hx hy) (H.inv_mem hx)) (H.inv_mem hy)

theorem val_comm (x y : BCH F L hnil) :
    (comm x y).val = commPoly (F := F) x.val y.val :=
  bch_comm hnil x.val y.val
''')
def gterm(nm):
    if nm == 'c2':
        return 'comm x y'
    l, inner, _ = W.C[nm]
    return f"comm {l} ({gterm(inner)})"
def valrhs(nm, xv='x.val', yv='y.val', F='F'):
    if nm.startswith('c7'):
        return intlin(W.C[nm][2], xv, yv)
    t = LNAME[nm]
    return f"{t} {xv} {yv}" if t in FFREE else f"{t} (F := {F}) {xv} {yv}"
def valname(nm):
    return 'val_comm' if nm == 'c2' else f"val_comm_{VALNAME[nm]}"
ORDER = ['c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n in FIVE] + W.USED6 + W.USED7
for nm in ORDER:
    l, inner, _ = W.C[nm]
    P(f'''theorem {valname(nm)} (x y : BCH F L hnil) :
    ({gterm(nm)}).val = {valrhs(nm)} := by
  rw [val_comm, {valname(inner)}, commPoly_{VALNAME[nm]} hnil]
''')
P('''end Words

/-- Install with `letI := neZeroTwo hp` when the characteristic bound is explicit. -/
theorem neZeroTwo {p : ℕ} (hp : 7 < p) : NeZero (2 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 2 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroThree hp` when the characteristic bound is explicit. -/
theorem neZeroThree {p : ℕ} (hp : 7 < p) : NeZero (3 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 3 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroFive hp` when the characteristic bound is explicit. -/
theorem neZeroFive {p : ℕ} (hp : 7 < p) : NeZero (5 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 5 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroSeven hp` when the characteristic bound is explicit. -/
theorem neZeroSeven {p : ℕ} (hp : 7 < p) : NeZero (7 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 7 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) hp)⟩

section StageValues

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
''')
# stage defs
for k, A in enumerate(W.BW_STAGES[:-1], start=1):
    P(f"/-- The logarithm of `bracketWord` after its first {k} correction factor(s). -/\n"
      f"def bwStage{k} (a b : L) : L :=\n  {poly(A, F='ZMod p')}\n")
for k, A in enumerate(W.AW_STAGES[:-1], start=1):
    P(f"/-- The logarithm of `addWord` after its first {k} correction factor(s). -/\n"
      f"def awStage{k} (a b : L) : L :=\n  {poly(A, F='ZMod p')}\n")
P('''end StageValues

section Stages

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)] [NeZero (7 : ZMod p)]
''')
def step(name, lhs1, scal, w, rhs, unf, doc, six=False):
    lint = LINT.get(name, {})
    omit = lint.get('omit', [])
    s = ''
    if omit:
        s += 'omit ' + ' '.join(f'[NeZero ({q} : ZMod p)]' for q in omit) + ' in\n'
    s += "set_option maxHeartbeats 0 in\n"
    s += (f"/-- {doc} -/\ntheorem {name} (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥) (a b : L) :\n"
          f"    bch (F := ZMod p) ({lhs1}) ({scal} • {w}) =\n      {rhs} := by\n")
    s += "  have height := oct_central hnil\n  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm\n"
    if six:
        s += (f"  rw [bch_eq_six_add ({lhs1}) ({scal} • {w}),\n"
              f"    z7_bracket_right (classSeven_of_lowerCentralSeries hnil), add_zero]\n")
    s += f"  simp only [{unf}, {SIMP}]\n"
    s += tactic_tail(lint, 'ZMod p', ne_for(omit, 'ZMod p'))
    P(s)
BWSTEPS = []
for k, (nm, t) in enumerate(W.fac[1:], start=1):
    lhs1 = 'commPoly (F := ZMod p) a b' if k == 1 else f'bwStage{k - 1} (p := p) a b'
    rhs = '⁅a, b⁆' if k == len(W.fac) - 1 else f'bwStage{k} (p := p) a b'
    wv = valrhs(nm, 'a', 'b', 'ZMod p')
    if not nm.startswith('c7'):
        wv = f'({wv})' if ' ' in wv else wv
    else:
        wv = f'({wv})' if ' + ' in wv or ' - ' in wv else wv
    unf = ', '.join(['bch'] + ([LNAME['c2']] if k == 1 else [f'bwStage{k - 1}']) +
                    ([f'bwStage{k}'] if rhs != '⁅a, b⁆' else []) +
                    ([LNAME[nm]] if not nm.startswith('c7') else []))
    step(f'bwStep{k}', lhs1, zq(t), wv, rhs, unf, f'`bracketWord`, factor {k}.')
    BWSTEPS.append(f'bwStep{k} hnil')
AWSTEPS = []
for k, (w, t) in enumerate(W.afac, start=1):
    lhs1 = 'bch (F := ZMod p) a b' if k == 1 else f'awStage{k - 1} (p := p) a b'
    rhs = 'a + b' if k == len(W.afac) else f'awStage{k} (p := p) a b'
    unf = ', '.join(['QSearch.BCHClassSix.bch'] + (['bch'] if k == 1 else []) +
                    ([f'awStage{k - 1}'] if k > 1 else []) + ([f'awStage{k}'] if k < len(W.afac) else []))
    step(f'awStep{k}', lhs1, zq(t), word(w), rhs, unf, f'`addWord`, factor {k}.', six=True)
    AWSTEPS.append(f'awStep{k} hnil')
P('''end Stages

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)] [NeZero (7 : ZMod p)]
  {hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥}

/-- A scalar multiple realized as an actual natural group power. -/
def powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  x ^ t.val

@[simp] theorem val_powerScalar (t : ZMod p) (x : BCH (ZMod p) L hnil) :
    (powerScalar t x).val = t • x.val := by
  rw [powerScalar, val_pow, ZMod.natCast_zmod_val]

theorem powerScalar_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p)
    {x : BCH (ZMod p) L hnil} (hx : x ∈ H) : powerScalar t x ∈ H :=
  H.pow_mem hx t.val
''')
body = 'comm x y'
for n, t in W.fac[1:]:
    body += f' *\n    powerScalar {zq(t)} ({gterm(n)})'
memlines = ['  have m_c2 := comm_mem H hx hy']
for nm in ORDER:
    l, inner, _ = W.C[nm]
    memlines.append(f"  have m_{nm} := comm_mem H h{l} m_{inner}")
BWTERM = 'm_c2'
for n, t in W.fac[1:]:
    BWTERM = f'H.mul_mem ({BWTERM})\n    (powerScalar_mem H _ m_{n})'
VALS = ', '.join(['val_comm'] + [f'commPoly_{VALNAME[n]} hnil' for n in ORDER])
def rwlist(steps):
    lines, cur = [], '  rw ['
    for i, s in enumerate(steps):
        piece = s + (', ' if i < len(steps) - 1 else ']')
        if len(cur) + len(piece) > 96:
            lines.append(cur.rstrip()); cur = '    ' + piece
        else:
            cur += piece
    lines.append(cur)
    return '\n'.join(lines)
P(f'''/-- Removing the degree-three to degree-six and then the central degree-seven
corrections from the group commutator recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, {VALS}]
{rwlist(BWSTEPS)}

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {{x y : BCH (ZMod p) L hnil}} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
{chr(10).join(memlines)}
  exact {BWTERM}
''')
def bwexpr(w):
    s = 'bracketWord x y'
    assert w.endswith('xy')
    for ch in reversed(w[:-2]):
        s = f'bracketWord {ch} ({s})'
    return s
body = 'x * y'
for w, t in W.afac:
    body += f' *\n    powerScalar {zq(t)} ({bwexpr(w)})'
blines = []
done = set()
def need(w):
    if w in done or w == 'xy':
        return
    need(w[1:])
    blines.append(f"  have b_{w} := bracketWord_mem H h{w[0]} b_{w[1:]}")
    done.add(w)
blines.append('  have b_xy := bracketWord_mem H hx hy')
for w, t in W.afac:
    need(w)
AWTERM = 'H.mul_mem hx hy'
for w, t in W.afac:
    AWTERM = f'H.mul_mem ({AWTERM})\n    (powerScalar_mem H _ b_{w})'
P(f'''/-- Addition is recovered by removing the bracket, then the degree-three to
central degree-seven errors, each by a power of an exact bracket monomial. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
{rwlist(AWSTEPS)}

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {{x y : BCH (ZMod p) L hnil}} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
{chr(10).join(blines)}
  exact {AWTERM}

theorem mk_smul_mem (H : Subgroup (BCH (ZMod p) L hnil)) (t : ZMod p) {{x : L}}
    (hx : BCH.mk x ∈ H) : BCH.mk (t • x) ∈ H := by
  have heq : powerScalar t (BCH.mk x : BCH (ZMod p) L hnil) = BCH.mk (t • x) :=
    BCH.ext (val_powerScalar t (BCH.mk x))
  rw [← heq]
  exact powerScalar_mem H t hx

theorem mk_lie_mem (H : Subgroup (BCH (ZMod p) L hnil)) {{x y : L}}
    (hx : BCH.mk x ∈ H) (hy : BCH.mk y ∈ H) : BCH.mk ⁅x, y⁆ ∈ H := by
  have heq : bracketWord (BCH.mk x : BCH (ZMod p) L hnil) (BCH.mk y) = BCH.mk ⁅x, y⁆ :=
    BCH.ext (val_bracketWord (BCH.mk x) (BCH.mk y))
  rw [← heq]
  exact bracketWord_mem H hx hy

theorem mk_add_mem (H : Subgroup (BCH (ZMod p) L hnil)) {{x y : L}}
    (hx : BCH.mk x ∈ H) (hy : BCH.mk y ∈ H) : BCH.mk (x + y) ∈ H := by
  have heq : addWord (BCH.mk x : BCH (ZMod p) L hnil) (BCH.mk y) = BCH.mk (x + y) :=
    BCH.ext (val_addWord (BCH.mk x) (BCH.mk y))
  rw [← heq]
  exact addWord_mem H hx hy

/-- The logarithm of an arbitrary subgroup, with all Lie closure derived from
the group subgroup axioms. The prime-field hypotheses exclude 2, 3, 5 and 7. -/
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥)
    (H : Subgroup (BCH (ZMod p) L hnil)) : LieSubalgebra (ZMod p) L where
  carrier := {{x | BCH.mk x ∈ H}}
  zero_mem' := H.one_mem
  add_mem' := mk_add_mem H
  smul_mem' t _ hx := mk_smul_mem H t hx
  lie_mem' := mk_lie_mem H

@[simp] theorem mem_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil)) (x : L) :
    x ∈ toLieSubalgebra hnil H ↔ BCH.mk x ∈ H := Iff.rfl

@[simp] theorem val_mem_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil))
    (x : BCH (ZMod p) L hnil) : x.val ∈ toLieSubalgebra hnil H ↔ x ∈ H := Iff.rfl

/-- The reverse construction uses only BCH closure of a Lie subalgebra. -/
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 7 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {{x | x.val ∈ K}}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    unfold bch
    repeat' first
      | exact hx | exact hy
      | apply K.add_mem | apply K.sub_mem | apply K.smul_mem | apply K.lie_mem

@[simp] theorem mem_toSubgroup (K : LieSubalgebra (ZMod p) L)
    (x : BCH (ZMod p) L hnil) : x ∈ toSubgroup hnil K ↔ x.val ∈ K := Iff.rfl

@[simp] theorem toLieSubalgebra_toSubgroup (K : LieSubalgebra (ZMod p) L) :
    toLieSubalgebra hnil (toSubgroup hnil K) = K := by
  ext x
  rfl

@[simp] theorem toSubgroup_toLieSubalgebra (H : Subgroup (BCH (ZMod p) L hnil)) :
    toSubgroup hnil (toLieSubalgebra hnil H) = H := by
  ext x
  rfl

end PrimeField

end
end QSearch.BCHClassSevenSubgroups
''')
for n in ['val_comm', 'val_bracketWord', 'val_addWord', 'toLieSubalgebra', 'mem_toLieSubalgebra',
          'toSubgroup', 'toLieSubalgebra_toSubgroup', 'toSubgroup_toLieSubalgebra']:
    P(f"/-- info: 'QSearch.BCHClassSevenSubgroups.{n}' depends on axioms: [propext, Classical.choice, Quot.sound] -/\n#guard_msgs (whitespace := lax) in\n#print axioms QSearch.BCHClassSevenSubgroups.{n}\n")
dest = sys.argv[1] if len(sys.argv) > 1 else '/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassSevenSubgroups.lean'
open(dest, 'w').write('\n'.join(out))
print('wrote', dest, len('\n'.join(out).splitlines()), 'lines; NUMS', NUMS)
