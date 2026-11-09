"""Write formal/Formal/BCHClassSeven.lean from the exact model (rules7.py).
Design aid only: Lean proves every rule and compares the two normal forms."""
from fractions import Fraction as Q
import rules7 as R
import model7 as M

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
INST = {4: R.INST4, 5: R.INST5, 6: R.INST6, 7: R.INST7}
PIV = {4: R.PIV4, 5: R.PIV5, 6: R.PIV6, 7: R.PIV7}
names = {}
rule_lines = []
BASE = ("lie_lie, lie_add, lie_sub, sub_lie, add_lie, lie_neg, neg_lie, neg_neg,\n"
        "      neg_add_rev, neg_sub, lie_self, lie_zero, zero_lie, neg_zero, hyx, hzx, hzy, jacobi3 x y z")
for n in (4, 5, 6, 7):
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
            assert coef.denominator == 1, (col, cert)
            es += [('' if coef > 0 else '-', e)] * abs(coef.numerator)
        lower = ''.join(f", {names[w]}" for m in range(4, n) for w in R.RULES[m])
        ev = ' '.join(dict.fromkeys(e for _, e in es))
        rule_lines.append(f"    simp only [{BASE}{lower}] at {ev}")
        combo = ' + '.join(f"{s}{e}" if s == '' else f"{s}{e}" for s, e in es).replace('+ -', '- ')
        rule_lines.append(f"    linear_combination (norm := module) {combo}")
ALLRULES = ', '.join(names[w] for n in (4, 5, 6, 7) for w in R.RULES[n])


# BCH definition terms (degrees 1-6 exactly as in BCHClassSix, then Z7)
Z7 = M.Z7
assert M.Z6 == [(Q(-1, 720), tuple('xxyyxy')), (Q(1, 240), tuple('xyxyxy')),
                (Q(1, 1440), tuple('xyyyxy')), (Q(1, 1440), tuple('yxxxxy'))]

def z7_groups():
    """Group the degree-7 terms by coefficient, in a fixed order."""
    g = {}
    for c, w in Z7:
        g.setdefault(c, []).append(''.join(w))
    return sorted(g.items(), key=lambda kv: (abs(kv[0]).denominator, abs(kv[0]).numerator, kv[0] < 0))

def scalar(a):
    """Lean scalar for a positive rational a."""
    if a.numerator == 1:
        return f"({a.denominator} : F)⁻¹"
    return f"({a.numerator} / {a.denominator} : F)"

def bch_def(xv='x', yv='y', ind='    '):
    mp = {'x': xv, 'y': yv}
    W = lambda s: word(tuple(s), mp)
    s = (f"{xv} + {yv} + (2 : F)⁻¹ • ⁅{xv}, {yv}⁆ +\n"
         f"{ind}(12 : F)⁻¹ • ({W('xxy')} + {W('yyx')}) - (24 : F)⁻¹ • {W('yxxy')} -\n"
         f"{ind}(720 : F)⁻¹ • ({W('yyyyx')} + {W('xxxxy')}) +\n"
         f"{ind}(360 : F)⁻¹ • ({W('xyyyx')} + {W('yxxxy')}) +\n"
         f"{ind}(120 : F)⁻¹ • ({W('yxyxy')} + {W('xyxyx')}) -\n"
         f"{ind}(720 : F)⁻¹ • {W('xxyyxy')} + (240 : F)⁻¹ • {W('xyxyxy')} +\n"
         f"{ind}(1440 : F)⁻¹ • ({W('xyyyxy')} + {W('yxxxxy')})")
    for c, ws in z7_groups():
        sg = '+' if c > 0 else '-'
        body = ' + '.join(W(w) for w in ws)
        if len(ws) > 1:
            body = f"({body})"
        s += f" {sg}\n{ind}{scalar(abs(c))} • {body}"
    return s

LOWTERMS = [(Q(1, 2), 'xy'), (Q(1, 12), 'xxy'), (Q(1, 12), 'yyx'), (Q(-1, 24), 'yxxy'),
            (Q(-1, 720), 'yyyyx'), (Q(-1, 720), 'xxxxy'), (Q(1, 360), 'xyyyx'), (Q(1, 360), 'yxxxy'),
            (Q(1, 120), 'yxyxy'), (Q(1, 120), 'xyxyx'), (Q(-1, 720), 'xxyyxy'), (Q(1, 240), 'xyxyxy'),
            (Q(1, 1440), 'xyyyxy'), (Q(1, 1440), 'yxxxxy')]
