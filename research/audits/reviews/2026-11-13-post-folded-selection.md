# 2026-11-13 Post-folded selection: rank, purity, and component discovery

## Decision and scope

No new end-to-end quantum **advantage** claim is currently admitted from these
three directions. The best focused construction/refutation attempt is a uniform
stabilizer-rank versus Pauli-purity inequality. Unlike the other two candidates,
it has an explicit native learning endpoint, an already retained inverse theorem,
and a cheap exact falsifier that changes the proposed exponent. It is a difficult
magic-complexity question, not evidence of a Shor-level separation.

Recommend one bounded mathematical attack on the inequality below, rather than
another full learner, implementation, source survey, or nearby folded/Kerr slice.
No shared status was changed. STATE/TRAPS/GOAL and the listed actual sources were
consulted; no network, API, Git, numerical control, or archive was used.

## 1. Copies-only discovery from growing stabilizer rank

**Native endpoint.** Input fresh copies of an unknown normalized n-qubit pure
state psi and an integer k with exact stabilizer rank chi(psi)<=k. Output a
classical stabilizer tableau phi with |<phi,psi>|^2>=c k^-C, with failure at most
eta, in poly(n,k,log(1/eta)) gates and copies. No supplied decomposition, Gram
matrix, state preparation/inverse oracle, conjugated copies, or conditioning
promise is permitted. A returned tableau's overlap can be checked by its Clifford
measurement using polynomially many fresh copies at the promised scale.

**Proposed mathematical operation.** Prove or refute the existence of absolute
c>0,C<infinity such that, uniformly in n and every normalized exact-rank-k state,

    P(psi) := 2^-n sum_(a,b in F_2^n) |<psi|X^a Z^b|psi>|^4 >= c k^-C.       (P)

This pays a missing signal bound; it does not assume that finding a stabilizer
decomposition is easy. For f(x)=2^(n/2)psi(x), Fourier expansion of the derivative
f(x)conj(f(x+a)) gives exactly ||f||_U3^8=P(psi). Indeed its b-th normalized Fourier
coefficient is <psi|X^a Z^b|psi> up to conjugation/sign, and the U3 identity averages
the fourth powers over a. The phase convention for Hermitian Paulis is immaterial.

The ordinary inverse theorem for bounded functions is insufficient: ||f||_2=1
does not bound ||f||_infinity independently of n. The actual quantum-state source
does pay this interface. Arunachalam--Dutt, `structure.txt`, physical LF932--970,
defines this quantum Gowers norm; Fact2.10 bounds its Bell-difference proxy Q by

    P(psi)^2 <= Q(psi) <= P(psi),

and Theorem2.11 gives stabilizer fidelity at least Omega(Q^C0). Its copies-only
self-correction theorem (LF180--213) finds a stabilizer of polynomially related
fidelity in polynomial inverse-fidelity time. The approximate-algorithmic-PFR
premise is removed by actual Marton Cor8.6, physical LF3152--3161. Thus (P) would
give the stated complete **component-discovery** endpoint with fixed polynomial
exponents. This composition does not require an amplitude-function oracle.

**Exact initial falsifier, including tensor amplification.** The enticing choice
c=1,C=3 is false. Put

    psi=(|0^6>-|+^6>)/sqrt(7/4).

It has rank at most two. The identity expectation is one. There are 126 Paulis
with exactly one of a,b zero, each of magnitude 3/7. For nonzero a,b with a.b=0
there are 63*31=1953 expectations of magnitude 1/7; all remaining expectations
vanish. Consequently

    P(psi)=[1+126(3/7)^4+1953(1/7)^4]/64=65/686 < 1/8.

Purity is multiplicative on tensor products and chi(psi^tensor r)<=2^r. Therefore
EVERY uniform lower bound c*k^-3, with any fixed c>0, is false. Any bound (P)
must have C>=log_2(686/65)>3.39. This is an exact analytical family, not finite
evidence extrapolated to a theorem. No fixed exponent C is refuted here.

**Strongest applicable prior result.** Actual `extent.txt`, Theorem1.1 LF132--140,
proves squared extent xi<=2^O(sqrt(k log(k+1))). Cor1.6 LF220--227 already gives
copies-only full tomography in that subexponential-k time and sample bound.
Its Pauli-projector elimination is already Lemma3.4 LF655--675, with the D+2b
recurrence; proposing that splitting again would not be a new operation.
The source explicitly asks about polynomial rank--extent in LF1385--1391.
Its full text contains no rank--purity theorem; this is a scoped source check,
not a literature-wide novelty claim. Its learning application already uses
Marton; simply importing PFR again does not improve the rank dependence.

For comparison, a supplied short tableau decomposition with controlled coefficient
norm admits familiar classical contraction/sampling procedures. That supplied
description is absent here. The above copies-only quantum upper bound is the
matched known learning baseline; no classical computational lower bound, sample
separation, or practical advantage follows from the absence of a decomposition.

**Limits and next falsifier.** A polynomial purity bound would imply exponential
exact stabilizer-rank lower bounds for |T>^tensor n, since P(T)=3/4 and purity is
multiplicative. This shows both its external payoff and its substantial difficulty.
It does NOT imply polynomial extent or full rank-k tomography: greedy subtraction
can increase residual stabilizer rank, so the bounded-extent learner cannot be
invoked without another proof. Nor does a small Gram eigenvalue refute (P): the
reviewed bad in-span-frame family has an easy outside-span computational expansion.

