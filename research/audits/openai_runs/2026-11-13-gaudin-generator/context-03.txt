# Two-cluster Richardson--Gaudin joint-gap test

2026-11-07. CLOSED written counterfamily, with independent core/source
reviews and parent verification. No asymptotic conclusion is taken from
the numerical search: finite-spacing fusion and min-max prove the bound.

## Selection, native contract and prior work

Start STATE/TRAPS; latest Binary Fock Kerr pass CLOSED. The preceding pass
was progress: reviewed classical sampler, exact interference controls and
updated authoritative state. Independent comparison covered sparse constant
residue maps (no new paid map), binary-spin recoupling (actual Hahn theorem
linear in numerical block size), full local Kummer halving (actual-point
conditioning still unpaid), and Kronecker weak projection (multiplicity1 can
have inverse Catalan-squared acceptance). None supplied a new endpoint.
The chosen question is the physical SAME-sector Gaudin joint separation:
a polynomial bound directly completes the existing conditional native
all-eigenstate preparation, rather than adding a filter or backend.

Native inputs and quantum mechanism remain GAUDIN_JOINT_CHARGE_TRAVERSAL.md:
Q_i=n_i+(g/2)sum_(j!=i)(P_ij-I)/(eps_i-eps_j), distinct real rational sites,
g>=0, fixed excitation count, ordinary initial bit label, no root/state
advice. Joint-charge randomization already pays conditional preparation in
poly(N,1/epsilon,1/kappa,coefficient norms); no full native algorithm until
an all-path inverse-polynomial gap is established. Expected upside is
access to arbitrary interacting eigenstates. Classical comparisons are
explicit diagonalization, compressed symmetry sectors, Bethe arithmetic,
and tensor-network/sampling under their actual hypotheses. No classical
hardness, novelty or separation is claimed.

Corpus been-tried/baselines preceded the test. Actual accepted Lutz etal
2503.21741v3 (Quantum10,2032,2026), retained under
 audits/sources/gaudin_gap_geometry/lutz_v3.pdf/.txt and source.json,
text270--395 Eq12/13 and sections7--9 STILL leaves finite-g SAME-sector gap
and efficient classical root tracking open. It discusses the proposed1/N
lower bound based on numerical families; the original v2 scope was not a
proof. No statement below attacks its proved weak/strong-coupling limits.

One bounded classical N6,M3 adversarial search, <=4096 evaluations, found
no1/N violation; minimum0.3531733>1/6 near two3-spin clusters. Its4015
calls and residuals are frozen in audits/controls/gaudin_adversarial_gap/.
This is FINITE_NONFALSIFICATION_ONLY. The cluster geometry suggested the
following analytic family; no size sweep or repeated optimizer is queued.

## 1. Native fusion with finite, distinct rational sites

Let N=2n,n>=2, total excitation M=n. Cluster sites are
 eps_Ai=delta*i, eps_Bi=1+delta*i, i=0,...,n-1,
 g=1/(2n), delta=n^(-8).
All sites are distinct; inverse spacing n^8 and charge norms are polynomial
inN, and the complete native input has polynomial bitlength. This is not a
coincident-site oracle or a supplied large-spin representation.

Let P project onto the fully symmetric spinS=n/2 representation in EACH
cluster, restricted to totalSz0. Its dimension is n+1. The exact commuting
separator H_sep=(-2delta/g)sum_i x_i Q_i (x_Ai=x_Bi=i) equals
 K_A+K_B+E, where K_C=sum_(i<j inC)(I-P_ij).
K_C=n(n+2)/4-S_C^2 has kernel the symmetric cluster and next eigenvalue n.
The exact error is
 E=-(2delta/g)sum_i i(n_Ai+n_Bi)
   +delta sum_(i,j)(i-j)/(1-delta(i-j))*(P_Ai,Bj-I).
For delta(n-1)<=1/2,
 ||E||<=delta*C_E,
 C_E=2n(n-1)/g+(4/3)n(n²-1)<=6n³.
