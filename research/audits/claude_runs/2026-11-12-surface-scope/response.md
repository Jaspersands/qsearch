# Source/scope audit: does Saxena–Venkatesh give a uniform classical polylog p algorithm for all smooth quintic surfaces over F_p?

## Verdict

**The cheapest attack is decisive: the quantifier.** The supplied sources prove a fixed-X statement. They do not prove a uniform polylog p classical algorithm for the native family:

> all smooth quintic surfaces X ⊂ P³ over F_p, input of size O(log p), output exact P₂ of degree 53.

Canonical integer lifting does make every native input an instance of the paper's hypotheses. The issue is what happens to the hidden constants:

- The only explicit height input the paper cites is Javanpeykar's Theorem 6.0.4/6.0.6 (= surfaces Theorem B.5). After substitution it gives Faltings-height bounds polynomial in **p**, with exponent about 10¹⁵⁰ (Theorem 6.0.4). The route through Theorem 6.0.6/B.5 is worse: the exponent itself grows like log log p.
- Several other proof steps have unstated dependence on X.

So the classical counterpart that actually follows for the native family is still the trivial p^{O(1)} kind. This is an **insufficient upper bound, not an impossibility**. Uniform classical polylog p for this family remains OPEN. Nothing here supports or refutes a quantum/classical separation.

## 1. Fixed-X quantifier (source text)

The surfaces paper is explicit:

- §1.1: "Let X ⊂ P^N be a **fixed** smooth, projective, geometrically integral … surface … We assume X is obtained via good reduction of a nice surface 𝒳 over a number field K at a prime p ⊂ O_K."
- Theorem 5.1: "Let 𝒳 be a **fixed**, nice surface of degree D defined over a number field K. Then … (ii) on input a prime p ⊂ O_K of good reduction … outputs the zeta function … in time poly(log q)."
- §1.2: "this work solves the above question in the case dim X = 2, when X is nice, **at large enough primes of good reduction**."
- Conclusion: "dependence of the total complexity on the degree of the surface which is, at the moment, exponential."

The paper is silent on dependence on the height of 𝒳. The complexity lemmas only claim "bounded by polynomial functions of ℓ and log q" (§6 preamble: "We do not deduce the exact complexities beyond showing that they are bounded by polynomial functions of ℓ and log q").

Three consequences:

- Theorem 5.1(ii) is a family-over-primes statement for one global surface.
- The polynomial's coefficients and degree may depend on 𝒳 (K, equations, heights). The proof never controls that dependence.
- The native problem changes 𝒳 with every input. So Theorem 5.1 cannot be invoked as a black box. Uniformity requires re-tracing every constant as a function of h(𝒳).

## 2. Canonical lift: what does go through

Let f ∈ F_p[x₀..x₃]₅ be smooth. Lift it to f̃ ∈ Z[x] with coefficients in [0,p), or in (−p/2, p/2).

**Proved (standard).** The hypersurface 𝒳 = V(f̃) ⊂ P³_{Z₍ₚ₎} has these properties:
- It is flat, since f̃ ≢ 0 mod p.
- It is proper with smooth closed fibre.
- The non-smooth locus is closed. Its image in Spec Z₍ₚ₎ is closed and misses the closed point, so it is empty.

Hence 𝒳_Q is a nice quintic over K = Q with good reduction at p, and every native input satisfies the paper's hypotheses. The coefficient height is h(f̃) ≤ log p.

**Invariants for d = 5** (standard Lefschetz bookkeeping; verify in repo):
- b₂ = d³ − 4d² + 6d − 2 = 53, and b₁ = 0. So P₁ = P₃ = 1 and deg P₂ = 53, consistent with the task.
- Generic hyperplane section: a plane quintic of genus 6, so M = F_η has dimension 12 and M'' = H¹(𝒳, μ_ℓ) = 0.
- Number of singular fibres of a Lefschetz pencil = class = d(d−1)² = 80. Check: χ(X̃) = 55 + 5 = 60 = 2·(−10) + #Z.
- If ∞ is not critical, B = Z is Galois-stable, so Javanpeykar's N equals #Z = 80.
- Monodromy (as quoted from [KV25, Thm 13] in Theorem 4.1): G = Sp(E_η) = Sp₁₂(F_ℓ). So deg j = |G| < ℓ⁷⁸.

