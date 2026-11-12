# HSP in H_3(Z) for arbitrary H: hardness, lower bounds, an alternative route (2026-11-12)

**Status: AI-checked, pending human review.** One Claude Code helper session, working
adversarially and independently of the agent building the direct algorithm. No paper,
`STATE.md`, handoff or registry file was edited, no git command was run, and no network
request went beyond read-only arXiv abstract pages. Scripts and outputs are in
`research/audits/reviews/2026-11-12-rees-h3z-hardness/` (run with
`nice -n 19 /opt/anaconda3/bin/python <script>`). The finite checks can only falsify (TRAPS 7).

Context read: `STATE.md` "Now" item (vi); `2026-11-12-rees-utz-finite-index.md`;
`main-core.tex` §8.4 (cor:utz, rem:utz-scope) read only; survey ePrint 2026/2678 §8.5, §9 and §10
item 5 [read, pdftotext in place]; Kuperberg arXiv:2507.18499 §1, §2.4 and §7.1 [read, local text
from an earlier pass]; ISS arXiv:0707.1260 §1 and §4 [read]; Horan–Kahrobaei arXiv:1805.04179 §5
[read]; Regev cs/0304005 [abstract only]; Bacon–Childs–van Dam quant-ph/0504083 [abstract only].
Items tagged [recalled] were not re-read in this pass and are not premises of any PROVED item.

**Claim gates.** All unchanged: `speedup_claim_allowed` and `novelty_established` stay false.
Nothing here claims to solve the survey's open problem.

## Setting and notation

