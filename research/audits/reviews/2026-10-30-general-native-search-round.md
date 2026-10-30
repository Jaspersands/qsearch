# Five-Agent General Native Search Round

30 October 2026. Classical dequantization of the arbitrary-target SEARCH
sequence, not a quantum breakthrough, a novelty certificate, or expert
peer review. The earlier five-agent trace-affine round is separate.

## Assignments And Outcomes

| Agent | Scope | Result |
| --- | --- | --- |
| Kuhn the 2nd | Find a valid short-block acceptance proof | Located Sawin--Shusterman 2512.24080v1, derived the new absolute first moment, checked the explicit growing-degree constant and conductor definition. |
| Dalton the 2nd | Attack partition legality and matched classical baselines | Retained original K, verified native words, exposed fast n17 flat baselines, and supplied deterministic conditional-expectation balancing. |
| Hubble the 2nd | Challenge the surviving quantum sampling task | Separated full-fiber ideal sampling from biased classical search; bounded the union of full-support norm families without claiming a general classical lower bound. |
| Franklin the 2nd | Independent audit of characteristic-two sheaf prerequisites | Checked middle extension, monodromy, wild infinity pullback and Fourier conductor; B6 suffices, so conservative B8 is valid. |
| Planck the 2nd | Independent counting, constants, threshold and implementation audit | Checked all expansion cases, zero-frequency subtraction, balancing, odd n61 threshold, proposal costs and exact-arithmetic implementation. |

IDs in that order:

```
01a18b3d-4e20-7d61-a37c-9a982fbd4d1d
01a18b3d-4eba-7b92-b203-fe9f14f36e6b
01a18b3d-4f1c-74c1-b219-04a4102830d7
01a18b48-01eb-71a1-aad8-f7013337b692
01a18b48-0279-7b03-9fa4-7631f66c7857
```

All were read-only and are now closed. Parent implemented and integrated.
The two final proof reviews had complementary scopes and did not each
claim to verify every imported theorem. No service was contacted to
submit a manuscript, and no parent commit or push was made.

## Surviving Result

Read INVERSE_TRACE_GENERAL_SEARCH.md for the full proof. Deterministic
balancing reduces ANY target pattern on ANY distinct native point set
to two trace-affine blocks of sizes[(n^2-n)/2,(n^2+n)/2], keeping K.
The new trace-sum theorem establishes an absolute first-moment error
at most2*24^M*q^((3K+3-M)/2). The old divisor second moment then pays
rejections and allocation multiplicity. At every odd n>=61, expected
proposals are at most8*(binom(e0+3,3)+binom(e1+3,3))=O(n^6).
Each proposal has polynomial expected cost. This is an expected-polynomial
classical search algorithm, not deterministic runtime or uniform output.

The original randomized balancing suggestion gave a more conservative
n103 threshold. Dalton's constructive balancing improved it to n61;
Planck checked the analytic all-n inequalities, not merely a finite table.
Franklin found a wording overreach: polynomial classical search rules out
a superpolynomial separation based on search hardness, not every possible
polynomial quantum speedup. The proof now states the narrower conclusion.

## Concrete Controls

- Fixed singleton n17 input: selected145 coordinates, SAME K36,
  2 norm proposals,27.178667s; full original witness retained.
- Fixed18-one n17 input: blocks139/150, SAME K36,23/13 proposals,
  13.237835/9.102800s; both certificates and failed trials retained.
- Matched d3 flat baselines, seed17022, cap32, solve both original inputs
  in0.592628/0.534356s, each binary rank612/612 with867 variables.
  This is measured finite feasibility, not an asymptotic flat-solver proof.
- New exact rational endpoint certificates at n61,63,65 do NOT run
  large-field factorization or native witness search. The all-n theorem
  comes from the proof, not that table.

Regression tests replay the seeded proposal hashes, exact norm identities,
binding to original points, independent binary-field syndromes/traces,
conditional-expectation scores, Fourier first moment, exceptional exponent
cases, certificate rounding, and capped-failure status. A transient test
wrongly expected two solver calls even when one balanced block was all
zero. It was corrected to count only nonzero-target blocks; the valid
zero-block shortcut was not disabled.

Artifacts: inverse_trace_singleton_subinstance_n17.json (already saved
and committed by another process), inverse_trace_sparse_partition_n17.json,
inverse_trace_partition_matched_flats_n17.json, and
inverse_trace_general_search_bounds.json, all under classical_baselines/.
New theorem modules: inverse_trace_affine_partition.py and
inverse_trace_short_sums.py, with corresponding test files.

## Consequence And Remaining Scope

Do not continue advertising arbitrary-target native search hardness.
The ideal full-fiber quantum sampler remains a distinct question, recorded
in INVERSE_TRACE_SAMPLING_RESIDUAL.md. Its useful application, novelty and
separation from ALL classical samplers remain unresolved. The direct norm
family's small support is not a lower bound on other classical methods.

Focused final implementation review passed47 tests. See the latest
AGENT_HANDOFF entry for the broader parent replay and any unrelated
failures. No registry candidate or speedup status is promoted by this pass.

Final parent replay after adding the bounds-artifact regression:48focused
tests passed; related broader suite994passed/1failed in62.48s. The failure
is an existing SMT CLI --write omission, reproduced in isolation without
changes to that command. Gemini repair details are in
MECHANICAL_FOLLOW_UP_PLAN.md; no assertion was suppressed. Four Python
compile checks,12siteJS checks,gitdiffcheck and qsearchvalidate passed.
The13registryJSON aggregate is unchanged at
79c8b3fca6c2bb7c70cca8116b8356bc3dc69734c682feeba16a8bbf1949c0fd.
