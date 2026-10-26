import Mathlib.Algebra.Lie.Basic
import Mathlib.LinearAlgebra.Span.Defs
import Mathlib.LinearAlgebra.Multilinear.Basic
import Mathlib.Tactic

/-!
# Class-three chart and common-potential algebra

Universal Lie-algebra identities, not finite-field interpolation controls.
Characteristic two and three are excluded explicitly where division is used.
The derived space is the span of actual brackets, not a supplied abelian
ideal with its needed identities assumed.
-/

namespace QSearch.ClassThreePotential

noncomputable section
variable {F L : Type*} [Field F] [LieRing L] [LieAlgebra F L]

def derived : Submodule F L :=
  Submodule.span F (Set.range (fun xy : L × L => ⁅xy.1, xy.2⁆))

def ClassThree (L : Type*) [LieRing L] : Prop :=
  ∀ x y z w : L, ⁅x, ⁅y, ⁅z, w⁆⁆⁆ = 0

theorem bracket_mem (x y : L) : ⁅x, y⁆ ∈ derived (F := F) :=
  Submodule.subset_span ⟨(x, y), rfl⟩

theorem derived_double (h3 : ClassThree L) (x y a : L)
    (ha : a ∈ derived (F := F)) : ⁅x, ⁅y, a⁆⁆ = 0 := by
  induction ha using Submodule.span_induction with
  | mem z hz =>
    obtain ⟨⟨v, w⟩, rfl⟩ := hz
    exact h3 x y v w
  | zero => simp
  | add a b _ _ ha hb => simp only [lie_add, ha, hb, add_zero]
  | smul r a _ ha => simp only [lie_smul, ha, smul_zero]

theorem derived_abelian (h3 : ClassThree L) (a b : L)
    (ha : a ∈ derived (F := F)) (hb : b ∈ derived (F := F)) :
    ⁅a, b⁆ = 0 := by
  induction ha using Submodule.span_induction with
  | mem z hz =>
    obtain ⟨⟨x, y⟩, rfl⟩ := hz
    rw [lie_lie, derived_double h3 x y b hb, derived_double h3 y x b hb, sub_self]
  | zero => simp
  | add a c _ _ ha hc => simp only [add_lie, ha, hc, add_zero]
  | smul r a _ ha => simp only [smul_lie, ha, smul_zero]

def action (q a : L) : L := a + ⁅q, a⁆

def cocycle (q r : L) : L :=
  (2 : F)⁻¹ • ⁅q, r⁆ + (3 : F)⁻¹ • ⁅q, ⁅q, r⁆⁆
    + ((2 : F)⁻¹ * (3 : F)⁻¹) • ⁅r, ⁅q, r⁆⁆

def bch (x y : L) : L :=
  x + y + (2 : F)⁻¹ • ⁅x, y⁆
    + ((2 : F)⁻¹ ^ 2 * (3 : F)⁻¹) • (⁅x, ⁅x, y⁆⁆ - ⁅y, ⁅x, y⁆⁆)

def graph (u a : L) : L := a + (2 : F)⁻¹ • ⁅u, a⁆

def potential (q u a : L) : L :=
  a + ⁅q, a⁆ - (2 : F)⁻¹ • ⁅u, a⁆
    + (2 : F)⁻¹ • ⁅q, u⁆ + (3 : F)⁻¹ • ⁅q, ⁅q, u⁆⁆
    - ((2 : F)⁻¹ * (3 : F)⁻¹) • ⁅u, ⁅q, u⁆⁆

theorem graph_mem (u a : L) (ha : a ∈ derived (F := F)) :
    graph (F := F) u a ∈ derived (F := F) :=
  (derived (F := F)).add_mem ha ((derived (F := F)).smul_mem _ (bracket_mem u a))

theorem cocycle_mem (q r : L) : cocycle (F := F) q r ∈ derived (F := F) := by
  exact (derived (F := F)).add_mem
    ((derived (F := F)).add_mem
      ((derived (F := F)).smul_mem _ (bracket_mem q r))
      ((derived (F := F)).smul_mem _ (bracket_mem q ⁅q, r⁆)))
    ((derived (F := F)).smul_mem _ (bracket_mem r ⁅q, r⁆))

