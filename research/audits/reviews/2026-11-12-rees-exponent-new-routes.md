# Rees exponent of m: new routes and limits (2026-11-12)

Status: AI only (Claude), pending human review. Every claim below is
AI-checked. No paper, `STATE.md`, handoff or reduction JSON was edited. The
scripts are in `research/audits/reviews/2026-11-12-rees-exponent-new-routes/`
(run with `/opt/anaconda3/bin/python`). Finite checks are labelled as such:
they can only falsify.

Notation is that of `docs/papers/rees-hsp/core/main-core.tex`: the cover
`A = ⊕ t^k γ_k(L)`, its truncations `A^(d)`, the groups `G_d`, `Z_d = t^d γ_d`,
the hidden lifts `H_d`, `K_d = t^d(h ∩ γ_d)`, `a_d = dim K_d^⊥ ≤ g_d`, and
`κ_d = gcd(d, p-1)`. If a stage-d node has arity `M_d ≍ g_d^{e_d}`, the
exponent of m in `Q = c(m+τ) ∏ M_d` is `E = 1 + Σ_{d=2}^c e_d`.

## 0. Headline

1. **The degree-one target is already met, conditionally, by a route in the
   repo.** Theorem A (§1): the full version's weight-doubling and
   free-coordinate nodes (`appendix-free-coordinate.tex`, Remarks
   `rem:fc-witness-h3` and `rem:fc-zero-sum-arity`) give
   `max_{p>c} E(c,p) = (2+o(1))c`. More precisely, `2c-1 ≤ max_p E ≤ 2c - 1 + (⌈log₂c⌉-1)(1 + c^{3/4+o(1)})`.
   CONDITIONAL on those appendix results: i.i.d. uniform labels from ideal
   sources, nodes that may abort, AI-checked only. The c² log c of Theorem
   `thm:main` comes only from requiring a *total, label-law-free* solver
   (Schedule 1). Discharging the conditions is the other agent's job; this
   note only adds the asymptotic count. Exact evaluation of the formula
   (§8) gives `max_p E - (2c-1) ≤ 4` for every `c ≤ 24` (the maximum is at
   p = 31 for most c ≥ 15). The proven bound in (ii) is far looser.
2. **New structural device: multi-output merges at the last stage.**
   Theorem MO2 (§3), PROVED. At stage d = 2, a single merge can output r
   independent exact copies of `ρ_{H_1}` when the weight matrix spans a
   totally isotropic subspace of the label quadratic map
   `q_λ(w) = Σ w_i² λ_i`. Supports may overlap, so a single-output merge's
   ≥ a+1 labels per output is no longer a floor. The rate is at most about
   1/2 (Lemma W). It is the first construction in this line where the stages
   do not compose purely multiplicatively. But it gains at most one grade's
   factor, O(1) in E.
3. **Limits (PROVED within stated models).** Multi-output is impossible at
   every stage d ≥ 3 (Proposition MO3): composition there is forced to be
   multiplicative. No other public symmetry of the Rees cover exists
   (Theorem R): the d-th powers on `Z_d` are intrinsic. No cover filtration
   has fewer grades. No direct homomorphic preparation of quotient sources
   exists (Theorem D). Two grades cannot be merged in one central step
   (Theorem Z). Partial or Kuperberg-style measurements reduce to classical
   label trees (Lemmas C, PM). The naive field-extension lift fails
   (Proposition F). In the label-combining model, `E ≥ c` for single-output
   trees and `E ≥ c-1` with stage-2 multi-output, on free nilpotent algebras
   with many generators (Theorem LB). So in the model the open window is
   `[c-1, 2c+o(c)]`, and the remaining question is a factor 2: poly-time
   arity `a^{1+o(1)}` at the grades with `κ_d ≥ 2`.

## 1. Theorem A: the known conditional route has degree one (CONDITIONAL)

