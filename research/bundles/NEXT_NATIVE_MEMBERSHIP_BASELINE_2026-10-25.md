# Next Pass: Replace Full Source Calls In The Classical Baseline

2026-10-25. RESOLVED AS A CONDITIONAL REDUCTION WITH EXACT ALGEBRA CONTROLS in
native-membership-baseline-2026-10-25. No native geometric interpolation or
unknown kernel recovery was executed. The original lead below is retained
for provenance; do not repeat it as unimplemented research. The successor
note also gives a tight query bound for the Boolean interface alone, NOT
native hardness. Scoped regression: 337 PASS, including 55 new tests.

## Question

Can the small-prime digit attack avoid the new dimension-16 coset-label
source entirely, using the PUBLISHED interpolation algorithm between the
ORIGINAL elliptic target and itself?

The repository already derived a scalar-cancelling conjugation integrality
test in ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md, Section 5. For any
known polarized source endomorphism alpha, gamma=phi alpha phi^-1 descends
integrally exactly when alpha preserves ker(phi), by containment, not
necessarily equality. Do not rediscover that lemma as new.

What is new to connect is the prefix certificate: over the local frame of
a proposed direction, the two required conditions are s*y^2=0 and s*x*y=0.
They can be tested on ONE elliptic factor by the matrices

    U_s=[[1,s],[0,1]],    P_s=s*E11,
    s=q^(d-j).

Conjugate by the candidate SL2 frame at the full q^e level. The first
preserves the local kernel iff s*y^2=0; the second maps it into itself iff
s*x*y=0. The latter is NONINVERTIBLE, which is allowed by the descent test.
On all other primary factors choose a scalar matrix, so containment there
is automatic. Every quaternion endomorphism of an elliptic curve is
polarized by its reduced norm. A surface Cayley lift is unnecessary.

## Public Integral Lifts And One Fixed Weak Transcript

Lift each prescribed residue matrix through O/nO to alpha in O. Since
gcd(n,p)=1, also impose alpha=1 mod pO by coefficient CRT. This ensures
its positive reduced norm N is coprime to p, without revealing any target
order. With coefficients bounded by np and source basis norm sum B0, the
conservative uniform bound Nmax=4*(np)^2*B0 has polynomial bit length.

Choose one odd squarefree prime product P>8*n^2*Nmax^2, excluding primes
dividing np. Precompute the same genuine weak phi images at these levels.
For a particular alpha omit primes dividing N. Their removed product is
at most N<=Nmax, so remaining M>=P/Nmax satisfies

    gcd(M,Nnp)=1,    M>N,    M^2>8*n^2*N.

Thus one uniformly bounded input transcript covers all adaptive prefix
queries. Insufficient existing finite data must remain insufficient; this
uses the original full weak evaluator if extra levels are required.

On each remaining prime r, in the basis Q=weak_phi(P), gamma acts by the
known source action matrix of alpha. The unknown common scalar cancels.
The resulting images are a basis because gcd(r,N)=1. Both modeled PPAVs
for interpolation are E' with its ORIGINAL polarization. There is no
unknown repolarization converter or canonical coset label in this call.

If the interpolator returns gamma0, put

    Delta=n*gamma0-phi*alpha*phi^dagger.

This is integral, kills E'[M], and has Rosati norm at most
2*n*sqrt(2*N)<M. Integral norm positivity forces Delta=0. Hence no distinct
interpolant can create a false membership answer. Conversely, integral
gamma is N-polarized and is a valid interpolant. Preserve this stronger
bound, not just the interpolator's own uniqueness bound.

## Authoritative Check Already Performed

The retained 44-page 2026/1142 PDF, SHA256
4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318,
was reread on pages 36-38. Theorem 7.1 explicitly returns an N-isogeny if
one exists and failure otherwise, with a polynomial bound in input length
and largest prime of M at fixed dimension. Algorithm 6 has bounded loops
and an explicit final verification/failure branch; it is not a promise-only
statement that may run forever on a negative candidate. Its internal product
dimension is 8g, hence 8 for these elliptic membership calls. Still audit
the validity of every candidate torsion-basis and isotropic-kernel input.
Source: https://eprint.iacr.org/2026/1142

## Decisive Implementation And Falsifiers

1. Implement public lifts with the p-coprimality CRT and exact norm bound.
   Test BOTH U_s and noninvertible P_s against supplied Smith subgroups.
2. Check one global prime transcript after per-query norm-factor omission.
   Do not accidentally give an adaptive transcript or ignore field costs.
3. Verify masked target actions from genuine supplied isogeny controls;
   compare positive and negative integral-descent cases exactly.
4. Distinguish published interpolation primitives from an actual installed
   geometric backend. No supplied-kernel predicate may masquerade as it.
5. If the reduction survives, classify the small-prime negative result as
   independent of the new full coset-source lemma, under the original weak
   input and published model. Do NOT extend it to large-prime recovery.

This only supplies membership, not labels constant on distinct cosets.
Returning one failure symbol outside a stabilizer cannot replace the
quantum Fourier source. Likewise, a large-prime classical search cost in
this baseline is not a native hardness proof. Prior-art comparison remains
required; smooth-degree IsERP may already have equivalent classical routes.

An optional consequence to examine AFTER the reduction is established:
recover the dyadic kernel classically, construct its known-ideal isogeny
eta, and run the existing odd-degree quantum source on phi/eta. On odd
auxiliary torsion, a preimage is [deg(eta)^-1] eta^dagger(Q). Full source-order
transport and original-kernel output must be charged; this is not yet an
implemented reduction and must not be granted as free advice.
