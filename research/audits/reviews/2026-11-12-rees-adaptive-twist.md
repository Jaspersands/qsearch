# Does an adaptive (H-dependent) ISS twist bypass the cover for graded L? (2026-11-12)

**Status: AI-checked, pending human review.** One AI session did the derivations. The finite
checks are exact (exhaustive or explicit-state), but they only falsify (TRAPS 7). Scripts and
outputs are in `research/audits/reviews/2026-11-12-rees-adaptive-twist/`. No `.tex` file was
edited. Context read: STATE.md lines 1296–1365, TRAPS.md, `2026-11-12-rees-direct-twist-class3.md`
(Prop T), its referee (T′), `class3-example/example_free.tex`, ISS arXiv:0707.1260 §2.3, §3
(Thm 2, Algorithm 1), §4 (Thms 3–4, Lemmas 4–6), and IS arXiv:1503.09016 §1 and §4.1.

## Verdict

**The proposed top-down adaptive scheme (i)→(ii)→(iii) is not an algorithm: it is circular
(Proposition C, proved).** Step (i) assumes an oracle for G/γ_c that f does not provide. Building
one is equivalent to solving the whole problem when |H| = p. Once K = Hγ_c is known, steps (ii)
and (iii) are unnecessary: K is abelian and one abelian HSP inside K gives H.

The verdict is neither (A) nor (B). E1 and E2 in general remain **(C) UNKNOWN**, but sharper than
before:

* **(ii) is never the obstruction in the tested cases.** In every graded algebra tested (32
  algebras of class 3 and 4, dimensions 4–8; 71 algebra–prime pairs at p = 5 and 7), Stab_Aut(G)(K) contains
  automorphisms that act on γ_c by every dilation scalar θ^c. This holds for every K = Hγ_c, and
  for dim ≤ 6 it holds for Stab(H) itself, for every cyclic H. So **no (B) example** appears: the
  scalers always exist, but you need to know H to find them.
* **The useful information is the whole problem.** At class 3 the only consistent adaptive
  order is bottom-up. Learning the image of H in G/γ_2 already finishes the job, by ISS inside
  exp(F_p v_1 + γ_2). For free23, the partial information that unlocks any twist is exactly
  characterized (exhaustive, p = 5, 7). Each such piece is about log p bits that no known
  primitive extracts.
* **E2.** I prove that every twist, H-dependent or not, and every coarse label measurement
  leaves route A's permuted-label failure in place (Lemma E). Strong Fourier sampling over G
  yields a state that can be an Hγ_2-eigenvector with probability **exactly 1/p** (free23,
  p = 5, 7, 8 hard H). Entangled multi-register measurements are not excluded.

**Consequence for the paper's novelty claim:** it is unaffected, and it can now be stated
sharply. What the cover supplies is exactly the quotient oracle that step (i) lacks. The dilations
preserve H̃Z_c for every homogeneous H̃, so the descent manufactures sources for G̃/Z_c without
knowing K. The paper should still not claim that the cover is *necessary* for graded L: E1 and E2
in full generality are UNKNOWN (TRAPS 8).

## 1. Proposition C (circularity; proved)

Let G = exp(L) have class c, with 2 ≤ c < p. Let H = ⟨h⟩, h = exp(η), |H| = p, and K = Hγ_c.

(a) *K known ⇒ H in polynomial time.* γ_c is central and h has order p. So
(t, z) ↦ k_0^t z, for any known k_0 ∈ K∖γ_c, is an isomorphism F_p × γ_c → K. The restriction
f|_K hides H, and abelian Fourier sampling on K ≅ F_p^{1+d_c} returns H with
O(d_c + log 1/ε) queries. (If η ∈ γ_c, then K = γ_c and the same holds.)

(b) *A twist in Stab(K) outputs only K.* The ISS template with N = γ_c and twists τ_i ∈ Stab(K)
gives a hiding set for HN = K (ISS Lemma 6). It can never hide a group that does not contain N,
because ψ_u(a)·n = ω^{u(n)}ψ_u(a).