**Statement.** Assume Theorem `thm:free-coordinate`(iii) and Remarks
`rem:fc-witness-h3`(b,c) and `rem:fc-zero-sum-arity`(b) of the full version.
Their exponent is `E(c,p) = 1 + Σ_{d=2}^c (1+j_d)`, with `j_d = 0` at
`κ_d = 1`, `j_d = ⌈log₂(p-1)⌉` at `κ_d = p-1`, and `j_d = j*_{h_d}` otherwise
(`h_d = (p-1)/κ_d`). Then for every `c ≥ 2`:

(i) `max_{p>c} E(c,p) ≥ 2c-1`;

(ii) for every prime `p > c`,
`E(c,p) ≤ 2c - 1 + (⌈log₂c⌉-1)·(1 + N(c,p))`, where
`N(c,p) ≤ c·τ(p-1)/p^{1/4}` and `N(c,p) = 0` unless `p ≤ c⁴`;

(iii) hence `max_{p>c} E(c,p) ≤ 2c + c^{3/4+o(1)} = (2+o(1))c`.

**Proof.** (i) By Dirichlet, some prime `p ≡ 1 (mod lcm(2..c))` exceeds
`c+1`. Then `κ_d = d ∈ [2, p-2]` for every d. Since `D_0 = μ_h ∪ {0}` has
`h+1 < p` elements, `j*_h ≥ 1`, so `E ≥ 1 + 2(c-1)`.

(ii) The appendix proves `j*_h ≤ ⌈log₂κ⌉`, because `|D_j| ≥ min(p, 2^j h + 1)`.
It also proves `j*_h = 1` when `√p > (κ-1)(κ-2)+3`. Call d *bad* if `j_d > 1`.
A bad d at a `Γ_F` grade has `(κ_d-1)(κ_d-2)+3 ≥ √p`. Since
`(κ-1)(κ-2)+3 ≤ κ²` for `κ ≥ 2`, this forces `κ_d ≥ p^{1/4}`. Each such d
is a multiple of a divisor `k ≥ p^{1/4}` of `p-1`, so
`N ≤ Σ_{k|p-1, k≥p^{1/4}} c/k ≤ c τ(p-1)/p^{1/4}`. Because `κ_d ≤ c`, bad
grades need `p ≤ c⁴`. The grade `κ_d = p-1` occurs only at `d = c = p-1`,
and it adds at most `⌈log₂c⌉ - 1` over the baseline `j = 1`.

(iii) Use `p > c`, so `p^{1/4} > c^{1/4}`, and `max_{n≤c⁴} τ(n) = c^{O(1/log log c)}`
(Wigert). ∎

**Exact values** (`exponent_exact.py`: exact `j*_h` by FFT sumsets at every
`(p, κ)` where the proven bound allows `j > 1`; exact evaluation of the
formula, which says nothing beyond the conditional theorem). They reproduce
the full version's `3, 6, 8, 10, 13, 14, 16, 19` for `c = 2..9` and extend
it to `c ≤ 24` (table in §8): the excess over `2c-1` is at most 4. With only
the proven bounds on `j*` (`exponent_asymptotics.out`), the computed maxima
are much larger (excess 45 at c = 40, at highly composite `p-1 = 30240`),
because `j* ≤ ⌈log₂κ⌉` is loose there. The asymptotic statement (iii) is the
proved part; the finite table only describes the formula.

What this changes: the target "exponent of degree ≤ 1 in c" is not an open
structural problem. It is the problem of making the existing nodes
unconditional, or total.

## 2. The label-combining model and lower bounds (route (e))

**Model.** A stage-d node receives sources `ρ_{H_d}` and may measure the
complete central instrument, or any partial one (Lemma PM). It chooses public
weights from the measured labels by any classical rule, of any running time,
and applies controlled right actions by public endomorphisms of `G_d` that
preserve every `H_d`. By Theorem R these are the dilations. It then traces
out the targets. A *single-output* node produces one `G_{d-1}` source.

