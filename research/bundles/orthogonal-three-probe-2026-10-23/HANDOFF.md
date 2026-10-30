# Research And Integration Handoff

The new scientific item is `THREE_PROBE_REDUCTION.md`: a proposed polynomial
quantum reduction for maximal-singular stabilizer HSP in split orthogonal
groups, using only abelian HSP and exact classical certification. It also
contains a scoped full-oracle classical query lower bound. Both need an
independent mathematical review. Do not mark a speedup candidate accepted.

## What Was Actually Implemented

- Public odd-prime E_e(w) probes, hyperbolic complements, neighbor/intersection
  reconstruction and a deterministic final certificate.
- A controller receiving only an opaque-label oracle; no hidden L argument.
- A DENSE REFERENCE for coset preparation and Fourier sampling. It spends
  p^(2n-2) classical oracle queries per probe and retains its full table.
  This is explicitly NOT the scalable quantum algorithm's runtime.
- An all-history query/error planner for the proposed standard AHSP schedule.
- Exact geometry, failure-boundary, oracle-fiber and controller tests.

## Review Before Further Expansion

1. Check the kernel lemma, especially its exceptional e-in-L branch and
   the need for the FULL stabilizer promise.
2. Check that three independent quotient classes really suffice; the learner
   cannot access those classes. It relies on an exact final certificate.
3. Attack the certificate with arbitrary maximal singular candidates. The
   elementary Levi alone is insufficient; the extra alternating unipotent
   eliminates the opposite-subspace false positive.
4. Review the full-oracle lower bound with L uniform in the KNOWN graph
   chart. Factor out the universal +/-I collisions before the adaptive
   dummy-transcript coupling. Do not replace this with a probe-only bound.
5. Check literature beyond keyword search. The technique resembles known
   GL parabolic methods; rank three also has an accidental type-A relation.
   The claim may be known or a straightforward application. No novelty
   certificate has been obtained.
6. Seek a useful original source with these exact fibers and opaque access.
   An explicit label gL reveals L at the identity and is classically trivial.
   Another arbitrary random labeling is not an application.

## Mechanical Work For Gemini After Migration

Only after the destination checkout is verified and no longer moving:

- Integrate the theorem note and public arithmetic using existing finite-field
  helpers. Keep the dense reference separate and visibly costed.
- Add a research-proposal artifact with literature links, falsifiers and
  review status, not a discovery admission. Preserve the older cut-list
  retraction and its counterexamples; this does not validate its false claims.
- Expose the result through an existing research-artifact CLI route if useful.
  No UI redesign or sprawling additional registry scaffolding is needed.
- A native scalable implementation would use the existing quantum AHSP
  interface; do not implement it by enumerating the probe's field table.
- Retain n>=3, odd-field, split-form and maximal-subspace guards. The proof
  allows effective extension fields, but this control implementation only
  handles prime fields. No chain-ring extension is established.
- Run the relevant instrument suites and repository validation after
  integration. They were not run during live migration.

The next research pass should scrutinize this argument or find a real source,
not add more primes, graph plots or a second equivalent simulator.
