# Full Low-Occupation Selector Bound with a Rank Charge

Status: derived, review pending. No independent proof review, formal
certificate, established novelty, classical sampler or algorithmic speedup.

This extends the entry-compression argument in
[the vacuum-coherence note](VACUUM_COHERENCE_BOUND.md) to the ENTIRE output
for a mask supported on sufficiently small subsets. Unlike the vacuum
bound, the quantity here is total class-decision trace distance. Its price
is the selector support dimension; that price cannot be dropped.

Follow-up: [occupation-band localization](OCCUPATION_BAND_LOCALIZATION.md)
now separately bounds the actual cross block for sufficiently separated
low/high sectors. The warning below against combining their diagonal bounds
alone remains valid. Intermediate-band mass and middle/outside coherence
remain unresolved.

## Statement

Use exactly the fixed one-common-group-algebra-query architecture of the
vacuum note: even S_n degree n>=8, standard mixed coset inputs, ONE shared
uniform fixed-point-free involution h, fixed irrep-coarsened classical
source labels, a fixed source-independent normalized pure mask alpha,
physical-input discard and unrestricted final source/selector measurement.
No hidden-correlated side information or prior transcript is available.

Let K be the total number of copies, M=(n-1)!!, and suppose alpha has at
most N nonzero coordinates and no coordinate of Hamming weight greater
than t. Put u=min(K,2t). For K<M the derived bound is

    T(Omega_0, E_h Omega_h)
       <= min(1, raw_copy_bound, sqrt(N*(K+2^u-1)/(M-K))/2).      (1)

Without a more precise support count one may take

    N = sum_(i=0)^t binomial(K,i).                              (2)

The mask need not be radial or uniform, and all intra-support coherences
are included. The claim is conditional on the stated support/weight
bounds: a CLI boolean is not a verifier of an arbitrary state preparation.
All source masses and source-only information are retained.

## Proof

Write the naturally weighted source-J output coefficient as

    C_(eta,J)(S,T)=Tr(U_T^dagger U_S sigma_(eta,J)),
    A_J=E_h C_(h,J)-C_(0,J),
    V(S,T)=sum_J |A_J(S,T)|^2/q0_J.

The common hidden h is averaged after the K-copy products. The source
law qh_j is a class function, and hence is independent of which h in C
was drawn. Its chi-square v satisfies v<=1/M by source-weighted character
column orthogonality, as proved in the vacuum note.

Fix S,T and let I=S union T, of size m. The UNITARY U_T^dagger U_S acts
only on these m inputs and commutes with each source projector. All other
inputs contribute only their classical source outcomes. Thus this SINGLE
matrix element is obtainable from the compressed hypotheses

    tau_0=rho_0^tensor m tensor q0^tensor(K-m),
    tau_1=(E_h rho_h^tensor m) tensor qh^tensor(K-m).

The Hilbert-Schmidt Cauchy argument with each active source projector
P_A and each inactive source tuple from the vacuum note applies unchanged,
replacing U_S by U_T^dagger U_S. It gives

    V(S,T) <= chi_square(tau_1,tau_0)
            = [1+(2^m-1)/M]*(1+v)^(K-m)-1.                     (3)

This equation is an entrywise bound, NOT a simulation of the full
selector channel by m or 2t raw coset copies. Different entries can involve
different subsets of the entire K-copy collection.

For every entry supported by alpha, m<=u. Since K<M, the geometric
envelope (1+v)^K<=M/(M-K)=Ebar gives

    V(S,T) <= Ebar-1+Ebar*(2^u-1)/M
            = (K+2^u-1)/(M-K) = B.                            (4)

Now Delta_J=diag(alpha) A_J diag(alpha)^dagger is the ACTUAL output
difference in source sector J. With p_S=|alpha_S|^2,

    sum_J ||Delta_J||_2^2/q0_J
       = sum_(S,T) p_S p_T V(S,T) <= B.                       (5)

Every Delta_J is supported on an N-dimensional selector space, so
||Delta_J||_1<=sqrt(N)||Delta_J||_2. Cauchy over the natural source
probabilities, whose sum is one, then gives

    T = (1/2)sum_J ||Delta_J||_1
      <= (sqrt(N)/2)*sqrt(sum_J ||Delta_J||_2^2/q0_J)
      <= sqrt(N B)/2.                                         (6)

The independent raw-copy bound is (1/2)sqrt((2^K-1)/M), capped at one;
it bounds the class-averaged decision problem and may be combined by taking
the minimum. It must not be applied to E_h T(Omega_0,Omega_h). Equations
(4)-(6) prove (1). No success renormalization or source postselection occurs.

