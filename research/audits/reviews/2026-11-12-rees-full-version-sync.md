# Rees full version: sync with the 12 Nov core changes (2026-11-12)

**Status: AI-made edits, AI-checked, pending human review.** One Claude session acted as integrator.
It edited only the gitignored full version: `docs/papers/rees-hsp/main.tex`,
`appendix-torsion-blackbox.tex`, `appendix-provenance.tex` and `references.bib`. It did not touch
`core/`, `docs/outreach`, `research/STATE.md`, the handoff or any `research/reductions/*.json`.
No git write, no network, and `make_numbers.py` was not run. Claim gates are unchanged.

Backup of the pre-sync files (main.tex, all appendices, references.bib):
`research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-pre-fullsync-2026-11-12/`.

Sources: the core diff (`backup-pre-restructure-2026-11-12/main-core.tex` against
`core/main-core.tex`, re-diffed at the end; the only later core change was the wording of the
`anc/make_numbers.py` item); `2026-11-12-rees-nilpotent-corollary-referee.md` (all 7 findings);
`-utz-finite-index.md`, `-index-p-family.md`, `-priority-algebra.md`, `-priority-quantum.md`,
`-direct-twist-class3.md`, `-eprint-2026-2678-check.md`; and the last two sections of the prep README.

## Ported items (label, status, location in the full version)

| Item | Label / status | Location |
|---|---|---|
| Corollary `cor:nilpotent` with proof | "AI-checked, pending human review"; assumes `thm:is-import`, imports II Thm 1 for p <= c (arXiv v1 numbering) | new §10.2 "Black-Box Nilpotent Groups of Fixed Class" (`sec:nilpotent`), before `thm:bb-envelope` |
| Remark `rem:nilpotent-scope` (a)-(c) | as in the core | §10.2 |
| Corollary `cor:utz` with proof; Remark `rem:utz-scope` (a)-(d), including the H_3(Z) sentence and the `DiConcilioFloresKahrobaeiNoce2026` citation | "AI-checked, pending human review" | new §10.3 (`sec:utz`) |
| Class-three example (`sec:example-class3`) | AI-checked, pending human review; exact checks labelled "finite computation" | new §7.1, at the end of the main-proof section |
| Remark `rem:fewer-points` with proof and the text after it | AI-checked, pending human review; checks "finite computation" | §2.2, after `prop:single-evaluation` and its example |
| "Why interpolation works" paragraph | text | §1.3 (Core Idea) |
| Obstacle (2), "preserve the hidden subgroup, and be public"; obstacle (1) tail; the primer sentence "chosen without knowing H" | text | §1.1 and §1.2 |
| Related Work, rewritten from the core: ISS 2007; BCvD Lemma 1 + Section 4.2 + Thm 6; the index-p caveat (BCvD Lemma 1 composed with IS Cor 8) | the composition labelled **argued** (provenance P-item `prov:related`) | new §1.5 `sec:related` (moved out of §1.2) |
| "Direct twists beyond class two" | argued, not proved | §1.5 |
| "What is new, and what is not": cover algebra standard (DELT Def. 9, Shpilka–Yehudayoff §2.5); algorithmic use not found; not a novelty claim | text | §1.5 |
| II §6 description fixed (referee Finding 1): they ask for a poly(np) zero-sum algorithm; their model is the subgroup-state oracle; the results cover a standard U_f only | text | §1.5, abstract, `rem:nilpotent-scope`, `rem:tb-scope` |
| II Lemma 1 purification; in-place multiplication construction; exact Watrous method "that II §2.2 use (they attribute it to their earlier exact abelian algorithm)" with clean workspace; precision schedule eps/(8j^2); s in the gate bound | applied to `cor:nilpotent` (verbatim from the core) and to `lem:tb-small-primes` (the full version's support for `thm:bb-envelope`) | §10.2; Appendix D, "Primes at most c" |
| c <= 2 unconditional by ISS 2012 | in `rem:nilpotent-scope`(b) and in the new paragraph before `thm:bb-envelope` | §10.2 |
| II numbering follows arXiv:2304.08376v1 | sentence in §1.5 and in the status box | §1.5; front matter |
| Abstract, contributions list, regimes table (new row for `cor:nilpotent`), organization paragraph | updated | front matter, §1.4 |
| Provenance items `prov:related`, `prov:class3`, `prov:nilpotent`, `prov:utz` | new | Appendix "Provenance and Verification Record" |
| Bibliography | `KannanBachem1979` added from the core bib; every core entry now matches the parent identically | `references.bib` |

## Core/full inconsistencies found and how they were resolved

1. **Identity encoding (hypothesis mismatch).** The full version's access model
   (`app:tb-blackbox`) listed "the identity" as given, and `lem:tb-sylow`(d) started order finding
   from z_0 = 1 and tested g^v = 1. The core's `cor:nilpotent` assumes no identity encoding. I applied
   the core's (refereed) version: the access model now says no identity is given, and
   `lem:tb-sylow`(d) uses k -> g_i^{k+1} with a coherent selection (referee check (b)), the tests
   g_i^{v+1} = g_i and g_i^{v/q+1} = g_i, and then the identity g_1^{o_1}. `thm:bb-envelope` now says
   no identity encoding is needed. **Flag:** this changes a full-version lemma; it is not refereed
   separately in the full version.
2. **Hypotheses of `thm:bb-envelope`.** It read only "Fix c", with no import named and no rational
   eps. It now names `thm:is-import`, `thm:power-sde`(ii) and the import of II Thm 1, the standard
   oracle U_f, rational eps, and "nothing about |G|". These match `cor:nilpotent`. The one remaining
   difference is the in-place multiplication oracle with its adjoint, which the full version admits
   (it yields the out-of-place one, per the access model). That is pre-existing and stated in the text.
   The status label is unchanged ("conditional, AI-checked only").
3. **II §6 misdescription.** The full version said II "pose the case of bounded class and smooth
   order as an open problem", and that `thm:bb-envelope` is not claimed to settle it "before it has
   had human review". Replaced with the core's refereed wording, including the oracle-model caveat.
4. **Bacon–Childs–van Dam scope.** The full version said BCvD solve only "hidden subgroups of order p
   not contained in F_p^m". Replaced with the core's statement (Lemma 1 reduction of an arbitrary H,
   Thm 6), and added the index-p caveat.
