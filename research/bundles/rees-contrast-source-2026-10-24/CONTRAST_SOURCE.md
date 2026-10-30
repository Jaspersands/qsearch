# Symmetry Sources From Scalar-Plus-Low-Rank Contrast

2026-10-24. LOCAL CONDITIONAL EXTENSION, NOT INDEPENDENTLY REVIEWED.
No new DME, antisymmetrization or HSP primitive is claimed. No executed
quantum algorithm, novelty certification or classical-input speedup follows.

## 1. Same Task, A Weaker Spectral Promise

Keep the explicit fixed-class exponent-p Lazard group, c<p, controlled
LINEAR representation U, fresh IID copies of rho, and global promise

    H = {g : U(g) rho U(g)* = rho},
    TD(rho,U(g)rho U(g)*) >= delta for EVERY g outside H.

Output this SAME H, not a principal-eigenstate or support stabilizer.
Copy/action acquisition, 1/delta, all receiver and moment-design costs remain
charged. The Hilbert-space dimension D is public in binary.

Replace rank(rho)<=R by the following EXISTENCE promise, for supplied R>=1:

    rho0 = b I + X >= 0, b>=0, X=X*, rank(X)<=R,
    ||rho-rho0||_1 <= eta = delta/256.

rho0 need not have trace one. Neither b, X, rho0, an eigenbasis nor a
decomposition is supplied. X need not be positive and need not commute with
rho. In particular, rho=(1-w)sigma+w I/D with rank(sigma)<=R is admitted,
with UNKNOWN w and arbitrarily large full rank. The original state, not
purified copies or a noiseless component, is used throughout.

The extension costs polynomially in R, 1/delta, log D, inverse error and
the existing fixed-class receiver/design costs. It remains conditional on
the preceding source and receiver proofs and their imported algorithms.

## 2. A Public Two-Branch Compiler

Put h0=delta/(64R). If

    D <= R + 2(1+eta)/h0,

use the preceding full-rank source with rank cap D. Here D=O(R/delta),
so this is a polynomial branch, not a field/dimension-sized fallback on
large inputs. Set b=0 FOR ITS PROOF; no background estimate is used.

Otherwise use the existing source planner with effective cap K=2R and
bin width h=delta/(32K)=h0. This cap is NOT a cap on rank(rho).
The old random grid has cutoff c in [h,2h), bin width h, margin
a=epsilon*h/(128K), and at least 128K/epsilon grid points. Here epsilon<=1.

Because rho0>=0, tr(rho0)<=1+eta and at least D-R of its eigenvalues
equal b, the large-D branch guarantees

    b <= (1+eta)/(D-R) < h/2.

The trace-norm best-rank-approximation inequality applied to rho-bI gives

    sum of all but R largest numbers |lambda_i(rho)-b| <= eta.       (1)

This is the usual singular-value tail bound for approximation by rank R;
it DOES NOT assume [rho,X]=0. Call the R exceptional eigenvalues E for the
proof only. All other centered absolute deviations have total at most eta.

## 3. Why The Cutoff Preserves The Exact Group

Let P_j be rho's nonempty bins above c and a_j their left endpoints.
The algorithm learns/uses these bins, never the exceptional set E. Define
only in the proof

    A = sum_j a_j P_j,
    C = sum_j (a_j-b) P_j,      B=bI+C.

All a_j-b are distinct and positive. Therefore A, C and B have the SAME
conjugation stabilizer (including the discarded subspace). Also C>=0 and
tr(C)<=1. Every symmetry of rho preserves every P_j.

For an exceptional discarded eigenvalue, |lambda-b|<2h; for an exceptional
retained one, lambda-a_j<h. For a nonexceptional retained eigenvalue,
0<=lambda-a_j<=lambda-b, because a_j>=h>b. Equation (1) thus gives

    ||rho-B||_1 <= 2Rh+eta = 9 delta/256 < delta/16.                 (2)

If g fixes B, TD(rho,U(g)rho U(g)*) <= ||rho-B||_1 < delta, so the
global promise forces g in H. Hence Stab(A)=Stab(B)=H EXACTLY.

For g outside H, TD(C,U(g)C U(g)*) >= delta-9delta/256.
Writing eta_j=||P_j-U(g)P_j U(g)*||_op and r_j=rank(P_j),

    TD(C,U(g)C U(g)*) <= sum_j (a_j-b) r_j eta_j <= max_j eta_j.

Some eta_j is at least delta/2. The separate top-wedge packet therefore
has off-H overlap at most sqrt(1-delta^2/4)<=1-delta^2/8, exactly the
conservative ray gap used by the preceding source. Its on-H determinant
character is erased by the EXISTING zero-moment Rees design. Do not replace
that design by tensoring arbitrary powers or assuming conjugate copies.

## 4. The Exponential Rank Does Not Reenter The Error Budget

Retained nonexceptional eigenvalues each have lambda-b>=h/2, so

    retained rank <= R+2eta/h = 3R/2 <= K.

