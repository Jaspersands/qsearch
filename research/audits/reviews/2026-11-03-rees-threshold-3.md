# Two-level SDE threshold, round 3: why the square gap resists character sums

3 November 2026 (written on the night of 2 November). This is an AI-only research
pass for item 3 of `research/REES_FULL_CAMPAIGN_3.md`. It is not a human review, a
Lean proof or a priority claim. **"AI-checked, pending human review" applies to every
claim below.**

Labels:
- **[proved]**: a written proof in this report.
- **[exact]**: a complete finite computation; the script is named.
- **[float]**: exact counts or Monte Carlo frequencies combined in floating point.
- **[argued]**: a heuristic.

Scripts and outputs are in `2026-11-03-rees-threshold-3/`, run with
`/opt/anaconda3/bin/python` and `cc -O2`. The notation follows
`2026-11-02-rees-weil-threshold.md` (below "WT") §1 and
`2026-11-02-rees-threshold-2.md` (below "TH2"):
- χ has order κ, and Q_b = {x ≠ 0 : χ(x) = ω^b};
- h = (p−1)/κ, Q = κ^{−(κ−1)} and λ = (p−1)/κ^κ;
- y = (0, y_1, …, y_{κ−1}) is uniform;
- n_j(y) = #{x : x + y_i ∈ Q_{−(i+j)} for all i}.

## 0. Verdict

**Neither target was reached.** This pass proves no threshold of order
κ^{(κ+1)/2+o(1)}, and no explicit bound substantially below T_A for every κ.

What it does prove is a **precise obstruction, in three parts**. Each part matches one
of the three ways the character-sum method has been used on this problem.

- **(O1) Term-by-term full expansion [proved].** Expand the exact count in all κ^{κ²}
  character tuples and bound the terms one by one: by |S_e|, or by any bound that does
  not depend on the target pattern. Then **no prime p ≤ 2^{−1/(κ−1)}κ^κ can be
  certified**.
  - The witnesses are the degenerate configurations with all α_j equal.
  - The Parseval (L²) version, which uses the full (κ!)²/κ relabelling symmetry, still
    cannot certify p ≤ κ^κ(1+√(|O|/κ^κ))^{−1/(κ−1)}. This is ≈ e·κ^{κ−1/2} for large κ
    and ≥ 0.26κ^κ for κ ≤ 100.
  - Katz's nonsingular theorem (IMRN 2002, Thm 5) needs the hyperplanes to be in
    general position. That hypothesis fails for every one of these sums, because the
    hyperplanes α_j + β_i = 0 form the graphic arrangement of K_{κ,κ} **[proved]**.
  - At κ = 3, about 100 sums of size ≈ p^{2κ−1}, with supports of size 4 and 6, carry
    75% of the error mass at p = 139 **[exact]**.
- **(O2) Averaging over β with information on at most κ−1 columns [proved].**
  Suppose a certificate uses only statements about at most κ−1 of the column counts
  (n_j) at a time, and each statement holds when the columns are independent copies of
  the true marginal. Then **no prime p ≤ κ^κ/2 can be certified.**
  - The reason is a law on ℕ^κ that is exactly independent on every κ−1 columns and
    gives probability 0 to all κ columns being solvable. This is Benjamini,
    Gurel-Gurevich and Peled's Proposition 26 (arXiv:1201.3261), applied here.
  - With information on k ≪ κ columns, their Theorem 27 pushes the obstruction up to
    λ ≈ ln(κ/(Ck log κ)), so close to ln κ.
  - Real instances show the same thing **[exact]**. At κ = 4, p ∈ {37, 53, 61}, and at
    κ = 5, p = 131: every set of κ−1 columns is solvable together for a positive
    fraction of β, yet no strict normalised contraction exists.
- **(O3) The κ-column statistic is the problem itself [proved].** The only joint
  statistic that can certify is E[∏_j n_j]. It equals the number of normalised
  contractions divided by p^{κ−1}. Bounding it with Weil one x-tuple at a time gives
  back exactly T_W ≈ κ^{2κ}.

