# Attractive pairing: canonical Born sampling and three-way selection

Independent source/composition review, completed 2026-11-14; filename retains
the assigned pass date. No experiment, network/API, implementation or shared
edit. Physical source lines are counted with `split('\n')`.

## 1. Decision and exact theorem

The most useful concrete operation is a CLASSICAL fixed-particle Born sampler:
combine sector-energy curvature with a chemical-potential grid, then repair
and use the actual operator-loop sampler. This matches polynomial-resource
occupation readouts at inverse-polynomial TV accuracy. It does not simulate
coherent ground states, arbitrary observables, or excited Richardson states.

Input: N, M, rational eps_i and g>=0, and the explicitly given Hamiltonian

 H = sum_i eps_i n_i - g sum_(i<j)(sigma_i^+sigma_j^- + sigma_j^+sigma_i^-).

For 0<M<N and g>0, promise that its fixed-M spectral gap is at least kappa>0,
supplied as a lower bound. No Bethe roots, amplitudes, energies, chemical
potential, conditional-marginal oracle or prepared quantum state is supplied.
Given dyadic TV tolerance tau and failure tolerance eta, there is a bounded
randomized classical algorithm returning the fixed-M ground Born law within
TV tau, with abort probability at most eta. Its bit cost is polynomial in
N, the native rational bit length, J/kappa, 1/tau and log(1/eta), where
J=max(g,max eps_i-min eps_i). NO inverse-g or site-spacing resource is needed.
Reading arbitrary rational accuracy encodings is charged separately. M=0,N
are deterministic. For g=0 the gap promise makes the lowest-M subset unique.

The only spectral promise is the stated FINAL-sector gap; the source loop
proof is composed below with boundary, TV and finite-clock repairs. No uniform
internal gap or certificate of a false gap promise is asserted.

## 2. What stability actually proves

Actual Borcea--Branden--Liggett, `bcs_stability_selection/bbl.txt`, Theorem4.20
LF1480--1486 and Proposition5.1/proof LF1617--1648 prove preservation under
partial symmetrization and symmetric exclusion. Positive real variable
rescaling preserves upper-half-plane stability directly.

Let L=sum_(i<j)(T_ij-I), the symmetric exclusion generator, and
D=sum eps_i n_i. On M-subsets, L=Adj_M-M(N-M)I. Thus

 A=gL-D,       A_M=-H_M-gM(N-M)I.                         (1)

The product formula for exp(tA), alternating exclusion and exp(-tD),
preserves nonnegative real stability. Its fixed-M Perron vector is the ground
amplitude vector of H_M. Apply the evolution to a monomial and normalize its
coefficient sum; irreducibility for g>0 and coefficientwise closure show that
the nonzero limiting ground AMPLITUDE polynomial is real stable.

No coefficient-square closure follows. For v1=(1,0),v2=(1,1),v3=(0,1),
v4=(-1,1), det(sum z_i v_i v_i^T) is stable: its imaginary part is positive
definite when all Im z_i>0. Its six coefficients are 1 except c24=4.
After squaring them, the Hessian restricted to vectors (a,b,a,b) is represented
by [[1,2],[2,16]], which has two positive eigenvalues (determinant12, trace17).
The squared polynomial is therefore not Lorentzian. This is a generic stable
counterexample, NOT a native pairing-ground-state counterexample.

The exact ground Doob rates q(S,T)=g psi(T)/psi(S) have stationary law psi^2
and gap equal to the sector quantum gap. This identity supplies neither
computable ratios nor a gap bound. It is not an oracle-free algorithm.

Actual Wei2609.26802v2, `stability_semigroup.txt`, Theorems4.3/4.8
LF1107--1119,1246--1274 concern positive damping on the FULL disk-stable
coordinate box. A positive-degree homogeneous polynomial vanishes at the
origin and is not in that disk-stable cone. A chemical potential is scalar
within fixed M. These statements do not bound the internal fixed-M gap.
Theorem6.1 LF1689--1722 additionally fixes graph degree and J/mu, so its
classical clock cannot simply be applied to a growing complete graph.

