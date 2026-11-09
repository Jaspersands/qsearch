# Rees diagonal SDE below quadratic arity: what column-dependent rules can and cannot do

**Status: COMPLETE (negative for the algorithmic goal; two new barrier results).**
5 November 2026 (overnight pass started 4 Nov). AI-only pass: one Claude Code session plus one
literature helper agent. This is not human review, not Lean, and not a priority claim. Everything
here is **AI-checked, pending human review.** Labels: **[proved]** (full proof written here),
**[proved, conditional]** (proof here, relative to a stated assumption), **[exact]** (complete finite
computation, script named), **[sampled]** (exact arithmetic on a random sample), **[argued]**,
**[conjecture]**. Scripts and outputs are in `2026-11-05-rees-sde-subquadratic/`; the interpreter is
`/opt/anaconda3/bin/python`. Only this file and that folder were written (no `.tex`, no git, no
handoff/STATE edits; the integrator owns those).

**Problem.** Columns λ_1..λ_M ∈ F_p^a are arbitrary, κ = gcd(d, p−1) ≥ 2, P = (F_p^×)^κ,
Sq = P ∪ {0}, Q_ν = g^ν P, cos(y) = ν for y ∈ Q_ν. Find x ∈ Sq^M, x ≠ 0, with Σ x_i λ_i = 0;
κ-th roots and a Bezout exponent then solve `eq:sde-target`. Known polynomial arity: (a+1)(a+2)/2
(`prop:triangular-sde`, p ∉ E_2(κ)) and (1−1/p)a²/2 + O(a log a) (sparse). Chevalley–Warning (CW)
existence: M ≥ κa + 1, tight in the worst case.

## 0. Verdict

1. **No o(a²) algorithm was found, for any κ, including κ = 2 with p large [argued + literature].**
   The best polynomial arity is unchanged: (a+1)(a+2)/2 for p ∉ E_2(κ) (κ = 2: every odd p), and the
   sparse (1−1/p)a²/2 + O(a log a). Goals (1) and (2) are **not** achieved. In particular the premise
   "a diagonal quadratic system in M = O(a) variables can be solved via isotropic vectors, which is
   classical" is **false as an algorithmic statement**: the classical facts are existence (CW, M ≥ 2a+1)
   and algorithms for a fixed number of forms. The isotropic-subspace recursion costs 2^{a+1} − 1
   variables (Proposition 5). The best polynomial threshold for general odd-q underdetermined quadratic
   systems is n ≥ m(m+1)/2 (Cheng–Hashimoto–Miura–Takagi 2014), the same quadratic barrier.
2. **Theorem 1 [proved; exact on 133 + 105 circuits]: one dependency gives at most one flexible
   direction, under ANY rule.** Let S be a circuit modulo U (the images of its columns in F_p^a/U have
   one dependency δ, with full support), and let δ not be monochromatic. Then the realizable set
   R_U(S) contains **no 2-dimensional subspace**. This holds for every rule, universal or
   column-dependent, adaptive or not, even computationally unbounded. So the "next hard question" of
   `2026-11-02-rees-linear-arity.md` (two or κ−1 directions per object from an instance-adaptive
   contraction) has a **negative answer** for circuit objects. A scheme that grows the realizable
   space one circuit at a time gains at most one dimension per circuit (Corollary 1). Under general
   position this forces (a+1)(a+2)/2 columns, i.e. the triangular solver is optimal among circuit
   schemes. This strengthens Proposition C of the linear-arity report (universal contractions only).
3. **Proposition 2 [proved; exact on 105 circuits]: column-dependent rules give nothing new for
   existence either.** A circuit has a flexible line iff a *class-restricted* two-level contraction
   exists on the set C of cosets met by δ. At C = Z_κ this is exactly p ∉ E_2(κ). So at
   p ∈ E_2(κ), a circuit whose dependency meets every coset has **no flexible line**. Column-dependent
   rules cannot rescue the exceptional primes for circuits that meet all cosets.
   - The set of flexible lines is larger than the class-constant ones (e.g. 12 of the 14 lines at
     p = 13, κ = 2, q = 2). Only *existence* reduces to class-constant rules.
4. **The information-theoretic barrier stops at circuits [exact].** Objects with a 2-dimensional
   kernel (q + 2 columns in a q-dimensional quotient) can have R(S) equal to the *whole* quotient:
   q = 3, p = 13 and 29, κ = 2, in 4 of 4 random samples each (`kernel2.out`). Any further barrier
   must be computational.
5. **Theorem 3 [proved, conditional on the power-residue PRF]: planted hardness below CW.** Let κ ≥ 2.
   Suppose an algorithm solves every *solvable* instance with M = a + 2 columns in time T. Then the
   power-residue PRF c ↦ χ_κ(K + c) (the Legendre PRF at κ = 2, i.e. the shifted Legendre symbol) has
   its key recovered:
   - from k = ⌈log_κ p⌉ + m random queries;
   - in time T(k−2, log p) + poly(k, log p);
   - except with probability ≤ κ^{1−k} + κp·κ^{−k}·e^{κk/(p−1)} + (p−1)^{1−k}.
   With p = 2^{Θ(a)}, a poly(a, log p) solver at arity a + 2 = o(a²) would break a believed-hard
   classical primitive. The primitive is quantumly easy (van Dam–Hallgren–Ip), which is consistent
   with the quantum setting of the paper. The deciding version is hard too (Corollary 3).
   - **Scope:** M = a + 2 < κa + 1. This is hardness for instance-wise solvers below the
     Chevalley–Warning bound. It says **nothing** about M ≥ κa + 1, where every instance is solvable.
   - The idea is due to the literature helper (an AI observation, not from the literature). The proof,
     the exact count lemma and the bound are written and checked here.
