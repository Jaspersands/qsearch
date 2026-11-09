# Rees HSP paper: computable SDE solvers in Lean (`ReesSdeSolver`)

5 November 2026. AI-only overnight pass (Claude Code). Machine-checked in Lean; AI-run,
pending human review. No `.tex`, registry JSON, claim gate, `AGENT_HANDOFF.md`,
`STATE.md`, existing Lean file, `formal/Formal.lean` or `formal/Formal/Audit.lean` was
edited. The claim gates `formal_compiler_checked` and `general_sde_implemented` stay
false. No git, no network.

New file: `formal/Formal/ReesSdeSolver.lean` (one module, namespace
`QSearch.ReesSdeSolver`). It imports the built modules `Formal.ReesSdeTriangular`,
`Formal.ReesSdeQuadratic`, `Formal.ReesSdeWitness` and Mathlib only.

## 1. Summary

Three solvers for the diagonal equation `∑_i s_i^d λ_i = 0` are now ordinary Lean
definitions that the code generator compiles and that run under `#eval`. Each comes with
a theorem that its output is a solution.

1. **The triangular two-level solver** (`prop:triangular-sde`) runs over any field, with the
   contraction given as input. At `κ = 2` it is complete over any finite field of odd
   characteristic, given a normalised contraction for some quadratic non-residue `g`.
   Over `ZMod p`, for every odd prime `p`, it is complete and unconditional: the
   contraction is computed by search. The arity is `(a+1)(a+2)/2`.
2. **The linear solver** (`thm:power-sde`(i), `κ = 1`) works over any finite field with
   arity `a + 1`.
3. **The Chevalley–Warning bound.** Exhaustive search over `K^M` returns a nonzero solution
   from any `κ a + 1` columns (`κ = d` over any finite field; `κ = gcd(d, p-1)` over
   `ZMod p`). Existence comes from `ReesSdeWitness`.

There are no `sorry`s and no new axioms. Every `#print axioms` lists exactly
`[propext, Classical.choice, Quot.sound]`; Section 5 explains why `Classical.choice`
appears for computable definitions. Running time is **not** formalized.

## 2. Exact Lean statements

Everything is in namespace `QSearch.ReesSdeSolver` (section variable
`{K : Type*} [Field K] [DecidableEq K]`). `Tab m α` is an array with a proof that its
length is `m`, read by `Tab.get : Tab m α → Fin m → α`. Solvers return a `Tab` and not a
function `Fin m → K`, because the compiler eta-expands function-valued definitions and
would recompute the whole solver at each index read (an exponential slowdown, observed
and measured). A `Tab` is computed once.

```lean
structure Tab (m : ℕ) (α : Type*) where
  arr : Array α
  size_eq : arr.size = m
```

### 2.1 Gaussian elimination

`kernelVec n m w` and `solveVec n m w t` eliminate the last coordinate and recurse on `n`.

```lean
theorem kernelVec_spec : ∀ (n m : ℕ) (w : Fin m → Fin n → K), n < m →
    (kernelVec n m w).get ≠ 0 ∧ ∑ j, (kernelVec n m w).get j • w j = 0 := ...

theorem solveVec_some : ∀ (n m : ℕ) (w : Fin m → Fin n → K) (t : Fin n → K) (c : Tab m K),
    solveVec n m w t = some c → ∑ j, c.get j • w j = t := ...

theorem solveVec_none : ∀ (n m : ℕ) (w : Fin m → Fin n → K) (t : Fin n → K),
    solveVec n m w t = none → ∀ c : Fin m → K, ∑ j, c j • w j ≠ t := ...
```

### 2.2 Triangular solver (any field, contraction as input)

`A, B : K → K` stand for the paper's maps `ζ ↦ α_{cos ζ}` and `δ ↦ β_{cos δ}`. `D` stands
for `P ∪ {0}`. Section variables: `(A B : K → K) {a M : ℕ} (col : Fin M → Fin a → K)`.

