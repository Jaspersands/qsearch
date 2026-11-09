# Brief: proof check of the three Rees extensions

Date written: 2026-11-02. Status: working brief for a stronger model, followed by human review.
Nothing here is established. Do not change claim gates, the manuscript, `STATE.md`, `TRAPS.md`,
`AGENT_HANDOFF.md`, the mechanical plan, registries or outreach drafts. Findings go in new review
files (section 6).

## 1. What is being checked

The core check (`research/audits/reviews/2026-11-01-rees-core-proof-check.md`) found steps 1–5
of `docs/papers/rees-hsp/main.tex` Theorem `thm:main` (line 169) hold under Schedule 1. Its §9
says steps 1–5 do NOT cover three results the paper builds on top of the core:

- **A. Derived-dimension corollary**, Cor `cor:fpt-r` (`main.tex:535–550`). It claims time
  2^{O(r log(r+2))}·poly for r = dim[L,L], with the class NOT fixed, for every p > c. It uses
  Schedule 3 (random column, Thm `thm:random-column`, line 445) when p ≥ 16(r+1)², and the
  Ivanyos–Magniez–Santha small-commutator algorithm (arXiv:quant-ph/0102014, Thm 11) below that.
  Source note: `research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md` §5 (lines 197–213), with §§1–4
  for the random-column machinery.
- **B. Torsion-rank row**, Thm `thm:ring-to-field` (`main.tex:557–580`) and the last row of
  Table `tab:main-regimes` (line 184). For a Lazard ring L ≅ ⊕ Z/p^{e_i} with class c < p and
  R = dim_{F_p}([L,L]/p[L,L]), it claims time 2^{O(R log(R+2))}·poly(B, log 1/ε). It does this
  through the socle Ω_1(G), Cor fpt-r on it, and an outer normalizer recursion with at most
  b = Σe_i calls. Source note: `research/UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md` §§1–3.
- **C. Black-box extension**, Prop `prop:black-box` (`main.tex:583–602`). The paper itself says
  that this "comes from project notes that are still under review; it is not a result of this
  paper". Its route is a Sylow split, then a free-Lie pullback Φ: (F_{s,c}, ∗) → G, then either
  the tuple lift (exponent p) or the ring-to-field recursion (exponent p^e). Source notes:
  `research/FREE_LAZARD_PULLBACK.md` §§2–5 and `research/CLASS_FOUR_PRIME_POWER_INPUT.md`
  §§1–5. The conditional outer envelope is in `research/reductions/rees_hsp_reduction.json`
  under `large_prime_outer_envelope` and `copy_only_outer_envelope`. Note its own false flags,
  for example `covers_small_prime_queries` and `is_total_gate_bound`.

The question for each is the same: given the core (steps 1–5, taken as proved), does the
extension's stated bound hold, under exactly which hypotheses, and with every cost charged?

## 2. Already settled (do not redo)

- Steps 1–5 of the core, for every c < p and every H: core report §§1–7. Take its §4 handoff
  ("Steps 3–5 may assume") and §5.1 schedule table as given. Schedule 3 was checked there only
  for **fixed** c and i.i.d. uniform banks (§5.5). Whether it stays uniform when c grows with r
  is part of item A.
- Priority (who did what first) is out of scope. See
  `research/audits/reviews/2026-11-01-rees-priority-check.md` only for citation keys.

## 3. Questions to answer

### A. Cor fpt-r

A1. **Uniformity in c.** With u = r+1 and c ≤ r+1, recompute the Schedule 3 tree:
    (4u)^{c−1} leaves, the per-bank acceptance bound 1 − 4/μ − 2p^{a−M}, the restart count
    and the error split. Is everything 2^{O(r log(r+2))}·poly with constants independent of c,
    for every p ≥ 16(r+1)²? The step-4 envelope in the core report §6 was computed for fixed c.
    Redo the parts that depend on c.
A2. **Hypotheses.** Check u ≥ c, u > max a_d and a_d ≤ g_d ≤ r, and that g_2 > … > g_c ≥ 1
    gives c ≤ r+1. Check the label-law use: the source note says a bank's labels are not i.i.d.
    after conditioning on its own acceptance, and that the next bank's law comes from
    independence of the states. Confirm that this is enough at every grade.
