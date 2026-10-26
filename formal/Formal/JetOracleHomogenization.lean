import Mathlib.GroupTheory.SemidirectProduct
import Mathlib.Tactic

/-!
# Public tuple-oracle reduction to a cocycle graph subgroup

The operational tuple oracle contains neither the cocycle nor its potential.
The theorem proves its exact coset relation from component hiding relations,
an injective public evaluation homomorphism, and a common left normalization.
Actual polynomial degree, simplex unisolvence, circuit synthesis and quantum
central descent are not formalized by this module.
-/

namespace QSearch.JetOracleHomogenization

noncomputable section

section NormalizedDifference
variable {k V N : Type*} [Field k] [AddCommGroup V] [Module k V] [Group N]

def normalizedDifference (P : V → N) (q u : V) (t : k) : N :=
  (P u)⁻¹ * P (u + t • q)

/-- The nonabelian cocycle law follows from the actual normalization order. -/
theorem normalized_cocycle (P : V → N) (q r u : V) (t : k) :
    normalizedDifference P (q+r) u t =
      normalizedDifference P q u t * normalizedDifference P r (u+t • q) t := by
  simp only [normalizedDifference, smul_add, ← add_assoc]
  group

/-- Scaling covariance is an identity of the actual pointwise curve. -/
theorem normalized_scaling (P : V → N) (q u : V) (t s : k) :
    normalizedDifference P (s • q) u t = normalizedDifference P q u (t*s) := by
  simp only [normalizedDifference, mul_smul]

end NormalizedDifference

variable {Q J : Type*} [Group Q] [Group J]
variable (action : Q →* MulAut J) (F : Q → J)
variable (hF : ∀ q r, F (q*r) = F q * action q (F r))

include hF in
theorem cocycle_one : F 1 = 1 := by
  have h := hF 1 1
  simp only [one_mul, map_one, MulAut.one_apply] at h
  have hc := congrArg (fun x : J => (F 1)⁻¹*x) h
  simpa [mul_assoc] using hc.symm

def graphHom : Q →* J ⋊[action] Q where
  toFun q := ⟨F q, q⟩
  map_one' := SemidirectProduct.ext (cocycle_one action F hF) rfl
  map_mul' q r := SemidirectProduct.ext (hF q r) rfl

@[simp] theorem graph_right (q : Q) : (graphHom action F hF q).right = q := rfl
@[simp] theorem graph_left (q : Q) : (graphHom action F hF q).left = F q := rfl

theorem graph_translate (q r : Q) (a : J) :
    (⟨a, q⟩ : J ⋊[action] Q) * graphHom action F hF (q⁻¹*r) =
      ⟨a * (F q)⁻¹ * F r, r⟩ := by
  have hc : action q (F (q⁻¹*r)) = (F q)⁻¹ * F r := by
    have h := hF q (q⁻¹*r)
    simp only [mul_inv_cancel_left] at h
    rw [h]
    simp
  apply SemidirectProduct.ext
  · change a * action q (F (q⁻¹*r)) = a * (F q)⁻¹ * F r
    rw [hc, mul_assoc]
  · exact mul_inv_cancel_left q r

theorem graph_coset_iff (U : Subgroup Q) (q r : Q) (a b : J) :
    (⟨a, q⟩ : J ⋊[action] Q)⁻¹ * ⟨b, r⟩ ∈ U.map (graphHom action F hF) ↔
      q⁻¹*r ∈ U ∧ b = a * (F q)⁻¹ * F r := by
  constructor
  · rintro ⟨u, hu, he⟩
    have hr : u = q⁻¹*r := by
      have h := congrArg SemidirectProduct.right he
      simpa using h
    subst u
    have hm := congrArg (fun x => (⟨a, q⟩ : J ⋊[action] Q)*x) he
    rw [graph_translate action F hF] at hm
    simp only [mul_inv_cancel_left] at hm
    exact ⟨hu, (congrArg SemidirectProduct.left hm).symm⟩
  · rintro ⟨hu, hb⟩
    refine ⟨q⁻¹*r, hu, ?_⟩
    apply mul_left_cancel (a := (⟨a, q⟩ : J ⋊[action] Q))
    rw [graph_translate action F hF, mul_inv_cancel_left, hb]

