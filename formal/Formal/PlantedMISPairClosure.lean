import Mathlib.Data.Set.Basic

/-!
# Two-seed recovery of a protected planted independent set

Only the set-theoretic recovery implication is formalized. This does not
verify Python, graph generation, runtime, optimality, or the interpretation
of an external paper's graph construction.
-/

namespace QSearch.PlantedMISPairClosure

variable {V B : Type*}

def closedAnti (adj : V → V → Prop) (a b : V) : Set V :=
  {v | ¬ adj v a ∧ ¬ adj v b}

theorem recover_from_separating_pair
    (adj : V → V → Prop) (S : Set V) (a b : V)
    (ha : a ∈ S) (hb : b ∈ S)
    (hind : ∀ u ∈ S, ∀ v ∈ S, ¬ adj u v)
    (hsep : ∀ v, v ∉ S → adj v a ∨ adj v b) :
    closedAnti adj a b = S := by
  classical
  apply Set.ext
  intro v
  change (¬ adj v a ∧ ¬ adj v b) ↔ v ∈ S
  constructor
  · intro hv
    by_contra hnot
    rcases hsep v hnot with h | h
    · exact hv.1 h
    · exact hv.2 h
  · intro hv
    exact ⟨hind v hv a ha, hind v hv b hb⟩

theorem recover_from_protected_blocks
    (adj : V → V → Prop) (S : Set V) (block : V → B) (a b : V)
    (ha : a ∈ S) (hb : b ∈ S) (hab : block a ≠ block b)
    (hind : ∀ u ∈ S, ∀ v ∈ S, ¬ adj u v)
    (hprotected : ∀ v, v ∉ S → ∀ s ∈ S, block v ≠ block s → adj v s) :
    closedAnti adj a b = S := by
  classical
  apply recover_from_separating_pair adj S a b ha hb hind
  intro v hnot
  by_cases hv : block v = block a
  · right
    apply hprotected v hnot b hb
    intro heq
    exact hab (hv.symm.trans heq)
  · left
    exact hprotected v hnot a ha hv

#print axioms recover_from_separating_pair
#print axioms recover_from_protected_blocks

end QSearch.PlantedMISPairClosure