G = H_3(Z). Elements are (a, b, c) = [[1,a,c],[0,1,b],[0,0,1]], with
(a,b,c)(a',b',c') = (a+a', b+b', c+c'+ab'); x = (1,0,0), y = (0,1,0), z = (0,0,1) = [x,y] up
to sign. π: G → G/Z = Z² is (a,b,c) ↦ (a,b), and ω(u,v) = u₁v₂ − u₂v₁. For a primitive
v₀ ∈ Z², A_{v₀} = π⁻¹(Zv₀) = ⟨ŵ, z⟩ ≅ Z², where ŵ is any lift of v₀; this is the
centralizer of every noncentral element over v₀. Input model as in cor:utz: f hides H, is given
by a coherent oracle on matrices with entries in [0, 2^B), and H has generators of bit size ≤ b.
"Kuperberg Thm 1.5" means [Kup, Thm 1.5]: HSP in Z^k for arbitrary H in quantum time
poly(k, n), where n is the bit size of the answer. It is imported and was not re-proved here.

## Verdict (summary)

| # | Claim | Label |
|---|---|---|
| 1 | Subgroup classification. Infinite-index H is ⟨z^k⟩, 1, ⟨h, z^k⟩ or ⟨h⟩ with h noncentral | PROVED |
| 2 | Every H with H ∩ Z ≠ 1 is found in quantum poly(b) time | CONDITIONAL on Kuperberg Thm 1.5 and B ≥ B₀(b) = poly(b) |
| 3 | Hard case (H ∩ Z = 1) is poly-time equivalent to finding the line Qπ(H) | PROVED (given Kuperberg Thm 1.5) |
| 4 | Restriction to abelian subgroups and the "period of t ↦ f(gz^t)" are blind in the hard case | PROVED (the route is REFUTED) |
| 5 | No reduction from dihedral, D_∞, Z⋊Z or hidden shift via subgroups or quotients | PROVED (narrow); general hardness UNKNOWN |
| 6 | Classical query complexity of the cyclic case is ≥ Ω(√δ · 2^{1.5b}) | PROVED |
| 7 | Zero-sum route: hard case ≤ random modular zero-sum subset sum | CONDITIONAL / argued (error analysis not written) |
| 8 | Hence poly(b) quantum queries (exponential time) and 2^{O(√log W)} time | CONDITIONAL / argued |
| 9 | Single-copy Fourier sampling (Mal'cev coordinates) loses information as \|v\| grows | finite check only; asymptotics UNKNOWN |
| 10 | Efficient (poly-time) algorithm for the hard case, or hardness | **UNKNOWN** |

**Main finding.** The easy and hard cases split exactly at H ∩ Z. When H ∩ Z ≠ 1 everything
reduces to Kuperberg's abelian algorithm in poly time, with no "mod z^e" step on the hard part
(§2). The hard case is "find the direction of π(h)" (§3). Every route tried here, including
the "reduce modulo z^e" route, needs to cancel random central characters. The most direct
form of that cancellation is a **random zero-sum subset-sum problem modulo W ≈ 2^{O(b)}**.
This is the same average-case problem through which Regev solves the dihedral HSP
([Regev, abstract]: "we solve the hidden subgroup problem on the dihedral group by using an
average case subset sum routine"). It gives a subexponential alternative route (§7), not a
polynomial one, and no hardness reduction in either direction.

## 1. Subgroups of H_3(Z) [PROVED]

Let r = rank π(H).
- r = 2: pick h₁, h₂ ∈ H with π(h₁), π(h₂) independent. Then [h₁,h₂] = z^{±det} ∈ H, so
  H ∩ Z ≠ 1, and [G:H] = [Z²:π(H)]·[Z:H∩Z] < ∞.
- r = 1: π(H) = Zv with v = d·v₀ and v₀ primitive. Then H ⊆ A_{v₀} ≅ Z², so H = ⟨h⟩ or
  H = ⟨h, z^k⟩ with k ≥ 1. If H ∩ Z = 1, H embeds in Z via its projection, so it is cyclic.
- r = 0: H = ⟨z^k⟩ (k ≥ 0).

So H has infinite index iff r ≤ 1. **H ∩ Z = 1 iff H = 1 or H = ⟨h⟩ with h noncentral.**
This is the hard case. In it the core of H is trivial, since the conjugates of h are h·z^{ω(u,v)}.
So f factors through no proper quotient of G, and in particular through no finite quotient.

## 2. H ∩ Z ≠ 1 is polynomial [CONDITIONAL on Kuperberg Thm 1.5]

**Proposition E.** Assume Kuperberg Thm 1.5 and B ≥ B₀(b) = poly(b), so that the boxes in
Kuperberg's Algorithm A fit into the oracle box after a left translation. If H ∩ Z ≠ 1, a
quantum algorithm finds H in poly(b) time. If H ∩ Z = 1, the same algorithm says so.

*Algorithm and proof.*
1. f restricted to Z hides H ∩ Z = ⟨z^k⟩. Kuperberg Thm 1.5 with k = 1 returns k, including
   k = 0 (trivial intersection), which is the case Shor–Kitaev does not handle. k ≤ 2^{O(b)}
   (rank 2: k divides det(π h₁, π h₂) ≤ 2^{2b+1}; rank 1: an index bound in A_{v₀}
   coordinates; rank 0: k ≤ 2^b).
2. If k ≥ 1, let φ(a,b,c) = x^{ka} y^{kb} z^c, a map from Z³ onto N = π⁻¹(kZ²). Since
   y^β x^α = x^α y^β z^{−αβ}, we get φ(u)φ(u') = φ(u+u')·z^{−k²u₂u₁'}, and z^{k²(·)} lies in
   ⟨z^k⟩ ⊆ H and is central. Hence Λ = φ⁻¹(H) is a subgroup of Z³, and
   φ(u)⁻¹φ(u') ∈ H ⇔ φ(u'−u) ∈ H. So u ↦ f(g₀φ(u)) hides Λ, where the left translate g₀ makes
   all queried entries nonnegative. Kuperberg Thm 1.5 (k = 3) returns Λ, and therefore
   H ∩ N, together with π(H) ∩ kZ² = kπ(Λ).
3. rank π(Λ) = 0 gives π(H) = 0, so H = ⟨z^k⟩. Rank 1 gives the direction v₀; then
   H ⊆ A_{v₀}, and Kuperberg Thm 1.5 on (s,t) ↦ f(ŵ^s z^t), a homomorphism Z² → A_{v₀},
   returns H. Rank 2 means finite index, handled by cor:utz with n = 3 (ISS 2012 plus periods,
   which needs no part of the Rees paper).

Finite check `central_case_check.py` (Check A): the hiding identity and the closure of Λ hold
for 96,000 pairs over 60 random H of all three kinds (⟨z^k⟩, ⟨h,z^k⟩, finite index), with exact
membership tests and 0 failures.

*Adversarial notes.* (i) Kuperberg's cost model is "polynomial query cost on Z^k". Our oracle
is a box of nonnegative entries, so B must be chosen poly(b) large enough. Cor utz's
B = (m+2)b+1 may be too small for Algorithm A's exp(poly(n)) parameters; this was not
checked. (ii) This uses no virtually-abelian machinery: G/⟨z^k⟩ is virtually abelian, but
[Kup, Cor 1.9] would give only 2^{O(√n)}, and step 2 avoids it.

## 3. The hard case is "find a line" [PROVED, given Kuperberg Thm 1.5]

**Proposition R.** Under the promise H ∩ Z = 1, the following are equivalent up to
quantum poly(b) time:
(a) find H;
(b) find the line Qπ(H) ⊂ Q², or certify π(H) = 0;
(c) obtain one element of H \ {1};
(d) have a quantum hiding procedure for the normal subgroup HZ = π⁻¹(π(H)).

(b)⇒(a) is the centralizer trick: H ⊆ A_{v₀}, then Kuperberg Thm 1.5 on Z². If π(H) = 0, then
H = H ∩ Z = 1. (c)⇒(b) via π. (d)⇒(b) because HZ ⊇ Z, so (d) is an abelian HSP on G/Z = Z².
Kuperberg's Algorithm A only uses the coset structure of the input register, so a quantum
hiding procedure is enough: this is the Z^k analogue of ISS Fact 1, argued, not re-proved.
(a)⇒(b),(c),(d) is trivial. The decision version "H ≠ 1?" is in NP, with a nontrivial element
of H as certificate ([Kup, Prop 2.3] pattern).

The centralizer trick of the brief is therefore exactly the reduction (b)⇒(a). It does not
remove the hard part: the hard part is (b), a choice among about 2^{2b} directions.

## 4. Blind routes [PROVED]

**Lemma 4.1.** Let H = ⟨h⟩ with h noncentral and π(h) ∥ v₀.
(i) For every g, t ↦ f(g z^t) is injective, since f(gz^t) = f(gz^{t'}) ⇔ z^{t'−t} ∈ H.
(ii) For every abelian subgroup A ⊄ A_{v₀}, f|_A is injective: an abelian subgroup containing
a noncentral element g lies in C(g) = A_{π(g)/gcd}, and H ∩ A_u ≠ 1 iff u ∥ v₀.

So the "continued fractions for the period of t ↦ f(gz^t)" idea is **REFUTED** as a route:
there is no period, and these restrictions give no information. Lattice decoding only helps
after the direction is known, and then (§3) Kuperberg's Z² algorithm already finishes the job.

**Fibers.** For u, u' ∈ Z², the fibers t ↦ f(σ(u)z^t) and t ↦ f(σ(u')z^t) have disjoint
images unless u'−u = mv. If u'−u = mv, they are shifts of each other by
s = u₁mv₂ − mc − C(m,2)v₁v₂, a hidden-shift pair on Z. Every such pair lies inside one coset
σ(u)A_{v₀}, and there the whole family of shifts is one abelian Z² instance. So the instance
carries hidden shifts only together with all their multiples. That is why the obvious
"hidden shift inside H_3(Z)" embedding makes the problem easy instead of hard (heuristic,
recorded for §5).

## 5. Hardness reductions [narrow PROVED; general UNKNOWN]

**Proposition 5.1 (narrow).** Every subgroup and every quotient of H_3(Z) is nilpotent of
class ≤ 2. The standard HSP reductions (to a visible subgroup with computable transversal, or
to a quotient; [Kup §2.4]) can therefore import hardness only from HSPs on nilpotent class-≤2
subquotients. These are: Z^k with k ≤ 3 (Kuperberg, poly); finite class-2 quotients such as
H_3(Z/N) (ISS 2012, poly); groups ⟨x,y,z | [x,y] = z^m⟩ (H_3(Z) again); and H_3(Z)/⟨z^m⟩
(case §2). D_N (N not a power of 2), D_∞, Z ⋊_{−1} Z, G wr Z/2 and dihedral hidden shift are
not nilpotent, or have class > 2, so none of them is a subquotient. *Proof:* subgroups and
quotients of a class-2 nilpotent group are nilpotent of class ≤ 2, and D_∞ and Z⋊_{−1}Z have
non-terminating lower central series. □

This excludes only homomorphic embeddings. Kuperberg's own hidden-shift-to-HSP reduction uses
a wreath product that is not a subquotient here. Section 4 suggests why a direct embedding of a
hidden shift fails, but that is heuristic.

Kuperberg's uSVP hardness [Kup, Thm 1.4] needs pseudo-polynomial query cost and growing
dimension k. Our oracle has binary cost and fixed dimension, so that mechanism does not
transfer. This is not a proof that lattice hardness is impossible: Regev's uSVP ≤ DCP goes
through a fixed-shape group with a large modulus.

**Status: UNKNOWN.** No reduction from DHSP, hidden shift on Z_N, Z⋊Z, D_∞ or a lattice
problem to any case was found. No reduction from the hard case to DHSP was found either.
Both the hard case (§7) and DHSP (Regev) reduce to average-case subset sum, which places them
in the same plausibly-hard class but proves nothing.

## 6. Lower bounds

**Proposition 6.1 (classical, cyclic case) [PROVED].** Let
F = {⟨h⟩ : h = (v₁,v₂,c), 0 ≤ v_i, c < 2^b, (v₁,v₂) primitive}, so |F| ≥ (6/π² − o(1))·2^{3b}.
A classical randomized algorithm that distinguishes H = 1 from H uniform in F with advantage
δ makes q ≥ √(δ|F|/2) = Ω(√δ·2^{1.5b}) queries, whatever B is.

*Proof.* Take f to be a uniformly random injective labelling of G/H. Until the first query pair
with g_i⁻¹g_j ∈ H, the answers are fresh distinct uniform labels, distributed exactly as for
H = 1, so the queried points are independent of H. Fix d = g_i⁻¹g_j ≠ 1. If d is central,
d ∉ H. Otherwise d ∈ ⟨h⟩ with π(h) primitive forces d = h^m with m = ±gcd(π(d)). Roots are
unique in G: h^m = h'^m with m ≠ 0 gives π(h) = π(h') and then c = c' from
mc + C(m,2)v₁v₂. So at most 2 members of F contain d, and Pr[d ∈ H] ≤ 2/|F|. A union bound
over q² pairs gives δ ≤ 2q²/|F|. □

Check B of `central_case_check.py` confirms the root count #{h : g ∈ ⟨h⟩} ≤ 2τ(gcd π(g))
(the non-primitive family) on 400 samples, with 0 failures. The trivial upper bound is 2^{O(b)}
(query a box containing 1 and h). The exact exponent between 1.5b and O(b) was not settled.
For ⟨z^k⟩ with k a random prime in [2^{b−1}, 2^b), the same argument gives Ω(2^{b/2}/poly(b)).
Finite index is rem:utz-scope(c).

**Quantum queries.** No nontrivial quantum query lower bound is known to me for any case.
Kuperberg's 2^{Θ(n)} quantum query lower bounds (Q/Z, free groups; [Kup, Cor 1.3]) use groups
that are not finitely generated or not amenable. §7 gives an argued **poly(b) query upper
bound** (Ettinger–Høyer style: poly queries, exponential classical post-processing), so no
such lower bound is expected for H_3(Z).

**Strong Fourier sampling count.**
- *Structure.* H_3(Z) is not type I: by Thoma's theorem [recalled], a countable discrete group
  is type I iff it is virtually abelian. So there is no canonical irrep decomposition of the
  regular representation, and "strong Fourier sampling over H_3(Z)" has no canonical meaning.
  Kuperberg's Cor 1.9 class (virtually abelian) is exactly the type I finitely generated
  groups.
- *Truncated boxes.* The irreps with central character p/q have dimension q. Resolving them
  needs base extent ≥ q, which creates central shifts ~q². A window W resolves only
  θ ∈ (1/W)Z, whose typical denominator is ~W. Since W ≫ q² is incompatible with q ~ W, only
  the θ ≈ 0 sector is usable from a single copy. That is the source of the zero-sum
  requirement (argued).
- *Finite check* `malcev_fourier_tv.py`, `_scaling.py`, `_ratio.py`, `_ratio2.py`: the exact
  single-copy law of Z³ QFT sampling in Mal'cev coordinates. TV(p_⟨h⟩, uniform) does not
  shrink with the box at fixed h (0.16 for h = (1,2,1) at R = 8, 12, 16). At box ratio R = 6|v|
  it decays with |v|: 0.191, 0.161, 0.109, 0.078, 0.062 for |v| = 1.4, 2.2, 3.6, 5.8, 8.1.
  The abelian control Z³/⟨(v,c)⟩ stays at ≈ 0.59. A fit gives ≈ |v|^{−0.65} over one decade,
  i.e. 2^{−Ω(b)} per sample if it persisted. **Finite only; the asymptotics are UNKNOWN.** An
  earlier heuristic of mine ("single-copy samples carry no information for |v|²/d > 1") is
  **REFUTED** by these numbers at small sizes, and I withdrew it.

## 7. Alternative route: zero-sum of central characters [CONDITIONAL / argued]

This route is independent of "reduce modulo z^e plus Kuperberg". It is ISS §4 with the
endomorphisms φ_j restricted to j ∈ {0,1}, transplanted to Z.

**Construction.** Measure f on a box to get a segment of a coset a_iH. Apply z^{−t} in
superposition over t < W, then QFT the t register (ISS Lemma 4). This gives a twisted coset
state |χ_i⟩ = Σ_{j<J, t<W} e(−k_i t/W)|a_i h^j z^t⟩ with a known random k_i ∈ Z_W. For a set S
of copies, the hiding procedure is g ↦ ⊗_{i∈S}|χ_i·g⟩, which needs no further f queries.

**Lemma 7.1 [PROVED, exact closed form].**
⟨χ_i·g'|χ_i·g⟩ = (1−|m|/J)(1−|s|/W)·e(k_i s/W) if g g'⁻¹ = h^m z^s (|m| < J, |s| < W), and 0
otherwise. The pair (m,s) does not depend on i. For g = σ(u), g' = σ(u'), u−u' = mv, it
contains the cocycle s = u₁mv₂ − mc − C(m,2)v₁v₂.

So the tensor product hides HZ up to the phase e(sK/W), K = Σ_{i∈S}k_i, and up to window
factors. If K ≡ 0 mod W (or |K| ≪ W/s_max), it is an approximate hiding procedure for HZ, and
Prop R(d) finishes. If K ≢ 0, the u-dependent phase spreads the Fourier law.

Finite check `zero_sum_hiding.py`: closed form vs brute force agree to 1.5e−13. With v = (1,2),
B = 8, J = 400, W = 4000, the Fourier mass on the dual line {ξ·v ≡ 0 mod 8} is:

| Case | Mass |
|---|---|
| ideal θ = 0 | 0.420 |
| zero-sum pair | 0.418 |
| zero-sum triple | 0.417 |
| near-zero pair, K = 1 | 0.418 |
| single copy | 0.115 |
| pair with K = 400 | 0.178 |
| H = 1 baseline | 0.125 |

**Proposition Z [argued; the approximation analysis for Kuperberg's Algorithm A with a
quantum, approximate hiding procedure was not written].** Suppose an algorithm, given n(W)
independent uniform k_i ∈ Z_W, returns a nonempty S with Σ_S k_i ≡ 0 mod W (or within
±W/D, D = poly·s_max) in time τ(W), with probability ≥ 1/2. Then the hard case is solved
with poly(b)·n(W) queries and poly(b)·(n(W) + τ(W)) time, where log W = O(log Q + b) and Q is
the Z² Fourier box.

Instantiations:
- *Queries.* For n = log₂W + log₂(1/ε) + 1, a zero-sum subset exists with probability
  ≥ 1 − ε. [PROVED: subset sums of distinct nonempty subsets are pairwise independent and
  uniform; second moment.] Exhaustive search gives **poly(b) queries** and exponential time.
- *Time.* Wagner's k-tree with + only (`zero_sum_sieve.py`: zero-sum 16-subsets mod 2^{48}
  from 16,384 samples, in 0.2 s) gives 2^{O(√log W)}. This is subexponential in b iff
  log Q = o(b²). I believe Q = 2^{O(b)} suffices for rank-1 H in Z² (two samples plus a
  three-dimensional lattice decode), but did not check it. Then the time is 2^{O(√b)},
  matching [Kup, Cor 1.9] for virtually abelian groups.