6. **Goal (3), in the CW regime, is unchanged [literature].** No hardness is known at fixed κ for
   M ≥ κa + 1. The problem is total and lies in PPA_p, so NP-hardness there would give NP = coNP.
   The uniform-in-p statement embeds open problems (Proposition 4):
   - At κ = 2 and p = 3 it is F_3^n-Subset-Sum. There KMOSW (arXiv:2609.40321) state that a classical
     polynomial algorithm at m = εn² for every ε > 0 "seems to require substantially new ideas". They
     also leave open a candidate exponential quantum speedup below 0.1022·n².
   - So a classical poly-time κ = 2 solver at o(a²), uniform in p, would settle that question
     classically.
7. **Best arity achieved: unchanged, (a+1)(a+2)/2 for every κ ≥ 2 with p ∉ E_2(κ).** Nothing at
   o(a²) for any κ.

## 1. Objects, realizable sets, flexibility

For a set S of columns and U ≤ F_p^a put
R_U(S) = { Σ_{i∈S} x_iλ_i + U : x ∈ Sq^S } ⊆ F_p^a/U.
If S_1, S_2 are disjoint, R_U(S_1 ∪ S_2) = R_U(S_1) + R_U(S_2) (Minkowski sum), because weights on
disjoint supports simply add.

A subspace U is **realizable** by disjoint sets S_1..S_l if U ⊆ R_0(S_1 ∪ … ∪ S_l).

The triangular solver builds a chain 0 = U_0 < U_1 < … < U_a = F_p^a. Its round-k object S_k is
a circuit modulo U_{k−1}, and U_k = U_{k−1} + F_p v_k with F_p v_k ⊆ R_{U_{k−1}}(S_k). One more
column of weight 1 then gives a nonzero solution. A set S is a **circuit modulo U** if its images in
F_p^a/U are linearly dependent but every proper subset is independent. Then the relation space is
F_p δ with every δ_i ≠ 0. δ is **monochromatic** if all cos(δ_i) are equal; then a multiple of δ lies in
Sq^S, and the object alone realizes an element of U with a nonzero weight, which finishes the
problem.

## 2. Theorem 1: one circuit, one direction

**Theorem 1 [proved].** Let κ ≥ 2, let S be a circuit modulo U, and let its dependency δ not be
monochromatic. Then R_U(S) contains no subspace of dimension 2. More precisely, take i, j ∈ S with
cos δ_i ≠ cos δ_j and H_ij = span of the images of S∖{i,j}. For every nonzero u ∈ H_ij, the set
{cos c : c ≠ 0, cu ∈ R_U(S)} has at most one element.

*Proof.*
- **Setting up.** Let W = span of the images of S in F_p^a/U. Since S is a circuit, dim W = |S| − 1,
  and S∖{i,j} is independent with span H_ij of dimension |S| − 2. So H_ij has codimension 1 in W.
  Every realizable vector lies in W, so a plane T ⊆ R_U(S) satisfies T ⊆ W, and T ∩ H_ij contains
  some u ≠ 0. It therefore suffices to prove the second claim.
- **The realizations of cu.** Let u ∈ H_ij∖{0} and let z be the unique vector supported on S∖{i,j}
  with Σ z_lλ_l ≡ u mod U. Then z ≠ 0. For c ∈ F_p^×, the vectors x ∈ F_p^S with Σ x_lλ_l ≡ cu are
  exactly x = cz + sδ, s ∈ F_p, because the relation space is F_p δ.
- **s must be 0.** Coordinates i and j of x are sδ_i and sδ_j, since z vanishes there. For s ≠ 0
  they are nonzero and lie in different cosets Q_{cos s + cos δ_i} ≠ Q_{cos s + cos δ_j}. So at most
  one of them is in P, and x ∉ Sq^S. Hence x ∈ Sq^S forces s = 0 and x = cz.
- **One class of c.** cz ∈ Sq^S requires cos c + cos z_l = 0 for every l with z_l ≠ 0. Since z ≠ 0,
  this fixes cos c. ∎

The proof never uses how a realization is chosen. So it bounds every rule, universal or depending on
the columns, adaptive or not, and also computationally unbounded ones.

**Ray members [proved].** The same proof works when the "columns" of S are virtual columns, i.e.
vectors w_l whose realizable set is Sq·w_l. Examples are a monochromatic half of a lower dependency,
or any fixed combination with coefficients in a single coset.

**Corollary 1 (circuit schemes) [proved].** Let S_1, S_2, … be disjoint column sets and
0 = U_0 ≤ U_1 ≤ … subspaces with U_l ⊆ U_{l−1} + R_{U_{l−1}}(S_l). Then by induction every U_l is
realizable by S_1..S_l. Suppose each S_l is a circuit modulo U_{l−1} with a non-monochromatic
dependency. Then:
- dim U_l ≤ dim U_{l−1} + 1, because U_l/U_{l−1} is a subspace contained in R_{U_{l−1}}(S_l), so its
  dimension is at most 1 by Theorem 1.
- Making F_p^a realizable needs at least a circuits.
- **(GP) case.** Assume that at each step every a − dim U_{l−1} of the fresh columns are independent
  modulo U_{l−1}. Then a circuit modulo U_{l−1} that adds a direction has at least a − dim U_{l−1} + 1
  columns. The total is at least Σ_{k=0}^{a−1}(a − k + 1) = a(a+3)/2, and (a+1)(a+2)/2 with the final
  column. This is exactly `prop:triangular-sde`.