**Lemma C (label arithmetic; PROVED).** Use an address register on `G_d`
itself (σ = id) instead of on `G_{d-1}`. The merge with weights s maps
`⊗_i ρ_{λ_i}` to exactly `ρ_μ` with `μ = Σ s_i^d λ_i`, the branch state of
Lemma `lem:central` with label μ. *Proof:* the proof of Proposition
`prop:descent` with `Q = G_d`. The entry at `(x,y)` is
`|G|^{-1} ∏_i tr(ρ_{λ_i} R_{δ_{s_i}(y^{-1}x)})`, which equals
`|G|^{-1} [y^{-1}x = hz ∈ HZ] χ_μ(z) = ⟨x|ρ_μ|y⟩`. ∎ So every
Kuperberg- or Regev-style sieve on central characters is a *classical*
label tree with d-th-power weights. Quantum combination of labels adds
nothing in this model: the models of Remark `rem:fc-zero-sum-arity`(c)
apply.

**Lemma PM (partial measurement; PROVED).** Measuring only `φ(λ)`, for a
linear map φ on the label space, is the complete central instrument for the
central subgroup `Z_φ = (ker φ)^⊥ ⊆ Z_d`. *Proof:*
`Σ_{λ ∈ λ_0+ker φ} χ_λ(-z) = |ker φ| χ_{λ_0}(-z) [z ∈ (ker φ)^⊥]`. ∎ So
splitting a stage into sub-stages of label dimensions `a^{(1)}, …, a^{(k)}`
gives a nested tree with worst-case arity at least `∏(a^{(j)}+1) ≥ Σ a^{(j)} + 1`.
Refinement never lowers the floor.

**Theorem LB (PROVED in the model).**
(i) A total node with `M ≤ a_d` fails on independent labels.
(ii) On i.i.d. uniform labels, a node with `M ≤ a_d` succeeds with
probability `< p^{M-a_d}/(p-1) ≤ 1/2`. It needs a nonzero relation, and
`Pr[M uniform vectors of F_p^a are dependent] ≤ Σ_{k<M} p^{k-a}`.
Restarting on fresh sources then costs more than `a_d+1` sources per output
in expectation.
(iii) By (i) and (ii), a single-output tree uses at least
`∏_{d=2}^c (a_d+1)` leaves per terminal sample. With stage-2 multi-output
(Theorem MO2), the number of leaves per terminal sample is still at least
`∏_{d=3}^c (a_d+1)`, because Proposition MO3 forces single output at d ≥ 3.
(iv) Take H = 1 (`a_d = g_d`, at least m terminal samples) and the free
nilpotent Lie algebra on r generators of class c, with `p > c`. By Witt's
formula, `g_d ≥ dim F_c = m(1-o(1))` as `r → ∞`. So `Q ≥ m^{c-1-o(1)}`: in
the model `E ≥ c-1`, and `E ≥ c` without multi-output.

Tightness in queries: the free-coordinate nodes have arity linear in `g_d`
(up to log p factors), so query exponent ≈ c is reached. They take
exponential classical time (Outlook of the core paper). Polynomial time is
at `2c+o(c)` (Theorem A). Both are CONDITIONAL as in §1.

## 3. Multi-output merges (route (a), reinterpreted)

The costs multiply because every merge consumes all of its active inputs and
returns one source. Costs can only add if one merge returns many outputs.

**Ansatz.** Use M targets `ρ_{λ_i}` on `G_d`, r address registers `q_j`
uniform on `Q = G_{d-1}`, and a weight matrix `W ∈ F_p^{M×r}`. Target i
receives `R_{Φ_i(q)}` with
`Φ_i(q) = δ_{W_{i1}}(σq_1) * ⋯ * δ_{W_{ir}}(σq_r)`. Rows `W_i = 0` are
discarded; the targets are then traced out. The output entry is
`|Q|^{-r} ∏_i tr(ρ_{λ_i} R_{Φ_i(r)^{-1}Φ_i(q)})`.