**Conclusion.** Any proof below about κ^κ/2 must do two things.
1. Control the event that all κ columns are solvable together, beyond what any κ−1
   columns can see.
2. Get cancellation **across** the κ^{κ²} character tuples, or use a non-character-sum
   argument.

Neither is available in Weil, Deligne or Katz as applied here, in the large sieve, or in
moment methods. Bilinear sums Σ_{a∈A, b∈B} χ(a+b) over general small sets meet the same
barrier: Hanson–Petridis (arXiv:1905.09134, §1) note that Vinogradov's √(p|A||B|) is
"still the best known estimate" there.

**Best proved threshold: unchanged.** It is min(T_A(κ), T_C(κ)) from WT and TH2:
- κ^{κ+o(1)} in general;
- T_A ≈ (κ−1)κ^κ is best for κ ≤ 14;
- T_C ≤ 4e⌈ln 4κ⌉²κ^κ + 1 for κ ≥ 32.

## 1. Setting: three levels of information

There are three levels at which the character-sum method has been used:

| level | statistic | best certified so far | obstruction (this pass) |
|---|---|---|---|
| 1 column | law of one n_j (moments via per-tuple Weil) | T_A (Paley–Zygmund), T_C (moments of order 2m) | union bound needs p ≥ (1−1/κ)κ^κ (WT §4) |
| ≤ κ−1 columns | joint laws of up to κ−1 of the n_j | nothing beyond level 1 | p ≤ κ^κ/2 cannot be certified (O2) |
| all κ columns | E∏_j n_j = N/p^{κ−1}, full expansion | T_W (per-tuple Weil), 139 at κ = 3 (triangle) | p ≤ 2^{−1/(κ−1)}κ^κ cannot be certified term by term (O1) |

The exceptional sets observed so far sit far below every obstruction line. The largest
exceptional primes are 53, 181, 859 and 3221 at κ = 4..7. The κ^κ/2 line is 128, 1563,
23328 and 411772. So the existence that holds in the gap
(1.5κ^{(κ+1)/2}, κ^κ/2) is invisible to every method above.

## 2. Theorem O1: term-by-term expansions are pattern-blind

**Setting.** For a pattern c ∈ Z_κ^{κ×κ}, let N_c = #{(α,β) ∈ F_p^{2κ} : α_j + β_i ∈ Q_{c_ij}
for all i, j}. With χ^s(0) = 0 for every s,

    N_c = κ^{−κ²} Σ_e ω^{−⟨e,c⟩} S_e,    S_e = Σ_{α,β} Π_{ij} χ^{e_ij}(α_j + β_i)    (TH2 §3.3).

Put S_0 = #{(α,β) : all cells ≠ 0} and μ = κ^{−κ²}S_0. The term-by-term certificate for
the Rees pattern c_0 = (−(i+j)) is L1 := Σ_{e≠0}|S_e| < S_0.

**Theorem O1 [proved].** For every κ ≥ 2 and prime p ≡ 1 (mod κ), if
κ^{κ(κ−1)} ≥ 2p^{κ−1}, that is if p ≤ 2^{−1/(κ−1)}κ^κ, then L1 ≥ S_0. The same holds for
any family of bounds B_e ≥ |S_e|, and more generally for any upper bound on
|N_c − μ| that holds for every pattern c.

*Proof.*
1. *The bound is pattern-blind.* N_c − μ = κ^{−κ²}Σ_{e≠0}ω^{−⟨e,c⟩}S_e, so
   |N_c − μ| ≤ κ^{−κ²}L1 for every c at once. If L1 < S_0, then N_c < 2μ for every c.
2. *A crowded pattern.* Let c* be row-constant, (c*)_ij = f(i). Configurations with
   α_0 = … = α_{κ−1} = a and a + β_i ∈ Q_{f(i)} have this pattern, and each β_i has
   exactly h choices for each a. So N_{c*} ≥ p h^κ.
