# Referee report: Proposition T (template no-go) in `2026-11-12-rees-direct-twist-class3.md` (2026-11-12)

**Status: AI referee, pending human review.** I read Proposition T and its proof (note §2),
the Ivanyos–Sanselme–Santha (ISS) source it formalizes (arXiv:0707.1260 §2.3 Prop 1, §4
Thm 4, Lemmas 4–6, system (1)), and Imran–Ivanyos (I–I) arXiv:2304.08376 §1. All finite
checks are exact, and none of them proves anything (TRAPS 7). The scripts are in the session
`2026-11-12-rees-direct-twist-class3-referee/` (copied there by the integrator; the `.pkl` automorphism caches were dropped and are rebuilt by `autenum.py`). No other file was edited.

## Verdict: CORRECT WITH FIXES

The mathematics in the three steps is right. I could not break the core claim, which is this:
beyond class two, a twist that keeps every HN fixed is the identity on [L,L]. But the
statement as written is not a theorem. Its probability hypothesis does not fit how ISS
actually choose their twists: ISS pick j from the measured labels. Read literally, the
hypothesis can be met by a non-central N, so conclusion 1 fails as worded (counterexample F1
below). The conclusion is also stated about the whole set A, when it should be stated about
the twists actually used. Both defects can be repaired. The repaired statement (T′ below) is
proved, and its 1/p bound is sharp on filiform4.

## 1. Is the template fair to ISS?

Mostly yes. ISS Thm 4 is exactly this template with N = G′ (central), A = {φ_j}, the
"drop the copy" map φ_0 (ISS: "φ_0(g) = 1", which is not an automorphism), j chosen
**from the measured u** (Theorem 5 solves system (1) for the given u), and target HG′. It is not a strawman. Four
points must be made explicit or changed:

* **Dropping copies.** φ_0 has to be allowed. The note's phrase "nontrivially twisted copy"
  implies it but does not say it.
* **Twists that depend on the labels** (and on coins, but not on H) are essential to ISS. The
  proof of step 2 treats α as fixed. It has to be redone with averaging (§3).
* **Scalars on N.** The hypothesis that A acts on N by scalars is unnecessary, and it is a
  real restriction: for fil4⊕F_p with N = Z (dim 2), the automorphisms that preserve every
  line of L/N act on N by non-scalar matrices (check C1). The conclusion still holds on
  N ∩ [L,L] without it.
* **"For every cyclic H" is load-bearing.** For H ≤ [G,G]N it fails. In fil4 with N = Z and
  h = exp(x_3 + t x_4), HN = γ_2 is characteristic, so every automorphism preserves it,
  including those that scale Z by κ ≠ 1. The hard H are exactly those with v_1 ≠ 0. The note's
  routes A and B show the same thing, but Prop T should say it.

Generalizations that escape the template, or are not covered by the proof:

* A non-abelian N with an irrep-level Fourier step. The H-action permutes N̂, and right
  multiplication by N acts on a multiplicity space as a unitary, not a phase. Cancelling that
  would take Clebsch–Gordan or sieve machinery, which is a different method. This is
  **not excluded**. It is plausible that the same orbit obstruction applies, but that is
  unproved.
* Twists that depend on H, or adaptive choices of N after partial information. Once the line
  of v_1 is known, ⟨h⟩γ_2 has class ≤ 2 and ISS finishes. So the obstruction is exactly
  "find v_1", as the note says.
* Several layers (copy i Fourier-sampled over its own N_i), non-invertible endomorphisms in
  place of automorphisms, and success "up to a character of HN that is trivial on N". The
  step-1/2/3 arguments apply copy by copy. An endomorphism that is scalar on L/N has κ ∈ {0,1}
  (κ = κ²), so its weight on N ∩ [L,L] is 0 or 1. The conclusion of T′(b) uses only the phase
  on N ∩ [L,L]. So all three stay within binary weights, but I only **argued** this; it is
  not written out as a proof.

## 2. The proof, step by step

* **Step 1 (N central).** Correct as mathematics. ψ_u(a)·h^r n = (phase)·ψ_{u∘Ad_h^r}, and
  ker(Ad_h^r − 1)|_N = ker(ad_η|_N) for r ≢ 0. Also r ≢ 0, because α(N) = N and h ∉ N. The
  distinct cosets aHn are orthogonal because H ∩ N = 1. The eigen-probability
  p^{−rank} is over a uniform u (Lemma 4). Confirmed at the level of explicit states, with
  the group law given by BCH (check S).
  **Defect F1:** the hypothesis "> 1/p for each nontrivially twisted copy" can be met by a
  non-central N. Take fil4, N = γ_2 = ⟨x_3,x_4⟩ (abelian, not central), [L,N] = ⟨x_4⟩. Keep a
  copy only if u(x_4) = 0. You can see this when you measure, and it happens with
  probability 1/p. Every kept copy is then an eigenvector for every h, with probability 1.
  Such copies are just ISS states for G/Z. The correct bound counts copies:
  P[success] ≤ 1/p + n·p^{−dim[L,N]}.