## Growing-Degree Consequence

At K=n^2 and t=c*n for any fixed c<1/2, the standard binomial-sum bound
gives log N<=t log(eK/t)=c*n*log n+O(n), while
log M=(n/2)*log n+O(n). Also log(K+2^(2t)-1)=O(n). Hence

    log T <= -(1/4-c/2)*n*log n + O(n),                       (7)

which is superpolynomially small. The implementation uses exact integer
support counts and outward dyadic rounding, not this asymptotic estimate.
For the convenient t=n/4:

| n | K | t | Total distance upper bound |
|---|---|---|---|
| 128 | 16384 | 32 | 1 (vacuous at this finite degree) |
| 1024 | 1048576 | 256 | 2^-217 |
| 4096 | 16777216 | 1024 | 2^-1884 |

These are evaluations of a conditional inequality, not simulations at those
degrees. The support count uses an O(t) binomial recurrence without
materializing selector strings. A bound already vacuous because of the
active-union size or K>=M exits before constructing huge powers or counts.
A separately justified sparse support N may improve (1); it is not inferred
from a compact classical description of alpha.

More generally, for K=n^a with fixed a>1 and t=c*n, the sufficient
condition is c*(a-1)<1/2. This is a scope/parameter tradeoff, not a uniform
low-weight obstruction independent of the available copy budget.

## Failed Shortcuts and Scope Tests

1. **Dropping the rank factor is false.** There are valid four-dimensional
   source-free Schur channels with unit diagonals and positive coefficient
   matrices for which the uniform mask gives T=1/2 while half the output
   Frobenius norm is only 1/4. The sqrt(N) charge is saturated in this
   control. It is a channel-algebra counterexample, not an oracle candidate.
2. **Radial parameters are not output rank.** In the actual dense noncentral
   S3 K=3 model, the uniform mask has four weight parameters, but the
   naturally weighted output for the all-standard-irrep source tuple has
   rank eight. One cannot replace N by K+1 using the symmetry reduction.
3. **Separate sectors cannot be pasted together for free.** A pair of
   diagonal-unitary channels has zero decision distance on each of two
   nonempty weight sectors and distance one on their coherent superposition.
   Thus the present low-weight theorem and the previous high-occupation
   theorem do not jointly imply an all-mask no-go. Their cross block needs
   an additional bound. The vacuum theorem addresses only one special case.
4. **Finite controls are not an asymptotic proof.** All 96 selector matrix
   entries in the actual S3 K=2,3 and fixed-point-free S4 K=2 channels
   satisfy (3), retaining every ordered source tuple and all shared hidden
   members. Twenty full-mask
   probes check (5)-(6). They support the algebra and conventions; the
   general proof, source-class assumption and support-rank charge still
   require independent scrutiny.

The immediate research consequence is narrower than "low weights cannot
work": do not search the certified low-support regimes as though they
remain unexplored escapes. At quadratic copy budgets the unresolved region
includes larger low-weight supports and nonempty low/high cross-sector
coherence, besides genuinely changed physical-retention/query architectures.

## Prior Art and Next Decision

The mathematical ingredients are standard: regular-representation trace
orthogonality, chi-square, Cauchy-Schwarz and Schatten norm comparison.
The scoped combination here has not been established as novel. It should
be reviewed alongside the preceding bounds as one argument about this
particular architecture, not advertised as several independent breakthroughs.

The positive missing-harmonic span construction of
[Moore and Russell](https://arxiv.org/html/quant-ph/0504067) remains outside
this discarded-input implementation. Neither (1) nor its support count
supplies an efficient measurement of that span or disproves its information.

Next try to bound or falsify the NONEMPTY low/high cross block, using the
actual environmental overlaps rather than convexly mixing sector distances.
If controlling it needs a prohibitively loose dimension charge, compare
that effort with moving to a concrete retained-physical span-measurement
primitive. A new queue of cosmetic mask mutations is not useful.

Implementation: `source_selector_low_occupation_contract` in
`core/isotypic_instruments.py`, physical controls in
`theorems/coset_mask_symmetry.py`, and `tests/test_coset_low_occupation.py`.
The existing `python qsearch.py coset-binary-carrier-instruments` workflow
records `LOW-OCCUPATION-SUPPORT-DIMENSION-OBSTRUCTION`. Its gates deny
an all-mask conclusion and retain the cross-sector proof obligation.