*Why larger j does not obviously help.* With general j, ISS's conditions become
Σk_i j_i ≡ Σk_i C(j_i,2) ≡ 0 (mod W). Over Z, φ_j multiplies the central shifts by j², so
J²s_max ≪ W is needed. For j ∈ {0,±1} the conditions collapse to subset sum. Whether
"quadratic SIS" with |j| ≤ W^{1/4} has a poly-time solution is **UNKNOWN**: there is no
linearization, and LLL handles only the linear row. This is the over-Z analogue of the
Imran–Ivanyos zero-sum obstruction at large primes.

*Consequence for the "mod z^e" route (adversarial note for the other agent).* For
H ∩ Z = 1, G/⟨z^e⟩ is virtually abelian, but f gives no hiding function for H⟨z^e⟩. The
quantum substitute Σ_t e(−θt)|gHz^{et}⟩ is invariant under z^e only up to the phase e(θ). So
that route needs either the same zero-sum cancellation or an HSP with a projective (2-cocycle)
twist, which Kuperberg's Cor 1.9 does not cover.

## 8. Prior art: what is known

- **Kuperberg 2507.18499** [read]:
  - Thm 1.5: Z^k, arbitrary H, poly time; Cor 1.7: finitely generated abelian groups.
  - Cor 1.9: virtually abelian groups in 2^{O(√n)}, through Thm 1.8, which is "Outlined" with
    statistical estimates omitted in his text.
  - Hardness: Thm 1.1 (Q/Z, NP-complete), Thm 1.2 (normal HSEP in free groups, NP-complete),
    Cor 1.3 (2^{Θ(n)} quantum query lower bounds) and Thm 1.4 (uSVP-hardness on Z^k with
    pseudo-polynomial cost).
  - Nothing on nilpotent groups or H_3(Z).