```lean
def triSolve : Tab M K :=
  if hM : (a + 1) * (a + 2) / 2 ≤ M then
    triRound A B col (by rwa [roundStart_top]) 0 (Nat.zero_le a) Fin.elim0 (fun _ => tab 0)
  else tab 0

theorem triSolve_spec {D : Set K} (h0 : (0 : K) ∈ D)
    (hAB : ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (A ζ + B δ) ∈ D) (h1 : A 1 + B 1 ≠ 0)
    (hM : (a + 1) * (a + 2) / 2 ≤ M) :
    (triSolve A B col).get ≠ 0 ∧ (∀ i, (triSolve A B col).get i ∈ D) ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (triSolve A B col).get i = 0) ∧
      ∑ i, (triSolve A B col).get i • col i = 0 := ...
```

`triRound` (round `k`) is defined by well-founded recursion on `a - k`. Its invariant is
`triRound_spec`: `v` is independent (`IndepVec v := ∀ γ, ∑ γ_l • v_l = 0 → γ = 0`), the
realizer `R` has weights in `D`, is supported below `roundStart a k` and has value
`∑ γ_l v_l`. Here `roundStart a k = ∑_{j<k} (a - j + 1)`, and `roundStart a (a+1) =
(a+1)(a+2)/2` (`roundStart_top`). A bridge lemma turns a coset index into the hypothesis
`hAB`:

```lean
theorem contraction_of_index {κ : ℕ} [NeZero κ] {g : K} (ind : K → ZMod κ)
    (hind : ∀ y : K, y ≠ 0 → ∃ w : K, y = g ^ (ind y).val * w ^ κ) (α β : ZMod κ → K)
    (hC : ∀ i j : ZMod κ, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ κ) :
    ∀ ζ δ : K, ζ ≠ 0 → δ ≠ 0 → ζ * δ * (α (ind ζ) + β (ind δ)) ∈ {y | ∃ w : K, y = w ^ κ} := ...
```

### 2.3 `κ = 2`, any finite field of odd characteristic

Section variable `[Fintype K]` (in addition to `[Field K] [DecidableEq K]`).

```lean
def cos2 (q : ℕ) (y : K) : ZMod 2 := if y ^ (q / 2) = 1 then 0 else 1

def sqrtSearch (elems : List K) (y : K) : K :=
  match elems.find? (fun w => w * w == y) with
  | some w => w
  | none => 0

def quadSolve (q : ℕ) (elems : List K) (α β : ZMod 2 → K) {a M : ℕ}
    (col : Fin M → Fin a → K) : Tab M K :=
  let x := (triSolve (fun ζ => α (cos2 q ζ)) (fun δ => β (cos2 q δ)) col).get
  tab fun i => sqrtSearch elems (x i)

theorem quadSolve_spec {q : ℕ} (hq : Fintype.card K = q) (hchar : ringChar K ≠ 2)
    {elems : List K} (hel : ∀ x, x ∈ elems) {g : K} (hg : ¬IsSquare g) (α β : ZMod 2 → K)
    (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod 2, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ 2)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → K) :
    (quadSolve q elems α β col).get ≠ 0 ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (quadSolve q elems α β col).get i = 0) ∧
      ∑ i, (quadSolve q elems α β col).get i ^ 2 • col i = 0 := ...

def bezoutExp (d N : ℕ) : ℕ :=
  ((d / Nat.gcd d N : ℕ) : ZMod (N / Nat.gcd d N))⁻¹.val + N / Nat.gcd d N

theorem pow_bezoutExp [Fintype K] {d : ℕ} (hd : 0 < d) (x : K) :
    (x ^ bezoutExp d (Fintype.card K - 1)) ^ d = x ^ Nat.gcd d (Fintype.card K - 1) := ...

def quadSolveExp (q d : ℕ) (elems : List K) (α β : ZMod 2 → K) {a M : ℕ}
    (col : Fin M → Fin a → K) : Tab M K :=
  let s := (quadSolve q elems α β col).get
  let t := bezoutExp d (q - 1)
  tab fun i => s i ^ t

theorem quadSolveExp_spec {q d : ℕ} (hq : Fintype.card K = q) (hd : 0 < d)
    (hκ : Nat.gcd d (q - 1) = 2) (hchar : ringChar K ≠ 2) {elems : List K}
    (hel : ∀ x, x ∈ elems) {g : K} (hg : ¬IsSquare g) (α β : ZMod 2 → K)
    (hα0 : α 0 = 1) (hβ0 : β 0 = 0)
    (hC : ∀ i j : ZMod 2, ∃ w : K, (α j + β i) * g ^ (i + j).val = w ^ 2)
    {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → K) :
    (quadSolveExp q d elems α β col).get ≠ 0 ∧
      ∑ i, (quadSolveExp q d elems α β col).get i ^ d • col i = 0 := ...
```

