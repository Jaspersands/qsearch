# Can adaptive, entangled twist schemes avoid the Rees cover? An impossibility attempt (2026-11-12)

**Status: AI-checked, pending human review.** One AI session did the derivations (adversarial brief:
try to prove that cover-free twist schemes cannot work). The finite checks are exact or explicitly
sampled, and they only falsify (TRAPS 7). Scripts and outputs are in
`research/audits/reviews/2026-11-12-rees-entangled-twist-impossibility/`. No paper, STATE, handoff
or reductions file was edited. Context read: STATE.md "Now" (iii) and (v); `main-core.tex`
§1.2, §3.3–3.4, §4.1–4.2, §7.2; `2026-11-12-rees-direct-twist-class3.md` (Prop T) and its referee
(T′ and the line-counting lemma); `2026-11-12-rees-adaptive-twist.md` (Prop C, Lemma E).

## Verdict

1. **REFUTED: impossibility in the literal model.** In the model "k coset copies, any channel
   built from public operations plus adaptively chosen automorphisms", the Rees cover algorithm is
   itself a polynomial-time member: Lemma copy-lift uses only public controlled right
   multiplications. Ettinger–Høyer–Knill (EHK) give O(log²|G| + log 1/ε) copies for any group. So
   no copy lower bound holds there, and no impossibility statement in that model can be true.
2. **REFUTED: copy lower bounds even in the narrowest twist model.** Take the source-only model
   SOT_bin below, which uses identity twists only. With unbounded classical post-processing, it
   solves the hard cyclic HSP in every class-3 Lazard group satisfying (Z), free23 and
   Dixmier–Lister (DL) included. It needs poly(m, log p, log 1/ε) copies (Prop B).
