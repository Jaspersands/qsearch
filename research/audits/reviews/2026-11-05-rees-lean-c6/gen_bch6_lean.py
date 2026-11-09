"""Write formal/Formal/BCHClassSix.lean from the exact model (rules6.py).
Design aid only: Lean proves every rule and compares the two normal forms."""
from fractions import Fraction as Q
import rules6 as R
import model6 as M

def word(w, mp=None):
    mp = mp or {}
    f = lambda c: mp.get(c, c)
    s = f(w[-1])
    for ch in reversed(w[:-1]):
        s = f"⁅{f(ch)}, {s}⁆"
    return s

def lin(d):
    parts = []
    for w in sorted(d):
        c = d[w]
        assert c.denominator == 1
        for _ in range(abs(c.numerator)):
            parts.append(('+' if c > 0 else '-', word(w)))
    s = ''
    for i, (sg, t) in enumerate(parts):
        s += (t if sg == '+' else f"-{t}") if i == 0 else f" {sg} {t}"
    return s or '0'

JAC4C = {('x','y','x','y'): 'x y', ('x','z','x','z'): 'x z', ('y','z','y','z'): 'y z'}
INST = {4: R.INST4, 5: R.INST5, 6: R.INST6}
PIV = {4: R.PIV4, 5: R.PIV5, 6: R.PIV6}
names = {}
rule_lines = []
BASE = ("lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,\n"
        "      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z")
for n in (4, 5, 6):
    for k, (col, v, cert) in enumerate(PIV[n]):
        nm = f"r{n}{chr(ord('a') + k)}" if k < 26 else f"r{n}{chr(ord('a') + k - 26)}{chr(ord('a') + k - 26)}"
        names[col] = nm
        rhs = lin(R.RULES[n][col])
        rule_lines.append(f"  have {nm} : {word(col)} =\n      {rhs} := by")
        if col in JAC4C:
            rule_lines.append(f"    exact jacobi4c {JAC4C[col]}")
            continue
        es = []
        for j, (i, c) in enumerate(sorted(cert.items())):
            U, V = INST[n][i][0]
            e = f"e{j}"
            if U == V:
                a, W = U[0], U[1:]
                rule_lines.append(f"    have {e} := (lie_lie (x := {a}) (y := ({word(W)} : L)) (m := ({word(U)} : L))).symm.trans\n"
                                  f"      (lie_self ({word(U)} : L))")
                coef = c
            else:
                rule_lines.append(f"    have {e} := lie_skew ({word(U)} : L) {word(V)}")
                coef = -c
            assert coef.denominator == 1 and abs(coef.numerator) == 1, (col, cert)
            es.append(('' if coef > 0 else '-', e))
        lower = ''.join(f", {names[w]}" for m in range(4, n) for w in R.RULES[m])
        ev = ' '.join(e for _, e in es)
        rule_lines.append(f"    simp only [{BASE}{lower}] at {ev}")
        combo = ' + '.join(f"{s}{e}" if s == '' else f"{s}{e}" for s, e in es).replace('+ -', '- ')
        rule_lines.append(f"    linear_combination (norm := module) {combo}")
ALLRULES = ', '.join(names[w] for n in (4, 5, 6) for w in R.RULES[n])

# BCH definition terms
def coeff_term(c, w, mp):
    return c, word(w, mp)

Z6 = M.Z6
def z6_lean(mp):
    # Z6 = -1/720 xxyyxy + 1/240 xyxyxy + 1/1440 (xyyyxy + yxxxxy)
    d = {}
    for c, w in Z6:
        d.setdefault(c, []).append(word(w, mp))
    return d

def bch_def(xv='x', yv='y', ind='    '):
    mp = {'x': xv, 'y': yv}
    W = lambda s: word(tuple(s), mp)
    return (f"{xv} + {yv} + (2 : F)⁻¹ • ⁅{xv}, {yv}⁆ +\n"
            f"{ind}(12 : F)⁻¹ • ({W('xxy')} + {W('yyx')}) - (24 : F)⁻¹ • {W('yxxy')} -\n"
            f"{ind}(720 : F)⁻¹ • ({W('yyyyx')} + {W('xxxxy')}) +\n"
            f"{ind}(360 : F)⁻¹ • ({W('xyyyx')} + {W('yxxxy')}) +\n"
            f"{ind}(120 : F)⁻¹ • ({W('yxyxy')} + {W('xyxyx')}) -\n"
            f"{ind}(720 : F)⁻¹ • {W('xxyyxy')} + (240 : F)⁻¹ • {W('xyxyxy')} +\n"
            f"{ind}(1440 : F)⁻¹ • ({W('xyyyxy')} + {W('yxxxxy')})")