* **Step 2 (scalar on L/N).** Correct when the twist is fixed. Moving the support is fatal,
  because aHN·g = aHN iff g ∈ HN. A linear map that preserves every line is a scalar. And
  ᾱ is F_p-linear (Lazard, c < p).
  **Defect F2:** with label-dependent or random twists, "α must preserve every line" does not
  follow. A random twist that is κ = 1 with probability ½ and non-scalar otherwise preserves
  every HN with probability ≥ ½ > 1/p, yet it uses a twist with μ ≠ 1 half the time. The
  repair is the averaging bound in T′(b).
* **Step 3 (κ = 1, identity on [L,L]).** Correct: κ[x,y] = κ²[x,y] when [L,L] ⊄ N, and
  [x+n, y+n′] = [x,y] when N is central. There is no characteristic issue for p > c ≥ 3.
  **Defect F3:** "μ_α = 1 on N ∩ [L,L]" says nothing when N ∩ [L,L] = 0, and in that case μ
  on N is arbitrary. In fil4⊕F_p with N = ⟨e_5⟩, the line-preserving automorphisms realize
  μ ∈ {1,2,3,4} (C1). The case does no harm: L = L′ ⊕ N, so G = G′ × N. But the conclusion
  should be stated on N ∩ [L,L], and "only binary weights" only for that part.
* There is no hidden use of grading. The characteristically nilpotent 7-dimensional algebra
  over F_7 (class 6, every derivation nilpotent, so no grading) behaves as predicted (C1).

## 3. Repaired statement (proved)

**Proposition T′.** Let L be a nilpotent Lie algebra over F_p of class c, 3 ≤ c < p, and
G = exp(L). Fix, independently of H, an abelian ideal 0 ≠ N ≠ L. A *template run* does the
following:

1. It prepares n states ψ_{u_i}(a_i) = Σ_{x∈N} ω^{−u_i(x)}|a_iHx⟩ with u_i uniform in N^*.
2. It chooses twists τ_i ∈ Aut(G) ∪ {φ_0}, not all φ_0, as functions of the labels and of
   coins, but not of H.
3. It outputs Ψ_g = ⊗_i ψ_{u_i}(a_i)·τ_i(g).

The run *succeeds* for H if Ψ_{gk} = Ψ_g for all g ∈ G and k ∈ HN. Let h = exp(η).

(a) Suppose N is not central and h is uniform on G∖N. Then
P[success] ≤ 1/p + n·p^{−dim[L,N]}.

(b) Suppose N is central, and h is uniform on G∖[G,G]N. Then
P[success and some used τ_i is nontrivial on N∩[L,L]] ≤ 1/p. Moreover, every successful run
whose used twists are all trivial on N∩[L,L] satisfies Σ_{i used} u_i|_{N∩[L,L]} = 0, a
binary zero-sum.

The bound 1/p in (b) is attained by the line count on filiform4 at p = 5 and 7.

*Proof.* (a) Success requires the first used copy i* to be an eigenvector, which means
u_{i*}∘ad_η|_N = 0. Suppose u does not vanish on [L,N]. Then {η : u([η,N]) = 0} is a proper
subspace containing N. So, over η ∉ N, the probability is < 1/p. Labels that do vanish on
[L,N] occur among the n copies with probability ≤ n·p^{−dim[L,N]}.

(b) Let τ be a used twist that is nontrivial on [L,L]. By steps 2–3, τ̄ is non-scalar on
V = L/N. Success requires τ̄ to preserve the line of η̄ ∉ D = [V,V]. The lemma below gives the
bound for fixed labels, and then we average. The binary statement holds because
ψ·τ(x) = ω^{u(x)}ψ for x ∈ N∩[L,L].

**Lemma (counting lines).** Let D = [V,V] ≠ 0 and T ∈ GL(V) with T(D) = D and T
non-scalar. Then at most a fraction 1/p of the lines of V outside D are T-invariant.

*Proof.* Let k = dim V/D, and let π: V → V/D be the projection. For each eigenvalue λ, write
E_λ for the λ-eigenspace of T and g_λ = dim π(E_λ). The invariant vectors outside D number
Σ_λ |E_λ∩D|(p^{g_λ} − 1), out of |D|(p^k − 1). At most one λ has E_λ ⊇ D.

* If T̄ (the map T induces on V/D) is a scalar, then either |E_λ∩D| ≤ |D|/p or
  g_λ ≤ k−1. Either way the fraction is ≤ 1/p.