**CRT range.** |coeff_k P₂| ≤ C(53,k)·p^k, so ∏ℓ > 2^{54}p^{53} suffices. That is O(log p / log log p) primes ℓ = O(log p), with a constant depending only on 53. This part is uniform.

**Branch-locus height (upper bound only).**
- The critical values are roots of a discriminant-type polynomial D(t) ∈ Z[t] of degree 80.
- For the pencil chosen with small-coordinate axis, its coefficients are integer forms of degree O(1) (depending only on d = 5) in the coefficients of f̃. So log‖D‖ ≤ k log p + O(1), with k = O(1).
- Mahler's inequality gives h(z) ≤ log M(D) ≤ k log p + O(1) for every z ∈ Z.
- Therefore h_B = O(log p) and **H_B = exp(h_B) ≤ C·p^k**.

I do not claim a lower bound on H_B for most inputs (see §6 for heuristic evidence only).

## 3. Explicit parameter substitution

Write E := 45·N³·2^{N−2}·N! with N = 80:
- 45·80³ = 2.304·10⁷
- 2⁷⁸ ≈ 3.02·10²³
- 80! ≈ 7.16·10¹¹⁸

So **E ≈ 5·10¹⁴⁹**.

### Javanpeykar Theorem 6.0.4 (equivalently 1.3.1 with X = P¹, B_f = ∅, f = id, deg f = 1)

Source:

> "c_B := (4N H_B)^{45N³2^{N−2}N!} … h_Fal(Y) ≤ 13·10⁶ g c_B (deg f)⁵(deg π)⁵"

and §1.3:

> "H_B = max{H(α)} … H(α) = (∏_v max(1,‖α‖_v))^{1/[K:Q]}"

So H_B is the **exponential** (multiplicative) height.

Substitution:
- Y = Ṽ, deg π = deg j ≤ |Sp₁₂(F_ℓ)| < ℓ⁷⁸.
- Riemann–Hurwitz gives g ≤ N·deg π.

Then

  h_Fal(Ṽ) ≤ 13·10⁶·80·c_B·(deg π)⁶ ≤ 1.04·10⁹ · ℓ⁴⁶⁸ · (320·H_B)^E,

and

  log c_B = E·(log 320 + h_B) ≤ 5·10¹⁴⁹·(5.77 + k log p + O(1)).

Hence **h_Fal(Ṽ) ≤ poly(ℓ) · p^{O(E)}**: polynomial in p, exponential in the input length log p. The same c_B appears in the δ_Fal bound the surfaces paper cites in Thm 4.5 item 2 ("[Jav14, Theorem 6.0.4]").

### Javanpeykar Theorem 6.0.6 / surfaces Theorem B.5

Source (Jav):

> "a = 6 + log(13·10⁶ N (4N H_B)^{45N³2^{N−2}N!})"

Surfaces B.5 transcribes this as

> "a = 6 + log(13·10⁶ A·(4AB)^{45A³2^{A−2}A!}) where A is the number of elements in the orbit of Z … and B is a bound for the height of the elements of Z."

The transcription is faithful **only if B means the exponential height H_B**. Then

  a = 6 + log(1.04·10⁹) + E·(log 320 + h_B) = Θ(E·log p) (upper bound),

and the stated bound

  (deg π)^a ≤ exp(78·log ℓ · a) = exp(O(E · log p · log log p)) = p^{O(E log log p)}.

This is **strictly weaker than 6.0.4**. In 6.0.4, c_B is a multiplicative factor. In 6.0.6, log c_B multiplies log deg π.

The surfaces paper's Thm 4.5 item 1 uses this weaker form:

> "the Faltings height h_F(Ṽ) … is bounded above by deg(j)^a, where the quantity a is independent of ℓ."

That is true for fixed 𝒳. For the native family, a = Θ(E log p).

### H_B vs h_B (the misreading trap)

B.5's phrase "a bound for the height" is ambiguous inside a paper whose Definition B.1 defines the logarithmic Weil height h. If one plugs in h_B ≈ k log p:

  a ≈ E·log(320·k log p),  (deg π)^a = exp(O(E·(log log p)²)) = (log p)^{O(E log log p)}.

This is a misreading: Javanpeykar's H_B is exponential. Even the misread value is super-polylog, with a constant of order 10¹⁵⁰ in the exponent. So **neither reading yields uniform polylog p**.

