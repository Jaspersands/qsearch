# Brief: independent proof check of the Rees core composition

Date written: 2026-11-01. Status: working brief for a stronger model, followed by human review.
The claim is NOT established. Do not change claim gates, the manuscript, STATE.md, TRAPS.md,
or any registry file. Findings go in a new review file (section 5).

## 1. Claim under check

Source of truth: `docs/papers/rees-hsp/main.tex`, abstract (lines 83–92), main theorem
"Proposed explicit-Lie theorem" (line 169), and the reduction note `research/REES_HSP_REDUCTION.md`
sections 2–5. The summary below is a pointer, not the statement. Read the theorem and the
complexity claim in those files before relying on any paraphrase.

In outline: let G be a finite p-group of nilpotency class c < p, given by its Lazard Lie
algebra L ≅ F_p^m, and let f hide an arbitrary subgroup H ≤ G. The composition builds a
Rees-homogenized tuple cover of L, uses c oracle calls per lifted source, removes grades
c, c−1, …, 2 by central-character measurement, a controlled-right-action channel and whole-grade
SDE solutions, and then runs abelian Fourier sampling on grade one to recover log H.

## 2. What is already known (do not redo)

- **Falsifiers, 31 Oct 2026.** Two steps were refuted: the single-evaluation pullback
  (dilation-invariant only when H ⊇ [G,G]) and product-and-measure (does not add central
  characters). Full record: `research/audits/reviews/2026-10-31-rees-manuscript-falsifiers.md`
  sections 1–2. The paper was rewritten the same day; the pre-correction text is archived at
  `docs/papers/rees-hsp/archive/main-2026-10-31-before-correction.tex`. Check the corrected text.
- **Tests, 27 pass.** `tests/test_rees_hsp_reduction.py` (diagnostic fixtures: UT3(F3) subgroups,
  UT5, UT9(F11), and the UT3(F3)×C3 central-channel check at p = 3 around lines 250–300),
  `tests/test_rees_single_evaluation_falsifier.py` (Proposition 2.3 checked exhaustively on
  19, 39, 220 and 6453 small subalgebras), `tests/tools/test_rees_paper_numbers.py`. The last two
  are untracked. These are diagnostics, not proofs.
- **Lean, formal/Formal/Rees*.lean (10 modules).** Covered: the concrete untruncated Rees Lie
  construction, evaluation, unit dilations, grade-one retention, hidden-subalgebra interpolation,
  the class-three BCH group, central quotients, and the measured receiver. NOT covered, by the
  project's own statement (`research/REES_HSP_REDUCTION.md` section 6; `formal/README.md`):
  general-class BCH/Lazard transport, solver and runtime, original-oracle preparation, final
  recovery with approximate error bounds. Also assumed as explicit inputs: total valid SDE policies,
  exact initial lifted coset supply, independent normalized input tensors, nonzero branch traces,
  active SDE witnesses (in the older receiver modules).
- **Prior art (scope only, not a priority audit).** `research/REES_HSP_REDUCTION.md` section 7 cites
  Ivanyos–Sanselme–Santha arXiv:0707.1260 (nil-2 twisted right actions), Ivanyos–Santha
  arXiv:1503.09016 (fixed-degree diagonal equations), and Imran–Ivanyos arXiv:2304.08376
  (zero-sum subsequences; its general fixed-class result also bounds the primes). Priority is a
  separate brief; do not conclude novelty either way.
- **Growing-class barriers.** Section 7 of the reduction note says the route must not evade
  existing growing-class descent barriers. Starting points: `research/BOUNDED_CLASS_METABELIAN_HSP.md`,
  `research/CLASS_FOUR_HSP_THEOREM_DRAFT.md`, `research/BOUNDED_CODIMENSION_HSP_REDUCTION.md`.
  Part of step 2 is to say whether the composition escapes their hypotheses.

## 3. The five steps

Section 6 of `research/REES_HSP_REDUCTION.md` says that failure of any one of these invalidates the
algorithmic claim. Each step is checked independently. Record dependencies, but keep going if one fails.

### Step 1 — Tuple group and BCH transport, general class c < p

Questions:
- Is the tuple algebra ⊕_k t^k γ_k(L), with the Lazard/BCH law, a group whose exponential image
  matches G on the graded pieces, for arbitrary c < p? Not only for c ≤ 3.
