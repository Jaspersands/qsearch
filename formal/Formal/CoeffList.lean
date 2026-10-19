import Formal.CycleIndicator

/-!
# A computable mirror of `exterior_characters`, proved equal to `stdDet`

Mathlib's `Polynomial ℤ` is not computable, so it cannot be compared with the
Python output by `decide` or `#eval` directly. Instead, polynomials are
represented here as coefficient lists (lowest degree first), and
`extCharsList L` computes the coefficients of `∏ (1 - (-z)^ℓᵢ) / (1 + z)` by
list arithmetic. `ofCoeffList_extCharsList` proves that this list is exactly
the coefficient list of the polynomial `stdDet L` from `Formal.CycleIndicator`,
so a `decide` check of `extCharsList` against Python values is a check of the
polynomial the theorems are about.
-/

open Polynomial

namespace QSearch

/-- Coefficient-wise sum of two coefficient lists (the shorter is padded by zeros). -/
def listAdd : List ℤ → List ℤ → List ℤ
  | [], b => b
  | a :: as, [] => a :: as
  | a :: as, b :: bs => (a + b) :: listAdd as bs

/-- Product of two coefficient lists. -/
def listMul : List ℤ → List ℤ → List ℤ
  | [], _ => []
  | a :: as, b => listAdd (b.map (a * ·)) (0 :: listMul as b)

/-- Coefficients of `∑_{i<ℓ} (-z)^i`. -/
def geomList : ℕ → List ℤ
  | 0 => []
  | ℓ + 1 => 1 :: (geomList ℓ).map Neg.neg

/-- Coefficients of `1 - (-z)^ℓ`. -/
def factorList (ℓ : ℕ) : List ℤ :=
  listAdd [1] (List.replicate ℓ 0 ++ [-(-1) ^ ℓ])

/-- Coefficients of `∏ (1 - (-z)^ℓᵢ)` (the Python `numerator`). -/
def permDetList : List ℕ → List ℤ
  | [] => [1]
  | ℓ :: rest => listMul (factorList ℓ) (permDetList rest)

/-- Coefficients of `∏ (1 - (-z)^ℓᵢ) / (1 + z)` (the Python `chars`). -/
def extCharsList : List ℕ → List ℤ
  | [] => []
  | ℓ :: rest => listMul (geomList ℓ) (permDetList rest)

/-- `∑ⱼ (-1)^j cⱼ` of a coefficient list. -/
def altSum : List ℤ → ℤ
  | [] => 0
  | c :: cs => c - altSum cs

noncomputable section

/-- The polynomial with the given coefficient list. -/
def ofCoeffList : List ℤ → ℤ[X]
  | [] => 0
  | c :: cs => C c + X * ofCoeffList cs

end

@[simp] lemma ofCoeffList_nil : ofCoeffList [] = 0 := rfl

@[simp] lemma ofCoeffList_cons (c : ℤ) (cs : List ℤ) :
    ofCoeffList (c :: cs) = C c + X * ofCoeffList cs := rfl

lemma ofCoeffList_listAdd (a b : List ℤ) :
    ofCoeffList (listAdd a b) = ofCoeffList a + ofCoeffList b := by
  induction a generalizing b with
  | nil => simp [listAdd]
  | cons x as ih =>
    cases b with
    | nil => simp [listAdd]
    | cons y bs => simp only [listAdd, ofCoeffList_cons, ih, C_add]; ring

lemma ofCoeffList_map_mul (x : ℤ) (b : List ℤ) :
    ofCoeffList (b.map (x * ·)) = C x * ofCoeffList b := by
  induction b with
  | nil => simp
  | cons y bs ih => simp only [List.map_cons, ofCoeffList_cons, ih, C_mul]; ring

lemma ofCoeffList_map_neg (b : List ℤ) :
    ofCoeffList (b.map Neg.neg) = -ofCoeffList b := by
  induction b with
  | nil => simp
  | cons y bs ih => simp only [List.map_cons, ofCoeffList_cons, ih, C_neg]; ring

