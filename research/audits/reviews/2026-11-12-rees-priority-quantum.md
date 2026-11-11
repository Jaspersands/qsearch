# Rees cover: priority check against the quantum-algorithms literature

Date: 2026-11-12. **AI-checked, pending human review.** Claude helper session; read-only on the
paper (no .tex edited). This file is the only repository file written. Downloads (arXiv PDFs and
`pdftotext -layout` output) are in the session scratchpad folder `lit-quantum/`, not in the repo.
A missing search hit is not evidence of novelty (TRAPS 7, 8, 10). Nothing here is a novelty claim.

Question. Is Lemma `lem:homogeneous` of `docs/papers/rees-hsp/core/main-core.tex` (query f at c
evaluations E_s of the positive lower-central Rees cover A = ⊕ t^k γ_k(L), so the hidden subgroup
on A is homogeneous and dilation-stable), or Theorem `thm:main` (poly-time HSP for arbitrary H in
explicit Lazard p-groups of fixed class c < p, p growing, conditional on the Ivanyos–Santha import),
already in the quantum-algorithms literature?

Builds on, and does not repeat: `2026-11-01-rees-priority-check.md`, `2026-11-02-rees-a1-priority.md`,
`2026-11-09-rees-paper-pass-prep/prior-art-search.md`. Corpus lookup
(`tools/corpus/cli.py been-tried "graded cover dilation hidden subgroup nilpotent class three"`):
only internal notes and negatives (central-descent barrier for dihedral 2-groups, supercharacter
barrier); no external precedent recorded.

## 1. Verdict

- **Theorem regime: plausibly new; no covering result found.** No paper read gives a bounded-error
  poly-time HSP algorithm for arbitrary H in p-groups of fixed class c >= 3 with p growing, in any
  input model. Imran–Ivanyos (April 2023) still describe the non-exact, bounded-class, smooth-order
  case as open and "of great interest" (§6). A Dec 2025 survey (arXiv:2512.02087) and Morales
  (arXiv:2608.05321, App. A.3) both list Imran–Ivanyos (bounded primes) as the latest
  nilpotent-group result.
- **Key step (cover plus tuple oracle): no precedent found, but it is a close relative of two
  known devices.** (a) ISS 2007/2012 combine several coset states acted on by the graded dilations
  φ_j of a class-2 exponent-p group, and correct for non-homogeneous H with an extra degree-1
  equation. (b) Ivanyos–Santha 2015/17, §5 and Prop. 7, eliminate degree by degree with weights
  δ^d in a framework where the hidden data is a polynomial in an auxiliary scalar. The Rees step
  supplies that scalar (t) externally for any Lazard algebra. The homogenization itself is an
  elementary Vandermonde argument. Its novelty, if any, lies in the use, not in the depth.
- **Explicitly posed as open?** Not for Lazard or unitriangular groups as such. What is posed:
  II §6 asks for a poly(np) zero-sum algorithm, and says a randomized one would give HSP for
  nilpotent groups of smooth order and O(1) class. ISS 2012's abstract hopes its reduction helps at
  higher class. ISS 2007 §5 announces the class-2 extension only. IS 2015/17 has no
  concluding/open-problems section (arXiv v2 ends at §5). The Rees result answers the HSP consequence
  of II §6 for p-groups, by a different route and not the zero-sum question. It covers every p > c,
  so it goes beyond the smooth case.

## 2. Sources read

FULL = full PDF converted to text; the sections named were read, the rest keyword-scanned for
nilpotent, Lazard, graded, Rees, dilation, automorphism, Ivanyos, class. SCAN = keyword scan plus
abstract/intro only.