# the low-degree terms are exactly the class-six law (model check)
_low = M.add(M.gen('x'), M.gen('y'), *[M.sc(c, M.rn(tuple(w))) for c, w in LOWTERMS])
assert _low == M.bch6(M.gen('x'), M.gen('y'))

def z7_def(xv='x', yv='y', ind='    '):
    mp = {'x': xv, 'y': yv}
    W = lambda s: word(tuple(s), mp)
    out = ''
    for i, (c, ws) in enumerate(z7_groups()):
        body = ' + '.join(W(w) for w in ws)
        if len(ws) > 1:
            body = f"({body})"
        t = f"{scalar(abs(c))} • {body}"
        if i == 0:
            out += t if c > 0 else f"-({t})"
        else:
            out += f" {'+' if c > 0 else '-'}\n{ind}{t}"
    return out

def sc_signed(c):
    return f"{scalar(c)}" if c > 0 else f"(-{scalar(-c)})"

def shape_rhs(xv='x', yv='y', ind='      '):
    mp = {'x': xv, 'y': yv}
    terms = LOWTERMS + [(c, ''.join(w)) for c, w in Z7]
    parts = [f"{xv} + {yv}"] + [f"{sc_signed(c)} • {word(tuple(w), mp)}" for c, w in terms]
    out, line = [], ''
    for i, p in enumerate(parts):
        piece = p if i == 0 else f" + {p}"
        if len(line) + len(piece) > 90:
            out.append(line); line = ind + "+ " + p
        else:
            line += piece
    out.append(line)
    return '\n'.join(out)

def smooth(n):
    e = []
    for p in (2, 3, 5, 7):
        k = 0
        while n % p == 0: n //= p; k += 1
        e.append(k)
    assert n == 1, n
    return tuple(e)
Z7DENS = sorted({c.denominator for c, _ in Z7} | {abs(c.numerator) for c, _ in Z7 if abs(c.numerator) > 1})
NUMS = sorted(set([4, 6, 8, 12, 16, 24, 36, 48, 72, 120, 144, 180, 240, 360, 720, 1440]) | set(Z7DENS) - {1, 2, 3, 5, 7})
nehyps = '\n'.join(f"  have h{n} : ({n} : F) ≠ 0 := by\n    have := smooth7_ne_zero h2 h3 h5 h7 {' '.join(map(str, smooth(n)))}; norm_num at this; exact this" for n in NUMS)
nelist = ', '.join(['h2', 'h3', 'h5', 'h7'] + [f'h{n}' for n in NUMS])
NRULES = {n: len(R.RULES[n]) for n in (4, 5, 6, 7)}
DIMS = ', '.join(str(len(R.BASIS[n])) for n in range(1, 8))
Z7TXT = '\n '.join(f"{'+' if c > 0 else '-'} {abs(c)}·({' + '.join(ws)})" for c, ws in z7_groups())
PRIMES7 = sorted({p for c, _ in Z7 for p in (2, 3, 5, 7) if c.denominator % p == 0})
assert PRIMES7 == [2, 3, 5, 7], PRIMES7

