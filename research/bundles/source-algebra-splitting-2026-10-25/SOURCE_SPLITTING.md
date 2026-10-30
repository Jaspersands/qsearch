# Construct The Source Split Without Large-Prime Torsion

2026-10-25. Repair for Finding 2 of the independent combined-source review.
This is standard finite-algebra/idempotent machinery applied to an omitted
input conversion, not a new quantum algorithm or a novelty claim. The
reviewer suggested the construction; the detailed argument and implementation
below are subsequent work, not independently reviewed a second time.

## Input And Output

Input: the supplied full source maximal order O0 as a four-dimensional
integral multiplication table, unit, involution, and reduced trace; its
ramified characteristic p; a factored m>=2 with gcd(m,p)=1. Prime factors
are promised prime. The implementation checks the factorization with the
existing helper, not a new proof-producing primality certificate. Any use
of quantum factoring is charged separately; classical comparators receive
the same factorization. For m=1 no split or kernel search is needed.

Output: an explicit algebra isomorphism

    rho_m : O0/mO0 -> M2(Z/mZ),

preserving the canonical involution, and its resource record. No geometric
m-torsion basis, target order, unknown connecting isogeny, or matching
geometric coordinates are required. Source maximality and a valid native
dictionary are still input promises, not authenticated by finite checks.

## Initial Odd-Prime Split

At an unramified odd prime ell, O0/ellO0 is M2(F_ell). Sample the four source
coefficients uniformly and compute the reduced characteristic polynomial
X^2-tX+n. Accept when t^2-4n is a nonzero square. The exact success fraction
is

    [ell*(ell-1)/2] * [ell*(ell+1)] / ell^4
       = (ell^2-1)/(2*ell^2) >= 4/9.

The first factor counts unordered distinct eigenvalue pairs and the second
the conjugacy class size. Thus expected sample count is at most 9/4. This
uses uniform coefficients in the abstract algebra, not knowledge of its
matrix realization. Trace, norm and the quadratic equation are computable
from the supplied multiplication table.

Find a square root of the discriminant by Tonelli-Shanks, with uniformly
sampled nonzero quadratic nonresidues where required. The latter has success
probability 1/2 per draw. Let lambda1,lambda2 be the distinct roots. Then

    e=(a-lambda2)/(lambda1-lambda2)

is an idempotent of rank one. The left ideal (O0/ellO0)e has dimension two.
Select two independent columns among b_i*e and a nonsingular two-row minor.
Express left multiplication by every b_i in this module basis. This is
rho_ell: the action of the simple algebra on its minimal nonzero left module
is faithful, and both domain and codomain have dimension four.

All linear algebra has constant dimensions. There is no ell^4 element
enumeration, ell^2 coordinate table, or ell-torsion construction. At ell=2
reuse the existing constant-size search through the 16 residue elements.

## Preserve Coordinates Through Prime-Power Lifting

Assume rho is already specified modulo n=ell^k. Pull back E11 and E21 via
the invertible four-by-four coordinate map. For arbitrary integral lifts
e0 and f0, put

    e=3*e0^2-2*e0^3 modulo ell*n,
    M=[e, f0*e].

The error e^2-e is a multiple of (e0^2-e0)^2, hence vanishes modulo ell*n
because n^2 is divisible by ell*n for k>=1. This works in characteristic
two as well; no division by two is involved. The columns of M reduce to
E11,E21 under the OLD rho, so they are a basis of the rank-two direct
summand Oe. A minor invertible modulo ell is invertible modulo ell*n.

Left multiplication on M defines the lifted isomorphism. In the old matrix
coordinates the columns E11,E21 are the standard column basis, so its
reduction modulo n is EXACTLY rho, not merely an unspecified conjugate.
The implementation verifies this congruence as well as the full algebra
and involution tables after each lift.

Repeat to ell^e and combine all prime-power matrices entrywise by CRT.
Verification checks the invertible coordinate map, unit, all 16 basis
products, and adjoint identities. The existing extend_split_to_double
routine now receives a CONSTRUCTED rho_m, which it preserves at level 2m.

## Why Arbitrary Initial Coordinates Are Legal

An initial choice only chooses coordinates for the unknown local kernel.
Use the same rho_m in group queries, local recovery and ideal reconstruction.
Changing it by conjugation changes the coordinate vectors and queries, not
the underlying annihilator subset of O0. The output ideal consists of the
source elements whose computed actions kill the recovered module, so it
is invariant under that joint coordinate change.

An exact degree-five control computes a kernel in both an old fixture split
and the newly sampled split, then obtains the identical right-order lattice.
This is coordinate-consistency evidence, not unknown-kernel recovery.

## Cost And Failure Contract

Given factorization, the expected bit cost is polynomial in log(m), source
coefficient lengths and the number of factors. Modular exponentiation and
Tonelli-Shanks use polynomially many bit operations; each nonresidue trial
has probability 1/2. There are sum(e_i-1)<=log2(m) precision steps, each
performing constant-size modular algebra with O(log(m))-bit entries, plus
polynomial-bit CRT. Intermediate bit lengths also depend polynomially on
the supplied source coefficients; their input lengths remain charged.
Nothing here is a factoring algorithm.

With cap T and s odd prime factors, the union bound for sampling failures is

    s * [(5/9)^T + 2^(-T)].

This probabilistic statement assumes independent uniform sampling; seeded
controls are reproducibility fixtures, not proof of this distribution.
Failure raises SearchBudgetExceeded with UNKNOWN status. It does not assert
that a split is absent or that the native input is hard. Successful outputs
are exactly checked. A malicious/invalid source order may fail the contract
checks and is not covered by the probability guarantee.

The code uses SymPy exact arithmetic; the analytic argument is not inferred
from timings. Controls include primes 65537, 1000000007 and 1000000009,
odd and dyadic prime powers, mixed CRT levels, a changed integral basis,
the existing 2m extension, and cap exhaustion. No curve points were used.

## What This Does Not Repair

The independent review's P1 native-input preprocessing obligation is OPEN.
One must still construct an evaluable reference maximal order/curve and a
compatible rational quaternion dictionary from a bare evaluable suborder,
with every assumption charged. The retained Chen--Petit manuscript,
Remark 17 and Lemmas 8/10, distinguishes quantum factorization from the
GRH-dependent reference construction in general characteristic. Removing
one norm-solving heuristic does not remove those dependencies.

The second P2 obligation is also OPEN: explicitly convert the original
curve/points into the represented geometric model and bound the complete
canonical-label algorithm uniformly before coherent reversible compilation.
The main composition remains conditional; finite splits do not execute it.