3. *Size of μ.* For fixed β, each α_j avoids the values −β_i, so
   S_0 ≤ p^κ(p−1)^κ and μ ≤ p^κ(p−1)^κ κ^{−κ²}.
4. *Comparison.* Now p h^κ ≥ 2μ follows from κ^{κ²−κ} ≥ 2p^{κ−1}. This contradicts
   step 1. ∎

**Corollary O1′ (Parseval) [proved].** The Rees pattern c_0 has the same count as every
pattern −(σ(i) + τ(j)), with σ, τ permutations (permute α and β). This orbit O has
(κ!)²/κ elements. So the L² certificate reads

    |N_{c0} − μ|² ≤ |O|^{−1} Σ_c (N_c − μ)² < μ².

Any upper bound for Σ_c(N_c − μ)² is at least κ^κ(p h^κ − μ)², from the row-constant
patterns. Hence the certificate is impossible whenever

    κ^{κ(κ−1)} ≥ p^{κ−1}(1 + √(|O|/κ^κ)).

The largest such p is P2 (`blind_bounds.py`, `blind_bounds.out` **[float, 40 digits]**):

| κ | 3 | 4 | 5 | 7 | 10 | 20 | 100 |
|---|---|---|---|---|---|---|---|
| P1/κ^κ (O1) | 0.71 | 0.79 | 0.84 | 0.89 | 0.93 | 0.96 | 0.99 |
| P2/κ^κ (O1′) | 0.77 | 0.83 | 0.85 | 0.83 | 0.76 | 0.56 | 0.27 |

Asymptotically P2 ≈ e·κ^{κ−1/2}. The large sieve over κ-th power classes is this
Parseval step, since only the κ characters χ^s of one modulus are available. So it
stays at exponent κ − 1/2 or above **[proved for this L² form]**.

**Scope.** O1 is witnessed by degenerate configurations, with all α_j equal. A
refinement that removes the degenerate strata by inclusion–exclusion over coincidences,
and treats them exactly, is **not** covered. For that refinement, the tuple-counting
heuristic (WT §4, TH2 §3.2) still gives about (κ−1)^{κ+1}, even if every remaining sum
had square-root size on the (2κ−2)-dimensional orbit space **[argued]**.

**Katz/Deligne do not apply [proved].** Take Katz, "Estimates for 'nonsingular'
multiplicative character sums", IMRN 2002, no. 7, 333–349. The full text read here is
`web.math.princeton.edu/~nmk/multp5.pdf`, Theorem 5 and its hypothesis (b). Theorem 5
gives |Σ_V ψ(f)| ≤ C q^{n/2} on V = X − ∪Z_i. Hypothesis (b) requires every
intersection ⋂_{i∈I} Z_i to have codimension #I.
- Our domain removes all κ² hyperplanes α_j + β_i = 0.
- The forms α_j + β_i for (i,j) in an edge set E are linearly independent exactly when
  E is a forest in K_{κ,κ}. For bipartite graphs the unsigned incidence vectors have
  rank v − (number of components).
- A 4-cycle gives four hyperplanes meeting in codimension 3.
- So (b) fails for every S_e once κ ≥ 2.

Theorem 1 of the same paper, for a single smooth f, fails too: f = Π(α_j+β_i)^{e_ij}
is singular. A singular-case estimate, Rojas-León (IMRN 2005, 1221–1234), was not
reachable: the repository returned 403 and there is no arXiv version. Its applicability
is therefore **UNKNOWN**, not refuted.

**The numbers at κ = 3 [exact].** Scripts: `triangle_strata_k3.py`,
`triangle_strata_k3.out`, `triangle_hist_k3.py`, `triangle_hist_k3.out`. This splits
TH2's L1 by the support graph of e. (`triangle_hist_k3.py` imports the strata script,
which reprints its p = 139, 199 lines at the top of `triangle_hist_k3.out`; those lines
are identical.)

| p | L1/S0 | cycle supports (13872 e) | forest supports (5298) | full supports (512) |
|---|---|---|---|---|
| 61 | 2.51 | 2.26 | 0.207 | 0.046 |
| 103 | 1.29 | 1.19 | 0.086 | 0.018 |
| 139 | 0.893 | 0.832 | 0.053 | 0.008 |
| 199 | 0.597 | 0.564 | 0.030 | 0.004 |

