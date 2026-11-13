# Native multi-community weak recovery

2026-11-13. Selected constructive candidate; full recovery theorem OPEN.
STATE/TRAPS and corpus been-tried/baselines preceded the primary-source
comparison. Rank-purity is parked. The single question is whether the
existing native Kikuchi detector can output one correlated labeling, with
all source, classical baseline and finite-clock costs paid.

## Problem, mechanism and honest resource target

Input ONE explicit array of independent conditional Bernoulli p-hyperedges,
fixed even p=2d>=4, fixed k>=3, q=1/4, known rational epsilon. Labels x_i
are IID uniform[k], and edge means are q+epsilon*f_x(E), where
f_x(E)=sum_a product_(i in E)(1[x_i=a]-1/k). No labels, gauge, useful
vector/projector, independent planted graph, QRAM or preparation oracle.
Choose growing polylogarithmic ell, divisible by p for the existing quantum
compiler; ell=o(sqrt n). Let D=binom(ell,d)binom(n-ell,d).
Target signal epsilon²D>=C_(p,k)*ell. Known stronger signal may be
attenuated first to a known constant multiple of this frontier using fresh
null bits; the cloning analysis needs this near-threshold effective signal.
Output ONE z in[k]^n with max_permutation n^-1 count[z_i=pi(x_i)]>=1/k+c_pk,
with probability1-o(1) over input and internal randomness.

First prove the CLASSICAL endpoint in n^(ell+O_p(1))*poly(inputbits).
Only then compose quantum accepted-band preparation, one-particle tomography,
rounding and validation. Expected charged quantum upper bound is the already
compiled n^(ell/4)*exp(O_pk(ell logell))*poly(n^p,inputbits), with the
existing loglog terms outside ell~logn retained if needed. This is a target,
not a new speedup, best-classical dominance, practicality or Shor-level claim.

Strong baselines: existing classical native log-free detector; sharp Boolean
Kikuchi recovery; HCE/color-coded noisy-XOR algorithms; ordinary clustering
at stronger signal. The lower marginals of this model vanish, so ordinary
pairwise SBM is not an automatic comparator. Exact source contracts stay
attached. No low-degree or LCDF inference becomes general hardness.

## Checked source boundary

Full selection audits/reviews/2026-11-13-post-purity-selection.md compares
native recovery, short-path optimization and dissipative PDE output. The
latter two lack a new paid operation. Actual 2510.08494v1 Definition2 gives
this multi-color signal; conclusion LF649-652 leaves label recovery open
in that version. Its original guiding-source proof is NOT imported: use
the repository's independently checked NATIVE_COMMUNITY_SOURCE_REPAIR.md.

Actual 2607.29672v1 Section12.4 already gives accepted-band one-particle
mass, tomography and rounding for BOOLEAN noisy XOR. Section13's transfer
reveals a random literal vector and extracts its XOR channels. Our input is
one Bernoulli edge bit with multi-color means; it does not supply those
literals. These are prior techniques, not a direct HSBM theorem.

Actual Mao2604.10457v1 was fetched to audits/sources/2026-11-13-community-
recovery/; Definition1.3 LF220-254 specifies random Boolean parity samples
with independent sign noise. It is not an automatic multi-color native
recovery theorem. No literature-wide novelty claim follows. All current
arXiv versions checked Nov13. HCE2610.40941 remains a distinct strong
classical method; prior native adaptation paid detection, not recovery.

## Parent operation: energy pays one-particle mass

All following label objects are analysis only. Set w_a(i)=1[x_i=a]-1/k,
W_a=w_a*w_a^T, L=span{w_a}, and Lambda=binom(ell,d)*n^d. On ordered slots,

 B=sum_(J subset[ell],|J|=d) sum_a tensor_(j in J) W_a^(j).

Since W_a<=n*P_L and different-slot projections commute,

 tensor_(j in J) W_a^(j) <= n^d/d * sum_(j in J) P_L^(j),
 B <= k*Lambda/ell * sum_j P_L^(j).

The existing exact native certificate supplies, on collision-free tuples,
||Pi B Pi-K_x||<=k*d²*binom(ell,d)*n^(d-1)=O_pk(Lambda/n).
For a unit collision-free state of positive observed Rayleigh quotient,
subtract the already paid uniform centered-noise bound and this error. If
its signal energy is >=a_pk*Lambda, the one-particle average rho satisfies
Tr(P_L rho)>=a_pk/k. The same statement is linear for mixed states and
applies to every accepted-band state, with small trace error paid. It does
NOT require a full k-block gap, a special top eigenvector or known labels.
All factorials/set-versus-ordered scaling require independent checking.