5. **"If Theorem main is correct, these results are special cases of its regime".** Replaced with
   the core's "the instances ... are instances of the setting of Theorem main ... scope only; bounds
   not implied".
6. **Contribution (1).** It said "the new ingredient is the interpolation of Lemma lem:homogeneous".
   This conflicted with the core's "the algebra is standard; what is new is its use". It now reads
   "the use of the interpolation ..., whose algebra is standard".
7. **Duplicate `Shor1997` in the parent `references.bib`.** This was a pre-existing BibTeX error. There
   were two entries, one with an extra doi note. I removed the first, so the entry matches the core
   identically.
8. **The Outlook claim.** The core says "The full version states the same composition with Schedule 2
   as well, which would give smaller query counts". This is now true. `thm:bb-envelope` is introduced
   as that composition with the combined rule (paragraph "The same composition with the combined rule").
   Its hypotheses match `cor:nilpotent`, as in item 2. It stays conditional on `thm:power-sde`(ii) at
   the Schedule-2 grades. Its counts are never larger, and are smaller when a linear or Schedule-2
   grade occurs.

No mathematical disagreement remains between the two versions in the ported statements. In the
full version, `thm:bb-envelope` splits the error differently from `cor:nilpotent` (quarters as
opposed to eps/4 + eps/2 + eps/4). Both are valid, so this is not a disagreement.

Ancillary-file wording (coordinator request): the status box and the provenance appendix now say
that the full version is the ancillary PDF `anc/rees-hsp-full.pdf` of the core's arXiv source, that
code and data are in the public repository, and that `docs/papers/rees-hsp/` is not public.
`make_numbers.py` is described as `anc/make_numbers.py`. **Flag:** the provenance text still names
`numbers_map.json` and `reproduce.sh`. Whether they ship with the arXiv source has not been checked.
The class-3 check folder (`2026-11-09-rees-paper-pass-prep/class3-example/`) is gitignored, and
`prov:class3` says so.

Not ported:
- The core's Appendix B restructure (the classical proof moved). The full version has its own layout.
- The draft AI-use statement (owner's text, arXiv prep).
- `\pdfoutput=1`.

## Kept

Every `% NEEDS HUMAN VERIFICATION` tag (main.tex 10 -> 11, torsion appendix 4 -> 5). The new tag is
on the clean-workspace exact Watrous preparation (referee Finding 4). All status labels are kept. No
statement is stronger than the core's.

## Compile

Built as README.md says: pdflatex, bibtex, pdflatex, pdflatex, under nice -n 19.
- Result: **222 pages** (211 before), 0 errors, 0 undefined references or citations, 0 BibTeX
  warnings or errors.
- Overfull boxes: one, 5.87pt, in the provenance item `prov:bb-subspace` heading. It is under 10pt
  and was not fixed.

Open for a human: II Thm 1 and Lemma 1; the clean workspace of the exact Watrous preparation; a
specialist priority check of `cor:nilpotent`; and the identity-free `lem:tb-sylow`(d) edit.

## Disposition (integrator, 2026-11-12)

- Inconsistency 1, the rewritten `lem:tb-sylow`(d): checked against the core's refereed
  Corollary `cor:nilpotent` ("Orders" paragraph). It is the same construction: order finding
  on k -> g^{k+1}, a coherent selection that keeps every intermediate register, acceptance
  when g^{v+1} = g (by right cancellation, g^v = 1), and the reduction loop. ACCEPTED. It
  carries the referee of the core version; no separate referee was run on the full-version text.
- The full version, now 222 pp., ships as `anc/rees-hsp-full.pdf` in the core's arXiv source
  package (`docs/papers/rees-hsp/arxiv/build_package.sh`, local). All of it is AI-checked,
  pending human review.