section TupleOracle
variable {I : Type*} [Nonempty I] {N O : I → Type*} [∀ i, Group (N i)]

/-- Public tuple oracle: only original component access and evaluation occur. -/
def tupleOracle (evaluation : J →* ∀ i, N i) (oracle : ∀ i, Q → N i → O i)
    (x : J ⋊[action] Q) : ∀ i, O i :=
  fun i => oracle i x.right (evaluation x.left i)

theorem tuple_relation (U : Subgroup Q)
    (evaluation : J →* ∀ i, N i) (injective : Function.Injective evaluation)
    (oracle : ∀ i, Q → N i → O i) (potential : Q → ∀ i, N i)
    (constant : ∀ i, N i)
    (normalize : ∀ q, potential q = constant * evaluation (F q))
    (hides : ∀ i q r x y, oracle i q x = oracle i r y ↔
      q⁻¹*r ∈ U ∧ y = x * (potential q i)⁻¹ * potential r i)
    (q r : Q) (a b : J) :
    tupleOracle action evaluation oracle ⟨a, q⟩ =
      tupleOracle action evaluation oracle ⟨b, r⟩ ↔
      q⁻¹*r ∈ U ∧ b = a * (F q)⁻¹ * F r := by
  have increment : evaluation a * (potential q)⁻¹ * potential r =
      evaluation (a * (F q)⁻¹ * F r) := by
    rw [normalize q, normalize r]
    simp only [map_mul, map_inv]
    group
  constructor
  · intro he
    have point (i : I) := (hides i q r (evaluation a i) (evaluation b i)).mp (congrFun he i)
    refine ⟨(point (Classical.choice inferInstance)).1, ?_⟩
    apply injective
    calc
      evaluation b = evaluation a * (potential q)⁻¹ * potential r := by
        funext i
        exact (point i).2
      _ = _ := increment
  · rintro ⟨hu, hb⟩
    apply funext
    intro i
    apply (hides i q r (evaluation a i) (evaluation b i)).mpr
    refine ⟨hu, ?_⟩
    have he : evaluation b = evaluation a * (potential q)⁻¹ * potential r := by
      rw [hb, increment]
    exact congrFun he i

/-- Exact ordinary HSP oracle reduction, not only equality of state marginals. -/
theorem tuple_hides_graph (U : Subgroup Q)
    (evaluation : J →* ∀ i, N i) (injective : Function.Injective evaluation)
    (oracle : ∀ i, Q → N i → O i) (potential : Q → ∀ i, N i)
    (constant : ∀ i, N i)
    (normalize : ∀ q, potential q = constant * evaluation (F q))
    (hides : ∀ i q r x y, oracle i q x = oracle i r y ↔
      q⁻¹*r ∈ U ∧ y = x * (potential q i)⁻¹ * potential r i)
    (x y : J ⋊[action] Q) :
    tupleOracle action evaluation oracle x = tupleOracle action evaluation oracle y ↔
      x⁻¹*y ∈ U.map (graphHom action F hF) := by
  cases x with | mk a q =>
    cases y with | mk b r =>
      exact (tuple_relation action F U evaluation injective oracle potential constant normalize hides q r a b).trans
        (graph_coset_iff action F hF U q r a b).symm

end TupleOracle

end
end QSearch.JetOracleHomogenization

/-- info: 'QSearch.JetOracleHomogenization.graph_coset_iff' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.JetOracleHomogenization.graph_coset_iff

/-- info: 'QSearch.JetOracleHomogenization.tuple_hides_graph' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms QSearch.JetOracleHomogenization.tuple_hides_graph
