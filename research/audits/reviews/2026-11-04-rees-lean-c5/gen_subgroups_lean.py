"""Write formal/Formal/BCHClassFiveSubgroups.lean from the exact model words5.py."""
from fractions import Fraction as Q
import words5 as W
from gen_words_lean import poly, word

NUMS = {4: (2, 0, 0), 6: (1, 1, 0), 8: (3, 0, 0), 10: (1, 0, 1), 12: (2, 1, 0), 15: (0, 1, 1),
        16: (4, 0, 0), 20: (2, 0, 1), 24: (3, 1, 0), 30: (1, 1, 1), 36: (2, 2, 0), 40: (3, 0, 1),
        48: (4, 1, 0), 60: (2, 1, 1), 72: (3, 2, 0), 120: (3, 1, 1), 144: (4, 2, 0), 180: (2, 2, 1),
        240: (4, 1, 1), 360: (3, 2, 1), 720: (4, 2, 1)}
NE = ', '.join(['NeZero.ne (2 : F)', 'NeZero.ne (3 : F)', 'NeZero.ne (5 : F)'] + [f'ne{n} (F := F)' for n in NUMS])
NEP = NE.replace('(F := F)', '(F := ZMod p)').replace('(2 : F)', '(2 : ZMod p)').replace('(3 : F)', '(3 : ZMod p)').replace('(5 : F)', '(5 : ZMod p)')
SIMP = """add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hsix, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    neg_smul, add_zero, zero_add, sub_zero, zero_sub, neg_zero, hba, jacobi4c a b"""

def zq(q):
    if q.denominator == 1:
        return f"({q.numerator} : ZMod p)"
    if q < 0:
        return f"(-({-q.numerator} / {q.denominator}) : ZMod p)"
    return f"({q.numerator} / {q.denominator} : ZMod p)"

out = []
P = out.append
P('''import Formal.BCHClassFive
import Mathlib.Data.ZMod.Basic

/-!
# Arbitrary subgroups of prime-field class-five BCH groups

Explicit commutator and power words recover Lie brackets and sums, so every
group subgroup has a Lie-subalgebra logarithm over `ZMod p`, `p > 5`. The words
were designed with the exact rational model
`research/audits/reviews/2026-11-04-rees-lean-c5/words5.py`; Lean checks every
identity independently.

* `bracketWord x y`: the group commutator `comm x y`, corrected by powers of the
  two degree-three, three degree-four and six degree-five iterated commutators,
  has logarithm exactly `[x, y]`.
* `addWord x y`: `x * y` corrected by powers of `bracketWord` monomials of
  degrees 2-5 (one, two, three and six of them) has logarithm exactly `x + y`.

Normal form in two letters `a < b`: right-normed brackets with innermost pair
`[a,b]`, and `[a,[b,[a,b]]]` rewritten to `[b,[a,[a,b]]]` (`jacobi4c`). In two
letters no degree-five rule is needed: the six words `a·w` (`w` one of the three
degree-four normal words) are a basis.
-/

-- The generated `simp only` sets are shared by all lemmas; not every lemma uses every entry.
set_option linter.unusedSimpArgs false

namespace QSearch.BCHClassFiveSubgroups

open LieModule QSearch.BCHClassFive
open QSearch.BCHClassFour (jacobi4c)

noncomputable section

section Numerals

variable {F : Type*} [Field F] [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]
''')
for n, (a, b, c) in NUMS.items():
    P(f'''theorem ne{n} : ({n} : F) ≠ 0 := by
  have := smooth_ne_zero (NeZero.ne (2 : F)) (NeZero.ne (3 : F)) (NeZero.ne (5 : F)) {a} {b} {c}
  norm_num at this; exact this
''')
P('''end Numerals

section PolynomialIdentities

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

omit [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] in
theorem quint_central (hnil : lowerCentralSeries F L L 5 = ⊥) (a b c d e f : L) :
    ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, f⁆⁆⁆⁆⁆ = 0 :=
  classFive_of_lowerCentralSeries hnil a b c d e f
''')
defs = [('commPoly', W.c2, 'The logarithm of the group commutator `x y x⁻¹ y⁻¹`, in normal form.'),
        ('p3x', W.c3x, 'The logarithm of `C(x, C(x,y))`.'),
        ('p3y', W.c3y, 'The logarithm of `C(y, C(x,y))`.'),
        ('p4xx', W.c4xx, 'The logarithm of `C(x, C(x, C(x,y)))`.'),
        ('p4yx', W.c4yx, 'The logarithm of `C(y, C(x, C(x,y)))`.'),
        ('p4yy', W.c4yy, 'The logarithm of `C(y, C(y, C(x,y)))`.')]
