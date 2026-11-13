# Core paper update for Theorem HSP23: drafted edits (2026-11-14)

**Status: AI-drafted, pending integrator and human review.** One AI helper (Claude). No Git, no network. The
core `docs/papers/rees-hsp/core/main-core.tex` was **not** edited. Files are in `2026-11-14-rees-hsp23-draft/`:
`edits.md` (exact old → new), `new_E3.tex`, `new_E4.tex`, `old_E3.tex`, `old_E4.tex`, and `apply_edits.py`
(applies the edits to a copy and refuses the real path). Sources: the HSP23 note and its referee, and the F23 note
and its referee (all 2026-11-13), the direct-twist note (2026-11-12, Proposition T), and the core.

## Verdict

No sentence of the core becomes **false** under HSP23. This agrees with the HSP23 referee. Three places become
**outdated or misleading**, and one becomes **incomplete**:

| place | status under HSP23 | edit |
|---|---|---|
| l. 230, DRAFT paragraph on F23 | outdated: "p ≥ 5000", the brute force, "only this promise", "we do not know whether it extends to other subgroups of G" | E3: replaced by Remark 1.4 (`rem:free23`) |
| l. 1148, artifacts paragraph | incomplete: it omits the HSP23 note and its referee | E4 |
| l. 104, intro bullet (2) | true, but read with l. 106 ("This paper avoids both obstacles by moving to a cover"), it suggests that free23 needs the cover | E1: one sentence saying the obstacle concerns automorphism alignment only |
| l. 222, "for the others, such as the free two-generator group of class three, we know of no earlier method" | literally true, since HSP23 is not earlier, but it now needs a pointer | E2: parenthetical pointer |
| l. 891, sec:example-class3 | true | E5 (optional): the same caveat as E1 |

Checked and left unchanged: the abstract, l. 143, l. 226, l. 228 (Direct twists), ll. 232–233 (What is new) and the
open problems. `edits.md` gives the reasons. The full version `main.tex` has no F23 paragraph.

## The remark (E3): what it states

* **Theorem HSP23**, with its assumptions:
  * p ≥ 5 and an arbitrary H;
  * a standard oracle, with left cosets;
  * IS Cor 8, resting on Prop 7 and Thms 3 and 5. The proof of Thm 5 is a sketch in arXiv v2 (referee fix 3).
    IS state their oracle for right cosets, and g ↦ f(g⁻¹) converts it (fix 3);
  * Las Vegas roots;
  * an **exact** QFT_p, needed for the branch selection to be correct. With an approximate QFT, an error of order
    (number of samples)·(approximation error) must be added (fix 2);
  * error only in the hard-cyclic case, ≤ (1−s(p))^R, or in the two IS types;
  * IS run with a cutoff and an outside-N candidate, so a trivial image is detected (fixes 4, 5);
  * poly(log p) queries, not O(1) (fix 3).
* **Routes (a)/(b)/(c).** Route (b) runs in quotients that have an abelian normal subgroup of index p. This is
  consistent with l. 222, where such groups need no cover.
* **Consistency.**
  * No H-preserving automorphism is used. The only automorphisms are uniformly random and public.
  * It is not the Proposition T template: the transformed abelian subgroup is non-central and depends on the label,
    and the weights act on coordinates.
  * The only H-dependent quotient is by the central, certified H ∩ γ_3.
* **Scope.**
  * It covers this one group.
  * For the free 3-generator class-3 group, the quotients G/ker λ have no abelian ideal of codimension 1, so route
    (c) fails at its first step. Whether another cover-free method works there is unknown.
  * Theorem 1.2 is uniform over all Lazard groups of class c < p.
  * "Until reviewed by a human, we do not rely on it."
* **Status line.** "proved in the research notes … refereed by AI only … pending human review … novelty has not
  been assessed."

## Compile check (scratch copy; pdflatex, bibtex, pdflatex ×2; TeX Live 2020)

* **Pages:** 57, against a baseline of 56 on the same toolchain.
* **References:** 0 undefined references or citations.
* **Boxes and warnings:** 0 overfull and 0 underfull boxes; 0 LaTeX warnings.
* **Numbering:** the new label `rem:free23` is Remark 1.4. Every other label keeps its number (aux diff).
* **Placement:** the remark falls on pp. 10–11.

## Claim gates

These stay false: "cover unnecessary" (in general, and for free23), novelty, priority and speedup. The remark
describes a cover-free algorithm for one group, conditional on cited theorems and pending human review. It says
explicitly that the paper does not rely on it.

## Adversarial self-check

* **"Does not contradict obstacle (2)".** Route A does achieve label alignment for free23, by weights on chart
  coordinates and without automorphisms. So obstacle (2) is a real obstacle only to automorphism-based alignment.
  E1 says exactly this. A reader could still see E1 as weakening the paper's motivation for this example. That is
  intended, and accurate.
* **"At most about 4200 coset states per attempt, at p = 7".** This is 18m/q_adm + 2, with m = 144 and q_adm(7) =
  0.617, taken from the HSP23 note §A4. q_adm increases in p, and m = 36 when p ≡ 2 mod 3, so p = 7 is the maximum.
  It is an expectation, not a worst case.
* **"The output is a subalgebra of h"** holds through certification. I did not re-derive that every default
  output is certified under an approximate QFT. The remark claims the error bound only for an exact QFT.
* **Not re-checked here.** I did not re-check any mathematics of HSP23 or F23. The remark inherits the referees'
  verdicts, including the open request that a human read Lemma E as a formal identity (stated in E4).
* **"Theorem HSP23" and "F23" in E4** are names in the notes, not theorems of the paper. E4 says "called … there".