(c) *Step (i) is as hard as the problem.* Solving the HSP "in G/γ_c" requires a hiding procedure
for K/γ_c, and f does not give one: f is not constant on γ_c-cosets. After the γ_c-label λ is
measured, |aH⟩ leaves φ_λ(a) = p^{-1/2} Σ_t ω^{λ(C_a(t))}|Q_a(t)⟩ on G/γ_c, where
a h^t = exp(Q_a(t) + C_a(t)) and λ∘C_a is a polynomial in t of degree ≤ 2 (class 3). Its fidelity
with the coset state |aK/γ_c⟩ is 1, 0 or 1/p, according as λ∘C_a is constant, linear or
quadratic. Averaged over the uniform label, it lies between 1/p and 0.36 at p = 5, and between
1/7 and 0.27 at p = 7 (exact; 1032/1032 cases match the prediction). By (a), any hiding
procedure for K yields H, and conversely. At c = 2 this procedure is exactly ISS Thm 4, which
uses the public twists that exist only in class 2 (Prop T′).

So step (i) needs (iii), (iii) needs (ii), (ii) needs K, and K is the output of (i). ∎

The cover avoids the circle because its twists are public: every dilation of 𝒜 preserves
H̃Z_c for every homogeneous H̃.

### Bottom-up adaptivity is the only consistent order