- **Survey 2026/2678** [read]: §10 item 5 says it is open whether the HSP in H_3(Z) can be
  solved efficiently; §8.5 covers ISS nil-2 and RRS for the Heisenberg group of order p³.
- **Horan–Kahrobaei 1805.04179 §5** [read]: the infinite non-abelian HSP "has not been
  addressed" (2018).
- **ISS 0707.1260 §4** [read]: hiding procedure for HG′ through φ_j and the Chevalley–Warning
  system; finite groups only.
- **BCvD quant-ph/0504083** [abstract]: Heisenberg groups (Z_p)² ⋊ Z_p via entangled
  measurements.
- **Regev cs/0304005** [abstract]: DHSP from average-case subset sum; uSVP ≤ DHSP coset
  sampling.
- **Wagner (k-tree), Lyubashevsky 2005, Flaxman–Przydatek 2005** [recalled]: average-case
  subset sum is 2^{O(√log W)} with that many samples, or 2^{O(log W/log log W)} with
  (log W)^{1+ε} samples. No poly algorithm with poly(log W) samples is known to me.

No source read gives any algorithm or hardness result for infinite-index HSP in H_3(Z) or in
any non-virtually-abelian finitely generated group. The search was not exhaustive. The
zero-sum route (§7) was not found stated, but its ingredients are ISS §4 and Wagner/Regev, so
it is a combination, not new technique.