### 2.4 `κ = 2` over `ZMod p`, unconditional

```lean
def findMu (p : ℕ) : ZMod p :=
  ((zmodElems p).find? (fun y => y != 0 && y ^ (p / 2) == 1 && 1 + y != 0 &&
    (1 + y) ^ (p / 2) != 1)).getD 0

theorem findMu_spec {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) :
    findMu p ≠ 0 ∧ IsSquare (findMu p) ∧ ¬IsSquare (1 + findMu p) := ...

theorem findMu_contraction {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) :
    ∀ i j : ZMod 2, ∃ w : ZMod p,
      (![1, 0] j + ![0, findMu p] i) * (1 + findMu p) ^ (i + j).val = w ^ 2 := ...

def quadSolveZMod (p : ℕ) [Fact p.Prime] {a M : ℕ} (col : Fin M → Fin a → ZMod p) :
    Tab M (ZMod p) :=
  quadSolve p (zmodElems p) ![1, 0] ![0, findMu p] col

theorem quadSolveZMod_spec {p : ℕ} [Fact p.Prime] (hp2 : p ≠ 2) {a M : ℕ}
    (hM : (a + 1) * (a + 2) / 2 ≤ M) (col : Fin M → Fin a → ZMod p) :
    (quadSolveZMod p col).get ≠ 0 ∧
      (∀ i : Fin M, (a + 1) * (a + 2) / 2 ≤ i.val → (quadSolveZMod p col).get i = 0) ∧
      ∑ i, (quadSolveZMod p col).get i ^ 2 • col i = 0 := ...

def quadSolveZModExp (p d : ℕ) [Fact p.Prime] {a M : ℕ} (col : Fin M → Fin a → ZMod p) :
    Tab M (ZMod p) :=
  quadSolveExp p d (zmodElems p) ![1, 0] ![0, findMu p] col

theorem quadSolveZModExp_spec {p : ℕ} [Fact p.Prime] {d : ℕ} (hd : 0 < d)
    (hκ : Nat.gcd d (p - 1) = 2) {a M : ℕ} (hM : (a + 1) * (a + 2) / 2 ≤ M)
    (col : Fin M → Fin a → ZMod p) :
    (quadSolveZModExp p d col).get ≠ 0 ∧
      ∑ i, (quadSolveZModExp p d col).get i ^ d • col i = 0 := ...
```

### 2.5 `κ = 1` (linear)

```lean
def linSolve (q d : ℕ) {a M : ℕ} (col : Fin M → Fin a → K) : Tab M K :=
  let rows := tabMat col
  let c := (kernelVec a M (fun j => (rows.get j).get)).get
  let t := bezoutExp d (q - 1)
  tab fun i => c i ^ t

theorem linSolve_spec [Fintype K] {q d a M : ℕ} (hq : Fintype.card K = q) (hd : 0 < d)
    (hκ : Nat.gcd d (q - 1) = 1) (hM : a + 1 ≤ M) (col : Fin M → Fin a → K) :
    (linSolve q d col).get ≠ 0 ∧ ∑ i, (linSolve q d col).get i ^ d • col i = 0 := ...

theorem linSolve_zmod_spec {p : ℕ} [Fact p.Prime] {d a M : ℕ} (hd : 0 < d)
    (hκ : Nat.gcd d (p - 1) = 1) (hM : a + 1 ≤ M) (col : Fin M → Fin a → ZMod p) :
    (linSolve p d col).get ≠ 0 ∧ ∑ i, (linSolve p d col).get i ^ d • col i = 0 := ...
```

### 2.6 Exhaustive search at the Chevalley–Warning arity

`allVecs elems M` lists every `Fin M → K` with entries from `elems` (`mem_allVecs`).