- With sparse circuits (small p, KOW) the per-step cost drops to the minimum circuit size, but the
  gain is still at most one dimension per circuit.

**What Corollary 1 does not exclude.**
- **(GP) is not automatic [argued].** The scheme chooses U_{l−1}, and it could choose U_{l−1} so that
  the later circuits are short. Example: make v_1 lie in span(λ_i, λ_j) for two fresh columns. For p
  large, R(S_1) contains many lines, so this is information-theoretically possible. But it requires
  finding s with a prescribed coset pattern of the affine forms x_0 + sδ. That is the problem of
  Theorem 3, so it is computationally hard-looking.
- **Objects with a larger kernel.** These are excluded only computationally, not
  information-theoretically (§4).

## 3. Proposition 2: flexible lines of a circuit are class-restricted contractions

Let C = {cos δ_i : i ∈ S} ⊆ Z_κ. A **C-restricted contraction** is a pair (α, β), with
α : Z_κ → F_p and β : C → F_p nonconstant, such that α_ν + β_c ∈ Q_{−(ν+c)} ∪ {0} for all
ν ∈ Z_κ and c ∈ C.

**Proposition 2 [proved].** Let S be a circuit modulo U with dependency δ and |C| ≥ 2.
(i) R_U(S) contains a line iff a C-restricted contraction exists.
(ii) The lines in R_U(S) are exactly the lines F_p·Λ(b∘δ) where:
- b ∈ F_p^S is nonconstant;
- for every ν there is s_ν with b_i + s_ν ∈ Q_{−(ν + cos δ_i)} ∪ {0} for all i;
- here Λ(y) = Σ y_iλ_i mod U, and b∘δ is the entrywise product.

(iii) For C = Z_κ, a C-restricted contraction exists iff p ∉ E_2(κ). So at p ∈ E_2(κ), a circuit
meeting all κ cosets has no flexible line at all.

*Proof.*
- **(ii), from a line to b.** Let F_p w ⊆ R_U(S) with w ≠ 0. Pick any x_0 with Λx_0 = w and write
  x_0 = b∘δ, which is possible since every δ_i ≠ 0. Take c ∈ Q_ν. A realization of cw in Sq^S has the
  form cx_0 + sδ, and multiplying by c^{−1} gives x_0 + (s/c)δ, all of whose nonzero entries lie in
  Q_{−ν}. Its entries are δ_i(b_i + s_ν) with s_ν = s/c. So b_i + s_ν ∈ Q_{−ν−cos δ_i} ∪ {0}.
  Finally b is nonconstant, since otherwise x_0 ∈ F_p δ and w = 0.
- **(ii), from b to a line.** Given such b, set w = Λ(b∘δ). Then w ≠ 0, because b∘δ ∉ F_p δ and the
  relation space is F_p δ. For c ∈ Q_ν, the vector c(b∘δ + s_νδ) has entries cδ_i(b_i + s_ν) in
  Q_{ν + cos δ_i − ν − cos δ_i} ∪ {0} = Sq, and it realizes cw.
