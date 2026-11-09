# Two arbitrary Gaussians: bounded actual-source audit

7 November2026. Read STATE/TRAPS, the current
`TWO_GAUSSIAN_PAIR_LEARNING.md`, and the five retained primary texts in
`audits/sources/two_gaussian_learning/` with matching PDFs/source.json.
No network/Git/API, implementation, broad archive, or novelty claim.
Locators below are exact local `.txt` line numbers.

**Verdict:** the EVEN two-branch paired normal form is source-supported,
including zero overlap, with the parity explanation below. The supplied-
description Pfaffian and variational baselines are substantial established
results. None of these checked statements supplies the new uniform copy
learner or its bounded-memory tomography/error composition. Those remain
parent derivations, not consequences of a source label or low-moment fit.

## Bloch--Messiah: exact even-pair scope

`pairing.txt` (0810.4772) at270--307 gives passive Bloch--Messiah reduction,
covariance blocks Eq13--14, and wavefunction Eq15:
`product_j(u_j+v_j a_j^dagger a_-j^dagger)|vac>` with
`|u_j|^2+|v_j|^2=1`. There is NO premise u_j!=0. Fully occupied pairs
u_j=0 are allowed, so vacuum overlap `product_j u_j` may vanish. The
normal form must not instead be justified by a Thouless matrix requiring
an invertible vacuum-overlap block.

For the native pair, apply an ANALYSIS-ONLY inverse preparing the first
even Gaussian, then canonicalize the relative even Gaussian by a passive
mode change. Fractional occupations pair in the Gaussian canonical form;
fully occupied blocked modes have even count and can also be paired.
Any remaining unpaired mode is empty. Passive mode rephasings, plus a
global branch phase absorbed in beta, make c_j,s_j nonnegative even at
zero coefficients. This proves the displayed common hidden frame with
normalization N>0, without supplying an unknown inverse to the learner.

The parity restriction is essential. The source's broad sentence at305--307
must not be read as making an ODD Gaussian a vacuum-product of occupied
pairs by passive rotation. Odd states require blocked occupied modes.
At130--138 the source distinguishes O(2M) canonical transformations from
determinant1 quadratic evolution. Bravyi--Gosset explicitly distinguishes
even/odd states and parity-flipping reflections (see below). Two even
branches permit the even-frame argument; arbitrary opposite parities do
not follow from Eq15. Normalization and near-cancellation remain exact
Gram-matrix issues; no source supplies a uniform learning stability bound.

## External motivation, not a rank-two ground-state theorem

`impurity.txt` (2105.01088), SectionII.C at165--196, defines the R-Gaussian
ansatz and its exact Gram normalization Eq4--5, with O(RN^2) parameters.
Lines197--210 solve the coefficient optimization for GIVEN Gaussian
branches by a generalized eigenproblem. Lines194--204 of the opposite
column discuss energy descent to a LOCAL minimum, not a global finite-time
copy-learning guarantee. Its reported polynomial numerical work per
variational update is not a theorem preparing an unknown rank-two state.

`bravyi_gosset.txt` (1609.00735) defines Gaussian rank at595--598.
Lines358--375 motivate variational fixed-rank superpositions and report a
rank2 numerical benchmark, not a universal rank2 guarantee. Its rigorous
impurity approximation uses a number of Gaussian branches depending on
accuracy/impurity size; the abstract at16--18 already states
`exp[O(b^3)]` branches for additive precision2^-b. Neither this source nor
the impurity ansatz makes general impurity ground states rank2. Learning
copies of a promised state also does not produce those copies from a
Hamiltonian or solve ground preparation.

## Supplied-description classical Pfaffian baseline

Bravyi--Gosset Section2.2 at502--535 gives polynomial Pfaffian evaluation;
Section2.3 at548--598 defines Gaussian states, O(2n), quadratic rotations,
reflection generators and fixed parity. Eq23 at638--642 computes overlap
magnitude. A covariance alone specifies a branch only up to global phase:
lines643--648 add a reference overlap to fix its phase. Coherent sums
require the relative phase as well as the two covariance matrices.