## 9. Adversarial self-check

1. *Did I mislabel the hard case?* No. §1 shows H ∩ Z = 1 ⇔ H ∈ {1, ⟨h⟩}, and §2 handles
   everything else, including ⟨h, z^k⟩ with exponentially large k.
2. *Prop E input model.* This is the weakest point of §2: it holds only if the oracle box
   (B) is large enough for Kuperberg's boxes, and B was not computed. Also Thm 1.5 is AI-read,
   not re-proved.
3. *Prop R(d)⇒(b) and Prop Z* use Kuperberg's Algorithm A with a quantum, approximately
   hiding procedure. That extension is argued, not proved. The n-fold product of window
   factors (1−|m|/J)^n needs J, W ≫ n·Q-scales; this is affordable but unchecked.
4. *Finite checks.* The zero-sum table is at toy size (B = 8; lines only 4 points long), so the
   ideal mass is 0.42, not near 1. It shows the mechanism, not the asymptotics. The TV decay in
   §6 covers one decade of |v| and is not a lower bound.
5. *Withdrawn claim.* "Single-copy Mal'cev Fourier samples carry zero information" was false
   at small sizes (§6) and was removed.
6. *Thoma's theorem* is recalled, not re-read. It is used only for a remark, never as a
   premise of a PROVED item.