- **(i).** If b works, define b'_i = b_{r(cos δ_i)}, where r(c) is a chosen index of coset c. Then
  b'_i + s_ν = b_{r(c)} + s_ν ∈ Q_{−ν−c} ∪ {0}, so b' works and is constant on cosets.
  - *b' can be made nonconstant.* If b is not constant on some coset c, choose r(c) with
    b_{r(c)} ≠ b_{r(c')} for some other coset c'. If b is constant on every coset, then b' = b is
    already nonconstant.
  - *Conclusion.* (α, β) = (s, b'|_C) is a C-restricted contraction. Conversely, a C-restricted
    contraction gives b_i = β_{cos δ_i} and s_ν = α_ν.
- **(iii), universal implies restricted.** Restrict a universal contraction (α_0 + β_0 ≠ 0) to C.
  Suppose β|_C were constant, equal to b. Since |C| ≥ 2 and the cosets are disjoint, α_ν + b ∈
  ∩_{c∈C} Q_{−(ν+c)} ∪ {0} = {0} for every ν. Then α ≡ −b. For c ∉ C we get
  β_c − b ∈ Q_{−(ν+c)} ∪ {0} for all ν, so β_c = b, and β is constant. This contradicts
  α_0 + β_0 ≠ 0.
- **(iii), restricted implies universal.** Since β is nonconstant, α_{j_0} + β_{i_0} ≠ 0 for some
  pair (i_0, j_0). Choose y ∈ Q_{i_0+j_0} and set α'_j = yα_{j+j_0}, β'_i = yβ_{i+i_0}. Then
  α'_j + β'_i ∈ Q_{i_0+j_0}·Q_{−(i+j+i_0+j_0)} ∪ {0} = Q_{−(i+j)} ∪ {0}, and α'_0 + β'_0 ≠ 0. That is a
  two-level contraction in the sense of the appendix definition (Lemma `lem:app-s2-normal`). ∎

**Consequence at exceptional primes [proved + argued].**
- **Proved.** At p ∈ E_2(κ), a circuit scheme can only use circuits whose dependency misses a coset.
- **Argued.** For random columns, the cosets of a dependency of size q + 1 are close to i.i.d. uniform.
  A coset is then missed with probability at most κ(1 − 1/κ)^{q+1}. So the fallback to Schedule 1 or
  the L-level schemes at E_2 primes is not an artefact of universality.
- **Small circuits can help [exact].** At p = 37 and 53 for κ = 4, and at 71 ≤ p ≤ 181 for κ = 5,
  every sampled q = 1, 2 circuit has a flexible line (`flexline_e2.out`), because small circuits meet
  few cosets.

## 4. Objects with a 2-dimensional kernel [exact]

Take |S| = q + 2 random columns in F_p^q, so the kernel is 2-dimensional. The largest flexible
subspace found in 4 samples per row is shown below (`circuit_flex.py kernel2`, `kernel2.out`).

| p | κ | q | max flexible dims (4 samples) |
|---|---|---|---|
| 5, 7, 13, 29 | 2 | 2 | 2,1,2,2 / 2,2,2,2 / 2,2,2,2 / 2,2,2,2 |
| 13 | 3, 4 | 2 | 2,1,2,2 / 1,0,2,0 |
| 7 | 2 | 3 | 2,2,2,2 |
| 13, 29 | 2 | 3 | 3,3,3,3 (R(S) = all of F_p^3) |
| 13, 37 | 3 | 3 | 1,1,1,1 / 2,2,2,3 |

So kernel-2 objects can be flexible in dim > 2, even fully. Theorem 1 cannot be extended
information-theoretically to "dimension gain ≤ kernel dimension". The obstacle beyond circuits is
computational. Realizing a target with such an object means finding a point of an affine plane whose
q + 2 coordinates lie in prescribed cosets. That is the Legendre-type problem of §5.

## 5. Theorem 3: power-residue PRF hardness at arity a + 2

χ = χ_κ : F_p → Z_κ ∪ {∗} is the coset index (∗ at 0). The power-residue PRF with key K ∈ F_p is
F_K(c) = χ(K + c) (Damgård, CRYPTO '88). At κ = 2 this is the Legendre PRF, or the shifted Legendre
symbol. The best known classical key-recovery attacks with Q queries cost about p log²p / Q²
Legendre evaluations for Q ≤ p^{1/4} (Beullens–Beyne–Udovenko–Vitto, ToSC 2020(1)), so the cost is
exponential in log p when Q = O(log p). Van Dam–Hallgren–Ip conjecture classical pseudorandomness, and
they give a polynomial quantum algorithm.

**Reduction R.**
1. Draw c_1..c_k i.i.d. uniform in F_p and query ε_i = F_K(c_i). If some ε_i = ∗, output −c_i.
2. Let u_i be uniform in Q_{−ε_i} and w_i = u_ic_i.
3. Let Λ be a random (k−2) × k matrix whose kernel is exactly span(u, w). This gives a = k − 2 and
   M = k.
4. Run the solver on Λ. Write its output as x = αu + βw. If β ≠ 0, output α/β.

**Count lemma [proved; exact for all K ≠ t at 8 (p, κ), `countlemma.out`].** For t ≠ K and θ ∈ Z_κ,
#{c ∉ {−K, −t} : χ(t+c) − χ(K+c) = θ} = (p − 1 − κ·[θ = 0])/κ.
*Proof.* The map c ↦ y = (t+c)/(K+c) is a bijection from F_p∖{−K} onto F_p∖{1}, and y = 0 exactly at
c = −t. For a nontrivial character ψ, Σ_{y≠1} ψ(y) = −ψ(1) = −1. By orthogonality, the count is
(1/κ)[(p−2) − Σ_{j=1}^{κ−1} ζ^{−jθ}] = (1/κ)[p − 1 − κ[θ=0]]. ∎

**Theorem 3 [proved, conditional].** Let κ ≥ 2 and let p ≡ 1 mod κ be prime. Let A be any algorithm
that, given Λ ∈ F_p^{a×(a+2)} for which a nonzero x ∈ Sq^{a+2} with Λx = 0 exists, outputs such an x
in time T(a, p). Then R recovers K with probability at least
1 − κ^{1−k} − κp·κ^{−k}·e^{κk/(p−1)} − (p−1)^{1−k},
in time T(k−2, p) + poly(k, log p) (Las Vegas for the coset representatives). With
k = ⌈log_κ p⌉ + m the failure is at most κ^{1−m}(1/p + e^{κk/(p−1)}) + (p−1)^{1−k}.

*Proof.*
- **Conditioning.** Condition on no ε_i being ∗; otherwise R outputs K. Then the c_i are i.i.d.
  uniform on F_p∖{−K}.
- **u and w are independent.** They are dependent only if all c_i are equal, which has probability
  (p−1)^{1−k}. Otherwise the instance's kernel is exactly span(u, w).
- **The planted solution.** x* = Ku + w has x*_i = u_i(K + c_i) with cos x*_i = −ε_i + ε_i = 0. So
  x* ∈ Sq^k, and the instance is solvable.
- **Solutions with β = 0.** Let x = αu + βw ∈ Sq^k∖{0}. If β = 0, then cos α = ε_i for all i, so all
  ε_i are equal. Each ε_i is uniform on Z_κ, so this has probability κ^{1−k}.
- **Solutions with β ≠ 0.** Put t = α/β. Then x_i = βu_i(t + c_i). For every i, either c_i = −t, or
  χ(t + c_i) − χ(K + c_i) = θ := −cos β.
- **Spurious solutions.** Fix t ≠ K and θ. By the count lemma, each i satisfies the condition with
  probability ≤ (1 + (p−1)/κ)/(p−1) = 1/κ + 1/(p−1), independently over i. The union bound over the
  p − 1 values of t and the κ values of θ gives at most κ(p−1)(1/κ + 1/(p−1))^k ≤ κp·κ^{−k}·e^{κk/(p−1)}.
- **Conclusion.** Outside these events, every solution has β ≠ 0 and t = K, so R outputs K. ∎

**Corollary 3 (deciding) [proved, conditional].** Replace F_K by a truly random function. Then u is
uniform in (F_p^×)^k and w is uniform in F_p^k, independent of u. So the instance is the random
matrix with a 2-dimensional kernel spanned by two uniform vectors, and it is solvable with probability
at most κ^{1−k} + κ(p+1)κ^{−k}. With F_K it is always solvable. So any algorithm that decides
solvability at M = a + 2 distinguishes F_K from random.

**Remark (arity a + n) [argued; sampled at n = 3].**
- **Construction.** Replace span(u, w) by {(u_i f(c_i))_i : deg f < n}. The planted solutions are
  f = y(z + K)g^κ, and K is the root of f whose multiplicity is not ≡ 0 mod κ.
- **Bound.** Spurious f are bounded by Weil's bound for χ(f(z)/(z+K)), i.e. (n−1)√p per character,
  and a union over p^n polynomials. This needs k ≳ n·log_κ p and p ≫ (nκk)².
- **Resulting arity.** M = a + n with n ≈ M/log_κ p. With p superpolynomial (so that the PRF is not
  trivially brute-forced), this stays at M = a(1 + o(1)), far below κa + 1. It never reaches the
  Chevalley–Warning regime.
- **Why it cannot reach CW [argued].** At M ≥ κa + 1 every instance, including a random-function
  instance, is solvable, with about p^{M−a}κ^{−M} solutions spread over the kernel. A planted
  structure can then no longer force every solution to reveal K.
- **Samples.** `sweep.out` rows with n = 3 show the failure rate of event G dropping to 0 at k = 26
  for κ = 2 and to 0.07 at k = 16 for κ = 3, p = 1009.

**Relation to the paper.**
- This is the worst-case and planted counterpart of `prop:rc-lower`, which shows that bank-oblivious
  designs need about κ^a trials at arity a + O(1).
- It also explains why the free-coordinate theorem pays κ^{a}.
- It does not bear on Schedules 1 to 3 at their arities, which are all ≥ κa + 1 or use the label law.

## 6. Proposition 4 and 5: embeddings, isotropic recursion, extensions

**Proposition 4 (uniform-in-p statements contain open problems) [proved, trivial embeddings].**
- **κ = 2, p = 3.** P = {1}, so the problem is worst-case F_3^n-Subset-Sum (BIS_3). The best rigorous
  classical polynomial arity is n²/3 + O(n log n) (KOW Thm 1.2). KMOSW §1.3 announce 0.1022n² without
  a full proof, and give a quantum average-case algorithm at εn² (Thm 1.3, Cor. 1.4).
- **κ = 2, p = 5.** P = {±1}, so the problem is SIS^∞ with β = 1 over Z_5. The best known is (n+1)²
  (II24 Prop. 4) and Cn² (KOW Thm 1.5).
- **Fixed κ in general.** Take the least prime p = hκ + 1. The problem is the h-element weighted
  Davenport search. At κ = p − 1 it is BIS_p (GKSZ Def. 6.1), whose linear regime is open for every
  p ≥ 3.
- **Consequence.** A classical poly(a, log p) algorithm at arity o(a²) for κ = 2, uniform over odd p,
  would beat every known classical algorithm for F_3^n-Subset-Sum. It would also answer KMOSW's
  question (classical algorithms at εn² for every ε > 0) for the worst case, hence the average case.
- **Not a hardness proof.** No hardness assumption is known to be implied.

**Proposition 5 (isotropic-subspace recursion) [proved, standard].**
- **The step.** Over F_p with p odd, a quadratic form in n variables has a totally isotropic subspace
  of dimension ⌊(n−1)/2⌋. Such a subspace is found in randomized polynomial time: split off hyperbolic
  planes using isotropic vectors of ternary subforms, and take the radical.
- **The recursion.** Restricting the other a − 1 forms (no longer diagonal) to it and recursing solves
  a common-zero problem for a forms in N(a) variables, with N(1) = 3 and N(a) = 2N(a−1) + 1. So
  N(a) = 2^{a+1} − 1.
- **What it gives.** This is polynomial for fixed a only. It is the "classical" route, and it is
  exponential in a.
- **Merges.** The pairing and merge variants are also exponential (the avg-case report,
  Propositions 2–3: 3^a, and ≥ ½(2/(1+1/p))^a).

**Lifting through extensions [proved].**
- **When every element becomes a κ-th power.** p ≡ 1 mod κ gives 1 + p + … + p^{k−1} ≡ k mod κ.
  Hence y ∈ F_p^× is a κ-th power in F_{p^k} iff y ∈ (F_p^×)^{κ/gcd(κ,k)}. For κ | k, every F_p
  element is a κ-th power in F_{p^k}. So the extension problem is plain linear algebra, but its
  witnesses s_i = x_i^{1/κ} lie in F_{p^k}∖F_p.
- **Why that does not help.** `prop:descent` applies δ_{s_i} with s_i ∈ F_p^×. Descending back
  requires x_i ∈ (F_p^×)^κ ∪ {0}, which is the original problem.
- **Intermediate k.** For gcd(κ, k) = e the problem becomes the κ/e problem over F_p, again with
  witnesses outside F_p.
- **Subfields.** F_p has none.

**Constructive Chevalley–Warning [literature].**
- The CW and Olson proofs count solutions mod p, which is a PPA_p-type argument.
- Chevalley_p (circuit-encoded) is PPA_p-complete (GKSZ), and PPA-completeness of circuit
  Chevalley/CNSS over GF(2) is BIQSY 2017.
- A constructive diagonal CW at o(a²) would put an explicit PPA_p subproblem into FP. That is not a
  contradiction, but no technique for it is known. Ivanyos–Santha say explicitly that they cannot
  solve under the Chevalley condition alone.

## 7. Tests

All arithmetic is exact mod p. `pytest` passes: 6 tests in 7 s.
Command (in the folder):
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider test_subquadratic.py`

| check | script → output | result |
|---|---|---|
| Theorem 1 on random circuits plus adversarial coset patterns (one odd coset; alternating; all cosets; monochromatic control); 14 (p, κ, q) with p ≤ 29, κ ∈ {2,3,4}, q ∈ {2,3} | `circuit_flex.py circuits` → `circuits.out` | 133 circuits. No plane inside R(S) for any non-monochromatic one. The H_ij one-class property holds in all. The triangular line is flexible in all κ = 2 cases. |
| Prop 2 (i) existence ⇔ class-constant contraction, and inclusion | `flexline_structure.py` → `flexline_structure.out` | 105/105 |
| Prop 2 (ii) exact set of flexible lines = column-dependent b-lines | same | 97/97 checked (p^q ≤ 3000) |
| Prop 2 (iii) at E_2 primes | `flexline_e2.out`, structure output | Circuits meeting all 4 cosets at p = 13, 17 (E_2(4)) have no flexible line. p = 11 (E_2(5)) has no flexible line even for q = 1. |
| Kernel-2 objects | `kernel2.out` | R(S) = F_p^3 at q = 3, p = 13, 29 (κ = 2) |
| Count lemma, all K ≠ t | `countlemma.out` | 8 (p, κ) pairs, 0 mismatches |
| Reduction: projective-kernel enumeration = exhaustive Sq^M search; planted solution present; random and consecutive query points (the standard Legendre-PRF pattern) | `legendre_reduction.py crosscheck` → `crosscheck.out` | 54/54 instances (p = 11..17, κ = 2,3,4, n = 2,3) |
| Reduction: failure of "every solution reveals K" vs. the bound | `sweep.out`, `bound_check.out` | Matches the union bound within binomial error. Examples: κ = 2, p = 1009, k = 16: 0.0335 vs 0.0318 (s.e. 0.004); k = 14: 0.111 vs 0.127; κ = 4, k = 9: 0.0175 vs 0.016 (s.e. 0.003). At p = 10007, k = 22: 0/60 failures. |

The "solver" in the reduction tests enumerates all p+1 (or p²+p+1) kernel rays. So the tests check
the *strong* event that every solution reveals K, not just one solver's output.

## 8. Literature

Full texts were read by the helper unless marked otherwise; details are in `lit/LITERATURE.md`.
- Ivanyos–Sanselme–Santha, Algorithmica 62 (2012), Claim 1: ≈ a²/2 for diagonal quadratic systems.
- Ivanyos–Santha, TCS 657 (2017) 73–85, arXiv:1503.09016: Prop. 9 gives (a+1)². Thm 3 gives fixed d.
  The introduction says the Chevalley-regime case is open.
- Cheng–Hashimoto–Miura–Takagi, PQCrypto 2014, LNCS 8772, 40–58: underdetermined MQ over odd q in
  polynomial time at n ≥ m(m+1)/2. Read from the table in Hashimoto, JSIAM Letters 15 (2023) 53–56,
  ePrint 2021/1045.
- Thomae–Wolf, PKC 2012; Furue–Nakamura–Takagi, PQCrypto 2021; Huang–Bao, arXiv:1507.03674;
  Asanuma et al., ePrint 2026/1054: all exponential below m²/2. Thomae–Wolf and Asanuma et al. were
  read from a table or abstract only.
- KOW, arXiv:2510.07515 (Thm 1.2, 1.5); KMOSW, arXiv:2609.40321 (Thm 1.3, 1.10, 1.11, §1.3); GKSZ,
  CCC 2020 (Def. 6.1, Thm 10, OP 6); Imran–Ivanyos, arXiv:2304.08376.
- Belovs–Ivanyos–Qiao–Santha–Yang, CCC 2017, LIPIcs 79:30, arXiv:1710.08602 (abstract only).
- Restricted syndrome decoding: Baldi et al. arXiv:2008.06403 Thm 5; Baldi et al. ISIT 2023,
  arXiv:2303.08882 Cor. 1; Beullens–Briaud–Øygarden, IACR CiC 1(3) 2024. These give NP-hardness of
  the inhomogeneous, weight-constrained, near-unique regime only, which does not cover our total
  problem.
- Legendre / power-residue PRF:
  - Damgård, "On the randomness of Legendre and Jacobi sequences", CRYPTO '88, LNCS 403, 163–172
    (not re-read).
  - Beullens–Beyne–Udovenko–Vitto, "Cryptanalysis of the Legendre PRF and generalizations", IACR
    ToSC 2020(1) 313–330, ePrint 2019/1357 (abstract and record).
  - Khovratovich, ePrint 2019/862 (not read).
  - van Dam–Hallgren–Ip, "Quantum algorithms for some hidden shift problems", SIAM J. Comput. 36(3)
    (2006) 763–778, arXiv:quant-ph/0211140. It gives a polynomial quantum algorithm for the shifted
    Legendre symbol and conjectures classical pseudorandomness. Read from the abstract and record;
    the page numbers were not checked.
- Peralta, Math. Comp. 58 (1992) 433–440: finding residue patterns costs about 2^k by random search.
- **Not found:** any polynomial algorithm at o(a²) for diagonal systems at any fixed κ ≥ 2, or any
  hardness at fixed κ in the CW regime.

## 9. Status

**Claims that hold:**
- Theorem 1 [proved].
- Corollary 1 [proved; the column count under (GP)].
- Proposition 2 [proved].
- Theorem 3 and Corollary 3 [proved, conditional on the power-residue PRF].
- Propositions 4 and 5 [proved].
- Kernel-2 flexibility [exact].

**Claim gates that must stay false:**
- "An efficient o(a²) (or linear) SDE solver exists", for any κ.
- "The SDE search is hard at M ≥ κa + 1 for fixed κ or p". Theorem 3 is **below** CW only, for planted
  instances, and conditional.
- "The triangular solver is optimal". It is optimal only among circuit schemes under (GP), Corollary 1.
- "Column-dependent rules are useless". They are useless only for circuits (Theorem 1, Prop 2).
  Kernel-2 objects are open.
- Any novelty or priority claim. Theorem 1 is a short observation, and the Theorem 3 idea came from an
  AI helper.

**Next hard question.** Can an object with a 2-dimensional kernel (q + 2 columns modulo U) be made
flexible in two directions by a *polynomial-time certified* rule? Here "certified" means a decision
tree of coset queries on linear forms of the target, with linear-on-leaf realizations whose coset
classes the queries certify. Information-theoretically it can (§4). If two directions cost q + 2
columns, the count becomes about a²/4. If they cost O(1) per direction, the count becomes linear.

**Next command:** a new script `kernel2_certified.py p kappa q D`. It should search, for small
(p, q), for coset-query decision trees of depth ≤ D that realize a plane from q + 2 columns.
- **Expected artifact:** the minimal depth D*(q) for q = 2, 3, 4 at p = 13, 29.
- **Acceptance test:** either D* = poly(q) with exact witnesses for every target, or a proof that
  D* ≥ κ^{Ω(q)} in this model.

## 10. Proposed LaTeX insertion

**Location.** `docs/papers/rees-hsp/main.tex`, immediately after `\end{remark}` of Remark
`rem:triangular-scope` (line 696 of main.tex as read on 2026-11-05, after its `% NEEDS HUMAN VERIFICATION` comment, before `\begin{remark}[Combined per-grade schedule;
conditional]`). **Status: AI-checked, pending human review.** Nothing else in the paper changes.

```latex
\begin{remark}[Below quadratic arity; AI-checked, pending human review]
\label{rem:sde-subquadratic}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-sde-subquadratic.md}); no human has checked it, and nothing else in the paper uses it. For a set $S$ of columns and a subspace $U\le\Fp^{a}$ put $R_U(S)=\{\sum_{i\in S}x_i\lambda_i+U : x\in(P\cup\{0\})^{S}\}$; when $S$ is disjoint from the other columns used, any subspace contained in $R_U(S)$ can be added to the realizable space $U$, as the vectors $v_l$ are in the proof of Proposition~\ref{prop:triangular-sde}.
\textup{(a)} \emph{One dependency gives one direction.} Suppose the images of $S$ in $\Fp^a/U$ form a circuit, with dependency $\delta$ whose entries do not all lie in one coset $g^\nu P$. Then $R_U(S)$ contains no $2$-dimensional subspace, whatever rule, universal or depending on the columns, is used to choose the weights. Indeed, choose $i,j\in S$ with $\mathrm{cos}(\delta_i)\ne\mathrm{cos}(\delta_j)$ and let $H$ be the span of the images of $S\setminus\{i,j\}$, a hyperplane in the span $W$ of the images of $S$. A plane $T\subseteq R_U(S)$ lies in $W$, so it contains some $u\ne0$ in $H$. For $c\in\Fp^\times$ the vectors realizing $cu$ are $cz+s\delta$, $s\in\Fp$, where $z\ne0$ realizes $u$ on $S\setminus\{i,j\}$; for $s\ne0$ their $i$th and $j$th entries $s\delta_i$, $s\delta_j$ lie in different cosets, so the vector lies in $(P\cup\{0\})^S$ only if $s=0$ and $cz\in(P\cup\{0\})^S$, which fixes $\mathrm{cos}(c)$. Hence a scheme that enlarges the realizable space one circuit at a time gains at most one dimension per circuit, and when the fresh columns are in general position modulo the current space and no dependency used lies in a single coset (which would already give a solution) it needs the $(a+1)(a+2)/2$ columns of Proposition~\ref{prop:triangular-sde}. Moreover $R_U(S)$ contains a line if and only if there are $\alpha\in\Fp^{\kappa}$ and a nonconstant $\beta$ on the set $C$ of cosets met by $\delta$ with $\alpha_\nu+\beta_{c}\in g^{-(\nu+c)}P\cup\{0\}$ for all $\nu\in\mathbb{Z}_\kappa$ and $c\in C$; for $C=\mathbb{Z}_\kappa$ this holds if and only if $p\notin E_2(\kappa)$. Objects with a two-dimensional space of relations are not covered: for $\kappa=2$, $p\in\{13,29\}$ and $a=3$, exact computation finds five columns whose realizable set is all of $\Fp^3$.
\textup{(b)} \emph{Planted hardness below the Chevalley--Warning bound.} Let $\chi(y)\in\mathbb{Z}_\kappa$ be the coset of $y\ne0$. Suppose an algorithm returns, in time $T$, a nonzero $x\in(P\cup\{0\})^{a+2}$ with $\sum_i x_i\lambda_i=0$ for every $\lambda_1,\dots,\lambda_{a+2}\in\Fp^{a}$ for which one exists. Query $\varepsilon_i=\chi(K+c_i)$ at $k$ independent uniform points $c_i$, pick $u_i\in g^{-\varepsilon_i}P$, and take columns in $\Fp^{k-2}$ whose relation space is exactly the span of $(u_i)_i$ and $(u_ic_i)_i$. The vector $x_i=u_i(K+c_i)$ is a solution, every solution is $x_i=\beta u_i(t+c_i)$ or a multiple of $(u_i)_i$, and since $c\mapsto(t+c)/(K+c)$ is a bijection of $\Fp\setminus\{-K\}$ onto $\Fp\setminus\{1\}$, every solution has $t=K$ except with probability at most $\kappa^{1-k}+\kappa p\,\kappa^{-k}e^{\kappa k/(p-1)}+(p-1)^{1-k}$. So the key of the power-residue pseudorandom function $c\mapsto\chi(K+c)$~\cite{Damgard1988,BeullensBeyneUdovenkoVitto2020}, which for $\kappa=2$ is the shifted Legendre symbol, conjectured classically pseudorandom and solved by a polynomial-time quantum algorithm in~\cite{vanDamHallgrenIp2006}, is recovered in time $T+\poly(k,\log p)$ from $k=\lceil\log_\kappa p\rceil+O(1)$ queries. These instances have $M=a+2<\kappa a+1$ columns, so the statement concerns solving whenever a solution exists below the Chevalley--Warning bound, and says nothing about arities at which every instance is solvable.
\textup{(c)} For $\kappa=2$ the problem is a homogeneous underdetermined system of quadratic equations, and the best polynomial-time threshold known for such systems over fields of odd characteristic is again quadratic, $n\ge m(m+1)/2$ variables for $m$ equations~\cite{ChengHashimotoMiuraTakagi2014}; recursing through totally isotropic subspaces of one form at a time needs $2^{a+1}-1$ variables.
\end{remark}
```

**Bibliography entries** for `references.bib`. The page numbers were not checked against the
publishers; the integrator should verify them or cite by DOI and ePrint only.

```bibtex
@inproceedings{Damgard1988,
  author    = {Damg{\aa}rd, Ivan B.},
  title     = {On the Randomness of {Legendre} and {Jacobi} Sequences},
  booktitle = {Advances in Cryptology -- CRYPTO '88},
  series    = {Lecture Notes in Computer Science}, volume = {403},
  pages     = {163--172}, publisher = {Springer}, year = {1990}
}
@article{BeullensBeyneUdovenkoVitto2020,
  author  = {Beullens, Ward and Beyne, Tim and Udovenko, Aleksei and Vitto, Giuseppe},
  title   = {Cryptanalysis of the {Legendre} {PRF} and Generalizations},
  journal = {IACR Transactions on Symmetric Cryptology}, volume = {2020}, number = {1},
  pages   = {313--330}, year = {2020}, doi = {10.13154/tosc.v2020.i1.313-330},
  note    = {IACR ePrint 2019/1357}
}
@article{vanDamHallgrenIp2006,
  author  = {van Dam, Wim and Hallgren, Sean and Ip, Lawrence},
  title   = {Quantum Algorithms for Some Hidden Shift Problems},
  journal = {SIAM Journal on Computing}, volume = {36}, number = {3}, year = {2006},
  doi     = {10.1137/S009753970343141X}, note = {arXiv:quant-ph/0211140}
}
@inproceedings{ChengHashimotoMiuraTakagi2014,
  author    = {Cheng, Chen-Mou and Hashimoto, Yasufumi and Miura, Hiroyuki and Takagi, Tsuyoshi},
  title     = {A Polynomial-Time Algorithm for Solving a Class of Underdetermined Multivariate Quadratic Equations over Fields of Odd Characteristics},
  booktitle = {Post-Quantum Cryptography (PQCrypto 2014)},
  series    = {Lecture Notes in Computer Science}, volume = {8772},
  pages     = {40--58}, publisher = {Springer}, year = {2014}
}
```

## 11. Artifacts

| file | content |
|---|---|
| `common.py` | field and coset arithmetic, rref and kernels, realizable sets as boolean arrays, exhaustive search |
| `circuit_flex.py` (→ `circuits.out`, `kernel2.out`) | Theorem 1 checks; kernel-2 objects |
| `flexline_structure.py` (→ `flexline_structure.out`) | Proposition 2 (i)–(ii) |
| `flexline_e2.py` (→ `flexline_e2.out`) | flexible lines at E_2(4), E_2(5) primes and nearby primes |
| `legendre_reduction.py` (→ `countlemma.out`, `crosscheck.out`, `sweep.out`) | Theorem 3: count lemma, exhaustive cross-check, failure sweep |
| `bound_check.py` (→ `bound_check.out`) | 2000-trial checks of the Theorem 3 bound |
| `test_subquadratic.py` | 6 pytest checks (pass) |
| `lit/` | helper's `LITERATURE.md` and text extracts |
