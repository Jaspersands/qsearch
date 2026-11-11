# Does the ISS class-two twist work directly for graded class 3? (2026-11-12)

**Status: AI-checked, pending human review.** The derivations are by one AI session. The
finite checks are exact (they are not samples), but they only falsify (TRAPS 7). Scripts and
outputs are in `research/audits/reviews/2026-11-12-rees-direct-twist-class3/`. No `.tex` file
was edited.

**Verdict: OBSTRUCTION FOUND for the ISS twist template. Whether any direct method works is
UNKNOWN.** Positive grading does not rescue the Ivanyos–Sanselme–Santha (ISS) mechanism at class 3.
Proposition T below shows the following. Suppose the template's abelian layer N and its automorphisms are fixed in advance, and the
template must work for every cyclic H. Then beyond class two it can only use weight 1 on every
character of γ_c. That is the binary zero-sum setting of Imran–Ivanyos, which is open for large p.
This holds for every Lazard algebra, graded or not. Some graded class-3 families are still solved
directly by other published methods: the filiform family, by ISS Thm 2 with Ivanyos–Santha (IS)
Cor 8. So this is not a no-go for direct methods (TRAPS 8). The smallest graded test that I
found outside every source in the local folder is the free 2-generator class-3 group, of order
p^5.

Sources read: ISS, arXiv:0707.1260 (§2.3 Prop 1; §3 Thm 2, Lemmas 2–3; §4 Thms 3–4,
Lemmas 4–6, system (1)). Ivanyos–Santha, arXiv:1503.09016 (Prop 7 and its proof in §4.1,
Cor 8). Imran–Ivanyos, arXiv:2304.08376 §1. The local copies are in the session scratchpad
`lit-quantum/`.

## 1. The ISS mechanism, exactly

G is a class-2 group of exponent p, with G' = Z_p^d central. ISS Thm 2 first reduces an
arbitrary H, in any constant class, to |H| ∈ {1, p} by normalizer recursion. So H = ⟨h⟩.

* **Twists.** φ_j(x_i) = x_i^j on generators. In Lazard terms this is the graded dilation δ_j
  of L = L_1 ⊕ G'. It acts on G' by j². For every g, φ_j(g) = g^j z_g^{j−j²}, with z_g ∈ G' unique
  (Prop 1). Write h = exp(v_1 + v_2), with v_2 ∈ G'. Then z_h corresponds to −v_2, the
  non-homogeneous part of H. So φ_j(H) ≠ H, but φ_j(H) ⊆ HG'.
* **States.** For a random coset representative a and a measured label u that is uniform on
  (G')^*, ψ_u(a) = Σ_{z∈G'} ω^{−⟨u,z⟩} |aHz⟩ (Lemma 4).
* **Twisted action.** Ψ_g = ⊗_i ψ_{u_i}(a_i)·φ_{j_i}(g). For g = h·z with z ∈ G', Lemma 5 gives
  ψ_u·φ_j(z) = ω^{j²⟨u,z⟩} ψ_u and ψ_u·φ_j(h) = ω^{(j−j²)⟨u,z_h⟩} ψ_u. The second phase is the
  only effect of φ_j(H) ≠ H. It holds because the correction z_h^{j−j²} is **central**: it
  multiplies the state by a phase and does not move its support.
* **Absorption.** The total phase is ω^{⟨Σ u_i(j_i−j_i²), z_h⟩ + ⟨Σ u_i j_i², z⟩}. The unknown z_h
  enters linearly, with a known coefficient. Requiring Σ u_i j_i² = 0 and Σ u_i j_i = 0 (system
  (1); Chevalley–Warning for n > 3d; ISS Thm 5 at n = (d+1)²(d+2)/2) makes Ψ constant on HG'.
  The target is **HG'**, not H. HG' is preserved by every φ_j, because φ_j is scalar on G/G'.
  H is then read off by abelian HSP inside HG' (Thm 3).

## 2. Graded class 3: where it breaks

Take L = L_1 ⊕ L_2 ⊕ L_3 to be Carnot (γ_k = ⊕_{j≥k} L_j), with Z = L_3 central and
h = exp(η), η = v_1 + v_2 + v_3. There are two ways to transplant the mechanism.

