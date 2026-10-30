# Research State

Read this page and `research/TRAPS.md` at the start of every Codex research
pass, instead of rereading `AGENT_HANDOFF.md` or
`RESEARCH_PRIORITY_DECISION.md`. Search those two by term when you need
history; never read them whole. `research/GOAL.md` is the binding owner
policy. Paths below are relative to `research/`.

Rewrite this page at the end of every pass. Replace stale lines instead of
appending, and keep it to about 120 lines. Detail belongs in the topic notes.

As of 2026-10-30 21:45 AEDT, after the handoff entry
"2026-10-30 Genus-Two Plus Quotient And Reverse Classical Attack". Check
with `grep -m1 '^## 20' research/AGENT_HANDOFF.md`; several entries share
a date, so compare titles.

## Now

- **Top open question:** solve or decisively bound an affordable mixed-prime
  multiplier selector for Nrd(x) = aN - (a+1)^2 with x in
  b + a*ell*q_0 + a*ell*R*O, then the actual charged geometric quotient and
  joint marked canonicalization. "Affordable": for every prime power s^e
  dividing N, the full-torsion degree (ord_(s^e)(-11) over F_121 for the
  current fixtures) and the quotient cost (Lubicz-Robert: O(s^2 log s) at
  genus two) are polynomial in the input size. Polynomial bit length of N
  is not enough. Details: `SIEGEL_CAYLEY_REPOLARIZATION.md` sections 5-6.
  The weak input is `SIEGEL_ELEMENTARY_REPOLARIZATION.md` section 1, and
  the conversion it needs is section 6.
- **Comparators.** Selector: KLPT and Wesolowski sections 5-6, under
  matching hypotheses (`tools/corpus/cli.py baselines "KLPT"`). Record
  which hypotheses fail; "use KLPT" is not a reduction. End to end:
  whenever the target model exposes computable polarized automorphisms,
  run `theorems/siegel_reverse_transport.py:kernel_from_reverse_transport`
  (`SIEGEL_REVERSE_TRANSPORT_ATTACK.md`).
- **Stop rule:** if no affordable selector route emerges, stop adding
  quotient plumbing and compare another native application (section 7).
  Default budget, set 2026-10-30: one pass. If it ends without a candidate
  selector and a proof sketch of its bound, apply the stop rule, or extend
  once with the reason written here. Small sweeps only falsify.
- **ePrint 2026/1142,** the closest prior-art lead, stays unread. Its full
  PDF was inaccessible by ordinary requests, and the public slides start
  from two encoded PPAVs (section 6). Retry only with a new access route.
- **What a win would mean:** a weak-input source for the known degree-two
  hidden polynomial graph problem (HPGP) receiver. It would not use a
  distinctive Rees receiver.
- **Already ruled out as next steps:** dummy converters, a tiny q-search
  backend, free field extensions, per-level canonicalizers, more SDE
  backends, and repeating the literature search already recorded.

## Live

| Direction | Where it stands | File |
|---|---|---|
| Weak-input genus-two repolarization | The Cayley plus-quotient fixes the polarization algebra. Still unpaid: the norm selector, the quotient and canonicalization. The six saved ell=61 lifts need huge torsion fields. | `SIEGEL_CAYLEY_REPOLARIZATION.md` |
| Reverse-transport classical attack | Comparator for the row above. Scalar or commuting u can give zero, and the original input need not expose a useful u, so it is not a general break. | `SIEGEL_REVERSE_TRANSPORT_ATTACK.md` |

## Parked: reopen only with a new input, theorem or application

