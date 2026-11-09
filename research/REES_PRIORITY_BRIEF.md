# Brief: literature-priority check for the Rees composition

Date written: 2026-11-01. Status: working brief for a stronger model, followed by human review.
This brief does not check whether the composition is correct; that is `research/REES_CORE_PROOF_CHECK_BRIEF.md`.
Do not conclude novelty or non-novelty from search snippets. Findings go in one new file (section 6).

## 1. Question

Is the Rees composition, or the regime it claims to cover, already in the published or arXiv literature?

Output one verdict among:
- **Known**: an existing theorem covers the same statement.
- **Partly known**: named parts are covered; name exactly which.
- **Possibly new in the stated regime**: no covering result found after the search in section 4; state the regime and the conditions.
- **Unknown**: the search could not decide.

## 2. The claim, split into atomic statements

The paper's own summary is `docs/papers/rees-hsp/main.tex`, abstract (lines 83–92), and the related-work
paragraph (line 116). `research/REES_HSP_REDUCTION.md` section 7 (lines 322–364) says the potential contribution
is "their specific composition making an arbitrary ordinary hidden subgroup dilation invariant with only c oracle
calls per source." Compare each atomic statement separately:

- **A1 (Rees homogenization).** For a finite p-group G of class c < p with Lazard Lie algebra L, and an arbitrary
  hidden subgroup H, the Rees tuple cover ⊕_k t^k γ_k(L) with c evaluations per source makes H-preserving graded
  dilations available.
- **A2 (central descent by scalar weights).** Central characters can be cancelled grade by grade from c down to 2,
  using whole-grade solutions of Σ_i s_i^d λ_i = 0 with scalar weights s^d, not binary weights.
- **A3 (readout).** Abelian Fourier sampling on grade one recovers log H exactly for arbitrary H.
- **A4 (growing prime).** A1–A3 hold with p growing, with the prime conditions the paper states.
- **A5 (complexity).** For fixed c, total time is polynomial in n and log p, with no bound on the prime factors of |G|,
  on the exponent, or on the derived length.

A verdict is needed for each of A1–A5, and for the conjunction.

## 3. Known anchors: verify each from full text

The paper cites these. Its characterizations are claims to test, not facts. The bibliography entries are in
`docs/papers/rees-hsp/references.bib`.

| Key | Work | What the paper says it covers | Check |
|---|---|---|---|
| IvanyosSanselmeSantha2012 | Ivanyos, Sanselme, Santha, Algorithmica 62 (2012) 480–498; arXiv:0707.1260 | Nil-2 groups; twisted right actions correct for hidden elements (Prop. 1, Lemmas 5–6, per REES §7) | Read the theorem statements. Is any part of A1–A3 already there? |
| IvanyosSantha2015 | Ivanyos, Santha, TCS 657 (2017) 73–85; FAW 2015 extended abstract; arXiv:1503.09016 | Fixed-degree diagonal-equation algorithm (Section 3); HSP in semidirect products Fp ⋉ Fp^m of constant class (Corollary 8, per paper) | Read Section 3 and Corollary 8. Does the HSP application cover A2 or A4? |
| ImranIvanyos2023 | Imran, Ivanyos, QIP 23 (2024) Art. 14; arXiv:2304.08376 | Exact HSP in nilpotent groups of bounded class with bounded prime factors (Theorem 1); arbitrary-H central-source conversion by zero-sum subsequences (Lemma 2, per REES §7); concluding section asks for an efficient bounded-class, growing-prime method | Read Theorem 1, Lemma 2 and the concluding section. Verify the exact question asked. |
| FIMSS2014 | Friedl, Ivanyos, Magniez, Santha, Sen, SICOMP 43(1) (2014) 1–24 | Paper says: solvable groups of bounded derived length and bounded exponent | Verify the scope from the full text. |
| DeckerHoyerIvanyosSantha2014 | Decker, Høyer, Ivanyos, Santha, QIC 14 (2014) 790–806; arXiv:1305.1543 | Paper says: Fp ⋉ Fp^m of constant class with p growing, hidden subgroups of order p not contained in Fp^m | Verify the statement and whether arbitrary H is excluded. |
| IvanyosMagniezSantha2001 | Ivanyos, Magniez, Santha, arXiv:quant-ph/0102014 | Non-abelian HSP instances; Theorem 11 (per the falsifier review, poly(input + |G′|) for unique encoding) | Verify Theorem 11 and its hypotheses, especially whether |G′| must be small. |
| HallgrenRussellTaShma2003 | Hallgren, Russell, Ta-Shma, SICOMP 32(4) (2003) 916–934 | General framework (representation-theoretic reduction) | Use only to confirm what is already standard. |
| Morales2026 | Morales, arXiv:2608.05321 | Cited in the paper's related work; title on HSP in semidirect products and quasi-Hamiltonian groups | Not yet verified by anyone. Fetch the paper and check whether it covers A1–A5. |
| HoltSubramanian2026 | Holt, Subramanian, arXiv:2609.38085 | Cited as "learning quantum symmetries" | Not yet verified. Fetch and check relevance; probably out of scope. |