# sanity: the Lean definition list matches the model
assert sorted((c, ''.join(w)) for c, w in Z6) == sorted([(Q(-1, 720), 'xxyyxy'), (Q(1, 240), 'xyxyxy'), (Q(1, 1440), 'xyyyxy'), (Q(1, 1440), 'yxxxxy')])

def smooth(n):
    a = b = c = 0
    while n % 2 == 0: n //= 2; a += 1
    while n % 3 == 0: n //= 3; b += 1
    while n % 5 == 0: n //= 5; c += 1
    assert n == 1
    return a, b, c
NUMS = [4, 6, 8, 12, 16, 24, 36, 48, 72, 120, 144, 180, 240, 360, 720, 1440]
nehyps = '\n'.join(f"  have h{n} : ({n} : F) ≠ 0 := by\n    have := smooth_ne_zero h2 h3 h5 {' '.join(map(str, smooth(n)))}; norm_num at this; exact this" for n in NUMS)
nelist = ', '.join(['h2', 'h3', 'h5'] + [f'h{n}' for n in NUMS])

lean = f'''import Formal.BCHClassFive

/-!
# The class-six BCH group

The group law is the degree-six truncated Baker-Campbell-Hausdorff product: the
quintic law of `BCHClassFive` plus the degree-six terms
`- [x,[x,[y,[y,[x,y]]]]]/720 + [x,[y,[x,[y,[x,y]]]]]/240
 + ([x,[y,[y,[y,[x,y]]]]] + [y,[x,[x,[x,[x,y]]]]])/1440`.
All coefficients have denominators `2^a 3^b 5^c`, so only `2, 3, 5 ≠ 0` is needed
in the field and every `ZMod p` with `p > 5` (hence every `p > 6`) is included.

Associativity is proved from Jacobi and the lower-central bound
`lowerCentralSeries F L L 6 = ⊥` exactly as in `BCHClassFive`: both sides are
brought to a normal form of right-normed brackets in `x, y, z` (innermost pair
sorted), rewritten by one degree-three rule (`jacobi3 x y z`), six degree-four,
six degree-five and twenty-eight degree-six rules. The irreducible words are a
basis of the free class-six Lie algebra on three generators (3, 3, 8, 18, 48, 116
words in degrees 1-6), so the normal form is unique. Each rule is proved in Lean
from at most two `lie_skew` or `lie_self` instances. The rules and certificates
were chosen with the exact rational model
`research/audits/reviews/2026-11-05-rees-lean-c6/rules6.py`; Lean does not rely
on that model, it proves every rule and checks that the two normal forms agree.
-/

namespace QSearch.BCHClassSix

open LieModule
open QSearch.BCHClassFour (jacobi3 jacobi4c)
open QSearch.BCHClassFive (smooth_ne_zero)

noncomputable section

/-- Explicit length-seven bracket vanishing, without a group-law hypothesis. -/
def ClassSix (L : Type*) [LieRing L] : Prop :=
  ∀ a b c d e f g : L, ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, g⁆⁆⁆⁆⁆⁆ = 0

variable {{F L M N : Type*}} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classSix_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 6 = ⊥) : ClassSix L := by
  intro a b c d e f g
  have h : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, g⁆⁆⁆⁆⁆⁆ ∈ lowerCentralSeries F L L 6 := by
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top a)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top b)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top c)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top d)
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top e)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top f) (LieSubmodule.mem_top g)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The degree-six truncated BCH polynomial. -/
def bch (x y : L) : L :=
  {bch_def()}

@[simp] theorem bch_zero_left (x : L) : bch (F := F) 0 x = x := by
  simp [bch]

@[simp] theorem bch_zero_right (x : L) : bch (F := F) x 0 = x := by
  simp [bch]

@[simp] theorem bch_neg_left (x : L) : bch (F := F) (-x) x = 0 := by
  simp [bch]

@[simp] theorem bch_neg_right (x : L) : bch (F := F) x (-x) = 0 := by
  simp [bch]

/-- Lie-commuting elements multiply by addition. -/
theorem bch_of_lie_eq_zero {{x y : L}} (h : ⁅x, y⁆ = 0) :
    bch (F := F) x y = x + y := by
  have hyx : ⁅y, x⁆ = 0 := by rw [← lie_skew y x, h, neg_zero]
  simp [bch, h, hyx]

/-- Lie maps preserve the actual BCH polynomial, without any class hypothesis. -/
theorem map_bch (f : L →ₗ⁅F⁆ M) (x y : L) :
    f (bch (F := F) x y) = bch (F := F) (f x) (f y) := by
  simp only [bch, map_add, map_sub, map_smul, LieHom.map_lie]

/-- Scalar multiples of one vector have vanishing mutual brackets. -/
theorem bch_smul_same (a b : F) (x : L) :
    bch (F := F) (a • x) (b • x) = (a + b) • x := by
  simp [bch, smul_lie, lie_smul, add_smul]

section Assoc

variable (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0)
include h2 h3 h5

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- Associativity follows from Jacobi and the disappearance of length-seven brackets. -/
theorem bch_assoc_of_classSix (h : ClassSix L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
{nehyps}
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have hseven (a b c d e f g : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, g⁆⁆⁆⁆⁆⁆ = 0 := h a b c d e f g
{chr(10).join(rule_lines)}

  simp only [bch, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, hseven, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, zero_sub, neg_zero, hyx, hzx, hzy, jacobi3 x y z,
    {ALLRULES}]
  match_scalars <;> field_simp [{nelist}]
  all_goals ring

end Assoc

theorem bch_assoc (hnil : lowerCentralSeries F L L 6 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classSix h2 h3 h5 (classSix_of_lowerCentralSeries hnil) x y z

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 6 = ⊥) where
  val : L

@[ext] theorem BCH.ext {{hnil : lowerCentralSeries F L L 6 = ⊥}}
    {{x y : BCH F L hnil}} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 6 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 6 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext
    (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) (NeZero.ne 5) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {{hL : lowerCentralSeries F L L 6 = ⊥}}
  {{hM : lowerCentralSeries F M M 6 = ⊥}}
  {{hN : lowerCentralSeries F N N 6 = ⊥}}

@[simp] theorem val_mul (x y : BCH F L hL) :
    (x * y).val = bch (F := F) x.val y.val := rfl

/-- The value formula used to integrate concrete Lie-algebra constructions. -/
theorem val_mul_formula (x y : BCH F L hL) :
    (x * y).val = {bch_def('x.val', 'y.val', '      ')} := rfl

@[simp] theorem val_one : (1 : BCH F L hL).val = 0 := rfl

@[simp] theorem val_inv (x : BCH F L hL) : x⁻¹.val = -x.val := rfl

/-- Natural group powers have the actual scalar-multiple logarithm. -/
@[simp] theorem val_pow (x : BCH F L hL) (n : ℕ) :
    (x ^ n).val = (n : F) • x.val := by
  induction n with
  | zero => simp
  | succ n ih =>
    simp [pow_succ, ih, bch, smul_lie, lie_smul, add_smul]

/-- Integer group powers have the actual scalar-multiple logarithm. -/
@[simp] theorem val_zpow (x : BCH F L hL) (n : ℤ) :
    (x ^ n).val = (n : F) • x.val := by
  cases n with
  | ofNat n => simp
  | negSucc n => simp only [zpow_negSucc, val_inv, val_pow, Int.cast_negSucc, neg_smul]

/-- Every Lie homomorphism between class-at-most-six algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 6 = ⊥)
    (hM : lowerCentralSeries F M M 6 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 6 = ⊥)
    (hM : lowerCentralSeries F M M 6 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
    BCH F L hL ≃* BCH F M hM where
  toFun := lieHom hL hM e.toLieHom
  invFun := lieHom hM hL e.symm.toLieHom
  left_inv x := BCH.ext (e.symm_apply_apply x.val)
  right_inv x := BCH.ext (e.apply_symm_apply x.val)
  map_mul' := (lieHom hL hM e.toLieHom).map_mul

@[simp] theorem lieEquiv_apply (e : L ≃ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieEquiv hL hM e x).val = e x.val := rfl

@[simp] theorem lieHom_id : lieHom hL hL (LieHom.id : L →ₗ⁅F⁆ L) = MonoidHom.id _ := by
  ext x
  rfl

@[simp] theorem lieHom_comp (f : L →ₗ⁅F⁆ M) (g : M →ₗ⁅F⁆ N) :
    lieHom hL hN (g.comp f) = (lieHom hM hN g).comp (lieHom hL hM f) := by
  ext x
  rfl

@[simp] theorem lieEquiv_symm (e : L ≃ₗ⁅F⁆ M) :
    (lieEquiv hL hM e).symm = lieEquiv hM hL e.symm := by
  ext x
  rfl

end
end QSearch.BCHClassSix
'''
GUARDS = [('classSix_of_lowerCentralSeries', '[propext, Quot.sound]')] + [
    (n, '[propext, Classical.choice, Quot.sound]') for n in
    ['bch_assoc_of_classSix', 'bch_assoc', 'instGroup', 'val_mul_formula', 'lieHom', 'lieEquiv', 'val_zpow']]
for n, ax in GUARDS:
    lean += f"\n/-- info: 'QSearch.BCHClassSix.{n}' depends on axioms: {ax} -/\n#guard_msgs (whitespace := lax) in\n#print axioms QSearch.BCHClassSix.{n}\n"
import sys
out = sys.argv[1] if len(sys.argv) > 1 else '/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassSix.lean'
open(out, 'w').write(lean)
print('wrote', out, len(lean.splitlines()), 'lines')