```lean
def cwSearch (elems : List K) (d : ℕ) {a M : ℕ} (col : Fin M → Fin a → K) : Tab M K :=
  tab (((allVecs elems M).find?
    (fun s => decide (s ≠ 0) && decide (∑ i, s i ^ d • col i = 0))).getD 0)

theorem cwSearch_spec {elems : List K} (hel : ∀ x, x ∈ elems) {d a M : ℕ}
    (col : Fin M → Fin a → K) (hex : ∃ s : Fin M → K, s ≠ 0 ∧ ∑ i, s i ^ d • col i = 0) :
    (cwSearch elems d col).get ≠ 0 ∧ ∑ i, (cwSearch elems d col).get i ^ d • col i = 0 := ...

theorem cwSearch_witness [Fintype K] {elems : List K} (hel : ∀ x, x ∈ elems) {κ a M : ℕ}
    (hκ : 0 < κ) (hM : κ * a < M) (col : Fin M → Fin a → K) :
    (cwSearch elems κ col).get ≠ 0 ∧ ∑ i, (cwSearch elems κ col).get i ^ κ • col i = 0 := ...

theorem cwSearch_zmod_gcd {p : ℕ} [Fact p.Prime] {d a M : ℕ} (hd : 0 < d)
    (hM : Nat.gcd d (p - 1) * a < M) (col : Fin M → Fin a → ZMod p) :
    (cwSearch (zmodElems p) d col).get ≠ 0 ∧
      ∑ i, (cwSearch (zmodElems p) d col).get i ^ d • col i = 0 := ...
```

## 3. Match with the paper, and what is not covered