| Source | Read | What it contains, as it bears on the question |
|---|---|---|
| Ivanyos–Sanselme–Santha, *HSP in extraspecial groups*, arXiv:quant-ph/0701235 (STACS 2007) | FULL: §1, §4.2 (Lemmas 4–7, Thm 3), §4.3, §5 | Growing-p extraspecial groups (class 2). Automorphisms φ_j: x_i -> x_i^j, y_i -> y_i^j, z -> z^{j²}, i.e. the graded dilation. Lemma 5: φ_j(h) acts on the state ∣aHG′_u⟩ with phase ω^{u(j−j²)ℓ}. Four copies; quadratic+linear system (1)–(3) in j solved by a square root. §5 announces the extension to two-step nilpotent groups. **Not cited by the core paper.** |
| ISS, *HSP in nil-2 groups*, arXiv:0707.1260 (Algorithmica 2012) | FULL: Fact 3, Prop 1, §3 (Thm 2, Lemmas 1–3), §4 (Lemmas 4–6, system (1), Thm 5) | Every exponent-p class-2 group admits φ_j (x_i -> x_i^j extends). Prop 1(2): φ_j(g) = g^j z_g^{j−j²}. Hiding procedure for HG′ from n copies ⊗∣a_i HG′_{u_i}·φ_{j_i}(g)⟩, with j solving Σu_i j_i² = 0, Σu_i j_i = 0 (vector, n = (d+1)²(d+2)/2). Abstract: the class-c reduction "might also be useful for dealing with groups of higher nilpotency class". |
| Ivanyos–Santha, arXiv:1503.09016v2 (TCS 2017; FAW 2015) | FULL: abstract, Def 4, Thms 3, 5, Cor 6, Prop 7 with proof (Claim 13), Cor 8, §5 | Prop 7 proof: G_B = F_p^B ⋉ F_p^m; uses A = log B and B^k = e^{kA} to show the hidden subgroup is the graph of a degree-<=d polynomial v(x). §5: states ∣ψ_Y⟩ with phase polynomial in x; shift x_i -> x_i + δ_i x with Σδ_i^d Y^i = 0 removes the top degree; the novelty they state is to "eliminate all the degree d terms simultaneously, in one step". H restricted to order p outside F_p^m. No open-problems section. |
| Imran–Ivanyos, arXiv:2304.08376 (QIP 23:14, 2024) | FULL: §1 (Thm 1, Related results), §5 closing remark, §6 | Thm 1: exact, arbitrary H, bounded class and bounded primes. §1 p. 4: the class-2 automorphism twists "do not exist in general nilpotent groups of class greater than two". It also says DHIS14/IS17 handle groups with an abelian quotient "of restricted kind (e.g., cyclic)". §6: open question; a randomized method "would be of great interest" via Prop 3. |
| Bacon–Childs–van Dam, arXiv:quant-ph/0504083 | SCAN (§§1, 6.2, 7) | Z_p^r ⋊ Z_p, PGM, H of order p; polynomial equations solved classically. No lift. Already cited. |
| Ivanyos–Magniez–Santha, arXiv:quant-ph/0102014 | SCAN (theorem list, §§5–6 statements) | Small commutator subgroup (Thm 11), elementary abelian normal 2-subgroup (Thm 13); quantum hiding functions. Not the regime (G′ is large here). Already cited. |
| Friedl–Ivanyos–Magniez–Santha–Sen, arXiv:quant-ph/0211091 | SCAN (abstract, intro) | Bounded exponent and derived length; Lazard groups of exponent p growing are outside. Already cited. |
| Decker–Høyer–Ivanyos–Santha, arXiv:1305.1543; Decker–Draisma–Wocjan, arXiv:0706.1219 | SCAN | Hidden polynomial graph problems in F_p ⋉ F_p^m-type groups, constant m/degree. Polynomial-in-a-scalar framework, no cover. DHIS cited; DDW not (not needed). |
| Krovi–Rötteler, *Weyl–Heisenberg groups*, arXiv:0810.3695 | FULL: abstract, §on label change (eqs. 30–35) | Class 2. Changes irrep labels with automorphisms of B that extend to G, "possibly with respect to a different subgroup H′". Automorphisms of G again; no cover. |
| Ivanyos–Prakash–Santha, arXiv:1806.09660 | SCAN (abstract, §1.4) | Hidden multiple shift: queries f(x − hs) for r values of h, i.e. queries at several images. Abelian setting, no grading. |
| Ivanyos, *Hidden Borel subgroups*, arXiv:1105.4416; DIKQS parabolic, arXiv:1406.6511 | SCAN (intro) | GL_n settings. Intro of 1105.4416 says efficiently solvable groups remain close to commutative. |
| Gonçalves–Portugal, arXiv:1104.1361; Inui–Le Gall, arXiv:quant-ph/0412033; Moore–Russell, arXiv:quant-ph/0504067; Childs–van Dam survey, arXiv:0812.0380 | SCAN | Metacyclic or semidirect families, multiregister measurements, survey. The survey lists nil-2 as the nilpotent frontier. Nothing graded. |
| Bermejo-Vega–Zatloukal, arXiv:1509.05806 | SCAN | Normal hidden subgroups only. |
| Morales, arXiv:2608.05321v2 | FULL: §1, App. A.3 | Records ISS (class 2) and II (bounded primes) as the nilpotent state of the art; its families have unbounded class. Already cited. |
| Dutto et al., survey, arXiv:2512.02087 (Dec 2025) | SCAN; nilpotent paragraph (~l. 2029) and summary table | Latest nilpotent entry is II (constant class, bounded primes). No class >= 3, growing-p result listed. |
| Boucher–Fouque–Shen, arXiv:2609.34996; Kothari–Metger–O'Donnell–Shutty–Wu, arXiv:2609.40321; Kothari–O'Donnell–Wu, arXiv:2510.07515 | read in the 11-02 pass; rechecked as citers | Already cited by the paper. No cover or dilation. |
| Imran, *Hidden parabolic subgroups over chain rings*, arXiv:2610.28368 (Oct 2026) | SCAN (abstract, intro, refs) | Uses auxiliary "probes" and a congruence filtration in GL_n(R); parabolic H only. Not the regime. |
| O'Brien, trapped-ion HSP, arXiv:2611.06716 (Nov 2026) | SCAN (abstract) | Experiment on q-hedral Z_q ⋉ Z_p, p <= 7. Irrelevant. |
| Ragavan–Shutty, arXiv:2610.00502 (cites IS15 and II24) | SCAN (§3 Related Work) | Regev-reduction decoders; cites ISS/IS/II for zero-sum and equation solving only. |
| Kuperberg, arXiv:2507.18499; Muchane, arXiv:2610.16827; arXiv:2408.00075 (QFTs); arXiv:2605.12615; arXiv:2609.10596; arXiv:2511.19494 | SCAN | Infinite groups, character transform, QFT circuits, state isomorphism, group rings, generating sets. No nilpotent HSP algorithm. |
| Grochow–Ivanyos–Qiao–Sun, arXiv:2610.00874 (Oct 2026) | SCAN | Classical isomorphism of 2-groups of Frattini class 2. No quantum, Lazard or graded hit. |
| Di Concilio–Flores–Kahrobaei–Noce, IACR ePrint 2026/2678 (survey) | **UNKNOWN**: landing page only (PDF 403) | The abstract says nothing about nilpotent groups. No verdict depends on it. |

