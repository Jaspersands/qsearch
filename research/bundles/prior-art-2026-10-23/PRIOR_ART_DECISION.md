# Rees Prior-Art And Research-Value Decision

2026-10-23. Local audit outside the actively migrating repository. No source
or staging edits, registry admission, quantum execution, or novelty claim.

## Decision

The proposed Rees result is NOT directly subsumed by the theorem hypotheses
checked below. That is a much weaker statement than establishing novelty.
An unexamined reduction to known results can still subsume it, and a search
that returns no matching title proves nothing. The core remains under review.

Retain the fixed-class, large-prime ordinary-oracle theorem as the smallest
review target. Do not expand its parameter variants or synthetic families to
manufacture evidence of significance. No new natural hard source was found.

The conditional bounded-index FPT extension, mixed/noisy state variants,
and source constructions must not make the short core harder to review.
They are downstream claims, not evidence that the core is right or new.

## Checked Primary Sources

1. [Ivanyos--Sanselme--Santha, nil-2 HSP](https://arxiv.org/html/0707.1260):
   polynomial-time HSP for class at most two, with a separate fixed-class
   reduction to exponent-p groups and hidden subgroups of size at most p.
   A reduction is not a solver for its higher-class terminal problem.
   Section 3 explicitly imports efficient collection and p-group normalizers.

2. [Ivanyos--Santha, diagonal equations](https://arxiv.org/html/1503.09016):
   its HSP application in Section 4.1 uses elementary-abelian-by-C_p groups.
   Its scalar diagonal solver and fixed-degree SDE algorithm are dependencies
   of Rees, not discoveries of this repository. The HPGP application does not
   by itself supply a reduction from arbitrary nilpotent HSP.

3. [Imran--Ivanyos, zero-sum subsequences](https://arxiv.org/abs/2304.08376),
   [published theorem](https://link.springer.com/article/10.1007/s11128-023-04228-2):
   the unconditional polynomial-time result bounds both nilpotency class and
   prime divisors. Central subgroup-state conversion is already prior art.
   Rees changes the public cover and available weights; it does not invent
   central descent or abelian Fourier recovery.

4. [Morales, semidirect and quasi-Hamiltonian HSP](https://arxiv.org/html/2608.05321v1):
   the two stated families are scalar abelian-by-cyclic semidirect products
   with additional bounds, and quasi-Hamiltonian groups with structured
   input. Quasi-Hamiltonian does not mean arbitrary nilpotent. The large
   nilpotency classes in this paper do not imply arbitrary fixed-class HSP.
   Abstract/introduction and relevant scope statements were checked; this
   audit is not a verification of its full algorithm.

5. [Te'eni--Oz--Cohen, index-q HSP, v2](https://arxiv.org/abs/2510.10538v2):
   exact one-query identification requires a cyclic quotient and compatible
   output alphabet. It is not an arbitrary-label, nonnormal p-group HSP
   solver. Only the primary abstract was used for this scope comparison.

6. [Miasnikov--Ushakov, metabelian conjugacy](https://arxiv.org/html/2610.27250v1):
   a different, naturally presented problem, using commutative algebra and
   known quantum arithmetic. Its input conventions fix generator/variable
   counts and charge numerical polynomial degrees. Theorem 1.2 cannot be
   applied to arbitrary succinct binary-degree circuits. Introduction and
   theorem statements were read, not the entire proof. No extension of it
   is proposed or credited to this repository.

These are selected comparisons, not an exhaustive literature certificate.
In particular, possible compositions of earlier reductions still need review.

## An Exact Scope Witness, Not A New Oracle Problem

Let G_m(p) be the group of 5 by 5 upper unitriangular BLOCK matrices with
m by m blocks over F_p and identity diagonal blocks; p>4. The corresponding
strict block-upper-triangular Lie algebra has lower central dimensions

    10m^2, 6m^2, 3m^2, m^2, 0.

Products of matrix units spanning block distance r and s span block distance
at least r+s. Every allowed longer-distance unit factors through an
intermediate block. This proves the displayed series for all m>=1, not just
the finite tested sizes. The group has order p^(10m^2), exponent p, and
class four: N^5=0 and (I+N)^p=I for p>=5, while a length-four commutator is
nonzero. The matrix-log/BCH correspondence is legal because 4<p.

Within one chosen coordinate of each block, write E_ij with ONE-based
block indices. For group commutators [a,b]=a^-1 b^-1 a b,

    [I+E_12,I+E_23] = I+E_13,
    [I+E_34,I+E_45] = I+E_35,
    [I+E_13,I+E_35] = I+E_15 != I.

Thus G' is nonabelian, and G is not metabelian. Every abelian-by-cyclic
group is metabelian, so this excludes DIRECT membership in those ambient
families, independently of the chosen coordinates or presentation.

Also A=<I+E_12> and B=<I+E_23> do not permute. The product
(I+E_12)(I+E_23) has E_13 entry 1; every element of BA has that entry zero.
Hence G is not quasi-Hamiltonian.

To avoid silently changing the hidden-subgroup promise, the subalgebra

    h = <E_13, E_35+E_25, E_15>

is nonabelian and nonnormal: [E_13,E_35+E_25]=E_15, whereas
[E_23,E_35+E_25]=E_25 is outside h. It is also not homogeneous in the
standard block-distance grading: the degree-two component E_35 of its
second generator is outside h. Thus assuming a normal hidden subgroup or
assuming its invariance under the existing matrix dilation changes this
instance. The proposed Rees cover specifically addresses that last issue.

This h is explicitly supplied here solely to verify a logical scope
distinction. We do NOT construct a hiding function or pretend recovering
these public generators is a hard task. The code performs matrix identities
over integers, not quantum search. The inequalities have coefficient 1 and
survive every prime reduction; tests include a 127-bit prime.

For fixed p the bounded-prime prior theorem may apply. The separated regime
lets p grow, for example primes between 2^m and 2^(m+1). A whole group entry
encoding then has polynomial length in m, while enumeration in p is not
polynomial in that length. This observation is NOT a classical lower bound.

Even this witness does not rule out a known polynomial-time reduction of its
HSP to another family. No classifier should turn these exclusions into a
novelty, hardness, or speedup flag.

## Scrutiny Of The Outer Normalizer Assumption

The normalizer assumption was rechecked against Section 3 of the nil-2
paper. It separates two assertions: efficient collection is available for
fixed class; p-group normalizers are polynomial given that collection,
using Eick and Luks. The newer local extension explicitly replaces the
growing-class collection cost with paid quantum unique normal-word maps.

No new contradiction was found in that interface. This is NOT an independent
proof of the Eick/Luks/IMS composition: the full normalizer implementation
and map interfaces were not reconstructed in this pass. Keep that review
obligation open. Generic permutation algorithms polynomial in permutation
degree, or Eick's practical general polycyclic algorithm by itself, cannot
replace the particular p-group bit-complexity claim.

## Two Rediscoveries Rejected Before Implementation

The repository already contains both of the following. Neither should be
counted as progress of this pass or reimplemented under a new name.

- CLASS_THREE_APPLICATION_AUDIT.md: explicit nilpotent finite-field linear
  actions split into a bounded-prime Luks part and a central abelian part
  handled by known abelian HSP. Increasing the prime alone does not make
  explicit vector/subspace/finite-set stabilization a new application.
- REES_PROJECTIVE_STATE_SOURCE.md: scalar Fermat rows, Cartesian-product
  zero-moment designs, and coverage yield forward-copy phase neutralization.
  The construction already removes unknown ray characters without inverse
  preparation or conjugate copies. It does not establish a useful state
  family's global separation gap.

The succinct-polynomial derivative, Frobenius, orbit-module and Moore
filters also remain active. The two isogeny lattice attacks still rule out
their strengthened advice models, not the original weak geometric source.

## Next Research Gate

1. Seek independent whole-proof scrutiny of the short explicit-Lie Rees
   statement. Inspect the cover fiber identity, complete central instrument,
   fresh-source composition, final full-h recovery and uniform cost. Do not
   present the number of passing tests as a proof or invent an external review.
2. Audit reductions, not only group-class names, against the literature above.
   A complete reduction of arbitrary fixed-class large-prime HSP to a known
   solver would remove the proposed theorem's novelty even though this
   structural witness remains correct.
3. Only reopen an application route with an actual public input and an
   end-to-end source construction, or a proved global state gap. No hidden
   advice, arbitrary opaque oracle, or uncharged coefficient expansion.
4. If no such application or substantive proof obligation is available, move
   research effort to an independent mechanism. Do not create another nearby
   field/ring/source-parameter variant merely to fill an autonomous pass.

## Verification And Integration

scope_witness.py checks integer group products, commutators, Lie closure,
and lower/derived series. test_scope_witness.py includes easy opposite-order
controls and guards against promoting the receipt to an algorithm claim.
replay.py writes source hashes and scope_receipt.json. These are finite
structural checks; the all-m proof is the matrix-unit argument above.

After migration is verified, Gemini may integrate this note under research/
and keep the finite controls with research proof diagnostics. Reconcile with
intervening edits. No CLI/UI expansion or central candidate record is needed.
The bundle is not a Git checkout; no commit or push was performed.

Full-repository tests, qsearch.py validate and UI syntax validation were NOT
run during copying. Local test and replay results belong in the handoff and
must not be described as whole-repository validation.