- At p = 139, 102 values of e with |S_e| ≥ p^{4.5} carry L1/S0 = 0.754. Their supports
  have 4 cells (54 of them) or 6 cells (48 of them).
- max|S_e|/p^5 → 1 on cycle supports, so these sums have size ≈ p^{2κ−1}.
- 15792 of the 19682 sums vanish. Scaling (α,β) → λ(α,β) kills every e with
  Σe ≢ 0 (mod κ), but that accounts for only 13122 of them. The remaining zero sums
  were not explained.
- O1's inequality L1 ≥ κ^{κ²}(ph^κ − μ) was checked at every listed p. It binds only at
  p ≤ 19.

## 3. Theorem O2: information on κ−1 columns cannot decide

Let ν be the law of n_0(y). Every n_j has this law (WT §6, the independent check).

**Lemma (BGP Proposition 26, restated) [proved here].** Let K ≥ 2 and 0 < q ≤ 1/2. Let
ν_0 be any law on ℕ with ν_0(0) = 1 − q. There is a law Λ on ℕ^K with these two
properties:
- (i) for every S ⊂ {0..K−1} with |S| ≤ K−1, the marginal of Λ on S is exactly ν_0^{⊗S};
- (ii) Λ(all coordinates > 0) = 0.

*Proof.* The construction has three steps.
1. Let W take values in {0..K} with
   w_z = C(K,z) q^z[(1−q)^{K−z} − (−q)^{K−z}].
   Then Σ w_z = 1 − (q−q)^K = 1 and w_K = 0. Every w_z ≥ 0, because q ≤ 1/2 and the
   bracket is negative only when K−z is even and q > 1/2.
2. The correction w − Bin(K,q) is −q^K(−1)^{K−z}C(K,z). Its factorial moments of order
   k ≤ K−1 vanish, since they are K-th finite differences of polynomials of degree
   k < K. So E(W)_k = (K)_k q^k for k < K.
3. Let I be a uniform W-subset of the K coordinates, put n_j = 0 for j ∉ I, and draw
   n_j for j ∈ I independently from ν_0 conditioned on n_j > 0.

Then P(I ⊇ T) = E(W)_{|T|}/(K)_{|T|} = q^{|T|} for |T| ≤ K−1. By inclusion–exclusion
the indicators on any S with |S| ≤ K−1 are i.i.d. Bernoulli(q). Mixing back gives
ν_0^{⊗S}. Finally P(all > 0) = w_K = 0. ∎

BGP state the bit version with "p ≤ 1/2, k < n" and an XOR construction (arXiv:1201.3261,
§4.9, Prop. 26; full text read).

**Converse [proved; exact + LP check].** If q > 1/2, every law on {0,1}^K with i.i.d.
Bernoulli(q) marginals on all (K−1)-sets has

    P(all ones) ≥ q^K − q^{K−d}(1−q)^d > 0,    d the largest even number ≤ K.

The fibre is the one-parameter family Bin + t·(K-th difference), and the binding
constraint sits at the largest even K − z. `obstruction_law.py`
(`obstruction_law.out`) checks the following:
- the identities exactly in rationals, for K = 2..20 and q = 1/40..39/40, with 0
  failures;
- the minimum over **all** (not only exchangeable) laws, by LP for K ≤ 6, agreeing with
  the formula to 2·10⁻¹⁶.

So with exact (κ−1)-wise independence the threshold would sit at q = 1/2, but no method
here gives exact independence.

**Theorem O2 [proved].** Let 𝔉 be a set of statements about the joint law of
(n_0, …, n_{κ−1}). Suppose each statement involves at most κ−1 coordinates and is true
for ν^{⊗κ} (independent copies of the true marginal). If ν(0) ≥ 1/2, then 𝔉 does not
imply P(all n_j > 0) > 0, so 𝔉 cannot show p ∉ E_2(κ) by the β-averaging route. In
particular this holds for every p ≤ κ^κ/2, since
ν(n > 0) ≤ E n_0 = h^κ/p^{κ−1} < p/κ^κ.