If delta*C_E<=n/4, the isolated low spectral projector P_delta of H_sep
has the same dimension as P and commutes with ALL Q_i. A direct-rotation
unitary U taking P to P_delta can satisfy ||U-I||<=4delta*C_E/n.
The dimension-free projector estimate is
 ||P_delta-P||<=delta*C_E/(n-delta*C_E)<=2delta*C_E/n;
it follows by solving the separated-spectrum Sylvester equation for
(I-P)P_delta. The core review spells out the integral bound. These are
proof-only operators, not supplied algorithmic state/projector access.

Write Q_i=A_i/delta+B_i(delta), with A_iP=PA_i=0,
 ||A_i||<=g(n-1), ||B_i(0)||<=1+gn,
 ||B_i(delta)-B_i(0)||<=g n(n-1)delta.
The singular term compresses as
 P U^* A_i U P =P(U-I)^* A_i(U-I)P,
so it contributes O(delta), not O(1). Hence onP,
 ||P U^*Q_i U P-PB_i(0)P||<= e=delta*C_Q,
 C_Q=16g(n-1)C_E²/n²+g n(n-1)+8(1+gn)C_E/n<=400n⁴.
These are dimension-independent operator bounds, not finite diagonalization.

The fused operators are
 F_Ai=c_A+H/n, F_Bi=c_B-H/n,
 c_A=1/2+gn/4, c_B=1/2-gn/4,
 H=S_A^z-g S_A dot S_B, S_A^z+S_B^z=0.
Thus fused label distance² is2(Delta h)²/n. The compressed actual charges
commute exactly. Order a simultaneous basis by the A0 charge; Weyl bounds
and ||Q_Ai-Q_A0||<=2e, ||Q_Bi+Q_A0-I||<=2e on the compressed space give
for the two corresponding fused eigenvalues h0<h1:
 physical squared joint distance <= (2/n)*(h1-h0+6n e)².       (1)
A positive fused gap larger than2n e guarantees distinct anchor eigenvalues.
No exponential-dimensional eigenvector has to be supplied or computed.

## 2. Exact finite compressed falsifier

At n64,N128,g1/128, H in m=-32,...,32 has diagonal m+g*m² and adjacent
entry -g/2*(S(S+1)-m(m+1)). These entries are rational; it is a65x65 matrix.
Exact QQ Sturm recurrence in fused_control.py/fused_result.json proves
 h0 in(-24173/1000,-6043/250), h1 in(-2988/125,-23903/1000).
Endpoint eigenvalue counts are(0,1) and(1,2). Therefore
 67/250<h1-h0<27/100<1/2.
With delta=64^(-8)=2^(-48), e<=25/1048576 and6n e<=75/8192<1/100.
The positive gap lower bound guarantees two distinct anchor eigenvalues.
Combining the independently checked fusion proof and frozen Sturm endpoints,
 physical distance² <(1/32)*(28/100)²=49/20000<1/400<1/128.
native_bound.py/native_bound.json additionally records exact rational
arithmetic giving the sharper upper3268523241/1342177280000. This is a
physical native certificate by theorem plus exact arithmetic; the compressed
result alone is NOT one. No full128-spin matrix is constructed.

## 3. All-family variational upper bound, not a fitted exponent

At g1/(2n), put k=m+n/2 in{0,...,n} and
 a_k=(n-k)(k+1)/(4n), a_-1=a_n=0.
An exact entrywise identity is
 H+3n/8+1/4 = L_a +diag(k²/n),
where L_a is the weighted-path Laplacian with edge weightsa_k. Both terms
are positive semidefinite, so the shifted ground energy is nonnegative.

For n>=27, ell=floor(n^(1/3)), choose two triangular tents of peak1 on
[0,2ell] and[3ell,5ell]. Each has squared norm(2ell²+1)/(3ell)>=2ell/3;
its2ell nonzero edge differences have absolute value1/ell. Since a_k<=5ell/4
on their support, each Laplacian Rayleigh quotient<=15/(4ell). The potential
is<=25ell²/n. Supports are disjoint and not adjacent, so cross quadratic
forms vanish. The min-max principle gives
 h1-h0 <=15/(4ell)+25ell²/n <=33n^(-1/3).