### Propagation to runtime (upper-bound chain only)

- Theorem 4.5 turns these into h(D_x) bounds.
- Lemma 6.7 Step 6 sets Mascot precision e from those heights. Theorem 4.4 cost is Õ(poly(g'·log #F_P·e·ℓ^s)).
- Here s = dim E. By Theorem 4.1, (E⊗M)^G has dimension b₂ − 2 = 51 and M is 12-dimensional self-dual, so s should be about 12·51 = 612. Treat this as an estimate; the paper only says "independent of ℓ".
- The output polynomial has ℓ^s roots with heights at least ℓ^s-scaled.

With bit-precision e ≳ h(D_x) and h_Fal ≤ poly(ℓ)·c_B, the best runtime upper bound derivable from the sources for the native family is **p^{Θ(E)}·poly(ℓ)**. Rigorously, this says only that the available upper bound is p^{O(E)}. It does not show the algorithm needs that much.

## 4. Is there a sharper already-stated bound in the supplied sources?

Three candidates exist; none is uniform polylog.

**1. Theorem 6.0.4 / 1.3.1 vs 6.0.6.**
- 6.0.4 is sharper: exponent 5 in deg π (6 after g ≤ N deg π), and linear in c_B.
- But c_B = (4N H_B)^E is still p^{Θ(E)} under the upper bound on H_B.
- The surfaces paper should cite 6.0.4/1.3.1 rather than 6.0.6 in any uniformity analysis. It does not change the conclusion.

**2. Theorem 1.1.1 (Belyi degree).** Source: "h_Fal(X) ≤ 13·10⁶ g deg_B(X)⁵."
- This is the real underlying statement.
- c_B enters only through Khadjavi: "deg R ≤ (4N H_B)^{9N³2^{N−2}N!}".
- A uniform polylog route would need a Belyi map R with R(Z) ⊂ {0,1,∞} and deg R ≤ poly(h_B), with N = 80 fixed, for every native Z.
- Javanpeykar points to "better bounds when B is contained in P¹(Q)" ([28], [26 Thm 1.1.b]). Z is generically not in P¹(Q), and those bounds are not quoted. So no such bound is stated in the supplied text.
- **Obligation (unsupplied):** deg_B(Z) ≤ F(N)·poly(h_B).

**3. Remark 6.0.5 (Bilu–Strambi).** Source: "Although their bound on the naive height is exponential in the degree, the dependence on the height of the branch locus in their result is logarithmic."
- Here deg π ≈ ℓ⁷⁸ ≈ (log p)⁷⁸.
- "Exponential in the degree" gives exp(poly(log p)). That is worse than polylog, and the remark does not state it for Faltings height or for the CE11 9.1.3 terms.

**Speculation, not a theorem.** Javanpeykar writes: "It should be possible to avoid the use of Belyi's theorem and improve the dependence on the branch locus in Theorem 6.0.4. This is not necessary for our present purposes." This is not a stated uniform bound.

**Other X-dependent terms with no stated height dependence:**
- CE11 Thm 9.1.3 item 4: integral ∫ log(1+|j̃|²)μ, stated only as "bounded by a polynomial in ℓ".
- Item 5: intersection numbers, via Wilms Props 1, 2.
- Theorem B.4's constant depends on "N, g, D" unspecified, polynomial only in the last three items.
- The B.4 "Remark" extension to K(t) heights (Moriwaki) is stated without proof.

Even if Javanpeykar's dependence were made logarithmic in H_B, each of these would still need an explicit poly(ℓ, h(𝒳)) bound.

## 5. Auxiliary-prime and arithmetic-action issues under the native lift

**(a) Auxiliary prime P = O(ℓ) (Alg 9 Step 5).** Requirements:
- Good reduction of 𝒳.
- The same number of singular fibres mod P. Source remark: "Provided P is large enough compared to the data of the surface, there is an equality between the number of singular fibres…"
- Good reduction of Ṽ (genus about ℓ⁷⁸).

For the native lift, the bad primes include divisors of disc(D) ≈ p^{O(1)}. That is up to O(log p / log log p) distinct primes, the same order as the number of primes below cℓ when ℓ ≈ log p. So "P = O(ℓ)" with an absolute constant is not guaranteed.

Counting repairs this: some P ≤ C'·log p avoids those divisors, with C' depending on k. That is still polylog, so this item is likely repairable.

Good reduction of Ṽ at P is a separate gap, for fixed 𝒳 as well. G = Sp₁₂(F_ℓ) has order ℓ³⁶∏_{i≤6}(ℓ^{2i}−1), and primes P = O(ℓ) can divide it. The standard sufficient criterion for good reduction (P ∤ |G| and no branch-point coalescence) is then unavailable. The paper offers no argument. **Obligation:** exhibit P = poly(log p) at which Ṽ (or the relevant Jacobian piece) has good reduction, with an efficient test.

**(b) "Large enough primes".** §1.2 restricts to "large enough primes of good reduction". Theorem 5.1(ii) says only "of good reduction". If any threshold C(𝒳) is needed, then for the native lift C(𝒳) depends on h(𝒳) ≈ log p and could exceed p. The paper does not state such a threshold explicitly. **Obligation:** confirm that no hidden threshold exists, or show C(𝒳) < p uniformly.

**(c) Frobenius at p via [DD13].** The Galois action factors through K'' of degree poly(ℓ). The defining polynomial's coefficients have height on the scale of §3's bounds, so even reading them costs the p^{O(E)} upper bound under current estimates. One also needs p-integrality and p ∤ index/discriminant of the chosen polynomial, or a Tschirnhaus fix. p is exactly the lifting prime, a non-generic choice. For fixed 𝒳 the paper's "large enough" covers this; natively it is an unstated obligation, probably repairable.

**(d) Coefficient twist.** H¹(Ṽ, μ_ℓ) ⊗ R¹π_*μ_ℓ carries μ_ℓ^{⊗2}. Theorem 4.1 and Alg 9 Step 8 must untwist consistently to recover P₂ mod ℓ: eigenvalues scale by p^{±1} mod ℓ. This is a bookkeeping obligation, not an error claim. It is harmless if tracked, but wrong exponents silently corrupt the CRT output.

**(e) Lefschetz pencil choice (Step 1, "polynomial time").** The bad axes form a proper closed subset of fixed degree, so a random small-height axis works with high probability. This is plausibly uniform.

## 6. Can small-height lifts rescue uniformity? (heuristic only)

Count hypersurface lifts up to scaling and PGL₄ with coefficient height ≤ p^ε. There are at most p^{56ε} forms, covering at most p^{56ε+16} of the roughly p⁵⁶ quintic forms mod p. So for ε < 40/56, most inputs have no such lift with small coefficients.

This does **not** lower-bound h_B for the critical values, and it does not exclude non-hypersurface models. It only shows "pick a cleverer lift" is not a free fix.

## 7. Narrow mathematical points (fixed-X)

**(i) Javanpeykar 6.0.6 proof, small degree.** The step

  13·10⁶ g c_B (deg π)⁵ ≤ (deg π)^{1+log(13·10⁶ N c_B)}

(after g ≤ N deg π) needs C ≤ C^{log deg π}, i.e. deg π ≥ e (natural log), i.e. deg π ≥ 3.
- For deg π = 2 with g ≥ 1 (a hyperelliptic double cover branched inside B, when N ≥ 4), the displayed derivation does not yield (deg π)^a.
- The bound is likely still true numerically, since 2^a is astronomically large. This is a proof gap, not a counterexample.
- Repair: use log₂, or take a = 6 + ⌈log₂(13·10⁶ N c_B)⌉. "Integers a" also needs a ceiling.
- Irrelevant to the surfaces paper, where deg π ≈ ℓ⁷⁸.

**(ii) Surfaces Thm 4.1.** "H^i(G,M) = 0 for 1 ≤ i ≤ 2, as … the centre has order 2 and acts non-trivially on M′". The center-kills argument handles M′ only. It does not apply to the trivial summand M'' ≅ H¹(𝒳, μ_ℓ), on which the center acts trivially. Vanishing there needs H^i(Sp, F_ℓ) = 0 for i = 1, 2 (perfectness and Schur multiplier), which presumably holds for large ℓ. Repairable. For the quintic, b₁ = 0, so M'' = 0 and it is irrelevant here.

**(iii) Lemma 4.2.** The bound J = poly(ℓ) is argued through GL(H²) of fixed rank 53. The Frobenius order on E_P should be bounded through the normalizer of G and the multiplicity space, not H² alone. Both are fixed-rank over F_ℓ, so the conclusion survives. The exponent (≥ 53) makes "poly(ℓ)" degree-heavy but still polylog p.

None of these falsifies the fixed-X theorem as stated. I make no claim that the paper is false.

## 8. What classical counterpart actually follows for the native family

**Proved/unconditional from standard facts.** P₂ is determined by #X(F_{p^k}) for k ≤ 53 (fewer via the functional equation), through Newton identities, since P₁ = P₃ = 1. Brute-force enumeration of P³(F_{p^k}) gives a deterministic p^{O(1)} algorithm. The surfaces paper itself says the p-adic algorithms (Lauder–Wan, Harvey) have "runtime exponential in log p". So the established native classical cost is exp(O(log p)), i.e. p^{O(1)} for fixed degree.

**From Saxena–Venkatesh plus Javanpeykar as stated:**
- Per-instance correctness after canonical lift: yes, modulo §5(a)–(d).
- Uniform runtime upper bound derivable from cited explicit bounds: poly(ℓ)·p^{O(E)} with E ≈ 5·10¹⁴⁹ via Theorem 6.0.4. Via 6.0.6/B.5 it is p^{O(E log log p)}.
- Polylog p: **not established**.

**Not established in either direction:** classical hardness, a lower bound, or that the actual algorithm is slow on native inputs. The gap is entirely in upper-bound bookkeeping. A sharper Arakelov or Belyi bound could close it.

## 9. Proof obligations to upgrade to uniform classical polylog p (each currently OPEN)

- **O1.** h_Fal(Ṽ), δ_Fal(Ṽ), ‖ϑ‖, and the CE11 9.1.3 terms (integral, intersection numbers) bounded by poly(ℓ, h(𝒳)), with N = 80 fixed. The cleanest route is deg_B(Z ∪ …) ≤ F(80)·poly(h_B) fed into Jav Thm 1.1.1; Khadjavi gives H_B^{Θ(E/5)} instead.
- **O2.** Theorem B.4 constants polynomial in h(𝒳), including the unstated N, g, D dependence and the K(t)/Moriwaki extension.
- **O3.** Auxiliary prime P ≤ poly(log p) with good reduction of 𝒳 and Ṽ and equal critical-fibre count, efficiently certifiable (§5a).
- **O4.** No "large enough p" threshold, or one below p uniformly (§5b).
- **O5.** DD13 Frobenius identification with poly(log p) cost given coefficient heights from O1; p-integrality and index handled (§5c).
- **O6.** Twist bookkeeping recovering P₂ mod ℓ exactly (§5d).
- **O7.** Lefschetz pencil and primitive-element data of height poly(ℓ, log p), uniformly.

## 10. Falsifiers

**Falsifiers of "the existing theorem already gives native polylog":**
- Any repo text that invokes Theorem 1.1/5.1 for the native family without O1–O7.
- Substituting h_B for H_B in B.5.
- Treating "a independent of ℓ" as "a independent of 𝒳".

All three are present risks. Classify such text as unsupported.

**Would falsify the "insufficient" verdict:** an explicit statement in a cited source giving h_Fal of G-covers of P¹ branched at N fixed points as poly(deg π, h_B). Neither supplied excerpt contains one. Bilu–Strambi as summarized is exponential in degree.

**Would falsify OPEN status toward possibility:** a written proof of O1–O7, or an alternative uniform algorithm. Either upgrades the classical side to polylog and removes any separation narrative.

**Finite controls** (e.g., running small p) cannot decide either direction. Constants ~10¹⁵⁰ are not observable, and agreement on small p only checks transcription.

## 11. Recommended STATE wording

"Native all-quintic P₂: Saxena–Venkatesh Theorem 5.1 is fixed-𝒳. Canonical lifting satisfies its hypotheses but the cited explicit height inputs (Javanpeykar 6.0.4/6.0.6 via Khadjavi–Belyi, c_B = (4N·H_B)^{45N³2^{N−2}N!}, N = 80, H_B ≤ p^{O(1)} exponential height) give only p^{O(10¹⁵⁰)} bounds. Uniform classical polylog p is OPEN (obligations O1–O7). No hardness, no separation."

Also keep the repo's quantum construction labeled "no separation claim". This audit gives no lower bound against classical.