The precise constructive attempt is to analyze cancellation of stabilizer Pauli
supports in an arbitrary k-term sum and either prove a dimension-independent
polynomial bound (with C>3.39 allowed) or exhibit explicit k_j-term states with
-log P(psi_j)/log k_j tending to infinity. Tensor products alone of the displayed
rank-two example only impose a fixed exponent; they do not achieve the latter.
Keep the endpoint at component discovery unless a separate full-learning bridge
is actually constructed. This is the single recommended mathematical question.

## 2. Canonically anchored cubic Gauss phase

**Native question.** Given a primary Eisenstein prime pi=a+b*rho of rational norm
p, use its fixed residue embedding to specify the cubic character chi, and output
the phase of sum_x chi(x)exp(2*pi*i*x/p) to prescribed constant accuracy. Both the
additive character and character embedding are native; the desired cube-root
branch is not advice. A complete poly(log p,1/epsilon) quantum phase algorithm is
the existing van Dam--Seroussi endpoint, not a proposed new mechanism.

**Potential operation and classical attack.** Ito's actual representative-product
formula reduces the remaining canonical branch to a finite-field product over
one representative of each order-three orbit. The geometric elliptic factor
already has an explicit evaluation; this is not a missing theta-function routine.
Classical exact Jacobi reconstruction determines the cube but leaves this anchor;
direct evaluation costs O(p), and the retained modular-factorial comparison is
not a general polylog-p algorithm. Changing the additive character rotates the
Gauss sum while preserving the Jacobi identities, killing a Jacobi-only selector.

An efficient native representative-product compiler would be a decisive classical
challenge to a genuine arithmetic phase endpoint. However, no new such operation
was found here. Real quadratic Hiary sums do not absorb an arbitrary cubic
multiplicative character. Repackaging the already recorded elliptic product would
repeat `CUBIC_GAUSS_ELLIPTIC_PRODUCT_ADMISSION.md`. Rank this below (P): a precise
product remains, but there is no fresh constructive attack to commission yet.

## 3. Expanded split-CSA output from a multiplication table

**Native question.** Given an expanded rational multiplication table for a central
simple algebra over a number field, promised split, compute an expanded explicit
matrix representation/minimal module in polynomial input BIT complexity under the
declared GRH/factoring quantum assumptions. The existing compact cochain endpoint
is not automatically this expanded output. Exact field arithmetic, maximal orders,
S-unit computation, map conversion, and every coordinate height must remain paid.

**Screened operation.** Replace scalar norm witnesses by the closed exponent-
mod-relative-degree/root compiler, then hope height multipliers telescope along a
field tower. Actual `amitsur.txt` Algorithm2, physical LF1103--1157, does NOT perform
such a norm tower. It decomposes F tensor2 and F tensor3 into field factors,
computes complete S-unit coordinate groups, and solves the simultaneous equation

    (psi_coord o Delta_Am^1 o phi_coord^-1)(a)=psi_coord(b).

Cocycle compatibility is built into this joint relation system. Reducing cochain
exponents modulo d only makes Delta(alpha0)/b a d-th power in the CODOMAIN. A
d-th root there need not be the coboundary of the needed domain cochain. The
scalar norm root lemma does not supply that lift. The source's Delta^0 gauge
freedom is real, but no efficient height-normalizing gauge has been derived.

Thus the proposed relative-degree ledger has no actual source operations on which
to telescope. A new compatible norm-tower reformulation or a cochain gauge-
shortening algorithm would itself be the hard new theorem. General number fields
do not come with a cheap solvable tower. Existing classical class-group/S-unit,
index-calculus and fixed quaternion norm methods remain the applicable baselines,
not a general expanded-output match. Do not reopen this direction from scalar
norm expansion alone. Its first decisive test is the simultaneous coboundary
equation above, before any height recurrence is claimed.

## Corpus and source gate

For all three directions, targeted `been-tried` preceded `baselines`; the new
rank/purity/Renyi query was also checked. Results were lexical leads, with no
matching baseline catalog entry for the purity question; this is NOT absence of
prior work. The actual retained sources needed for the proposed component endpoint
are already local; no additional PDF is required before its narrowly scoped attack:

- `sources/stabilizer_rank_priority/extent.txt`: arXiv2610.06819, Thm1.1, Cor1.6,
  Lemma3.4, conclusion. It states polynomial rank--extent as an open question.
- `sources/stabilizer_rank_priority/structure.txt`: arXiv2510.05890v2, Fact2.10,
  Thm2.11, copies-only self-correction; these are quantum-state inverse statements.
- `sources/stabilizer_extent/marton.txt`: arXiv2609.20771v1, Cor8.6 and8.11.
  This paper's extent is UNSQUARED; the rank--extent paper's xi is SQUARED.
- `sources/global_isotropy/amitsur.txt`: arXiv2307.00261v3, Algorithm2 andThm4.12.
  The Gauss comparison uses the already scoped cubic-Gauss topic and its retained
  van Dam--Seroussi, Ito and exact-Jacobi primary-source dispositions.

All `sources/` paths above are relative to `research/audits/`. The recommendation
is one constructive/refutation attempt at (P), not confirmation of a theorem,
automatic continuation of a neighboring line, or authorization to implement.