## 3. Sector curvature, without ground-energy advice

For completeness, apply exp(tA) to product_i(1+z_i). Write c_m(t)>0 for the
sum of its degree-m coefficients and r_m=lambda_max(A_m). The diagonal
restriction is real-rooted with negative roots, so Newton gives

 (c_m/binom(N,m))^2 >=
 (c_(m-1)/binom(N,m-1)) (c_(m+1)/binom(N,m+1)).

The positive initial vectors have nonzero Perron overlap, hence
lim_(t->infty) log c_m(t)/t=r_m. Therefore 2r_m>=r_(m-1)+r_(m+1).
This is also exactly Wei Theorem7.1/proof LF2520--2575; it does not concern
an internal eigenvalue gap. By (1), with E_m=min spec H_m,

 E_(m+1)+E_(m-1)-2E_m >= 2g.                              (2)

Shift all eps by min eps and rescale H by J; these change neither the target
sector eigenvector nor the theorem. Henceforth 0<=eps_i,g<=1. A rational
K=N max_i eps_i+g N^2 bounds ||H||. Put d_m=E_m-E_(m-1).
Then |d_m|<=2K and d_(m+1)-d_m>=2g. The grid of spacing g/4 covering
[-2K-g,2K+g] has G=O(1+K/g) points. At least one point mu is at distance
>=g/2 from both ends of [d_M,d_(M+1)]. For this point, H-mu sum n_i has
its unique global ground state in sector M and every other sector starts
at least g/2 higher. No grid endpoint d_m is computed.

Choose rational beta >= (N+ceil(log2(64/tau)))/min(kappa,g/2).
At the good grid point the true grand-canonical Gibbs mass of sector M is
>=1-tau/64, in particular >=3/4. At EVERY mu, conditioning the true Gibbs
diagonal law on M gives exactly the same canonical law

 p_beta,M(S)=<S|exp(-beta H_M)|S>/Tr exp(-beta H_M).          (3)

Its TV distance from the ground Born law is <=2^N exp(-beta kappa)<=tau/64.
Thus samples, not unknown ground energies, can select a usable grid point.

## 4. Actual XY source and the two necessary repairs

Rayudu--Takahashi2509.21683v1, `xy_loops.txt`, Eq3 LF258--272 allows
arbitrary graphs and Z fields with |b_ij|<=a_ij, after rescaling. Our
H_mu has a=g/2,b=-g/2 and d_i=(mu-eps_i)/2, up to a scalar. Equations8--12
LF329--368 show that a closed path's distinguished slice has the diagonal
of (CC^dagger)^L/Tr (CC^dagger)^L. Lemma2 LF443--448 and proof
LF1258--1323 give polynomial closed-path acceptance. Theorem3 and actual
proof Eqs31--45 LF727--840 bound mixing from the all-zero closed path.

IMPORTANT: the proof has the factor c_min^-1, with
c_min=min_(ij){a_ij-b_ij,a_ij+b_ij}. It is ZERO at native number-conserving
XY. Also Theorem1 LF285--313 only states relative partition-function error;
that alone does not imply slice TV accuracy. Neither gap is silently imported.

Fix a desired single-sample error q<=min(1/64,tau/256). Replace H_mu by
H'_mu=H_mu-nu sum_(i<j) X_i X_j, with rational
nu=q^2/(1024 beta N^2). Then ||H'-H||<=nu N^2/2. For arbitrary Hermitian
A,B, their Gibbs states obey

 D(rho_A||rho_B)<=2 beta ||A-B||,
 TV(meas rho_A,meas rho_B)<=sqrt(beta ||A-B||).              (4)

