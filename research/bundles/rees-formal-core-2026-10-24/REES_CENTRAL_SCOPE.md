# Central Instrument: Exact Checked Scope

2026-10-24. This pass closes the finite normalized all-record channel
identity, conditional on explicit group support/cancellation certificates.
It does not close the BCH bridge, supply an efficient cancellation solver,
implement the full Rees HSP algorithm, or establish quantum advantage.

## Why This Was A Real Gap

The existing main `formal/Formal/CentralCharacterDescent.lean` checks an
important but narrower calculation: a fresh uniform address, a transverse
hidden central intersection, and a supplied normalized tensor correlation.
It explicitly leaves complete spectral measurement outside its formal scope.
The external physical-channel audit already supplies finite reference-aware
controls. Repeating those alone would not prove the general channel identity.

The new module supplies 31 theorems and nine definitions/structures. It
derives the normalized correlations from the actual two-sided measured
coset matrix, works for nontrivial intersections, proves measurement Kraus
completeness on arbitrary vectors, and checks every outcome including the
zero-mass outcomes. It then proves the complete adaptive instrument on all
address/reference matrix entries. No uniform-input restriction remains.

## Definitions And Normalization

Let G and C be finite groups, C commutative, with a central homomorphism
e: C -> G. Let H <= G and m = |e^{-1}(H)|. The theorem does not assume e
injective. Only when it is injective may m be called |H intersect e(C)|.
The independent target source has entries

```
rho_H(x,y) = |G|^{-1} 1[y^{-1} x in H].
P_chi v(x) = |C|^{-1} sum_z chi(z) v(x e(z)^{-1}).
tau_chi = P_chi rho_H P_chi^*.
```

The supplied character family consists of homomorphisms to C (the complex
numbers), satisfies chi(z) conjugate(chi(z)) = 1, and obeys the explicit
Fourier identity `sum_chi chi(z) = |C| 1[z=1]`. The module derives pair
orthogonality, Fourier Gram preservation and Kraus completeness. The
character family and its efficient Fourier implementation are not synthesized
by this file. No unknown character-table access is silently granted.

Centrality gives `tau_chi = P_chi rho_H`, proved by reindexing the literal
two-sided sum, rather than assuming that the matrices commute. Its entries
are `coefficient(y^{-1}x)/(|G||C|)` using the previously verified coefficient.
If chi annihilates e^{-1}(H), its mass is m/|C|, and division by that mass
gives a trace-one kernel with correlation chi(z) at h e(z), h in H, and
zero outside H e(C). A forbidden character instead gives the ZERO matrix.
It is never normalized as a positive branch.

`normalizedEntry` is an algebraic definition for all characters; its
trace-one theorem requires the allowed-character premise. A user must not
mistake the definition's name for an unconditional density-state theorem.

## What The Final Theorem Proves

For an arbitrary complex matrix X on an address/reference space and an
independent target matrix tau, literal controlled right translations followed
by target discard have entries

```
output(q,a;r,b) = X(q,a;r,b) sum_x tau(x, x (A(r)^{-1} A(q))^{-1}).
```

For fresh independent targets this correlation is the product of the
individual correlations. The formal `CancellationCertificate` consists of:

- A nonempty active set, allowing other targets to use zero scale.
- An outside-support zero for every active target.
- Inside-support decompositions into a hidden element and a central element.
- Product character phase exactly equal to one on the support relation.

This certificate states group/phase obligations, not an assumed ideal
channel. Its witnesses may be noncomputable proofs. In the intended
application the implemented actions must be computed from PUBLIC data and
the observed labels; the formal theorem alone does not certify that fact.

`central_cq_record` composes the actual two-sided source calculation,
normalization, tensor factorization and controlled discard. For EVERY label
tuple, including forbidden tuples, it proves

```
output_labels(q,a;r,b)
    = probability(labels) X(q,a;r,b) 1[relation(q,r)].
```

`packet_mass_complete` derives the sum of the actual product probabilities
as one. `central_instrument` then sums the above identity over all tuples.
Thus the retained classical label has its actual distribution independent
of the final pinched address/reference matrix. There is no rare-outcome
postselection division, no discarded-record conditioning error, and no
assumption that the reference is unentangled. This is an exact finite linear
map identity, not a numerical test of selected input states.

The source is explicitly a product. Neither identical marginals nor repeated
use of the same target satisfies it. The prior correlated-bank counterexample
still applies. `zero_actions_identity` proves that all identity actions
produce the identity channel, rather than the required coset pinching.

## Finite Falsification Controls

`central_controls.py` uses UT3(F3) x C3 with 81 elements and a rank-two
center of order nine. Sources are constructed by tracing ordinary explicit
hiding labels, not by inserting the claimed output Gram matrix.

The main control uses H = <x,z>, for which the central intersection has
order three. Of nine single labels, three have mass 1/3 and six are zero.
All 729 three-target records are retained: 27 positive and 702 forbidden.
For positive records a bounded exhaustive moment solver supplies nonzero
scales. Impossible records do not require a solver. Ordinary and twisted
sections, and reference dimensions 1, 3 and 9, are tested.

Additional checks cover intersection sizes one and nine, all matrix entries,
correlations at every group element, positivity of the finite measured
matrices, completeness on arbitrary target vectors, and these falsifiers:

- Reusing transverse mass 1/9 loses two thirds of the mass.
- All-zero actions produce the identity channel.
- A linear instead of quadratic moment fails under a twisted section.
- A noncentral measured subgroup invalidates the one-sided reduction.
- An incomplete character family is not trace preserving.

These tests are finite floating-point controls, not research candidates,
oracle separations, quantum executions, or scaling evidence. The formal
theorems, rather than their numerical tolerances, support the general claim.

## Remaining Scientific Boundary

Still NOT formalized or executed:

1. BCH/Lazard functoriality connecting the checked Lie maps to the group
   actions and quotient descent. A Lie automorphism is not silently a
   checked group automorphism.
2. Construction of an efficient public adaptive action and cancellation
   certificate, including SDE existence, runtime and all resource charges.
3. Approximate preparation/implementation errors, gate complexity, or a
   full recursive recovery algorithm. Exact channel equality is not an
   error budget or a reusable oracle/inverse.
4. A general quantum-information API statement using positive-semidefinite
   operators or the diamond norm. The checked objects are explicit finite
   Kraus/vector/matrix formulas; the source coset matrix is specified
   directly. Main-repo source preparation proofs are not imported here.
5. A natural input family surviving the matched classical portfolio, or
   novelty and significance of the resulting algorithm.

No new independent review was requested or performed in this pass. The one
authorized independent Rees review remains a separate earlier artifact.

Do not turn this result into a claim that the full Rees algorithm is proved
in Lean. Do not continue formalizing nearby facts simply to grow the count.
The next research decision should prioritize a genuinely new input/reduction
or decisive classical attack; further formal work is warranted only on the
specific remaining BCH or efficient certificate obligation.