Citation lists (12 Nov 2026). Semantic Scholar: IS (1503.09016) has 4 citers since 2022, all known.
II (2304.08376) has 9 citers, all read in the 11-02 pass. Citers of ISS 2007 and 2012, DHIS14 and
IMS01 since 2022 are all in the table, or are irrelevant by abstract. OpenAlex: II has 9 citers,
adding nothing new. IS has 7, one new: 2610.00502, read above. Not reached: Google Scholar
(redirect), and Semantic Scholar citers of 2512.02087 (HTTP 429). The arXiv API was queried for
"hidden subgroup" plus nilpotent / p-group / Heisenberg / Lazard / nil-2 / extraspecial / exponent p,
and for authors Ivanyos and Santha, 2022 to Nov 2026. It turned up no other nilpotent HSP algorithm
paper.

## 3. Closest prior work and the precise difference

1. **ISS 2007/2012 (closest in mechanism).** At class 2, exponent p, φ_j is a graded dilation of G
   itself. Every such group is graded, since all relations lie in degree 2. ISS build a quantum
   hiding function for HG′ from several copies ⊗∣a_i HG′_{u_i}·φ_{j_i}(g)⟩, which evaluates the
   coset data at several automorphic images of g. A non-homogeneous H shows up as the phase
   (j − j²)ℓ, which costs an extra linear equation. Differences in the Rees version:
   - The images are the fixed evaluation surjections E_{s_i}: A -> L from a larger group, not
     automorphisms of G, and they are chosen non-adaptively.
   - The hidden subgroup on A is the homogeneous lift ⊕ t^k(h ∩ γ_k), so no lower-degree
     correction occurs. At c = 2 one needs Σ s_i² λ_i = 0 only, not ISS's linear-plus-quadratic system.
   - It works for non-gradable L (Dixmier–Lister), where II §1 observes that suitable
     automorphisms of G do not exist.
   - It outputs H directly; ISS hide HG′ and need the classical reduction to |H| <= p.
2. **Ivanyos–Santha §5 and Prop. 7 (closest in algebra).** The hidden object is polynomial in a
   scalar (via log B and e^{kA}, Claim 13). Elimination uses δ^d weights, one degree at a time.
   This is the descent the Rees paper imports and credits. Difference: IS get the scalar from the
   cyclic factor F_p^B of one group family, with |H| = p outside F_p^m. Rees adjoins a formal
   scalar t to any Lazard algebra and handles every H.