*Proof.* Apply the Lemma with ν_0 = ν and K = κ. Λ satisfies every statement in 𝔉,
and Λ(all > 0) = 0. ∎

**Remarks.**
- *Which methods this covers [argued].* All single-column facts are allowed, because
  they hold for ν^{⊗κ}. That covers Lemma D, Theorem 5 and Paley–Zygmund. Also allowed
  are mixed-moment bounds whose Weil error intervals contain the product value. The
  Lemma D intervals do, because E_k grows roughly additively in k.
- *Information on fewer columns [proved, via BGP Theorem 27, eq. (15)].* For
  information on k ≪ κ columns and 1 − q = 1/(prime power), a bad law exists once
  κ ≥ C(k/(1−q))log(1/(1−q)). C is an absolute constant that BGP do not make explicit.
  So with k = O(1) columns the obstruction reaches 1 − q ≈ C k log κ/κ, that is
  λ ≈ ln κ − O(ln ln κ). That is within O(ln ln κ) of the Poisson limit ln κ of the
  union bound (TH2 §3.1). BGP's eq. (14) is the matching positive side for exact k-wise
  independence.
- *No other row order helps [argued].* The bijection between β-orders and patterns is
  absorbed by relabelling (TH2 §3.4 and `blind_bounds.py`). Taking β unordered helps
  only through the event that all κ columns are solvable for some order, which is
  again a κ-column event.

**Real instances [exact; `jointlaw.c`, `jointlaw_exact.out`].** These are exact joint
laws of the indicators (1[n_j > 0])_j over every y, using the free Q_0-scaling of y.
They cover κ = 3 (p ≤ 1500), κ = 4 (p ≤ 700) and κ = 5 (p ≤ 131). "AND_{κ−1}/Π" below is
P(the κ−1 columns of a set S are all nonempty)/Π q over all (κ−1)-sets S (a single value
when they agree).

| κ, p | q | P(all) | AND_{κ−1}/Π | comment |
|---|---|---|---|---|
| 4, 37 | 0.124 | 0 | 0.374 | 37 ∈ E_2(4) |
| 4, 53 | 0.181 | 0 | 0.415 | 53 ∈ E_2(4) |
| 4, 61 | 0.206 | 0 | 0.396 | 61 ∉ E_2(4): contractions there need zero cells |
| 4, 73 | 0.248 | 3.7·10⁻⁴ | 0.414 | P(all)/Πq = 0.098 |
| 4, 137 | 0.425 | 0.0329 | 0.974 | P(all)/Πq = 1.01 |
| 5, 131 | 0.040 | 0 | 0.348 | 131 ∈ E_2(5) |

So the obstruction is realised by actual primes. Every κ−1 columns are solvable together
with positive probability, the κ columns never are, and q < 1/2. The strict normalised
search reproduces E_2 exactly for κ = 4, 5 in range, except κ = 4, p = 61 (zero cells
needed). At κ = 3 it also gives 7 and 13; zero cells handle those, and E_2(3) = ∅.

Sampled runs (`jointlaw_sample.out`, 2·10⁵ uniform y each, **[float]**) show the true
law close to fully independent once p is above E_2. Examples:
- κ = 5: P(all)/Πq = 0.80, 0.89, 0.93, 0.98 at p = 401, 1511, 2161, 3001;
- κ = 6: 0.97, 0.99, 0.99 at p = 23311, 32341, 70009.

In the window max E_2 < p ≤ κ^κ/2, existence is therefore carried by the κ-column
correlation, that is P(all) ≈ Π q > 0. That is exactly the quantity O2 says lower-order
information cannot reach.

## 4. O3: the κ-column statistic is the original problem [proved]