FFREE = set()
for nm, A, doc in defs:
    if all(c == 1 for c in A.values()):
        FFREE.add(nm)
    P(f"/-- {doc} -/\ndef {nm} (a b : L) : L :=\n  {poly(A)}\n")
def ap(nm):
    return nm if nm in FFREE else f"{nm} (F := F)"
UNF = 'commPoly, p3x, p3y, p4xx, p4yx, p4yy'
O35 = '[NeZero (3 : F)] [NeZero (5 : F)]'
OALL = '[NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]'
def lemma(name, lhs, rhs, doc, maxhb=None, omit=None, ne=None, closes=False):
    s = ''
    if omit:
        s += f"omit {omit} in\n"
    if maxhb:
        s += f"set_option maxHeartbeats {maxhb} in\n"
    s += f"/-- {doc} -/\ntheorem {name} (hnil : lowerCentralSeries F L L 5 = ⊥) (a b : L) :\n    {lhs} =\n      {rhs} := by\n"
    s += "  have hsix := quint_central hnil\n  have hba : ⁅b, a⁆ = -⁅a, b⁆ := (lie_skew b a).symm\n"
    s += f"  simp only [{'bch, ' if 'bch' in lhs else ''}{UNF}, {SIMP}]\n"
    if not closes:
        s += f"  match_scalars <;> field_simp [{ne or NE}]\n  all_goals ring\n"
    P(s)
lemma('bch_comm', 'bch (F := F) (bch (F := F) (bch (F := F) a b) (-a)) (-b)', 'commPoly (F := F) a b',
      'The commutator polynomial, derived from the quintic BCH law.', maxhb=4000000)
lemma('commPoly_left', 'commPoly (F := F) a (commPoly (F := F) a b)', 'p3x (F := F) a b', '`C(a, C(a,b))`.', maxhb=1000000)
lemma('commPoly_right', 'commPoly (F := F) b (commPoly (F := F) a b)', 'p3y (F := F) a b', '`C(b, C(a,b))`.', maxhb=1000000)
lemma('commPoly_ll', 'commPoly (F := F) a (p3x (F := F) a b)', 'p4xx (F := F) a b', '`C(a, C(a, C(a,b)))`.', maxhb=1000000, omit=O35, ne='NeZero.ne (2 : F)')
lemma('commPoly_rl', 'commPoly (F := F) b (p3x (F := F) a b)', ap('p4yx') + ' a b', '`C(b, C(a, C(a,b)))`.', maxhb=1000000, omit=O35, ne='NeZero.ne (2 : F)')
lemma('commPoly_rr', 'commPoly (F := F) b (p3y (F := F) a b)', 'p4yy (F := F) a b', '`C(b, C(b, C(a,b)))`.', maxhb=1000000, omit=O35, ne='NeZero.ne (2 : F)')
C5 = [('xxx', 'a', 'p4xx', 'xxxxy'), ('yxx', 'b', 'p4xx', 'yxxxy'), ('xyx', 'a', 'p4yx', 'xyxxy'),
      ('yyx', 'b', 'p4yx', 'yyxxy'), ('xyy', 'a', 'p4yy', 'xyyxy'), ('yyy', 'b', 'p4yy', 'yyyxy')]
for nm, l, inner, w in C5:
    lemma(f'commPoly_{nm}', f'commPoly (F := F) {l} ({ap(inner)} a b)', word(w),
          'A degree-five commutator is its central bracket.', omit=OALL, closes=True)
P('''end PolynomialIdentities

section Words

variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]
  [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] {hnil : lowerCentralSeries F L L 5 = ⊥}

/-- Our commutator convention is `x * y * x⁻¹ * y⁻¹`. -/
def comm (x y : BCH F L hnil) : BCH F L hnil := x * y * x⁻¹ * y⁻¹

theorem comm_mem (H : Subgroup (BCH F L hnil)) {x y : BCH F L hnil}
    (hx : x ∈ H) (hy : y ∈ H) : comm x y ∈ H :=
  H.mul_mem (H.mul_mem (H.mul_mem hx hy) (H.inv_mem hx)) (H.inv_mem hy)

theorem val_comm (x y : BCH F L hnil) :
    (comm x y).val = commPoly (F := F) x.val y.val :=
  bch_comm hnil x.val y.val

theorem val_comm_left (x y : BCH F L hnil) :
    (comm x (comm x y)).val = p3x (F := F) x.val y.val := by
  rw [val_comm, val_comm, commPoly_left hnil]

theorem val_comm_right (x y : BCH F L hnil) :
    (comm y (comm x y)).val = p3y (F := F) x.val y.val := by
  rw [val_comm, val_comm, commPoly_right hnil]

theorem val_comm_ll (x y : BCH F L hnil) :
    (comm x (comm x (comm x y))).val = p4xx (F := F) x.val y.val := by
  rw [val_comm, val_comm_left, commPoly_ll hnil]

theorem val_comm_rl (x y : BCH F L hnil) :
    (comm y (comm x (comm x y))).val = p4yx x.val y.val := by
  rw [val_comm, val_comm_left, commPoly_rl hnil]

theorem val_comm_rr (x y : BCH F L hnil) :
    (comm y (comm y (comm x y))).val = p4yy (F := F) x.val y.val := by
  rw [val_comm, val_comm_right, commPoly_rr hnil]
''')
G4 = {'p4xx': ('comm x (comm x (comm x y))', 'val_comm_ll'),
      'p4yx': ('comm y (comm x (comm x y))', 'val_comm_rl'),
      'p4yy': ('comm y (comm y (comm x y))', 'val_comm_rr')}