lemma ofCoeffList_listMul (a b : List ℤ) :
    ofCoeffList (listMul a b) = ofCoeffList a * ofCoeffList b := by
  induction a with
  | nil => simp [listMul]
  | cons x as ih =>
    simp only [listMul, ofCoeffList_listAdd, ofCoeffList_map_mul, ofCoeffList_cons, ih,
      C_0]
    ring

lemma ofCoeffList_geomList (ℓ : ℕ) : ofCoeffList (geomList ℓ) = geomFactor ℓ := by
  induction ℓ with
  | zero => simp [geomList, geomFactor]
  | succ ℓ ih =>
    rw [geomList, ofCoeffList_cons, ofCoeffList_map_neg, ih, geomFactor, geomFactor,
      Finset.sum_range_succ']
    simp only [C_1, pow_zero, pow_succ, ← Finset.sum_mul]
    ring

lemma ofCoeffList_replicate_append (ℓ : ℕ) (c : ℤ) :
    ofCoeffList (List.replicate ℓ 0 ++ [c]) = C c * X ^ ℓ := by
  induction ℓ with
  | zero => simp
  | succ ℓ ih =>
    rw [List.replicate_succ, List.cons_append, ofCoeffList_cons, ih, C_0, pow_succ]
    ring

lemma ofCoeffList_factorList (ℓ : ℕ) : ofCoeffList (factorList ℓ) = 1 - (-X) ^ ℓ := by
  rw [factorList, ofCoeffList_listAdd, ofCoeffList_replicate_append, neg_pow (X : ℤ[X])]
  simp only [ofCoeffList_cons, ofCoeffList_nil, mul_zero, add_zero, map_one, map_neg, map_pow]
  ring

lemma ofCoeffList_permDetList (L : List ℕ) : ofCoeffList (permDetList L) = permDet L := by
  induction L with
  | nil => simp [permDetList]
  | cons ℓ rest ih => rw [permDetList, ofCoeffList_listMul, ofCoeffList_factorList, ih,
      permDet_cons]

/-- **Bridge.** The computable list is the coefficient list of `stdDet L`. -/
theorem ofCoeffList_extCharsList (L : List ℕ) : ofCoeffList (extCharsList L) = stdDet L := by
  cases L with
  | nil => simp [extCharsList, stdDet]
  | cons ℓ rest => rw [extCharsList, ofCoeffList_listMul, ofCoeffList_geomList,
      ofCoeffList_permDetList, stdDet_cons]

lemma coeff_ofCoeffList (l : List ℤ) (j : ℕ) : (ofCoeffList l).coeff j = l.getD j 0 := by
  induction l generalizing j with
  | nil => simp
  | cons c cs ih =>
    cases j with
    | zero => simp
    | succ j =>
      rw [ofCoeffList_cons, coeff_add, coeff_C, coeff_X_mul, ih]
      simp

/-- The `j`-th entry of `extCharsList L` is the `j`-th coefficient of `stdDet L`. -/
theorem stdDet_coeff_eq (L : List ℕ) (j : ℕ) : (stdDet L).coeff j = (extCharsList L).getD j 0 := by
  rw [← ofCoeffList_extCharsList, coeff_ofCoeffList]

lemma altSum_eq_eval (l : List ℤ) : altSum l = (ofCoeffList l).eval (-1) := by
  induction l with
  | nil => simp [altSum]
  | cons c cs ih => simp [altSum, ih]; ring

/-- The computable alternating sum is the cycle indicator, for every cycle list. -/
theorem altSum_extCharsList (L : List ℕ) :
    altSum (extCharsList L) = if L.length = 1 then (L.sum : ℤ) else 0 := by
  rw [altSum_eq_eval, ofCoeffList_extCharsList, stdDet_eval_neg_one]

end QSearch