theorem potential_mem (q u a : L) (ha : a ∈ derived (F := F)) :
    potential (F := F) q u a ∈ derived (F := F) := by
  exact (derived (F := F)).sub_mem
    ((derived (F := F)).add_mem
      ((derived (F := F)).add_mem
        ((derived (F := F)).sub_mem
          ((derived (F := F)).add_mem ha (bracket_mem q a))
          ((derived (F := F)).smul_mem _ (bracket_mem u a)))
        ((derived (F := F)).smul_mem _ (bracket_mem q u)))
      ((derived (F := F)).smul_mem _ (bracket_mem q ⁅q, u⁆)))
    ((derived (F := F)).smul_mem _ (bracket_mem u ⁅q, u⁆))

theorem action_add (h3 : ClassThree L) (q r a : L)
    (ha : a ∈ derived (F := F)) :
    action (q + r) a = action q (action r a) := by
  simp only [action, add_lie, lie_add, derived_double h3 q r a ha]
  abel

/-- Exp(n) exp(q) has logarithm n+q-[q,n]/2. -/
theorem normal_chart (h3 : ClassThree L) (q n : L)
    (hn : n ∈ derived (F := F)) :
    bch (F := F) n q = n + q - (2 : F)⁻¹ • ⁅q, n⁆ := by
  have hnq : ⁅n, q⁆ = -⁅q, n⁆ := (lie_skew n q).symm
  simp only [bch, hnq, lie_neg, derived_double h3 n q n hn,
    derived_double h3 q q n hn, neg_zero, sub_self, smul_zero, add_zero]
  module

theorem graph_log (h3 : ClassThree L) (u a : L)
    (ha : a ∈ derived (F := F)) :
    bch (F := F) (graph (F := F) u a) u = u + a := by
  rw [normal_chart h3 u _ (graph_mem u a ha)]
  simp only [graph, lie_add, lie_smul, derived_double h3 u u a ha, smul_zero,
    add_zero]
  module

/-- The compact section construction expands into the explicit cubic. -/
theorem potential_expansion (h3 : ClassThree L) (h2 : (2 : F) ≠ 0)
    (q u a : L) (ha : a ∈ derived (F := F)) :
    action (q - u) (graph (F := F) u a) + cocycle (F := F) (q - u) u =
      potential (F := F) q u a := by
  simp only [action, graph, cocycle, potential, sub_lie, lie_add,
    lie_smul, lie_self, sub_zero, derived_double h3 q u a ha,
    derived_double h3 u u a ha, smul_zero, add_zero]
  match_scalars <;> field_simp <;> ring

/-- The key increment identity. The only hidden-subgroup premise is that
the two lifted logarithms commute; no increment/cocycle identity is assumed. -/
theorem potential_increment (h3 : ClassThree L) (h2 : (2 : F) ≠ 0)
    (q u v a b : L) (ha : a ∈ derived (F := F)) (hb : b ∈ derived (F := F))
    (commute : ⁅u + a, v + b⁆ = 0) :
    potential (F := F) (q + v) (u + v) (a + b) - potential (F := F) q u a =
      action q (graph (F := F) v b) + cocycle (F := F) q v := by
  have ha0 (x y : L) : ⁅x, ⁅y, a⁆⁆ = 0 := derived_double h3 x y a ha
  have hb0 (x y : L) : ⁅x, ⁅y, b⁆⁆ = 0 := derived_double h3 x y b hb
  have hav : ⁅a, v⁆ = -⁅v, a⁆ := (lie_skew a v).symm
  have hzero : ⁅u, v⁆ + ⁅u, b⁆ - ⁅v, a⁆ = 0 := by
    have h : ⁅u, v⁆ - ⁅v, a⁆ + ⁅u, b⁆ = 0 := by
      simpa only [add_lie, lie_add, derived_abelian h3 a b ha hb, add_zero,
        hav, ← sub_eq_add_neg] using commute
    calc
      ⁅u, v⁆ + ⁅u, b⁆ - ⁅v, a⁆ = ⁅u, v⁆ - ⁅v, a⁆ + ⁅u, b⁆ := by abel
      _ = 0 := h
  have huv : ⁅u, v⁆ = ⁅v, a⁆ - ⁅u, b⁆ :=
    eq_sub_of_add_eq (sub_eq_zero.mp hzero)
  have hvu : ⁅v, u⁆ = ⁅u, b⁆ - ⁅v, a⁆ := by
    rw [← lie_skew v u, huv]
    abel
  have hkill (x : L) : ⁅x, ⁅v, u⁆⁆ = 0 := by
    rw [hvu, lie_sub, hb0, ha0, sub_self]
  have hquv : ⁅q, ⁅u, v⁆⁆ = 0 := by
    rw [← lie_skew u v, lie_neg, hkill, neg_zero]
  have hvq : ⁅v, q⁆ = -⁅q, v⁆ := (lie_skew v q).symm
  have hj : ⁅v, ⁅q, u⁆⁆ = ⁅u, ⁅q, v⁆⁆ := by
    have h := lie_jacobi q u v
    rw [hquv, hvq, lie_neg, zero_add] at h
    exact sub_eq_zero.mp (by simpa only [sub_eq_add_neg, add_comm] using h)
  simp only [potential, action, graph, cocycle, add_lie, lie_add, lie_smul,
    lie_self, add_zero, hvu, lie_sub, ha0, hb0, sub_self, hj,
    smul_zero]
  match_scalars <;> field_simp <;> ring