**Theorem MO2 (stage 2; PROVED).** Let d = 2, so Q = G_1 = tL is abelian and
`σq = q`. Let W have rank r, with
`Σ_i W_{ij}W_{ik} λ_i = 0` for all `1 ≤ j ≤ k ≤ r`. That is, the column span
of W is totally isotropic for `q_λ(w) = Σ_i w_i² λ_i ∈ F_p^{g_2}`. Then for
every positive-probability label tuple, the output is exactly
`ρ_{H_1}^{⊗ r}`.

*Proof.* In class 2,
`x_1 * ⋯ * x_r = Σx_j + ½Σ_{j<k}[x_j,x_k]` for grade-one `x_j`. Put
`g_i = Φ_i(r)^{-1} * Φ_i(q)`.
- Grade 1 of `g_i` is `Σ_j W_{ij}(q_j - r_j)`.
- Grade 2 of `g_i` is `Φ_i(q)_2 - Φ_i(r)_2 - ½[Φ_i(r)_1, Φ_i(q)_1]`, which is
  `Σ_{j≤k} W_{ij}W_{ik} B_{jk}` with `B_{jk} ∈ Z_2` independent of i.

By Lemma `lem:central`, `tr(ρ_λ R_g) = [g_1 ∈ t h] χ_λ(g_2)`, since
`λ ⊥ K_2` and `log(hz) = log h + z`.
- *Indicator.* Write `x_j` for the image of `q_j - r_j` in `tL/th`. All
  `g_{i,1} ∈ th` iff `Σ_j W_{ij} x_j = 0` for every i, iff every `x_j = 0`,
  because W has rank r.
- *Phase.* When all `x_j = 0`, the product of the phases is
  `χ(Σ_i λ_i·g_{i,2}) = ∏_{j≤k} χ_{Σ_i W_{ij}W_{ik}λ_i}(B_{jk}) = 1`.

So the entry is `|Q|^{-r} ∏_j [q_j ≡ r_j]`. As in Proposition
`prop:descent`, the output does not depend on the record. ∎

Finite check (`check_multioutput.py`, exact):
- Heisenberg, p = 3: exhaustive over all `(Q²)²` pairs (531441).
- Heisenberg at p = 5, 7; free class-3 stage 2 (a = 3) at p = 5, 7;
  filiform m = 4 stage 2 (a = 2) at p = 5: 8000 pairs each, half of them
  same-coset.
- With isotropic W (overlapping supports), indicator and phase are exact.
- Negative control: W whose columns each solve `q_λ = 0` but have
  `Σ W_{i1}W_{i2}λ_i ≠ 0`. The indicator stays exact; the phase fails on
  2545–2964 same-coset pairs per case. So the bilinear condition is
  necessary.

**Lemma W (rate; PROVED).** For every `μ ∈ F_p^{g_2}`, let
`z_μ = #{i : μ·λ_i = 0}`. Then every totally isotropic W has
`r ≤ ⌊(M + z_μ)/2⌋`. *Proof:* W is totally isotropic for the single diagonal
form `Σ (μ·λ_i) w_i²`, whose radical has dimension `z_μ`; apply Witt. ∎
If `M < p`, some μ avoids the M hyperplanes `μ·λ_i = 0` with `λ_i ≠ 0`. So
the rate `r/M` is at most `1/2 + #{λ_i = 0}/(2M)`.

Achievability:
- `g_2 = 1` (Heisenberg, filiform): `q_λ` is one nondegenerate diagonal form
  plus a radical, so `r ≥ z + ⌊(M-z-1)/2⌋`. This is found in Las Vegas
  polynomial time by splitting off hyperbolic planes: rate → 1/2.
  PROVED (standard).