A classical unit high-Rayleigh vector should come from O(log N) exact
integer powers, N=binom(n,ell), with Rademacher starts, as in the detector.
Check its Rayleigh quotient directly; repeat logarithmically with a fixed
cap. This avoids constructing a full projector. For set amplitudes v,

 rho_ij=(1/ell) sum_(|T|=ell-1,T disjoint{i,j})
                     v_(T union{i}) conj(v_(T union{j})),

with the analogous diagonal sum. It costs n^(ell+O(1)), trace is one.
Quantumly use the average over ordered slots, or the exact set deletion
isometry. No full lifted-space tomography is needed.

## Parent rounding operation, conditional only on the mass bound

Take real part R=Re(rho), a real PSD trace-one matrix. On the IID balance
high-probability event n_a>=n/(2k), the nonzero eigenvalues of sum_a W_a
are at least n/(2k): on 1^perp in color space, W^T W has quadratic form
sum_a n_a*u_a². The constant mass Tr(P_L R)>=eta implies a leading constant-
dimensional eigenspace V with Tr(P_L P_V)>=eta/2, since R<=P_V+alpha I
for alpha<=eta/(2(k-1)). Thus some w_a has ||P_V w_a||>=c*sqrt(n).
Operator-norm approximation of R and approximate diagonalization suffice;
no eigenvalue-gap promise is allowed. A constant-radius net of V includes
a real unit v with <v,w_a>>=a*sqrt(n), after choosing its sign.

Let L0=2/a and g_i=clip(sqrt(n)*v_i,[-L0,L0]). The removed correlation is
at most n/L0 because sum_i (sqrt(n)*v_i)²=n and |w_a(i)|<=1. Hence
n^-1 sum_i g_i*w_a(i)>=a/2. Round independently: output label1 with
probability h_i=(1+g_i/L0)/2, otherwise a uniform label2..k. For the
permutation sending1 to a, expected agreement is

 (1-n_a/n)/(k-1) + k/(k-1) * n^-1 sum_i h_i*w_a(i).

IID balance and the positive correlation give 1/k+Omega_pk(1).
Hoeffding makes the actual agreement hold with high probability. Do this
for every constant-net vector, creating a finite candidate list. The true
a and a good net index are never queried. Net size/constants depend only
on fixed p,k and the mass margin; output is not yet one labeling.

## Parent native validation and source obligation

For each edge, route the original Y to one of three outputs with weights
(1-2t,t,t), t=1/ceil(log2 n); fill the other two with independent Bern(q)
null bits. The marginals have signal strengths epsilon*(1-2t),epsilon*t,
epsilon*t. Need an exact per-edge chi-square proof giving <=C_q delta^4*t²
against their independent product, delta=epsilon*f_x(E), |delta|<=q/2.
Then total conditional-and-mixed-label TV is
O(sqrt(exp(C*M*beta^4*t²)-1))=o(1) at the effective frontier. Freeze these
three datasets once; transfer TV through the WHOLE algorithm once, not
per quantum call. Fixed coins and original-input attenuation are charged.

Candidates depend only on matrix/guide arrays and internal randomness.
Validate z on the third array with S_z=sum_E f_z(E)*(Y_validation(E)-q).
For C_ab=n^-1 sum_i(1[z_i=a]-1/k)(1[x_i=b]-1/k), the target exact expansion is

 E S_z=epsilon_v*n^p/p!*sum_ab C_ab^p+O_pk(epsilon_v*n^(p-1)),
 Var(S_z)<=O_pk(n^p).

The error is collision removal from ordered products; p is even. At this
frontier epsilon_v²*n^p grows polynomially in n, so a constant-size list
can be validated with failure o(1). A good candidate gives a positive
constant sum C_ab^p. Conversely a high score forces a constant positive
entry of C, because its rows/columns sum to zero. Averaging permutations
conditioned to include that entry gives assignment advantage at least
k/(k-1)*max_positive C_ab. Exactly sum_a C_(a,pi(a))=agreement_pi-1/k.
Thus choose the largest observed score and output ONE labeling, with no
latent-label check or independent-graph advice. All claims in this section
are under independent derivation; no theorem is promoted yet.

## Decisive falsifiers and next experiment

First test the operator comparison on the exact native mean and every
high-energy state; one counterexample with vanishing planted one-body mass
kills the operation. Then attack clone independence and candidate validation
on the same observed graph, including imbalance, huge-signal attenuation,
constant factors, fixed precision and all-branch clocks. Classical recovery
must close before quantum composition. No new code/sweep is needed for
already proved collision/noise identities. Pending independent proofs:
community-recovery-mass.md and community-recovery-validation.md. Paid calls
will target only a surviving concrete obligation, not a broad open conjecture.