for nm, l, inner, w in C5:
    g, v = G4[inner]
    gl = 'x' if l == 'a' else 'y'
    P(f'''theorem val_comm_{nm} (x y : BCH F L hnil) :
    (comm {gl} ({g})).val = {word(w, 'x.val', 'y.val')} := by
  rw [val_comm, {v}, commPoly_{nm} hnil]
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
  {hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥}

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
# bracketWord
gw = {'c2': 'comm x y', 'c3x': 'comm x (comm x y)', 'c3y': 'comm y (comm x y)',
      'c4xx': 'comm x (comm x (comm x y))', 'c4yx': 'comm y (comm x (comm x y))',
      'c4yy': 'comm y (comm y (comm x y))',
      'xxx': 'comm x (comm x (comm x (comm x y)))', 'yxx': 'comm y (comm x (comm x (comm x y)))',
      'xyx': 'comm x (comm y (comm x (comm x y)))', 'yyx': 'comm y (comm y (comm x (comm x y)))',
      'xyy': 'comm x (comm y (comm y (comm x y)))', 'yyy': 'comm y (comm y (comm y (comm x y)))'}
fac = [(n, t) for n, t, _ in W.fac]
body = 'comm x y'
for n, t in fac[1:]:
    body += f' *\n    powerScalar {zq(t)} ({gw[n]})'
HN = {'c3x': 'hcx', 'c3y': 'hcy', 'c4xx': 'hcxx', 'c4yx': 'hcyx', 'c4yy': 'hcyy',
      'xxx': 'm5xxx', 'yxx': 'm5yxx', 'xyx': 'm5xyx', 'yyx': 'm5yyx', 'xyy': 'm5xyy', 'yyy': 'm5yyy'}
BWTERM = 'hc'
for n, t in fac[1:]:
    BWTERM = f'H.mul_mem ({BWTERM})\n    (powerScalar_mem H _ {HN[n]})'
P(f'''/-- Removing the degree-three, degree-four and then the central degree-five
corrections from the group commutator recovers the exact Lie bracket. -/
def bracketWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

set_option maxHeartbeats 8000000 in
theorem val_bracketWord (x y : BCH (ZMod p) L hnil) :
    (bracketWord x y).val = ⁅x.val, y.val⁆ := by
  unfold bracketWord
  simp only [val_mul, val_powerScalar, val_comm, val_comm_left, val_comm_right, val_comm_ll,
    val_comm_rl, val_comm_rr, val_comm_xxx, val_comm_yxx, val_comm_xyx, val_comm_yyx,
    val_comm_xyy, val_comm_yyy]
  have hsix := quint_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, {UNF}, {SIMP.replace('jacobi4c a b', 'jacobi4c x.val y.val')}]
  all_goals match_scalars
  all_goals (try field_simp [{NEP}])
  all_goals ring

theorem bracketWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {{x y : BCH (ZMod p) L hnil}} (hx : x ∈ H) (hy : y ∈ H) : bracketWord x y ∈ H := by
  have hc := comm_mem H hx hy
  have hcx := comm_mem H hx hc
  have hcy := comm_mem H hy hc
  have hcxx := comm_mem H hx hcx
  have hcyx := comm_mem H hy hcx
  have hcyy := comm_mem H hy hcy
  have m5xxx := comm_mem H hx hcxx
  have m5yxx := comm_mem H hy hcxx
  have m5xyx := comm_mem H hx hcyx
  have m5yyx := comm_mem H hy hcyx
  have m5xyy := comm_mem H hx hcyy
  have m5yyy := comm_mem H hy hcyy
  exact {BWTERM}