7. *Hardness.* Nothing here shows the hard case is hard. The subset-sum connection is an upper
   bound only. A cleverer measurement (e.g. Bell-type sampling on pairs with θ₁ + θ₂ of small
   denominator) is not excluded.

## 10. Next hard question

Is the cyclic case equivalent to average-case zero-sum subset sum? Concretely, either:
- (a) produce, from poly(b) twisted coset states with random central characters, a state
  whose central character is 0 (or of poly-bounded denominator) in poly time, by a method
  other than subset selection, or decide whether "quadratic SIS"
  (Σk_i j_i ≡ Σk_i C(j_i,2) ≡ 0 mod W, 0 < |j|_∞ ≤ W^{1/4}) is solvable in poly time; or
- (b) reduce average-case zero-sum subset sum, or DCP, to the H_3(Z) cyclic case.

**Next command:** LLL/BKZ experiment for (a) with fpylll (`research/TOOLBOX.md`):
`nice -n 19 $E/python quad_sis_lll.py --W 2^64 --n 8..24`. This requires writing
`quad_sis_lll.py` first. It searches for short solutions via an LLL basis of the linear row,
followed by a search over small combinations of that basis.
**Artifact:** `2026-11-12-rees-h3z-hardness/quad_sis_lll.out`.
**Acceptance test:** a solution found in poly time with |j|_∞ ≤ W^{1/4} for W ≥ 2^{64}
in ≥ 50% of instances would refute "zero-sum is the bottleneck" and give a candidate poly
route. Consistent failure is only evidence (TRAPS 7).