**Route B: IS central descent on Z with dilations.** The states are ψ_λ(a) = Σ_{z∈Z} ω^{−λ(z)}|aHz⟩. We have
δ_s(h) = h^s e(s) with e(s) ∈ γ_2 and e(s) ≡ (s²−s)v_2 mod γ_3. If v_1 ≠ 0 and v_2 ≠ 0,
then e(s) ∉ HZ for s ∉ {0,1}. The correction is no longer central. It moves the support:
ψ_λ(a)·δ_s(h) is supported on aHZe(s), which is disjoint from aHZ. So no phase equation can
repair it. Next, δ_s^{-1}(HZ)/Z = F_p(v_1 + s^{−1}v_2). These are distinct lines for distinct s,
so the twisted product hides only ∩_i δ_{s_i}^{-1}(HZ) = Z, and the information is lost. A
useful procedure therefore needs every nonzero s_i equal. The equation Σ s_i³λ_i = 0 then
becomes s_0³Σ_{i∈S}λ_i = 0, a **binary zero-sum** problem. The v_3 part, by contrast, is
central and is absorbed as in ISS: when v_2 = 0, the system Σλ_i s_i = Σλ_i s_i³ = 0 suffices.

**Route A: ISS target Hγ_2, Fourier over N = γ_2.** Here γ_2 is abelian, but it is not central. Since
zh = h·Ad_h^{-1}(z), the H-action permutes labels instead of multiplying them by a phase:
ψ_u·h = ψ_{u∘Ad_h}. In class 3, u∘Ad_h − u = u_3∘ad_{v_1} on L_2. So ψ_u is an eigenvector exactly
when u_3 vanishes on [v_1, L_2]. That happens with probability p^{−dim[v_1,L_2]} ≤ 1/p over the
measured label. The non-homogeneity itself is harmless here. In the eigen cases the phase of
ψ_u·δ_s(h) is a polynomial in s of degree ≤ 3 that vanishes at s = 0, so a degree-(1,2,3)
diagonal system would absorb it (checked exactly; see below). The failure is the non-centrality
of N. It occurs even for homogeneous H = ⟨exp(x_1)⟩. For such H, route B works.

**Tensor lemma (C).** For unit vectors, |⟨⊗φ_i, ⊗U_iφ_i⟩| = ∏|⟨φ_i, U_iφ_i⟩|. So the product
is invariant up to phase iff every factor is. Label equations control only the phases of factors
that are already eigenvectors. They cannot repair a moved support (route B) or a permuted label
(route A). The two failures compound: route A needs the γ_3 labels cancelled first, and that
cancellation is route B, which degenerates to binary weights.

**Proposition T (template no-go, AI-proved, pending review).** Let G = exp(L) have class c,
with 3 ≤ c < p. Fix, independently of H, an abelian normal N ⊊ G and a set A ⊆ Aut(G) that
acts on N by scalars μ_α. The template prepares the states ψ_u(a) over N and twists by
α_i ∈ A. Suppose it hides HN, for every cyclic H with H ∩ N = 1, with probability > 1/p for
each nontrivially twisted copy. Then:

1. N is central. If h ∉ N and [h,N] ≠ 1, a copy is an eigenvector with probability
   p^{−rank(Ad_h−1)|_N} ≤ 1/p (Lemma B, applied to α(h) = h^r n). The elements outside N
   generate G.
2. Every α ∈ A acts on L/N by a scalar κ_α. With N central, ψ·α(h) has the support of ψ iff
   α(h) ∈ HN. So α must preserve every line of L/N.
3. If L/N is nonabelian, then κ_α = 1, α − id maps L into N ⊆ Z(L), and α = id on [L,L]. If
   L/N is abelian, then [L,L] ⊆ N ⊆ Z and c ≤ 2, a contradiction.

So μ_α = 1 on N ∩ [L,L] ⊇ N ∩ γ_c, and the only available weights are binary. In class 2,
L/G' is abelian and step 3 does not apply, which is exactly why ISS works. Positive grading
plays no role in the proof. This is a precise form of the Imran–Ivanyos remark that such
automorphisms "do not exist in general" beyond class two.

What lies outside the template, and is not excluded: H-dependent automorphisms (they exist:
for filiform, every κ ∈ F_p^× occurs among automorphisms that preserve a given H, but they
depend on H); operations on quotient coordinates instead of automorphisms of G, as in IS's
HPGP route; and adaptive or non-product schemes.

## 3. Exact finite checks

Every line η is checked, i.e. every cyclic H of order p; the coset representative a is random.