* Otherwise the fraction is at most [p^{g_1} − 1 + (p^{k−g_1} − 1)/p]/(p^k − 1) with
  g_1 ≤ k − 1. This is convex in g_1 and equals 1/p at both ends. ∎

Check C2b agrees exactly: the maximum fraction is 1/p for fil4 at p = 5 and 7, and 1/6 < 1/5
for fil5 at p = 5. For heis3, where the class is 2 and the lemma does not apply, it is 1/3.

## 4. Exact checks (`2026-11-12-rees-direct-twist-class3-referee/`; numbers are mine, independent of the note's scripts)

| check | result |
|---|---|
| S: explicit BCH-group states, all abelian ideals N, random h, a, sampled α ∈ Aut preserving N, all u: is ψ_u(a)·α(h) ∝ ψ_u(a) iff [α(h) ∈ HN and u∘ad_η\|_N = 0]? Also the N-phase ω^{u(αn)} | 0 mismatches in every case: heis3 p=5,7 (8370, 21546 cases), fil4 p=5,7 (8370, 21546), free23 p=5 (9720; 8 abelian ideals), fil5 p=5, class 4 (8370). The N-phase checks (2.4k–6.4k cases each) also have 0 mismatches |
| C1: every automorphism that is a scalar κ mod a central N (linear algebra, all central N) | heis3: κ ∈ F_5^*, acts on Z by κ² (class 2, so ISS is fine). fil4 p=5,7, free23 p=5 (all 7 central N), fil5 p=5, charnil7 p=7: only κ = 1, and it is the identity on [L,L]. fil4⊕F_p: N ∩ [L,L] = 0 gives μ ∈ {1..4}; N = Z gives non-scalar action on N |
| C2: exhaustive Aut, central N: automorphisms that preserve every line of L/N and are nontrivial on N∩[L,L] | heis3: 50 (p=5), 196 (p=7). fil4 p=5,7, fil5 p=5, and free23 p=5 (all 7 central N; 7.5·10^6 automorphisms for N = Z): 0 |
| C2: maximum fraction of lines preserved by a twist that is nontrivial on N∩[L,L]; LP for the best H-independent mixture (worst line) | fil4: 7/31 and 9/57 (= ρ), LP = 1/5 and 1/7 exactly. free23 p=5: ρ attained, LP = 1/5 exactly for every central N. fil5: 0.077, LP = 1/25 |
| C3: non-central abelian N: max over u ∉ [L,N]^⊥ of P_{η∉N}[u∘ad_η\|_N = 0] | below 1/p in every case (fil4 p=5: 1/6; p=7: 1/8; free23: 1/6; fil5, fil4⊕F_p: 6/31) |

Counterexamples found: none to T′, and none to the core algebraic claim. F1 and F2 show that
the note's *wording* fails, not its mathematics.

## 5. Literature

Prop T is not in the local corpus as a theorem. The closest locator is I–I arXiv:2304.08376,
§1, the "Related results" paragraph, page 4. It says that in class two one can twist by
automorphisms that "do not change the hidden subgroup too much", and that such automorphisms
"do not exist in general nilpotent groups of class greater than two". There is no definition
and no proof. The mechanism itself is ISS §2.3 Prop 1 and §4 Lemma 5. Fair attribution:
"a precise form of a remark of Imran and Ivanyos". It should not be claimed as a new obstruction.

## 6. Paper remark (fair statement)

> **Remark (proved).** Let G = exp(L) have class c with 3 ≤ c < p. Consider the
> Ivanyos–Sanselme–Santha template, in which:
>
> * the abelian normal subgroup N is fixed in advance;
> * each copy is Fourier-sampled over N;
> * each copy's right action is twisted by an automorphism or dropped, chosen from the
>   measured labels but not from H;
> * the target is HN.
>
> Unless N is central, the template succeeds with probability at most 1/p + n·p^{−dim[L,N]}
> on a random cyclic H. If N is central, then except with probability at most 1/p over a
> random cyclic H ⊄ [G,G]N, every successful run twists only by automorphisms that fix
> N ∩ [L,L] pointwise. Cancellation on N ∩ [L,L] is then exactly the binary zero-sum
> condition of Imran and Ivanyos. This makes precise their remark that the class-two twists
> do not exist beyond class two. It does not exclude non-abelian Fourier steps, twists that
> depend on H, or adaptive schemes.

For the note itself:

* Replace the "probability > 1/p for each nontrivially twisted copy" hypothesis with T′.
* State the conclusion for the twists used, on N ∩ [L,L].
* Drop "A acts on N by scalars".
* Allow φ_0 explicitly.
* Add "H ⊄ [G,G]N" as the hard case.
