# Complete native local Kummer images at every prime

2026-11-13. REVIEWED WRITTEN classical polynomial-bit algorithm. The parent
read the complete 898-line odd-prime proposal, repaired its unpaid coarse
clock and coordinate guards, and checked the full independent 510-line
odd-prime proof and the 231-line final dyadic composition review. The
underlying component derivations and primary-source interfaces were
separately checked. No implementation, novelty, speedup or hardness claim.

## Exact contract and scientific purpose

Input: a monic squarefree f in Z[x], degree 2g+1, coefficient bit length B,
a prime p supplied in binary, and failure tolerance eta. Output: a basis
of the COMPLETE Kummer image J(Q_p)/2J(Q_p) in explicit native squareclass
coordinates of Q_p[x]/f, together with polynomial-size finite field/frame
data allowing evaluation and comparison of native elements. Degree one
has the trivial answer. Arbitrary bad reduction is allowed.

The written classical algorithm has time polynomial(g,B,log p,log(1/eta)),
returns the correct complete image or ABORT, and aborts with probability
at most eta. It receives no model, generators, conditioning, splitting
field, exact local-field oracle or local-image advice. Infinite p-adic
points appear only through finite digits and exact source/root-chart DAG
identities. All arithmetic is charged in bits.

This directly removes the local-image blocker from the native global
two-Selmer construction. The strongest classical baseline is already the
mechanism used here: Stoll halving, native local-field arithmetic and
classical divisor operations. There is no quantum advantage in this local
routine. Corpus lookups and the actual Stoll and OM sources preceded it.

## Mechanism and the different finite quotients

Use independent near-infinity formal seeds and fix their closed Z_p span L.
At p=2, fix E=2L in the maximal pro-2 group, initialize the finite quotient's
2-torsion with seed classes and rational branch torsion, and saturate by
halving zero-label nonzero classes. At odd p, fix E=L and use only the
2-primary subgroup of J(Q_p)/E; its 2-torsion is rational branch torsion.
The odd part of J(Q_p)/E is not silently declared trivial.

Keep every old generator. Append triangular relations 2q_new=v for binary
vectors v nonzero modulo 2 times the current subgroup and with zero Kummer
label. Each half doubles the subgroup. Labels reaching dimension g+t at
2, or t at odd p, prove completeness by the finite 2-group quotient argument,
where t is the number of local irreducible factors of f minus one. No
point equality test or exponentially large generator recombination is used.

An exact finite sampler in a known formal subgroup shifts input points by
2sigma in the ORIGINAL E. Uniform geometric tail and local-chart stability
bounds put actual canonical divisors and ALL rational halves in controlled
coordinates with high probability. These sets are never enumerated.
Saturated graph-ideal products and two consecutive weighted RR sections
materialize canonical representatives, including overlaps. A same-class
scalar pencil gives controlled Stoll determinants and resultants.

Every accepted inverse has a visible finite-precision certificate. In
particular an augmented Stoll determinant is insufficient: the separate
Res(U,W) extraction guard is mandatory. A native genus-2 example with
determinant one and Res(U,W)=0 established this acceptance gap and supplied
the repair. The one example does not prove the universal algorithm.

## Explicit precision and characteristic changes

The exact dyadic algorithm and all constants are in
LOCAL_KUMMER_NATIVE_END_TO_END.md. The complete odd-prime substitution is
Section 7 of audits/reviews/2026-11-13-odd-prime-native-interfaces.md.
That proof supplies computable index and group-node bounds, fixed pole
caps, C_mat, C_half, initialization guards and

    C_max=C_mat+C_half+1,
    P_star=P_cert+T0*C_max.

Compute a group node of depth j ONCE at P_star-j*C_max. All source leaves
and frozen native field data have the requisite extra setup precision.
No old-node re-evaluation, polynomial-in-parent-precision recurrence or
symbolic expansion is hidden. Matrix degrees and all precision quantities
are polynomial. A p-adic digit costs O(log p) bits.

Odd-prime changes are substantive: the actual inverse chart uses p^2 and
is localized at 1+p^2 v; integration denominators are charged; the scalar
discriminant coefficient pays N'v_p(N'); root-coordinate guards include
the order-index D loss; exact uniform grid sampling uses capped binary
rejection. Residue roots use one verified nonsquare per residue field and
deterministic later Tonelli--Shanks/Hensel refinement. There is no loop of
length p. The paid proposal's unsupported Lambda^80 clock is NOT used.

Both branches use actual-factor OM identifiers and Okutsu data for the
original f. They do not substitute an approximate root field or assume an
unpaid isomorphism. Finite residue algebra, deterministic uniformizers,
unit squareclass presentations and frozen root balls make the labels
interpretable in the same native frame as arbitrary input elements.

Uniform conditional-on-history geometry/pencil bounds and capped setup
probabilities sum to less than eta. Good events guarantee completion;
accepted algebraic charts give correctness even off those sufficient events.
A failed visibility or clock test aborts, never returns an incomplete basis
labelled complete.

## Proof evidence, falsifiers and next action

- Current dyadic whole-clock review: audits/reviews/2026-11-13-native-dyadic-whole-clock.md.
- Complete odd-prime proof and ledger: audits/reviews/2026-11-13-odd-prime-native-interfaces.md.
- Exact extraction counterexample: audits/controls/dyadic_extraction_guard/.
- Native backend: audits/reviews/2026-11-13-native-local-squareclass-backend.md.
- Explicit operation ledgers: audits/reviews/2026-11-13-canonical-materializer-precision.md
  and audits/reviews/2026-11-13-stoll-half-precision-ledger.md.

The primary chain includes Stoll's actual halving proposition, OM2012
Proposition 3.8/Corollary 3.10 and Theorems 3.14/5.18, and the number-field
Okutsu integral-basis proposition. These supply exact specified interfaces;
passing tests and advisory agent verdicts do not replace their proofs.

Decisive falsifiers remain an accepted chart with the wrong divisor class,
an unpaid inverse/precision loss, invalid original-E relation, biased finite
sampler, or a source interface lacking its stated polynomial refinement.
The next scientific action is global composition and the strongest classical
counterpart, not a broad local implementation or parameter sweep.