- `g_2 = 2`: over `F̄_p` the smooth pencil `Q_1 ∩ Q_2 ⊂ P^{2k+1}` contains
  `(k-1)`-planes, so the rate approaches 1/2. CONDITIONAL: recalled from the
  geometry of intersections of two quadrics (Reid); rationality over F_p is
  via Lang. Not re-derived.
- `g_2 ≥ 3`: UNKNOWN.

Finite data on uniform labels (`isotropic_rates.py`) are in §8; they compare
`r_max` with `r_dec`, the best family of disjoint single-output merges.

**Proposition MO3 (no multi-output at d ≥ 3; PROVED).** Let `3 ≤ d ≤ c` and L
be nonabelian. Choose `v ∉ γ_2(L)` that is not central; it exists, since
otherwise L would be spanned by central elements. Choose a with
`[a,v] ≠ 0`, and let `H = exp(F_p v)`. Suppose some active row of a
multi-output merge of the ansatz has `W_{ij}W_{ik} ≠ 0` for two registers
j < k. Then the output is not `ρ_{H_{d-1}}^{⊗r}`.

*Proof.* Take `r_j = e`, `q_j = tv` (in `H_{d-1}`), `q_k = r_k = ta`, and all
other registers equal. Then `g_i = δ_{W_{ik}}(ta)^{-1} δ_{W_{ij}}(tv) δ_{W_{ik}}(ta)`
(up to the order of the factors). Its grade-2 part is
`±W_{ij}W_{ik} t²[v,a] ≠ 0`. Since d ≥ 3, grade 2 is not central, and
`H_dZ_d` has grade-2 part `t²(h∩γ_2) = 0`. So `tr(ρ_{λ_i}R_{g_i}) = 0`,
while the target entry is `|Q|^{-r} ≠ 0`. This holds for every label
tuple. ∎ Hence exactness for all H forces pairwise disjoint column
supports: the merge is a union of single-output merges.

Exact check: free class-3 algebra at p = 5, 7 and filiform m = 4 at p = 5.
The weights (1,1) and (2,3) leave a grade-2 residue, for example
`t²(z + 4w)`. The weights (1,0) and (0,1) are exact.

The same cross term explains why d = 2 is special: there the residue lies in
the centre, and the labels can cancel it.

## 4. Merging grades in one central step (route (a); PROVED)

**Theorem Z.** For `d ≤ c ≤ p-1`,
`Z(A^(d)) = A_d ⊕ ⊕_{k<d} t^k(γ_k ∩ Z(L))`.

*Proof.* Dilation-stable subspaces are graded, because the characters
`θ ↦ θ^k` (`1 ≤ k ≤ d ≤ p-1`) are distinct. For `t^k y` with `k < d`,
centrality needs `[tL, t^k y] = t^{k+1}[L,y] = 0`, that is, `y ∈ Z(L)`;
conversely, `y ∈ Z(L)` suffices. ∎

So a "mixed-degree" central step can remove grade d only together with the
pieces `t^k(γ_k ∩ Z(L))`. For the free nilpotent algebra these are
`t^kγ_c`. The non-central part of every grade k ≥ 2 still needs its own
stage, so there are at least c-1 nested stages. The finest admissible
measurement that commutes with every `ρ_H` is the G-orbit decomposition of
the characters of a normal N. On the Heisenberg example `N = ⟨y,z⟩`, the
orbits with nonzero central part are full fibres over the central character:
they carry no extra label information.

## 5. Covers, filtrations, symmetry (route (c))

**Theorem R (rigidity; PROVED).** Let p ≥ 3 and `1 ≤ d ≤ c`. Every F_p-linear
Lie endomorphism ψ of `A^(d)` with `ψ(F_p tv) ⊆ F_p tv` for all `v ∉ γ_2(L)`
equals `δ_α` for some `α ∈ F_p`. These subspaces are the lifts `H_d` of the
lines `h = F_p v`.

