# Rees cover: priority check in the algebra and computational group theory literature

Date: 2026-11-12. **AI-checked, pending human review.** One Opus 5.5 helper session. I did not edit
the paper. This file is the only repository file written.

Question: is the key step of `docs/papers/rees-hsp/core/main-core.tex` already known? That step is
§1.3 "Core Idea", Theorem `thm:rees-cover` and Lemma `lem:homogeneous`. It forms the positive Rees
algebra A = ⊕_{k=1}^c t^k γ_k(L) and the tuple oracle f̂ = (f∘E_{s_1}, …, f∘E_{s_c}), whose hidden
subgroup is ĥ = ⊕ t^k (h ∩ γ_k), so every dilation preserves it. The earlier checks covered the HSP
and quantum literature (2026-11-01, 2026-11-02, 2026-11-09 prior-art-search). This pass covers
algebra and computational group theory (CGT) only.

Downloaded texts (pdftotext output, gitignored scratchpad, not part of the repository):
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/265ea4e4-9d06-4353-9b18-ca6cd6e80035/scratchpad/lit-algebra/`.

Repo corpus check (`tools/corpus/cli.py been-tried "Rees cover interpolation homogeneous hidden
subgroup"`): it returns only internal notes (`REES_CONCRETE_FORMALIZATION.md`,
`REES_NONGRADABLE_INPUT.md`, the 2026-10-22 handoff entry) and unrelated negatives. None of them is
an external precedent.

## 0. Verdicts