- Is exp(⊕_k t^k (log H ∩ γ_k)) a subgroup, and is it preserved by every graded dilation, with a
  proof valid for every H? Check the bracket closure [h∩γ_i, h∩γ_j] ⊆ h∩γ_{i+j} as well.
- Does the Lazard correspondence give the F_p-linearity of log H that the argument uses?

Where: `docs/papers/rees-hsp/main.tex` section 2 (line 214 onward; Positive Rees cover at line 222;
Dixmier–Lister control at line 267); `research/REES_HSP_REDUCTION.md` sections 2–3 (lines 60–128);
`research/REES_CLASS_THREE_GROUP_FORMALIZATION.md`; `formal/Formal/BCHClassThreeSubgroups.lean`,
`ReesGroupClassThree.lean`; `theorems/rees_nongradable_control.py` (non-gradable class-three fixture).

Produce: a proof a referee can follow, or an explicit counterexample (basis, brackets, c, p) with a
reproducing script.

### Step 2 — Measured channel and central descent, general class

Questions:
- Normalized source: is Tr(ρ_λ R_g) = χ_λ(z) for g = hz ∈ HZ, with the stated normalization, for
  arbitrary K = H∩Z? (`research/REES_HSP_REDUCTION.md` section 4, lines 129–184.)
- Independence: across fresh disjoint sources, does the joint correlation factorize as claimed,
  so the product over targets is what the proof needs? Do not assume it.
- Oracle model and cleanup: the controlled right actions must be implementable with c oracle calls
  per source, and evaluation workspaces must be uncomputed while tuple labels are kept
  (falsifier review section 1, last paragraph).
- Output: is the traced output the mixed coset state of HZ/Z, as claimed, for every positive-probability
  label tuple?
- Growing-class barriers (section 2 above): does the composition escape their hypotheses?

Where: `docs/papers/rees-hsp/main.tex` section 4 (line 356; Pointwise quotient conversion at line 360;
Recursion at line 393) and section 3 (Complete central instrument, line 315); Proposition "Refreshing
correlated coset centers" (line 298); `research/REES_PREMATURE_GRADE_MEASUREMENT.md`;
`theorems/central_character_descent.py` (`check_moment`, `controlled_discard`, `HeisenbergFixture`,
`exhaustive_scale_fixture`).

Produce: a proof of the channel lemma for general class if it holds. Otherwise a counterexample. Also,
a machine check at class three on the Dixmier–Lister algebra at p = 5 over all positive-probability label
tuples, comparing the traced output with the expected quotient coset state. Prefer exact arithmetic
(fractions or cyclotomic fields) over floating point, or state the tolerance.

### Step 3 — SDE step

Questions:
- For the observed labels λ_1,…,λ_M, is there a nonzero solution of Σ_i s_i^d λ_i = 0 with the
  scale sets the paper uses? Check existence under each schedule's prime condition:
  symmetric schedule (a+1)((δ−1)a+1) with p ≥ 16 δ^(2δ+2), δ = gcd(d, p−1); random-column schedule
  M = 4u, p ≥ 16u², with kernel rejection.
- What is the success probability under the random law of labels? Does it depend on the law?
- Arity: is the claimed arity B_d(a) correctly attributed to Ivanyos–Santha? Read arXiv:1503.09016
  section 3 and its theorem statement yourself. The earlier reconciliation was by an automated reviewer.
- The paper labels these schedules conditional (main.tex section 4, Theorems at lines 424 and 444).
  State exactly which conditions remain open.

Where: `docs/papers/rees-hsp/main.tex` lines 410–455; `research/RANDOM_COLUMN_REES_PARAMETER_BOUND.md`;
falsifier review section 3 and the disposition in its section 5; `research/REES_HSP_REDUCTION.md` section 5.

Produce: a verdict per schedule. For small p (for example p = 5 and 7), report how often a random label
tuple admits a nonzero solution under the stated rejection rule, with a script.

### Step 4 — Complexity envelope, end to end

Questions:
- Write the total cost as an explicit function of n, c, log p and the arities. Include the original oracle
  queries, the classical solver calls, the complete instruments and the final Fourier readout.