Σ_y Π_j n_j(y) = #{(y, x_0..x_{κ−1}) : all κ² conditions}, which is the number N of
normalised strict contractions. So E[Π n_j] > 0 ⟺ N > 0. Write it as
Σ_x Π_{i≥1} N_i(x)/p, where N_i(x) counts y_i with κ conditions, one per column.
- Lemma D's bound for a κ-point inner count has relative error κ^κ E_κ(p)/(p−κ) ≈ (κ−1)κ^κ/√p.
  That is < 1 only for p ≳ (κ−1)²κ^{2κ}, which is WT's T_W ("the per-tuple Weil value
  of the κ-column statistic").
- For p < κ^κ the inner counts N_i(x) vanish for most x. So any estimate must locate the
  rare x-tuples with N_i(x) > 0, which is the same problem with rows and columns swapped.

## 5. Other routes in the brief

- **Higher moments of one column.** Covered by O2: they are single-column information.
  TH2's T_C is within O(ln κ) of the union-bound limit.
- **Large sieve over κ-th power classes.** This is Parseval over the κ^{κ²} tuples, and
  O1′ covers it. The multiplicative large sieve needs many moduli or characters; here
  there is one modulus and κ characters **[argued]**.
- **Weil for the contraction variety.** Lang–Weil (WT §4) gives a worse result.
  Katz/Deligne's nonsingular form fails hypothesis (b), as shown in §2.
- **Waring over F_p, Cochrane–Pinner.** Those results concern sums of many κ-th powers,
  or small subgroups (h < p^{1/2}). Here the subgroup has index κ, and the condition is
  that two-term sums α_j + β_i land in prescribed cosets. No statement was found that
  applies, and none was read in full, so **no claim is made**.
- **Stepanov / Hanson–Petridis** (arXiv:1905.09134, Thm 1.2:
  A + B ⊆ Z_d ∪ {0} ⇒ |A||B| ≤ d + |B ∩ (−A)|, read in full). This bounds such
  configurations from above, where Z_d is the subgroup of order d. In our problem the
  cells lie in different cosets, and κ² ≪ p/κ, so it gives no constraint. The paper's §1
  remark on Vinogradov's estimate is the bilinear form of the same square-root barrier
  **[argued]**.

## 6. Statement that now holds

AI-checked, pending human review.
- (a) The threshold statements of WT, SPA and TH2 are unchanged.
  - p ∉ E_2(κ) for p ≥ min(T_A(κ), T_C(κ)), and T_A ≤ κ^{κ+1}.
  - T_C ≤ 4e⌈ln 4κ⌉²κ^κ + 1 for κ ≥ 32.
  - E_2(κ) is known exactly for κ ≤ 7.
- (b) **Theorem O1.** Term-by-term (or any pattern-uniform) bounding of the full
  character expansion cannot certify any p ≤ 2^{−1/(κ−1)}κ^κ. The L² form cannot
  certify p ≤ P2(κ) ≈ e·κ^{κ−1/2}.
- (c) **Theorem O2.** Take any set of facts about at most κ−1 column counts at a time,
  each true for independent copies of the true marginal. Such facts cannot certify any
  p ≤ κ^κ/2, or more generally any p where P(n_0 > 0) ≤ 1/2. Exact (κ−1)-wise
  independence would certify exactly when P(n_0 > 0) > 1/2.
- (d) Katz's nonsingular estimate (IMRN 2002, Thm 5) has hypothesis (b) false for every
  sum S_e of the expansion.
- (e) Exact instances of (c): κ = 4, p ∈ {37, 53, 61}, and κ = 5, p = 131.

The access model is unchanged: arbitrary columns, scalars as public precomputation.

## 7. Still missing

- (i) Any threshold below min(T_A, T_C), and any exponent below κ.
  - By (b)–(c), this needs κ-column information, together with cancellation across
    tuples, or a construction that is not a character sum.
  - The simplest open sub-question: show, for a single κ ≥ 8, that the strict count N
    is positive for all p in (C·κ^{(κ+1)/2}, κ^κ/2], by any method.
- (ii) Whether O1 survives once the degenerate strata are removed exactly. That is
  [argued] only: about (κ−1)^{κ+1}.