The first inequality uses log rho and |log Z_A-log Z_B|<=beta||A-B||;
Pinsker gives the second. The perturbation therefore costs less than q/16.
Now a=g/2+nu,b=-g/2, so both off-diagonal types are strictly positive and
c_min=nu before normalization. Rescale by a known rational S=poly(K,N)
to meet Eq3, and replace beta by beta'=beta S. The inverse of the normalized
c_min is S/nu, polynomial in the declared parameters. No magnetization
conservation is claimed for the perturbed model; (4) pays that change.

Here is a direct TV repair for its Trotterization. Write H'/S=sum_l h_l,
take a rational b0>=max(1,sum_l||h_l||), and set
C=product_l(I-theta h_l), theta=beta'/(2L). Choose integer

 L >= max(8 beta' b0, 4096 beta'^2 b0^2/q^2, 16 N^2 beta'^2, 8).

For theta b0<=1/8, product expansion gives
C=I-theta H'/S+R with ||R||<=theta^2 b0^2. Consequently
||log(CC^dagger)+2theta H'/S||<=10 theta^2 b0^2.
The logarithm is the Hermitian principal logarithm: all factors are positive
definite and CC^dagger is within 1/2 of I. Thus the exact effective Hamiltonian
H_eff=-log(CC^dagger)/(2theta) differs from H'/S by at most5theta b0^2.
Applying (4) at beta' makes the Trotterized slice TV error less than q/16.
This logarithm is analysis only; the algorithm uses rational local factors.

Use all one-site factors, including identities. With T=M1+M2 and
P=M1+2M2, one has T<=P=2LN^2. The source parameter delta is theta above.
Its Eq47 encoding ambiguity is <=(1+delta^2)^T<=exp(T delta^2)<2 by our
extra L cap. This was the only further large-L condition hidden in the
epsilon-substituted formulas. No inverse c_min enters that encoding.

For clarity, the following independent weaker clock also pays the terse
four-insertion step behind source Eq34. Put U=CC^dagger. Every partial-period
product has norm<=2, and s_min(U)>=1/2. A cyclic trace with k<=4 fixed Pauli-X
insertions splits into k factors S_i U^(a_i) T_i, with sum a_i>=L-k.
Schatten Holder gives absolute trace <=4^k Tr U^(sum a_i)<=8^k Tr U^L.
The factor s_min(U)>=1/2 is essential for the last inequality: it explicitly
repairs source (C7)->(C8), which does not follow from s_max(U)<=2 alone.
There are at most P^2 head pairs. Since the extended measure weights C2 by
2/P, its ratio pi(C2)/pi(C0)<=128P; set rho0=(1+128P)^-1.

Source Eqs28/36 bound flow through z by O(pi(z)) / O(P*pi(z)) for z in
C0/C2. Even without Eq34's sharper summation, the four-insertion bound and
at most P^2 free head positions give O(P^2*pi(z)) for z in C2. Heat-bath
transition probabilities are >=c delta*c_min/P from C0 and >=c delta*c_min
from C2 (Eqs32/39); all constants are absolute. Thus base congestion is
O(P^2/(delta*c_min)). Rerouting C2--C2 flow via C0 costs at most128P, and
path lengths are O(P). A safe lazy-chain mixing cap to error xi is therefore

 O(P^4/(delta*c_min) * (NP+log(P/xi))).                    (5)

Source Eq36 yields the sharper P^3 version; (5) suffices independently.
The exponent of c_min^-1 is ONE: only the inverse transition probability.
The crude NP term follows by counting <=poly(P)*2^(N(T+2)) configurations:
local weights are <=3/2, and the all-zero path has weight >=2^-T.
All local weights/heat-bath ratios are rational with polynomial bit lengths.
With step cap t, round each transition to TV error <=xi/(2t), and run the
ideal mixing cap for xi/2. This uses O(log(t/xi)) additional coin bits.
Set xi=q*rho0/64. Conditioning the resulting law on C0 costs <=2xi/rho0;
its acceptance is >=rho0/2. At most ceil(2 rho0^-1 log(1/zeta)) fresh capped
runs suffice except with probability zeta. The two Gibbs/Trotter errors and
this conditioning give TV<q to the TRUE unperturbed Gibbs diagonal.

## 5. Finite grid selection, conditioning and final clock

For each mu use independent samples of the preceding finite sampler to
estimate its M-mass within 1/16 by Hoeffding, simultaneously over the G
grid points. O(log(G/zeta)) samples per point suffice. Choose any empirical
mass >=1/2. Except with probability zeta, a good point passes, and every
selected point has true M-mass >=1/2-1/16-q>=3/8.

Use fresh samples at that point and retain M. Their acceptance is >=1/4;
cap at O(log(1/zeta)) attempts. If distributions differ by TV q and the
true event mass is p, their conditional laws differ by at most2q/p.
Thus the fresh conditional output differs from (3) by at most16q/3.
Data-dependent choice causes no additional bias: (3) is identical at every
mu. All internal aborts, Hoeffding failure and circuit-free coin errors can
be allocated total probability <=min(eta,tau)/64. Combining these with
(3),(4) proves the stated TV/abort theorem. Rounding up all caps gives a
bounded BIT clock; no expected-only rejection or tiny-prefix oracle is used.

Run this small-g branch FIRST, removing both inverse-g and spacing promises.
Let v=||g Adj_M||=gM(N-M)<=gN^2/4. Weyl gives the diagonal gap
Delta>=kappa-2v. If gN^2<=tau*kappa/8 (take tau<=1/4), then Delta>0 and
the sorted product vector is unique. Projecting the ground eigen-equation
onto its orthogonal complement gives sin(angle)<=v/(Delta-v)
<=v/(kappa-3v)<tau/8. Its Born law is therefore already sufficiently close.
Otherwise 1/g<8N^2/(tau*kappa), so ALL grid, beta, c_min and mixing costs
above are polynomial in the theorem's final parameters. This includes g=0.
The elementary repair was suggested by the completed paid review; its Weyl
and projection inequalities are independently checked here.

## 6. External-value comparison and next action

**Attractive pairing.** Native levels/coupling and particle number describe
a physical paired-fermion ground state. The proved classical construction
matches occupation readouts under a final gap promise weaker than a usual
adiabatic path-gap promise. Doob ratios/gap are not free operations; coherent
ground preparation remains distinct. A coefficient-square or finite-gap
test would not supersede this source-backed readout comparator.

**Periodic conductivity.** `PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`
specifies a Boolean material circuit on a 2^n torus, fixed contrast, and
additive-epsilon effective conductivity. The quantum clock is poly(B,n,1/epsilon);
the classical heat estimator is polynomial at fixed epsilon, quasipolynomial
at inverse-polynomial epsilon. A cancellation-preserving Neumann estimator
with a joint-polynomial second moment would change the endpoint, but none
was supplied. Prior independent-path failures are not lower bounds.

**Projected Slater with ancillas.** `PROJECTED_SLATER_GAUSSIAN_FEEDFORWARD.md`
specifies rational 2s-by-s isometry V and one occupied mode per pair; output
weights are |det V_S|^2/Z. State loading is polynomial but postselection costs
1/Z (amplification 1/sqrt Z). Its same-mode feedback falsifier does NOT cover
ancillary Gaussian channels. Nevertheless no correct branch-reset instrument
preserving this determinant law with normalization-independent success is
supplied. Its first gate is the opposite-angle four-mode input. General
partition-DPP algorithms and the broader quantum sampler remain open.

Select the pairing CLASSICAL comparison as the one concrete action: it has
a source-backed sampler and a new exact sector-selection composition, and
can dispose of an apparent physical advantage without inventing one. Do not
start a quantum implementation or claim novelty, hardness, a uniform pairing
gap, a general Born log-concavity theorem, or a coherent classical match.
