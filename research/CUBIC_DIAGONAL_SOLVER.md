# Cubic Cancellation From Public Labels, Including Nonbijective Cubing

2026-10-22. Implementation of a published classical arithmetic dependency
and a stronger finite quantum-channel control. NOT a new SDE algorithm,
independent verification of Rees, a general-degree backend or a speedup.

## Scientific Question

The earlier complete Rees replay used F5. Cubing there is a permutation,
so a linear dependence followed by inverse cubing suffices. It did not
exercise the genuine three-coset arithmetic needed at p=1 mod3. Could
that missing arithmetic invalidate the proposed all-prime composition?

The new backend and F7 replay found no counterexample in their tested
scope. They replace hand-supplied cubic witnesses with an input-uniform
construction, not with a search for favorable label lists. The general
theorem and its novelty remain unverified.

## Published Ingredient

[Ivanyos--Santha, Proposition10](https://arxiv.org/pdf/1503.09016) supplies
a cubic solution from (r+1)(3r+1)(9r+1) public columns of equation rank r.
Linear dependencies are classified into three multiplicative cube cosets.
Three recursive levels give disjoint coefficient cells with weighted
axis relations. Alternating over permutations gives cancellation; a
distinguished nonempty cell prevents the zero witness. Negative signs are
absorbed into cube roots. This is a known construction, not our invention.

The existing conservative general-degree arity remains valid and is not
silently replaced throughout the resource reports. No global receiver
query or gate budget is inferred from the selected finite records below.

## Operational Contract

`theorems/cubic_diagonal_solver.py` takes only a prime p>3 and a rectangular
matrix of canonical public field labels. It has no hidden-subgroup,
potential, source-preparation, or expected-answer argument.

- Row compression preserves every input column and its original index.
  The returned moment is checked again on the ORIGINAL equations.
- At p=2 mod3, the separate bijective branch needs r+1 columns. Rank zero
  returns a unit witness. Neither branch pretends to test three-coset work.
- At p=1 mod3, the input count is cubic_arity(r). Extra input columns are
  retained in the output indexing with zero scales when unused.
- A quantum caller can size its bank from the public center-rank bound.
  Rank is compressed only after acquiring labels; lower measured rank
  does not refund already consumed input copies.
- A uniform nonzero field draw is a cube with probability1/3. After K
  independent failed draws the nonresidue sampler explicitly aborts;
  its exhaustion probability is 3^(-K). It never replaces quantum labels.
- Cubic roots use FLINT degree-three polynomial roots and are checked by
  modular exponentiation. There is no field scan, discrete-log oracle,
  factorization of p-1, or enumeration of multiplicative group elements.
- FLINT root computation is still an expected-time arithmetic dependency,
  NOT a locally enforced worst-case clock. The nonresidue cap alone is
  not a total runtime bound. Seeded replays do not certify random failure
  probabilities; use independent randomness for that interpretation.
- Every tensor-axis relation and the distinguished-cell invariant are
  checked before the final alternating combination. Overlapping final
  supports, a bad root, or a nonzero final moment fail closed.

For fixed cubic degree, the public matrices, number of recursive nodes,
and number of degree-three root requests are polynomial in r. Arithmetic
uses arbitrary-size integers. These are structural bounds, not a measured
asymptotic speedup or a practical quantum-resource estimate.

## Existing Controller Integration

`solve_bezout_sde_weights` in `weighted_two_erasure_cascade.py` now accepts
g=gcd(d,p-1)=3, calls this backend and raises its scales to the existing
Bezout exponent u. The final degree-d moment is verified on original
columns. Tests cover d=3,9,15, including a127-bit prime. No phase labels
or hidden parameters are supplied to this adapter.

Unsupported cases still reject: g>3 and the old quadratic backend's
p=1 mod4 case. Thus completing cubic arithmetic does NOT implement the
general fixed-degree dependency used by high-class Rees claims.

This arithmetic routine is classical by design. It cancels known public
character labels; it does not manufacture the unknown quantum states,
read their hidden subgroup, or dequantize the whole receiver.

## Actual F7 Source And Readout Controls

The bounded regular-operator harness now accepts F5 or F7. F7 multiplication
uses the correct inverse of2 rather than the old F5 literal3. Independent
tests compare its group law and dilations with the Lie Rees compiler.

For each of the nonnormal, nonhomogeneous lines X+W and Z+W, the new
`nonbijective_cubic_control` starts from an explicitly constructed lifted
mixed coset density. It computes the full central projectors and actual
normalized conditional operators, asks the cubic backend for scales on
80 public nonzero character records, and contracts their regular traces.
The actual output becomes the next source; it is not replaced by the
expected answer. The second stage uses nine records and the existing
capped quadratic solver. The full final Fourier distribution recovers
the original line, including Z+W lying inside the original derived algebra.

Important scope limits:

- The original F5 ordinary-oracle replay remains. The F7 addition does NOT
  replay all tuple-oracle fibers or lift original source copies.
- Nonzero character records were deliberately selected as legal test
  branches to force genuine cubic arithmetic. These are NOT IID sampling
  statistics or permission for free physical postselection.
- Repeated conditional density matrices represent fresh independent inputs
  to the tensor contraction, not cloning or reusing one physical target.
- The source and quotient spaces are bounded finite controls. Character
  phases are floating point; group laws and SDE witnesses are exact.
- All label tuples were not enumerated. No coherent quantum gate compiler,
  hardware execution, independent proof or new central candidate is supplied.

## Falsifiers And Next Work

Tests reject a linear dependence that is not a cubic witness at p7,
corrupted roots, lying row compression, exhausted randomness, malformed
labels and unsupported reduced exponents. The live arithmetic replay also
checks rank-three matrices with1120 columns at p43 and p=2^127-1.

The concrete missing arithmetic regimes are now explicit rather than
hidden behind successful bijective-cube fixtures. Higher reduced exponents
need the full published collision construction or a genuinely different
proved method. This remains an implementation dependency, not evidence of
a new algorithmic idea. Independent scrutiny of the complete Rees theorem
and a meaningful application remain higher-level scientific obligations.

## Reproduction

```
python -m theorems.cubic_diagonal_solver --write
python -m theorems.rees_complete_instrument --write
python -m theorems.weighted_two_erasure_cascade --write
python -m pytest tests/test_cubic_diagonal_solver.py tests/test_rees_complete_instrument.py tests/test_weighted_two_erasure_cascade.py -q
```

The standalone arithmetic artifact is reductions/cubic_diagonal_solver.json.
The two F7 records are in reductions/rees_complete_instrument.json under
nonbijective_cubic_controls. None of these artifacts clears discovery flags.

Verification this pass:31 dedicated tests PASS (12.72s),121 connected tests
PASS (143.26s), Python/site-JS syntax and all three live workflows pass.
The connected run preceded one additional test-only regression, which is
included in the31-test dedicated rerun. A broader run including the symbolic
phase test module was stopped during collection on an iCloud dataless
dependency, tests/test_metabelian_phase_extension.py. Registry validation
was also stopped while reading dataless research/registry/negative_results.json.
Neither stopped command is a pass. Full repository tests and Lean were not
run; no sync/cache repair or central-registry edit was performed.