Since e<=400n^(-4) and6n e<=2400n^(-3)<=n^(-1/3) for n>=27,
equation(1) yields
 min_(v!=w inM=n) ||q_v-q_w||² <=2312 n^(-5/3).              (2)
This refutes a UNIFORM Omega(1/N) lower bound across all native rational
site families. It does NOT prove a matching asymptotic lower bound, a
superpolynomially small gap, failure for equally spaced sites, a general
no-go for preparation, or any speedup. The fused problem is classically
polynomial dimension. This does not assert classical efficient simulation
of arbitrary states in the perturbed native sector. For (2), the two actual
joint states are orthogonal even without an individual gap perturbation
bound; any exact joint-label degeneracy would itself violate the required
rank-one separation premise. No starting bit labels need to be computed for
this existential upper bound on the minimum.

## 4. Prior physical mechanism and source scope

The critical two-level BCS mechanism is PRIOR ART. Actual Dusuel--Vidal,
cond-mat/0501282v2, retained as two_level_bcs.pdf/.txt with manifest in the
same source directory, Eq3 and TableI/Eq14--15, gives on totalSz0 and maximal
cluster spin, at h=1 and after exchanging the two level labels,
 H_BCS=2H-(n+2)I/4, Delta_BCS=2(h1-h0).
Thus the fused squared joint distance is Delta_BCS²/N. Its known critical
finite-size analysis predicts Delta_BCS~N^-1/3; that is not imported as an
all-n certified theorem or a matching lower bound. Our elementary min-max
upper bound and finite-distinct-site join supply the stated quantifiers.
No novelty claim is made for either the mechanism or this deduction.

Lutzv3 concerns numerical central-spin/equally-spaced/random families and
explicitly leaves the general SAME-sector gap open. This counterfamily
refutes the unrestricted uniform1/N extension, not a proved paper theorem
or those three specific families. Its weak-coupling sufficient scale is
minspacing/N²=Theta(n^-10); g=1/(2n) is outside it. Its strong-coupling limit
holds at fixed N/sites. Neither proved limit is contradicted. The paper's
magnetization is sum sigma_z; our M=n is excitation count and totalSz0.

## 5. Review, controls and Claude disposition

Parent read and checked both CLOSED reviews:
 audits/reviews/2026-11-07-gaudin-fusion-core.md;
 audits/reviews/2026-11-07-gaudin-fusion-source.md.
The core independently checks the singular-term cancellation, commuting
compression, anchor transfer and all-family tents, including delta=n^-8.
The source review checks actual accepted text and the exact BCS normalization.
It does not replace the separate mathematical proof. Parent read all three
new control scripts: boundedN6 numerical attack, exact65-dimensional Sturm,
and exact native-bound arithmetic. Frozen result gates retain their local
scope; no finite control is relabeled an asymptotic theorem.

One distinct narrow Claude Opus/high16384 fusion review was attempted at
 audits/claude_runs/2026-11-07-gaudin-fusion.
It terminated empty_response/refusal, input3922/output5894, reported usage
estimateUSD0.133568. No findings, no completed review and no retry. Its
historical context uses the valid but weaker delta=n^-16; preserve it exactly.
This result relies on the parent/core proof, not an external approval label.
Scoped milestone: audits/controls/gaudin_adversarial_gap/checkpoint.json.

## Next scientific question

The algorithm needs some weaker uniform inverse-polynomial all-path joint
gap under paid native conditioning; this pass does not decide it. Any next
candidate bound must first survive the analytic critical family above.
Independently compare high-upside directions before returning. A re-entry
needs a new all-parameter inequality or explicit superpolynomial counterfamily,
not another finite gap curve, nearby critical variant, filter or backend.
Next command: read STATE/TRAPS, corpus been-tried for that exact proposed
operation, then primary literature and classical baselines. Acceptance is
a paid proof/counterfamily that changes the end-to-end algorithm decision.