/-- The class-three BCH product in the normal-first exponential chart.
No chart multiplication or cocycle identity is a hypothesis. -/
theorem chart_product (h3 : ClassThree L) (h2 : (2 : F) ≠ 0)
    (hthree : (3 : F) ≠ 0) (q r n n' : L)
    (hn : n ∈ derived (F := F)) (hn' : n' ∈ derived (F := F)) :
    bch (F := F) (bch (F := F) n q) (bch (F := F) n' r) =
      bch (F := F) (n + action q n' + cocycle (F := F) q r) (q + r) := by
  have hn0 (x y : L) : ⁅x, ⁅y, n⁆⁆ = 0 := derived_double h3 x y n hn
  have hn'0 (x y : L) : ⁅x, ⁅y, n'⁆⁆ = 0 := derived_double h3 x y n' hn'
  have hnd (x y : L) : ⁅n, ⁅x, y⁆⁆ = 0 :=
    derived_abelian h3 n _ hn (bracket_mem x y)
  have hn'd (x y : L) : ⁅n', ⁅x, y⁆⁆ = 0 :=
    derived_abelian h3 n' _ hn' (bracket_mem x y)
  have hnn : ⁅n, n'⁆ = 0 := derived_abelian h3 n n' hn hn'
  have hnr : ⁅n, r⁆ = -⁅r, n⁆ := (lie_skew n r).symm
  have hfour (x y z w : L) : ⁅x, ⁅y, ⁅z, w⁆⁆⁆ = 0 := h3 x y z w
  have hnormal : n + action q n' + cocycle (F := F) q r ∈ derived (F := F) :=
    (derived (F := F)).add_mem
      ((derived (F := F)).add_mem hn
        ((derived (F := F)).add_mem hn' (bracket_mem q n')))
      (cocycle_mem q r)
  rw [normal_chart h3 q n hn, normal_chart h3 r n' hn',
    normal_chart h3 (q + r) _ hnormal]
  simp only [bch, action, cocycle, add_lie, lie_add, sub_lie, lie_sub,
    smul_lie, lie_smul, lie_lie, hn0, hn'0, hnd, hn'd, hnn, hfour, hnr,
    lie_neg, lie_zero, smul_zero, add_zero, zero_add, sub_zero, sub_self, neg_zero]
  match_scalars <;> field_simp <;> ring

def sectionPotential (projection normal : L →ₗ[F] L) (q : L) : L :=
  potential (F := F) q (projection q) (normal (projection q))

def quadraticForm (projection normal : L →ₗ[F] L) :
    MultilinearMap F (fun _ : Fin 2 => L) L := by
  refine MultilinearMap.mk' (fun v =>
    ⁅v 0, normal (projection (v 1))⁆
      - (2 : F)⁻¹ • ⁅projection (v 0), normal (projection (v 1))⁆
      + (2 : F)⁻¹ • ⁅v 0, projection (v 1)⁆) ?_ ?_
  · intro v i x y
    fin_cases i <;> simp <;> module
  · intro v i c x
    fin_cases i <;> simp <;> module

def cubicForm (projection : L →ₗ[F] L) :
    MultilinearMap F (fun _ : Fin 3 => L) L := by
  refine MultilinearMap.mk' (fun v =>
    (3 : F)⁻¹ • ⁅v 0, ⁅v 1, projection (v 2)⁆⁆
      - ((2 : F)⁻¹ * (3 : F)⁻¹) • ⁅projection (v 0), ⁅v 1, projection (v 2)⁆⁆) ?_ ?_
  · intro v i x y
    fin_cases i <;> simp <;> module
  · intro v i c x
    fin_cases i <;> simp <;> module