Eq24/27 at649--687 gives reference-based Pfaffian formulas for overlaps
and transition Majorana matrix elements. The simpler Eq25/28 at658--705
uses `(M1+M2)^-1` and is restricted to NONORTHOGONAL branch pairs. Do not
use that inverse at zero overlap; Eq24/27 instead needs a common reference
having nonzero overlap with each branch. Supplied Gaussian circuits also
carry phase information. Thus known Gaussian branches/coefficients permit
classical probability/observable and sequential Gaussian-measurement
simulation, with polynomial matrix dimensions. Pay precision, reference
conditioning and the normalized sum's cancellation; these arithmetic
formulas are not an n-only BIT theorem for arbitrarily succinct angles.
This is a supplied-description comparator, not unknown-copy inference.
No classical-input computational or sampling advantage follows here.

## Learning and sequential-tomography boundary

The previous Mele--Herasymenko source pays fixed-small-mode Gaussian
compression tomography, including its stated robustness threshold and
O/Pin versus even-control bookkeeping; see the already retained
`audits/reviews/2026-11-07-two-fock-sources.md`. It does not cover arbitrary
rank2 by constant compression: balanced vacuum/full cats on growing even
n have covariance0 and Gaussian nullity n. The old shared-frame two-Fock
learner also cannot be invoked for two arbitrary nonorthogonal Gaussians
without the new reduction. Even zero overlap alone does not make the two
covariances commute or give a shared Fock frame.

In the paired frame, the two branches are product vectors over logical
pair sites, so the coherent sum has MPS bond dimension at most2. This is
a structural fact once a usable frame is known. It is NOT justification
for learning only fixed-size marginals: the native even states
`(|0^n>+|1^n>)/sqrt2` and `(|0^n>-|1^n>)/sqrt2`, n even, have identical
EVERY proper-subsystem marginal but are orthogonal. Their global phase
must survive in a coherent memory or be measured by additional global data.

A bounded-memory sequential proof must specify the known prefix circuits
applied to FRESH copies, how each local compression preserves the bond
coherence, how data determine the final memory state, and a uniform global
error bound without division by tiny Schmidt weights. Any conditional
sampling/postselection needs a success bound and a capped copy clock.
Approximated prefix unitaries, local tomography, circuit compilation and
confidence must all be charged. None of the five current source texts
asserts this new uniform theorem. This review neither rejects a sequential
construction nor replaces its proof by a low-marginal reconstruction claim.

## Two selection screens only

`quadratic.txt` (MFCS2020) at103--108 records polynomial quadratic-form
equivalence over finite fields, a factoring-oracle algorithm over Q, and
a randomized reduction of factoring to the Q SEARCH problem. This does
not establish unconditional classical polynomial factoring or transfer
search hardness to a different decision contract.
`finite_algebra.txt` (2608.30340v1) at57--90 explicitly retains randomized
polynomial EXPECTED classical splitting and distinguishes exact quantum
splitting from a speedup. Its radical/semisimple-decomposition discussion
at42--52 is not a theorem for arbitrary algebra automorphism groups.
These are scoped baseline screens; neither pays the Gaussian learner.

## Added primary MPS endpoint source

The subsequently retained SIXTH source, Landon-Cardinal--Liu--Poulin,
`mps_tomography.txt` (1002.4632v1), DOES supply the sequential-compression
machinery. Lines60--70 describe local compression to a coherent memory;
108--134 specify prefix-unitary application, window tomography and local
disentangling. Lines86--91 give inverse-circuit reconstruction and
poly(n,chi) resources. For qubit bond8, their k=ceil(log_2 chi)+1 is exactly
a four-qubit window and three-qubit memory. This is established MPS
tomography, not a new endpoint primitive of the present candidate.

Their accuracy discussion at100--151 includes truncation, postselection,
finite precision and cumulative error. Lines163--179 explicitly explain
why fixed marginals miss GHZ phase and why FINAL MEMORY tomography
recovers it. Thus the earlier "five current source texts" statement is
historical, not an assertion that this method was absent from literature.
The current note's explicit gap-free Ky Fan and capped conditional-error
proof supplies its chosen quantitative interface; this addendum checks
the source match, not that entire new error calculation. Neither the MPS
source nor this addendum pays the unknown Gaussian-frame recovery or
establishes a theorem-priority/novelty claim for the whole learner.