| Direction | Why parked | File |
|---|---|---|
| Rees nilpotent HSP cover reduction (c<p) | Proposed fixed-class, growing-prime polynomial-time composition, pending independent correctness and priority review. Reviewed only by AI, and no native application. See the `main.tex` issue below. | `REES_HSP_REDUCTION.md` |
| Rees applications | None survived. Needs a motivated native residual family plus a decoder. | `audits/reviews/2026-10-30-rees-application-selection.md` |
| Siegel/symplectic HSP reductions | Waiting on a useful source, which the first Live row is meant to supply. | `SYMPLECTIC_CHAIN_RING_DIGIT_REDUCTION.md` |
| SDE solver campaign | Stopped. The regular-pivot backend was declined because Boolean enumeration matches it. | `PIVOT_REGULARITY_DECISION.md` |
| Inverse-trace uniform sampling | No useful reduction needs the full law. No more backends. | `INVERSE_TRACE_SAMPLING_DECISION.md` |
| Mersenne reciprocal-trace | Published machinery, no reduction, classical witnesses. | `MERSENNE_TRIAGE_DECISION.md` |
| Quaternion compact-orbit receiver | No polynomial decoder, and Cartesian readout is classically simulable. Re-entry needs a native family with an affordable contraction. | `QUATERNION_ARITHMETIC_RECEIVER.md` |
| Arithmetic orbits (pencils, tensors, PIP) | Known machinery or classical. Needs a native problem whose format grows. | `ARITHMETIC_TENSOR_DIRECTION_AUDIT.md` |
| Goppa quantum access | Needs a quotient map that preserves the characteristic. Held-out readout costs 2^rank postselection. | `GOPPA_LOCAL_QUOTIENT_PRESENTATION.md` |
| Parabolic / Lie-type matrix HSPs | n=3 (SO6/SL4) is prior art. Recovery for n>=4 orthogonal is proposed, with novelty unresolved. The 10-11 negatives are withdrawn. | `PARABOLIC_CUT_LIST_CORRECTION.md` |
| DQI/OPI-family decoders (OPI, polar Gibbs, MPI, Hermite, chirp) | Each tested decoder met a classical competitor or prior art. MPI is a failed transfer, not hardness. Reopen only with a consequential problem. | `HERMITE_DECODER_PRIOR_ART.md`, `../docs/papers/classical-competitors/` |
| Ternary/F3 syndrome filtering | Two tested corrections were falsified, and Kothari et al. cover fixed positive density. Structured optimized Q is not excluded (review pending). | `TERNARY_SYNDROME_CORRECTION.md` |
| Other DCP sources and sieves | Reserve only, until a concrete new rule appears. Do not continue DCP by inertia. | `RESEARCH_PRIORITY_DECISION.md`, "Portfolio Comparison" |
| Code equivalence / GI collective observables | No concrete receiver. | `NONABELIAN_BARRIER_SCOPE_AUDIT.md` |
| Symmetry and noisy-phase learning | Scoped learners built on known theorems. | `audits/reviews/2026-10-30-noisy-phase-native-scope.md` |
| Natural dynamics (boson, Fokker-Planck) | Tested readouts matched classically. | `FOKKER_PLANCK_CLASSICAL_BASELINE.md` |

## Closed: do not reopen

| Direction | Killed by | File |
|---|---|---|
| Inverse-trace native search | Classical expected-poly search for any target, odd n>=61 (10-30) | `INVERSE_TRACE_GENERAL_SEARCH.md` |
| Complete AG full-support syndrome (DQI) | Expected-poly classical solver and exact uniform sampler for every complete AG input with odd q>=1019, e>=8, q^2>=44e. Novelty demoted (10-27). Fixed q with e->infinity is still open. | `bundles/two-component-norm-2026-10-27/`, `bundles/norm-sampling-2026-10-27/` |
| Siegel shortcuts (stabilization, supplied Hom/End) | Wrong polarization, and strong lattice advice makes the kernel classical | `WEAK_SIEGEL_CONVERSION_AUDIT.md`, `SIEGEL_ENDOMORPHISM_TRANSPORT_ATTACK.md` |
| Simon DCP decoder (ePrint 2026/1591) | The Lemma 3 step is unsupported, and the October revision is unchanged | `DCP_SIMON_OCTOBER_REVISION_AUDIT.md` |
| Permutation-coset sources (CFI, wreath, bank) | Luks gives poly time, and the wreath is recovered classically | `WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md` |

## Standing owner rules

- `GOAL.md` is binding: Codex does the deep reasoning, and Gemini does
  low-judgment work through `MECHANICAL_FOLLOW_UP_PLAN.md`. No tiny-circuit
  search or toy oracles. Running out of usage is a handoff, not completion.
- No outside contact or submission without explicit owner instruction.
  Everything in `../docs/outreach/` is unsent.
- No registry promotion: `registry/candidates.json` holds 8 unpromoted
  hypotheses, unchanged since 10-09.
- Gemini "Investigations 21-61" are unreviewed (specific records are
  quarantined in `CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md`). Never cite them to
  rule a direction out.

## Where things live

- **Algebra tools:** `TOOLBOX.md`. **Review receipts:** `audits/reviews/`.
  **Classical baselines and certificates:** `classical_baselines/`.
- **Bundles:** the 10-22 to 10-27 working bundles that the handoff cites
  under `~/Developer/qsearch-research-work/<bundle>/` are copied, text only,
  to `bundles/<bundle>/`. See `bundles/README.md`.
- **Tests:**
  `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error <tests>`.
  `../tests/KNOWN_FAILURES.txt` lists the 134 tests that already fail.
- **iCloud:** the repo is on an iCloud Desktop. Put `timeout` on long reads;
  a hang usually means an evicted file.

## Known open issues

- `../docs/outreach/05-rees-personalized-emails.md` flags a possible gap in
  `../docs/papers/rees-hsp/main.tex`: pi^-1(H) is not dilation-invariant.
  Both files are local and untracked. The gap is not yet in the handoff.
- `NEG-CHARACTER-SHIFT-UNIFORM-DECODING-LOWER-BOUND-BARRIER` (10-11) says it
  proves a uniform Omega(p) classical lower bound. Its proof
  (`CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND.md`, Theorem 4) covers only
  candidate-testing algorithms and assumes Legendre PRF hardness. Treat it
  as conditional, and never cite it as hardness.