The paper also uses DixmierLister1957 (the non-gradable eight-dimensional class-three algebra) and Lazard1954
(the correspondence). These are standard and do not need priority checks.

## 4. Procedure

**P1. Full text first.** For each row of the table, fetch the primary paper (arXiv or journal). Record the theorem
numbers and hypotheses. A snippet or abstract is not enough for a verdict.

**P2. Search.** Use WebSearch (mode `standard` first; `extended` if results are thin). Record every query and
its date. Suggested queries:
- "hidden subgroup problem" p-group "class less than p" quantum polynomial time
- "hidden subgroup" "Lazard correspondence" quantum algorithm
- "hidden subgroup" nilpotent "bounded class" "large prime" OR "growing prime"
- "non-abelian hidden subgroup" Rees OR graded OR dilation
- "hidden subgroup" "central character" Fourier nilpotent class three
- "diagonal polynomial equations" hidden subgroup 2024 OR 2025 OR 2026
- Morales "hidden subgroup problem" semidirect quasi-Hamiltonian
- Papers citing arXiv:2304.08376 or arXiv:1503.09016 (follow-up work on bounded class)

A missing hit is not evidence of novelty. Say so in the findings.

**P3. Claim-by-claim comparison.** For each A1–A5 and each candidate work, mark one of: subsumes, overlaps
(say which part), disjoint, unknown. Cite the theorem number.

**P4. Test the paper's own characterizations.** Check each sentence that describes a prior work (main.tex
lines 110–113 and 116; REES §7 lines 322–364) against the full text. A mis-description is a finding.

**P5. Resolve the conditional caveat.** A third-party summary of Imran and Ivanyos says their bounded-class
result is conditional on a polynomial-time exact method for zero-sum subsequences in Z_p^n. Another summary says
it is unconditional for smooth order. Resolve this from the primary text. The paper cites Theorem 1 as unconditional.

**P6. Growing-prime regime.** For A4 and A5, find the strongest known bound on the primes and check whether any
published result already gives arbitrary H with growing p at fixed class. Identify the first theorem that would
make the claim non-novel, if one exists.

**P7. Growing-class barriers.** The reduction note (section 7) says the route must not evade existing barriers and
must not erase or overrule them. Read the barrier notes in the repo: `research/BOUNDED_CLASS_METABELIAN_HSP.md`,
`research/CLASS_FOUR_HSP_THEOREM_DRAFT.md`, `research/BOUNDED_CODIMENSION_HSP_REDUCTION.md`,
`research/AMBIENT_SECTION_POTENTIAL.md`. Say which barrier, if any, is a published result, and which are internal.

**P8. Bibliography errors.** The bibliography and the text give different years and venues for the Ivanyos–Santha
paper (2015 in the text, 2017 in the entry, FAW 2015 as the extended abstract). Record every mismatch. Do not edit
the bibliography.

## 5. What the pre-brief search found (snippets only, not evidence)

- ISS (arXiv:0707.1260): efficient quantum HSP for nil-2 groups. Snippet confirms class at most two.
- IvanyosSantha2015 (arXiv:1503.09016): polynomial time for diagonal polynomial systems of constant degree over finite fields,
  with HSP applications to certain semidirect products of constant class.
- ImranIvanyos2023 (arXiv:2304.08376): one summary says polynomial-time exact quantum HSP for constant class and smooth
  order. Another summary frames the bounded-class result as conditional on a zero-sum algorithm. Unresolved.

## 6. Output

Write one new file: `research/audits/reviews/2026-11-01-rees-priority-check.md` (untracked). It must contain:

- **Sources table:** each source, marked FULL TEXT, ABSTRACT or SNIPPET, with theorem numbers.
- **Verdict per atomic statement** (A1–A5) and for the conjunction, with the closest prior work and the
  difference in hypotheses.
- **Search log:** queries, dates and hit counts.
- **Mis-characterizations** of prior work in the paper, with the correct statement.
- **Bibliography mismatches** (P8).
- **Proposed wording** for the related-work paragraph (main.tex line 116), written as a proposal. Do not edit the paper.
- **What an expert must still check.**

## 7. Rules

- Read-only with respect to the paper, `references.bib`, the notes, registries, STATE.md, TRAPS.md and claim gates.
- No novelty claim unless the verdict cites a full-text source for each atomic statement.
- No non-novelty claim unless a prior theorem covers the exact statement, with the theorem number and full text.
- The 2026 arXiv IDs (Morales, Holt–Subramanian) must be fetched before they are cited as support.
- Do not contact authors, send messages, or work on the outreach drafts.
- Use the session scratchpad for downloads. Do not use `/tmp`.

## 8. Out of scope

- Whether the composition is correct (proof-check brief).
- Outreach drafts and submission.
- Repo issues unrelated to the Rees composition.