At class 3, M = exp(F_p v_1 + γ_2) has class ≤ 2, because [M,M] ⊆ γ_3. Given the line of v_1,
ISS solves the HSP in M with f|_M (polynomial, with ISS's query count). So at class 3,
**E1 succeeds iff some direct method learns the line of v_1**. That is the open core named in the
direct-twist note (an HPGP along an unknown line, for free23). At class c > 3 the same step drops
the class by one, and the core problem recurs at each level. The quotient M need not stay graded:
M is a subgroup of class ≤ c−1, not necessarily of gradable type. I did not test this.

### Which partial information unlocks a twist (free23, exhaustive)

`partial_info.py` enumerates the image of Aut(free23) on (L/γ_3, γ_3): order |GL_2|p², which is
12000 at p = 5 and 98784 at p = 7. Each candidate family F of K's is tested for a common
stabilizing element that acts nontrivially on γ_3:

| family F | p = 5 | p = 7 |
|---|---|---|
| a single K | 30/30 have one | 56/56 |
| all K with a given v_1-line | 6/6 | 8/8 |
| any two K with distinct v_1-lines | 375/375 | 1372/1372 |
| three K with distinct v_1-lines | 500/2500; **0 mismatches** with "coplanar in L/γ_3" | 2744/19208; 0 mismatches |
| all K (Prop T) | none | none |

So a twist exists for F exactly when F has at most two v_1-lines, or when F lies in one plane
W ⊂ L/γ_3 complementary to γ_2/γ_3. In the second case, W is a degree-one space of a new Carnot
grading of the free algebra, and its dilations work. Either kind of information is Θ(log p)
bits (a line among p+1, or a plane among p²). Guessing it costs poly(p), which is exponential in
log p. No primitive that extracts it is known. The first round of any adaptive scheme is
H-independent, so T′ bounds its success at hiding HN. T′ does **not** bound the information
that failed runs leak. That gap is exactly what is left UNKNOWN.

## 2. Step (ii), exhaustively: do H-preserving central scalers exist?

`auts_gap.py` builds the Lazard group (pc presentation from BCH) and calls GAP/autpgrp. It
converts each generator back to a Lie automorphism and checks it is one (every generator passed).
|Aut| matches the known values: fil4 has 50000 and 605052 automorphisms at p = 5 and 7;
free23 has |GL_2|p^6. `stab_scalers.py` computes, from Schreier generators, the exact image of
Stab(K) on γ_c for every line of L/γ_c. For m ≤ 6 it also computes Stab(H) for every line of L.
Every scaler reported is a product of verified automorphisms, so each existence claim is sound
even if GAP's generators missed part of Aut.

Algebras: fil4, free23 (= L5,9), fil4⊕F, L5,5 (degrees 1,1,2,2,3, not Carnot), L5,9⊕F,
L4,3⊕F², L4,3⊕L3,2, the 6-dimensional class-3 algebras L6,10, L6,19(ε), L6,20, L6,23(0),
L6,24(ε), L6,25 and L5,5⊕F, two Jacobi-valid variants V6,23(ε), two 7-dimensional Carnot
algebras N7a and N7b. Class 4: L5,6 (degrees 1,…,5), L5,7, L6,11, L6,12, L6,13, L6,21(ε),
L5,6⊕F, L5,7⊕F, and free24 (dim 8). **Caveat:** LieAlgDB is not installed. I wrote down the
de Graaf tables from memory and checked each with Jacobi. The ε ≠ 0 members of L6,23 as I
recalled them fail Jacobi, so I replaced them with a variant. Completeness against the source is
NOT checked.

Result (`stab_scalers.out`, `free24.out`):

* For **every** hard K (v_1 ≠ 0) in every algebra at p = 5 and 7, Stab(K) acts on γ_c by every
  dilation scalar θ^c. The same holds for every hard H, for m ≤ 6.
  `hard_missing_dilation_scalars = 0` throughout. Altogether this covers about 0.55M hard H and
  0.14M hard K, counted over the 71 algebra–prime pairs (free23, L55, L56 and L57 also appear as L5,9, L5,5, L5,6 and L5,7, so they are counted
  twice).
* Uninformative cases: at p = 5 and class 4, θ⁴ ≡ 1, so dilations give only {1}. For free24 at
  p = 5 the scalar set is {1}, as expected. At p = 7 free24 gives {1, 2, 4} for all 2744 hard K.

So there is **no graded (L, K) without suitable α** in this list. Outcome (B) does not appear.
The class-3 example's remark ("the stabilizer of every subgroup acts on the centre by every
cube") extends to every algebra tested. Whether this holds for all positively graded L is open.
A natural conjecture is that every cyclic H is Aut-conjugate to a subgroup stable under some
torus with the dilation weights on γ_c. I did not attempt a proof.

**Cost of (ii).** For free nilpotent L, ψ_θ = φδ_θφ^{-1} is explicit: φ(x) = v. In general,
finding such an α means finding φ with φ(K_0) = K for a torus-stable K_0. That is an orbit
problem for Aut(G), of p-group-isomorphism flavour. It is not known to be polynomial, and the
GAP computations here are not polynomial-time algorithms.

## 3. The ISS correction when α moves H by a central element (exact)

Let α ∈ Stab(K). Then α(η) = rη + ζ_α with ζ_α ∈ γ_c, so α(h) = h^r·exp(ζ_α). This gives

  ψ_u(a)·α(h^t z) = ω^{t·u(ζ_α) + u(αz)} ψ_u(a).

From K alone, write η = η̄ + η_c with η̄ known and η_c ∈ γ_c unknown. Then
ζ_α = known_α + (A_α − r)η_c, where A_α = α|_{γ_c}. Hence the K-only system

  Σ A_iu_i = 0,  Σ r_iu_i = 0,  Σ u_i(known_i) = 0

makes the product constant on K. `twist_known_K.py` checks this on fil4 and free23 at p = 5 and
7 (explicit BCH states, four hard H each):

| check | result |
|---|---|
| single-copy phases | 0 mismatches in 12384 cases |
| the decomposition of ζ_α | 0 mismatches |
| multi-copy invariance vs the exact condition | 0 mismatches in 4800 cases |
| solutions of the K-only system | 3018 found, all invariant on K |
| support | the resulting hiding set hides exactly K (16/16) |

So the analysis is right. Its output is the K that was its input.

## 4. H not cyclic; interaction with ISS Thm 2

ISS Algorithm 1 calls the order-≤ p solver P on subgroups of N_G(H̃)/H̃, for intermediate
H̃ ≤ H. Its final call is made in N_G(H)/H. Graded Lazard groups are not closed under quotients.
Every class-3 algebra on k generators is a quotient of the free one F_{k,3}, which is graded. Take
G = exp(F_{4,3}) and H = exp(I) with F_{4,3}/I ≅ L_DL. Then H is normal, and P must run on the
non-gradable Dixmier–Lister group, whose centre scalars are only ±1 (prop:dl-central-scalars).
So for arbitrary H in a graded G, any direct method routed through Thm 2 must handle non-graded
groups, and gradedness buys nothing there (argued from the ISS text). The cover treats arbitrary
H with no reduction. With K known but H not cyclic, f|_K hides H in K, and K has the class of H,
so no reduction occurs in general.

## 5. E2: non-abelian or coarse Fourier steps over a non-central N

**Lemma E (proved).** Let N be an abelian normal subgroup, η ∉ log N, and H ∩ N = 1. Let τ be
any automorphism with τ(HN) = HN, H-dependent or not. Every ψ in span{ψ_u(a) : u ∈ N^*} that
is an eigenvector of the right action of τ(HN) is proportional to a single ψ_u with
u∘ad_η|_N = 0. This covers any coarse or irrep-level measurement of the N-label.

*Proof.* τ permutes HN, so the condition is HN-eigen. N acts on ψ_u by the distinct characters
ω^{u(·)}, so an N-eigenvector is a single ψ_u. And ψ_u·h = ψ_{u∘Ad_h}, with
ker(Ad_h − 1)|_N = ker ad_η|_N for c < p. ∎

So route A fails for every twist, adaptive or not, with probability ≥ 1 − p^{-rank ad_η|N} per
copy. Combined with the tensor lemma, products need every copy to be eigen. This extends T′(a)
to H-dependent twists.

**Strong Fourier sampling over G** (`e2_strong_fourier.py`, GAP character tables). This is the
probability that the measured irrep σ of free23 admits *any* Hγ_2-eigenvector, i.e. that χ_σ|_{Hγ_2}
has a linear constituent. It equals **1/p exactly** for 4/4 hard H at p = 5 and 4/4 at p = 7,
matching the Mackey prediction:

* σ|_{Hγ_2} is reducible iff the central character λ satisfies λ([v_1, γ_2]) = 0;
* that event has mass (p−1)/p², and λ = 0 has mass 1/p².

**An observation (argued, not checked):** if Hγ_2-eigenstates were available, *public*
dilations would suffice, because δ_θ(Hγ_2) = Hγ_2 for every H. The correction would then be
linear in the unknown (v_2, v_3) with coefficients polynomial in θ, giving fixed-degree diagonal
equations. So in E2 the obstruction is the 1/p eigenstate yield, not the twist. Detecting the
good copies would reveal the line ℓ_λ = ℓ, which is the goal itself.

Entangled multi-register measurements (Clebsch–Gordan or sieve, Kuperberg-style) are not
excluded. That is the general HSP problem, and it stays UNKNOWN.

## 6. Literature (local folder only; not exhaustive)

* Neither (A) nor (B) appears. No local text uses twists that depend on H for nilpotent class
  ≥ 3.
* Closest:
  * Imran–Ivanyos (2304.08376 §1) remark that the class-2 automorphisms "do not exist in general"
    beyond class 2.
  * ISS Thm 3, the "HG′ known ⇒ H" step, is Prop C(a) at c = 2.
  * The general pattern "learn part of H, then restrict" is ISS Algorithm 1, and also the
    hidden-Borel and hidden-parabolic iterations in 1105.4416 and 1406.6511.
* "Adaptive" in 1509.05806 concerns abelian hypergroups, which is unrelated.

## 7. For the paper (integrator; nothing inserted)

Suggested sentence: "One might first learn Hγ_c(G) and then twist by automorphisms stabilizing
it. Such automorphisms exist in every graded example we checked, but finding Hγ_c is itself
the problem. A hiding procedure for Hγ_c already yields H, and the oracle supplies none.
The dilations of the cover preserve the lifted subgroup for every H, and so build that
procedure without knowing it."

Keep "We do not claim that the cover is necessary for graded L."

## Reproduce (from this folder's parent)

```
cd research/audits/reviews/2026-11-12-rees-adaptive-twist
nice -n 19 /opt/anaconda3/bin/python alg.py                 # BCH associativity self-test
nice -n 19 /opt/anaconda3/bin/python auts_gap.py            # GAP/autpgrp, ~5 min; caches auts/*.json
nice -n 19 /opt/anaconda3/bin/python stab_scalers.py > stab_scalers.out    # ~10 min
nice -n 19 /opt/anaconda3/bin/python twist_known_K.py > twist_known_K.out  # ~40 s
nice -n 19 /opt/anaconda3/bin/python partial_info.py > partial_info.out    # ~10 s
nice -n 19 /opt/anaconda3/bin/python e2_strong_fourier.py   # GAP character tables, ~5 min
```

Acceptance criteria:

* `hard_missing_dilation_scalars` = 0 in every row;
* every mismatch counter in `twist_known_K.out` is 0, and `Konly_invariant` = `Konly_solutions`;
* `triples_pred_mismatch` = 0;
* every `e2_free23_*.gout` line reads `eigen_possible 1/p`.

**Next hard question:** for free23 with |H| = p, can a direct method extract Θ(log p) bits about
v_1 (or about a complement W ∋ v) from polynomially many coset states? This could be done by
entangled measurements or by the HPGP route along an unknown line. A yes would give an
adaptive direct algorithm for this graded group. A no needs a lower-bound technique that is
not in hand.