''')
# addWord
def bwexpr(w):
    # right-normed word over x,y as nested bracketWord
    s = 'bracketWord x y'
    assert w.endswith('xy')
    for ch in reversed(w[:-2]):
        s = f'bracketWord {ch} ({s})'
    return s
body = 'x * y'
for w, t in W.afac:
    body += f' *\n    powerScalar {zq(t)} ({bwexpr(w)})'
BN = {'xy': 'b2', 'xxy': 'b3x', 'yxy': 'b3y', 'xxxy': 'b4xx', 'yxxy': 'b4yx', 'yyxy': 'b4yy',
      'xxxxy': 'b5xxx', 'yxxxy': 'b5yxx', 'xyxxy': 'b5xyx', 'yyxxy': 'b5yyx', 'xyyxy': 'b5xyy',
      'yyyxy': 'b5yyy'}
AWTERM = 'H.mul_mem hx hy'
for w, t in W.afac:
    AWTERM = f'H.mul_mem ({AWTERM})\n    (powerScalar_mem H _ {BN[w]})'
P(f'''/-- Addition is recovered by removing the bracket, then the degree-three,
degree-four and central degree-five errors, each by a power of an exact
bracket monomial. -/
def addWord (x y : BCH (ZMod p) L hnil) : BCH (ZMod p) L hnil :=
  {body}

set_option maxHeartbeats 8000000 in
theorem val_addWord (x y : BCH (ZMod p) L hnil) :
    (addWord x y).val = x.val + y.val := by
  unfold addWord
  simp only [val_mul, val_powerScalar, val_bracketWord]
  have hsix := quint_central hnil
  have hba : ⁅y.val, x.val⁆ = -⁅x.val, y.val⁆ := (lie_skew y.val x.val).symm
  simp only [bch, {SIMP.replace('jacobi4c a b', 'jacobi4c x.val y.val')}]
  all_goals match_scalars
  all_goals (try field_simp [{NEP}])
  all_goals ring

theorem addWord_mem (H : Subgroup (BCH (ZMod p) L hnil))
    {{x y : BCH (ZMod p) L hnil}} (hx : x ∈ H) (hy : y ∈ H) : addWord x y ∈ H := by
  have b2 := bracketWord_mem H hx hy
  have b3x := bracketWord_mem H hx b2
  have b3y := bracketWord_mem H hy b2
  have b4xx := bracketWord_mem H hx b3x
  have b4yx := bracketWord_mem H hy b3x
  have b4yy := bracketWord_mem H hy b3y
  have b5xxx := bracketWord_mem H hx b4xx
  have b5yxx := bracketWord_mem H hy b4xx
  have b5xyx := bracketWord_mem H hx b4yx
  have b5yyx := bracketWord_mem H hy b4yx
  have b5xyy := bracketWord_mem H hx b4yy
  have b5yyy := bracketWord_mem H hy b4yy
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
def toLieSubalgebra (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
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
def toSubgroup (hnil : lowerCentralSeries (ZMod p) L L 5 = ⊥)
    (K : LieSubalgebra (ZMod p) L) : Subgroup (BCH (ZMod p) L hnil) where
  carrier := {{x | x.val ∈ K}}
  one_mem' := K.zero_mem
  inv_mem' hx := K.neg_mem hx
  mul_mem' := by
    intro x y hx hy
    change bch (F := ZMod p) x.val y.val ∈ K
    unfold bch
    have hxy := K.lie_mem hx hy
    have hyx := K.lie_mem hy hx
    exact K.add_mem (K.add_mem (K.sub_mem (K.sub_mem (K.add_mem (K.add_mem (K.add_mem hx hy)
      (K.smul_mem _ hxy)) (K.smul_mem _ (K.add_mem (K.lie_mem hx hxy) (K.lie_mem hy hyx))))
      (K.smul_mem _ (K.lie_mem hy (K.lie_mem hx hxy))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hy (K.lie_mem hy (K.lie_mem hy hyx)))
        (K.lie_mem hx (K.lie_mem hx (K.lie_mem hx hxy))))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hx (K.lie_mem hy (K.lie_mem hy hyx)))
        (K.lie_mem hy (K.lie_mem hx (K.lie_mem hx hxy))))))
      (K.smul_mem _ (K.add_mem (K.lie_mem hy (K.lie_mem hx (K.lie_mem hy hxy)))
        (K.lie_mem hx (K.lie_mem hy (K.lie_mem hx hyx)))))

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
end QSearch.BCHClassFiveSubgroups
''')
for n in ['val_comm', 'val_bracketWord', 'val_addWord', 'toLieSubalgebra', 'mem_toLieSubalgebra',
          'toSubgroup', 'toLieSubalgebra_toSubgroup', 'toSubgroup_toLieSubalgebra']:
    P(f"/-- info: 'QSearch.BCHClassFiveSubgroups.{n}' depends on axioms: [propext, Classical.choice, Quot.sound] -/\n#guard_msgs (whitespace := lax) in\n#print axioms QSearch.BCHClassFiveSubgroups.{n}\n")
open('/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassFiveSubgroups.lean', 'w').write('\n'.join(out))