For the grid union bound only eigenvalues lambda>=h-a can approach ANY
boundary (the first boundary is at least h). Since a<h/4 and b<h/2,
each nonexceptional such eigenvalue costs more than h/4 in (1). Thus

    number of potentially boundary-adjacent eigenvalues
      <= R+4eta/h = 2R = K.

Counting only distinct eigenvalues would also suffice; the multiplicity
bound is conservative. There is NO union bound over D. The previous
finite-grid failure bound, DME/QPE budget, occupied-bin fetch probability
at least h, nonflat antisymmetric-growth lower bound h/(K+1), rank stopping,
source amplification, and whole-run copy/action caps apply unchanged.
QPE classification is compared on fresh rho eigenstate mixtures, NOT as
a coarse-projector channel on arbitrary coherent superpositions.

One algorithmic change is ESSENTIAL: if preprocessing records no occupied
bins, return generators of the WHOLE public group, rather than aborting.
On the ideal successful history, A=0 and (2) then force H=G. A genuinely
occupied bin has mass at least h; the existing capped-fetch union bound
already pays for falsely missing it. Inconsistent or over-cap metadata
still means ABORT. Maximally mixed input is a valid empty-filter case.

## 5. Matched Classical Baseline For Diagonal Inputs

This theorem is NOT evidence of an advantage on diagonal distributions.
Suppose the state is diagonal in a KNOWN basis, and U acts by public
permutations there. Measuring copies gives the same native IID samples.
Use the same random grid. For N draws, Hoeffding plus a union bound over
the D labels gives, with failure at most zeta,

    max_x |P_hat(x)-P(x)| < a/2,
    N >= 2 log(2D/zeta)/a^2.

The cost depends on log D, not D. Store observed labels only. An unobserved
label cannot have mass >=h on this event. On a good grid, classify all
observed frequencies above c; this recovers EXACTLY the retained colored
point set, not just an approximate distribution. Its stabilizer is H by
Section 3. Uniform-background samples are charged, not silently removed.

For the previously specified faithful affine p-group action over F_p,
the existing colored affine lift and published p-group set-stabilizer
backend finish in polynomial time. The Luks backend is still CITED, not
implemented. Arbitrary succinct permutation actions do not automatically
inherit that backend. Unknown non-diagonal states do not supply this known
basis or classical probability access. No matching general classical
algorithm or lower bound is asserted for them.

## 6. Attempts To Falsify The Extension

1. HIGH-RANK DIAGONAL BIAS: eigenvalues (1+alpha)/D and (1-alpha)/D,
   each D/2 times, have translation gap alpha. A cutoff above both loses
   the symmetry. For R<=D/2 their best centered rank-R trace residual is
   alpha(1-2R/D), not <=delta/256 at delta=alpha and R<<D. A global gap
   alone is insufficient. The planner does not certify compressibility.
2. BROKEN SYMMETRY BY TINY NOISE: perturb one member of a formerly symmetric
   orbit by tau. That element is now outside H but moves rho by O(tau).
   A previously valid constant delta is no longer promised. The theorem
   does NOT recover a noiseless state's H under arbitrary perturbations.
3. EMPTY FILTER: identity backgrounds must return H=G, not an empty hidden
   subgroup and not an automatic failure. Finite fetch failure stays paid.
4. WRONG RANK COUNT: inserting full rank D in the boundary union bound
   destroys the claimed leverage. Conversely using K without the margin
   argument is unjustified. Both retained and near-boundary counts are tested.
5. HIDDEN ACCESS: the proof's b, X, spectra, projectors and frames are not
   input oracles. Reference code using them is diagnostic only. Raw copies,
   program copies and every failed fetch/growth attempt are still charged.

The regression controls include a nonnormal UT3(F3) subgroup with a full
scalar background and an H-invariant, NONCOMMUTING low-weight perturbation.
These are easy mathematical controls, never proposed hard problem families.
An enormous symbolic dimension tests the ledger without allocating its
state. It is not a large quantum execution.

## 7. Status, Prior Art, And Next Decision

This removes exact low state rank from a scoped source conversion. It does
not remove low-rank CONTRAST, the global orbit gap, independent copies,
controlled linear action, fixed class, or the missing natural hard input.
Do not spend another pass on a neighboring noise model. The next scientific
priority is an explicit useful input family meeting these promises whose
best known classical algorithm has a genuine unresolved bottleneck.

Imported tools, not discoveries here:
- [Go et al., non-asymptotic DME](https://arxiv.org/html/2412.02134): use
  rigorous complete-channel accounting; an earlier asymptotic proof was
  identified as incomplete. The local predecessor separately bounds its
  controlled partial-swap primitive.
- [Bene Watts et al., anti-symmetrization](https://arxiv.org/html/2610.06737v1):
  the growth instrument is published; our preceding note treats nonflat
  filtered bins and capped rank discovery.
- The preceding Rees source, zero-moment design, receiver, and diagonal
  Luks baseline are dependencies, not re-established by these tests.

Independent review, novelty assessment and a useful application remain
open. This bundle grants no new candidate admission or speedup status.