3. **Imran–Ivanyos (closest in goal).** Arbitrary H, any fixed class, central-series descent.
   But it uses binary (zero-sum) weights, so polynomial time only for bounded p. Rees uses scalar
   weights s^d at every p > c. The input model also differs: an explicit Lazard chart, bounded
   error, versus II's black box with unique encoding, exact.

## 4. Hostile referee: the strongest "not new / incremental" case

"The Rees algebra ⊕ t^kγ_k(L) is the textbook deformation to the associated graded. Interpolating
at c points to separate graded components is a Vandermonde exercise. Everything quantum is
borrowed:
- the coset-state machinery and multi-copy twisting from ISS 2007/2012, where φ_j are exactly the
  dilations of a graded class-2 group;
- the δ^d degree-by-degree elimination and the diagonal-equation solver from Ivanyos–Santha;
- even the 'make it polynomial in a scalar via the logarithm' step from IS Prop. 7.
The paper itself concedes that the growing-prime feature, the elimination and the query separation
are not new. What remains is the observation that one may pull f back along c evaluation maps,
which an expert would regard as folklore once the IS framework is known. Lazard groups of class
below p are the most Lie-like p-groups, so the result is the IS method transported to its natural
home. Its main consequence (black-box p-groups) leans on the ISS 2012 reduction. The paper fixes no
open problem of record: II §6 asks about zero-sum and smooth order; Rees treats p-groups only, and
is conditional on an imported solver read by AI sessions."

Best rebuttal available from the sources, which a human must still weigh:
- II §1 (2023), written by an author of all three prior lines, says the class-2 twist does not
  extend beyond class two. II §6 calls even a randomized bounded-class result "of great interest".
  So the experts did not regard the extension as folklore in 2023.
- Nothing from 2023 to Nov 2026 supplies it.

That is evidence about the state of the art. It does not make the step deep.

## 5. Honest statement of what is plausibly new

- Plausibly new: obtaining dilation-invariance for an *arbitrary* H in an *arbitrary* (possibly
  non-gradable) Lazard algebra by pulling the oracle back through a graded cover at c fixed points;
  and the resulting theorem for fixed class c < p, p growing, explicit chart, bounded error.
  Wording per TRAPS: "proposed fixed-class, growing-prime polynomial-time composition, pending
  independent correctness and priority review".
- Not new (the paper already says so): growing p at fixed class (IS Cor 8, BCvD), the elimination
  (IS §5), the solver (IS Thm 3/11), the exponent-p^e reduction (ISS 2012 Thm 2), the query
  separation.
- Gates that must stay false: "first graded cover in HSP" (only absence of hits); "solves II's open
  problem" (it answers the HSP consequence for p-groups, not the zero-sum question or general
  smooth nilpotent groups); "contradicts II §1" (their remark is about automorphisms of G).

## 6. Citations the paper should add or adjust (not applied)

1. **Add ISS, STACS 2007 (arXiv:quant-ph/0701235).** It is the first appearance of the φ_j twist
   with p growing (extraspecial groups, four copies, a quadratic+linear system). Related Work and
   §1.2 item (2) attribute the twist only to ISS 2012.
2. Optional: in §1.2 item (2), note that at class 2 the φ_j of ISS *are* dilations, and that ISS
   absorb the non-homogeneity of H by a linear equation. This makes the Lemma `lem:homogeneous`
   contrast exact.
3. Optional: in Related Work, note that IS Prop. 7 already uses the logarithm of B to make the
   hidden subgroup polynomial in a scalar. This anticipates the referee point in §4.
4. Optional: the Dec 2025 survey arXiv:2512.02087, as a record of the state of the art.
   Krovi–Rötteler (arXiv:0810.3695) and Ivanyos–Prakash–Santha (arXiv:1806.09660) are not needed.
5. Update the coverage sentence in Related Work (currently "on 2 November 2026") to 12 November
   2026. Name the gaps: Google Scholar not reached; ePrint 2026/2678 not opened.

## 7. Still open (needs a person)

- Ask Ivanyos or Santha directly whether the cover-and-interpolation step is known to them. This
  is the only check that settles priority. The paper already says no specialist has checked it.
- ePrint 2026/2678 full text; Google Scholar "cited by" for II (Scholar reported 14 on 11-02,
  versus 9 found).
- Not checked: whether a direct ISS-style generalisation (automorphism twists plus mixed-degree
  diagonal systems) already works for *graded* Lazard groups of class 3 without the cover. If it
  did, the cover's contribution would narrow to non-gradable algebras and to removing the
  lower-degree corrections.