*Proof.*
1. The vectors v span L, so ψ maps tL into itself; let T be its restriction.
2. T fixes every line through a vector outside `γ_2`.
3. For `v ∉ γ_2` and `0 ≠ w ∈ γ_2`, compare `T(v)`, `T(v+w)` and `T(2v+w)`
   (p ≥ 3). This gives `T(w) = α_v w`.
4. The usual three-line argument gives the same α for independent `v, v'`.
   If `v+v' ∈ γ_2`, use step 3.
5. So `T = α·id`. Then `ψ(t^k[x_1..x_k]) = α^k t^k[x_1..x_k]`, and these
   span `t^kγ_k`. ∎

Exact checks: for the Heisenberg algebra at p = 3, 5, the only line-preserving
3×3 maps are the scalars, by brute force over `p^9` maps. `⟨tL⟩ = A` for
heis, free3 and fili4 at p = 5, 7.

Consequence: in the model of §2, the only available scalars on `Z_d` are the
d-th powers, so `κ_d` is intrinsic. *Generalized filtrations.* Let
`F_1 = L ⊇ F_2 ⊇ …` with `[F_i,F_j] ⊆ F_{i+j}`. Then `γ_k ⊆ F_k` by
induction, so `R_F = ⊕ t^kF_k` has a nonzero grade at every `k ≤ c`. The
argument above (with `F_2` in place of `γ_2`) shows that every admissible ψ
acts on `t^kγ_k ⊆ t^kF_k` by `α^k`. A merge that removes a central subgroup
containing `t^kγ_k` therefore solves the degree-k system on the restricted
labels. No admissible filtration has fewer grades or avoids any degree
`2..c`. The p-central series equals `γ` in exponent p, and the "2-step"
filtration `L ⊇ γ_2 ⊇ 0` is admissible only in class 2. PROVED.

*More interpolation points* give nothing new: by Lemma `lem:homogeneous`,
`hlift = ∩_{s∈F_p^×} E_s^{-1}(h)`, and `E_0 = 0`. *Weights* live in
`Z/(p-1)`: `t^w x - t^{w'}x` with `w ≡ w' (mod p-1)` is killed by every
evaluation, so grades with congruent weights cannot be separated. PROVED.

**Proposition F (naive field extension; REFUTED).** Let `q = p^k` and
`ω ∈ F_q∖F_p`, and let δ_ω be the dilation of `A⊗F_q`. The map
`(y_1,y_2) ↦ y_1 δ_ω(y_2)` does not send pairs of left cosets of `H̃` to
left cosets of `H̃(F_q) = exp(hlift⊗F_q)` for every H. *Proof:* the image of
`H̃ × bH̃` is `δ_ω(b)·H̃^{δ_ω(b)}δ_ω(H̃)`. For a line h with v and a as in
MO3, `H̃^{δ_ω(b)}` has the grade-2 component `±ω t²[a,v] ∉ hlift⊗F_q`. ∎
There is also no Lie homomorphism of the form `id⊗φ: L⊗F_q → L`, because F_q
has no ring homomorphism to F_p. So F_q-scalars, which would put every grade
in the large-field regime of Schedule 2, are unavailable on an F_p oracle by
this route. Other constructions remain UNKNOWN.

## 6. Direct preparation of lower-grade sources (route (d); PROVED)

**Theorem D.** Let `2 ≤ d ≤ c` with `γ_d(L) ≠ 0`. For every finite family of
Lie homomorphisms `φ_i: A^(d-1) → L`, some line `h = F_p v` has
`∩_i φ_i^{-1}(h) ≠ H_{d-1}(h) = F_p tv`. Hence no oracle `f∘φ_i`, or tuple of
them, hides `H_{d-1}`.