- (iii) Whether Rojas-León's singular estimates beat O1's refinement. UNKNOWN; the full
  text was not read.
- (iv) A human check of O1, O1′, O2 and the κ = 3, 4, 5 computations. No independent
  AI re-derivation was run in this pass.

## 8. Claim gates that must stay false

- "Two-level threshold ≈ κ^{(κ+1)/2}" or "exponent below κ" proved.
- "The character-sum method cannot reach κ^{(κ+1)/2}" as a general theorem. O1 and O2
  cover only the method classes defined above.
- "E_2(κ) known for κ ≥ 8"; "Schedule 2 optimal".
- Any equivalence with the Paley clique problem, or with Vinogradov's bilinear
  conjecture.
- Any priority or novelty claim for O1 or O2. O2's lemma is BGP Proposition 26.
- The gates of SPA, WT and TH2 are unchanged.

## 9. Proposed paper text

**Target:** `main.tex`, Remark `rem:two-level-threshold-size`. Replace its last
sentence, which begins "Any argument that averages over $\beta$ …", with the text below.
**Status label:** AI-checked, pending human review.

```latex
Closing it needs information that the standard tools do not supply. If $p \le \kappa^\kappa/2$, no argument that averages over $\beta$ and uses only statements about at most $\kappa-1$ of the column counts $|X_j(\beta)|$ at a time, each true when the columns are independent, can prove $p \notin E_2(\kappa)$: there is a law of the column counts that agrees with independence on every $\kappa-1$ columns and gives probability $0$ to all $\kappa$ columns being nonempty (Benjamini, Gurel-Gurevich and Peled, arXiv:1201.3261, Proposition~26), and exact searches find primes, such as $p = 37, 53$ for $\kappa = 4$ and $p = 131$ for $\kappa = 5$, where any $\kappa-1$ columns can be filled simultaneously but no strict contraction exists. Bounding the full character expansion of the number of contractions term by term cannot certify any $p \le 2^{-1/(\kappa-1)}\kappa^\kappa$, because the bound applies to every coset pattern at once and the configurations with all $\alpha_j$ equal overfill the row-constant patterns; and the linear forms $\alpha_j + \beta_i$ are not in general position, so nonsingular Deligne--Katz estimates do not apply (\file{research/audits/reviews/2026-11-03-rees-threshold-3.md}, Sections~2--3). A sub-family of the problem is a coloured-clique question in $\Fp$ of the same type as the clique number of the Paley graph, where the analogous gap is a long-standing open problem.
```

If the citation is kept, add a bibliography entry for Benjamini–Gurel-Gurevich–Peled
(arXiv:1201.3261). Otherwise, drop the parenthetical and keep the `\file` reference. No
other change to the theorem statements, Table `tab:main-regimes` or
`appendix-schedule2.tex` is proposed.

## 10. Artifacts (`2026-11-03-rees-threshold-3/`)

| file | role |
|---|---|
| `obstruction_law.py`, `obstruction_law.out` | O2 lemma: exact identities, converse, LP over all laws (κ ≤ 6), q = 1/2 thresholds |
| `jointlaw.c`, `jointlaw_exact.out`, `jointlaw_sample.out` | exact and sampled joint laws of the column indicators (`cc -O2 -o jointlaw jointlaw.c -lm; ./jointlaw K P0 P1 [S seed]`) |
| `blind_bounds.py`, `blind_bounds.out` | O1 and O1′ thresholds P1, P2 |
| `triangle_strata_k3.py`, `triangle_strata_k3.out`, `triangle_hist_k3.py`, `triangle_hist_k3.out` | κ = 3 expansion split by support class; check of O1's inequality |

Literature read in full: BGP arXiv:1201.3261 (§4.9, Prop. 26, Thm 27); Katz IMRN 2002
(multp5.pdf, Thms 1 and 5); Hanson–Petridis arXiv:1905.09134 (§1, Thm 1.2). Not read:
Rojas-León IMRN 2005; Cochrane–Pinner.
