"""Write formal/Formal/BCHClassSixSubgroups.lean from the exact model words6.py.
Design aid only: Lean checks every identity independently."""
from fractions import Fraction as Q
import sys
import rules2 as R2
import words6 as W

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

def smooth(n):
    e = []
    for p in (2, 3, 5):
        k = 0
        while n % p == 0: n //= p; k += 1
        e.append(k)
    assert n == 1, n
    return tuple(e)

# all denominators that occur, closed under the products field_simp may form
dens = {2, 12, 24, 120, 240, 360, 720, 1440}
for A in [W.C[n][2] for n in W.C]:
    dens |= {c.denominator for c in A.values()}
dens |= {t.denominator for _, t in W.fac} | {t.denominator for _, t in W.afac}
NUMS = sorted(n for n in {d for d in dens if d > 1} | {4, 6, 8, 16, 36, 48, 72, 144, 180} if n not in (2, 3, 5))
NE = ', '.join(['NeZero.ne (2 : F)', 'NeZero.ne (3 : F)', 'NeZero.ne (5 : F)'] + [f'ne{n} (F := F)' for n in NUMS])
NEP = NE.replace('(F := F)', '(F := ZMod p)').replace(' : F)', ' : ZMod p)')
TWO6 = list(R2.RULES[6])
T6 = ', '.join(f'two6{chr(97 + i)} a b' for i in range(len(TWO6)))
SIMP = f"""add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b, {T6}"""
SIMPV = SIMP.replace('jacobi4c a b', 'jacobi4c x.val y.val').replace(' a b', ' x.val y.val')

def zq(q):
    if q.denominator == 1:
        return f"({q.numerator} : ZMod p)"
    if q < 0:
        return f"(-({-q.numerator} / {q.denominator}) : ZMod p)"
    return f"({q.numerator} / {q.denominator} : ZMod p)"

out = []
P = out.append
P('''import Formal.BCHClassSix
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-six BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 5` (so every
`p > 6`). The words were designed with the exact rational model
`research/audits/reviews/2026-11-05-rees-lean-c6/words6.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of two
  degree-three, three degree-four, six degree-five and nine degree-six iterated
  commutators, has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-6 (one, two, three, six and nine of them) has logarithm exactly
  `x + y`.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`), no degree-five
rule, and three degree-six rules `two6a`-`two6c` (the twelve words `a·w`, `w` a
degree-five normal word, span a space of dimension nine).
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassSixSubgroups

open LieModule QSearch.BCHClassSix
open QSearch.BCHClassFour (jacobi4c)
open QSearch.BCHClassFive (smooth_ne_zero)

noncomputable section

section TwoLetterRules

variable {L : Type*} [LieRing L]
''')
for i, col in enumerate(TWO6):
    pv = [p for p in R2.PIV6 if p[0] == col][0]
    cert = pv[2]
    lines = []
    es = []
    for j, (k, c) in enumerate(sorted(cert.items())):
        U, V = R2.INST6[k][0]
        assert U != V
        lines.append(f"  have e{j} := lie_skew ({word(U)} : L) {word(V)}")
        coefv = -c; assert abs(coefv) == 1
        es.append(('' if coefv > 0 else '-') + f"e{j}")
    ev = ' '.join(f"e{j}" for j in range(len(es)))
    P(f'''/-- A degree-six two-letter rule, from one `lie_skew` instance. -/
theorem two6{chr(97 + i)} (a b : L) : {word(col)} =
    {intlin(R2.RULES[6][col])} := by
{chr(10).join(lines)}
  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm
  simp only [lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,
    neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hba, jacobi4c a b] at {ev}
  linear_combination (norm := module) {' + '.join(es).replace('+ -', '- ')}
''')
P('''end TwoLetterRules

section Numerals

variable {F : Type*} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]
''')
for n in NUMS:
    a, b, c = smooth(n)
    P(f'''theorem ne{n} : ({n} : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) {a} {b} {c}
  norm_num at this; exact this
''')
P('''end Numerals

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
theorem sext_central (hnil : lowerCentralSeries F L L 6 = ⊥) (a b c d e f g : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, g⁆⁆⁆⁆⁆⁆ = 0 :=
  classSix_of_lowerCentralSeries hnil a b c d e f g
''')
LNAME = {'c2': 'commPoly', 'c3x': 'p3x', 'c3y': 'p3y', 'c4xx': 'p4xx', 'c4yx': 'p4yx', 'c4yy': 'p4yy'}
for n, _, _ in W.FIVE:
    LNAME['c5' + n] = 'p5' + n