*Proof.* Containing tv for every `v ∉ γ_2` forces
`φ_i(tv) ∈ F_p v`. As in Theorem R, `φ_i|_{tL} = α_i·(tx ↦ x)`. If
`α_i ≠ 0`, the image contains L, which has class ≥ d. That is impossible
for a quotient of a class-(d-1) algebra. So all `φ_i = 0`, and the pullback
is everything. ∎ The extension `0 → A_d → A^(d) → A^(d-1) → 0` is moreover
non-split: d-fold brackets of `tL` are nonzero in `A^(d)` and zero in
`A^(d-1)`.

## 7. Quantum solvers for the diagonal system (route (b); UNKNOWN)

Once the labels are measured, each stage is a classical search problem
(Lemmas C, PM). A quantum algorithm could only help there. At arity
`a + O(1)` the solutions are exponentially rare (density about `κ^{-M}`
on the kernel), so Grover-type search is exponential. At polynomial arity,
the problem on uniform labels is the Module-SIS-type problem of Remark
`rem:fc-witness-h3`(d). No quantum algorithm is known to us for
"all M linear forms are κ-th power residues" problems. The literature check
was shallow (two web searches; Ivanyos–Sanselme–Santha and Imran–Ivanyos
were noted). Status: UNKNOWN; no lead found.

## 8. Finite computations (exact; finite checks only)

| script | output | result |
|---|---|---|
| `check_multioutput.py` | `check_multioutput.out` | MO2 exact (isotropic W) in all 6 cases; phase failures in all 6 non-isotropic controls; MO3 residues at d = 3 in 3 cases |
| `check_rigidity.py` | `check_rigidity.out` | heis p = 3, 5: line-preserving maps = scalars (3 and 5 of them); `⟨tL⟩ = A` for heis, free3, fili4 at p = 5, 7 |
| `isotropic_rates.py` | `isotropic_rates.out` | see below |
| `exponent_asymptotics.py` | `exponent_asymptotics.out` | E with proven j-bounds beyond p = 20000 (an upper bound; loose) |
| `exponent_exact.py` | `exponent_exact.out` | exact formula maxima, see below |
| `find_gain_example.py` | `find_gain_example.out` | an explicit indecomposable stage-2 gain, see below |

**Stage-2 rates** (`isotropic_rates.out`; 20 uniform label draws per case;
exact enumeration). Here `r_max` is the largest totally isotropic subspace
and `r_dec` the largest family of disjoint supports that carry isotropic
vectors. Both are existence counts, not counts of what a poly-time solver
finds.

| (p, a, M) | (5,1,5) | (7,1,5) | (5,2,5) | (5,2,6) | (7,2,6) | (5,2,7) | (11,2,5) | (5,3,7) | (7,3,7) |
|---|---|---|---|---|---|---|---|---|---|
| draws with r_max > r_dec | 0 | 2 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| Witt-bound violations | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Explicit gain (p = 7, a = 2, M = 6). The labels are
`(0,6),(6,5),(1,6),(1,5),(5,6),(5,0)`: all nonzero, pairwise
non-proportional. The vectors `w1 = (0,0,1,1,2,2)` and `w2 = (0,1,0,2,5,6)`
span a totally isotropic plane (checked by hand: both `q`-values and the
bilinear term are `(0,0)` mod 7). No two disjoint supports carry isotropic
vectors. So one MO2 merge returns 2 outputs from these 6 labels, where
disjoint single-output merges return 1.

Reading: at these small sizes, MO2 beats disjoint merges in 5 of 180 draws.
Usually `r_max = r_dec`. Finite data only; no asymptotic conclusion.

**Theorem A formula, exact** (`exponent_exact.out`: exact `j*` at every
`(p, κ)` with `j > 1` allowed, primes `c < p ≤ ((c-1)(c-2)+3)²`; beyond that
range `E ≤ 2c-1`). The `j*` code reproduces the appendix's
`j*_3 = 1,1,2,2` (p = 7, 13, 19, 31) and `j*_4 = 1,2` (p = 13, 17).