- The reduction note gives original queries = c·(n+t)·Π_{d=2..c} B_d(r_d) with
  B_d(r) = [d^{d(d−1)/2}(r+1)^d]^{⌈log₂(d+1)⌉} (`research/REES_HSP_REDUCTION.md` section 5;
  falsifier review section 4). Check it is the full cost and that r_d is bounded polynomially.
- Where does p enter? Growing p must be paid for in bits, and the prime condition must hold.
- Error budget: check the composition across the c−1 stages. The paper charges solver aborts at
  ε/(3N_solver) with a Markov cap, and each complete instrument gets an approximation share. Check that
  these add up to the claimed success probability.

Where: `docs/papers/rees-hsp/main.tex` section 4, Recursion (line 393) and the three schedules (line 410),
with the budget bullets at lines 402–406; section 5 (line 456, resource bounds; line 479, profiles);
`research/REES_HSP_REDUCTION.md` section 5 (lines 186–228); `theorems/central_character_descent.py`
(`tree_budget`, line 182).

Produce: one written envelope with every factor, and a script that evaluates it at several (n, c, p) and
compares with the paper's stated form.

### Step 5 — Final readout and preserved H

Questions:
- After removing grades c..2, does grade one give exactly log H? The tuple hides ⊕_r t^r(h∩γ_r), so grade
  one is h itself, but check the terminal quotient. The falsifier review says the pre-correction text used
  L/[L,L] at line 330, while the actual terminal quotient is tL. Check the corrected text.
- Does abelian Fourier sampling on the terminal quotient recover h exactly, and does classical
  post-processing recover H = exp(h) (not only h modulo some subspace)?
- Approximate error bounds for the final readout are listed as outside the Lean formalization. Does the
  claim need them? If so, state the bound.
- Is H preserved at every quotient of the recursion (falsifier review section 3)?

Where: `docs/papers/rees-hsp/main.tex` section 4, Pointwise quotient conversion (line 360) and the terminal
step; `research/REES_HSP_REDUCTION.md` section 3 (lines 91–128), section 5 (lines 186–228), and the readout
section at line 293; `formal/Formal/ReesCentralQuotient.lean` (terminal retention, around lines 334–347).

Produce: a verdict; the exact terminal quotient; an error-bound statement for the readout. If the paper and
the proof disagree, write the proposed correction into the findings file. Do not edit `main.tex`.

## 4. Environment

- Python: `/opt/anaconda3/bin/python`. Use `python -m pytest -p no:cacheprovider`.
- Sage: `/opt/anaconda3/envs/qsearch-cas/bin/sage` (the falsifier review's exact check used it).
- Lean: `lake` at `/Users/jaspersands/.elan/bin/lake` (toolchain v4.35.0). Build in a COPY of
  `formal/`, because lake writes `.lake/`. Never build in place.
- Scratch: `/private/tmp/claude-501/-Users-jaspersands--claude-spares-spare-plCTD2/e88bfe41-4971-4b70-8898-8c87a7f17e74/scratchpad/<step>/`.
  Do not use `/tmp`.
- Git hygiene: before any test run, record `git status --short`; after the run, compare. Some tests once
  overwrote tracked report files when run with default paths, and the two known cases have been fixed.
  Check any test you run.

## 5. Rules and output

- Read-only with respect to everything in section 2 and all `research/*.md` notes, registry files,
  `STATE.md`, `TRAPS.md`, `docs/papers/`, and every test expectation.
- Write only one new file: `research/audits/reviews/2026-11-01-rees-core-proof-check.md` (untracked).
- Do not commit, push, send email, or contact anyone.
- Do not mark anything verified unless it is machine-checked (name the checker: Lean build, exact script,
  or Sage) or proved in writing. Say which parts are only argued.
- A failed step is a result. Report it with the smallest reproducing instance. Do not patch around it.
- Do not fix the paper's prose. List the needed changes instead.

For each step, report:
- Verdict: Holds / Gap / Counterexample / Could not decide.
- Evidence type: proof, exact computation, Lean, float check, or argued.
- File and line references.
- The reproduction command.
- What a human reviewer must still check.

Then give an overall summary. Say which steps block the claim, which are conditional and on what, and a ranked
list of what to fix first.

## 6. Out of scope

- Literature priority (separate brief).
- Outreach, submission, or any drafts in `docs/outreach/`.
- Repo issues unrelated to the Rees composition.
- Rewriting old REES notes. Note them only.