DOC = {'c2': 'The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form.'}
def gdesc(nm):
    l, inner, _ = W.C[nm]
    if nm == 'c2':
        return 'C(x,y)'
    return f"C({l}, {gdesc(inner)})"
FFREE = set()
for nm in ['c2', 'c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in W.FIVE]:
    A = W.C[nm][2]
    if all(c.denominator == 1 and c == 1 for c in A.values()):
        FFREE.add(LNAME[nm])
    doc = DOC.get(nm, f"The logarithm of `{gdesc(nm)}`.")
    P(f"/-- {doc} -/\ndef {LNAME[nm]} (a b : L) : L :=\n  {poly(A)}\n")
def ap(nm):
    return nm if nm in FFREE else f"{nm} (F := F)"
UNF = ', '.join(LNAME[n] for n in LNAME)
import json, os
LINT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lint6.json')))
def ne_for(omit):
    keep = [q for q in (2, 3, 5) if str(q) not in omit]
    hs = [f'NeZero.ne ({q} : F)' for q in keep]
    if omit:  # the composite `neN` lemmas need all three instances
        return ', '.join(hs)
    for n in NUMS:
        if all(str(q) not in omit for q, e in zip((2, 3, 5), smooth(n)) if e):
            hs.append(f'ne{n} (F := F)')
    return ', '.join(hs)
def lemma(name, lhs, rhs, doc, maxhb=None):
    lint = LINT.get(name, {})
    omit = lint.get('omit', [])
    s = ''
    if omit:
        s += 'omit ' + ' '.join(f'[NeZero ({q} : F)]' for q in omit) + ' in\n'
    if maxhb is not None:
        s += f"set_option maxHeartbeats {maxhb} in\n"
    s += f"/-- {doc} -/\ntheorem {name} (hnil : lowerCentralSeries F L L 6 = ⊥) (a b : L) :\n    {lhs} =\n      {rhs} := by\n"
    s += "  have hseven := sext_central hnil\n  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm\n"
    s += f"  simp only [{'bch, ' if 'bch' in lhs else ''}{UNF}, {SIMP}]\n"
    if not lint.get('closes'):
        s += f"  all_goals match_scalars\n  all_goals (try field_simp [{ne_for(omit)}])\n  all_goals ring\n"
    P(s)
lemma('bch_comm', 'bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b)', 'commPoly (F := F) a b',
      'The commutator polynomial, derived from the sextic BCH law.', maxhb=0)
def lhs_of(nm):
    l, inner, _ = W.C[nm]
    inner_t = 'commPoly (F := F) a b' if inner == 'c2' else f"{ap(LNAME[inner])} a b"
    return f"commPoly (F := F) {'a' if l == 'x' else 'b'} ({inner_t})"
VALNAME = {'c3x': 'left', 'c3y': 'right', 'c4xx': 'll', 'c4yx': 'rl', 'c4yy': 'rr'}
for n, _, _ in W.FIVE:
    VALNAME['c5' + n] = n
for nm in ['c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in W.FIVE]:
    lemma(f'commPoly_{VALNAME[nm]}', lhs_of(nm), f"{ap(LNAME[nm])} a b", f"`{gdesc(nm)}`.", maxhb=0)
USED6 = [n for n, _ in W.fac if n.startswith('c6')]
for nm in USED6:
    VALNAME[nm] = nm[2:]
    A = W.C[nm][2]
    lemma(f'commPoly_{VALNAME[nm]}', lhs_of(nm), intlin(A),
          'A degree-six commutator is its central bracket.', maxhb=0)
P('''end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] {hnil : lowerCentralSeries F L L 6 = ⊥}

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
def valrhs(nm, xv='x.val', yv='y.val'):
    if nm.startswith('c6'):
        return intlin(W.C[nm][2], xv, yv)
    t = LNAME[nm]
    return f"{t} {xv} {yv}" if t in FFREE else f"{t} (F := F) {xv} {yv}"
def valname(nm):
    return 'val_comm' if nm == 'c2' else f"val_comm_{VALNAME[nm]}"
for nm in ['c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in W.FIVE] + USED6:
    l, inner, _ = W.C[nm]
    P(f'''theorem {valname(nm)} (x y : BCH F L hnil) :
    ({gterm(nm)}).val = {valrhs(nm)} := by
  rw [val_comm, {valname(inner)}, commPoly_{VALNAME[nm]} hnil]
''')
P('''end Words

/-- Install with `letI := neZeroTwo hp` when the characteristic bound is explicit. -/
theorem neZeroTwo {p : ℕ} (hp : 5 < p) : NeZero (2 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 2 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroThree hp` when the characteristic bound is explicit. -/
theorem neZeroThree {p : ℕ} (hp : 5 < p) : NeZero (3 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 3 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) (by omega))⟩

/-- Install with `letI := neZeroFive hp` when the characteristic bound is explicit. -/
theorem neZeroFive {p : ℕ} (hp : 5 < p) : NeZero (5 : ZMod p) :=
  ⟨(ZMod.natCast_eq_zero_iff 5 p).not.mpr
    (Nat.not_dvd_of_pos_of_lt (by decide) hp)⟩

section PrimeField

variable {p : ℕ} [Fact p.Prime] {L : Type*} [LieRing L] [LieAlgebra (ZMod p) L]
  [NeZero (2 : ZMod p)] [NeZero (3 : ZMod p)] [NeZero (5 : ZMod p)]
  {hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥}

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
HN = {}
memlines = ['  have m_c2 := comm_mem H hx hy']
order = ['c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in W.FIVE] + USED6
for nm in order:
    l, inner, _ = W.C[nm]
    memlines.append(f"  have m_{nm} := comm_mem H h{l} m_{inner}")
BWTERM = 'm_c2'
for n, t in W.fac[1:]:
    BWTERM = f'H.mul_mem ({BWTERM})\n    (powerScalar_mem H _ m_{n})'
VALS = ', '.join(['val_comm'] + [valname(n) for n in order])
P(f'''/-- Removing the degree-three, -four, -five and then the central degree-six
corrections from the group commutator recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, {VALS}]
  have hseven := sext_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, {UNF}, {SIMPV}]
  all_goals match_scalars
  all_goals (try field_simp [{NEP}])
  all_goals ring

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
central degree-six errors, each by a power of an exact bracket monomial. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

set_option maxHeartbeats 0 in
set_option maxRecDepth 100000 in
theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
  have hseven := sext_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, {SIMPV}]
  all_goals match_scalars
  all_goals (try field_simp [{NEP}])
  all_goals ring

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
the group subgroup axioms. The prime-field hypotheses exclude 2, 3 and 5. -/
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥)
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
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 6 = ⊥)
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
end QSearch.BCHClassSixSubgroups
''')
for n in ['val_comm', 'val_bracketWord', 'val_addWord', 'toLieSubalgebra', 'mem_toLieSubalgebra',
          'toSubgroup', 'toLieSubalgebra_toSubgroup', 'toSubgroup_toLieSubalgebra']:
    P(f"/-- info: 'QSearch.BCHClassSixSubgroups.{n}' depends on axioms: [propext, Classical.choice, Quot.sound] -/\n#guard_msgs (whitespace := lax) in\n#print axioms QSearch.BCHClassSixSubgroups.{n}\n")
dest = sys.argv[1] if len(sys.argv) > 1 else '/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassSixSubgroups.lean'
open(dest, 'w').write('\n'.join(out))
print('wrote', dest, 'NUMS', NUMS)