A3. **IMS fallback.** Read IMS Thm 11 in full text. State its exact hypotheses: input model,
    unique encoding, whether |G'| or generators of G' must be given, error type, and arbitrary
    vs normal H. Does the explicit Lazard chart meet them? Is the time poly(input) + poly(|G'|)
    or poly(input)·|G'|^{O(1)}? Is p^r with p < 16(r+1)² really 2^{O(r log(r+2))}?
A4. **The gap 1 < p ≤ c.** The corollary assumes c < p. Confirm that no case is silently
    claimed for p ≤ r+1.

### B. Torsion rank / ring-to-field

B1. Part (i): L[p] is an ideal, exp L[p] = Ω_1(G), dim[L[p],L[p]] ≤ R, and class ≤ min(c, R+1).
B2. Part (ii): restricting f to Ω_1(G) hides H ∩ Ω_1(G), and Cor fpt-r applies with r ≤ R and
    input size poly(B). This is conditional on item A; say so.
B3. Part (iii), the outer recursion, which needs the most care:
    - H ≤ N_G(H_1), and log N is the idealizer, a linear condition mod p^{max e_i}. Is it
      computable in poly(B) (Smith/Howell form)?
    - **Quotient oracle.** Does f descend to N/H_1 coherently, with left cosets and charged
      reversible cleanup? Can N/H_1 be given explicit structure constants as a Lazard ring of
      class < p in poly(B)?
    - **Rank and class of every section.** Is the derived cyclic rank ≤ R (check the
      "subgroups and quotients" step for finite abelian p-groups), and the class ≤ c < p?
    - **Termination and error.** Are there at most b calls, each with error ε/b, and does
      every nontrivial step strictly enlarge the known part of H?
    - **Readout over mixed orders.** The paper's Z/3 × Z/9 example (line 561) shows annihilator
      readout fails without a complete label set. Confirm that the recursion never relies on it.
B4. Compare with `UNIFORM_RING_TO_FIELD_RANK_REDUCTION.md` §2 ("Public Operations Have Fixed
    Polynomial Degree", "One Original Query Per Local Oracle Query"). Record any place where
    the paper's statement is stronger than the note's.

### C. Black-box extension

C1. **Sylow split.** For a finite nilpotent G, every subgroup is the direct product of its
    Sylow parts, and f restricted to G_p hides H ∩ G_p. What exactly is needed to get
    generators of each G_p (orders of the generators by quantum order finding, factoring those
    orders), and is |G| itself needed? Is all of this charged?
C2. **Primes p ≤ c.** These Sylows are not covered (`covers_small_prime_queries = false`).
    Could Imran–Ivanyos (arXiv:2304.08376, Thm 1, bounded primes, black-box unique encoding,
    exact) cover exactly those parts, giving all-prime bounded-class black-box nilpotent HSP?
    Check their hypotheses from full text. This is a question about correctness and
    composition, not priority.
C3. **Pullback Φ.** Check:
    - Lazard functoriality, so that Φ is a surjective homomorphism for c < p and exponent p^e;
    - rank of F_{s,c} = O(s^c);
    - evaluating Φ coherently by inverse-BCH words with denominators inverted mod p^e. Is the
      word length poly(s) for fixed c, and is the cost charged?
    - The paper says the word compiler covers exponent p in general class, but prime-power
      exponents only for c ≤ 4. Confirm, and state the exact uncovered regime (e > 1, c ≥ 5).
C4. **Exponent p (e = 1).** The tuple lift applied to F_{s,c} with f∘Φ hides Φ^{-1}(H). Check
    the push-forward Φ(Φ^{-1}(H)) = H and the cost in s and c.
C5. **Exponent p^e (e > 1).** Part (iii) of the proposition needs Φ^{-1}(Ω_1(G)), and so the
    relation lattice of ker Φ. How is ker Φ obtained? (It is a normal subgroup hidden by Φ
    itself, so possibly another HSP instance.) Is that step charged anywhere? Check the
    metacyclic counterexample C_{p²} ⋊ C_p in (iii) exactly, at small p.
C6. Check the call cap b(b+1) and the outer exponent 3 + Σ d⌈log₂(d+1)⌉ in
    `rees_hsp_reduction.json` against the written recursion.

## 4. Falsifier hunting

For each item, look for the smallest instance that breaks it, and check it exactly (Sage/GAP
or exact Python mod p):

- **A:** a family where c grows with r and some bank's acceptance or the error split fails.
- **B:** a section N/H_1 with derived cyclic rank > R, or class ≥ p, or a recursion that stalls.
- **C:** a black-box p-group, c < p, e > 1, where Φ^{-1}(Ω_1(G)) or ker Φ cannot be obtained
  within the claimed cost.

Small groups are in GAP's SmallGroups library. A failed claim is a result: report the smallest
instance, and do not patch around it.

## 5. Environment

- Read `research/STATE.md` and `research/TRAPS.md` first. Read `main.tex` and the source notes
  only at the line ranges and sections named above (grep for anything else). Never read
  `research/AGENT_HANDOFF.md` or `research/RESEARCH_PRIORITY_DECISION.md` whole.
- Python `/opt/anaconda3/bin/python`. Sage, GAP, PARI and others: `research/TOOLBOX.md`
  (conda env `qsearch-cas`).
- Papers: fetch arXiv full texts (IMS quant-ph/0102014, Imran–Ivanyos 2304.08376) and cite
  theorem and section numbers. Abstracts and snippets do not support a verdict.
- Scripts go in `research/audits/reviews/2026-11-02-rees-extensions/<item>/`, so they stay
  reproducible (the core check's scripts were left outside the repo). Run long jobs in the
  background with a time limit, and do not end a turn while your own jobs are still running.
- Record `git status --short` before and after any test run, and compare.

## 6. Rules and output

- Write only: `research/audits/reviews/2026-11-02-rees-fpt-torsion-check.md` (items A and B),
  `research/audits/reviews/2026-11-02-rees-black-box-check.md` (item C), and the scripts
  directory above. A session doing only one part writes only its file.
- Do not commit, push, send email, contact anyone, or edit the paper. List needed text changes;
  do not apply them.
- Do not mark anything verified unless it is proved in writing or machine-checked (name the
  checker). Say which parts are only argued.

For each numbered question, report:
- Verdict: Holds / Holds with stronger hypothesis (state it) / Gap / Counterexample / Could not decide.
- Evidence type: proof, exact computation, float check, full-text citation, or argued.
- File and line references, and the reproduction command.
- What a human reviewer must still check.

End each file with:
- the exact statement that survives, with quantifiers, input/access model and every charged cost;
- the Table `tab:main-regimes` row or proposition wording that would match it;
- which claim gates must stay false;
- a ranked list of text fixes.

## 7. Out of scope

- The core steps 1–5, the hidden-codimension remark (`rem:codim`, which relies on
  `BOUNDED_CODIMENSION_HSP_REDUCTION.md` and is a separate audit), the subspace-source section
  (`sec:subspace`), and literature priority.
- Outreach and anything in `docs/outreach/`.