| Sub-question | Verdict | Best source (opened) |
|---|---|---|
| (a1) Rees algebra of a filtered algebra; specialisation t → 1 gives the algebra | STANDARD | Decker–Eder–Levandovskyy–Tiwari, arXiv:1704.02852v1, §2.4, Thm 8 (p. 6); Etingof–Ma, arXiv:1001.0432v4, §2.9 |
| (a2) ⊕ t^k (h ∩ F_k) as the Rees module (homogenization) of a sub-object for the induced filtration | STANDARD (for ideals; the Lie-subalgebra version is the same linear algebra) | DELT arXiv:1704.02852v1, **Definition 9 (p. 6)**: I^h = ⟨f^h⟩ = ⊕_d (F_d A ∩ I) t^d |
| (a3) A homogeneous subspace is exactly one that is stable under the scalar (GL_1) action of the grading; positive gradings ↔ such actions; characteristically nilpotent algebras admit no positive grading | STANDARD | Cornulier, Bull. SMF 144 (2016) 693–744 (arXiv:1403.5295v5), §1.2.1 (p. 4), Def. 1.5 (pp. 5–6), Remark 3.2, Lemma 3.10 (char p, class ≤ p+1) |
| (a4) Recovering homogeneous components from finitely many dilated evaluations (Vandermonde) | STANDARD (folklore in algebraic complexity) | Shpilka–Yehudayoff, FnT TCS 5 (2010), §2.5, sketch of proof of Thm 2.12 (p. 22 of the authors' version): evaluate at R+1 points and interpolate |
| (a5) Contractions/degenerations as families L_s; generalized Inönü–Wigner contraction with respect to a filtration gives gr L | STANDARD | Kochetov–Koval, J. Algebra 696 (2026) 245–277 (arXiv:2506.00610v2), §2.2, eqs. (1)–(3), **Remark 2** (p. 4) |
| (a6) Using several fibres to recover the Rees module of an unknown subspace | STANDARD as linear algebra (a2 + a4), but I found no source that states it in this form | none states it; it follows in two lines from DELT Def. 9 and SY10 §2.5 |
| (b1) In CGT: making an unknown sub-object homogeneous by evaluating a black-box function at several fibres of a Rees family | POSSIBLY NEW (not found) | BOW 2019, Wilson 2013, Maglione 2016/2021, BMW 2015, Grochow–Qiao 2021 read: none does it |
| (b2) Turning a non-gradable algebra into a graded one (a cover, not a quotient) to get scalar automorphisms for an algorithm | POSSIBLY NEW in CGT (not found); possible analogue in analysis (Rothschild–Stein lifting) is UNKNOWN (not opened) | the CGT sources pass to the associated graded quotient gr = ⊕ γ_k/γ_{k+1}, never to a graded cover |
| (b3) Is the step the Lie/group analogue of ideal homogenization? | YES, as algebra: ĥ = h^h for the lower central filtration, and ĥ = largest dilation-stable subspace of E_1^{-1}(h) | DELT Def. 9 (the identity); the rest is a one-line remark (§3) |
| Cicalò–de Graaf–Vaughan-Lee 2012; Eick–Leedham-Green–O'Brien 2002; Eick/O'Brien/Vaughan-Lee Lazard-algorithm papers | UNKNOWN (not opened; no arXiv version, publisher copy gated) | — |
| Textbook locators (Eisenbud; Cox–Little–O'Shea; Bruns–Herzog; Kreuzer–Robbiano; Li–van Oystaeyen) | UNKNOWN (not opened) | see §5 |

Bottom line. The algebra in Lemma `lem:homogeneous` is standard: Rees module of the induced
filtration, homogeneous core, and Vandermonde extraction of homogeneous parts. It deserves explicit
credit rather than a novelty claim. None of the CGT sources I read applies these facts to transport
a hiding function, or any oracle for an unknown sub-object, to a graded cover. None of them builds a
graded cover (as opposed to the associated-graded quotient) to supply dilations for a non-gradable
algebra. So (b) stays "possibly new, not found". This search is not exhaustive, and the paper's
sentence that a specialist has not checked it is still true.

## 1. Sources read

"FULL" means that the named sections were read in full text; the rest of the paper was
keyword-scanned for: Rees, homogeniz*, deformation, contraction, Vandermonde, interpolat*, dilation,
[t], Carnot, characteristically nilpotent, filtration, associated graded, Lazard.

1. **Brooksbank–O'Brien–Wilson, "Testing isomorphism of graded algebras"**, Trans. AMS 372 (2019)
   8067–8090; arXiv:1708.08873v2. FULL: §1 (pp. 1–3), §2.1 (pp. 3–4), §4 opening and §4.1; keyword
   scan of the rest. *Contains:* an algorithm deciding **graded** isomorphism of finite graded
   algebras generated in degree 1 (Thm 1.1). Graded inputs come from filtrations, as associated
   graded objects: gr R from the Jacobson radical and gr G from the exponent-p central series (p. 1).
   *Does not contain:* Rees algebras, a parameter t, evaluation at fibres, homogenization of a
   sub-object, or any treatment of non-graded inputs other than passing to gr. The input is assumed
   graded from the start.
2. **J. B. Wilson, "Longer nilpotent series"**, arXiv:1303.3157v1. The journal reference on arXiv
   is J. Group Theory 16(6) (2013) 875–897; this appears to be the paper the brief calls "More
   characteristic subgroups, Lie rings, and isomorphism tests for p-groups" (title of the published
   version not seen). FULL: §3 (filters, Thm 3.3), §5 (isomorphism testing, Thm 5.1), §6.4. Keyword
   scan of the rest. *Contains:* filters φ: M → subgroups with [φ_s, φ_t] ≤ φ_{s+t}. It also gives
   the associated M-graded Lie ring L(φ) = ⊕ φ_s/φ_s^+ (Thm 3.3; for M = N it credits Lazard
   1954, p. 106), and covering groups in the nilpotent quotient algorithm (§5). *Does not contain:*
   Rees algebras, homogenization, or evaluations. Here "covering group" is the p-covering group of
   the nilpotent quotient algorithm, not a graded cover. The graded object is always the
   associated-graded quotient.
3. **J. Maglione, "Efficient characteristic refinements for finite groups"**, arXiv:1607.01344v1.
   Keyword scan, plus the passages on L(η) and L(γ) (around pp. 8–9). Associated graded only.
   **J. Maglione, "Filters compatible with isomorphism testing"**, arXiv:1805.03732v4 ("to appear in
   J. Pure Appl. Algebra"). FULL: abstract, §1 including Theorems A–D; keyword scan of the rest.
   *Contains:* conditions under which every group isomorphism lifts from a graded isomorphism of
   L(φ) (Thm A). The abstract warns that the graded Lie ring "may share few features with the
   original group". *Does not contain:* Rees algebras or any cover. The lifting runs from gr back to
   G, which is the opposite direction to the Rees cover.
4. **Brooksbank–Maglione–Wilson, "A fast isomorphism test for groups of genus 2"**,
   arXiv:1508.03033v1. Keyword scan, plus §5.3.2 where L[t]/(t^e) occurs. The only t is the
   coefficient ring K = L[t]/(t^e) of an adjoint algebra (the ΓL(1,K) sequence (5.8)), which is
   unrelated. The setting is class 2, where groups are automatically graded. Their tensor and
   adjoint papers (e.g. "Groups acting on tensors", arXiv:1210.0827) were **not opened**.
5. **Grochow–Qiao, "On p-group isomorphism: search-to-decision, counting-to-decision, and nilpotency
   class reductions via tensors"**, CCC 2021 (LIPIcs 200, paper 16), Dagstuhl PDF; also
   arXiv:1907.00309 (keyword scan). FULL: §1.2 (techniques), §1.2.2; keyword scan of §6.3. *Contains:*
   a reduction from class c < p to class 2 via the constructive Lazard correspondence and tensor
   isomorphism-completeness. *Does not contain:* gradings, filtrations or Rees constructions. The
   class reduction goes through tensors, not through grading.
6. **Y. Cornulier, "Gradings on Lie algebras, systolic growth, and cohopfian properties of nilpotent
   groups"**, Bull. SMF 144 (2016) 693–744; arXiv:1403.5295v5. FULL: §1.2.1 (pp. 3–6), §3.1
   (Remark 3.2), §3.2 (Defs. 3.3–3.4, Prop. 3.5, Cor. 3.6, Lemma 3.10). *Contains:* that Z-gradings
   correspond to GL_1-actions (p. 4); contractable (positive grading) versus Carnot versus
   characteristically nilpotent; the associated Carnot-graded algebra Car(g) = ⊕ g^(i)/g^(i+1)
   (Def. 3.4); and Lemma 3.10, valid in characteristic p when the class is at most p+1. *Does not
   contain:* a graded cover, a Rees construction or any algorithm. This is the best citable source
   for "non-gradable means no positive grading, hence no dilations".
7. **Kochetov–Koval, "Generic graded contractions of Lie algebras"**, J. Algebra 696 (2026) 245–277;
   arXiv:2506.00610v2. FULL: §1 (introduction), §2.2. *Contains:* contractions
   [x,y]_t = U_t^{-1}[U_t x, U_t y] (eq. 1); generalized Inönü–Wigner contractions with
   U_t = ⊕ t^{n_s} Id (eq. 2); Remark 2: such a contraction is associated with a filtration, and gr L
   is isomorphic to the contracted algebra L_0. It also cites Saletan 1961 and Inönü–Wigner. *Does not
   contain:* a Rees module of a subalgebra, or several fibres used together.
8. **Decker–Eder–Levandovskyy–Tiwari, "Modular techniques for noncommutative Gröbner bases"**,
   arXiv:1704.02852v1; published as Math. Comput. Sci. 14(1) (2020) 19–33 (venue from a citing
   paper and MaRDI; the journal version was not opened). FULL: §2.3–2.4 (pp. 5–7), Thm 8 and Def. 9.
   *Contains:* the Rees algebra R_ωA = ⊕_d (F_d A) t^d ⊂ A[t] of a filtered G-algebra (G-algebras
   include universal enveloping algebras). Def. 9 defines the homogenization of a left ideal I as
   I^h = ⟨f^h | f ∈ I⟩ = ⊕_d (F_d A ∩ I) t^d, with dehomogenization F ↦ F|_{t=1}, and eq. (3)
   gives I^h = ⟨f_i^h⟩ : t^∞. It treats increasing filtrations; the lower central series is
   decreasing, but the identity is the same. *Does not contain:* evaluation at several t, or oracles.
9. **Etingof–Ma, "Lecture notes on Cherednik algebras"**, arXiv:1001.0432v4, §2.9 "Rees algebras"
   (pp. 11–12) and §2.10. The definition is Rees(A) = ⊕ F^n A over k[ħ], and §2.10 reduces modulo
   ħ. These are lecture notes, so a weak citation.
10. **Shpilka–Yehudayoff, "Arithmetic circuits: a survey of recent results and open questions"**,
    FnT TCS 5(3–4) (2010) 207–388; authors' version via an IIT Kanpur course page. FULL: §2.2
    (Thm 2.2, Strassen homogenization) and §2.5 (Thms 2.11–2.12). *Contains:* the step "multiply each
    variable by y, evaluate at R+1 values of y, interpolate to recover H_i" in the sketch of proof
    of Thm 2.12 (p. 22). This is the polynomial version of the Vandermonde step in
    `lem:homogeneous`.
11. **M. Lazard, "Sur les groupes nilpotents et les anneaux de Lie"**, Ann. Sci. ENS 71 (1954)
    101–190 (Numdam). Keyword scan of the whole text, plus the introduction and Ch. I §2 (graded Lie
    rings of N-series) and the passage around Déf. (2.5) (homogeneous components in the free
    completed Lie algebra). *Contains:* associated graded Lie rings of N-series and the
    filtered-to-graded passage. *No* Rees algebra, *no* t-parameter, *no* dilation used as a tool
    (OCR scan only; a French reader should confirm).

Not opened, therefore UNKNOWN (TRAPS rule 10): Cicalò–de Graaf–Vaughan-Lee, J. Algebra 352 (2012)
430–450 (gated, no arXiv version found); Eick–Leedham-Green–O'Brien, Comm. Algebra 30 (2002); any
Eick/O'Brien/Vaughan-Lee Lazard-algorithm paper; Saletan 1961 and Inönü–Wigner 1953 (original
papers); Rothschild–Stein 1976 and Folland 1977 (lifting to free nilpotent groups); Brooksbank–Wilson
tensor papers; all textbooks in §5.

## 2. What exactly is standard, and what is not

Write J := E_1^{-1}(h) ⊂ A (the preimage under dehomogenization t ↦ 1). Since E_s = E_1 ∘ δ_s
(Thm `thm:rees-cover`(ii)), E_s^{-1}(h) = δ_s^{-1}(J). Then:

- ĥ = ⊕ t^k (h ∩ γ_k) is **the homogenization h^h of h for the lower central filtration**. This is
  the Lie-subalgebra analogue of DELT Def. 9, and it is the Rees module of the induced filtration
  h ∩ γ_k. Standard.
- ĥ = ∩_{θ ∈ F_p^×} δ_θ(J) is **the largest dilation-stable (that is, homogeneous) subspace of J**,
  the homogeneous core J*. A homogeneous element t^k x lies in J iff x ∈ h. Standard, one line;
  Cornulier p. 4 for the dictionary between gradings and scalar actions.
- That c distinct nonzero points already cut out ĥ is the Vandermonde extraction of homogeneous
  components (SY10 §2.5), with degrees 1..c. Standard.
- The group-level statement needs every E_s and δ_θ to be a BCH group homomorphism (c < p, Lazard).
  This is standard Lazard theory, already credited to Khukhro and Lazard in the paper.
- **Not found anywhere I read:** using these identities when h is *unknown* and reachable only
  through a hiding function f. The c queries f∘E_{s_i} produce a hiding function for h^h on a graded
  group, so the dilations act as public automorphisms preserving the hidden subgroup. They act on
  the cover, not on G (for Dixmier–Lister they cannot act on G: `prop:dl-central-scalars`). All CGT
  sources read here go the other way: they pass to the associated-graded **quotient**, which loses
  information and needs a lifting theory (Wilson §5, Maglione Thm A, BOW §1).

One precision the paper may want: A is the positive part ⊕_{k≥1} t^k γ_k. It is not closed under
multiplication by t, so it is not the flat F_p[t]-family of the textbook "deformation to the
associated graded". Its "special fibre" E_0 is zero, not gr L. The paper already says that grade one
is tL, not L/[L,L], and it never uses gr L as a fibre. So the paper is consistent, and should not
borrow the "deformation to gr" phrase without that caveat.

## 3. Strongest "already known" case (hostile referee)

"Lemma `lem:homogeneous` is a textbook remark dressed up. ⊕ t^k (h ∩ γ_k) is the homogenization of
h with respect to the lower central filtration: the Rees module of the induced filtration, as in
every treatment of homogenization (e.g. DELT Def. 9, even for noncommutative filtered algebras). The
fact that the homogenization is the largest torus-stable subspace of the dehomogenized preimage is
immediate. Recovering homogeneous components from c dilated evaluations by a Vandermonde inverse is
folklore (Strassen; SY10 §2.5). The lemma is three standard facts and a Vandermonde determinant. The
use of graded Lie rings in p-group algorithms is pervasive (Lazard; Wilson's filters; Maglione;
Brooksbank–O'Brien–Wilson). Lifting a nilpotent object to a graded one to gain dilations is the idea
of Rothschild–Stein lifting in analysis. Querying an HSP oracle through several twisted maps already
occurs in Ivanyos–Sanselme–Santha (the maps φ_j, class two). The descent is Ivanyos–Santha's. I see
no new idea."

Fair reply, which the paper mostly already makes (§1.3 "What is new, and what is not"):

1. Concede all the algebra and cite it (§4).
2. Say that the new element, if any, is the *oracle* use. Homogenization is applied to an unknown
   subgroup accessible only through f, at the cost of c queries, and produces public dilations
   preserving the hidden subgroup for groups that have none (Dixmier–Lister). None of the CGT papers
   read contains this.
3. Do not claim the Rothschild–Stein analogy either way until someone reads it. It is UNKNOWN. If it
   is cited, it is cited as an analogy (a graded cover giving dilations), not as prior art for the
   oracle step.
4. The ISS twists are automorphism-type maps of G at class 2. The Rees cover uses homomorphisms from
   a different, larger group A to G. The 11-02 note already records this distinction.

The referee's charge that the step is elementary is fair and should be conceded. The charge that the
oracle use is already published is not supported by anything I opened.

## 4. Suggested citations and wording (for the integrator; the paper is not edited)

Suggested sentence for §1.3 or Related Work:

> The cover A is the positive part of the Rees algebra of the lower central filtration, and
> ĥ = ⊕ t^k (h ∩ γ_k) is the homogenization of h for the induced filtration, the Lie analogue of the
> homogenization of an ideal [DELT, Def. 9]. That c evaluations cut it out is the usual
> interpolation of homogeneous components [SY10, §2.5], and a positive grading is the same as a
> scalar action [Cor16, §1.2.1]. These facts are standard. What we have not found in the literature
> is their use to turn a hiding function for an unknown subgroup into a hiding function, on a graded
> cover, for a subgroup that every dilation preserves. Graded-Lie methods for p-groups pass to the
> associated graded quotient instead [BOW19, Wil13, Mag21].

Citations, in order of preference:

- Homogenization / Rees module: DELT, Math. Comput. Sci. 14 (2020), Def. 9 (arXiv v1 numbering; a
  human should check the journal numbering). A commutative-algebra textbook would be better for a
  referee (see §5), but none was opened.
- Gradings ↔ scalar actions; non-gradable / characteristically nilpotent: Cornulier, Bull. SMF 144
  (2016), §1.2.1, Def. 1.5, Lemma 3.10.
- Interpolation of homogeneous parts: Shpilka–Yehudayoff 2010, §2.5 (proof of Thm 2.12).
- Contractions as filtration families (optional): Kochetov–Koval, J. Algebra 696 (2026), §2.2,
  Remark 2.
- Graded methods in p-group isomorphism, for contrast: BOW, Trans. AMS 372 (2019), §1; Wilson, J.
  Group Theory 16 (2013), §3 and Thm 3.3; Maglione, J. Pure Appl. Algebra (2021), Thm A (volume and
  pages not verified).

## 5. Textbook candidates (NOT opened; locators unverified)

These are the sources a referee would most readily accept. A human with library access should pick
one and fix the locator: Eisenbud, *Commutative Algebra with a View Toward Algebraic Geometry* (the
Rees algebra and the deformation to the associated graded ring, in the chapter on flat families);
Cox–Little–O'Shea, *Ideals, Varieties, and Algorithms* (homogenization I^h of an ideal, in the
chapter on projective geometry); Bruns–Herzog, *Cohen–Macaulay Rings* (the ideal I* generated by the
homogeneous elements of I); Kreuzer–Robbiano, *Computational Commutative Algebra 2*
(homogenization); Li–van Oystaeyen, *Zariskian Filtrations*, or H. Li, LNM 1795 (Rees rings of
filtered rings). I give no section numbers because I did not open them.

## 6. Claim gates that must stay false

- "The Rees cover / homogenization is new." False as algebra (§2).
- "First use of a graded cover in CGT or HSP." Not established: the search is not exhaustive, CDV,
  ELGO and the Brooksbank–Wilson tensor papers are UNKNOWN, and Rothschild–Stein is unread.
- Any citation of the §5 textbooks with a locator, until a human has opened them.

## 7. Next check

Ask a p-group isomorphism specialist (Wilson, Maglione or Brooksbank) one question: "Is the
homogenization of an unknown subgroup through c evaluations of a Rees cover, used to obtain
dilations of a non-gradable Lazard group, known in your area?" Separately, a human should open one
textbook in §5 and the lifting theorem of Rothschild–Stein 1976 (Acta Math. 137), and record whether either states the
oracle-free algebra (expected yes) or anything like the oracle step (expected no).