**`prop:triangular-sde`.**
- *Rounds.* `triSolve` follows the paper's rounds. Round `k` takes the next `a - k + 1`
  fresh columns. It finds a dependence modulo `U_k` with one `kernelVec` call on the
  fresh columns together with `v_1..v_k`, normalises the first nonzero fresh entry to `1`
  (the paper's "for definiteness the first"), forms `v_{k+1} = ∑ β(δ_i) δ_i λ_i`, and
  tests `v_{k+1} ∈ U_k` with one `solveVec` call.
- *Back substitution.* It is a closure `R`; Lean has no explicit `τ` loop. The weights
  are the paper's `ζ δ_i (α_{cos ζ} + β_{cos δ_i})`.
- *Conclusion.* `triSolve_spec` is the paper's conclusion: a nonzero `x ∈ (P∪{0})^M`
  with `∑ x_i λ_i = 0`. It adds the support bound (`x_i = 0` for `i ≥ (a+1)(a+2)/2`) and
  holds over any field and any set `D`.
- *Coset condition.* The paper's `α_j + β_i ∈ g^{-(i+j)}P ∪ {0}` appears as
  `∃ w, (α_j + β_i) g^{(i+j).val} = w^κ`.
- *At `κ = 2`.* `quadSolve_spec` takes `g` to be **any** quadratic non-residue, matching
  the paper's "any quadratic non-residue can serve as `g`". The algorithm never uses `g`;
  it only needs one to exist.
- *Lifted limitation.* `ReesSdeTriangular`'s restriction to a generator `g` of
  `F_p^×` is lifted here at `κ = 2`.
- *Roots and Bezout step.* Square roots come from `sqrtSearch`, and the Bezout step is
  `bezoutExp` / `pow_bezoutExp`, matching Lemma `lem:app-s2-gcd`(b).
- *`ZMod p`.* `quadSolveZMod_spec` needs only `p` odd prime and `M ≥ (a+1)(a+2)/2`. The
  contraction is `α = (1,0)`, `β = (0,μ)` with `μ` the first `y` with `y` and `1+y`
  nonzero, `y` a square and `1+y` a non-square (`findMu`), which is exactly what
  `findMu_spec` proves. (`ReesSdeQuadratic` uses `μ = n_0 - 1` with `n_0` the least
  non-residue. `findMu` returns that same value; this is not proved and not needed.)

**`thm:power-sde`(i).** `linSolve_spec` matches it: `a + 1` columns, `gcd(d, q-1) = 1`,
over any finite field (`q = |K|` as a hypothesis), by one elimination and `s_i = c_i^t`.
That `s ↦ s^d` is a bijection appears only through `(c^t)^d = c` (`pow_bezoutExp`).

**Chevalley–Warning at `κ a + 1`.** `cwSearch_witness` (exponent `κ`, any finite field)
and `cwSearch_zmod_gcd` (exponent `d`, `gcd(d,p-1) a + 1` columns over `ZMod p`) are
complete searches: when a solution exists (Chevalley–Warning), they return one
(`cwSearch_spec` needs the existence hypothesis `hex`). They are **exponential**
(`|K|^M` candidates).

**Not covered (all outside the Lean boundary):**
- *Running time.* No cost statement is proved. In particular the paper's `O(a+1)`
  eliminations and `O((a+1)^2)` power evaluations are not proved. They hold by
  inspection of the code, which is not a proof.
- *Root extraction.* Square roots are found by an `O(|K|)` list search, not by the
  paper's Las Vegas `κ`-th root extraction in `poly(κ, log p)`. `quadSolveZMod` is
  therefore polynomial in `p`, not in `log p`.
- *`κ ≥ 3`.* There is no computable coset index and no root extraction. Only the abstract
  `triSolve_spec` (any `A, B, D`) and `contraction_of_index` apply, with the index map and
  the contraction as inputs. The contraction for `κ ≥ 3` (Prop. `prop:decoupled-sde`, the
  `E_2(κ)` condition) is not constructed.
- *Field size as an input.* `quadSolve`, `quadSolveExp` and `linSolve` take the field size
  `q` and (for `quadSolve`) a list of all field elements as data. Their correctness
  theorems require `Fintype.card K = q` and `∀ x, x ∈ elems`. Over `ZMod p` both are
  discharged (`ZMod.card`, `mem_zmodElems`).
- *Schedules 2 and 3.* Schedule 2's arity `(a+1)((κ-1)a+1)`, the Schedule 3 samplers and
  `thm:power-sde`(ii, iii) are not touched.
- *Label rank.* The label rank `a_d ≤ g_d` is not addressed. The solvers take any `a`; the
  receiver still uses `g_{d+1}` (`ReesSdePolicy`).
- *Receiver integration.* The receiver policies in `ReesSdePolicy` are still chosen by
  choice. Replacing them by `quadSolveZMod` / `cwSearch` is not done.
- *Claim gates.* `formal_compiler_checked` and `general_sde_implemented` stay false.

**Non-vacuity checks in the file** (`#guard_msgs` on `#eval`; these are tests, not
proofs):
- `findMu 7 = 2`.
- `quadSolveZMod 7` on 6 columns in `F_7^2` gives `#[3,3,3,1,1,0]` with residual `[0,0]`.
- `quadSolveZMod 11` on 10 columns in `F_11^3` gives `#[4,4,4,1,0,0,0,0,1,0]` with
  residual 0.
- `quadSolveZModExp 11 4` (`gcd(4,10)=2`) gives residual 0.
- `linSolve 11 3` on 4 columns gives `#[10,10,10,1]` with residual 0.
- `cwSearch (zmodElems 7) 2` on 5 columns gives `#[0,1,2,1,3]`.
- `quadSolveZMod 1009` on 45 pseudo-random columns in `F_1009^8` gives residual 0 with 33
  nonzero entries.

Scratch runs (not in the file):
- `a = 12` (91 columns) gave residual 0 with 54 nonzero entries.
- `a = 20` (231 columns) gave residual 0 with 171 nonzero entries.
- Each run took about 1 s of evaluation.

The hypotheses of the main theorems are satisfiable, as these runs instantiate them
(e.g. `quadSolveZMod_spec` at `p = 7, 11, 1009`).

## 4. Build

The other agent's `lake build Formal.BCHClassSevenSubgroups` held the lake lock, so only
the single file was checked, without `lake build`:

```
cd formal && PATH=$HOME/.elan/bin:$PATH nice -n 10 lake env /usr/bin/time -l lean Formal/ReesSdeSolver.lean
```

The result was exit 0 with no output (no error, warning, `sorry` or failed guard):
- 19.13 s wall, 7.11 s user;
- max RSS 2.01 GB, under a load average of 200–400 from other agents;
- an earlier identical run took 17.39 s wall, 7.46 s user and 2.09 GB.

The file imports only built modules (`Formal.ReesSdeTriangular`,
`Formal.ReesSdeQuadratic`, `Formal.ReesSdeWitness`) and Mathlib, so
`lake build Formal.ReesSdeSolver` should also work once the lock is free. That was not
run. No `--wfail` or clean-copy build was run. The file has 1236 lines and 33
`#guard_msgs` commands: 23 `#print axioms` and 10 `#eval`.

## 5. Axioms

`#print axioms` for each of these 22 names is guarded in the file and prints
`[propext, Classical.choice, Quot.sound]`:

- definitions: `kernelVec`, `solveVec`, `triSolve`, `quadSolveZMod`, `linSolve`,
  `cwSearch`;
- theorems: `kernelVec_spec`, `solveVec_some`, `solveVec_none`, `triRound_spec`,
  `triSolve_spec`, `pow_bezoutExp`, `linSolve_spec`, `linSolve_zmod_spec`,
  `quadSolve_spec`, `quadSolveExp_spec`, `findMu_spec`, `quadSolveZMod_spec`,
  `quadSolveZModExp_spec`, `cwSearch_spec`, `cwSearch_witness`, `cwSearch_zmod_gcd`.

There is no `sorry`, no `axiom`, no `noncomputable` declaration and no `implemented_by`
or `extern`.

**Why `Classical.choice` appears for computable definitions.** `#print axioms` follows
proof terms inside the definitions. Every `∑` over `Fin n` goes through Mathlib's
`Fin.fintype`, whose proof fields use `Classical.choice`. The file's one-line probe
`finSumProbe n := ∑ j : Fin n, j.val` prints the same list.

The evidence that the data is computable is that Lean's code generator compiled every
definition (none is `noncomputable`) and the `#eval` runs above executed them. No
`Classical.choice` is evaluated at run time. The axiom list cannot tell this apart from a
noncomputable definition. Compilation can.

## 6. Proposed text (not applied)

### 6.1 Lean paragraph (`main.tex`, the paragraph beginning "For the SDE step")

Replace the first sentence, "For the SDE step, Lean checks existence and algebra but no
algorithm.", with:

```latex
For the SDE step, Lean checks existence and algebra, and the solvers described at the end of this paragraph.
```

In the same paragraph, replace "Lean takes $g$ to generate $\Fp^\times$; the reduction from an arbitrary coset generator is not formalized." with:

```latex
\texttt{ReesSdeTriangular} takes $g$ to generate $\Fp^\times$, and the reduction from an arbitrary coset generator is not formalized there; at $\kappa = 2$, \texttt{ReesSdeSolver} accepts any quadratic non-residue as $g$.
```

Append at the end of that paragraph:

```latex
The module \texttt{ReesSdeSolver} (\file{research/audits/reviews/2026-11-05-rees-lean-sde-solver.md}; machine-checked in Lean; AI-run, pending human review) gives algorithms that Lean compiles and runs, each with a proof that its output is a solution. Gaussian elimination returns a nonzero kernel vector of any $m>n$ vectors in $K^n$ and decides membership in their span. The triangular solver of Proposition~\ref{prop:triangular-sde} runs over any field, with the contraction given as the two maps $\zeta\mapsto\alpha_{\mathrm{cos}(\zeta)}$ and $\delta\mapsto\beta_{\mathrm{cos}(\delta)}$; from any $M\ge(a+1)(a+2)/2$ columns it returns a nonzero $x$, supported on the first $(a+1)(a+2)/2$ columns, with $\sum_ix_i\lambda_i=0$ and with entries in every set $D\ni0$ that contains all products $\zeta\delta(\alpha_{\mathrm{cos}(\zeta)}+\beta_{\mathrm{cos}(\delta)})$ with $\zeta,\delta\ne0$ (over $\Fp$, $D=P\cup\{0\}$). At $\kappa=2$, over any finite field of odd characteristic, with cosets tested by Euler's criterion and square roots found by search through all field elements, it returns a nonzero solution of $\sum_is_i^2\lambda_i=0$ for every normalised contraction with respect to any quadratic non-residue $g$. Over $\Fp$ the contraction $((1,0),(0,\mu))$ is itself found by search, so for every odd prime $p$ the solver needs no input but $p$, $d$ and the columns, and with the Bezout exponent it returns a nonzero solution of~\eqref{eq:sde-target} from any $(a+1)(a+2)/2$ columns at every $d$ with $\gcd(d,p-1)=2$. At $\kappa=1$, one elimination on any $a+1$ columns and the Bezout exponent give a nonzero solution over any finite field (Theorem~\ref{thm:power-sde}(i)). An exhaustive search returns a nonzero solution from any $\gcd(d,p-1)\,a+1$ columns over $\Fp$, by the Chevalley--Warning statement above. Running time is not formalized. By inspection of the code, not by proof, the root search costs $O(p)$ field operations per entry and the exhaustive search visits up to $p^M$ vectors, so neither is the polynomial-time procedure of the paper. The Las Vegas root extraction, coset indices and contractions for $\kappa\ge3$, the arities of Schedules~2 and~3, the use of the label rank $a_{d+1}$, and the replacement of the chosen policies of \texttt{ReesSdePolicy} by these solvers remain outside the boundary.
```

### 6.2 Abstract / introduction sentence (`main.tex` line 110)

In the sentence beginning "For the diagonal equation, Lean checks existence", insert before
its final period:

```latex
, and runs, with correctness proofs, the triangular solver with the contraction as input, a solver at $\kappa = 2$ over $\Fp$ that needs no contraction input (square roots found by search), the linear solver at $\kappa = 1$, and exhaustive search at the Chevalley--Warning arity
```

In the next sentence, replace "the SDE algorithms," with "polynomial-time SDE algorithms,".
The positive claims stay out of the list of what lies outside the boundary.

### 6.3 `tab:lean-modules` row (after `\texttt{ReesSdePolicy}`)

```latex
\texttt{ReesSdeSolver} & 22 & Computable solvers with correctness proofs: Gaussian elimination; the triangular solver of Proposition~\ref{prop:triangular-sde} with the contraction as input; at $\kappa=2$ over $\Fp$, $p$ odd, a nonzero solution from any $(a+1)(a+2)/2$ columns with no other input; at $\kappa=1$ from any $a+1$ columns; exhaustive search at $\gcd(d,p-1)\,a+1$ columns; running time not checked \\
```

Total row: add 22 to the current total. When this was checked (after the class-seven
integration) the paper said 471 module guards and 509 in all, so the row becomes
`\textbf{Total} & \textbf{493} & \\`. In the formalization paragraph, the module-guard
count 471 becomes 493, and "$509$ in all" becomes "$531$ in all". If the base has changed
again, add 22 to whatever it is. Write those sentences only after the guards below are added to `Audit.lean` and a
`lake build Formal.Audit` (or `lake build --wfail`) has succeeded. Proposed sentence for
that paragraph, once it has:

```latex
On 5 November 2026 an AI session added the module \texttt{ReesSdeSolver} (\file{research/audits/reviews/2026-11-05-rees-lean-sde-solver.md}); \texttt{lake env lean} on it succeeded with no error, warning or \texttt{sorry}, and its $22$ guards were added to \file{formal/Formal/Audit.lean} (machine-checked in Lean; AI-run, pending human review); no clean-copy build was run for it.
```

### 6.4 Lines for `formal/Formal.lean` and `formal/Formal/Audit.lean` (not applied)

`formal/Formal.lean`, after `import Formal.ReesSdePolicy`:

```lean
import Formal.ReesSdeSolver
```

`formal/Formal/Audit.lean`: add `import Formal.ReesSdeSolver` after
`import Formal.ReesSdePolicy`. Then add these 22 guards after the last
`QSearch.ReesSdePolicy` guard (`classSix_measured_terminal_source_cw`). The probe
`finSumProbe` stays in the module only.

```lean
/-- info: 'QSearch.ReesSdeSolver.kernelVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec

/-- info: 'QSearch.ReesSdeSolver.solveVec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec

/-- info: 'QSearch.ReesSdeSolver.triSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod

/-- info: 'QSearch.ReesSdeSolver.linSolve' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve

/-- info: 'QSearch.ReesSdeSolver.cwSearch' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch

/-- info: 'QSearch.ReesSdeSolver.kernelVec_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.kernelVec_spec

/-- info: 'QSearch.ReesSdeSolver.solveVec_some' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_some

/-- info: 'QSearch.ReesSdeSolver.solveVec_none' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.solveVec_none

/-- info: 'QSearch.ReesSdeSolver.triRound_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triRound_spec

/-- info: 'QSearch.ReesSdeSolver.triSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.triSolve_spec

/-- info: 'QSearch.ReesSdeSolver.pow_bezoutExp' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.pow_bezoutExp

/-- info: 'QSearch.ReesSdeSolver.linSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_spec

/-- info: 'QSearch.ReesSdeSolver.linSolve_zmod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.linSolve_zmod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolve_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolve_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveExp_spec

/-- info: 'QSearch.ReesSdeSolver.findMu_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.findMu_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveZMod_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZMod_spec

/-- info: 'QSearch.ReesSdeSolver.quadSolveZModExp_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.quadSolveZModExp_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_spec

/-- info: 'QSearch.ReesSdeSolver.cwSearch_witness' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_witness

/-- info: 'QSearch.ReesSdeSolver.cwSearch_zmod_gcd' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs (whitespace := lax) in
#print axioms QSearch.ReesSdeSolver.cwSearch_zmod_gcd
```

Proposed `formal/README.md` row (README not edited):

```
| `ReesSdeSolver` | Computable SDE solvers with correctness proofs: elimination, the triangular solver (contraction as input), the unconditional κ = 2 solver over ZMod p, the κ = 1 solver, exhaustive search at κa+1. Running time not formalized. Report: research/audits/reviews/2026-11-05-rees-lean-sde-solver.md |
```


## 7. Independent check (fresh general-purpose subagent, 5 November 2026)

**Verdict: PASS WITH FIXES.** The Lean file is sound, and all fixes were to the report's
text or its proposed LaTeX. No Lean change was needed.

The reviewer compiled the file once (`lake env lean`, exit 0, no output, about 26 s) and
checked the following:

- **No forbidden constructs.** There is no `sorry`, `axiom`, `noncomputable`,
  `implemented_by`/`extern`, `native_decide`, `unsafe`, `opaque`, `csimp` or `set_option`.
- **Axioms.** Every `#print axioms` guard gives `[propext, Classical.choice, Quot.sound]`.
- **`Classical.choice`.** The explanation in Section 5 was confirmed in a scratch file:
  `#print axioms Fin.fintype` lists `Classical.choice`, and the same sum over
  `List.finRange` depends on no axioms.
- **Statements.** The Lean statements match Section 2 word for word.
- **The algorithm.** `triSolve` is the stated algorithm, with no hidden search and no
  `Classical.choose`. The reviewer checked both branches of `triRound` by hand against
  the paper's proof.
- **No vacuity.** The fallback values (`tab 0`, `sqrtSearch` returning `0`, `cwSearch`
  returning `0`) cannot reach the theorems. The hypotheses are satisfiable, since
  `findMu_contraction`, `ZMod.card` and `mem_zmodElems` discharge them over `ZMod p`.
- **Extra tests**, all passed:
  - `findMu` is 1, 2, 1, 1 at p = 3, 7, 11, 13, equal to `n_0 - 1`;
  - zero columns, repeated columns and `a = 0`;
  - 600 random cases at p = 3 and 13 (a = 4, M = 15).
- **Section 6.4.** All 22 names exist, and the guard format and the anchor are correct.

Findings, all non-blocking, and what was done with each:

1. The totals in 6.3 were out of date: the paper now says 471 module guards and 509 in
   all. **Fixed**: they now read 493 and 531.
2. 6.1 said "x∈(P∪{0})^M over any field". **Fixed**: it now says the entries lie in every
   set D ∋ 0 closed under the products, with D = P∪{0} over F_p.
3. A sentence in the paper ("Lean takes g to generate F_p^×") would contradict the new
   text. **Fixed**: 6.1 now includes a replacement sentence for it.
4. The 6.2 abstract edit put positive claims inside the "outside the boundary" list.
   **Fixed**: they moved to the "Lean checks" sentence, and the outside list now says
   "polynomial-time SDE algorithms".
5. The guard count was wrong: there are 33 `#guard_msgs` commands, 23 of them axiom
   guards and 10 evals. **Fixed** in Section 4.
6. `cwSearch` was called "sound and complete", but only completeness given existence is
   proved. **Fixed**: the report now says "complete".
7. 6.1 said "three solvers" and "no input but the columns". **Fixed**: it now says "the
   solvers" and "no input but p, d and the columns".
8. The cost remarks were informal. **Fixed**: they are marked "by inspection of the code,
   not by proof".