3. **PROVED: shadow reduction (Theorem R), for every class-3 Lazard group with (Z).**
   * Setting: the source-only automorphism-twist model SOT(Aut), defined in §1. It allows
     adaptive choices, merges that entangle copies through a shared address register, twists by
     automorphisms of central quotients of G, restrictions and abelian Fourier sampling.
   * Claim: any SOT(Aut) algorithm that finds a uniformly random hard cyclic H yields a classical
     algorithm. That algorithm has no quantum resources and no access to H. Its running time is
     the same up to poly(m, log p, #operations). It finds a nonempty **binary zero-sum** among
     i.i.d. uniform vectors of F_p^{dim γ_3}, with probability at least
     P[success] − (#promotions + #restrictions)/(p−1) − 1/#hard H.
   * Converse (Prop R′, proved): when dim γ_2/γ_3 ≤ dim γ_3 (free23, DL), a zero-sum finder gives
     an SOT(Aut) algorithm.
   * So within SOT(Aut), free23 and DL are exactly as hard as the random zero-sum problem
     ZS(p, 2, n), up to polynomial factors.
   * Adaptivity and H-dependent twists buy nothing. Before the first H-dependent outcome, the
     transcript is independent of H. A twist that is not the identity on V = L/γ_3 is useful only on
     a "guess" event of probability ≤ 1/p (Lemma F).
4. **PROVED (corollary): a barrier.** Under P = NP, SOT(Aut) solves free23 and DL in polynomial
   time. So an unconditional super-polynomial lower bound in SOT(Aut) would prove P ≠ NP.
5. **CONDITIONAL.** Suppose ZS(p, 2, poly(log p)) has no poly(log p)-time solver with
   non-negligible success. We know of none; generalized-birthday and sieve methods suggest
   2^{O(√log p)}, which we did not verify. Then no polynomial-time SOT(Aut) algorithm finds hard
   cyclic H in free23, DL, or the filiform fil4. **Calibration:** fil4 is solved in polynomial time
   outside SOT, by Ivanyos–Santha (IS) Cor 8 and by the cover. The conditional statement therefore
   restricts a *method class*, not the problem.
6. **What a working cover-free scheme must look like (§8).** It must leave SOT(Aut). There are
   three exits:
   * a merge address group that is not a section of G. The cover is this case: a subgroup
     Γ ≅ G̃ of G^c of order p^{Σ dim γ_k} > |G|;
   * a measurement of a label-carrying register on a non-abelian frame (HPGP-type, as IS Cor 8);
   * a polynomial zero-sum solver.

   For free23 the second exit is the open "HPGP along an unknown line". **UNKNOWN.**

## 1. Models

Throughout, G = exp(L) is a Lazard group of class exactly 3, with p > 3. Write
V = L/γ_3, D = γ_2/γ_3 = [V,V], g = dim γ_3 and d = dim D. A cyclic H = ⟨exp η⟩ is *hard* if
η ∉ γ_2. Then H ∩ γ_2 = 1 and K := Hγ_3 is abelian, and K̄ = K/γ_3 is a line of V outside D. We
use one hypothesis:

**(Z)** Z(G/N) = γ_3/N for every N ⊊ γ_3.

(Z) holds for free23, where every quotient by a line is fil4. It holds for fil4, where γ_3 is
1-dimensional. It holds for DL at every p > 3:
* if x = ae_5 + be_6 ≠ 0, then [x, L] = γ_3;
* if x ∉ γ_2, then [x, L] ⊄ γ_3, by the e_1, …, e_4 brackets mod γ_3.

GAP confirms dim Z(DL/Z′) = 1 for all lines at p = 5, 7.

**M_full.** The algorithm may request copies of ρ_H and apply any quantum channel. It contains EHK
and the Rees cover.

**SOT(Aut): source-only automorphism-twist model.** The algorithm holds registers. Each register
has a public *frame* Q, which is a section M/N of G, and a state on ℂ[Q]. Every choice is an
arbitrary classical function of all earlier outcomes and coins. The operations are:

* (O1) a fresh copy ρ_H, with frame G;
* (O2) the complete central instrument (core Lemma instrument) for a public Z ≤ Z(Q);
* (O3) *merge*. Choose registers R_i with frames Q/N_i, where N_i ≤ Z(Q), and twists
  φ_i = π_i∘α_i with α_i ∈ Aut(Q) and π_i: Q → Q/N_i. Prepare the uniform address superposition
  on Q. Apply the controlled right action R_{φ_i(q)} to R_i, then trace out the R_i. A dropped
  copy is simply not an input. This is the twisted diagonal action of ISS, with entanglement
  through the shared address;
* (O4) *promotion*. If R_zρ = ρ for all z in a public central Z ≤ Q, re-encode ρ on Q/Z;
* (O5) *restriction*. Measure the left coset of a public subgroup M ≥ γ_3(Q), and translate it
  into M;
* (O6) abelian Fourier sampling of a register whose frame is abelian.

ISS class 2 (Thm 4) appears to fit this model: central labels over G′, dilation twists, dropping,
Fourier sampling of HG′-invariant states, restriction to HG′. This is argued from the
direct-twist note's summary of ISS; ISS was not re-read. Imran–Ivanyos binary conversion fits. The
core's descent has this form with frame G̃ instead of G. Its section-address conversion (address
over Q = G/Z through a section σ) equals "merge on G, then O4" exactly when the labels cancel. SOT_bin
is SOT(Aut) with α_i = id.

**Excluded by definition** (the referee's sharpening):
* tracing out the central coordinates of a register in a section;
* the core's section address when the labels do *not* cancel;
* right-coset restriction;
* public ancilla registers as merge inputs (if allowed, count each as a restriction in r).

The first two are cheap public operations, and they produce exactly the cocycle-twisted states
Σ_t ω^{P(t)}|q + t v_1⟩ on V. So the excluded exit (ii) of §8 is reachable with public
polynomial-time operations. The model's boundary is the *measurement* of such states, not their
preparation.

| procedure | in M_full | in SOT(Aut) | why |
|---|---|---|---|
| Rees cover (copy-lift + descent) | yes | **no** | its frame G̃ is not a section of G. As a merge on G^c, its address group is Γ = {(E_{s_1}(a),…,E_{s_c}(a))}, of order p^{Σ dim γ_k} > \|G\|, so Γ is not the graph of any tuple of maps G → G |
| EHK (O(log²\|G\|) copies, exponential time) | yes | no (joint measurement) | Prop B gives an in-model substitute with polylog copies |
| binary descent + brute-force zero-sum | yes | yes | Prop B |
| IS Cor 8 / HPGP (fil4) | yes | **no** | measures label-carrying states on a non-abelian frame |
| twists by endomorphisms (det A = 0), anti-automorphisms, Fourier over a non-central N | — | not included | §10 |

## 2. Barrier results

**Prop A (proved).** The Rees algorithm is in M_full with polynomially many copies (core Lemma
copy-lift and Thm main). Any lower bound claimed for "public operations plus adaptive
automorphisms on coset copies" is therefore false.

**Prop B (proved).** Let G be class 3 with (Z), and let H be hard cyclic. In SOT_bin with
unbounded classical computation, H is found with error ε from O(n² (m + log 1/ε)) copies, where
n = max(g, d)⌈log₂ p⌉ + ⌈log₂(1/δ)⌉ + 1 and δ is constant.

*Proof.* There are three steps.
1. **Zero-sums exist.** Let X count the nonempty S ⊆ [n] with Σ_S λ_i = 0. Distinct nonempty 0/1
   vectors are F_p-independent, so the sums Σ_S λ are pairwise independent and uniform. Hence
   Var X ≤ EX = (2^n − 1)/p^g. Chebyshev gives P[X = 0] ≤ p^g/(2^n − 1) ≤ δ.
2. **One merge makes a source.** Merge the copies in S with identity twists and promote along
   γ_3. By Lemma T, the result has type (K, χ) with χ(hz) = ω^{Σλ_i(z)} = 1. It is exactly the
   coset state of K̄ on V.
3. **Finish.**
   * Repeat with fresh copies to get the sources.
   * On V, binary-descend along D. D is central in V for every class-3 group, and the labels are
     uniform on F_p^d. Fourier sampling of L/γ_2 then gives the line of v_1.
   * Restrict raw copies to M = exp(F_p v_1 + γ_2), which contains γ_3 and has class ≤ 2 with
     [M,M] ⊆ γ_3. A binary descent along γ_3 inside M gives K. Restricting to the abelian K and
     Fourier sampling gives H.

The brute-force search costs about p^g/δ classical time per merge. ∎

So copy counts cannot separate anything here. Exact check (`zerosum.out`): P[no zero-sum] for
F_5, F_7, F_5² at every n up to the Davenport constant g(p−1)+1. Every value is below the
Chebyshev bound whenever that bound is below 1; for example, F_5², n = 7 gives 0.0029 ≤ 0.197.

## 3. Lemma F (fixed hard lines; proved)

**Lemma F.** Let V be a nilpotent Lie algebra over F_p with D = [V,V] ≠ 0. Let T ∈ Aut(V) with
T ≠ id. Then at most a fraction 1/p of the lines of V outside D are T-invariant. For
V = heis_3 the bound is attained, by p+1 of the p²+p lines.

*Proof.*
* T is not a scalar. If T = κ·id, then T acts on D by κ², because D is spanned by brackets. So
  κ = κ² and T = id.
* The rest is the referee's line-counting lemma (direct-twist referee, §3), which holds for any
  T ∈ GL(V) with T(D) = D that is not a scalar. We re-derived its multi-eigenvalue case.
  * Write e_κ, f_κ and g_κ for dim E_κ, dim(E_κ∩D) and e_κ − f_κ. Then Σf ≤ d and Σg ≤ k, where
    k = dim V/D, because (⊕E_κ) ∩ D = ⊕(E_κ∩D).
  * The number of invariant vectors outside D is Σ p^{f_κ}(p^{g_κ}−1).
  * Suppose at least two terms are nonzero. Putting all of f on the largest term and using
    (p^a−1)+(p^b−1) ≤ p^{a+b}−1, the count is at most φ(g_1) = p^d(p^{g_1}−1) + p^{k−g_1} − 1.
    This is convex in g_1. Both endpoints are ≤ p^{d−1}(p^k−1), with difference
    (p^d−1)(p^{k−1}−p) + (p−1)(p^{d−1}−1) ≥ 0 at g_1 = 1.
  * Suppose exactly one term is nonzero. Since T is not a scalar, (f, g) ≠ (d, k), and
    p^f(p^g−1) ≤ p^{d−1}(p^k−1). ∎

For 2-generator class 3 (free23 and fil4), the fixed hard lines of T ≠ id have a simple form:
1. they lie on ≤ 2 lines of v_1 (eigenlines of A = T|_{V/D}); or
2. they are the p+1 lines of one plane W with W ∩ D = 0 (when A = κI with κ ≠ 1).

Either way, the "hint" is computable from T in polynomial time. Exhaustive check (`fix_lemma.out`,
p = 5, 7):
* every V-image of Aut(free23) (12000 and 98784 of them) and of Aut(free23/Z′) for all p+1 lines Z′;
* the maximum fixed count is p+1 (6 and 8);
* violations of the ≤ p+1 bound: 0. Violations of the structure: 0;
* "T = id_V but nontrivial on the top layer": 0.

Sampled check on Aut(DL) and Aut(DL/Z′) for every line, 150 random elements each
(`dl_fix_sample.out`): the fixed fraction never exceeds 1/p.

## 4. Type calculus (Lemma T; proved)

Write ρ_{S,χ} = |Q|^{-1} Σ_{g,g′} 1_S(g′^{-1}g) χ(g′^{-1}g)|g⟩⟨g′|, for S ≤ Q and χ a linear
character of S. This is the uniform mixture of the twisted coset states |aS,χ⟩.

* **Raw copies.** ρ_H = ρ_{H,1}. O2 on γ_3 gives a label λ uniform on (F_p^g)^* (H ∩ γ_3 = 1),
  and type (K, χ_λ) with χ_λ(hz) = ω^{λ(z)} (core Lemma central).
* **O3.** The output is ρ_{S,χ} with S = ∩φ_i^{-1}(S_i) and χ = Π χ_i∘φ_i. Indeed
  ⟨g|ρ|g′⟩ = |Q|^{-1} Π_i tr(ρ_i R_{φ_i(g′^{-1}g)}), and the φ_i are homomorphisms.
* **O4 and O5.** O4 gives (S/Z, χ̄). O5 has a uniform outcome, because ρ_{S,χ} is
  left-invariant. It leaves type (S∩M, χ|) on M.
* **Top-layer bookkeeping.** Let B: V^{⊗3} → γ_3 be the map x⊗y⊗w ↦ [x̃,[ỹ,w̃]]. It is
  well defined and onto, because γ_3 is central, [γ_2, γ_2] = 0 and [L, γ_3] = 0. For a register
  on frame G/N, write ẑ := (χ|_{γ_3/N}) ∘ B_N. For α ∈ Aut(G/N) with V-map T, we have
  α_top∘B_N = B_N∘T^{⊗3}. By induction, every register built only from labelled copies by O3 and
  O4 satisfies

  S̄ = ∩_j P_j^{-1}(K̄) and ẑ = Σ_j λ_j∘B∘P_j^{⊗3}.

  Here j runs over the raw ancestors, and P_j ∈ Aut(V) is the product of the twists' V-maps along
  the path, P_j = T^{(1)}∘…∘T^{(m)}. T^{(1)} belongs to the first merge on the path and T^{(m)} to
  the last, so the latest merge's twist acts first. **No lifting of quotient automorphisms to
  Aut(G) is needed.** This matters for DL, whose quotients have non-lifting automorphisms (§7).

  *Scope:* (P_j, ẑ, S̄) does not determine the type. The character on the H-part of S is not
  tracked. For example, central automorphisms x ↦ x·f(x̄) add ISS-style correction phases there.
  This is harmless for Theorem R: those phases change χ only on S̄, and they matter only after
  γ_3 has been crossed.

**Lemma D (deferred labels; proved).** WLOG, O2 on all of γ_3 follows every O1 immediately. Every
SOT operation on a raw copy commutes with R_z for z ∈ γ_3:
* controlled right actions commute with R_z;
* O5 commutes because M ⊇ γ_3;
* the copy is traced out at its merge.

An O4 or O6 that is legal for the mixture is legal on each branch: the PSD components of a state
supported on the R_Z-fixed subspace are supported there.

## 5. Theorem R and its converse

Call a register **binary** if all its P_j are equal, to P say. Then S̄ = P^{-1}K̄ ≠ 0. Call a
register **dead** if its type is H-independent, for instance S̄ = 0.

**Theorem R (proved).**
* Setting: G is class 3 with (Z), and H is uniform over the hard cyclic subgroups. A is an
  SOT(Aut) algorithm with N copies, π promotions, r restrictions and success probability ε.
* Claim: there is a classical randomized B, with no access to H. B draws N i.i.d. uniform
  vectors of F_p^g. It runs in time t_A + poly(N, π, r, m, log p), where (O6) is Fourier sampling.
  It outputs a nonempty S with Σ_S λ_i = 0 with probability at least

  ε − (π + r)/(p−1) − 1/h(G), where h(G) is the number of hard cyclic subgroups.

*Proof.*
1. **Simulation.** B simulates A with simulated labels. It tracks every type symbolically through
   (P_j, ẑ, S̄ as "P^{-1}K̄ or 0"), and samples the outcomes of dead registers exactly. All of
   these are linear algebra over F_p.
2. **Which outcomes depend on H.** Under (Z), a register with S̄ ≠ 0 has frame G/N, N ⊆ γ_3, with
   frame centre γ_3/N.
   * O2 outcomes are then deterministic, and O5 outcomes are uniform.
   * O6 needs an abelian frame. On the way, all of γ_3 and then D must be promoted.
   * By Lemma T, promoting the last part of γ_3 requires ẑ = 0.
3. **Binary case.** If the register is binary, then ẑ = (Σ_j λ_j)∘B∘P^{⊗3}. P is invertible and
   B is onto, so ẑ = 0 forces Σ_j λ_j = 0. Raw copies are consumed once, so the ancestors form a
   set, and B outputs it.
4. **Non-binary case.** If the register is not binary, then S̄ ≠ 0 forces K̄ ∈ Fix(P_1P_j^{-1})
   for some P_1P_j^{-1} ≠ id. P_1P_j^{-1} is a function of the H-independent past, and K̄ is
   uniform over the hard lines. By Lemma F this event has probability ≤ 1/p. The event is fixed
   at the merge; we charge it at the full-γ_3 promotion of that register.
5. **Restrictions.** An O5 produces an H-dependent register only if P^{-1}K̄ lies in M/γ_3,
   which is a proper subspace of V when M ≠ Q (recall M ⊇ γ_3). Hard lines inside a proper
   subspace form a fraction ≤ 1/p (≤ 1/(p−1) is used for safety). Otherwise the register is dead.
6. **Coupling.** Merging a dead register with any register gives a dead register. Define the bad
   events (a binary crossing, a Fix event at a non-binary crossing, a live restriction) in B's
   *ideal* H-independent process, in which K̄ stays uniform. The true run and the ideal run are
   identical until the first bad event. Every outcome before it is H-independent. If no bad
   event occurs, A's output is independent of H, so it is correct with probability ≤ 1/h(G). ∎

**Prop R′ (proved; converse).** Assume d ≤ g, as in free23 (d = 1, g = 2) and DL (d = g = 2).
Let C find a nonempty zero-sum among n i.i.d. uniform vectors of F_p^g with probability ≥ 1/2,
in time t. Then SOT_bin finds every hard cyclic H with error ε. It uses O(n² · poly(m, log 1/ε))
copies and time poly(m, log p, log 1/ε)·t.

*Proof.* Run Prop B's pipeline with C in place of brute force. Every call to C gets fresh labels;
leftovers are conditioned on C's choice. Descending D in V needs zero-sums in F_p^d. Padding each
label with g−d uniform coordinates turns C into a solver for that. ∎

**Corollary (barrier; proved).**
* Suppose P = NP. Draw n = 2⌈log₂ p⌉ + 4 labels. A zero-sum then exists with probability ≥ 15/16,
  and an NP-search oracle finds it in poly(log p) time.
* So, by Prop R′, SOT(Aut) solves free23 and DL in polynomial time.
* Hence an unconditional super-polynomial time lower bound for SOT(Aut) on these groups would
  prove P ≠ NP.
* Copy lower bounds are already false (Prop B).

**Conditional theorem.** If ZS(p, 2, poly(log p)) has no poly(log p)-time solver with success
1/poly, then no poly-time SOT(Aut) algorithm solves the hard cyclic HSP in free23, DL or fil4.
Theorem R needs only N and π + r = poly(log p) ≪ p.

For fil4, g = 1, so Theorem R gives a ZS(p, 1) solver. ZS(p, 1) easy implies ZS(p, 2) easy, with
about n² samples. To see this, solve the first coordinate on disjoint blocks. Each chosen subset
depends only on first coordinates, so its second-coordinate sum is uniform. Then solve ZS(p, 1) on
those sums.

## 6. The "[L,L]-coordinates" form, made precise

In SOT(Aut), a twist that is not the identity on V is useful only if K̄ ∈ Fix(T). By Lemma F,
Fix(T) is at most a 1/p fraction of the hard lines. For 2-generator groups it is ≤ 2 lines of
v_1, or one plane W. A useful twist therefore *encodes* log₂ p − O(1) bits about K̄, including the
D-coordinate of η, which is the [L,L]-coordinate at grade 2.

Theorem R shows that before the first binary zero-sum crossing, the transcript carries **zero**
information about H. So the adaptive escape left open by the adaptive-twist note ("T′ does not
bound what failed runs leak") is closed inside SOT(Aut): failed runs leak nothing. This also
subsumes that note's Lemma E: a non-binary relative twist is just a guess. It also subsumes its
Prop C: the "learn Hγ_c first" step has no in-model source of information.

## 7. Dixmier–Lister specifics (finite checks; `dl_aut_5_7.out`)

| p | \|Aut(DL)\| | image on γ_3 | scalars | Aut(DL/Z′) on the centre, over the p+1 lines Z′ |
|---|---|---|---|---|
| 5 | 4·5^12 | order 4 | ±1 | 5 lines: {±1}; one line (e_7+4e_8): all of F_5^× |
| 7 | 12·7^12 | order 12 | ±1 | all 8 lines: all of F_7^× |

* The first three columns agree with core prop:dl-central-scalars.
* **New:** the "±1 only" property is *not inherited by quotients*. Automorphisms of DL/Z′ scale
  its centre by every element of F_7^×, and these automorphisms do not lift to Aut(DL).
* This does not create an escape. Lemma F and the B_N-bookkeeping apply to every automorphism of
  every frame.
* For SOT(Aut) the DL-specific scalar fact is therefore *not* the obstruction. The obstruction is
  Lemma F, which holds for every class-3 group. The paper's prop:dl-central-scalars is correct as
  stated, since it concerns Aut(G) itself.
* `dl_aut_11.out` (p = 11, Aut(DL) only, 3000 s cap) was still running at writing. It is not
  needed for any claim.

## 8. What a working cover-free scheme must look like

A polynomial algorithm for hard cyclic H in free23 or DL that avoids the cover must do at least
one of the following.

* **(i) Use a merge address group outside the sections of G.** The cover's copy-lift is a merge
  over Γ ≅ G̃ ≤ G^c of order p^{Σ_k dim γ_k} (p^{10} vs p^5 for free23). Whether smaller
  non-graph Γ ≤ G^k suffice is open.
* **(ii) Measure a label-carrying register on a non-abelian frame,** that is, an HPGP or
  pretty-good-measurement step. IS Cor 8 does exactly this for fil4. For free23 the candidate is
  the state Σ_t ω^{P(t)}|q_a + t v_1⟩ along an unknown line (Prop C(c)). Preparing it is cheap
  and public: trace the central coordinates of a labelled copy in a section. Whether it can be
  measured usefully is **UNKNOWN**.
* **(iii) Use twists outside the model,** such as non-surjective endomorphisms or
  anti-automorphisms. This is argued not to help (§10), but it is not proved.
* **(iv) Solve ZS(p, 2, poly log p) in polynomial time.** That would also make the Imran–Ivanyos
  binary route polynomial.

## 9. Finite checks (exact unless marked sampled)

| script → output | what | result |
|---|---|---|
| `fix_lemma.py` → `fix_lemma.out` | Lemma F and the hint structure, free23 and all quotients free23/Z′, p = 5, 7, exhaustive over the V-images of Aut | max fix = p+1; 0 bound, structure or "T=id ⇒ top=id" failures |
| `merge_check.py` → `merge_check.out` | explicit BCH states, free23: F_λ(g) = ⟨ψ\|R_gψ⟩ vs 1_K χ_λ; (A) binary zero-sum merge = 1_K; (B) ρ ∉ Stab(K) ⇒ support γ_3, same F for another H; (C) ρ ∈ Stab(K), T ≠ id ⇒ support K, character Σλ_i∘C_i; (D) informative ⇔ K̄ ∈ Fix(T) | p = 5: 72 twist trials, 36 informative; p = 7: 36 trials, 19 informative; every mismatch counter 0; max informative fraction 1/p |
| `zerosum.py` → `zerosum.out` | exact P[no zero-sum] in F_5, F_7, F_5² | consistent with Chebyshev; reaches 0 exactly at Davenport g(p−1)+1 |
| `dl_aut.py` → `dl_aut_5_7.out` | GAP/autpgrp Aut(DL), Aut(DL/Z′), image on the centre (generators re-verified as Lie automorphisms) | table §7 |
| `dl_fix_sample.py` → `dl_fix_sample.out` | Lemma F on DL and DL/Z′ (sampled, 150 each) | max fraction ≤ 1/p in all 16 groups |

## 10. Adversarial self-check

* **Independent AI referee** (subagent, adversarial; no counterexample found): verdict CORRECT
  WITH FIXES.
  * Lemma F correct; it needs only T(D) = D, T non-scalar, and is re-checked on 24,820 random
    block-triangular matrices.
  * Lemma T correct, with the order and scope fixes now applied.
  * Lemma D correct.
  * Theorem R correct within the model, with the charging and coupling wording fixed.
  * Prop B: n now uses max(g, d). Prop R′: the copy count is now n².
  * fil4 needs the ZS(p,1) ⇒ ZS(p,2) step, now added.
  * The model's exclusions are now listed.
  * Attacks tried, all failing: partial central instruments; non-lifting fil4/DL quotient twists;
    dead-register merges; H-part correction phases; abelian restrictions; a live register as
    address; keeping and labelling targets.
* **Is the model a strawman?** It contains ISS (class 2), the Imran–Ivanyos binary conversion,
  the core's descent run on G, adaptivity, and entanglement through shared addresses. It
  excludes exactly the two known polynomial escapes, the cover (i) and HPGP (ii), and it
  says so. Calibration with fil4 shows that the theorem cannot be read as hardness of the problem.
* **Does it exclude generic exponential algorithms?** No: brute-force zero-sum is inside
  (Prop B). EHK is outside, but its role, few copies, is reproduced inside.
* **The weakest points.**
  * (Z) and the restriction O5 ⊇ γ_3 are used. Without (Z), extra central directions enlarge
    S̄. Without M ⊇ γ_3, Lemma D fails. The raw-copy case of O5 with M ⊉ γ_3 reduces to
    P[H ≤ M] < 1/p (argued, not written in full).
  * O6 is restricted to Fourier sampling, so that B is efficient. Arbitrary POVMs on abelian
    frames keep the information statement but not B's running time.
  * Non-surjective twists. A singular endomorphism acts on γ_3 by 0 (free23: det(A)A). In the
    examples checked, it only yields guess events (e.g. τ^{-1}(K) = G iff the image line lies in
    K). Not proved in general.
  * Anti-automorphisms (inversion) turn right cosets into left cosets of conjugates aKa^{-1} with
    random a. A mixed left/right merge is then invariant only under the core of K. Argued, not
    proved.
  * Fourier over non-central abelian N (route A) is not in SOT. Lemma E covers single twisted
    copies only.
  * Lemma F's general proof was re-derived here. The constant 1/(p−1) in Theorem R absorbs the
    1/p of Lemma F.
* **Could the theorem be vacuous?** Theorem R is information-theoretic about H and does not
  bound B's success. Its force rests entirely on ZS hardness, which is open. I tried to find a
  poly(log p) zero-sum method for F_p² (lattice: dimension n, det p², a 0/1 vector needed,
  LLL/BKZ far off; collisions need weight −1, which requires an H-dependent twist). I found none,
  which is not evidence of hardness.
* **Novelty.** The reduction of the top layer to zero-sums is the Imran–Ivanyos observation, in
  model form. Lemma F is the referee's line-counting lemma. What is new is the closure under
  adaptivity and merges, the B_N bookkeeping (which allows non-lifting quotient twists), the
  converse, and the P ≠ NP barrier. Their priority is unchecked.

## 11. Claim gates (stay false)

* "The cover is necessary for graded (or DL) groups."
* "Twist methods are impossible beyond class 2."
* Any unconditional lower bound.
* "ZS is hard."

The paper may say, if the integrator wants: within source-only automorphism-twist descent on G,
the top layer of every class-3 Lazard group reduces to finding binary zero-sums of random labels
(conditional and model-bound; AI-checked).

**Next hard question.** For free23 with hard cyclic H: is there a poly(log p)-time measurement on
poly(log p) labelled copies ψ_λ (exit (ii)) that outputs the line of v_1? For example, an IS
HPGP′-style algorithm for Σ_t ω^{λ∘C_a(t)}|Q_a(t)⟩, whose phase is quadratic in t, on
G/γ_3 = heis_3. Or is there a proof that every measurement in a natural label-carrying class
reduces to ZS?
* **Next command:** `nice -n 19 /opt/anaconda3/bin/python hpgp_free23.py 5 7` (to be written).
* **Expected artifact:** the exact output distribution of IS's HPGP′ measurement applied to φ_λ(a)
  on heis_3, and the mutual information with v_1 per copy.
* **Acceptance test:** the information per copy is Ω(1/poly(log p)) with an efficiently invertible
  likelihood, which would make exit (ii) viable; or it is ≤ p^{−Ω(1)}, which would close the simple
  versions of exit (ii).

## Reproduce (from this note's folder)

```
nice -n 19 /opt/anaconda3/bin/python fix_lemma.py   > fix_lemma.out      # ~1 min
nice -n 19 /opt/anaconda3/bin/python merge_check.py > merge_check.out    # ~2 min
nice -n 19 /opt/anaconda3/bin/python zerosum.py     > zerosum.out        # ~1 min
nice -n 19 /opt/anaconda3/bin/python dl_aut.py 5 7  > dl_aut_5_7.out     # GAP, ~10 min, caches gap/*.json
nice -n 19 /opt/anaconda3/bin/python dl_fix_sample.py > dl_fix_sample.out  # needs gap/*.json
```

Acceptance:
* every failure or mismatch counter is 0;
* max fixed fraction ≤ 1/p;
* the DL table matches §7.