/-- An actual degree certificate: a linear map plus diagonal evaluations
of bundled bilinear and trilinear maps. It is not inferred from scaling
tests or interpolation over a finite field. -/
theorem section_cubic_decomposition (projection normal : L →ₗ[F] L) (q : L) :
    sectionPotential projection normal q =
      (normal.comp projection) q
        + quadraticForm projection normal (fun _ => q)
        + cubicForm projection (fun _ => q) := by
  simp only [sectionPotential, potential, quadraticForm, cubicForm,
    MultilinearMap.mk'_apply, LinearMap.comp_apply]
  module

/-- A single polynomial is fixed by proof-only linear witnesses for the
entire hidden subspace, not chosen anew for each source coset. -/
theorem section_increment (h3 : ClassThree L) (h2 : (2 : F) ≠ 0)
    (U : Submodule F L) (projection normal : L →ₗ[F] L)
    (hrange : ∀ q, projection q ∈ U)
    (hfix : ∀ v ∈ U, projection v = v)
    (hnormal : ∀ u ∈ U, normal u ∈ derived (F := F))
    (hcommute : ∀ u ∈ U, ∀ v ∈ U, ⁅u + normal u, v + normal v⁆ = 0)
    (q v : L) (hv : v ∈ U) :
    sectionPotential projection normal (q + v) - sectionPotential projection normal q =
      action q (graph (F := F) v (normal v)) + cocycle (F := F) q v := by
  simpa only [sectionPotential, map_add, hfix v hv] using
    potential_increment h3 h2 q (projection q) v (normal (projection q)) (normal v)
      (hnormal _ (hrange q)) (hnormal v hv) (hcommute _ (hrange q) v hv)

/-- The log-coordinate form of the right-action law used by the source
Fourier theorem, now derived from Lie axioms rather than assumed. -/
theorem section_right_action (h3 : ClassThree L) (h2 : (2 : F) ≠ 0)
    (hthree : (3 : F) ≠ 0) (U : Submodule F L) (projection normal : L →ₗ[F] L)
    (hrange : ∀ q, projection q ∈ U)
    (hfix : ∀ v ∈ U, projection v = v)
    (hnormal : ∀ u ∈ U, normal u ∈ derived (F := F))
    (hcommute : ∀ u ∈ U, ∀ v ∈ U, ⁅u + normal u, v + normal v⁆ = 0)
    (q v n : L) (hv : v ∈ U) (hn : n ∈ derived (F := F)) :
    bch (F := F) (bch (F := F) n q) (v + normal v) =
      bch (F := F) (n + sectionPotential projection normal (q + v)
        - sectionPotential projection normal q) (q + v) := by
  calc
    bch (F := F) (bch (F := F) n q) (v + normal v) =
        bch (F := F) (bch (F := F) n q) (bch (F := F) (graph (F := F) v (normal v)) v) := by
      rw [graph_log h3 v _ (hnormal v hv)]
    _ = bch (F := F) (n + action q (graph (F := F) v (normal v))
        + cocycle (F := F) q v) (q + v) :=
      chart_product h3 h2 hthree q v n _ hn (graph_mem v _ (hnormal v hv))
    _ = bch (F := F) (n + sectionPotential projection normal (q + v)
        - sectionPotential projection normal q) (q + v) := by
      congr 1
      rw [show n + sectionPotential projection normal (q + v)
          - sectionPotential projection normal q =
          n + (sectionPotential projection normal (q + v)
            - sectionPotential projection normal q) by abel,
        section_increment h3 h2 U projection normal hrange hfix hnormal hcommute q v hv]
      abel

/-- info: 'QSearch.ClassThreePotential.potential_increment' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreePotential.potential_increment

/-- info: 'QSearch.ClassThreePotential.chart_product' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreePotential.chart_product

/-- info: 'QSearch.ClassThreePotential.section_right_action' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreePotential.section_right_action

/-- info: 'QSearch.ClassThreePotential.section_cubic_decomposition' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.ClassThreePotential.section_cubic_decomposition

end
end QSearch.ClassThreePotential