lean = f'''import Formal.BCHClassSix

/-!
# The class-seven BCH group

The group law is the degree-seven truncated Baker-Campbell-Hausdorff product: the
sextic law of `BCHClassSix` plus the degree-seven part, written with right-normed
words in `x, y` (`xxyyxy` stands for `[x,[x,[y,[y,[x,y]]]]]`):
 {Z7TXT}
The degree-seven coefficients have denominators dividing `2^5 3^3 5 7 = 30240`,
so the law needs `2, 3, 5, 7 ≠ 0` in the field; every `ZMod p` with `p > 7` (so
every prime `p ≥ 11`) is included.

Associativity is proved from Jacobi and the lower-central bound
`lowerCentralSeries F L L 7 = ⊥` in two parts. First, the degree-seven part `z7`
is central and depends only on the degree-one parts of its arguments
(`z7_central`, `z7_peel_left`, `z7_peel_right`, applied to `bch_shape`), and a
central summand passes through the sextic law (`six_central_left/right`), so
both sides reduce to the sextic law of `BCHClassSix` plus `z7` terms. Second,
the remaining identity `defect` is checked as in `BCHClassSix`: both sides are
brought to a normal form of right-normed brackets in `x, y, z` (innermost pair
sorted), rewritten by one degree-three rule (`jacobi3 x y z`), {NRULES[4]} degree-four,
{NRULES[5]} degree-five, {NRULES[6]} degree-six and {NRULES[7]} degree-seven rules. The irreducible
words are a basis of the free class-seven Lie algebra on three generators
({DIMS} words in degrees 1-7), so the normal form is unique. Each rule is
proved in Lean from a few `lie_skew` or `lie_self` instances with integer
coefficients. The rules and certificates were chosen with the exact rational
model `research/audits/reviews/2026-11-05-rees-lean-c7/rules7.py`, and the
degree-seven coefficients were cross-checked against Dynkin's formula, a
Varadarajan recursion in Sage and nilpotent matrices (`cross7.py`,
`check_lean_def7.py`); Lean does not rely on any of them, it proves every rule
and checks that the two normal forms agree.
-/

namespace QSearch.BCHClassSeven

open LieModule
open QSearch.BCHClassFour (jacobi3 jacobi4c)

noncomputable section

/-- Explicit length-eight bracket vanishing, without a group-law hypothesis. -/
def ClassSeven (L : Type*) [LieRing L] : Prop :=
  ∀ a b c d e f g k : L, ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0

variable {{F L M N : Type*}} [Field F]
  [LieRing L] [LieAlgebra F L]
  [LieRing M] [LieAlgebra F M]
  [LieRing N] [LieAlgebra F N]

/-- Mathlib indexes the full Lie algebra as term zero. -/
theorem classSeven_of_lowerCentralSeries
    (hnil : lowerCentralSeries F L L 7 = ⊥) : ClassSeven L := by
  intro a b c d e f g k
  have h : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ ∈ lowerCentralSeries F L L 7 := by
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
    rw [lowerCentralSeries_succ]
    apply LieSubmodule.lie_mem_lie (LieSubmodule.mem_top f)
    rw [lowerCentralSeries_succ, lowerCentralSeries_zero]
    exact LieSubmodule.lie_mem_lie (LieSubmodule.mem_top g) (LieSubmodule.mem_top k)
  simpa only [hnil, LieSubmodule.mem_bot] using h

/-- The degree-seven truncated BCH polynomial. -/
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

/-- The degree-seven part of `bch`. -/
def z7 (x y : L) : L :=
  {z7_def()}

theorem bch_eq_six_add (x y : L) :
    bch (F := F) x y = QSearch.BCHClassSix.bch (F := F) x y + z7 (F := F) x y := by
  simp only [bch, QSearch.BCHClassSix.bch, z7]
  abel

/-- `bch` as `x + y` plus scalar multiples of single brackets `[p, q]`. -/
theorem bch_shape (x y : L) :
    bch (F := F) x y =
      {shape_rhs()} := by
  simp only [bch]
  module

section Central

variable (h : ClassSeven L)
include h

set_option linter.unusedSimpArgs false in
/-- Every degree-seven term is central. -/
theorem z7_central (a b w : L) : ⁅w, z7 (F := F) a b⁆ = 0 := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, lie_add, lie_sub, lie_neg, lie_smul, height, smul_zero, add_zero, sub_zero,
    neg_zero]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket added to its first argument. -/
theorem z7_peel_left (u v p q : L) (t : F) :
    z7 (F := F) (u + t • ⁅p, q⁆) v = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- `z7` ignores a bracket added to its second argument. -/
theorem z7_peel_right (u v p q : L) (t : F) :
    z7 (F := F) u (v + t • ⁅p, q⁆) = z7 (F := F) u v := by
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
  simp only [z7, add_lie, lie_add, sub_lie, lie_sub, smul_lie, lie_smul, lie_lie, neg_lie, lie_neg,
    height, smul_zero, smul_neg, smul_sub, neg_zero, add_zero, zero_add, sub_zero, zero_sub,
    lie_zero, zero_lie, sub_self]

omit h in
/-- A central summand passes through the sextic law (first argument). -/
theorem six_central_left (u v c : L) (hc : ∀ w : L, ⁅w, c⁆ = 0) :
    QSearch.BCHClassSix.bch (F := F) (u + c) v = QSearch.BCHClassSix.bch (F := F) u v + c := by
  have hc' : ∀ w : L, ⁅c, w⁆ = 0 := fun w => by rw [← lie_skew, hc, neg_zero]
  simp only [QSearch.BCHClassSix.bch, add_lie, lie_add, hc, hc', add_zero]
  abel

omit h in
/-- A central summand passes through the sextic law (second argument). -/
theorem six_central_right (u v c : L) (hc : ∀ w : L, ⁅w, c⁆ = 0) :
    QSearch.BCHClassSix.bch (F := F) u (v + c) = QSearch.BCHClassSix.bch (F := F) u v + c := by
  have hc' : ∀ w : L, ⁅c, w⁆ = 0 := fun w => by rw [← lie_skew, hc, neg_zero]
  simp only [QSearch.BCHClassSix.bch, add_lie, lie_add, hc, hc', add_zero]
  abel

end Central

section Assoc

variable (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (h7 : (7 : F) ≠ 0)
include h2 h3 h5 h7

/-- Products of the excluded primes are nonzero. -/
theorem smooth7_ne_zero (a b c d : ℕ) : ((2 : F) ^ a * 3 ^ b * 5 ^ c * 7 ^ d) ≠ 0 :=
  mul_ne_zero (mul_ne_zero (mul_ne_zero (pow_ne_zero _ h2) (pow_ne_zero _ h3))
    (pow_ne_zero _ h5)) (pow_ne_zero _ h7)

set_option linter.unusedSimpArgs false in
set_option maxHeartbeats 0 in
/-- The associativity defect of the sextic law in class seven, balanced by `z7`. -/
theorem defect (h : ClassSeven L) (x y z : L) :
    QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y +
        z7 (F := F) (x + y) z =
      QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) +
        z7 (F := F) y z + z7 (F := F) x (y + z) := by
{nehyps}
  have hyx : ⁅y, x⁆ = -⁅x, y⁆ := (lie_skew y x).symm
  have hzx : ⁅z, x⁆ = -⁅x, z⁆ := (lie_skew z x).symm
  have hzy : ⁅z, y⁆ = -⁅y, z⁆ := (lie_skew z y).symm
  have height (a b c d e f g k : L) : ⁅a, ⁅b, ⁅c, ⁅d, ⁅e, ⁅f, ⁅g, k⁆⁆⁆⁆⁆⁆⁆ = 0 :=
    h a b c d e f g k
{chr(10).join(rule_lines)}

  simp (maxSteps := 100000000) only [QSearch.BCHClassSix.bch, z7, add_lie, lie_add, sub_lie,
    lie_sub, smul_lie, lie_smul, lie_lie,
    neg_lie, lie_neg, height, lie_self, lie_zero, zero_lie, smul_zero, smul_neg, neg_neg,
    add_zero, zero_add, sub_zero, zero_sub, neg_zero, hyx, hzx, hzy, jacobi3 x y z,
    {ALLRULES}]
  match_scalars <;> field_simp [{nelist}]
  all_goals ring

omit h2 h3 h5 h7 in
/-- Associativity follows from Jacobi and the disappearance of length-eight brackets. -/
theorem bch_assoc_of_classSeven' (hdef : ∀ x y z : L,
      QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y +
          z7 (F := F) (x + y) z =
        QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) +
          z7 (F := F) y z + z7 (F := F) x (y + z))
    (h : ClassSeven L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) := by
  have e1 : z7 (F := F) (bch (F := F) x y) z = z7 (F := F) (x + y) z := by
    rw [bch_shape x y]
    simp only [z7_peel_left h]
  have e2 : QSearch.BCHClassSix.bch (F := F) (bch (F := F) x y) z =
      QSearch.BCHClassSix.bch (F := F) (QSearch.BCHClassSix.bch (F := F) x y) z + z7 (F := F) x y := by
    rw [bch_eq_six_add x y, six_central_left _ _ _ (fun w => z7_central h x y w)]
  have e3 : z7 (F := F) x (bch (F := F) y z) = z7 (F := F) x (y + z) := by
    rw [bch_shape y z]
    simp only [z7_peel_right h]
  have e4 : QSearch.BCHClassSix.bch (F := F) x (bch (F := F) y z) =
      QSearch.BCHClassSix.bch (F := F) x (QSearch.BCHClassSix.bch (F := F) y z) + z7 (F := F) y z := by
    rw [bch_eq_six_add y z, six_central_right _ _ _ (fun w => z7_central h y z w)]
  rw [bch_eq_six_add (bch (F := F) x y) z, bch_eq_six_add x (bch (F := F) y z), e1, e2, e3, e4]
  exact hdef x y z

/-- Associativity follows from Jacobi and the disappearance of length-eight brackets. -/
theorem bch_assoc_of_classSeven (h : ClassSeven L) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classSeven' (defect h2 h3 h5 h7 h) h x y z

end Assoc

theorem bch_assoc (hnil : lowerCentralSeries F L L 7 = ⊥)
    (h2 : (2 : F) ≠ 0) (h3 : (3 : F) ≠ 0) (h5 : (5 : F) ≠ 0) (h7 : (7 : F) ≠ 0) (x y z : L) :
    bch (F := F) (bch (F := F) x y) z = bch (F := F) x (bch (F := F) y z) :=
  bch_assoc_of_classSeven h2 h3 h5 h7 (classSeven_of_lowerCentralSeries hnil) x y z

/-- A separate carrier prevents the BCH multiplication from being confused with
the original additive structure. The class bound is a proof argument. -/
structure BCH (F L : Type*) [Field F] [LieRing L] [LieAlgebra F L]
    (hnil : lowerCentralSeries F L L 7 = ⊥) where
  val : L

@[ext] theorem BCH.ext {{hnil : lowerCentralSeries F L L 7 = ⊥}}
    {{x y : BCH F L hnil}} (h : x.val = y.val) : x = y := by
  cases x
  cases y
  cases h
  rfl

/-- The underlying exponential/logarithm bijection, with no compatibility assumed. -/
def equiv (hnil : lowerCentralSeries F L L 7 = ⊥) : BCH F L hnil ≃ L where
  toFun := BCH.val
  invFun := BCH.mk
  left_inv _ := rfl
  right_inv _ := rfl

variable [NeZero (2 : F)] [NeZero (3 : F)] [NeZero (5 : F)] [NeZero (7 : F)]

/-- All group laws are proved from the Lie structure and the class bound. -/
instance instGroup (hnil : lowerCentralSeries F L L 7 = ⊥) : Group (BCH F L hnil) where
  mul x y := ⟨bch (F := F) x.val y.val⟩
  one := ⟨0⟩
  inv x := ⟨-x.val⟩
  mul_assoc x y z := BCH.ext
    (bch_assoc hnil (NeZero.ne 2) (NeZero.ne 3) (NeZero.ne 5) (NeZero.ne 7) x.val y.val z.val)
  one_mul x := BCH.ext (bch_zero_left x.val)
  mul_one x := BCH.ext (bch_zero_right x.val)
  inv_mul_cancel x := BCH.ext (bch_neg_left x.val)

variable {{hL : lowerCentralSeries F L L 7 = ⊥}}
  {{hM : lowerCentralSeries F M M 7 = ⊥}}
  {{hN : lowerCentralSeries F N N 7 = ⊥}}

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

/-- Every Lie homomorphism between class-at-most-seven algebras gives a group map. -/
def lieHom (hL : lowerCentralSeries F L L 7 = ⊥)
    (hM : lowerCentralSeries F M M 7 = ⊥) (f : L →ₗ⁅F⁆ M) :
    BCH F L hL →* BCH F M hM where
  toFun x := ⟨f x.val⟩
  map_one' := BCH.ext (map_zero f)
  map_mul' x y := BCH.ext (map_bch f x.val y.val)

@[simp] theorem lieHom_apply (f : L →ₗ⁅F⁆ M) (x : BCH F L hL) :
    (lieHom hL hM f x).val = f x.val := rfl

/-- Every Lie equivalence gives an equivalence of the constructed groups. -/
def lieEquiv (hL : lowerCentralSeries F L L 7 = ⊥)
    (hM : lowerCentralSeries F M M 7 = ⊥) (e : L ≃ₗ⁅F⁆ M) :
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
end QSearch.BCHClassSeven
'''
GUARDS = [('classSeven_of_lowerCentralSeries', '[propext, Quot.sound]')] + [
    (n, '[propext, Classical.choice, Quot.sound]') for n in
    ['bch_assoc_of_classSeven', 'bch_assoc', 'instGroup', 'val_mul_formula', 'lieHom', 'lieEquiv', 'val_zpow']]
for n, ax in GUARDS:
    lean += f"\n/-- info: 'QSearch.BCHClassSeven.{n}' depends on axioms: {ax} -/\n#guard_msgs (whitespace := lax) in\n#print axioms QSearch.BCHClassSeven.{n}\n"
import sys
out = sys.argv[1] if len(sys.argv) > 1 else '/Users/jaspersands/Developer/qsearch/formal/Formal/BCHClassSeven.lean'
open(out, 'w').write(lean)
print('wrote', out, len(lean.splitlines()), 'lines', 'NUMS', NUMS)