| check | heis3 p=5,7 | filiform4 p=5 | filiform4 p=7 | free23 p=5 |
|---|---|---|---|---|
| route A (H, labels): eigen count; mismatches with the prediction u_3⊥[v_1,L_2] | all eigen; 0 | 1250/3750; 0 | 4802/19208; 0 | 18750/93750; 0 |
| route A eigen cases: phase polynomial degree in s (max); independent of a | 2; yes | 3; yes | 3; yes | 3; yes |
| route B (H, λ, s ≥ 2): eigen count; mismatches with prediction v_1=0 or v_2=0 | all; 0 | 525/2325; 0 | 2205/13965; 0 | 13125/58125; 0 |
| route B non-eigen cases with support disjoint from the original | n/a | 1800/1800 | 11760/11760 | 45000/45000 |
| H defeating both routes | 0 | 100 of 155 | 294 of 399 | 600 of 775 |

The explicit example in filiform is h = exp(x_1 + x_3) with u = x_4^*. Its route-A stabilizer
is γ_2 (order 25, without H). Its route-B stabilizer is HZ, but the twisted intersection for
s ∈ {2,3} is Z (order 5). For h = exp(x_1 + x_4) (v_2 = 0) the twisted intersection keeps H
(`stab_check.out`). The free23 rows show the same pattern.

Automorphisms (`aut_check.out`, exhaustive): |Aut(filiform4)| = 50000 at p = 5 and 605052 at
p = 7, both equal to (p−1)²p^5. The automorphisms that preserve every HZ number p², and they
act on Z by κ = 1 only. For free23 at p = 5 and 7, the only map of L/Z that preserves every
line is the identity, and all of its lifts act on Z as the identity. For filiform at p = 5 and 7, the
automorphisms that preserve H = ⟨exp(x_1+x_3)⟩, or each of four other lines, realize every
κ ∈ F_p^×. Such scalers exist, but they depend on H.

The checks confirm Lemma B, route B and Lemma A on these groups. They do not prove
Proposition T, whose proof is the argument above.

## 4. Consequences for the paper, and a framing

* For graded L, obstacle (2) is genuine and independent of obstacle (1). The cover's
  contribution does **not** narrow to non-gradable algebras on the strength of the ISS twist.
* It does narrow by family. Groups with an abelian normal subgroup of index p (the filiform
  algebras, F_p ⋉ F_p^m) are handled for arbitrary H by composing ISS Thm 2 (whose class is
  closed under subgroups and quotients) with IS Cor 8, with no cover. This composition is my
  reasoning and I did not find it stated. Core line 210 already counts these instances as
  scope overlap. The paper should not say that the cover is necessary for graded L.
* The free 2-generator class-3 group has no abelian subgroup of index p: [ax+by, z] = aw_1 + bw_2.
  Neither the template nor IS Cor 8 applies to it directly. Once Hγ_2 is known, ISS finishes,
  because ⟨h⟩γ_2 has class ≤ 2. The open core is to find the line of v_1 in G/γ_2 = F_p^2.
  This amounts to a hidden polynomial graph problem along an unknown line,
  Σ_t ω^{P(t)}|q_a + t v_1⟩. I did not attempt it to completion. Status: UNKNOWN.

**Candidate paragraph (for the integrator; not inserted):** "A positive grading alone does not
let the class-two method of Ivanyos, Sanselme and Santha proceed. Their template Fourier-samples an
abelian normal subgroup N fixed in advance and twists right actions by automorphisms that
scale N. To hide HN for every cyclic H, N must be central and the automorphisms must act as
scalars on L/N. Beyond class two such automorphisms are the identity on [L,L], so the weights
on the top layer degenerate to the binary weights of Imran and Ivanyos. On the cover, the hidden
subgroup is homogeneous, so the dilations preserve it on every central quotient. One procedure
applies to every H: one diagonal equation of degree d per grade, with no lower-degree
correction equations, exact on every branch, with no reduction to |H| = p, and all of log H
retained at grade one. We do not claim that the cover is necessary for graded L. Groups with an
abelian normal subgroup of index p, for instance, are handled by combining [ISS, Thm 2] with
[IS, Cor 8]."

## Reproduce

```
cd research/audits/reviews/2026-11-12-rees-direct-twist-class3
nice -n 19 /opt/anaconda3/bin/python twist_check.py > twist_check.out   # ~1 min
nice -n 19 /opt/anaconda3/bin/python aut_check.py   > aut_check.out     # ~15 s
nice -n 19 /opt/anaconda3/bin/python stab_check.py  > stab_check.out    # ~25 s
```

Acceptance: every `pred_mismatch` is 0, `phase_poly_bad` is 0, and `kappa_on_Z_for_those` is [1].

Next hard question: is the HSP in the free 2-generator class-3 group (order p^5), with
|H| = p, solvable in polynomial time with no cover, through an HPGP route along an unknown line?