| c | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 14 | 15 | 16 | 18 | 20 | 22 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| max_p E | 3 | 6 | 8 | 10 | 13 | 14 | 16 | 19 | 21 | 25 | 28 | 33 | 35 | 39 | 43 | 47 | 51 |
| 2c-1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 | 23 | 27 | 29 | 31 | 35 | 39 | 43 | 47 |
| argmax p | – | 7 | 7 | 11 | 7 | 31 | 31 | 19 | 11 | 13 | 19 | 31 | 31 | 19 | 31 | 31 | 31 |

The excess is at most 4 for every c ≤ 24 (full list in the `.out` file). For
comparison, Schedule 1's bound is 145 at c = 9 and the combined rule's is
143.

## 9. Adversarial self-check

- *Is MO2 new, and does it matter?* We found no prior statement of it (shallow
  search; novelty UNKNOWN). It changes only the stage-2 factor, so E moves
  by at most `e_2 ≤ 2`. It is also only useful if an efficient finder of
  large isotropic subspaces exists for `g_2 ≥ 2` (UNKNOWN). Do not overstate
  it.
- *Is MO3 too narrow?* It covers products of dilated section elements in a
  fixed order, which is the natural ansatz. Merges by other channels
  (arbitrary maps `Φ_i`, or coherent use of the targets) are not covered.
  The claim "composition is multiplicative at d ≥ 3" is PROVED only for this
  ansatz.
- *Theorem R* assumes the descent's public maps are Lie endomorphisms that
  preserve all hidden lifts of lines. A label-dependent map is still
  H-independent on lines with `K_d = 0`, so the argument applies. Maps that
  are not homomorphisms are not covered, beyond the remark that left
  translations act trivially and right translations conjugate H.
- *Theorem LB* bounds only the label-combining model. It is not a lower
  bound on quantum query complexity: information-theoretically, O(m²log p)
  copies determine H. The model excludes learning H by entangled
  measurements.
- *Theorem A* inherits every condition of the appendix nodes: the uniform
  label law, aborts, imported KMOSW constants, and AI-only checks. The
  proven o(c) bound is weak at moderate c; the exact excess is ≤ 4 only for
  c ≤ 24 and is not proved bounded. The degree-one statement is asymptotic.
  The exact `j*` uses floating-point FFT sumsets, thresholded at 0.5. They
  agree with the appendix's values for c ≤ 9, but an independent integer
  implementation was not run.
- Two sign conventions (`R_g`, entry `(q,r)`) were taken from the paper's
  Proposition `prop:descent` proof. The exact checks use the same
  convention, so a convention error would affect both consistently, not the
  isotropy criterion.

## 10. Next hard question

Is there a polynomial-time node, at a grade with `κ_d ≥ 2`, of arity
`a^{1+o(1)}` on i.i.d. uniform labels, at every prime `p > c`? Equivalently,
can the factor 2 in Theorem A be removed? A cheaper sub-question: at
`g_2 = a ≥ 2`, can a common totally isotropic subspace of dimension `Ω(M/a)`
of the a diagonal forms be found in polynomial time from `M = O(a)` labels?
That would make the stage-2 cost amortized-linear via MO2.

Next command:
`/opt/anaconda3/bin/python isotropic_rates.py 200` with cases `a ∈ {2,3}` and
`M` up to 9 at p = 5, 7. Expected artifact: a histogram of
`(r_max, r_dec)`. Acceptance test: if `r_max/M` stays near `1/(a+1)`, the
MO2 amortization is no better than disjoint merges and the sub-question is
closed negatively at these sizes; if it approaches 1/2, look for a
constructive finder (a pencil or Jacobian construction for a = 2).

## Disposition (integrator, 2026-11-12)

Not refereed; nothing enters the papers. Theorem MO2 and the limits (E ≥ c in the
label-combining model; no multi-output merge for d ≥ 3) are candidates for a referee pass
before any use.
